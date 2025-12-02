"""
Tests for data models
"""

import pytest
from datetime import datetime
from src.penta_cs_agent.models import (
    EmailCategory,
    EmailClassification,
    ClassificationResult,
    FeedbackEntry
)


def test_email_category_enum():
    """Test EmailCategory enum"""
    assert EmailCategory.QUOTE_REQUEST.value == "quote_request"
    assert EmailCategory.ORDER_PLACEMENT.value == "order_placement"
    assert EmailCategory.PRODUCT_INQUIRY.value == "product_inquiry"


def test_email_category_descriptions():
    """Test category descriptions"""
    desc = EmailCategory.get_description(EmailCategory.QUOTE_REQUEST)
    assert "quote" in desc.lower()
    assert "price" in desc.lower()


def test_email_classification_creation():
    """Test creating EmailClassification"""
    email = EmailClassification(
        subject="Test Subject",
        body="Test body content",
        sender="test@example.com"
    )

    assert email.subject == "Test Subject"
    assert email.body == "Test body content"
    assert email.sender == "test@example.com"
    assert isinstance(email.received_at, datetime)


def test_email_classification_without_sender():
    """Test EmailClassification without sender"""
    email = EmailClassification(
        subject="Test",
        body="Body"
    )

    assert email.sender is None
    assert email.metadata == {}


def test_classification_result_creation():
    """Test creating ClassificationResult"""
    result = ClassificationResult(
        primary_category=EmailCategory.QUOTE_REQUEST,
        confidence=0.95,
        secondary_categories=[EmailCategory.PRODUCT_INQUIRY],
        reasoning="Customer is asking for pricing",
        extracted_entities={"product": "citric acid", "quantity": "5000 kg"},
        recommended_action="Route to sales team",
        priority="high"
    )

    assert result.primary_category == EmailCategory.QUOTE_REQUEST
    assert result.confidence == 0.95
    assert len(result.secondary_categories) == 1
    assert result.priority == "high"


def test_classification_result_defaults():
    """Test ClassificationResult default values"""
    result = ClassificationResult(
        primary_category=EmailCategory.GENERAL_INQUIRY,
        confidence=0.7,
        reasoning="General question",
        recommended_action="Route to support"
    )

    assert result.secondary_categories == []
    assert result.extracted_entities == {}
    assert result.priority == "normal"


def test_feedback_entry_creation():
    """Test creating FeedbackEntry"""
    feedback = FeedbackEntry(
        email_id="test123",
        original_classification=EmailCategory.GENERAL_INQUIRY,
        correct_classification=EmailCategory.COMPLAINT,
        confidence=0.8,
        email_content="Test email content",
        notes="This was actually a complaint"
    )

    assert feedback.email_id == "test123"
    assert feedback.original_classification == EmailCategory.GENERAL_INQUIRY
    assert feedback.correct_classification == EmailCategory.COMPLAINT
    assert feedback.notes == "This was actually a complaint"


def test_confidence_score_validation():
    """Test confidence score must be between 0 and 1"""
    with pytest.raises(Exception):
        ClassificationResult(
            primary_category=EmailCategory.SPAM,
            confidence=1.5,  # Invalid: > 1
            reasoning="Test",
            recommended_action="Test"
        )

    with pytest.raises(Exception):
        ClassificationResult(
            primary_category=EmailCategory.SPAM,
            confidence=-0.1,  # Invalid: < 0
            reasoning="Test",
            recommended_action="Test"
        )
