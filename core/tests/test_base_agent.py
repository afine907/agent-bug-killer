"""Tests for core base_agent module."""

from unittest.mock import MagicMock, patch

import pytest

from core.base_agent import AgentConfig, create_agent


class TestAgentConfig:
    """Tests for AgentConfig dataclass."""

    def test_default_config(self) -> None:
        """Should have sensible defaults."""
        config = AgentConfig()
        assert config.model == "anthropic:claude-sonnet-4-6"
        assert config.system_prompt == ""
        assert config.tools == []

    def test_custom_config(self) -> None:
        """Should accept custom values."""
        config = AgentConfig(
            model="openai:gpt-4o",
            system_prompt="You are a helper.",
            tools=["tool1", "tool2"],
        )
        assert config.model == "openai:gpt-4o"
        assert config.system_prompt == "You are a helper."
        assert len(config.tools) == 2


class TestCreateAgent:
    """Tests for the create_agent factory function."""

    @patch("core.base_agent.create_deep_agent")
    def test_create_agent_calls_deep_agents(self, mock_create: MagicMock) -> None:
        """Should delegate to create_deep_agent with correct args."""
        mock_create.return_value = MagicMock()

        config = AgentConfig(
            model="anthropic:claude-sonnet-4-6",
            system_prompt="You are a log analyzer.",
            tools=[],
        )
        agent = create_agent(config)

        mock_create.assert_called_once_with(
            model="anthropic:claude-sonnet-4-6",
            tools=[],
            system_prompt="You are a log analyzer.",
            middleware=[],
            debug=False,
        )
        assert agent is not None

    @patch("core.base_agent.create_deep_agent")
    def test_create_agent_with_tools(self, mock_create: MagicMock) -> None:
        """Should pass tools to create_deep_agent."""
        mock_tool = MagicMock()
        mock_create.return_value = MagicMock()

        config = AgentConfig(
            model="anthropic:claude-sonnet-4-6",
            system_prompt="test",
            tools=[mock_tool],
        )
        create_agent(config)

        _, kwargs = mock_create.call_args
        assert kwargs["tools"] == [mock_tool]

    @patch("core.base_agent.create_deep_agent")
    def test_create_agent_returns_compiled_graph(self, mock_create: MagicMock) -> None:
        """Should return whatever create_deep_agent returns."""
        mock_agent = MagicMock()
        mock_create.return_value = mock_agent

        config = AgentConfig()
        result = create_agent(config)
        assert result is mock_agent
