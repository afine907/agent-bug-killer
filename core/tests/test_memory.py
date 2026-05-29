"""Tests for core.memory module."""

from __future__ import annotations

from pathlib import Path

from core.memory import create_memory_config, resolve_memory_paths


class TestResolveMemoryPaths:
    """Tests for resolve_memory_paths function."""

    def test_explicit_paths(self, tmp_path: Path) -> None:
        """Test with explicitly provided paths."""
        mem_file = tmp_path / "AGENTS.md"
        mem_file.write_text("# Memory", encoding="utf-8")
        result = resolve_memory_paths([mem_file])
        assert len(result) == 1
        assert str(mem_file.resolve()) in result[0]

    def test_explicit_missing_path_skipped(self, tmp_path: Path) -> None:
        """Test that missing explicit paths are skipped."""
        result = resolve_memory_paths([tmp_path / "missing.md"])
        assert result == []

    def test_default_discovery_agents_md(self, tmp_path: Path) -> None:
        """Test auto-discovery of AGENTS.md in project root."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Agents", encoding="utf-8")
        result = resolve_memory_paths(project_root=tmp_path)
        assert len(result) == 1

    def test_default_discovery_deepagents_dir(self, tmp_path: Path) -> None:
        """Test auto-discovery from .deepagents/ directory."""
        deep_dir = tmp_path / ".deepagents"
        deep_dir.mkdir()
        agents_file = deep_dir / "AGENTS.md"
        agents_file.write_text("# Memory", encoding="utf-8")
        result = resolve_memory_paths(project_root=tmp_path)
        assert len(result) == 1

    def test_no_memory_files_found(self, tmp_path: Path) -> None:
        """Test when no memory files exist."""
        result = resolve_memory_paths(project_root=tmp_path)
        assert result == []


class TestCreateMemoryConfig:
    """Tests for create_memory_config function."""

    def test_returns_none_when_no_files(self, tmp_path: Path) -> None:
        """Test that None is returned when no memory files found."""
        result = create_memory_config(project_root=tmp_path)
        assert result is None

    def test_returns_paths_when_files_exist(self, tmp_path: Path) -> None:
        """Test that paths are returned when memory files exist."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Memory", encoding="utf-8")
        result = create_memory_config(project_root=tmp_path)
        assert result is not None
        assert len(result) == 1
