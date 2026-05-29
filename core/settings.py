"""Global settings for Agent Bug Killer.

Configuration is loaded from environment variables and .env file.
See .env.example for available options.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings can be overridden via environment variables
    with the same name (case-insensitive).
    """

    # LLM Configuration
    llm_model: str = Field(
        default="anthropic:claude-sonnet-4-6",
        description="Primary LLM model identifier",
    )
    llm_fallback_model: str = Field(
        default="anthropic:claude-haiku-4-5",
        description="Fallback model for rate-limited scenarios",
    )

    # SSH Configuration
    ssh_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="SSH connection timeout in seconds",
    )
    ssh_max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum SSH connection retry attempts",
    )
    ssh_key_path: str = Field(
        default="",
        description="Path to SSH private key file",
    )
    ssh_default_user: str = Field(
        default="root",
        description="Default SSH username",
    )

    # CDP Configuration
    cdp_timeout: int = Field(
        default=10,
        ge=1,
        le=60,
        description="CDP connection timeout in seconds",
    )
    cdp_screenshot_dir: str = Field(
        default=str(Path(tempfile.gettempdir()) / "agent-bug-killer" / "screenshots"),
        description="Directory for saving CDP screenshots",
    )

    # Log Parsing Configuration
    log_max_lines: int = Field(
        default=500,
        ge=10,
        le=100000,
        description="Maximum lines to parse from a log file",
    )
    log_max_tokens: int = Field(
        default=8000,
        ge=100,
        le=1000000,
        description="Maximum tokens for log content (rough estimate)",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @field_validator("cdp_screenshot_dir")
    @classmethod
    def ensure_screenshot_dir(cls, v: str) -> str:
        """Create screenshot directory if it doesn't exist."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v


settings = Settings()
