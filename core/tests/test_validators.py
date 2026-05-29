"""Tests for core.validators module."""

from __future__ import annotations

from pathlib import Path

from core.validators import (
    sanitize_path,
    validate_file_path,
    validate_host,
    validate_log_content,
    validate_port,
    validate_timeout,
)


class TestValidateFilePath:
    """Tests for validate_file_path function."""

    def test_valid_existing_file(self, tmp_path: Path) -> None:
        """Should validate an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        is_valid, error = validate_file_path(test_file)
        assert is_valid is True
        assert error == ""

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        """Should reject nonexistent file when must_exist=True."""
        is_valid, error = validate_file_path(tmp_path / "missing.txt")
        assert is_valid is False
        assert "does not exist" in error

    def test_nonexistent_file_allowed(self, tmp_path: Path) -> None:
        """Should accept nonexistent file when must_exist=False."""
        is_valid, error = validate_file_path(tmp_path / "missing.txt", must_exist=False)
        assert is_valid is True

    def test_directory_not_file(self, tmp_path: Path) -> None:
        """Should reject directory when must_be_file=True."""
        is_valid, error = validate_file_path(tmp_path, must_be_file=True)
        assert is_valid is False
        assert "not a file" in error


class TestValidateHost:
    """Tests for validate_host function."""

    def test_valid_hostname(self) -> None:
        """Should validate a valid hostname."""
        is_valid, error = validate_host("example.com")
        assert is_valid is True

    def test_valid_ip(self) -> None:
        """Should validate a valid IP address."""
        is_valid, error = validate_host("192.168.1.1")
        assert is_valid is True

    def test_empty_host(self) -> None:
        """Should reject empty host."""
        is_valid, error = validate_host("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_invalid_ip(self) -> None:
        """Should reject invalid IP address."""
        is_valid, error = validate_host("999.999.999.999")
        assert is_valid is False

    def test_localhost(self) -> None:
        """Should validate localhost."""
        is_valid, error = validate_host("localhost")
        assert is_valid is True


class TestValidatePort:
    """Tests for validate_port function."""

    def test_valid_port(self) -> None:
        """Should validate a valid port."""
        is_valid, error = validate_port(8080)
        assert is_valid is True

    def test_port_zero(self) -> None:
        """Should reject port 0."""
        is_valid, error = validate_port(0)
        assert is_valid is False

    def test_port_too_high(self) -> None:
        """Should reject port > 65535."""
        is_valid, error = validate_port(70000)
        assert is_valid is False

    def test_port_minimum(self) -> None:
        """Should accept port 1."""
        is_valid, error = validate_port(1)
        assert is_valid is True

    def test_port_maximum(self) -> None:
        """Should accept port 65535."""
        is_valid, error = validate_port(65535)
        assert is_valid is True


class TestValidateTimeout:
    """Tests for validate_timeout function."""

    def test_valid_timeout(self) -> None:
        """Should validate a valid timeout."""
        is_valid, error = validate_timeout(30)
        assert is_valid is True

    def test_negative_timeout(self) -> None:
        """Should reject negative timeout."""
        is_valid, error = validate_timeout(-1)
        assert is_valid is False
        assert "negative" in error.lower()

    def test_timeout_too_large(self) -> None:
        """Should reject timeout exceeding max."""
        is_valid, error = validate_timeout(400, max_timeout=300)
        assert is_valid is False
        assert "exceed" in error.lower()


class TestValidateLogContent:
    """Tests for validate_log_content function."""

    def test_valid_content(self) -> None:
        """Should validate valid log content."""
        is_valid, error = validate_log_content("Some log content")
        assert is_valid is True

    def test_empty_content(self) -> None:
        """Should reject empty content."""
        is_valid, error = validate_log_content("")
        assert is_valid is False
        assert "empty" in error.lower()


class TestSanitizePath:
    """Tests for sanitize_path function."""

    def test_normal_path(self) -> None:
        """Should keep normal path unchanged."""
        assert sanitize_path("/path/to/file") == "/path/to/file"

    def test_null_bytes(self) -> None:
        """Should remove null bytes."""
        assert sanitize_path("/path/to/\0file") == "/path/to/file"

    def test_double_slashes(self) -> None:
        """Should remove double slashes."""
        assert sanitize_path("/path//to//file") == "/path/to/file"

    def test_backslashes(self) -> None:
        """Should normalize backslashes."""
        assert sanitize_path("\\path\\to\\file") == "/path/to/file"

    def test_whitespace(self) -> None:
        """Should strip whitespace."""
        assert sanitize_path("  /path/to/file  ") == "/path/to/file"
