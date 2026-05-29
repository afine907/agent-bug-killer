"""Edge case tests for core modules.

Tests boundary conditions and unusual inputs.
"""

from __future__ import annotations

from core.analyzer import analyze_error
from core.formatters import format_json, format_markdown
from core.validators import sanitize_path, validate_file_path, validate_host


class TestAnalyzerEdgeCases:
    """Edge cases for error analyzer."""

    def test_empty_message(self) -> None:
        """Should handle empty error message."""
        result = analyze_error("")
        assert result.error_type == "Unknown"

    def test_very_long_message(self) -> None:
        """Should handle very long error message."""
        long_message = "Error: " + "x" * 10000
        result = analyze_error(long_message)
        assert result is not None

    def test_unicode_message(self) -> None:
        """Should handle unicode in error message."""
        result = analyze_error("错误: 连接被拒绝")
        assert result is not None

    def test_special_characters(self) -> None:
        """Should handle special characters."""
        result = analyze_error("Error: <script>alert('xss')</script>")
        assert result is not None

    def test_multiple_patterns(self) -> None:
        """Should match first pattern when multiple match."""
        # ConnectionRefused should match before Timeout
        result = analyze_error("ConnectionRefused: timeout waiting for response")
        assert result.error_type == "ConnectionRefused"


class TestFormatterEdgeCases:
    """Edge cases for formatters."""

    def test_empty_report(self) -> None:
        """Should handle empty report."""
        result = format_json({})
        assert result == "{}"

    def test_nested_empty(self) -> None:
        """Should handle nested empty structures."""
        report = {"errors": [], "findings": []}
        result = format_markdown(report)
        assert "0" in result

    def test_none_values(self) -> None:
        """Should handle None values."""
        report = {"summary": None, "errors": None}
        # Should not crash
        result = format_json(report)
        assert result is not None

    def test_large_report(self) -> None:
        """Should handle large reports."""
        report = {
            "summary": "Test",
            "errors": [{"level": "ERROR", "message": f"Error {i}"} for i in range(1000)],
        }
        result = format_json(report)
        assert len(result) > 0


class TestValidatorEdgeCases:
    """Edge cases for validators."""

    def test_empty_path(self) -> None:
        """Should handle empty path."""
        is_valid, error = validate_file_path("", must_exist=False)
        # Empty path is technically valid when not checking existence
        assert is_valid is True

    def test_whitespace_host(self) -> None:
        """Should handle whitespace-only host."""
        is_valid, error = validate_host("   ")
        assert is_valid is False

    def test_very_long_host(self) -> None:
        """Should handle very long hostname."""
        long_host = "a" * 256 + ".com"
        is_valid, error = validate_host(long_host)
        # Should be invalid (too long)
        assert is_valid is False

    def test_path_with_spaces(self) -> None:
        """Should handle paths with spaces."""
        result = sanitize_path("/path with spaces/file.txt")
        assert result == "/path with spaces/file.txt"

    def test_path_with_dots(self) -> None:
        """Should handle paths with dots."""
        result = sanitize_path("/path/../file.txt")
        # Should keep the dots (not our job to resolve)
        assert "../file.txt" in result

    def test_mixed_separators(self) -> None:
        """Should handle mixed path separators."""
        result = sanitize_path("/path\\to/file.txt")
        assert "\\" not in result
