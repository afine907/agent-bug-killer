"""Tests for core.history module."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.history import DiagnosticHistory


@pytest.fixture
def history(tmp_path: Path) -> DiagnosticHistory:
    """Create a DiagnosticHistory with temp directory."""
    return DiagnosticHistory(storage_dir=tmp_path / "diagnostics")


@pytest.fixture
def sample_report() -> dict:
    """Return a sample diagnostic report."""
    return {
        "summary": "Database connection failed",
        "errors": [{"level": "ERROR", "message": "Connection refused"}],
        "root_cause": "Database server down",
        "recommendations": ["Restart database"],
    }


class TestDiagnosticHistory:
    """Tests for DiagnosticHistory class."""

    def test_save_and_load(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should save and load a report."""
        report_id = history.save(sample_report)
        assert report_id is not None

        loaded = history.load(report_id)
        assert loaded is not None
        assert loaded["report"]["summary"] == "Database connection failed"

    def test_save_with_metadata(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should save metadata alongside report."""
        metadata = {"bug": "DB connection error", "source": "api"}
        report_id = history.save(sample_report, metadata=metadata)

        loaded = history.load(report_id)
        assert loaded is not None
        assert loaded["metadata"]["bug"] == "DB connection error"

    def test_load_nonexistent(self, history: DiagnosticHistory) -> None:
        """Should return None for nonexistent report."""
        assert history.load("nonexistent") is None

    def test_list_reports(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should list saved reports."""
        history.save(sample_report)
        history.save(sample_report)

        reports = history.list_reports()
        assert len(reports) == 2
        assert all("id" in r for r in reports)

    def test_list_reports_with_limit(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should respect limit parameter."""
        for _ in range(5):
            history.save(sample_report)

        reports = history.list_reports(limit=3)
        assert len(reports) == 3

    def test_delete_report(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should delete a report."""
        report_id = history.save(sample_report)
        assert history.delete(report_id) is True
        assert history.load(report_id) is None

    def test_delete_nonexistent(self, history: DiagnosticHistory) -> None:
        """Should return False for nonexistent report."""
        assert history.delete("nonexistent") is False

    def test_search_reports(
        self, history: DiagnosticHistory
    ) -> None:
        """Should search reports by query."""
        history.save(
            {"summary": "Database connection failed"},
            metadata={"bug": "DB error"},
        )
        history.save(
            {"summary": "API timeout"},
            metadata={"bug": "Network issue"},
        )

        results = history.search("database")
        assert len(results) == 1
        assert "Database" in results[0]["summary"]

    def test_search_case_insensitive(
        self, history: DiagnosticHistory, sample_report: dict
    ) -> None:
        """Should perform case-insensitive search."""
        history.save(sample_report)

        results = history.search("DATABASE")
        assert len(results) == 1
