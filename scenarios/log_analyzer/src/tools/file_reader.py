"""File reader tool for reading log files from disk."""

from __future__ import annotations

from pathlib import Path

from langchain_core.tools import tool

from core.settings import settings


@tool
def file_reader(file_path: str, max_lines: int = 0) -> str:
    """Read a file from disk and return its content.

    Args:
        file_path: Absolute or relative path to the file to read.
        max_lines: Maximum number of lines to return. 0 uses settings default.

    Returns:
        The file content as a string, or an error message.
    """
    path = Path(file_path).resolve()

    if not path.exists():
        return f"Error: File not found: {file_path}"

    if not path.is_file():
        return f"Error: Path is not a file: {file_path}"

    # Limit file size to prevent OOM
    try:
        file_size = path.stat().st_size
        max_size = settings.log_max_tokens * 4  # rough estimate: 4 chars per token
        if file_size > max_size:
            return f"Error: File too large ({file_size} bytes). Max allowed: {max_size} bytes."
    except OSError as e:
        return f"Error: Cannot access file: {e}"

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="latin-1")
            return f"[Binary/non-UTF8 file content]\n{content[:5000]}"
        except Exception as e:
            return f"Error: Cannot read file (encoding issue): {e}"
    except PermissionError:
        return f"Error: Permission denied: {file_path}"
    except OSError as e:
        return f"Error: Cannot read file: {e}"

    if max_lines <= 0:
        max_lines = settings.log_max_lines

    lines = content.splitlines()
    content = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        content += f"\n... (truncated, {len(lines)} total lines)"

    return content
