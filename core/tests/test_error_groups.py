"""Tests for core.error_groups module."""

from __future__ import annotations

from core.error_groups import (
    ErrorGroup,
    compute_fingerprint,
    format_group_summary,
    get_top_groups,
    group_errors,
    normalize_error_message,
)


class TestNormalizeErrorMessage:
    """Tests for normalize_error_message function."""

    def test_remove_timestamps(self) -> None:
        """Should remove timestamps."""
        msg = "2024-01-15 10:30:00 ERROR Connection failed"
        result = normalize_error_message(msg)
        assert "2024-01-15" not in result
        assert "<TIMESTAMP>" in result

    def test_remove_uuids(self) -> None:
        """Should remove UUIDs."""
        msg = "Request abc12345-1234-1234-1234-123456789abc failed"
        result = normalize_error_message(msg)
        assert "abc12345-1234-1234-1234-123456789abc" not in result
        assert "<UUID>" in result

    def test_remove_hex_addresses(self) -> None:
        """Should remove hex addresses."""
        msg = "Memory access at 0x7fff5fbff8ac failed"
        result = normalize_error_message(msg)
        assert "0x7fff5fbff8ac" not in result
        assert "<HEX>" in result

    def test_remove_large_numbers(self) -> None:
        """Should remove large numbers (IDs)."""
        msg = "Order 123456789 not found"
        result = normalize_error_message(msg)
        assert "123456789" not in result
        assert "<ID>" in result

    def test_remove_file_paths(self) -> None:
        """Should remove file paths."""
        msg = "Error in /app/src/main.py line 42"
        result = normalize_error_message(msg)
        assert "/app/src/main.py" not in result
        assert "<PATH>" in result

    def test_remove_quoted_strings(self) -> None:
        """Should remove quoted strings."""
        msg = 'Cannot find user "john@example.com"'
        result = normalize_error_message(msg)
        assert "john@example.com" not in result

    def test_preserve_error_type(self) -> None:
        """Should preserve error type names."""
        msg = "ConnectionRefusedError: cannot connect"
        result = normalize_error_message(msg)
        assert "ConnectionRefusedError" in result


class TestComputeFingerprint:
    """Tests for compute_fingerprint function."""

    def test_same_message_same_fingerprint(self) -> None:
        """Should produce same fingerprint for same message."""
        fp1 = compute_fingerprint("Connection refused")
        fp2 = compute_fingerprint("Connection refused")
        assert fp1 == fp2

    def test_different_message_different_fingerprint(self) -> None:
        """Should produce different fingerprint for different message."""
        fp1 = compute_fingerprint("Connection refused")
        fp2 = compute_fingerprint("Timeout error")
        assert fp1 != fp2

    def test_normalized_message_same_fingerprint(self) -> None:
        """Should produce same fingerprint for normalized messages."""
        fp1 = compute_fingerprint("Request 123456 failed")
        fp2 = compute_fingerprint("Request 789012 failed")
        assert fp1 == fp2

    def test_with_stack_trace(self) -> None:
        """Should include stack trace in fingerprint."""
        fp1 = compute_fingerprint("Error", "File app.py line 10")
        fp2 = compute_fingerprint("Error", "File main.py line 20")
        assert fp1 != fp2

    def test_returns_hex_string(self) -> None:
        """Should return hex string."""
        fp = compute_fingerprint("test")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)


class TestGroupErrors:
    """Tests for group_errors function."""

    def test_group_similar_errors(self) -> None:
        """Should group similar errors together."""
        errors = [
            {"message": "Request 123456 failed", "timestamp": "2024-01-15T10:00:00"},
            {"message": "Request 789012 failed", "timestamp": "2024-01-15T10:01:00"},
            {"message": "Connection refused", "timestamp": "2024-01-15T10:02:00"},
        ]
        groups = group_errors(errors)
        assert len(groups) == 2  # Two distinct groups

    def test_group_count(self) -> None:
        """Should count errors in each group."""
        errors = [
            {"message": "Request 123456 failed"},
            {"message": "Request 789012 failed"},
            {"message": "Request 345678 failed"},
        ]
        groups = group_errors(errors)
        # All should be in same group (after normalization)
        assert len(groups) == 1
        group = list(groups.values())[0]
        assert group.count == 3

    def test_group_metadata(self) -> None:
        """Should preserve metadata from first error."""
        errors = [
            {"message": "Error", "level": "ERROR", "source": "app.py"},
        ]
        groups = group_errors(errors)
        group = list(groups.values())[0]
        assert group.metadata["level"] == "ERROR"
        assert group.metadata["source"] == "app.py"

    def test_empty_errors(self) -> None:
        """Should handle empty error list."""
        groups = group_errors([])
        assert len(groups) == 0


class TestGetTopGroups:
    """Tests for get_top_groups function."""

    def test_returns_sorted_by_count(self) -> None:
        """Should return groups sorted by count."""
        groups = {
            "a": ErrorGroup("a", "Error A", count=1),
            "b": ErrorGroup("b", "Error B", count=3),
            "c": ErrorGroup("c", "Error C", count=2),
        }
        top = get_top_groups(groups, limit=2)
        assert len(top) == 2
        assert top[0].count == 3
        assert top[1].count == 2

    def test_respects_limit(self) -> None:
        """Should respect limit parameter."""
        groups = {
            f"g{i}": ErrorGroup(f"g{i}", f"Error {i}", count=i)
            for i in range(10)
        }
        top = get_top_groups(groups, limit=5)
        assert len(top) == 5


class TestFormatGroupSummary:
    """Tests for format_group_summary function."""

    def test_format_basic(self) -> None:
        """Should format basic group."""
        group = ErrorGroup(
            fingerprint="abc123",
            title="Connection refused",
            count=5,
            first_seen="2024-01-15T10:00:00",
            last_seen="2024-01-15T11:00:00",
        )
        result = format_group_summary(group)
        assert "abc123" in result
        assert "Connection refused" in result
        assert "5" in result
