"""
Main email classification agent
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime

from anthropic import Anthropic
from openai import OpenAI

from .models import (
    EmailClassification,
    EmailCategory,
    ClassificationResult,
    FeedbackEntry
)
from .config import AgentConfig
from .knowledge_base import KnowledgeBase
from .tools import ToolRegistry, default_registry


class EmailClassificationAgent:
    """
    Email Classification Agent for Penta Fine Ingredients Customer Service

    This agent uses LLMs (Anthropic Claude or OpenAI GPT) to classify incoming
    customer service emails, can call external functions for data lookup,
    learns from feedback, and maintains a knowledge base.
    """

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        tool_registry: Optional[ToolRegistry] = None,
        knowledge_base: Optional[KnowledgeBase] = None
    ):
        """
        Initialize the email classification agent

        Args:
            config: Agent configuration
            tool_registry: Tool registry for function calling
            knowledge_base: Knowledge base instance
        """
        self.config = config or AgentConfig()
        self.config.validate_keys()

        # Initialize LLM client based on provider
        if self.config.llm_provider == "anthropic":
            self.anthropic_client = Anthropic(api_key=self.config.anthropic_api_key)
            self.openai_client = None
        else:
            self.openai_client = OpenAI(api_key=self.config.openai_api_key)
            self.anthropic_client = None

        # Initialize tool registry and knowledge base
        self.tool_registry = tool_registry or default_registry
        self.knowledge_base = knowledge_base or KnowledgeBase(
            persist_directory=self.config.knowledge_base_path
        )

    def _get_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate the system prompt for the LLM

        Args:
            context: Additional context from knowledge base

        Returns:
            System prompt string
        """
        base_prompt = f"""You are an expert email classification agent for Penta Fine Ingredients, a company specializing in fine chemical ingredients.

Your job is to classify incoming customer service emails into one of the following categories:

{self._get_categories_description()}

For each email, you must:
1. Analyze the email subject and body carefully
2. Determine the primary intent of the email
3. Extract any relevant entities (product names, order numbers, quantities, etc.)
4. Assign a confidence score (0.0 to 1.0)
5. Identify any secondary categories if applicable
6. Suggest a priority level (low, normal, high, urgent)
7. Provide a recommended action or routing

Consider:
- Product inquiries about chemical ingredients, specifications, or applications
- Quote requests may include specific quantities or technical requirements
- Regulatory compliance questions are common in the chemical industry
- Technical support may involve formulation questions or usage guidance

Be thorough in your analysis and provide clear reasoning for your classification.
"""

        # Add context from knowledge base if available
        if context:
            context_text = self._format_context(context)
            if context_text:
                base_prompt += f"\n\nRelevant Context:\n{context_text}"

        return base_prompt

    def _get_categories_description(self) -> str:
        """Get formatted description of all categories"""
        descriptions = []
        for category in EmailCategory:
            desc = EmailCategory.get_description(category)
            descriptions.append(f"- {category.value}: {desc}")
        return "\n".join(descriptions)

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context from knowledge base for the prompt"""
        parts = []

        if context.get("similar_queries"):
            parts.append("Similar past queries:")
            for item in context["similar_queries"][:2]:
                meta = item.get("metadata", {})
                parts.append(f"  - Category: {meta.get('classification')} (confidence: {meta.get('confidence', 0):.2f})")

        if context.get("relevant_products"):
            parts.append("\nRelevant products:")
            for item in context["relevant_products"][:3]:
                meta = item.get("metadata", {})
                parts.append(f"  - {meta.get('name')}")

        return "\n".join(parts) if parts else ""

    def _create_classification_prompt(self, email: EmailClassification) -> str:
        """Create the user prompt for classification"""
        return f"""Please classify this customer service email:

Subject: {email.subject}

Body:
{email.body}

{f"Sender: {email.sender}" if email.sender else ""}

