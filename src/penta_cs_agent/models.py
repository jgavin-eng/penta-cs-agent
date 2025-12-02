"""
Data models for email classification
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class EmailCategory(str, Enum):
    """Email classification categories for Penta Fine Ingredients customer service"""

    QUOTE_REQUEST = "quote_request"
    ORDER_PLACEMENT = "order_placement"
    ORDER_INQUIRY = "order_inquiry"
    PRODUCT_INQUIRY = "product_inquiry"
    TECHNICAL_SUPPORT = "technical_support"
    SHIPPING_INQUIRY = "shipping_inquiry"
    BILLING_INQUIRY = "billing_inquiry"
    COMPLAINT = "complaint"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    SAMPLE_REQUEST = "sample_request"
    GENERAL_INQUIRY = "general_inquiry"
    SPAM = "spam"

    @classmethod
    def get_description(cls, category: "EmailCategory") -> str:
        """Get human-readable description of category"""
        descriptions = {
            cls.QUOTE_REQUEST: "Customer requesting a price quote for one or more products",
            cls.ORDER_PLACEMENT: "Customer placing a new order or ready to purchase",
            cls.ORDER_INQUIRY: "Customer asking about status, tracking, or details of an existing order",
            cls.PRODUCT_INQUIRY: "Customer asking questions about product specifications, availability, or information",
            cls.TECHNICAL_SUPPORT: "Customer needs technical help with product application, formulation, or usage",
            cls.SHIPPING_INQUIRY: "Customer asking about shipping options, costs, delivery times, or logistics",
            cls.BILLING_INQUIRY: "Customer has questions about invoices, payments, or account balance",
            cls.COMPLAINT: "Customer expressing dissatisfaction or reporting an issue",
            cls.REGULATORY_COMPLIANCE: "Questions about certifications, regulatory compliance, safety data sheets, or documentation",
            cls.SAMPLE_REQUEST: "Customer requesting product samples for testing or evaluation",
            cls.GENERAL_INQUIRY: "General questions about the company, policies, or other topics",
            cls.SPAM: "Unsolicited, irrelevant, or marketing emails not related to customer service",
        }
        return descriptions.get(category, "Unknown category")


class EmailClassification(BaseModel):
    """Input model for email to be classified"""

    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    sender: Optional[str] = Field(None, description="Sender email address")
    received_at: Optional[datetime] = Field(default_factory=datetime.now, description="When email was received")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ClassificationResult(BaseModel):
    """Result of email classification"""

    primary_category: EmailCategory = Field(..., description="Primary classification category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    secondary_categories: List[EmailCategory] = Field(default_factory=list, description="Other possible categories")
    reasoning: str = Field(..., description="Explanation for the classification")
    extracted_entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted information (product names, order numbers, etc.)")
    recommended_action: str = Field(..., description="Suggested next steps or routing")
    priority: str = Field(default="normal", description="Priority level: low, normal, high, urgent")
    timestamp: datetime = Field(default_factory=datetime.now, description="Classification timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FeedbackEntry(BaseModel):
    """Feedback entry for learning system"""

    email_id: str = Field(..., description="Unique identifier for the email")
    original_classification: EmailCategory = Field(..., description="Original classification")
    correct_classification: EmailCategory = Field(..., description="Correct classification")
    confidence: float = Field(..., description="Original confidence score")
    email_content: str = Field(..., description="Email content for retraining")
    feedback_timestamp: datetime = Field(default_factory=datetime.now, description="When feedback was provided")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
