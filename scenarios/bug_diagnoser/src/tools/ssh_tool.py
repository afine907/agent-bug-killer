"""SSH tools for remote command execution and log reading."""

from __future__ import annotations

import shlex

import paramiko
from langchain_core.tools import tool

from core.settings import settings


@tool
def ssh_exec(
    host: str,
    user: str,
    command: str,
    key_path: str = "",
    port: int = 22,
    timeout: int = 0,
) -> str:
    """Execute a command on a remote server via SSH.

    Args:
        host: Hostname or IP of the remote server.
        user: SSH username.
        command: Command to execute on the remote server.
        key_path: Path to SSH private key. If empty, uses default key.
        port: SSH port number.
        timeout: Connection timeout in seconds. 0 uses settings default.

    Returns:
        Command output as a string, or error message.
    """
    if timeout <= 0:
        timeout = settings.ssh_timeout

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        connect_kwargs: dict = {
            "hostname": host,
            "port": port,
            "username": user,
            "timeout": timeout,
        }
        if key_path:
            connect_kwargs["key_filename"] = key_path

        client.connect(**connect_kwargs)
        _, stdout, stderr = client.exec_command(command, timeout=timeout)

        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode("utf-8", errors="replace")
        error_output = stderr.read().decode("utf-8", errors="replace")

        if exit_status != 0:
            return f"Command failed (exit code {exit_status}):\n{error_output or output}"

        return output

    except Exception as e:
        return f"Error connecting to {host}: {e}"
    finally:
        client.close()


@tool
def ssh_read_log(
    host: str,
    user: str,
    path: str,
    lines: int = 100,
    key_path: str = "",
    port: int = 22,
    timeout: int = 0,
) -> str:
    """Read the last N lines of a log file on a remote server via SSH.

    Args:
        host: Hostname or IP of the remote server.
        user: SSH username.
        path: Path to the log file on the remote server.
        lines: Number of lines to read from the end of the file (1-10000).
        key_path: Path to SSH private key. If empty, uses default key.
        port: SSH port number.
        timeout: Connection timeout in seconds. 0 uses settings default.

    Returns:
        The last N lines of the log file, or error message.
    """
    lines = max(1, min(lines, 10000))
    safe_path = shlex.quote(path)
    command = f"tail -n {lines} {safe_path}"
    return ssh_exec.invoke({
        "host": host,
        "user": user,
        "command": command,
        "key_path": key_path,
        "port": port,
        "timeout": timeout,
    })
