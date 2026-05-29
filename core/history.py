"""Diagnostic history storage.

Stores diagnostic reports for later retrieval and analysis.
Uses file-based storage for simplicity.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class DiagnosticHistory:
    """Manages diagnostic report history."""

    def __init__(self, storage_dir: str | Path = ".diagnostics") -> None:
        """Initialize the history store.

        Args:
            storage_dir: Directory for storing diagnostic reports.
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, report: dict[str, Any], metadata: dict[str, Any] | None = None) -> str:
        """Save a diagnostic report.

        Args:
            report: The diagnostic report to save.
            metadata: Optional metadata (bug description, source, etc.).

        Returns:
            The unique ID of the saved report.
        """
        report_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()

        entry = {
            "id": report_id,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "report": report,
        }

        file_path = self.storage_dir / f"{report_id}.json"
        file_path.write_text(
            json.dumps(entry, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report_id

    def load(self, report_id: str) -> dict[str, Any] | None:
        """Load a diagnostic report by ID.

        Args:
            report_id: The unique ID of the report.

        Returns:
            The report entry, or None if not found.
        """
        file_path = self.storage_dir / f"{report_id}.json"
        if not file_path.exists():
            return None

        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def list_reports(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List recent diagnostic reports.

        Args:
            limit: Maximum number of reports to return.
            offset: Number of reports to skip.

        Returns:
            List of report summaries (without full report data).
        """
        reports = []
        for file_path in sorted(self.storage_dir.glob("*.json"), reverse=True):
            try:
                entry = json.loads(file_path.read_text(encoding="utf-8"))
                reports.append({
                    "id": entry["id"],
                    "timestamp": entry["timestamp"],
                    "metadata": entry.get("metadata", {}),
                    "summary": entry["report"].get("summary", "No summary"),
                })
            except (json.JSONDecodeError, OSError, KeyError):
                continue

        return reports[offset:offset + limit]

    def delete(self, report_id: str) -> bool:
        """Delete a diagnostic report.

        Args:
            report_id: The unique ID of the report.

        Returns:
            True if deleted, False if not found.
        """
        file_path = self.storage_dir / f"{report_id}.json"
        if not file_path.exists():
            return False

        try:
            file_path.unlink()
            return True
        except OSError:
            return False

    def search(self, query: str) -> list[dict[str, Any]]:
        """Search reports by summary or metadata.

        Args:
            query: Search query (case-insensitive).

        Returns:
            List of matching report summaries.
        """
        query_lower = query.lower()
        results = []

        for file_path in self.storage_dir.glob("*.json"):
            try:
                entry = json.loads(file_path.read_text(encoding="utf-8"))
                summary = entry["report"].get("summary", "").lower()
                metadata_str = json.dumps(entry.get("metadata", {})).lower()

                if query_lower in summary or query_lower in metadata_str:
                    results.append({
                        "id": entry["id"],
                        "timestamp": entry["timestamp"],
                        "metadata": entry.get("metadata", {}),
                        "summary": entry["report"].get("summary", "No summary"),
                    })
            except (json.JSONDecodeError, OSError, KeyError):
                continue

        return results
