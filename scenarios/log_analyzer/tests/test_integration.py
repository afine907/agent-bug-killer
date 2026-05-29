"""Integration tests for Log Analyzer scenario.

Tests the full flow: file_reader → log_parser → structured output.
These tests use real tool calls (no mocks) to verify tool interoperability.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scenarios.log_analyzer.src.tools.file_reader import file_reader
from scenarios.log_analyzer.src.tools.log_parser import log_parser


@pytest.mark.integration
class TestFileReaderToLogParser:
    """Test file_reader and log_parser working together."""

    def test_read_and_parse_real_log_file(self, tmp_path: Path) -> None:
        """Should read a log file and parse errors from it."""
        log_content = (
            "2024-01-15 10:30:15,123 ERROR [web.app] Request failed\n"
            "Traceback (most recent call last):\n"
            '  File "/app/views.py", line 42, in handle_request\n'
            "    result = process_data(request.data)\n"
            "ValueError: Invalid JSON payload\n"
            "\n"
            "2024-01-15 10:30:16,000 INFO [web.app] Request completed\n"
        )
        log_file = tmp_path / "app.log"
        log_file.write_text(log_content, encoding="utf-8")

        # Step 1: Read file
        read_result = file_reader.invoke({"file_path": str(log_file)})
        assert "ERROR" in read_result

        # Step 2: Parse errors from read content
        parse_result = log_parser.invoke({"content": read_result})
        assert isinstance(parse_result, list)
        assert len(parse_result) >= 1

        error_entries = [e for e in parse_result if e.get("level") == "ERROR"]
        assert len(error_entries) >= 1
        assert "Request failed" in error_entries[0]["message"]

    def test_read_and_parse_empty_file(self, tmp_path: Path) -> None:
        """Should handle empty log file gracefully."""
        log_file = tmp_path / "empty.log"
        log_file.write_text("", encoding="utf-8")

        read_result = file_reader.invoke({"file_path": str(log_file)})
        parse_result = log_parser.invoke({"content": read_result})
        assert isinstance(parse_result, list)
        assert len(parse_result) == 0

    def test_read_and_parse_multiline_traceback(self, tmp_path: Path) -> None:
        """Should correctly chain through multiline stack traces."""
        log_content = (
            "2024-01-15 11:00:00,001 ERROR [db.connection] Connection failed\n"
            "Traceback (most recent call last):\n"
            '  File "/app/db/pool.py", line 15, in get_connection\n'
            "    conn = psycopg2.connect(self.dsn)\n"
            '  File "/app/db/pool.py", line 28, in connect\n'
            '    raise ConnectionError(f"Cannot connect to {host}:{port}")\n'
            "ConnectionError: Cannot connect to db-primary:5432\n"
        )
        log_file = tmp_path / "db.log"
        log_file.write_text(log_content, encoding="utf-8")

        read_result = file_reader.invoke({"file_path": str(log_file)})
        parse_result = log_parser.invoke({"content": read_result})

        assert isinstance(parse_result, list)
        error_entries = [e for e in parse_result if e.get("level") == "ERROR"]
        assert len(error_entries) >= 1
        assert "Connection failed" in error_entries[0]["message"]

    def test_read_nonexistent_file_returns_error(self) -> None:
        """Should return error message for missing file."""
        result = file_reader.invoke({"file_path": "/nonexistent/path/app.log"})
        assert "not found" in result.lower() or "error" in result.lower()

    def test_read_and_parse_mixed_levels(self, tmp_path: Path) -> None:
        """Should focus on ERROR entries when parsing mixed-level logs."""
        log_content = (
            "2024-01-15 12:00:00,001 INFO [startup] Application starting\n"
            "2024-01-15 12:00:01,002 DEBUG [config] Loading config\n"
            "2024-01-15 12:00:02,003 WARNING [scheduler] Queue depth 45/50\n"
            "2024-01-15 12:00:03,004 ERROR [scheduler] Task timeout after 30s\n"
            "2024-01-15 12:00:04,005 ERROR [worker] Worker OOM killed\n"
        )
        log_file = tmp_path / "mixed.log"
        log_file.write_text(log_content, encoding="utf-8")

        read_result = file_reader.invoke({"file_path": str(log_file)})
        parse_result = log_parser.invoke({"content": read_result})

        assert isinstance(parse_result, list)
        error_entries = [e for e in parse_result if e.get("level") == "ERROR"]
        assert len(error_entries) == 2
        assert "Task timeout" in error_entries[0]["message"]
        assert "OOM" in error_entries[1]["message"]


@pytest.mark.integration
class TestLogParserEdgeCases:
    """Test log_parser with various real-world log formats."""

    def test_parse_java_stack_trace(self) -> None:
        """Should handle Java-style stack traces."""
        content = (
            "2024-01-15 10:00:00 ERROR com.example.App - NullPointerException\n"
            "java.lang.NullPointerException: Cannot invoke method on null\n"
            "\tat com.example.App.process(App.java:42)\n"
            "\tat com.example.App.main(App.java:10)\n"
        )
        result = log_parser.invoke({"content": content})
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["level"] == "ERROR"

    def test_parse_json_log_format(self) -> None:
        """Should handle JSON-formatted log lines (returns empty as format is unsupported)."""
        content = (
            '{"level":"ERROR","time":"2024-01-15T10:00:00Z",'
            '"msg":"Connection refused","host":"db.local"}\n'
        )
        result = log_parser.invoke({"content": content})
        assert isinstance(result, list)
        # JSON format is not matched by the regex parser

    def test_parse_single_line_error(self) -> None:
        """Should handle single-line error messages."""
        content = "2024-01-15 10:00:00 ERROR [disk] Disk space critically low\n"
        result = log_parser.invoke({"content": content})
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["level"] == "ERROR"
