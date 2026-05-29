"""Base tool utilities for creating LangChain-compatible tools."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from langchain_core.tools import StructuredTool


def create_tool(
    func: Callable[..., Any],
    *,
    name: str | None = None,
    description: str | None = None,
) -> StructuredTool:
    """Create a LangChain StructuredTool from a Python function.

    Args:
        func: The function to wrap.
        name: Optional override for the tool name.
        description: Optional override for the tool description.

    Returns:
        A StructuredTool ready for use with an agent.
    """
    return StructuredTool.from_function(
        coroutine=func if inspect.iscoroutinefunction(func) else None,
        func=func if not inspect.iscoroutinefunction(func) else None,
        name=name or func.__name__,
        description=description or (func.__doc__ or "").strip(),
    )


def tool_metadata(
    func: Callable[..., Any],
    *,
    description: str | None = None,
) -> dict[str, Any]:
    """Extract metadata from a function for tool registration.

    Args:
        func: The function to extract metadata from.
        description: Optional override for the description.

    Returns:
        A dict with name, description, and args schema.
    """
    sig = inspect.signature(func)
    args: dict[str, Any] = {}
    for param_name, param in sig.parameters.items():
        arg_info: dict[str, Any] = {}
        if param.annotation is not inspect.Parameter.empty:
            type_name = (
                param.annotation.__name__
                if hasattr(param.annotation, "__name__")
                else str(param.annotation)
            )
            arg_info["type"] = _python_type_to_json(type_name)
        if param.default is not inspect.Parameter.empty:
            arg_info["default"] = param.default
        args[param_name] = arg_info

    return {
        "name": func.__name__,
        "description": description or (func.__doc__ or "").strip(),
        "args": args,
    }


def _python_type_to_json(type_name: str) -> str:
    """Map Python type names to JSON schema types."""
    mapping = {
        "str": "string",
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "list": "array",
        "dict": "object",
    }
    return mapping.get(type_name, "string")
