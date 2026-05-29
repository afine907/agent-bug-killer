"""Tests for core.knowledge_base module."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.knowledge_base import KnowledgeBase, KnowledgeEntry


@pytest.fixture
def kb(tmp_path: Path) -> KnowledgeBase:
    """Create a KnowledgeBase with temp storage."""
    return KnowledgeBase(storage_path=tmp_path / "kb.json")


class TestKnowledgeBase:
    """Tests for KnowledgeBase class."""

    def test_init_creates_defaults(self, kb: KnowledgeBase) -> None:
        """Should initialize with default entries."""
        assert len(kb.entries) > 0
        assert "kb-001" in kb.entries

    def test_search_by_title(self, kb: KnowledgeBase) -> None:
        """Should find entries by title."""
        results = kb.search("database")
        assert len(results) > 0
        assert any("Database" in e.title for e in results)

    def test_search_by_pattern(self, kb: KnowledgeBase) -> None:
        """Should find entries by error pattern."""
        results = kb.search("OOM")
        assert len(results) > 0

    def test_search_by_tag(self, kb: KnowledgeBase) -> None:
        """Should find entries by tag."""
        results = kb.search("ssl")
        assert len(results) > 0

    def test_search_case_insensitive(self, kb: KnowledgeBase) -> None:
        """Should perform case-insensitive search."""
        results = kb.search("DATABASE")
        assert len(results) > 0

    def test_get_by_category(self, kb: KnowledgeBase) -> None:
        """Should filter by category."""
        db_entries = kb.get_by_category("database")
        assert len(db_entries) > 0
        assert all(e.category == "database" for e in db_entries)

    def test_add_entry(self, kb: KnowledgeBase, tmp_path: Path) -> None:
        """Should add a new entry."""
        entry = KnowledgeEntry(
            id="kb-test",
            title="Test Entry",
            error_pattern="test error",
            category="test",
            root_cause="Test cause",
            solution="Test solution",
        )
        kb.add_entry(entry)
        assert "kb-test" in kb.entries

        # Verify persistence
        kb2 = KnowledgeBase(storage_path=tmp_path / "kb.json")
        assert "kb-test" in kb2.entries

    def test_increment_occurrences(self, kb: KnowledgeBase) -> None:
        """Should increment occurrence count."""
        initial = kb.entries["kb-001"].occurrences
        kb.increment_occurrences("kb-001")
        assert kb.entries["kb-001"].occurrences == initial + 1

    def test_get_top_entries(self, kb: KnowledgeBase) -> None:
        """Should return entries sorted by occurrences."""
        kb.increment_occurrences("kb-001")
        kb.increment_occurrences("kb-001")
        kb.increment_occurrences("kb-002")

        top = kb.get_top_entries(limit=2)
        assert len(top) == 2
        assert top[0].id == "kb-001"
