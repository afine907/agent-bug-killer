"""API middleware for security and monitoring."""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all API requests with timing information."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Process and log the request."""
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        logger.info(
            "%s %s %d %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        response.headers["X-Process-Time"] = f"{duration:.3f}"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter."""

    def __init__(self, app: Any, requests_per_minute: int = 60) -> None:
        """Initialize rate limiter.

        Args:
            app: The FastAPI application.
            requests_per_minute: Maximum requests per minute per IP.
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Check rate limit and process request."""
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if now - t < 60
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
            )

        # Record request
        self.requests[client_ip].append(now)

        return await call_next(request)
