"""Tests for BugDiagnoserAgent with mocked LLM."""

from unittest.mock import MagicMock, patch

from scenarios.bug_diagnoser.src.agent import (
    create_bug_diagnoser_agent,
)


class TestBugDiagnoserAgent:
    """Tests for the BugDiagnoserAgent."""

    @patch("scenarios.bug_diagnoser.src.agent.create_agent")
    def test_create_agent_with_all_tools(self, mock_create: MagicMock) -> None:
        """Should create agent with all required tools."""
        mock_create.return_value = MagicMock()

        agent = create_bug_diagnoser_agent()
        assert agent is not None

        mock_create.assert_called_once()
        call_args = mock_create.call_args
        config = call_args[0][0]
        tool_names = [t.name for t in config.tools]
        assert "ssh_exec" in tool_names
        assert "ssh_read_log" in tool_names
        assert "cdp_connect" in tool_names
        assert "cdp_screenshot" in tool_names
        assert "cdp_console" in tool_names
        assert "cdp_network" in tool_names
        assert "code_search" in tool_names
        assert "log_parser" in tool_names

    @patch("scenarios.bug_diagnoser.src.agent.create_agent")
    def test_create_agent_with_custom_model(self, mock_create: MagicMock) -> None:
        """Should pass custom model to agent config."""
        mock_create.return_value = MagicMock()

        create_bug_diagnoser_agent(model="openai:gpt-4o")

        call_args = mock_create.call_args
        config = call_args[0][0]
        assert config.model == "openai:gpt-4o"

    @patch("scenarios.bug_diagnoser.src.agent.create_agent")
    def test_system_prompt_is_set(self, mock_create: MagicMock) -> None:
        """Agent should have a system prompt."""
        mock_create.return_value = MagicMock()

        create_bug_diagnoser_agent()

        call_args = mock_create.call_args
        config = call_args[0][0]
        assert len(config.system_prompt) > 0
        assert "Bug Diagnoser" in config.system_prompt
