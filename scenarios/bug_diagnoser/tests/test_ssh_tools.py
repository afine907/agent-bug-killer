"""Tests for SSH tools: ssh_exec and ssh_read_log."""

from unittest.mock import MagicMock, patch

from scenarios.bug_diagnoser.src.tools.ssh_tool import ssh_exec, ssh_read_log


class TestSshExec:
    """Tests for the ssh_exec tool."""

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_exec_command_success(self, mock_ssh_class: MagicMock) -> None:
        """Should execute command and return output."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client

        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()
        stdout.read.return_value = b"hello world\n"
        stdout.channel.recv_exit_status.return_value = 0
        mock_client.exec_command.return_value = (stdin, stdout, stderr)

        result = ssh_exec.invoke({
            "host": "test-server",
            "user": "deploy",
            "command": "echo hello",
        })

        assert "hello world" in result
        mock_client.exec_command.assert_called_once_with("echo hello", timeout=30)

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_exec_command_failure(self, mock_ssh_class: MagicMock) -> None:
        """Should return error message on command failure."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client

        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()
        stdout.read.return_value = b""
        stderr.read.return_value = b"command not found"
        stdout.channel.recv_exit_status.return_value = 127
        mock_client.exec_command.return_value = (stdin, stdout, stderr)

        result = ssh_exec.invoke({
            "host": "test-server",
            "user": "deploy",
            "command": "nonexistent-cmd",
        })

        assert "command not found" in result or "Error" in result

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_exec_command_connection_error(self, mock_ssh_class: MagicMock) -> None:
        """Should handle connection errors gracefully."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client
        mock_client.connect.side_effect = Exception("Connection refused")

        result = ssh_exec.invoke({
            "host": "unreachable-server",
            "user": "deploy",
            "command": "ls",
        })

        assert "Error" in result or "error" in result.lower()


class TestSshReadLog:
    """Tests for the ssh_read_log tool."""

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_read_log_file(self, mock_ssh_class: MagicMock) -> None:
        """Should read a log file via SSH."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client

        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()
        log_content = "2024-01-15 ERROR something failed\nTraceback...\n"
        stdout.read.return_value = log_content.encode()
        stdout.channel.recv_exit_status.return_value = 0
        mock_client.exec_command.return_value = (stdin, stdout, stderr)

        result = ssh_read_log.invoke({
            "host": "test-server",
            "user": "deploy",
            "path": "/var/log/app.log",
        })

        assert "something failed" in result
        # Should use tail to read last N lines
        call_args = mock_client.exec_command.call_args[0][0]
        assert "tail" in call_args or "/var/log/app.log" in call_args

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_read_log_with_lines(self, mock_ssh_class: MagicMock) -> None:
        """Should respect the lines parameter."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client

        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()
        stdout.read.return_value = b"log line 1\nlog line 2\n"
        stdout.channel.recv_exit_status.return_value = 0
        mock_client.exec_command.return_value = (stdin, stdout, stderr)

        result = ssh_read_log.invoke({
            "host": "test-server",
            "user": "deploy",
            "path": "/var/log/app.log",
            "lines": 100,
        })

        assert "log line 1" in result
        # Verify tail -100 was used
        call_args = mock_client.exec_command.call_args[0][0]
        assert "100" in call_args

    @patch("scenarios.bug_diagnoser.src.tools.ssh_tool.paramiko.SSHClient")
    def test_read_log_file_not_found(self, mock_ssh_class: MagicMock) -> None:
        """Should handle missing log files gracefully."""
        mock_client = MagicMock()
        mock_ssh_class.return_value = mock_client

        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()
        stdout.read.return_value = b""
        stderr.read.return_value = b"tail: cannot open '/nonexistent.log' for reading"
        stdout.channel.recv_exit_status.return_value = 1
        mock_client.exec_command.return_value = (stdin, stdout, stderr)

        result = ssh_read_log.invoke({
            "host": "test-server",
            "user": "deploy",
            "path": "/nonexistent.log",
        })

        assert "Error" in result or "failed" in result.lower() or "cannot" in result.lower()
