"""
Tests for configuration
"""

import pytest
import os
from src.penta_cs_agent.config import AgentConfig


def test_agent_config_defaults():
    """Test default configuration values"""
    # Temporarily clear env vars
    old_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    old_openai_key = os.environ.get("OPENAI_API_KEY")

    os.environ["ANTHROPIC_API_KEY"] = "test-key"

    config = AgentConfig()

    assert config.llm_provider in ["anthropic", "openai"]
    assert config.confidence_threshold == 0.7
    assert config.max_tokens == 4096
    assert config.temperature == 0.3

    # Restore
    if old_anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = old_anthropic_key
    if old_openai_key:
        os.environ["OPENAI_API_KEY"] = old_openai_key


def test_agent_config_custom_values():
    """Test custom configuration values"""
    os.environ["ANTHROPIC_API_KEY"] = "test-key"

    config = AgentConfig(
        llm_provider="anthropic",
        confidence_threshold=0.8,
        temperature=0.5
    )

    assert config.llm_provider == "anthropic"
    assert config.confidence_threshold == 0.8
    assert config.temperature == 0.5


def test_agent_config_validation_anthropic():
    """Test validation requires Anthropic key when using anthropic provider"""
    old_key = os.environ.get("ANTHROPIC_API_KEY")
    if "ANTHROPIC_API_KEY" in os.environ:
        del os.environ["ANTHROPIC_API_KEY"]

    config = AgentConfig(llm_provider="anthropic")

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        config.validate_keys()

    if old_key:
        os.environ["ANTHROPIC_API_KEY"] = old_key


def test_agent_config_validation_openai():
    """Test validation requires OpenAI key when using openai provider"""
    old_key = os.environ.get("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    config = AgentConfig(llm_provider="openai")

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        config.validate_keys()

    if old_key:
        os.environ["OPENAI_API_KEY"] = old_key
