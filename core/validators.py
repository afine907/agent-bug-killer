"""Input validation utilities.

Provides validators for common inputs like file paths, hosts, ports, etc.
"""

from __future__ import annotations

import re
from pathlib import Path


def validate_file_path(
    path: str | Path,
    must_exist: bool = True,
    must_be_file: bool = True,
) -> tuple[bool, str]:
    """Validate a file path.

    Args:
        path: The file path to validate.
        must_exist: Whether the path must exist.
        must_be_file: Whether the path must be a file (not directory).

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    p = Path(path)

    if must_exist and not p.exists():
        return False, f"Path does not exist: {path}"

    if must_exist and must_be_file and not p.is_file():
        return False, f"Path is not a file: {path}"

    return True, ""


def validate_host(host: str) -> tuple[bool, str]:
    """Validate a hostname or IP address.

    Args:
        host: The hostname or IP to validate.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    if not host:
        return False, "Host cannot be empty"

    # Check for valid hostname pattern
    hostname_pattern = re.compile(
        r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
    )

    # Check for valid IP pattern
    ip_pattern = re.compile(
        r"^(\d{1,3}\.){3}\d{1,3}$"
    )

    if hostname_pattern.match(host) or ip_pattern.match(host):
        # Additional check for IP address ranges
        if ip_pattern.match(host):
            parts = host.split(".")
            for part in parts:
                if int(part) > 255:
                    return False, f"Invalid IP address: {host}"
        return True, ""

    return False, f"Invalid hostname or IP: {host}"


def validate_port(port: int) -> tuple[bool, str]:
    """Validate a port number.

    Args:
        port: The port number to validate.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    if not 1 <= port <= 65535:
        return False, f"Port must be between 1 and 65535, got {port}"
    return True, ""


def validate_timeout(timeout: int, max_timeout: int = 300) -> tuple[bool, str]:
    """Validate a timeout value.

    Args:
        timeout: The timeout in seconds.
        max_timeout: Maximum allowed timeout.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    if timeout < 0:
        return False, f"Timeout cannot be negative, got {timeout}"
    if timeout > max_timeout:
        return False, f"Timeout cannot exceed {max_timeout}s, got {timeout}"
    return True, ""


def validate_log_content(content: str) -> tuple[bool, str]:
    """Validate log content for parsing.

    Args:
        content: The log content to validate.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    if not content:
        return False, "Log content cannot be empty"

    if len(content) > 10_000_000:  # 10MB limit
        return False, "Log content too large (max 10MB)"

    return True, ""


def sanitize_path(path: str) -> str:
    """Sanitize a file path to prevent path traversal.

    Args:
        path: The path to sanitize.

    Returns:
        Sanitized path string.
    """
    # Remove null bytes
    path = path.replace("\0", "")

    # Normalize path separators
    path = path.replace("\\", "/")

    # Remove double slashes
    while "//" in path:
        path = path.replace("//", "/")

    # Remove leading/trailing whitespace
    path = path.strip()

    return path
