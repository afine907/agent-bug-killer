"""Tests for core.exceptions module."""

from __future__ import annotations

import pytest

from core.exceptions import (
    AgentBugKillerError,
    ConfigurationError,
    RetryExhaustedError,
    ValidationError,
    format_error,
)


class TestAgentBugKillerError:
    """Tests for AgentBugKillerError."""

    def test_basic_error(self) -> None:
        """Should create basic error."""
        error = AgentBugKillerError("Test error")
        assert str(error) == "Test error"
        assert error.details == {}

    def test_error_with_details(self) -> None:
        """Should create error with details."""
        error = AgentBugKillerError("Test error", details={"key": "value"})
        assert error.details == {"key": "value"}


class TestRetryExhaustedError:
    """Tests for RetryExhaustedError."""

    def test_basic_error(self) -> None:
        """Should create retry exhausted error."""
        error = RetryExhaustedError("All attempts failed", attempts=3)
        assert error.attempts == 3
        assert error.last_exception is None

    def test_error_with_last_exception(self) -> None:
        """Should include last exception."""
        last_exc = ValueError("Original error")
        error = RetryExhaustedError(
            "All attempts failed",
            attempts=3,
            last_exception=last_exc,
        )
        assert error.last_exception == last_exc
        assert "Original error" in str(error.details["last_exception"])


class TestFormatError:
    """Tests for format_error function."""

    def test_format_basic_error(self) -> None:
        """Should format basic error."""
        error = ValueError("Test error")
        result = format_error(error)
        assert "ValueError" in result
        assert "Test error" in result

    def test_format_agent_error(self) -> None:
        """Should format AgentBugKillerError."""
        error = AgentBugKillerError("Test error")
        result = format_error(error)
        assert result == "Test error"

    def test_format_agent_error_with_details(self) -> None:
        """Should include details in formatted message."""
        error = AgentBugKillerError("Test error", details={"key": "value"})
        result = format_error(error)
        assert "key=value" in result


class TestExceptionHierarchy:
    """Tests for exception hierarchy."""

    def test_configuration_error_is_agent_error(self) -> None:
        """ConfigurationError should be AgentBugKillerError."""
        error = ConfigurationError("Config error")
        assert isinstance(error, AgentBugKillerError)

    def test_validation_error_is_agent_error(self) -> None:
        """ValidationError should be AgentBugKillerError."""
        error = ValidationError("Validation error")
        assert isinstance(error, AgentBugKillerError)

    def test_catch_all_agent_errors(self) -> None:
        """Should catch all agent errors with base class."""
        errors = [
            ConfigurationError("config"),
            ValidationError("validation"),
            RetryExhaustedError("retry", attempts=1),
        ]

        for error in errors:
            with pytest.raises(AgentBugKillerError):
                raise error
