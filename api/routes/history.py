"""History API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.history import DiagnosticHistory

router = APIRouter()
history = DiagnosticHistory()


class HistoryEntry(BaseModel):
    """History entry summary."""

    id: str
    timestamp: str
    summary: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class HistoryListResponse(BaseModel):
    """Response for history list."""

    total: int
    entries: list[HistoryEntry]


@router.get("/history", response_model=HistoryListResponse)
async def list_history(
    limit: int = 20,
    offset: int = 0,
) -> HistoryListResponse:
    """List diagnostic history entries.

    Args:
        limit: Maximum entries to return.
        offset: Number of entries to skip.

    Returns:
        List of history entries.
    """
    entries = history.list_reports(limit=limit, offset=offset)
    return HistoryListResponse(
        total=len(entries),
        entries=[HistoryEntry(**e) for e in entries],
    )


@router.get("/history/{report_id}")
async def get_report(report_id: str) -> dict[str, Any]:
    """Get a specific diagnostic report.

    Args:
        report_id: The report ID.

    Returns:
        The full diagnostic report.

    Raises:
        HTTPException: If report not found.
    """
    entry = history.load(report_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Report not found")
    return entry


@router.delete("/history/{report_id}")
async def delete_report(report_id: str) -> dict[str, str]:
    """Delete a diagnostic report.

    Args:
        report_id: The report ID.

    Returns:
        Deletion confirmation.

    Raises:
        HTTPException: If report not found.
    """
    if not history.delete(report_id):
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted", "id": report_id}


@router.get("/history/search/{query}")
async def search_history(query: str) -> HistoryListResponse:
    """Search diagnostic history.

    Args:
        query: Search query.

    Returns:
        Matching history entries.
    """
    entries = history.search(query)
    return HistoryListResponse(
        total=len(entries),
        entries=[HistoryEntry(**e) for e in entries],
    )
