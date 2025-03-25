from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Runtime(str, Enum):
    """Available Knative function runtimes"""
    PYTHON = "python"
    NODE = "node"
    GO = "go"
    QUARKUS = "quarkus"
    RUST = "rust"
    TYPESCRIPT = "typescript"

class FunctionConfig(BaseModel):
    """Common function configuration"""
    path: str
    runtime: Runtime
    namespace: Optional[str] = None 

class Builder(str, Enum):
    """Available Knative function builders"""
    HOST = "host"

class BuilderConfig(BaseModel):
    """Builder configuration"""
    builder: Builder
    path: str
    registry: str
