"""Memory system wrapper for Agent Bug Killer.

Provides a clean API over DeepAgents' MemoryMiddleware for loading
agent memory from markdown files (AGENTS.md pattern).
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def resolve_memory_paths(
    paths: list[str | Path] | None = None,
    project_root: str | Path | None = None,
) -> list[str]:
    """Resolve and validate memory file paths.

    Args:
        paths: Explicit memory file paths. If None, uses defaults.
        project_root: Project root directory for resolving relative paths.

    Returns:
        List of resolved path strings suitable for DeepAgents memory parameter.
    """
    if paths is not None:
        resolved = []
        for p in paths:
            path = Path(p)
            if path.exists():
                resolved.append(str(path.resolve()))
            else:
                logger.debug("Memory file not found, skipping: %s", path)
        return resolved

    # Default: look for AGENTS.md in common locations
    root = Path(project_root) if project_root else Path.cwd()
    candidates = [
        root / ".deepagents" / "AGENTS.md",
        root / "AGENTS.md",
    ]
    return [str(p.resolve()) for p in candidates if p.exists()]


def create_memory_config(
    paths: list[str | Path] | None = None,
    project_root: str | Path | None = None,
) -> list[str] | None:
    """Create memory configuration for create_deep_agent.

    Args:
        paths: Explicit memory file paths. If None, auto-discovers.
        project_root: Project root for path resolution.

    Returns:
        List of memory file paths, or None if no memory files found.
    """
    resolved = resolve_memory_paths(paths, project_root)
    if not resolved:
        logger.info("No memory files found, memory disabled")
        return None
    logger.info("Memory files loaded: %s", resolved)
    return resolved
