from typing import Dict, Type
from ..domain.base import CoreToolBase

class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self._tools: Dict[str, Type[CoreToolBase]] = {}
    
    def register(self, tool_class: Type[CoreToolBase]) -> None:
        """Register a tool class"""
        tool = tool_class()
        self._tools[tool.tool_id] = tool_class
    
    def get_tool(self, tool_id: str) -> CoreToolBase:
        """Get a tool instance by its ID"""
        if tool_id not in self._tools:
            raise KeyError(f"Tool with ID '{tool_id}' not found")
        return self._tools[tool_id]()

# Create a singleton instance
registry = ToolRegistry() 