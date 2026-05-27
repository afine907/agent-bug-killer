"""Shared test fixtures for bug-diagnoser scenario."""

import pytest


@pytest.fixture
def mock_ssh_client():
    """Return a mock SSH client."""
    from unittest.mock import MagicMock

    client = MagicMock()
    stdin = MagicMock()
    stdout = MagicMock()
    stderr = MagicMock()
    stdout.read.return_value = b"command output"
    stderr.read.return_value = b""
    client.exec_command.return_value = (stdin, stdout, stderr)
    return client


@pytest.fixture
def sample_server_info():
    """Return sample server connection info."""
    return {
        "host": "test-server.example.com",
        "user": "deploy",
        "key_path": "/home/user/.ssh/id_rsa",
        "port": 22,
    }
