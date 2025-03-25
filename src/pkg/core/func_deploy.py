import subprocess
from typing import Dict, Any, Tuple
from ..domain.base import CoreToolBase, ToolResponse
from ..domain.models import Builder, BuilderConfig
import asyncio
import logging

class FunctionDeployer(CoreToolBase):
    """Core function deployment logic"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
    
    @property
    def tool_id(self) -> str:
        return "deploy-function"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Function directory path"
                },
                "builder": {
                    "type": "string",
                    "enum": [r.value for r in Builder],
                    "description": "Function builder"
                },
                "registry": {
                    "type": "string",
                    "description": "Function registry"
                }
            },
            "required": ["path", "builder", "registry"]
        }
    
    async def execute(self, **kwargs) -> ToolResponse:
        try:
            config = BuilderConfig(**kwargs)
            stdout, stderr = await self._run_command(config)
            
            if stderr and "warning:" not in stderr.lower():
                self.logger.error(f"Deployment error: {stderr}")
                return ToolResponse(error=stderr)
            
            return ToolResponse(
                result=stdout,
                metadata=config.dict()
            )
        except Exception as e:
            self.logger.error(f"Exception during deployment: {str(e)}")
            return ToolResponse(error=str(e))
    
    async def _run_command(self, config: BuilderConfig) -> Tuple[str, str]:
        cmd = f"cd {config.path} && func deploy --builder={config.builder.value} --registry={config.registry}"
        process = await asyncio.create_subprocess_shell(
            f"export FUNC_ENABLE_HOST_BUILDER=1 && {cmd}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.logger.debug(f"Executing command: {cmd}")
        
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode() 