"""CLI entry point for the Log Analyzer Agent."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


@click.command()
@click.option("--file", "-f", "log_file", help="Path to the log file to analyze")
@click.option("--text", "-t", "log_text", help="Raw log text to analyze")
@click.option("--model", "-m", default="anthropic:claude-sonnet-4-6", help="LLM model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file for the report")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def analyze(
    log_file: str | None,
    log_text: str | None,
    model: str,
    output: str | None,
    debug: bool,
) -> None:
    """Analyze a log file or log text for errors."""
    if not log_file and not log_text:
        console.print("[red]Error: Please provide either --file or --text[/red]")
        sys.exit(1)

    if log_file:
        path = Path(log_file)
        if not path.exists():
            console.print(f"[red]Error: File not found: {log_file}[/red]")
            sys.exit(1)
        content = path.read_text(encoding="utf-8")
        console.print(f"[blue]Analyzing log file: {log_file}[/blue]")
    else:
        content = log_text
        console.print("[blue]Analyzing provided log text...[/blue]")

    # Import here to avoid circular imports
    from scenarios.log_analyzer.src.tools.log_parser import log_parser

    console.print("[dim]Parsing log entries...[/dim]")
    entries = log_parser.invoke({"content": content})

    error_entries = [e for e in entries if e["level"] in ("ERROR", "CRITICAL", "FATAL")]

    if not error_entries:
        console.print("[green]No errors found in the log.[/green]")
        return

    console.print(f"\n[bold]Found {len(error_entries)} error(s):[/bold]\n")

    for i, entry in enumerate(error_entries, 1):
        console.print(Panel(
            f"[red]{entry['message']}[/red]\n\n"
            f"[dim]Level: {entry['level']}[/dim]\n"
            f"[dim]Source: {entry['source'] or 'N/A'}[/dim]\n"
            f"[dim]Time: {entry['timestamp'] or 'N/A'}[/dim]"
            + (f"\n\n[bold]Stack Trace:[/bold]\n{entry['stack_trace']}" if entry.get("stack_trace") else ""),
            title=f"Error #{i}",
            border_style="red",
        ))

    report = {
        "total_errors": len(error_entries),
        "errors": error_entries,
    }

    if output:
        Path(output).write_text(json.dumps(report, indent=2), encoding="utf-8")
        console.print(f"\n[green]Report saved to: {output}[/green]")
    else:
        console.print("\n[dim]Use --output to save the full report to a file.[/dim]")


if __name__ == "__main__":
    analyze()
