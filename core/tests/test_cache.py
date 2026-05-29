"""Tests for core.cache module."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from core.cache import FileCache, cached


@pytest.fixture
def cache(tmp_path: Path) -> FileCache:
    """Create a FileCache with temp directory."""
    return FileCache(cache_dir=tmp_path / "cache", ttl=60)


class TestFileCache:
    """Tests for FileCache class."""

    def test_set_and_get(self, cache: FileCache) -> None:
        """Should set and get values."""
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_nonexistent(self, cache: FileCache) -> None:
        """Should return None for nonexistent key."""
        assert cache.get("nonexistent") is None

    def test_delete(self, cache: FileCache) -> None:
        """Should delete cached value."""
        cache.set("key1", "value1")
        assert cache.delete("key1") is True
        assert cache.get("key1") is None

    def test_delete_nonexistent(self, cache: FileCache) -> None:
        """Should return False for nonexistent key."""
        assert cache.delete("nonexistent") is False

    def test_clear(self, cache: FileCache) -> None:
        """Should clear all cached values."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        count = cache.clear()
        assert count == 2
        assert cache.get("key1") is None

    def test_ttl_expiration(self, tmp_path: Path) -> None:
        """Should expire after TTL."""
        cache = FileCache(cache_dir=tmp_path / "cache", ttl=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_complex_values(self, cache: FileCache) -> None:
        """Should cache complex values."""
        value = {"key": "value", "list": [1, 2, 3]}
        cache.set("complex", value)
        assert cache.get("complex") == value


class TestCachedDecorator:
    """Tests for cached decorator."""

    def test_caches_result(self, tmp_path: Path) -> None:
        """Should cache function result."""
        call_count = 0

        @cached(cache_dir=str(tmp_path / "cache"), ttl=60)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = expensive_func(5)
        result2 = expensive_func(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Only called once

    def test_different_args_different_cache(self, tmp_path: Path) -> None:
        """Should cache different arguments separately."""
        call_count = 0

        @cached(cache_dir=str(tmp_path / "cache"), ttl=60)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        expensive_func(5)
        expensive_func(10)

        assert call_count == 2
