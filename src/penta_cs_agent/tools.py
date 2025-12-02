"""
Function calling framework for external integrations
"""

from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass
import json


@dataclass
class ToolDefinition:
    """Definition of a tool/function that can be called by the agent"""

    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable


class ToolRegistry:
    """
    Registry for managing tools/functions that the agent can call
    """

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable
    ):
        """
        Register a new tool

        Args:
            name: Tool name
            description: Description of what the tool does
            parameters: JSON schema for the tool parameters
            function: The callable function
        """
        tool = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            function=function
        )
        self._tools[name] = tool

    def register_decorator(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Decorator for registering tools

        Args:
            name: Tool name
            description: Tool description
            parameters: JSON schema for parameters

        Example:
            @registry.register_decorator(
                name="get_order_status",
                description="Get status of an order",
                parameters={
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "Order ID"}
                    },
                    "required": ["order_id"]
                }
            )
            def get_order_status(order_id: str) -> dict:
                return {"order_id": order_id, "status": "shipped"}
        """
        def decorator(func: Callable):
            self.register(name, description, parameters, func)
            return func
        return decorator

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name"""
        return self._tools.get(name)

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool by name with arguments

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")

        try:
            return tool.function(**arguments)
        except Exception as e:
            return {"error": str(e), "tool": name}

    def get_tool_definitions_for_anthropic(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in Anthropic's format

        Returns:
            List of tool definitions for Anthropic API
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters
            }
            for tool in self._tools.values()
        ]

    def get_tool_definitions_for_openai(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in OpenAI's format

        Returns:
            List of tool definitions for OpenAI API
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self._tools.values()
        ]

    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())

    def get_tool_count(self) -> int:
        """Get the number of registered tools"""
        return len(self._tools)


# Default tool registry instance
default_registry = ToolRegistry()


# Example default tools for Penta Fine Ingredients

@default_registry.register_decorator(
    name="lookup_order",
    description="Look up an order by order ID or customer email",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID to look up"
            },
            "customer_email": {
                "type": "string",
                "description": "Customer email address"
            }
        }
    }
)
def lookup_order(order_id: Optional[str] = None, customer_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Look up order information (placeholder implementation)
    In production, this would connect to your order management system
    """
    return {
        "status": "example",
        "message": "This is a placeholder. Integrate with your order management system.",
        "order_id": order_id,
        "customer_email": customer_email
    }


@default_registry.register_decorator(
    name="check_product_availability",
    description="Check if a product is available and get current pricing",
    parameters={
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "Name of the product"
            },
            "product_id": {
                "type": "string",
                "description": "Product ID or SKU"
            }
        },
        "required": ["product_name"]
    }
)
def check_product_availability(product_name: str, product_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Check product availability (placeholder implementation)
    In production, this would connect to your inventory system
    """
    return {
        "status": "example",
        "message": "This is a placeholder. Integrate with your inventory system.",
        "product_name": product_name,
        "product_id": product_id,
        "available": True,
        "in_stock": 1000
    }


@default_registry.register_decorator(
    name="get_shipping_quote",
    description="Get a shipping quote for a location and quantity",
    parameters={
        "type": "object",
        "properties": {
            "destination": {
                "type": "string",
                "description": "Destination address or zip code"
            },
            "weight": {
                "type": "number",
                "description": "Weight in pounds"
            },
            "quantity": {
                "type": "number",
                "description": "Quantity of items"
            }
        },
        "required": ["destination"]
    }
)
def get_shipping_quote(destination: str, weight: Optional[float] = None,
                      quantity: Optional[int] = None) -> Dict[str, Any]:
    """
    Get shipping quote (placeholder implementation)
    In production, this would connect to your shipping system
    """
    return {
        "status": "example",
        "message": "This is a placeholder. Integrate with your shipping system.",
        "destination": destination,
        "estimated_cost": "$25.00",
        "estimated_days": "3-5 business days"
    }


@default_registry.register_decorator(
    name="search_knowledge_base",
    description="Search the company knowledge base for information",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            }
        },
        "required": ["query"]
    }
)
def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Search knowledge base (placeholder implementation)
    This can be enhanced to search FAQs, documentation, etc.
    """
    return {
        "status": "example",
        "message": "This is a placeholder. Connect to your knowledge base.",
        "query": query,
        "results": []
    }
