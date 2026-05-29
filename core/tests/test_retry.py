"""Tests for core.retry module."""

from __future__ import annotations

import pytest

from core.retry import retry


class TestRetryDecorator:
    """Tests for retry decorator."""

    def test_success_on_first_attempt(self) -> None:
        """Should return result on first successful attempt."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def successful_func() -> str:
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_on_failure(self) -> None:
        """Should retry on failure and succeed."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def failing_then_success() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = failing_then_success()
        assert result == "success"
        assert call_count == 3

    def test_max_attempts_exceeded(self) -> None:
        """Should raise exception after max attempts."""
        @retry(max_attempts=3, delay=0.01)
        def always_fails() -> None:
            raise ValueError("Permanent failure")

        with pytest.raises(ValueError, match="Permanent failure"):
            always_fails()

    def test_specific_exception_types(self) -> None:
        """Should only catch specified exception types."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def raises_type_error() -> str:
            nonlocal call_count
            call_count += 1
            raise TypeError("Wrong type")

        with pytest.raises(TypeError):
            raises_type_error()
        assert call_count == 1  # Should not retry

    def test_different_exception_types(self) -> None:
        """Should catch multiple exception types."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError, TypeError))
        def raises_value_error() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary")
            return "success"

        result = raises_value_error()
        assert result == "success"
        assert call_count == 3

    def test_preserves_function_metadata(self) -> None:
        """Should preserve function name and docstring."""
        @retry(max_attempts=3, delay=0.01)
        def documented_func() -> None:
            """This function has a docstring."""
            pass

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This function has a docstring."
