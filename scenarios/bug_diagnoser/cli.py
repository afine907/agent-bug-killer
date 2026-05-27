"""CLI entry point for the Bug Diagnoser Agent."""

from __future__ import annotations

import json
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.command()
@click.option("--bug", "-b", "bug_description", required=True, help="Description of the bug")
@click.option("--host", "-H", help="SSH host for remote server")
@click.option("--user", "-u", help="SSH user")
@click.option("--key", "-k", "key_path", help="SSH key path")
@click.option("--browser", "-B", "browser_ws", help="CDP WebSocket URL")
@click.option("--code", "-c", "code_path", help="Path to source code")
@click.option("--model", "-m", default="anthropic:claude-sonnet-4-6", help="LLM model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file for the report")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def diagnose(
    bug_description: str,
    host: str | None,
    user: str | None,
    key_path: str | None,
    browser_ws: str | None,
    code_path: str | None,
    model: str,
    output: str | None,
    debug: bool,
) -> None:
    """Diagnose a production bug using multiple data sources."""
    from pathlib import Path

    from scenarios.bug_diagnoser.src.agent import diagnose_bug

    server_info = None
    if host:
        server_info = {"host": host, "user": user or "root", "key_path": key_path or ""}

    console.print(f"[bold blue]Diagnosing bug:[/bold blue] {bug_description}\n")

    if server_info:
        console.print(f"[dim]Server: {host} (user: {user or 'root'})[/dim]")
    if browser_ws:
        console.print(f"[dim]Browser: {browser_ws}[/dim]")
    if code_path:
        console.print(f"[dim]Code: {code_path}[/dim]")

    console.print("\n[dim]Running diagnosis...[/dim]")

    result = diagnose_bug(
        bug_description=bug_description,
        server_info=server_info,
        browser_ws=browser_ws,
        code_path=code_path,
        model=model,
        debug=debug,
    )

    # Extract the response content
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        if messages:
            last_msg = messages[-1]
            content = last_msg.get("content", "") if isinstance(last_msg, dict) else str(last_msg)
        else:
            content = str(result)
    else:
        content = str(result)

    # Display results
    console.print(Panel(content, title="Diagnosis Report", border_style="green"))

    if output:
        Path(output).write_text(
            json.dumps({"report": content}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        console.print(f"\n[green]Report saved to: {output}[/green]")


if __name__ == "__main__":
    diagnose()
