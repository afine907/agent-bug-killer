"""Output formatters for diagnostic reports.

Supports JSON, Markdown, and HTML output formats.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def format_json(report: dict[str, Any], pretty: bool = True) -> str:
    """Format a diagnostic report as JSON.

    Args:
        report: The diagnostic report dictionary.
        pretty: Whether to pretty-print the JSON.

    Returns:
        JSON string representation.
    """
    indent = 2 if pretty else None
    return json.dumps(report, indent=indent, ensure_ascii=False)


def format_markdown(report: dict[str, Any]) -> str:
    """Format a diagnostic report as Markdown.

    Args:
        report: The diagnostic report dictionary.

    Returns:
        Markdown formatted string.
    """
    lines = [
        "# Diagnostic Report",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    # Summary
    if "summary" in report:
        lines.extend(["## Summary", "", report["summary"], ""])

    # Errors
    errors = report.get("errors", [])
    if errors:
        lines.extend([f"## Errors ({len(errors)})", ""])
        for i, error in enumerate(errors, 1):
            level = error.get("level", "ERROR")
            message = error.get("message", "No message")
            source = error.get("source", "Unknown")
            timestamp = error.get("timestamp", "N/A")

            lines.extend([
                f"### Error {i}: {level}",
                "",
                f"- **Source**: {source}",
                f"- **Time**: {timestamp}",
                f"- **Message**: {message}",
                "",
            ])

            if error.get("stack_trace"):
                lines.extend([
                    "**Stack Trace**:",
                    "```",
                    error["stack_trace"],
                    "```",
                    "",
                ])

    # Findings (for bug_diagnoser)
    findings = report.get("findings", [])
    if findings:
        lines.extend([f"## Findings ({len(findings)})", ""])
        for finding in findings:
            source = finding.get("source", "unknown")
            desc = finding.get("description", "")
            lines.extend([
                f"### [{source.upper()}]",
                "",
                desc,
                "",
            ])

    # Root Cause
    if "root_cause" in report:
        lines.extend(["## Root Cause", "", report["root_cause"], ""])

    # Impact
    if "impact" in report:
        lines.extend(["## Impact", "", report["impact"], ""])

    # Recommendations
    recommendations = report.get("recommendations", [])
    if recommendations:
        lines.extend(["## Recommendations", ""])
        for rec in recommendations:
            lines.append(f"- {rec}")
        lines.append("")

    # Urgency
    if "urgency" in report:
        lines.extend([f"**Urgency**: {report['urgency']}"])

    return "\n".join(lines)


def format_html(report: dict[str, Any]) -> str:
    """Format a diagnostic report as HTML.

    Args:
        report: The diagnostic report dictionary.

    Returns:
        HTML formatted string.
    """
    md_content = format_markdown(report)

    # Simple markdown-to-html conversion
    html = md_content
    html = html.replace("# ", "<h1>").replace("\n<h1>", "\n<h1>")
    html = html.replace("## ", "<h2>").replace("\n<h2>", "\n<h2>")
    html = html.replace("### ", "<h3>").replace("\n<h3>", "\n<h3>")

    # Wrap in basic HTML structure
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnostic Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 10px; }}
        h2 {{ color: #1976d2; margin-top: 30px; }}
        h3 {{ color: #388e3c; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 5px; }}
        .error {{ color: #d32f2f; }}
        .warning {{ color: #f57c00; }}
        .info {{ color: #1976d2; }}
    </style>
</head>
<body>
<pre>{html}</pre>
</body>
</html>"""


def format_report(report: dict[str, Any], fmt: str = "json") -> str:
    """Format a diagnostic report in the specified format.

    Args:
        report: The diagnostic report dictionary.
        fmt: Output format ("json", "markdown", "md", "html").

    Returns:
        Formatted string.

    Raises:
        ValueError: If format is not supported.
    """
    formatters = {
        "json": format_json,
        "markdown": format_markdown,
        "md": format_markdown,
        "html": format_html,
    }

    formatter = formatters.get(fmt.lower())
    if not formatter:
        raise ValueError(f"Unsupported format: {fmt}. Use: {', '.join(formatters.keys())}")

    return formatter(report)
