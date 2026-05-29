"""Prompt Loader — Load agent system prompts from markdown files.

Provides a utility to load prompt templates from markdown files with
graceful fallback to hardcoded defaults when files are unavailable.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_prompt(file_path: str | Path, default: str = "") -> str:
    """Load a prompt template from a markdown file.

    Args:
        file_path: Path to the markdown prompt file.
        default: Fallback prompt if the file cannot be read.

    Returns:
        The prompt content as a string, or the default if loading fails.
    """
    path = Path(file_path)

    if not path.exists():
        logger.warning("Prompt file not found: %s, using default", path)
        return default

    if not path.is_file():
        logger.warning("Prompt path is not a file: %s, using default", path)
        return default

    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            logger.warning("Prompt file is empty: %s, using default", path)
            return default
        return content
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Failed to read prompt file %s: %s, using default", path, exc)
        return default


def load_scenario_prompt(
    scenario_dir: str | Path,
    prompt_name: str = "system.md",
    default: str = "",
) -> str:
    """Load a prompt from a scenario's prompts directory.

    Convenience wrapper that resolves the path as:
        <scenario_dir>/src/prompts/<prompt_name>

    Args:
        scenario_dir: Root directory of the scenario (e.g. scenarios/log_analyzer).
        prompt_name: Name of the prompt file (default: system.md).
        default: Fallback prompt if the file cannot be read.

    Returns:
        The prompt content as a string, or the default if loading fails.
    """
    prompt_path = Path(scenario_dir) / "src" / "prompts" / prompt_name
    return load_prompt(prompt_path, default=default)
