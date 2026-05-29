"""Tests for core.analyzer module."""

from __future__ import annotations

from core.analyzer import (
    AnalysisResult,
    analyze_error,
    analyze_errors,
    get_severity_summary,
)


class TestAnalyzeError:
    """Tests for analyze_error function."""

    def test_connection_refused(self) -> None:
        """Should detect connection refused errors."""
        result = analyze_error("ConnectionRefused: cannot connect to localhost:5432")
        assert result.error_type == "ConnectionRefused"
        assert result.category == "network"
        assert result.severity == "high"
        assert len(result.common_causes) > 0
        assert len(result.fix_suggestions) > 0

    def test_timeout(self) -> None:
        """Should detect timeout errors."""
        result = analyze_error("Request timed out after 30 seconds")
        assert result.error_type == "Timeout"
        assert result.category == "network"

    def test_out_of_memory(self) -> None:
        """Should detect OOM errors."""
        result = analyze_error("java.lang.OutOfMemoryError: Java heap space")
        assert result.error_type == "OutOfMemory"
        assert result.severity == "critical"

    def test_null_pointer(self) -> None:
        """Should detect null pointer errors."""
        result = analyze_error("TypeError: Cannot read properties of undefined (reading 'map')")
        assert result.error_type == "NullPointer"
        assert result.category == "code"

    def test_permission_denied(self) -> None:
        """Should detect permission errors."""
        result = analyze_error("403 Forbidden: access denied")
        assert result.error_type == "PermissionDenied"
        assert result.category == "security"

    def test_disk_full(self) -> None:
        """Should detect disk full errors."""
        result = analyze_error("OSError: [Errno 28] No space left on device")
        assert result.error_type == "DiskFull"
        assert result.severity == "critical"

    def test_database_error(self) -> None:
        """Should detect database errors."""
        result = analyze_error("psycopg2.OperationalError: connection to server failed")
        assert result.error_type == "DatabaseError"
        assert result.category == "database"

    def test_unknown_error(self) -> None:
        """Should handle unknown error patterns."""
        result = analyze_error("Something weird happened")
        assert result.error_type == "Unknown"
        assert result.confidence == 0.1

    def test_case_insensitive(self) -> None:
        """Should match patterns case-insensitively."""
        result = analyze_error("CONNECTION REFUSED to database")
        assert result.error_type == "ConnectionRefused"


class TestAnalyzeErrors:
    """Tests for analyze_errors function."""

    def test_multiple_errors(self) -> None:
        """Should analyze multiple errors."""
        errors = [
            {"message": "Connection refused to db"},
            {"message": "Request timed out"},
            {"message": "Out of memory"},
        ]
        results = analyze_errors(errors)
        assert len(results) == 3
        assert results[0].error_type == "ConnectionRefused"
        assert results[1].error_type == "Timeout"
        assert results[2].error_type == "OutOfMemory"

    def test_empty_errors(self) -> None:
        """Should handle empty error list."""
        results = analyze_errors([])
        assert results == []

    def test_missing_message(self) -> None:
        """Should skip errors without message."""
        errors = [{"level": "ERROR"}, {"message": "Connection refused"}]
        results = analyze_errors(errors)
        assert len(results) == 1


class TestGetSeveritySummary:
    """Tests for get_severity_summary function."""

    def test_severity_counts(self) -> None:
        """Should count errors by severity."""
        results = [
            AnalysisResult("A", "network", "high", confidence=0.8),
            AnalysisResult("B", "network", "high", confidence=0.8),
            AnalysisResult("C", "resource", "critical", confidence=0.8),
        ]
        summary = get_severity_summary(results)
        assert summary["high"] == 2
        assert summary["critical"] == 1

    def test_empty_results(self) -> None:
        """Should handle empty results."""
        summary = get_severity_summary([])
        assert summary == {}
