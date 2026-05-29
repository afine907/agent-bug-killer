"""Tests for core.prompt_loader module."""

from __future__ import annotations

from pathlib import Path

from core.prompt_loader import load_prompt, load_scenario_prompt


class TestLoadPrompt:
    """Tests for load_prompt function."""

    def test_load_existing_file(self, tmp_path: Path) -> None:
        """Test loading a valid prompt file."""
        prompt_file = tmp_path / "test.md"
        prompt_file.write_text("# Test Prompt\n\nHello world.", encoding="utf-8")
        result = load_prompt(prompt_file)
        assert result == "# Test Prompt\n\nHello world."

    def test_load_nonexistent_file_returns_default(self, tmp_path: Path) -> None:
        """Test that missing file returns the default value."""
        result = load_prompt(tmp_path / "missing.md", default="fallback")
        assert result == "fallback"

    def test_load_empty_file_returns_default(self, tmp_path: Path) -> None:
        """Test that empty file returns the default value."""
        prompt_file = tmp_path / "empty.md"
        prompt_file.write_text("", encoding="utf-8")
        result = load_prompt(prompt_file, default="fallback")
        assert result == "fallback"

    def test_load_whitespace_only_file_returns_default(self, tmp_path: Path) -> None:
        """Test that whitespace-only file returns the default value."""
        prompt_file = tmp_path / "blank.md"
        prompt_file.write_text("   \n\n  ", encoding="utf-8")
        result = load_prompt(prompt_file, default="fallback")
        assert result == "fallback"

    def test_load_strips_surrounding_whitespace(self, tmp_path: Path) -> None:
        """Test that surrounding whitespace is stripped."""
        prompt_file = tmp_path / "padded.md"
        prompt_file.write_text("\n\n  Hello  \n\n", encoding="utf-8")
        result = load_prompt(prompt_file)
        assert result == "Hello"

    def test_load_directory_returns_default(self, tmp_path: Path) -> None:
        """Test that passing a directory returns the default value."""
        result = load_prompt(tmp_path, default="fallback")
        assert result == "fallback"

    def test_load_with_string_path(self, tmp_path: Path) -> None:
        """Test loading with a string path instead of Path object."""
        prompt_file = tmp_path / "test.md"
        prompt_file.write_text("content", encoding="utf-8")
        result = load_prompt(str(prompt_file))
        assert result == "content"

    def test_default_is_empty_string(self, tmp_path: Path) -> None:
        """Test that default fallback is empty string when not specified."""
        result = load_prompt(tmp_path / "missing.md")
        assert result == ""


class TestLoadScenarioPrompt:
    """Tests for load_scenario_prompt function."""

    def test_load_from_scenario_prompts_dir(self, tmp_path: Path) -> None:
        """Test loading prompt from a scenario's src/prompts/ directory."""
        scenario_dir = tmp_path / "my_scenario"
        prompts_dir = scenario_dir / "src" / "prompts"
        prompts_dir.mkdir(parents=True)
        (prompts_dir / "system.md").write_text("System prompt content", encoding="utf-8")

        result = load_scenario_prompt(scenario_dir)
        assert result == "System prompt content"

    def test_load_custom_prompt_name(self, tmp_path: Path) -> None:
        """Test loading a non-default prompt file name."""
        scenario_dir = tmp_path / "my_scenario"
        prompts_dir = scenario_dir / "src" / "prompts"
        prompts_dir.mkdir(parents=True)
        (prompts_dir / "diagnose.md").write_text("Diagnose prompt", encoding="utf-8")

        result = load_scenario_prompt(scenario_dir, prompt_name="diagnose.md")
        assert result == "Diagnose prompt"

    def test_missing_prompts_dir_returns_default(self, tmp_path: Path) -> None:
        """Test fallback when scenario has no prompts directory."""
        scenario_dir = tmp_path / "empty_scenario"
        scenario_dir.mkdir()

        result = load_scenario_prompt(scenario_dir, default="fallback prompt")
        assert result == "fallback prompt"

    def test_missing_prompt_file_returns_default(self, tmp_path: Path) -> None:
        """Test fallback when prompt file doesn't exist in the directory."""
        scenario_dir = tmp_path / "my_scenario"
        prompts_dir = scenario_dir / "src" / "prompts"
        prompts_dir.mkdir(parents=True)

        result = load_scenario_prompt(scenario_dir, default="fallback")
        assert result == "fallback"
