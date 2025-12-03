"""
Configuration management for the email classification agent
"""

import os
from typing import Optional, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class AgentConfig(BaseModel):
    """Configuration for the Email Classification Agent"""

    # LLM Provider Settings
    llm_provider: Literal["anthropic", "openai"] = Field(
        default=os.getenv("LLM_PROVIDER", "anthropic"),
        description="LLM provider to use"
    )
    anthropic_api_key: Optional[str] = Field(
        default=os.getenv("ANTHROPIC_API_KEY"),
        description="Anthropic API key"
    )
    openai_api_key: Optional[str] = Field(
        default=os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key"
    )
    anthropic_model: str = Field(
        default=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"),
        description="Anthropic model to use"
    )
    openai_model: str = Field(
        default=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
        description="OpenAI model to use"
    )

    # Knowledge Base Settings
    knowledge_base_path: str = Field(
        default=os.getenv("KNOWLEDGE_BASE_PATH", "./data/knowledge_base"),
        description="Path to knowledge base storage"
    )
    feedback_log_path: str = Field(
        default=os.getenv("FEEDBACK_LOG_PATH", "./data/feedback_log.json"),
        description="Path to feedback log file"
    )

    # Agent Settings
    confidence_threshold: float = Field(
        default=float(os.getenv("CONFIDENCE_THRESHOLD", "0.7")),
        description="Minimum confidence threshold for classification"
    )
    enable_learning: bool = Field(
        default=os.getenv("ENABLE_LEARNING", "true").lower() == "true",
        description="Enable learning from feedback"
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum tokens for LLM response"
    )
    temperature: float = Field(
        default=0.3,
        description="Temperature for LLM (lower = more deterministic)"
    )

    class Config:
        validate_assignment = True

    def validate_keys(self) -> bool:
        """Validate that required API keys are present"""
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when using anthropic provider")
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using openai provider")
        return True
