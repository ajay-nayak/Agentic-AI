"""Shared type definitions and schemas for Agentic AI projects."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentActionLog(BaseModel):
    """Log entry for an agent's reasoning step or tool execution."""
    step: int = Field(..., description="Step sequence number")
    thought: Optional[str] = Field(None, description="Agent reasoning or internal thought")
    tool_name: Optional[str] = Field(None, description="Name of tool invoked")
    tool_input: Optional[Any] = Field(None, description="Arguments passed to tool")
    tool_output: Optional[Any] = Field(None, description="Result returned by tool")


class AgentExecutionResult(BaseModel):
    """Standard container for agent workflow results."""
    query: str = Field(..., description="Original user prompt or task")
    output: str = Field(..., description="Final synthesized answer")
    steps: List[AgentActionLog] = Field(default_factory=list, description="List of intermediate reasoning and tool steps")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata such as provider, model, latency")
