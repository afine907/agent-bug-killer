"""Fix suggestions module.

Generates actionable fix suggestions based on error analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.analyzer import AnalysisResult


@dataclass
class FixSuggestion:
    """A fix suggestion for an error."""

    title: str
    description: str
    priority: str  # high, medium, low
    effort: str  # small, medium, large
    steps: list[str] = field(default_factory=list)
    code_example: str | None = None
    references: list[str] = field(default_factory=list)


def generate_fix_suggestions(
    analysis: AnalysisResult,
    context: dict[str, Any] | None = None,
) -> list[FixSuggestion]:
    """Generate fix suggestions based on error analysis.

    Args:
        analysis: The error analysis result.
        context: Additional context (language, framework, etc.).

    Returns:
        List of fix suggestions.
    """
    suggestions: list[FixSuggestion] = []
    _ = context  # reserved for future use

    if analysis.error_type == "ConnectionRefused":
        suggestions.append(FixSuggestion(
            title="Check service availability",
            description="Verify the target service is running and accessible",
            priority="high",
            effort="small",
            steps=[
                "Check if the service process is running",
                "Verify the host and port are correct",
                "Test connectivity with telnet or curl",
                "Check firewall rules",
            ],
        ))

    elif analysis.error_type == "Timeout":
        suggestions.append(FixSuggestion(
            title="Increase timeout or optimize performance",
            description="The operation is taking longer than expected",
            priority="medium",
            effort="medium",
            steps=[
                "Increase timeout configuration",
                "Check for slow queries or operations",
                "Add connection pooling",
                "Consider caching frequently accessed data",
            ],
        ))

    elif analysis.error_type == "OutOfMemory":
        suggestions.append(FixSuggestion(
            title="Fix memory usage",
            description="The application is consuming too much memory",
            priority="high",
            effort="large",
            steps=[
                "Profile memory usage to find leaks",
                "Process large datasets in chunks",
                "Implement object pooling",
                "Increase memory limits if justified",
                "Add memory usage monitoring",
            ],
        ))

    elif analysis.error_type == "NullPointer":
        suggestions.append(FixSuggestion(
            title="Add null checks",
            description="Handle null/None values properly",
            priority="high",
            effort="small",
            steps=[
                "Identify where null values originate",
                "Add null checks before access",
                "Use Optional/nullable types",
                "Add input validation",
            ],
            code_example=(
                "# Python example\n"
                "if value is not None:\n"
                "    process(value)\n"
                "else:\n"
                "    handle_missing()"
            ),
        ))

    elif analysis.error_type == "PermissionDenied":
        suggestions.append(FixSuggestion(
            title="Fix permissions",
            description="The application lacks necessary permissions",
            priority="high",
            effort="small",
            steps=[
                "Check file/directory permissions",
                "Verify API keys and tokens",
                "Review IAM roles and policies",
                "Check authentication headers",
            ],
        ))

    elif analysis.error_type == "DiskFull":
        suggestions.append(FixSuggestion(
            title="Free disk space",
            description="The disk is full and needs cleanup",
            priority="high",
            effort="medium",
            steps=[
                "Identify large files with du or ncdu",
                "Clean up old log files",
                "Remove temporary files",
                "Implement log rotation",
                "Increase disk space allocation",
            ],
        ))

    elif analysis.error_type == "DatabaseError":
        suggestions.append(FixSuggestion(
            title="Check database connectivity",
            description="Database connection or query issues",
            priority="high",
            effort="medium",
            steps=[
                "Verify database server is running",
                "Check connection string/credentials",
                "Review connection pool settings",
                "Check for pending migrations",
                "Review slow query logs",
            ],
        ))

    else:
        suggestions.append(FixSuggestion(
            title="Manual investigation required",
            description="This error pattern is not recognized",
            priority="medium",
            effort="medium",
            steps=[
                "Review the error message and stack trace",
                "Check recent code changes",
                "Search for similar issues online",
                "Add more logging around the error",
            ],
        ))

    return suggestions


def format_suggestions_markdown(suggestions: list[FixSuggestion]) -> str:
    """Format fix suggestions as Markdown.

    Args:
        suggestions: List of fix suggestions.

    Returns:
        Markdown formatted string.
    """
    if not suggestions:
        return "No fix suggestions available."

    lines = ["## Fix Suggestions\n"]

    for i, suggestion in enumerate(suggestions, 1):
        lines.extend([
            f"### {i}. {suggestion.title}",
            "",
            f"**Priority**: {suggestion.priority} | **Effort**: {suggestion.effort}",
            "",
            suggestion.description,
            "",
        ])

        if suggestion.steps:
            lines.append("**Steps**:")
            for step in suggestion.steps:
                lines.append(f"1. {step}")
            lines.append("")

        if suggestion.code_example:
            lines.extend([
                "**Example**:",
                "```",
                suggestion.code_example,
                "```",
                "",
            ])

        if suggestion.references:
            lines.append("**References**:")
            for ref in suggestion.references:
                lines.append(f"- {ref}")
            lines.append("")

    return "\n".join(lines)
