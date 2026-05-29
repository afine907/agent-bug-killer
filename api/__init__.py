"""Agent Bug Killer Web API."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Agent Bug Killer API",
    description="AI-powered bug diagnosis API",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


# Import routes after app creation to avoid circular imports
from api.routes import bug_diagnoser, log_analyzer  # noqa: E402

app.include_router(log_analyzer.router, prefix="/api/v1", tags=["log-analyzer"])
app.include_router(bug_diagnoser.router, prefix="/api/v1", tags=["bug-diagnoser"])
