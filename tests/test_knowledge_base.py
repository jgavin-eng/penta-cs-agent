"""
Tests for knowledge base
"""

import pytest
import tempfile
import shutil
from src.penta_cs_agent.knowledge_base import KnowledgeBase


@pytest.fixture
def temp_kb():
    """Create a temporary knowledge base for testing"""
    temp_dir = tempfile.mkdtemp()
    kb = KnowledgeBase(persist_directory=temp_dir)
    yield kb
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_knowledge_base_creation(temp_kb):
    """Test creating a knowledge base"""
    assert temp_kb is not None
    stats = temp_kb.get_stats()
    assert stats["total_products"] == 0
    assert stats["total_queries"] == 0
    assert stats["total_history"] == 0


def test_add_product(temp_kb):
    """Test adding a product to knowledge base"""
    temp_kb.add_product(
        product_id="TEST-001",
        name="Test Product",
        description="A test product description",
        category="Test Category"
    )

    stats = temp_kb.get_stats()
    assert stats["total_products"] == 1


def test_add_multiple_products(temp_kb):
    """Test adding multiple products"""
    products = [
        ("P1", "Product 1", "Description 1", "Cat1"),
        ("P2", "Product 2", "Description 2", "Cat2"),
        ("P3", "Product 3", "Description 3", "Cat3"),
    ]

    for pid, name, desc, cat in products:
        temp_kb.add_product(pid, name, desc, cat)

    stats = temp_kb.get_stats()
    assert stats["total_products"] == 3


def test_search_products(temp_kb):
    """Test searching for products"""
    temp_kb.add_product(
        product_id="CA-001",
        name="Citric Acid",
        description="Food-grade citric acid for beverages",
        category="Acidulants"
    )

    temp_kb.add_product(
        product_id="AA-001",
        name="Ascorbic Acid",
        description="Vitamin C for supplements",
        category="Vitamins"
    )

    # Search for acidulant
    results = temp_kb.search_products("citric acid beverages", n_results=2)
    assert len(results) > 0
    # Should find citric acid as most relevant
    assert "Citric Acid" in results[0]["metadata"]["name"]


def test_add_common_query(temp_kb):
    """Test adding common queries"""
    temp_kb.add_common_query(
        query_id="Q001",
        query_text="What is the price for citric acid?",
        classification="quote_request",
        confidence=0.95
    )

    stats = temp_kb.get_stats()
    assert stats["total_queries"] == 1


def test_search_similar_queries(temp_kb):
    """Test searching for similar queries"""
    temp_kb.add_common_query(
        query_id="Q001",
        query_text="I need a price quote for citric acid",
        classification="quote_request",
        confidence=0.95
    )

    temp_kb.add_common_query(
        query_id="Q002",
        query_text="Where is my order?",
        classification="order_inquiry",
        confidence=0.92
    )

    # Search for price-related query
    results = temp_kb.search_similar_queries("How much does citric acid cost?", n_results=2)
    assert len(results) > 0
    # Should find the quote request as most similar
    assert results[0]["metadata"]["classification"] == "quote_request"


def test_add_classification_history(temp_kb):
    """Test adding classification history"""
    temp_kb.add_classification_history(
        email_id="EMAIL001",
        email_content="Subject: Quote request Body: Need pricing",
        classification="quote_request",
        confidence=0.9,
        was_correct=True
    )

    stats = temp_kb.get_stats()
    assert stats["total_history"] == 1


def test_search_classification_history(temp_kb):
    """Test searching classification history"""
    temp_kb.add_classification_history(
        email_id="EMAIL001",
        email_content="I need a quote for 500kg citric acid",
        classification="quote_request",
        confidence=0.95
    )

    results = temp_kb.search_classification_history("quote for citric acid", n_results=1)
    assert len(results) > 0
    assert results[0]["metadata"]["classification"] == "quote_request"


def test_get_context_for_classification(temp_kb):
    """Test getting full context for classification"""
    # Add some data
    temp_kb.add_product("P1", "Citric Acid", "Description", "Cat")
    temp_kb.add_common_query("Q1", "price quote", "quote_request", 0.9)
    temp_kb.add_classification_history("E1", "need quote", "quote_request", 0.9)

    context = temp_kb.get_context_for_classification("I need a price quote")

    assert "similar_queries" in context
    assert "relevant_products" in context
    assert "similar_history" in context
