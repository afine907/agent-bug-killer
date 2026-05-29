"""Knowledge base API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.knowledge_base import KnowledgeBase

router = APIRouter()
kb = KnowledgeBase()


class KnowledgeEntryResponse(BaseModel):
    """Knowledge entry response."""

    id: str
    title: str
    error_pattern: str
    category: str
    root_cause: str
    solution: str
    tags: list[str]
    occurrences: int


class KnowledgeListResponse(BaseModel):
    """Response for knowledge list."""

    total: int
    entries: list[KnowledgeEntryResponse]


@router.get("/knowledge", response_model=KnowledgeListResponse)
async def list_knowledge(
    category: str | None = None,
    limit: int = 20,
) -> KnowledgeListResponse:
    """List knowledge base entries.

    Args:
        category: Filter by category.
        limit: Maximum entries to return.

    Returns:
        List of knowledge entries.
    """
    if category:
        entries = kb.get_by_category(category)
    else:
        entries = kb.get_top_entries(limit=limit)

    return KnowledgeListResponse(
        total=len(entries),
        entries=[KnowledgeEntryResponse(**e.__dict__) for e in entries],
    )


@router.get("/knowledge/search/{query}")
async def search_knowledge(query: str) -> KnowledgeListResponse:
    """Search knowledge base.

    Args:
        query: Search query.

    Returns:
        Matching knowledge entries.
    """
    entries = kb.search(query)
    return KnowledgeListResponse(
        total=len(entries),
        entries=[KnowledgeEntryResponse(**e.__dict__) for e in entries],
    )


@router.get("/knowledge/{entry_id}", response_model=KnowledgeEntryResponse)
async def get_knowledge_entry(entry_id: str) -> KnowledgeEntryResponse:
    """Get a specific knowledge entry.

    Args:
        entry_id: The entry ID.

    Returns:
        The knowledge entry.

    Raises:
        HTTPException: If entry not found.
    """
    if entry_id not in kb.entries:
        raise HTTPException(status_code=404, detail="Entry not found")

    entry = kb.entries[entry_id]
    return KnowledgeEntryResponse(**entry.__dict__)
