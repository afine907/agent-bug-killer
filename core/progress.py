"""Progress tracking utilities.

Provides progress indicators for long-running operations.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager


class ProgressTracker:
    """Track progress of multi-step operations."""

    def __init__(self, total: int, description: str = "Processing") -> None:
        """Initialize progress tracker.

        Args:
            total: Total number of steps.
            description: Description of the operation.
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self._last_update = 0.0

    def update(self, step: int = 1, status: str = "") -> None:
        """Update progress.

        Args:
            step: Number of steps completed.
            status: Optional status message.
        """
        self.current = min(self.current + step, self.total)
        self._display(status)

    def _display(self, status: str = "") -> None:
        """Display progress bar."""
        now = time.time()
        if now - self._last_update < 0.1 and self.current < self.total:
            return
        self._last_update = now

        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        bar_length = 30
        filled = int(bar_length * self.current / self.total) if self.total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        elapsed = time.time() - self.start_time
        eta = (elapsed / self.current * (self.total - self.current)) if self.current > 0 else 0

        line = f"\r{self.description}: [{bar}] {percent:.1f}% ({self.current}/{self.total})"
        if eta > 0:
            line += f" ETA: {eta:.0f}s"
        if status:
            line += f" - {status}"

        sys.stderr.write(line)
        sys.stderr.flush()

        if self.current >= self.total:
            sys.stderr.write("\n")

    def finish(self, message: str = "Complete") -> None:
        """Mark progress as complete.

        Args:
            message: Completion message.
        """
        self.current = self.total
        elapsed = time.time() - self.start_time
        sys.stderr.write(f"\r{self.description}: Complete ({elapsed:.1f}s)\n")
        sys.stderr.flush()


@contextmanager
def progress(
    total: int,
    description: str = "Processing",
) -> Iterator[ProgressTracker]:
    """Context manager for progress tracking.

    Args:
        total: Total number of steps.
        description: Description of the operation.

    Yields:
        ProgressTracker instance.
    """
    tracker = ProgressTracker(total, description)
    try:
        yield tracker
    finally:
        if tracker.current < tracker.total:
            tracker.finish()


class Spinner:
    """Simple spinner for indeterminate progress."""

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, description: str = "Working") -> None:
        """Initialize spinner.

        Args:
            description: Description to show alongside spinner.
        """
        self.description = description
        self.running = False
        self._frame = 0

    def _render(self) -> None:
        """Render current spinner frame."""
        frame = self.FRAMES[self._frame % len(self.FRAMES)]
        sys.stderr.write(f"\r{frame} {self.description}...")
        sys.stderr.flush()
        self._frame += 1

    def start(self) -> None:
        """Start the spinner."""
        self.running = True
        self._render()

    def stop(self, message: str = "Done") -> None:
        """Stop the spinner.

        Args:
            message: Message to show when stopped.
        """
        self.running = False
        sys.stderr.write(f"\r✓ {message}\n")
        sys.stderr.flush()


@contextmanager
def spinner(description: str = "Working") -> Iterator[Spinner]:
    """Context manager for spinner.

    Args:
        description: Description to show alongside spinner.

    Yields:
        Spinner instance.
    """
    s = Spinner(description)
    s.start()
    try:
        yield s
    finally:
        s.stop()
