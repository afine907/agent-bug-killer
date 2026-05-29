"""Tests for core.progress module."""

from __future__ import annotations

from core.progress import ProgressTracker, Spinner, progress, spinner


class TestProgressTracker:
    """Tests for ProgressTracker class."""

    def test_initial_state(self) -> None:
        """Should initialize with correct values."""
        tracker = ProgressTracker(10, "Test")
        assert tracker.total == 10
        assert tracker.current == 0
        assert tracker.description == "Test"

    def test_update(self) -> None:
        """Should update progress."""
        tracker = ProgressTracker(10, "Test")
        tracker.update(3)
        assert tracker.current == 3

    def test_update_capped(self) -> None:
        """Should not exceed total."""
        tracker = ProgressTracker(10, "Test")
        tracker.update(15)
        assert tracker.current == 10

    def test_finish(self) -> None:
        """Should set current to total on finish."""
        tracker = ProgressTracker(10, "Test")
        tracker.update(5)
        tracker.finish()
        assert tracker.current == 10


class TestSpinner:
    """Tests for Spinner class."""

    def test_initial_state(self) -> None:
        """Should initialize with correct values."""
        s = Spinner("Test")
        assert s.description == "Test"
        assert s.running is False

    def test_start_stop(self) -> None:
        """Should start and stop correctly."""
        s = Spinner("Test")
        s.start()
        assert s.running is True
        s.stop()
        assert s.running is False


class TestProgressContextManager:
    """Tests for progress context manager."""

    def test_context_manager(self) -> None:
        """Should work as context manager."""
        with progress(10, "Test") as p:
            p.update(5)
            assert p.current == 5


class TestSpinnerContextManager:
    """Tests for spinner context manager."""

    def test_context_manager(self) -> None:
        """Should work as context manager."""
        with spinner("Test") as s:
            assert s.running is True
