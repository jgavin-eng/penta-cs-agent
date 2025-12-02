"""
Example demonstrating the learning/feedback mechanism
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.penta_cs_agent import (
    EmailClassificationAgent,
    EmailClassification,
    EmailCategory,
    AgentConfig
)


def main():
    """Demonstrate the feedback and learning mechanism"""

    # Initialize agent with learning enabled
    config = AgentConfig(enable_learning=True)
    agent = EmailClassificationAgent(config=config)

    print("=" * 80)
    print("Feedback and Learning Example")
    print("=" * 80)
    print()

    # Classify an email
    email = EmailClassification(
        subject="Invoice payment question",
        body="""Hi,

I received invoice #INV-2024-001 but the amount seems incorrect.
Our original quote was for $5,000 but the invoice shows $5,500.

Can you please clarify?

Thanks,
Robert Davis
        """,
        sender="r.davis@company.com"
    )

    print("Classifying email...")
    result = agent.classify(email)

    print(f"Original Classification: {result.primary_category.value}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Reasoning: {result.reasoning}")
    print()

    # Let's say the agent classified this as BILLING_INQUIRY (correct)
    # but in some case it might have misclassified
    # Here's how to provide feedback

    # Example: Correcting a misclassification
    # Let's simulate that it was actually a complaint, not just a billing inquiry
    print("Providing feedback...")
    print("Actual category should be: COMPLAINT (due to billing discrepancy)")
    print()

    agent.provide_feedback(
        email=email,
        original_classification=result.primary_category,
        correct_classification=EmailCategory.COMPLAINT,
        confidence=result.confidence,
        notes="Customer is questioning invoice accuracy - this is a complaint about billing error"
    )

    print("Feedback saved! The agent will learn from this.")
    print()

    # Now let's classify a similar email to see if the agent has learned
    similar_email = EmailClassification(
        subject="Incorrect invoice amount",
        body="""Hello,

The invoice I received doesn't match the quote you provided.
This is concerning as we need to resolve this before payment.

Please review.

Best,
Jane Wilson
        """,
        sender="j.wilson@business.com"
    )

    print("Classifying a similar email after feedback...")
    result2 = agent.classify(similar_email)

    print(f"New Classification: {result2.primary_category.value}")
    print(f"Confidence: {result2.confidence:.2%}")
    print(f"Reasoning: {result2.reasoning}")
    print()
    print("The agent now has the previous similar case in its knowledge base")
    print("which may influence future classifications!")
    print()

    # Show statistics
    stats = agent.get_statistics()
    print("Knowledge Base Statistics:")
    print(f"- Classification History: {stats['knowledge_base']['total_history']} entries")
    print(f"- Common Queries: {stats['knowledge_base']['total_queries']} entries")
    print()


if __name__ == "__main__":
    main()
