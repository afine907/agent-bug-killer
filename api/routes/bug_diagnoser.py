"""Bug Diagnoser API routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class DiagnoseRequest(BaseModel):
    """Request model for bug diagnosis."""

    bug_description: str = Field(..., description="Description of the bug")
    server_host: str | None = Field(None, description="SSH server host")
    server_user: str | None = Field(None, description="SSH username")
    browser_ws: str | None = Field(None, description="CDP WebSocket URL")
    code_path: str | None = Field(None, description="Local code path for search")
    model: str = Field(
        default="anthropic:claude-sonnet-4-6",
        description="LLM model to use",
    )


class Finding(BaseModel):
    """Diagnostic finding."""

    source: str
    description: str
    evidence: str | None = None


class DiagnoseResponse(BaseModel):
    """Response model for bug diagnosis."""

    summary: str
    error_type: str | None = None
    findings: list[Finding]
    root_cause: str | None = None
    recommendations: list[str]
    urgency: str = "medium"


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose_bug(request: DiagnoseRequest) -> DiagnoseResponse:
    """Diagnose a production bug using available data sources.

    This endpoint requires an LLM API key and will make real API calls.

    Args:
        request: Diagnosis request with bug description and optional sources.

    Returns:
        Structured diagnostic report.
    """
    # For now, return a placeholder response
    # Real implementation will call the agent
    return DiagnoseResponse(
        summary=f"Diagnosis for: {request.bug_description}",
        findings=[],
        root_cause="Not implemented yet - requires LLM integration",
        recommendations=["Use CLI for full diagnosis"],
        urgency="low",
    )
