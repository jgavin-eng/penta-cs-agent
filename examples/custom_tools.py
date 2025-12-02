"""
Example showing how to add custom tools/functions for the agent to call
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.penta_cs_agent import (
    EmailClassificationAgent,
    EmailClassification,
    AgentConfig
)
from src.penta_cs_agent.tools import ToolRegistry


def main():
    """Demonstrate custom tool registration"""

    print("=" * 80)
    print("Custom Tools Example")
    print("=" * 80)
    print()

    # Create a custom tool registry
    custom_registry = ToolRegistry()

    # Register a custom tool using the decorator
    @custom_registry.register_decorator(
        name="check_customer_history",
        description="Check customer's order history and account status",
        parameters={
            "type": "object",
            "properties": {
                "customer_email": {
                    "type": "string",
                    "description": "Customer's email address"
                }
            },
            "required": ["customer_email"]
        }
    )
    def check_customer_history(customer_email: str):
        """
        Custom function to check customer history
        In production, this would query your CRM/database
        """
        # Simulated customer data
        customer_db = {
            "valued.customer@company.com": {
                "total_orders": 25,
                "account_status": "premium",
                "last_order": "2024-11-15",
                "total_spent": "$125,000"
            },
            "new.customer@startup.com": {
                "total_orders": 0,
                "account_status": "new",
                "last_order": None,
                "total_spent": "$0"
            }
        }

        customer_info = customer_db.get(
            customer_email,
            {
                "total_orders": 0,
                "account_status": "unknown",
                "last_order": None,
                "total_spent": "$0"
            }
        )

        return {
            "customer_email": customer_email,
            **customer_info
        }

    # Register another custom tool for pricing
    @custom_registry.register_decorator(
        name="get_product_price",
        description="Get current pricing for a specific product",
        parameters={
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product"
                },
                "quantity": {
                    "type": "number",
                    "description": "Quantity in kilograms"
                }
            },
            "required": ["product_name"]
        }
    )
    def get_product_price(product_name: str, quantity: float = 1000):
        """
        Get product pricing with volume discounts
        In production, this would query your pricing system
        """
        # Simulated pricing database
        base_prices = {
            "citric acid": 2.50,
            "ascorbic acid": 8.75,
            "sodium benzoate": 3.25,
            "potassium sorbate": 4.50
        }

        product_key = product_name.lower()
        base_price = base_prices.get(product_key, 5.00)

        # Volume discount tiers
        if quantity >= 10000:
            discount = 0.15
        elif quantity >= 5000:
            discount = 0.10
        elif quantity >= 1000:
            discount = 0.05
        else:
            discount = 0.0

        unit_price = base_price * (1 - discount)
        total_price = unit_price * quantity

        return {
            "product_name": product_name,
            "quantity_kg": quantity,
            "unit_price_usd": round(unit_price, 2),
            "total_price_usd": round(total_price, 2),
            "discount_percent": discount * 100
        }

    print(f"Registered {custom_registry.get_tool_count()} custom tools:")
    for tool_name in custom_registry.list_tools():
        print(f"  - {tool_name}")
    print()

    # Initialize agent with custom tool registry
    config = AgentConfig()
    agent = EmailClassificationAgent(config=config, tool_registry=custom_registry)

    # Test with an email that could benefit from tool usage
    email = EmailClassification(
        subject="Quote request for Citric Acid",
        body="""Hello,

I'd like to get a quote for 7500 kg of citric acid.
We've been a customer for several years and wondering if there are
any volume discounts available.

Our email on file is valued.customer@company.com

Best regards,
Thomas Anderson
Purchasing Manager
        """,
        sender="valued.customer@company.com"
    )

    print("Classifying email with custom tools available...")
    print()
    result = agent.classify(email)

    print(f"Primary Category: {result.primary_category.value}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Extracted Entities: {result.extracted_entities}")
    print(f"Recommended Action: {result.recommended_action}")
    print(f"Priority: {result.priority}")
    print()
    print("Note: The agent can use the custom tools (check_customer_history,")
    print("get_product_price) to provide more informed classifications and")
    print("extract relevant information!")
    print()


if __name__ == "__main__":
    main()
