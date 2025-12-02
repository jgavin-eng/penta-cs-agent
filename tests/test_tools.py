"""
Tests for tool registry and function calling
"""

import pytest
from src.penta_cs_agent.tools import ToolRegistry, default_registry


def test_tool_registry_creation():
    """Test creating a new tool registry"""
    registry = ToolRegistry()
    assert registry.get_tool_count() == 0


def test_tool_registration():
    """Test registering a tool"""
    registry = ToolRegistry()

    def test_function(param1: str) -> dict:
        return {"result": param1}

    registry.register(
        name="test_tool",
        description="A test tool",
        parameters={
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            }
        },
        function=test_function
    )

    assert registry.get_tool_count() == 1
    assert "test_tool" in registry.list_tools()


def test_tool_registration_decorator():
    """Test registering a tool with decorator"""
    registry = ToolRegistry()

    @registry.register_decorator(
        name="decorated_tool",
        description="A decorated tool",
        parameters={
            "type": "object",
            "properties": {
                "value": {"type": "number"}
            }
        }
    )
    def decorated_function(value: int) -> dict:
        return {"doubled": value * 2}

    assert registry.get_tool_count() == 1
    tool = registry.get_tool("decorated_tool")
    assert tool is not None
    assert tool.name == "decorated_tool"


def test_tool_calling():
    """Test calling a registered tool"""
    registry = ToolRegistry()

    @registry.register_decorator(
        name="add_numbers",
        description="Add two numbers",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            }
        }
    )
    def add_numbers(a: int, b: int) -> dict:
        return {"sum": a + b}

    result = registry.call_tool("add_numbers", {"a": 5, "b": 3})
    assert result["sum"] == 8


def test_tool_calling_nonexistent():
    """Test calling a tool that doesn't exist"""
    registry = ToolRegistry()

    with pytest.raises(ValueError, match="not found"):
        registry.call_tool("nonexistent_tool", {})


def test_tool_calling_with_error():
    """Test tool call that raises an error"""
    registry = ToolRegistry()

    @registry.register_decorator(
        name="error_tool",
        description="A tool that errors",
        parameters={"type": "object", "properties": {}}
    )
    def error_function():
        raise RuntimeError("Something went wrong")

    result = registry.call_tool("error_tool", {})
    assert "error" in result
    assert "Something went wrong" in result["error"]


def test_anthropic_format():
    """Test getting tools in Anthropic format"""
    registry = ToolRegistry()

    @registry.register_decorator(
        name="test_tool",
        description="Test tool",
        parameters={
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    )
    def test_func(param: str):
        return {"result": param}

    tools = registry.get_tool_definitions_for_anthropic()
    assert len(tools) == 1
    assert tools[0]["name"] == "test_tool"
    assert tools[0]["description"] == "Test tool"
    assert "input_schema" in tools[0]


def test_openai_format():
    """Test getting tools in OpenAI format"""
    registry = ToolRegistry()

    @registry.register_decorator(
        name="test_tool",
        description="Test tool",
        parameters={
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    )
    def test_func(param: str):
        return {"result": param}

    tools = registry.get_tool_definitions_for_openai()
    assert len(tools) == 1
    assert tools[0]["type"] == "function"
    assert tools[0]["function"]["name"] == "test_tool"
    assert tools[0]["function"]["description"] == "Test tool"


def test_default_registry_has_tools():
    """Test that default registry has pre-registered tools"""
    assert default_registry.get_tool_count() > 0
    tools = default_registry.list_tools()
    assert "lookup_order" in tools
    assert "check_product_availability" in tools
    assert "get_shipping_quote" in tools
