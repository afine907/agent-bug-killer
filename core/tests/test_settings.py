"""Tests for core settings module."""

import os
from unittest.mock import patch

import pytest

from core.settings import Settings


class TestSettings:
    """Tests for the Settings configuration class."""

    def test_default_settings(self) -> None:
        """Settings should have sensible defaults."""
        settings = Settings()
        assert settings.llm_model == "anthropic:claude-sonnet-4-6"
        assert settings.llm_fallback_model == "anthropic:claude-haiku-4-5"
        assert settings.ssh_timeout == 30
        assert settings.ssh_max_retries == 3
        assert settings.cdp_timeout == 10
        assert settings.log_max_lines == 500
        assert settings.log_max_tokens == 8000

    def test_settings_from_env(self) -> None:
        """Settings should read from environment variables."""
        env = {
            "LLM_MODEL": "openai:gpt-4o",
            "SSH_TIMEOUT": "60",
            "LOG_MAX_LINES": "1000",
        }
        with patch.dict(os.environ, env, clear=False):
            settings = Settings()
            assert settings.llm_model == "openai:gpt-4o"
            assert settings.ssh_timeout == 60
            assert settings.log_max_lines == 1000

    def test_settings_custom_values(self) -> None:
        """Settings should accept custom values via constructor."""
        settings = Settings(
            llm_model="openai:gpt-4o",
            ssh_timeout=60,
            log_max_lines=1000,
        )
        assert settings.llm_model == "openai:gpt-4o"
        assert settings.ssh_timeout == 60
        assert settings.log_max_lines == 1000
