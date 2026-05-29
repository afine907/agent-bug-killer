"""Tests for log_analyzer CLI."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from scenarios.log_analyzer.cli import analyze


@pytest.fixture
def runner() -> CliRunner:
    """Create a Click test runner."""
    return CliRunner()


@pytest.fixture
def sample_log_file(tmp_path: Path) -> Path:
    """Create a sample log file for testing."""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2024-01-15 10:00:00 ERROR [app] Test error\n"
        "2024-01-15 10:00:01 INFO [app] Test info\n",
        encoding="utf-8",
    )
    return log_file


class TestAnalyzeCommand:
    """Tests for the analyze CLI command."""

    def test_no_input_shows_error(self, runner: CliRunner) -> None:
        """Should show error when no input provided."""
        result = runner.invoke(analyze)
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_analyze_file(self, runner: CliRunner, sample_log_file: Path) -> None:
        """Should analyze a log file."""
        result = runner.invoke(analyze, ["--file", str(sample_log_file)])
        assert result.exit_code == 0
        assert "Found" in result.output

    def test_analyze_text(self, runner: CliRunner) -> None:
        """Should analyze log text."""
        result = runner.invoke(analyze, ["--text", "2024-01-15 10:00:00 ERROR [app] Test"])
        assert result.exit_code == 0

    def test_nonexistent_file(self, runner: CliRunner) -> None:
        """Should show error for nonexistent file."""
        result = runner.invoke(analyze, ["--file", "/nonexistent/file.log"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower() or "Error" in result.output

    def test_output_json_format(
        self, runner: CliRunner, sample_log_file: Path, tmp_path: Path
    ) -> None:
        """Should output JSON format."""
        output_file = tmp_path / "output.json"
        result = runner.invoke(analyze, [
            "--file", str(sample_log_file),
            "--output", str(output_file),
            "--format", "json",
        ])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_output_markdown_format(
        self, runner: CliRunner, sample_log_file: Path, tmp_path: Path
    ) -> None:
        """Should output Markdown format."""
        output_file = tmp_path / "output.md"
        result = runner.invoke(analyze, [
            "--file", str(sample_log_file),
            "--output", str(output_file),
            "--format", "markdown",
        ])
        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Diagnostic Report" in content

    def test_no_errors_found(self, runner: CliRunner, tmp_path: Path) -> None:
        """Should show message when no errors found."""
        log_file = tmp_path / "clean.log"
        log_file.write_text("2024-01-15 10:00:00 INFO [app] All good\n", encoding="utf-8")
        result = runner.invoke(analyze, ["--file", str(log_file)])
        assert result.exit_code == 0
        assert "No errors" in result.output
