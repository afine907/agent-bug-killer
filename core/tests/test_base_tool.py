"""Tests for core base_tool module."""

import pytest
from langchain_core.tools import StructuredTool

from core.base_tool import create_tool, tool_metadata


class TestCreateTool:
    """Tests for the create_tool factory function."""

    def test_create_tool_from_function(self) -> None:
        """Should create a StructuredTool from a plain function."""

        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        tool = create_tool(add)
        assert isinstance(tool, StructuredTool)
        assert tool.name == "add"
        assert "Add two numbers" in tool.description

    def test_create_tool_with_custom_name(self) -> None:
        """Should allow custom tool name."""

        def my_func(x: int) -> int:
            """Process x."""
            return x * 2

        tool = create_tool(my_func, name="double_it")
        assert tool.name == "double_it"

    def test_create_tool_with_custom_description(self) -> None:
        """Should allow custom description."""

        def my_func(x: int) -> int:
            """Original description."""
            return x

        tool = create_tool(my_func, description="Custom description")
        assert tool.description == "Custom description"

    def test_create_tool_is_coroutine(self) -> None:
        """Should detect async functions."""

        async def async_func(x: int) -> int:
            """Async function."""
            return x

        tool = create_tool(async_func)
        assert tool.coroutine is not None

    def test_create_tool_invocation(self) -> None:
        """Tool should be invokable."""

        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b

        tool = create_tool(multiply)
        result = tool.invoke({"a": 3, "b": 4})
        assert result == 12


class TestToolMetadata:
    """Tests for tool_metadata helper."""

    def test_metadata_from_function(self) -> None:
        """Should extract metadata from function signature and docstring."""

        def read_file(path: str, encoding: str = "utf-8") -> str:
            """Read a file from disk."""
            return ""

        meta = tool_metadata(read_file)
        assert meta["name"] == "read_file"
        assert "path" in meta["args"]
        assert meta["args"]["path"]["type"] == "string"
        assert meta["args"]["encoding"]["type"] == "string"
        assert meta["args"]["encoding"]["default"] == "utf-8"

    def test_metadata_with_description_override(self) -> None:
        """Should use provided description over docstring."""

        def func(x: int) -> int:
            """Original."""
            return x

        meta = tool_metadata(func, description="Override")
        assert meta["description"] == "Override"
