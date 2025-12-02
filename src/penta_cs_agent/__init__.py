"""
Penta CS Agent - Email Classification Agent for Customer Service Routing
"""

from .agent import EmailClassificationAgent
from .models import EmailClassification, EmailCategory, ClassificationResult
from .config import AgentConfig

__version__ = "1.0.0"
__all__ = [
    "EmailClassificationAgent",
    "EmailClassification",
    "EmailCategory",
    "ClassificationResult",
    "AgentConfig",
]
