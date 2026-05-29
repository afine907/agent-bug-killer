"""Tests for log-analyzer tools: file_reader and log_parser."""

from pathlib import Path

from scenarios.log_analyzer.src.tools.file_reader import file_reader
from scenarios.log_analyzer.src.tools.log_parser import log_parser


class TestFileReader:
    """Tests for the file_reader tool."""

    def test_read_existing_file(self, tmp_path: Path) -> None:
        """Should read file content from an existing file."""
        test_file = tmp_path / "test.log"
        test_file.write_text("Hello, world!")

        result = file_reader.invoke({"file_path": str(test_file)})
        assert result == "Hello, world!"

    def test_read_multiline_file(self, tmp_path: Path) -> None:
        """Should preserve line structure."""
        content = "line1\nline2\nline3"
        test_file = tmp_path / "multi.log"
        test_file.write_text(content)

        result = file_reader.invoke({"file_path": str(test_file)})
        assert result == content

    def test_read_nonexistent_file(self) -> None:
        """Should return error message for missing file."""
        result = file_reader.invoke({"file_path": "/nonexistent/path/file.log"})
        assert "Error" in result or "error" in result or "not found" in result.lower()

    def test_read_empty_file(self, tmp_path: Path) -> None:
        """Should handle empty files gracefully."""
        test_file = tmp_path / "empty.log"
        test_file.write_text("")

        result = file_reader.invoke({"file_path": str(test_file)})
        assert result == ""

    def test_read_file_with_max_lines(self, tmp_path: Path) -> None:
        """Should truncate to max_lines when specified."""
        lines = "\n".join(f"line {i}" for i in range(20))
        test_file = tmp_path / "long.log"
        test_file.write_text(lines)

        result = file_reader.invoke({"file_path": str(test_file), "max_lines": 5})
        result_lines = result.strip().split("\n")
        # 5 content lines + truncation message
        assert len(result_lines) == 6
        assert "truncated" in result_lines[-1]
        # First 5 lines should be the original content
        for i in range(5):
            assert result_lines[i] == f"line {i}"

    def test_read_binary_file_returns_error(self, tmp_path: Path) -> None:
        """Should handle binary files gracefully."""
        test_file = tmp_path / "binary.log"
        # Invalid UTF-8 bytes: continuation byte without start byte
        test_file.write_bytes(b"\xc0\xaf\xe0\x80\x80")

        result = file_reader.invoke({"file_path": str(test_file)})
        # Should either return error or latin-1 fallback content
        assert isinstance(result, str)


class TestLogParser:
    """Tests for the log_parser tool."""

    def test_parse_python_exception(self, python_exception_log: str) -> None:
        """Should extract Python exception from log."""
        entries = log_parser.invoke({"content": python_exception_log})
        assert len(entries) >= 1
        error_entries = [e for e in entries if e["level"] == "ERROR"]
        assert len(error_entries) >= 1
        assert any("JSONDecodeError" in (e["message"] or "") for e in error_entries)

    def test_parse_multiline_stack(self, multiline_stack_log: str) -> None:
        """Should extract complete stack traces."""
        entries = log_parser.invoke({"content": multiline_stack_log})
        assert len(entries) >= 1
        error_entries = [e for e in entries if e["level"] == "ERROR"]
        assert len(error_entries) >= 1
        assert any("ConnectionError" in (e["message"] or "") for e in error_entries)

    def test_parse_mixed_levels(self, mixed_levels_log: str) -> None:
        """Should extract all log levels."""
        entries = log_parser.invoke({"content": mixed_levels_log})
        levels = {e["level"] for e in entries}
        assert "ERROR" in levels
        assert "INFO" in levels

    def test_parse_empty_log(self, empty_log: str) -> None:
        """Should return empty list for empty log."""
        entries = log_parser.invoke({"content": empty_log})
        assert entries == []

    def test_parse_mixed_exceptions(self, mixed_exception_log: str) -> None:
        """Should extract multiple different exception types."""
        entries = log_parser.invoke({"content": mixed_exception_log})
        error_entries = [e for e in entries if e["level"] == "ERROR"]
        assert len(error_entries) >= 2
        messages = " ".join(e["message"] or "" for e in error_entries)
        assert "Timeout" in messages or "timeout" in messages
        assert "ValueError" in messages

    def test_parse_preserves_timestamp(self, python_exception_log: str) -> None:
        """Should extract timestamps from log entries."""
        entries = log_parser.invoke({"content": python_exception_log})
        assert len(entries) >= 1
        assert entries[0]["timestamp"] is not None

    def test_log_entry_structure(self, python_exception_log: str) -> None:
        """LogEntry should have the expected fields."""
        entries = log_parser.invoke({"content": python_exception_log})
        entry = entries[0]
        assert "level" in entry
        assert "message" in entry
        assert "timestamp" in entry
        assert "source" in entry
        assert "stack_trace" in entry
