"""Global settings for Agent Bug Killer."""

import tempfile
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM
    llm_model: str = "anthropic:claude-sonnet-4-6"
    llm_fallback_model: str = "anthropic:claude-haiku-4-5"

    # SSH
    ssh_timeout: int = 30
    ssh_max_retries: int = 3

    # CDP
    cdp_timeout: int = 10
    cdp_screenshot_dir: str = str(Path(tempfile.gettempdir()) / "agent-bug-killer" / "screenshots")

    # Log parsing
    log_max_lines: int = 500
    log_max_tokens: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
