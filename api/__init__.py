"""Agent Bug Killer Web API."""

from __future__ import annotations

from fastapi import FastAPI

from api.middleware import RateLimitMiddleware, RequestLoggingMiddleware

app = FastAPI(
    title="Agent Bug Killer API",
    description="AI-powered bug diagnosis API",
    version="0.2.0",
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.2.0"}


# Import routes after app creation to avoid circular imports
from api.routes import bug_diagnoser, history, knowledge, log_analyzer  # noqa: E402

app.include_router(log_analyzer.router, prefix="/api/v1", tags=["log-analyzer"])
app.include_router(bug_diagnoser.router, prefix="/api/v1", tags=["bug-diagnoser"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])
app.include_router(knowledge.router, prefix="/api/v1", tags=["knowledge"])
