"""Global exception handler.

Maps application exceptions to RFC 7807 Problem Details responses.

RFC 7807 defines a standard format for HTTP API error responses:
{
    "type": "https://api.barbershop.com/errors/validation-error",
    "title": "Validation Error",
    "status": 422,
    "detail": "The request was invalid.",
    "instance": "/api/v1/bookings",
    "error_code": "VALIDATION_ERROR"
}
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException
from src.core.logging import app_logger, security_logger

logger = app_logger


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI application.

    Called during application factory creation.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        """Handle all application-specific exceptions."""
        logger.warning(
            "app_exception",
            error_code=exc.error_code,
            message=exc.message,
            path=str(request.url.path),
            details=exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"https://api.barbershop.com/errors/{exc.error_code.lower()}",
                "title": exc.error_code.replace("_", " ").title(),
                "status": exc.status_code,
                "detail": exc.message,
                "instance": str(request.url.path),
                "error_code": exc.error_code,
                **(exc.details if exc.details else {}),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle standard HTTP exceptions (404, 405, etc.)."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"https://httpstatuses.com/{exc.status_code}",
                "title": "HTTP Error",
                "status": exc.status_code,
                "detail": exc.detail or "An error occurred.",
                "instance": str(request.url.path),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors (422)."""
        errors = []
        for error in exc.errors():
            errors.append(
                {
                    "field": ".".join(str(loc) for loc in error["loc"]),
                    "message": error["msg"],
                    "type": error["type"],
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "type": "https://api.barbershop.com/errors/validation-error",
                "title": "Validation Error",
                "status": 422,
                "detail": "The request was invalid. Check the 'errors' field for details.",
                "instance": str(request.url.path),
                "error_code": "VALIDATION_ERROR",
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Catch-all handler for unexpected errors.

        Logs full traceback for debugging but returns a generic
        message to the client (security best practice).
        """
        logger.exception(
            "unhandled_exception",
            error_type=type(exc).__name__,
            path=str(request.url.path),
        )
        security_logger.error(
            "unhandled_error",
            path=str(request.url.path),
            error=str(exc),
        )
        return JSONResponse(
            status_code=500,
            content={
                "type": "https://api.barbershop.com/errors/internal-error",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred. The team has been notified.",
                "instance": str(request.url.path),
                "error_code": "INTERNAL_ERROR",
            },
        )
