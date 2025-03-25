import subprocess
from typing import Dict, Any, Tuple
from ..domain.base import CoreToolBase, ToolResponse
from ..domain.models import Runtime, FunctionConfig
import asyncio

class FunctionCreator(CoreToolBase):
    """Core function creation logic"""
    
    @property
    def tool_id(self) -> str:
        return "create-function"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Function directory path"
                },
                "runtime": {
                    "type": "string",
                    "enum": [r.value for r in Runtime],
                    "description": "Function runtime"
                }
            },
            "required": ["path", "runtime"]
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        try:
            config = FunctionConfig(**kwargs)
            stdout, stderr = await self._run_command(config)
            
            if stderr and "warning:" not in stderr.lower():
                return ToolResponse(error=stderr)
            
            return ToolResponse(
                result=stdout,
                metadata=config.dict()
            )
        except Exception as e:
            return ToolResponse(error=str(e))
    
    async def _run_command(self, config: FunctionConfig) -> Tuple[str, str]:
        cmd = f"func create -l {config.runtime.value} {config.path}"
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode() 