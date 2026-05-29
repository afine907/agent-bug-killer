"""Knowledge base for error patterns and solutions.

Stores and retrieves known error patterns with their solutions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class KnowledgeEntry:
    """A knowledge base entry."""

    id: str
    title: str
    error_pattern: str
    category: str
    root_cause: str
    solution: str
    tags: list[str] = field(default_factory=list)
    occurrences: int = 0


class KnowledgeBase:
    """Manages error pattern knowledge base."""

    def __init__(self, storage_path: str | Path = "knowledge_base.json") -> None:
        """Initialize the knowledge base.

        Args:
            storage_path: Path to the knowledge base JSON file.
        """
        self.storage_path = Path(storage_path)
        self.entries: dict[str, KnowledgeEntry] = {}
        self._load()

    def _load(self) -> None:
        """Load entries from storage."""
        if not self.storage_path.exists():
            self._init_defaults()
            self._save()
            return

        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            for entry_data in data.get("entries", []):
                entry = KnowledgeEntry(**entry_data)
                self.entries[entry.id] = entry
        except (json.JSONDecodeError, OSError):
            self._init_defaults()

    def _save(self) -> None:
        """Save entries to storage."""
        data = {
            "version": "1.0",
            "entries": [
                {
                    "id": e.id,
                    "title": e.title,
                    "error_pattern": e.error_pattern,
                    "category": e.category,
                    "root_cause": e.root_cause,
                    "solution": e.solution,
                    "tags": e.tags,
                    "occurrences": e.occurrences,
                }
                for e in self.entries.values()
            ],
        }
        self.storage_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _init_defaults(self) -> None:
        """Initialize with default knowledge entries."""
        defaults = [
            KnowledgeEntry(
                id="kb-001",
                title="Database Connection Pool Exhaustion",
                error_pattern="Pool exhausted|connection pool|too many connections",
                category="database",
                root_cause=(
                    "Connection pool size is too small for the current load, "
                    "or connections are not being released properly."
                ),
                solution=(
                    "1. Increase pool size (e.g., from 5 to 20)\n"
                    "2. Add connection timeout\n"
                    "3. Ensure connections are returned to pool\n"
                    "4. Add connection pool monitoring"
                ),
                tags=["database", "connection", "pool", "performance"],
            ),
            KnowledgeEntry(
                id="kb-002",
                title="Memory Leak in Long-Running Process",
                error_pattern="OutOfMemory|OOM|memory leak|heap space",
                category="resource",
                root_cause=(
                    "Objects are being created but not garbage collected, "
                    "often due to circular references or caches without eviction."
                ),
                solution=(
                    "1. Profile memory usage\n"
                    "2. Check for circular references\n"
                    "3. Implement cache eviction policies\n"
                    "4. Increase memory limits if needed\n"
                    "5. Restart services periodically as temporary fix"
                ),
                tags=["memory", "leak", "performance", "java", "python"],
            ),
            KnowledgeEntry(
                id="kb-003",
                title="API Rate Limiting",
                error_pattern="429|rate limit|too many requests|throttl",
                category="api",
                root_cause="Client is making too many requests within the rate limit window.",
                solution=(
                    "1. Implement exponential backoff\n"
                    "2. Add request queuing\n"
                    "3. Cache responses where possible\n"
                    "4. Request rate limit increase from provider\n"
                    "5. Use batch APIs if available"
                ),
                tags=["api", "rate-limit", "http", "429"],
            ),
            KnowledgeEntry(
                id="kb-004",
                title="SSL/TLS Certificate Issues",
                error_pattern="SSL|certificate|CERT_|handshake|verify",
                category="security",
                root_cause=(
                    "SSL certificate is expired, self-signed, "
                    "or the certificate chain is incomplete."
                ),
                solution=(
                    "1. Check certificate expiration date\n"
                    "2. Verify certificate chain is complete\n"
                    "3. Update CA certificates\n"
                    "4. For self-signed certs, add to trusted store\n"
                    "5. Use openssl s_client to debug"
                ),
                tags=["ssl", "tls", "certificate", "security", "https"],
            ),
            KnowledgeEntry(
                id="kb-005",
                title="DNS Resolution Failure",
                error_pattern="DNS|ENOTFOUND|name resolution|resolve.*host",
                category="network",
                root_cause=(
                    "DNS server is unreachable, domain doesn't exist, "
                    "or DNS cache is stale."
                ),
                solution=(
                    "1. Check DNS server configuration\n"
                    "2. Verify domain name is correct\n"
                    "3. Flush DNS cache\n"
                    "4. Try using IP address directly\n"
                    "5. Check /etc/hosts or Windows hosts file"
                ),
                tags=["dns", "network", "domain", "resolution"],
            ),
        ]

        for entry in defaults:
            self.entries[entry.id] = entry

    def search(self, query: str) -> list[KnowledgeEntry]:
        """Search knowledge base by query.

        Args:
            query: Search query (matches title, pattern, tags).

        Returns:
            List of matching entries.
        """
        query_lower = query.lower()
        results = []

        for entry in self.entries.values():
            if (
                query_lower in entry.title.lower()
                or query_lower in entry.error_pattern.lower()
                or query_lower in entry.root_cause.lower()
                or any(query_lower in tag for tag in entry.tags)
            ):
                results.append(entry)

        return results

    def get_by_category(self, category: str) -> list[KnowledgeEntry]:
        """Get entries by category.

        Args:
            category: The category to filter by.

        Returns:
            List of entries in the category.
        """
        return [e for e in self.entries.values() if e.category == category]

    def add_entry(self, entry: KnowledgeEntry) -> None:
        """Add a new entry to the knowledge base.

        Args:
            entry: The entry to add.
        """
        self.entries[entry.id] = entry
        self._save()

    def increment_occurrences(self, entry_id: str) -> None:
        """Increment the occurrence count for an entry.

        Args:
            entry_id: The ID of the entry.
        """
        if entry_id in self.entries:
            self.entries[entry_id].occurrences += 1
            self._save()

    def get_top_entries(self, limit: int = 10) -> list[KnowledgeEntry]:
        """Get the most frequently occurring entries.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            List of entries sorted by occurrences.
        """
        return sorted(
            self.entries.values(),
            key=lambda e: e.occurrences,
            reverse=True,
        )[:limit]
