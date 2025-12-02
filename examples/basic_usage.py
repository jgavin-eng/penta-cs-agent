"""
Basic usage example for the Penta CS Email Classification Agent
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.penta_cs_agent import (
    EmailClassificationAgent,
    EmailClassification,
    EmailCategory,
    AgentConfig
)


def main():
    """Demonstrate basic usage of the email classification agent"""

    # Initialize the agent with default configuration
    # Make sure to set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file
    config = AgentConfig()
    agent = EmailClassificationAgent(config=config)

    print("=" * 80)
    print("Penta Fine Ingredients - Email Classification Agent")
    print("=" * 80)
    print()

    # Example 1: Quote Request
    print("Example 1: Quote Request")
    print("-" * 80)
    email1 = EmailClassification(
        subject="Request for quote - Citric Acid",
        body="""Hello,

We are interested in purchasing citric acid for our beverage production line.
Could you please provide a quote for 5000 kg of food-grade citric acid?

We need:
- Product specifications
- Pricing for 5000 kg
- Lead time
- Shipping options to Chicago, IL

Best regards,
John Smith
Beverage Corp
john.smith@beveragecorp.com
        """,
        sender="john.smith@beveragecorp.com"
    )

    result1 = agent.classify(email1)
    print(f"Primary Category: {result1.primary_category.value}")
    print(f"Confidence: {result1.confidence:.2%}")
    print(f"Reasoning: {result1.reasoning}")
    print(f"Extracted Entities: {result1.extracted_entities}")
    print(f"Recommended Action: {result1.recommended_action}")
    print(f"Priority: {result1.priority}")
    print()

    # Example 2: Order Status Inquiry
    print("Example 2: Order Status Inquiry")
    print("-" * 80)
    email2 = EmailClassification(
        subject="Order #12345 - Shipping Status?",
        body="""Hi,

I placed an order last week (Order #12345) for sodium benzoate and haven't
received any tracking information yet. Can you please let me know the status?

Thanks,
Sarah Johnson
        """,
        sender="sarah.j@email.com"
    )

    result2 = agent.classify(email2)
    print(f"Primary Category: {result2.primary_category.value}")
    print(f"Confidence: {result2.confidence:.2%}")
    print(f"Reasoning: {result2.reasoning}")
    print(f"Extracted Entities: {result2.extracted_entities}")
    print(f"Recommended Action: {result2.recommended_action}")
    print(f"Priority: {result2.priority}")
    print()

    # Example 3: Product Inquiry
    print("Example 3: Product Inquiry")
    print("-" * 80)
    email3 = EmailClassification(
        subject="Question about Ascorbic Acid specifications",
        body="""Hello Penta team,

We're considering using your ascorbic acid in our nutraceutical products.
Can you provide information about:
- Purity levels available
- Country of origin
- Certifications (GMP, Kosher, Halal)
- Particle size distribution

Looking forward to your response.

Best,
Michael Chen
Quality Manager
        """,
        sender="m.chen@nutra.com"
    )

    result3 = agent.classify(email3)
    print(f"Primary Category: {result3.primary_category.value}")
    print(f"Confidence: {result3.confidence:.2%}")
    print(f"Reasoning: {result3.reasoning}")
    print(f"Extracted Entities: {result3.extracted_entities}")
    print(f"Recommended Action: {result3.recommended_action}")
    print(f"Priority: {result3.priority}")
    print()

    # Example 4: Sample Request
    print("Example 4: Sample Request")
    print("-" * 80)
    email4 = EmailClassification(
        subject="Sample request for testing",
        body="""Dear Penta,

We would like to request samples of the following products for evaluation:
1. Potassium Sorbate - 100g
2. Calcium Propionate - 100g

Please send to our R&D facility in Boston.

Thank you,
Lisa Martinez
R&D Director
        """,
        sender="l.martinez@foodtech.com"
    )

    result4 = agent.classify(email4)
    print(f"Primary Category: {result4.primary_category.value}")
    print(f"Confidence: {result4.confidence:.2%}")
    print(f"Reasoning: {result4.reasoning}")
    print(f"Extracted Entities: {result4.extracted_entities}")
    print(f"Recommended Action: {result4.recommended_action}")
    print(f"Priority: {result4.priority}")
    print()

    # Get agent statistics
    print("Agent Statistics")
    print("-" * 80)
    stats = agent.get_statistics()
    print(f"LLM Provider: {stats['llm_provider']}")
    print(f"Model: {stats['model']}")
    print(f"Tools Registered: {stats['tools_registered']}")
    print(f"Learning Enabled: {stats['learning_enabled']}")
    print(f"Knowledge Base Stats: {stats['knowledge_base']}")
    print()


if __name__ == "__main__":
    main()
