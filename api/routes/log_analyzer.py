"""Log Analyzer API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from scenarios.log_analyzer.src.tools.file_reader import file_reader
from scenarios.log_analyzer.src.tools.log_parser import log_parser

router = APIRouter()


class AnalyzeLogRequest(BaseModel):
    """Request model for log analysis."""

    file_path: str | None = Field(None, description="Path to log file")
    log_text: str | None = Field(None, description="Raw log text")
    model: str = Field(
        default="anthropic:claude-sonnet-4-6",
        description="LLM model to use",
    )


class LogEntry(BaseModel):
    """Parsed log entry."""

    level: str
    message: str
    timestamp: str | None = None
    source: str | None = None
    stack_trace: str | None = None


class AnalyzeLogResponse(BaseModel):
    """Response model for log analysis."""

    total_errors: int
    errors: list[LogEntry]
    summary: str


@router.post("/analyze-log", response_model=AnalyzeLogResponse)
async def analyze_log(request: AnalyzeLogRequest) -> AnalyzeLogResponse:
    """Analyze a log file or text for errors.

    Args:
        request: Analysis request with file path or log text.

    Returns:
        Structured analysis results.

    Raises:
        HTTPException: If input is invalid or processing fails.
    """
    if not request.file_path and not request.log_text:
        raise HTTPException(
            status_code=400,
            detail="Either file_path or log_text must be provided",
        )

    try:
        if request.file_path:
            content = file_reader.invoke({"file_path": request.file_path})
            if content.startswith("Error:"):
                raise HTTPException(status_code=400, detail=content)
        else:
            content = request.log_text

        entries = log_parser.invoke({"content": content})
        error_entries = [
            e for e in entries if e.get("level") in ("ERROR", "CRITICAL", "FATAL")
        ]

        return AnalyzeLogResponse(
            total_errors=len(error_entries),
            errors=[LogEntry(**e) for e in error_entries],
            summary=f"Found {len(error_entries)} error(s) in log",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