Provide your response in the following JSON format:
{{
    "primary_category": "category_name",
    "confidence": 0.95,
    "secondary_categories": ["other_category"],
    "reasoning": "Detailed explanation of why you chose this classification",
    "extracted_entities": {{
        "product_names": ["Product A", "Product B"],
        "order_number": "12345",
        "quantity": "500 kg",
        "other_info": "any other relevant extracted information"
    }},
    "recommended_action": "Route to sales team for quote preparation",
    "priority": "normal"
}}
"""

    def classify_with_anthropic(
        self,
        email: EmailClassification,
        context: Optional[Dict[str, Any]] = None
    ) -> ClassificationResult:
        """
        Classify email using Anthropic Claude

        Args:
            email: Email to classify
            context: Additional context from knowledge base

        Returns:
            Classification result
        """
        system_prompt = self._get_system_prompt(context)
        user_prompt = self._create_classification_prompt(email)

        # Get tool definitions if available
        tools = self.tool_registry.get_tool_definitions_for_anthropic()

        # Call Anthropic API
        response = self.anthropic_client.messages.create(
            model=self.config.anthropic_model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            tools=tools if tools else None
        )

        # Handle tool calls if present
        tool_results = []
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = self.tool_registry.call_tool(
                        block.name,
                        block.input
                    )
                    tool_results.append({
                        "tool": block.name,
                        "result": tool_result
                    })

            # If tools were called, get final response
            if tool_results:
                messages = [
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(tool_results)
                            }
                            for block in response.content if block.type == "tool_use"
                        ]
                    }
                ]
                response = self.anthropic_client.messages.create(
                    model=self.config.anthropic_model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    system=system_prompt,
                    messages=messages,
                    tools=tools
                )

        # Extract text response
        text_content = ""
        for block in response.content:
            if block.type == "text":
                text_content += block.text

        return self._parse_classification_response(text_content, email)

    def classify_with_openai(
        self,
        email: EmailClassification,
        context: Optional[Dict[str, Any]] = None
    ) -> ClassificationResult:
        """
        Classify email using OpenAI GPT

        Args:
            email: Email to classify
            context: Additional context from knowledge base

        Returns:
            Classification result
        """
        system_prompt = self._get_system_prompt(context)
        user_prompt = self._create_classification_prompt(email)

        # Get tool definitions if available
        tools = self.tool_registry.get_tool_definitions_for_openai()

        # Call OpenAI API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.openai_client.chat.completions.create(
            model=self.config.openai_model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            tools=tools if tools else None
        )

        # Handle tool calls if present
        message = response.choices[0].message
        if message.tool_calls:
            tool_results = []
            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments)
                tool_result = self.tool_registry.call_tool(
                    tool_call.function.name,
                    arguments
                )
                tool_results.append({
                    "tool": tool_call.function.name,
                    "result": tool_result
                })

            # Add tool results to messages and get final response
            messages.append(message)
            messages.append({
                "role": "tool",
                "content": json.dumps(tool_results),
                "tool_call_id": message.tool_calls[0].id
            })

            response = self.openai_client.chat.completions.create(
                model=self.config.openai_model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

        text_content = response.choices[0].message.content
        return self._parse_classification_response(text_content, email)

    def _parse_classification_response(
        self,
        response_text: str,
        email: EmailClassification
    ) -> ClassificationResult:
        """
        Parse LLM response into ClassificationResult

        Args:
            response_text: LLM response text
            email: Original email

        Returns:
            ClassificationResult
        """
        try:
            # Try to extract JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            data = json.loads(response_text)

            # Parse the response
            primary_category = EmailCategory(data["primary_category"])
            confidence = float(data.get("confidence", 0.5))
            secondary_categories = [
                EmailCategory(cat) for cat in data.get("secondary_categories", [])
            ]

            result = ClassificationResult(
                primary_category=primary_category,
                confidence=confidence,
                secondary_categories=secondary_categories,
                reasoning=data.get("reasoning", ""),
                extracted_entities=data.get("extracted_entities", {}),
                recommended_action=data.get("recommended_action", ""),
                priority=data.get("priority", "normal")
            )

            return result

        except Exception as e:
            # Fallback to general inquiry if parsing fails
            return ClassificationResult(
                primary_category=EmailCategory.GENERAL_INQUIRY,
                confidence=0.3,
                secondary_categories=[],
                reasoning=f"Failed to parse classification response: {str(e)}",
                extracted_entities={},
                recommended_action="Manual review required",
                priority="normal"
            )

    def classify(self, email: EmailClassification) -> ClassificationResult:
        """
        Classify an email using the configured LLM provider

        Args:
            email: Email to classify

        Returns:
            Classification result
        """
        # Get context from knowledge base
        email_content = f"{email.subject} {email.body}"
        context = self.knowledge_base.get_context_for_classification(email_content)

        # Classify using appropriate provider
        if self.config.llm_provider == "anthropic":
            result = self.classify_with_anthropic(email, context)
        else:
            result = self.classify_with_openai(email, context)

        # Store in history if learning is enabled
        if self.config.enable_learning:
            email_id = self._generate_email_id(email)
            self.knowledge_base.add_classification_history(
                email_id=email_id,
                email_content=email_content,
                classification=result.primary_category.value,
                confidence=result.confidence,
                metadata={
                    "subject": email.subject,
                    "sender": email.sender,
                    "extracted_entities": result.extracted_entities
                }
            )

        return result

    def provide_feedback(
        self,
        email: EmailClassification,
        original_classification: EmailCategory,
        correct_classification: EmailCategory,
        confidence: float,
        notes: Optional[str] = None
    ):
        """
        Provide feedback on a classification for learning

        Args:
            email: The original email
            original_classification: What the agent classified it as
            correct_classification: What it should have been classified as
            confidence: Original confidence score
            notes: Additional notes
        """
        if not self.config.enable_learning:
            return

        email_id = self._generate_email_id(email)
        email_content = f"{email.subject} {email.body}"

        # Create feedback entry
        feedback = FeedbackEntry(
            email_id=email_id,
            original_classification=original_classification,
            correct_classification=correct_classification,
            confidence=confidence,
            email_content=email_content,
            notes=notes
        )

        # Save feedback to file
        self._save_feedback(feedback)

        # Update knowledge base with corrected classification
        self.knowledge_base.add_classification_history(
            email_id=f"{email_id}_corrected",
            email_content=email_content,
            classification=correct_classification.value,
            confidence=1.0,  # High confidence for corrected classifications
            was_correct=True,
            metadata={
                "original_classification": original_classification.value,
                "feedback_notes": notes
            }
        )

        # Add to common queries if significantly different
        if original_classification != correct_classification:
            self.knowledge_base.add_common_query(
                query_id=f"feedback_{email_id}",
                query_text=email_content,
                classification=correct_classification.value,
                confidence=1.0,
                metadata={"source": "feedback"}
            )

    def _generate_email_id(self, email: EmailClassification) -> str:
        """Generate unique ID for an email"""
        content = f"{email.subject}{email.body}{email.sender}{email.received_at}"
        return hashlib.md5(content.encode()).hexdigest()

    def _save_feedback(self, feedback: FeedbackEntry):
        """Save feedback to feedback log file"""
        import os

        feedback_path = self.config.feedback_log_path
        os.makedirs(os.path.dirname(feedback_path), exist_ok=True)

        # Load existing feedback
        feedbacks = []
        if os.path.exists(feedback_path):
            with open(feedback_path, 'r') as f:
                try:
                    feedbacks = json.load(f)
                except json.JSONDecodeError:
                    feedbacks = []

        # Add new feedback
        feedbacks.append(feedback.model_dump())

        # Save back
        with open(feedback_path, 'w') as f:
            json.dump(feedbacks, f, indent=2, default=str)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the agent and knowledge base"""
        kb_stats = self.knowledge_base.get_stats()
        return {
            "llm_provider": self.config.llm_provider,
            "model": (self.config.anthropic_model if self.config.llm_provider == "anthropic"
                     else self.config.openai_model),
            "knowledge_base": kb_stats,
            "tools_registered": self.tool_registry.get_tool_count(),
            "learning_enabled": self.config.enable_learning
        }
