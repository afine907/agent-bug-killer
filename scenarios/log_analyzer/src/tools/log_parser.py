"""Log parser tool for extracting errors and stack traces from logs."""

from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_core.tools import tool

# Pattern for standard log lines: 2024-01-15 10:30:15,123 LEVEL [module] message
LOG_LINE_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[,\s]*\d{0,3})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\s+"
    r"(?:\[(?P<source>[^\]]*)\]\s+)?"
    r"(?P<message>.+)$",
    re.MULTILINE,
)

# Pattern for Python exception lines
EXCEPTION_PATTERN = re.compile(
    r"^(?P<exc_type>[\w.]+(?:Error|Exception|Warning|BaseException))"
    r"(?::\s*(?P<exc_message>.+))?$",
    re.MULTILINE,
)


@dataclass
class LogEntry:
    """A parsed log entry."""

    level: str
    message: str
    timestamp: str | None = None
    source: str | None = None
    stack_trace: str | None = None


def _parse_log_lines(content: str) -> list[LogEntry]:
    """Parse log content into structured entries."""
    if not content.strip():
        return []

    entries: list[LogEntry] = []
    lines = content.split("\n")
    current_entry: LogEntry | None = None
    stack_lines: list[str] = []

    for line in lines:
        match = LOG_LINE_PATTERN.match(line)
        if match:
            # Save previous entry
            if current_entry is not None:
                if stack_lines:
                    current_entry.stack_trace = "\n".join(stack_lines)
                    stack_lines = []
                entries.append(current_entry)

            current_entry = LogEntry(
                level=match.group("level"),
                message=match.group("message"),
                timestamp=match.group("timestamp"),
                source=match.group("source"),
            )
        elif current_entry is not None:
            # Could be a continuation line or stack trace
            stripped = line.strip()
            if stripped.startswith("Traceback") or stripped.startswith("  File ") or stripped == "":
                stack_lines.append(line)
            elif EXCEPTION_PATTERN.match(stripped):
                # This is an exception line - add to current entry's message
                current_entry.message += f"\n{line}"
            else:
                # Regular continuation line
                current_entry.message += f"\n{line}"

    # Don't forget the last entry
    if current_entry is not None:
        if stack_lines:
            current_entry.stack_trace = "\n".join(stack_lines)
        entries.append(current_entry)

    return entries


@tool
def log_parser(content: str) -> list[dict[str, str | None]]:
    """Parse log content and extract structured error entries.

    Extracts log levels, timestamps, sources, messages, and stack traces.
    Handles Python Traceback format and multiple exception types.

    Args:
        content: Raw log text content to parse.

    Returns:
        A list of parsed log entries as dictionaries.
    """
    entries = _parse_log_lines(content)
    return [
        {
            "level": entry.level,
            "message": entry.message,
            "timestamp": entry.timestamp,
            "source": entry.source,
            "stack_trace": entry.stack_trace,
        }
        for entry in entries
    ]
