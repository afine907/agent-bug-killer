"""Tests for core.fix_suggestions module."""

from __future__ import annotations

from core.analyzer import AnalysisResult
from core.fix_suggestions import (
    FixSuggestion,
    format_suggestions_markdown,
    generate_fix_suggestions,
)


class TestGenerateFixSuggestions:
    """Tests for generate_fix_suggestions function."""

    def test_connection_refused(self) -> None:
        """Should generate suggestions for connection refused."""
        analysis = AnalysisResult(
            error_type="ConnectionRefused",
            category="network",
            severity="high",
            confidence=0.8,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions) > 0
        assert suggestions[0].priority == "high"

    def test_timeout(self) -> None:
        """Should generate suggestions for timeout."""
        analysis = AnalysisResult(
            error_type="Timeout",
            category="network",
            severity="medium",
            confidence=0.8,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions) > 0

    def test_out_of_memory(self) -> None:
        """Should generate suggestions for OOM."""
        analysis = AnalysisResult(
            error_type="OutOfMemory",
            category="resource",
            severity="critical",
            confidence=0.8,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions) > 0
        assert suggestions[0].priority == "high"

    def test_null_pointer(self) -> None:
        """Should generate suggestions for null pointer."""
        analysis = AnalysisResult(
            error_type="NullPointer",
            category="code",
            severity="high",
            confidence=0.8,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions) > 0
        assert suggestions[0].code_example is not None

    def test_unknown_error(self) -> None:
        """Should generate generic suggestions for unknown errors."""
        analysis = AnalysisResult(
            error_type="Unknown",
            category="unknown",
            severity="medium",
            confidence=0.1,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions) > 0
        assert "Manual" in suggestions[0].title

    def test_suggestion_has_steps(self) -> None:
        """Should include steps in suggestions."""
        analysis = AnalysisResult(
            error_type="ConnectionRefused",
            category="network",
            severity="high",
            confidence=0.8,
        )
        suggestions = generate_fix_suggestions(analysis)
        assert len(suggestions[0].steps) > 0


class TestFormatSuggestionsMarkdown:
    """Tests for format_suggestions_markdown function."""

    def test_format_empty(self) -> None:
        """Should handle empty suggestions."""
        result = format_suggestions_markdown([])
        assert "No fix suggestions" in result

    def test_format_with_suggestions(self) -> None:
        """Should format suggestions as markdown."""
        suggestions = [
            FixSuggestion(
                title="Fix connection",
                description="Check the connection",
                priority="high",
                effort="small",
                steps=["Step 1", "Step 2"],
            ),
        ]
        result = format_suggestions_markdown(suggestions)
        assert "## Fix Suggestions" in result
        assert "Fix connection" in result
        assert "Step 1" in result

    def test_format_with_code_example(self) -> None:
        """Should include code examples."""
        suggestions = [
            FixSuggestion(
                title="Add null check",
                description="Check for null",
                priority="high",
                effort="small",
                code_example="if x is not None:\n    process(x)",
            ),
        ]
        result = format_suggestions_markdown(suggestions)
        assert "```" in result
        assert "if x is not None" in result
