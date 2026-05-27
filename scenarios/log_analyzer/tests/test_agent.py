"""Tests for LogAnalyzerAgent with mocked LLM."""

from unittest.mock import MagicMock, patch

import pytest

from scenarios.log_analyzer.src.agent import (
    create_log_analyzer_agent,
)


class TestLogAnalyzerAgent:
    """Tests for the LogAnalyzerAgent."""

    @patch("scenarios.log_analyzer.src.agent.create_agent")
    def test_create_agent_with_tools(self, mock_create: MagicMock) -> None:
        """Should create agent with file_reader and log_parser tools."""
        mock_create.return_value = MagicMock()

        agent = create_log_analyzer_agent()
        assert agent is not None

        # Verify create_agent was called
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        config = call_args[0][0]
        assert len(config.tools) == 2
        tool_names = [t.name for t in config.tools]
        assert "file_reader" in tool_names
        assert "log_parser" in tool_names

    @patch("scenarios.log_analyzer.src.agent.create_agent")
    def test_create_agent_with_custom_model(self, mock_create: MagicMock) -> None:
        """Should pass custom model to agent config."""
        mock_create.return_value = MagicMock()

        create_log_analyzer_agent(model="openai:gpt-4o")

        call_args = mock_create.call_args
        config = call_args[0][0]
        assert config.model == "openai:gpt-4o"

    @patch("scenarios.log_analyzer.src.agent.create_agent")
    def test_create_agent_with_debug(self, mock_create: MagicMock) -> None:
        """Should pass debug flag to agent config."""
        mock_create.return_value = MagicMock()

        create_log_analyzer_agent(debug=True)

        call_args = mock_create.call_args
        config = call_args[0][0]
        assert config.debug is True

    @patch("scenarios.log_analyzer.src.agent.create_agent")
    def test_system_prompt_is_set(self, mock_create: MagicMock) -> None:
        """Agent should have a system prompt."""
        mock_create.return_value = MagicMock()

        create_log_analyzer_agent()

        call_args = mock_create.call_args
        config = call_args[0][0]
        assert len(config.system_prompt) > 0
        assert "Log Analyzer" in config.system_prompt
