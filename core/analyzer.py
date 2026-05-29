"""Root Cause Analysis (RCA) module.

Provides structured analysis of errors to identify root causes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ErrorPattern:
    """A recognized error pattern."""

    name: str
    pattern: str
    category: str
    severity: str
    common_causes: list[str] = field(default_factory=list)
    fix_suggestions: list[str] = field(default_factory=list)


# Common error patterns database
ERROR_PATTERNS: list[ErrorPattern] = [
    ErrorPattern(
        name="ConnectionRefused",
        pattern=r"ConnectionRefused|Connection refused|ECONNREFUSED",
        category="network",
        severity="high",
        common_causes=[
            "Service not running",
            "Wrong host/port",
            "Firewall blocking",
            "Service crashed",
        ],
        fix_suggestions=[
            "Check if the service is running",
            "Verify host and port configuration",
            "Check firewall rules",
            "Review service logs for crashes",
        ],
    ),
    ErrorPattern(
        name="Timeout",
        pattern=r"Timeout|timeout|ETIMEDOUT|timed out",
        category="network",
        severity="medium",
        common_causes=[
            "Slow network",
            "Service overloaded",
            "Database slow query",
            "Deadlock",
        ],
        fix_suggestions=[
            "Increase timeout values",
            "Check network connectivity",
            "Optimize slow queries",
            "Add connection pooling",
        ],
    ),
    ErrorPattern(
        name="OutOfMemory",
        pattern=r"OutOfMemory|OOM|out of memory|MemoryError",
        category="resource",
        severity="critical",
        common_causes=[
            "Memory leak",
            "Large dataset in memory",
            "Insufficient container memory",
            "Too many concurrent connections",
        ],
        fix_suggestions=[
            "Increase memory allocation",
            "Fix memory leaks",
            "Process data in chunks",
            "Add memory monitoring",
        ],
    ),
    ErrorPattern(
        name="NullPointer",
        pattern=r"NullPointer|NoneType|undefined.*not|TypeError.*null|Cannot read propert",
        category="code",
        severity="high",
        common_causes=[
            "Missing null check",
            "Race condition",
            "Uninitialized variable",
            "API returned unexpected null",
        ],
        fix_suggestions=[
            "Add null/None checks",
            "Use Optional/nullable types",
            "Initialize variables properly",
            "Handle API edge cases",
        ],
    ),
    ErrorPattern(
        name="PermissionDenied",
        pattern=r"Permission|PermissionError|EACCES|403 Forbidden|401 Unauthorized",
        category="security",
        severity="high",
        common_causes=[
            "Wrong file permissions",
            "Missing API key",
            "Expired token",
            "Insufficient IAM roles",
        ],
        fix_suggestions=[
            "Check file permissions (chmod)",
            "Verify API keys and tokens",
            "Review IAM/ACL configuration",
            "Check authentication headers",
        ],
    ),
    ErrorPattern(
        name="DiskFull",
        pattern=r"disk full|ENOSPC|No space left|DiskFull",
        category="resource",
        severity="critical",
        common_causes=[
            "Log files too large",
            "Temp files not cleaned",
            "Database grew too large",
            "Backup files accumulating",
        ],
        fix_suggestions=[
            "Clean up old log files",
            "Increase disk space",
            "Add disk monitoring",
            "Implement log rotation",
        ],
    ),
    ErrorPattern(
        name="DatabaseError",
        pattern=r"SQL|database|postgres|mysql|redis|mongo|psycopg|OperationalError",
        category="database",
        severity="high",
        common_causes=[
            "Connection pool exhausted",
            "Database server down",
            "Schema migration needed",
            "Query syntax error",
        ],
        fix_suggestions=[
            "Check database server status",
            "Review connection pool settings",
            "Run pending migrations",
            "Check query syntax",
        ],
    ),
]


@dataclass
class AnalysisResult:
    """Result of error analysis."""

    error_type: str
    category: str
    severity: str
    matched_pattern: str | None = None
    common_causes: list[str] = field(default_factory=list)
    fix_suggestions: list[str] = field(default_factory=list)
    confidence: float = 0.0


def analyze_error(error_message: str) -> AnalysisResult:
    """Analyze an error message and suggest root cause.

    Args:
        error_message: The error message to analyze.

    Returns:
        AnalysisResult with categorized error and suggestions.
    """
    error_lower = error_message.lower()

    for pattern in ERROR_PATTERNS:
        if re.search(pattern.pattern, error_lower, re.IGNORECASE):
            return AnalysisResult(
                error_type=pattern.name,
                category=pattern.category,
                severity=pattern.severity,
                matched_pattern=pattern.pattern,
                common_causes=pattern.common_causes,
                fix_suggestions=pattern.fix_suggestions,
                confidence=0.8,
            )

    return AnalysisResult(
        error_type="Unknown",
        category="unknown",
        severity="medium",
        confidence=0.1,
        common_causes=["Unknown error pattern"],
        fix_suggestions=["Review error logs manually"],
    )


def analyze_errors(errors: list[dict[str, Any]]) -> list[AnalysisResult]:
    """Analyze multiple errors and find patterns.

    Args:
        errors: List of error dictionaries with 'message' key.

    Returns:
        List of analysis results.
    """
    results = []
    for error in errors:
        message = error.get("message", "")
        if message:
            results.append(analyze_error(message))
    return results


def get_severity_summary(results: list[AnalysisResult]) -> dict[str, int]:
    """Summarize errors by severity.

    Args:
        results: List of analysis results.

    Returns:
        Dictionary with severity counts.
    """
    summary: dict[str, int] = {}
    for result in results:
        summary[result.severity] = summary.get(result.severity, 0) + 1
    return summary
