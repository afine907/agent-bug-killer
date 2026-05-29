"""Caching utilities.

Provides simple caching mechanisms for expensive operations.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class FileCache:
    """Simple file-based cache."""

    def __init__(self, cache_dir: str | Path = ".cache", ttl: int = 3600) -> None:
        """Initialize file cache.

        Args:
            cache_dir: Directory for cache files.
            ttl: Time-to-live in seconds (default: 1 hour).
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

    def _get_path(self, key: str) -> Path:
        """Get cache file path for key."""
        hashed = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed}.json"

    def get(self, key: str) -> Any | None:
        """Get value from cache.

        Args:
            key: Cache key.

        Returns:
            Cached value or None if not found/expired.
        """
        path = self._get_path(key)
        if not path.exists():
            return None

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if time.time() - data["timestamp"] > self.ttl:
                path.unlink()
                return None
            return data["value"]
        except (json.JSONDecodeError, OSError, KeyError):
            return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        path = self._get_path(key)
        data = {
            "key": key,
            "value": value,
            "timestamp": time.time(),
        }
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def delete(self, key: str) -> bool:
        """Delete value from cache.

        Args:
            key: Cache key.

        Returns:
            True if deleted, False if not found.
        """
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self) -> int:
        """Clear all cached values.

        Returns:
            Number of entries cleared.
        """
        count = 0
        for path in self.cache_dir.glob("*.json"):
            path.unlink()
            count += 1
        return count


def cached(
    cache_dir: str = ".cache",
    ttl: int = 3600,
) -> Callable[[F], F]:
    """Decorator to cache function results.

    Args:
        cache_dir: Directory for cache files.
        ttl: Time-to-live in seconds.

    Returns:
        Decorated function with caching.
    """
    cache = FileCache(cache_dir, ttl)

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from function name and arguments
            key_data = {
                "func": func.__name__,
                "args": str(args),
                "kwargs": str(sorted(kwargs.items())),
            }
            key = json.dumps(key_data, sort_keys=True)

            # Check cache
            result = cache.get(key)
            if result is not None:
                return result

            # Compute and cache result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator
