"""Tests for core.rca_engine module."""

from __future__ import annotations

import pytest

from core.rca_engine import RCAEngine


@pytest.fixture
def engine() -> RCAEngine:
    """Create an RCAEngine instance."""
    return RCAEngine()


class TestRCAEngine:
    """Tests for RCAEngine class."""

    def test_analyze_empty_errors(self, engine: RCAEngine) -> None:
        """Should handle empty error list."""
        result = engine.analyze([])
        assert result.root_cause == "No errors to analyze"
        assert result.confidence == 0.0

    def test_analyze_single_error(self, engine: RCAEngine) -> None:
        """Should analyze single error."""
        errors = [{"message": "ConnectionRefused: cannot connect to database"}]
        result = engine.analyze(errors)
        assert result.category == "network"
        assert result.severity == "high"

    def test_analyze_multiple_errors(self, engine: RCAEngine) -> None:
        """Should analyze multiple errors."""
        errors = [
            {"message": "ConnectionRefused to db1"},
            {"message": "ConnectionRefused to db2"},
            {"message": "ConnectionRefused to db3"},
        ]
        result = engine.analyze(errors)
        assert result.category == "network"
        assert result.confidence > 0.5

    def test_analyze_mixed_errors(self, engine: RCAEngine) -> None:
        """Should analyze mixed error types."""
        errors = [
            {"message": "ConnectionRefused to database"},
            {"message": "OutOfMemory: heap space"},
            {"message": "Permission denied"},
        ]
        result = engine.analyze(errors)
        assert result.category in ["network", "resource", "security"]

    def test_analyze_with_context(self, engine: RCAEngine) -> None:
        """Should accept context."""
        errors = [{"message": "Error"}]
        context = {"service": "api", "environment": "production"}
        result = engine.analyze(errors, context=context)
        assert result is not None

    def test_result_has_evidence(self, engine: RCAEngine) -> None:
        """Should include evidence."""
        errors = [
            {"message": "ConnectionRefused to db"},
            {"message": "ConnectionRefused to cache"},
        ]
        result = engine.analyze(errors)
        assert len(result.evidence) > 0

    def test_result_has_fix_suggestions(self, engine: RCAEngine) -> None:
        """Should include fix suggestions."""
        errors = [{"message": "ConnectionRefused to database"}]
        result = engine.analyze(errors)
        assert len(result.fix_suggestions) > 0

    def test_confidence_range(self, engine: RCAEngine) -> None:
        """Confidence should be between 0 and 1."""
        errors = [{"message": "Test error"}]
        result = engine.analyze(errors)
        assert 0.0 <= result.confidence <= 1.0

    def test_analyze_database_errors(self, engine: RCAEngine) -> None:
        """Should categorize database errors."""
        errors = [
            {"message": "psycopg2.OperationalError: connection failed"},
            {"message": "SQL syntax error near SELECT"},
        ]
        result = engine.analyze(errors)
        assert result.category == "database"

    def test_analyze_resource_errors(self, engine: RCAEngine) -> None:
        """Should categorize resource errors."""
        errors = [
            {"message": "OutOfMemoryError: Java heap space"},
            {"message": "MemoryError: unable to allocate"},
        ]
        result = engine.analyze(errors)
        assert result.category == "resource"
