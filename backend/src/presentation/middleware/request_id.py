"""Request ID Middleware.

Assigns a unique request ID to every incoming HTTP request.
The request ID is:
- Added to response headers (X-Request-ID)
- Stored in context variables for logging
- Propagated to all downstream operations

This is the FIRST middleware in the stack — must run before
all other middleware and route handlers.
"""

from __future__ import annotations

import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging import (
    generate_request_id,
    request_id_ctx,
    performance_logger,
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that assigns a unique request ID to every request.

    The request ID is a UUID v7 (time-ordered) for optimal
    database/log index performance.

    Also logs request duration on response for performance monitoring.
    """

    async def dispatch(self, request: Request, call_next: object) -> Response:
        request_id = generate_request_id()
        request_id_ctx.set(request_id)

        # Track request timing
        start_time = time.monotonic()

        # Inject request_id into request state for access in route handlers
        request.state.request_id = request_id

        # Process the request
        response: Response = await call_next(request)  # type: ignore[arg-type]

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Log request performance
        duration_ms = round((time.monotonic() - start_time) * 1000)
        performance_logger.debug(
            "request_completed",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
