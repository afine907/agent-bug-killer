"""Custom exceptions for Agent Bug Killer.

Provides structured exceptions with helpful error messages.
"""

from __future__ import annotations


class AgentBugKillerError(Exception):
    """Base exception for Agent Bug Killer."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialize exception.

        Args:
            message: Human-readable error message.
            details: Optional dictionary with additional error details.
        """
        super().__init__(message)
        self.details = details or {}


class ConfigurationError(AgentBugKillerError):
    """Configuration-related errors."""

    pass


class ToolError(AgentBugKillerError):
    """Tool execution errors."""

    pass


class SSHError(ToolError):
    """SSH connection/execution errors."""

    pass


class CDPError(ToolError):
    """CDP (Chrome DevTools Protocol) errors."""

    pass


class ParseError(ToolError):
    """Log parsing errors."""

    pass


class ValidationError(AgentBugKillerError):
    """Input validation errors."""

    pass


class TimeoutError(AgentBugKillerError):
    """Operation timeout errors."""

    pass


class RetryExhaustedError(AgentBugKillerError):
    """All retry attempts exhausted."""

    def __init__(
        self,
        message: str,
        attempts: int,
        last_exception: Exception | None = None,
    ) -> None:
        """Initialize exception.

        Args:
            message: Human-readable error message.
            attempts: Number of attempts made.
            last_exception: The last exception that caused the failure.
        """
        super().__init__(
            message,
            details={
                "attempts": attempts,
                "last_exception": str(last_exception) if last_exception else None,
            },
        )
        self.attempts = attempts
        self.last_exception = last_exception


class ResourceNotFoundError(AgentBugKillerError):
    """Resource not found errors."""

    pass


def format_error(e: Exception) -> str:
    """Format an exception into a user-friendly message.

    Args:
        e: The exception to format.

    Returns:
        Formatted error message string.
    """
    if isinstance(e, AgentBugKillerError):
        msg = str(e)
        if e.details:
            details_str = ", ".join(f"{k}={v}" for k, v in e.details.items())
            msg += f" ({details_str})"
        return msg

    return f"{type(e).__name__}: {e}"
