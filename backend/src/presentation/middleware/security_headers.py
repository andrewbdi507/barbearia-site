"""Security Headers Middleware.

Adds HTTP security headers to every response.

Headers follow OWASP recommendations:
- Strict-Transport-Security: Enforce HTTPS
- X-Content-Type-Options: Prevent MIME sniffing
- X-Frame-Options: Prevent clickjacking
- Content-Security-Policy: Restrict resource loading
- Referrer-Policy: Control referrer information
- Permissions-Policy: Restrict browser features
"""

from __future__ import annotations

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds security headers to all responses.

    These headers protect against common web vulnerabilities:
    XSS, clickjacking, MIME sniffing, and others.
    """

    async def dispatch(self, request: Request, call_next: object) -> Response:
        response: Response = await call_next(request)  # type: ignore[arg-type]

        # HSTS — only in production (HTTPS)
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Basic CSP — can be tightened per-route
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' https: data:; "
            "font-src 'self'; "
            "connect-src 'self'"
        )

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Restrict browser features
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        # Prevent IE from mapping to old document modes
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        return response
