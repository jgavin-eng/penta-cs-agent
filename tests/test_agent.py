"""
Tests for the main agent
Note: These tests require valid API keys and will make actual API calls
For unit testing without API calls, mock the LLM responses
"""

import pytest
import os
import tempfile
import shutil
from src.penta_cs_agent import (
    EmailClassificationAgent,
    EmailClassification,
    EmailCategory,
    AgentConfig
)
from src.penta_cs_agent.tools import ToolRegistry


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_config(temp_data_dir):
    """Create a config for testing (requires API key in env)"""
    # This will use API keys from environment
    config = AgentConfig(
        knowledge_base_path=os.path.join(temp_data_dir, "kb"),
        feedback_log_path=os.path.join(temp_data_dir, "feedback.json"),
        enable_learning=True
    )
    return config


def test_agent_initialization(mock_config):
    """Test agent initialization"""
    agent = EmailClassificationAgent(config=mock_config)
    assert agent is not None
    assert agent.config == mock_config
    assert agent.tool_registry is not None
    assert agent.knowledge_base is not None


def test_agent_with_custom_tools(mock_config):
    """Test agent with custom tool registry"""
    custom_registry = ToolRegistry()

    @custom_registry.register_decorator(
        name="test_tool",
        description="Test",
        parameters={"type": "object", "properties": {}}
    )
    def test_func():
        return {"test": True}

    agent = EmailClassificationAgent(
        config=mock_config,
        tool_registry=custom_registry
    )

    assert agent.tool_registry.get_tool_count() == 1


def test_agent_get_statistics(mock_config):
    """Test getting agent statistics"""
    agent = EmailClassificationAgent(config=mock_config)
    stats = agent.get_statistics()

    assert "llm_provider" in stats
    assert "model" in stats
    assert "knowledge_base" in stats
    assert "tools_registered" in stats
    assert "learning_enabled" in stats


def test_email_id_generation(mock_config):
    """Test email ID generation is consistent"""
    agent = EmailClassificationAgent(config=mock_config)

    email = EmailClassification(
        subject="Test",
        body="Body",
        sender="test@test.com"
    )

    id1 = agent._generate_email_id(email)
    id2 = agent._generate_email_id(email)

    # Same email should generate same ID
    assert id1 == id2

    # Different email should generate different ID
    email2 = EmailClassification(
        subject="Different",
        body="Body",
        sender="test@test.com"
    )
    id3 = agent._generate_email_id(email2)
    assert id1 != id3


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Requires API key to run integration test"
)
def test_agent_classification_integration(mock_config):
    """
    Integration test - actually classifies an email
    Skipped if no API key is available
    """
    agent = EmailClassificationAgent(config=mock_config)

    email = EmailClassification(
        subject="Request for quote - Citric Acid",
        body="We would like a price quote for 5000 kg of food-grade citric acid.",
        sender="customer@example.com"
    )

    result = agent.classify(email)

    # Verify result structure
    assert result.primary_category is not None
    assert isinstance(result.primary_category, EmailCategory)
    assert 0.0 <= result.confidence <= 1.0
    assert result.reasoning != ""
    assert result.recommended_action != ""
    assert result.priority in ["low", "normal", "high", "urgent"]

    # For this specific email, should likely be quote_request
    # (though this depends on LLM, so we don't assert it)


def test_feedback_mechanism(mock_config, temp_data_dir):
    """Test providing feedback"""
    agent = EmailClassificationAgent(config=mock_config)

    email = EmailClassification(
        subject="Test",
        body="Test body",
        sender="test@test.com"
    )

    # Provide feedback
    agent.provide_feedback(
        email=email,
        original_classification=EmailCategory.GENERAL_INQUIRY,
        correct_classification=EmailCategory.COMPLAINT,
        confidence=0.7,
        notes="This was actually a complaint"
    )

    # Check that feedback file was created
    feedback_path = mock_config.feedback_log_path
    assert os.path.exists(feedback_path)

    # Check knowledge base was updated
    kb_stats = agent.knowledge_base.get_stats()
    assert kb_stats["total_history"] > 0
    assert kb_stats["total_queries"] > 0


def test_system_prompt_generation(mock_config):
    """Test system prompt generation"""
    agent = EmailClassificationAgent(config=mock_config)
    prompt = agent._get_system_prompt()

    assert "Penta Fine Ingredients" in prompt
    assert "email classification" in prompt.lower()
    assert "quote_request" in prompt


def test_classification_prompt_generation(mock_config):
    """Test classification prompt generation"""
    agent = EmailClassificationAgent(config=mock_config)

    email = EmailClassification(
        subject="Test Subject",
        body="Test Body",
        sender="test@test.com"
    )

    prompt = agent._create_classification_prompt(email)

    assert "Test Subject" in prompt
    assert "Test Body" in prompt
    assert "test@test.com" in prompt
    assert "JSON" in prompt  # Should request JSON format
