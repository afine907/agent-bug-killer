"""Base agent factory using LangChain DeepAgents."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from deepagents import create_deep_agent
from langchain_core.tools import BaseTool


@dataclass
class AgentConfig:
    """Configuration for creating a Deep Agent."""

    model: str = "anthropic:claude-sonnet-4-6"
    system_prompt: str = ""
    tools: Sequence[BaseTool | Any] = field(default_factory=list)
    middleware: Sequence[Any] = field(default_factory=list)
    debug: bool = False


def create_agent(config: AgentConfig) -> Any:
    """Create a Deep Agent from the given configuration.

    Args:
        config: Agent configuration including model, prompt, and tools.

    Returns:
        A compiled LangGraph agent ready for invocation.
    """
    return create_deep_agent(
        model=config.model,
        tools=list(config.tools),
        system_prompt=config.system_prompt,
        middleware=config.middleware,
        debug=config.debug,
    )
