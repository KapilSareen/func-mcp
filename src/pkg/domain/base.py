from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolResponse(BaseModel):
    """Base response for all tools"""
    result: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class CoreToolBase(ABC):
    """Base interface for core tool logic"""
    
    @property
    @abstractmethod
    def tool_id(self) -> str:
        """Unique tool identifier"""
        pass
    
    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        """Tool's input schema"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResponse:
        """Execute tool logic"""
        pass 