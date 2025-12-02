"""
Example showing how to populate the knowledge base with product and query data
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.penta_cs_agent.knowledge_base import KnowledgeBase


def main():
    """Demonstrate knowledge base population"""

    print("=" * 80)
    print("Knowledge Base Setup Example")
    print("=" * 80)
    print()

    # Initialize knowledge base
    kb = KnowledgeBase(persist_directory="./data/knowledge_base")

    print("Populating knowledge base with Penta Fine Ingredients data...")
    print()

    # Add product information
    products = [
        {
            "product_id": "CA-001",
            "name": "Citric Acid",
            "description": "Food-grade citric acid, white crystalline powder. Used as acidulant, preservative, and flavoring agent in food and beverages. Available in anhydrous and monohydrate forms.",
            "category": "Acidulants",
            "metadata": {"grades": ["Food Grade", "USP", "FCC"], "cas": "77-92-9"}
        },
        {
            "product_id": "AA-001",
            "name": "Ascorbic Acid",
            "description": "Vitamin C, white to slightly yellow crystalline powder. Antioxidant and nutrient supplement for food, pharmaceutical, and cosmetic applications.",
            "category": "Vitamins",
            "metadata": {"grades": ["Food Grade", "USP", "Pharmaceutical"], "cas": "50-81-7"}
        },
        {
            "product_id": "SB-001",
            "name": "Sodium Benzoate",
            "description": "White granular or crystalline powder. Widely used preservative in acidic foods and beverages. Effective against yeasts and bacteria.",
            "category": "Preservatives",
            "metadata": {"grades": ["Food Grade", "FCC"], "cas": "532-32-1"}
        },
        {
            "product_id": "PS-001",
            "name": "Potassium Sorbate",
            "description": "White crystalline powder. Preservative effective against molds and yeasts. Used in cheese, wine, baked goods, and other food products.",
            "category": "Preservatives",
            "metadata": {"grades": ["Food Grade", "FCC"], "cas": "24634-61-5"}
        },
        {
            "product_id": "CP-001",
            "name": "Calcium Propionate",
            "description": "White crystalline powder. Preservative and mold inhibitor used primarily in baked goods. Also provides calcium fortification.",
            "category": "Preservatives",
            "metadata": {"grades": ["Food Grade", "FCC"], "cas": "4075-81-4"}
        },
    ]

    for product in products:
        kb.add_product(
            product_id=product["product_id"],
            name=product["name"],
            description=product["description"],
            category=product["category"],
            metadata=product.get("metadata", {})
        )
        print(f"Added product: {product['name']}")

    print()

    # Add common queries
    common_queries = [
        {
            "query_id": "Q001",
            "text": "What is the price for bulk citric acid?",
            "classification": "quote_request",
            "confidence": 0.95
        },
        {
            "query_id": "Q002",
            "text": "Do you have the COA and specifications for sodium benzoate?",
            "classification": "regulatory_compliance",
            "confidence": 0.90
        },
        {
            "query_id": "Q003",
            "text": "Can I get samples of your preservatives to test?",
            "classification": "sample_request",
            "confidence": 0.98
        },
        {
            "query_id": "Q004",
            "text": "Where is my order? I haven't received tracking.",
            "classification": "order_inquiry",
            "confidence": 0.92
        },
        {
            "query_id": "Q005",
            "text": "What are the differences between your citric acid grades?",
            "classification": "product_inquiry",
            "confidence": 0.88
        },
    ]

    for query in common_queries:
        kb.add_common_query(
            query_id=query["query_id"],
            query_text=query["text"],
            classification=query["classification"],
            confidence=query["confidence"]
        )
        print(f"Added common query: {query['query_id']}")

    print()

    # Test search functionality
    print("Testing knowledge base search...")
    print()

    # Search for products
    print("Searching for 'preservative for baked goods':")
    results = kb.search_products("preservative for baked goods", n_results=3)
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['metadata']['name']} (relevance: {1 - result['distance']:.2f})")
    print()

    # Search for similar queries
    print("Searching for similar query: 'I need pricing for large order'")
    results = kb.search_similar_queries("I need pricing for large order", n_results=3)
    for i, result in enumerate(results, 1):
        print(f"  {i}. Classification: {result['metadata']['classification']}")
        print(f"     Query: {result['document'][:60]}...")
        print(f"     Relevance: {1 - result['distance']:.2f}")
    print()

    # Get statistics
    stats = kb.get_stats()
    print("Knowledge Base Statistics:")
    print(f"  Total Products: {stats['total_products']}")
    print(f"  Total Common Queries: {stats['total_queries']}")
    print(f"  Total Classification History: {stats['total_history']}")
    print()

    print("Knowledge base setup complete!")
    print("The agent will now use this information to make better classifications.")
    print()


if __name__ == "__main__":
    main()
