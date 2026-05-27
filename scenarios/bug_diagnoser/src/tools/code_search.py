"""Code search tool for finding code patterns in a project."""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from langchain_core.tools import tool

# File extensions to search by default
DEFAULT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
    ".rb", ".php", ".cs", ".swift", ".kt", ".scala", ".vue",
    ".html", ".css", ".scss", ".yaml", ".yml", ".json", ".toml",
    ".sh", ".bash", ".sql", ".md", ".txt",
}

# Directories to skip
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "egg-info", ".tox", ".eggs",
}


@tool
def code_search(
    pattern: str,
    path: str = ".",
    extensions: str = "",
    max_results: int = 50,
) -> list[dict[str, str | int]]:
    """Search for a text pattern in source code files.

    Args:
        pattern: Text pattern to search for (case-insensitive substring match).
        path: Root directory to search in.
        extensions: Comma-separated file extensions to search (e.g., ".py,.js"). Empty means all.
        max_results: Maximum number of results to return.

    Returns:
        List of matches with file path, line number, and matching line.
    """
    root = Path(path)
    if not root.exists():
        return [{"error": f"Path not found: {path}"}]

    ext_set: set[str] = set()
    if extensions:
        ext_set = {e.strip() if e.strip().startswith(".") else f".{e.strip()}" for e in extensions.split(",")}

    results: list[dict[str, str | int]] = []
    search_lower = pattern.lower()

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip unwanted directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            ext = file_path.suffix.lower()

            if ext_set and ext not in ext_set:
                continue
            if not ext_set and ext not in DEFAULT_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                for i, line in enumerate(content.splitlines(), 1):
                    if search_lower in line.lower():
                        results.append({
                            "file": str(file_path.relative_to(root)),
                            "line": i,
                            "content": line.strip(),
                        })
                        if len(results) >= max_results:
                            return results
            except (OSError, PermissionError):
                continue

    return results
