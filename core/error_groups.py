"""Error grouping and aggregation.

Groups similar errors together for better analysis.
Inspired by Sentry's error grouping algorithm.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ErrorGroup:
    """A group of similar errors."""

    fingerprint: str
    title: str
    count: int = 0
    first_seen: str = ""
    last_seen: str = ""
    messages: list[str] = field(default_factory=list)
    stack_traces: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_error_message(message: str) -> str:
    """Normalize error message for grouping.

    Removes variable parts like IDs, timestamps, paths.

    Args:
        message: The error message to normalize.

    Returns:
        Normalized message for fingerprinting.
    """
    # Remove timestamps
    normalized = re.sub(
        r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.\d]*",
        "<TIMESTAMP>",
        message,
    )

    # Remove UUIDs
    normalized = re.sub(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "<UUID>",
        normalized,
        flags=re.IGNORECASE,
    )

    # Remove hex addresses
    normalized = re.sub(r"0x[0-9a-f]+", "<HEX>", normalized, flags=re.IGNORECASE)

    # Remove numbers that look like IDs
    normalized = re.sub(r"\b\d{6,}\b", "<ID>", normalized)

    # Remove file paths
    normalized = re.sub(
        r"[/\\][\w./\\]+\.\w+",
        "<PATH>",
        normalized,
    )

    # Remove quoted strings
    normalized = re.sub(r'"[^"]*"', '"<STRING>"', normalized)
    normalized = re.sub(r"'[^']*'", "'<STRING>'", normalized)

    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def compute_fingerprint(message: str, stack_trace: str = "") -> str:
    """Compute a fingerprint for error grouping.

    Args:
        message: The error message.
        stack_trace: Optional stack trace.

    Returns:
        Hex fingerprint string.
    """
    # Normalize the message
    normalized = normalize_error_message(message)

    # Include stack trace if available
    content = normalized
    if stack_trace:
        # Extract just the file/function names from stack trace
        frames = re.findall(
            r"(?:File|at)\s+[\"']?([^\"':]+)[\"']?:?\s*(?:line\s+)?(\d+)?",
            stack_trace,
        )
        if frames:
            frame_str = " | ".join(f"{f[0]}:{f[1]}" for f in frames[:5])
            content = f"{normalized} || {frame_str}"

    return hashlib.md5(content.encode()).hexdigest()[:16]


def group_errors(errors: list[dict[str, Any]]) -> dict[str, ErrorGroup]:
    """Group similar errors together.

    Args:
        errors: List of error dictionaries with 'message' and optional 'stack_trace'.

    Returns:
        Dictionary mapping fingerprint to ErrorGroup.
    """
    groups: dict[str, ErrorGroup] = {}

    for error in errors:
        message = error.get("message", "")
        stack_trace = error.get("stack_trace", "")
        timestamp = error.get("timestamp", "")

        fingerprint = compute_fingerprint(message, stack_trace)

        if fingerprint not in groups:
            # Create new group
            normalized = normalize_error_message(message)
            groups[fingerprint] = ErrorGroup(
                fingerprint=fingerprint,
                title=normalized[:100],
                first_seen=timestamp,
                metadata={
                    "level": error.get("level", "ERROR"),
                    "source": error.get("source", ""),
                },
            )

        group = groups[fingerprint]
        group.count += 1
        group.last_seen = timestamp
        group.messages.append(message)
        if stack_trace:
            group.stack_traces.append(stack_trace)

    return groups


def get_top_groups(
    groups: dict[str, ErrorGroup],
    limit: int = 10,
) -> list[ErrorGroup]:
    """Get the most frequent error groups.

    Args:
        groups: Dictionary of error groups.
        limit: Maximum number of groups to return.

    Returns:
        List of ErrorGroup sorted by count.
    """
    return sorted(
        groups.values(),
        key=lambda g: g.count,
        reverse=True,
    )[:limit]


def format_group_summary(group: ErrorGroup) -> str:
    """Format an error group as a summary string.

    Args:
        group: The error group to format.

    Returns:
        Formatted summary string.
    """
    lines = [
        f"Error Group: {group.fingerprint}",
        f"  Title: {group.title}",
        f"  Count: {group.count}",
        f"  First seen: {group.first_seen or 'N/A'}",
        f"  Last seen: {group.last_seen or 'N/A'}",
    ]

    if group.metadata:
        lines.append(f"  Level: {group.metadata.get('level', 'N/A')}")
        lines.append(f"  Source: {group.metadata.get('source', 'N/A')}")

    return "\n".join(lines)
