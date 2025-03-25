from mcp.server.fastmcp import FastMCP
from pkg.core.func_creator import FunctionCreator
from pkg.core.func_deploy import FunctionDeployer
from pkg.registry import registry
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("Knative Tools MCP")

# Register tools
registry.register(FunctionCreator)
registry.register(FunctionDeployer)

# Create MCP endpoints
@mcp.tool()
async def create_function(path: str, runtime: str) -> str:
    """Create a Knative function"""
    try:
        tool = registry.get_tool("create-function")
        response = await tool.execute(path=path, runtime=runtime)
        if response.error:
            raise Exception(response.error)
        return response.result
    except Exception as e:
        logger.error(f"Failed to create function: {e}")
        raise

@mcp.tool()
async def deploy_function(path: str, builder: str, reg: str) -> str:
    """Deploy a Knative function"""
    try:
        tool = registry.get_tool("deploy-function")
        response = await tool.execute(path=path, builder=builder, registry=reg)
        if response.error:
            raise Exception(response.error)
        return response.result
    except Exception as e:
        logger.error(f"Failed to deploy function: {e}")
        raise

if __name__ == "__main__":
    mcp.run(transport="stdio") 