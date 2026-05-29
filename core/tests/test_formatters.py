"""Tests for core.formatters module."""

from __future__ import annotations

from typing import Any

import pytest

from core.formatters import format_html, format_json, format_markdown, format_report


@pytest.fixture
def sample_report() -> dict[str, Any]:
    """Return a sample diagnostic report."""
    return {
        "summary": "Database connection pool exhausted",
        "errors": [
            {
                "level": "ERROR",
                "message": "Pool exhausted",
                "source": "db.pool",
                "timestamp": "2024-01-15 14:35:01",
                "stack_trace": "ConnectionError: Pool exhausted",
            }
        ],
        "root_cause": "Connection pool size too small for traffic",
        "impact": "All API requests failing with 500",
        "recommendations": [
            "Increase pool size from 5 to 20",
            "Add connection pool monitoring",
        ],
        "urgency": "critical",
    }


class TestFormatJson:
    """Tests for format_json function."""

    def test_pretty_print(self, sample_report: dict[str, Any]) -> None:
        """Should produce pretty-printed JSON."""
        result = format_json(sample_report)
        assert "\n" in result
        assert "  " in result

    def test_compact(self, sample_report: dict[str, Any]) -> None:
        """Should produce compact JSON when pretty=False."""
        result = format_json(sample_report, pretty=False)
        assert "\n" not in result

    def test_valid_json(self, sample_report: dict[str, Any]) -> None:
        """Should produce valid JSON."""
        import json

        result = format_json(sample_report)
        parsed = json.loads(result)
        assert parsed["summary"] == "Database connection pool exhausted"


class TestFormatMarkdown:
    """Tests for format_markdown function."""

    def test_contains_title(self, sample_report: dict[str, Any]) -> None:
        """Should contain report title."""
        result = format_markdown(sample_report)
        assert "# Diagnostic Report" in result

    def test_contains_summary(self, sample_report: dict[str, Any]) -> None:
        """Should contain summary section."""
        result = format_markdown(sample_report)
        assert "## Summary" in result
        assert "Database connection pool exhausted" in result

    def test_contains_errors(self, sample_report: dict[str, Any]) -> None:
        """Should contain errors section."""
        result = format_markdown(sample_report)
        assert "## Errors" in result
        assert "Pool exhausted" in result

    def test_contains_root_cause(self, sample_report: dict[str, Any]) -> None:
        """Should contain root cause section."""
        result = format_markdown(sample_report)
        assert "## Root Cause" in result

    def test_contains_recommendations(self, sample_report: dict[str, Any]) -> None:
        """Should contain recommendations section."""
        result = format_markdown(sample_report)
        assert "## Recommendations" in result
        assert "Increase pool size" in result


class TestFormatHtml:
    """Tests for format_html function."""

    def test_contains_html_structure(self, sample_report: dict[str, Any]) -> None:
        """Should contain basic HTML structure."""
        result = format_html(sample_report)
        assert "<!DOCTYPE html>" in result
        assert "<html" in result
        assert "</html>" in result

    def test_contains_css(self, sample_report: dict[str, Any]) -> None:
        """Should contain CSS styles."""
        result = format_html(sample_report)
        assert "<style>" in result
        assert "font-family" in result


class TestFormatReport:
    """Tests for format_report function."""

    def test_json_format(self, sample_report: dict[str, Any]) -> None:
        """Should format as JSON."""
        result = format_report(sample_report, "json")
        assert result.startswith("{")

    def test_markdown_format(self, sample_report: dict[str, Any]) -> None:
        """Should format as Markdown."""
        result = format_report(sample_report, "markdown")
        assert "# Diagnostic Report" in result

    def test_md_alias(self, sample_report: dict[str, Any]) -> None:
        """Should support 'md' as alias for 'markdown'."""
        result = format_report(sample_report, "md")
        assert "# Diagnostic Report" in result

    def test_html_format(self, sample_report: dict[str, Any]) -> None:
        """Should format as HTML."""
        result = format_report(sample_report, "html")
        assert "<!DOCTYPE html>" in result

    def test_unsupported_format(self, sample_report: dict[str, Any]) -> None:
        """Should raise ValueError for unsupported format."""
        with pytest.raises(ValueError, match="Unsupported format"):
            format_report(sample_report, "xml")
