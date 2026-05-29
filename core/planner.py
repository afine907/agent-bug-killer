"""Planner wrapper for Agent Bug Killer.

Provides utilities for working with DeepAgents' built-in TodoListMiddleware
planning capabilities. The planning system is automatically enabled by
create_deep_agent — this module provides helpers for diagnostic workflows.
"""

from __future__ import annotations

from typing import Any


def create_diagnostic_plan(bug_description: str) -> list[dict[str, str]]:
    """Create a structured diagnostic plan for a bug.

    Generates a todo list template that the agent can use as a starting
    point for multi-step diagnostic workflows.

    Args:
        bug_description: Description of the bug to diagnose.

    Returns:
        List of todo items compatible with write_todos tool.
    """
    return [
        {"content": f"Understand the bug: {bug_description}", "status": "in_progress"},
        {"content": "Gather info from sources (logs, server, browser)", "status": "pending"},
        {"content": "Analyze collected data and identify patterns", "status": "pending"},
        {"content": "Determine root cause", "status": "pending"},
        {"content": "Generate diagnostic report with recommendations", "status": "pending"},
    ]


def create_log_analysis_plan(log_path: str) -> list[dict[str, str]]:
    """Create a structured plan for log analysis.

    Args:
        log_path: Path to the log file to analyze.

    Returns:
        List of todo items compatible with write_todos tool.
    """
    return [
        {"content": f"Read log file: {log_path}", "status": "in_progress"},
        {"content": "Parse log entries and extract error information", "status": "pending"},
        {"content": "Identify error patterns and correlations", "status": "pending"},
        {"content": "Determine root cause and impact", "status": "pending"},
        {"content": "Generate diagnostic report with recommendations", "status": "pending"},
    ]


def format_plan_summary(todos: list[dict[str, Any]]) -> str:
    """Format a todo list into a human-readable summary.

    Args:
        todos: List of todo items with 'content' and 'status' keys.

    Returns:
        Formatted string representation of the plan.
    """
    status_icons = {
        "completed": "✅",
        "in_progress": "🔄",
        "pending": "⏳",
    }
    lines = []
    for item in todos:
        icon = status_icons.get(item.get("status", "pending"), "❓")
        lines.append(f"{icon} {item['content']}")
    return "\n".join(lines)
