"""Structured logging system.

Design:
    Uses structlog for structured JSON logging.
    Three distinct loggers: application, security, audit.
    All logs are emitted as JSON to stdout (12-Factor App).
    In development, optional console pretty-printing.

Log Schema (every log entry carries):
    - timestamp: ISO 8601 with timezone
    - level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    - logger: which logger produced this entry
    - event: human-readable event description
    - request_id: UUID propagated across the request lifecycle
    - tenant_id: tenant context (if available)
    - user_id: user context (if available)
"""

from __future__ import annotations

import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

import structlog

from src.core.config import get_settings

# Context variables — populated by middleware per-request
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
tenant_id_ctx: ContextVar[str] = ContextVar("tenant_id", default="")
user_id_ctx: ContextVar[str] = ContextVar("user_id", default="")


def add_context_fields(
    logger: logging.Logger,
    method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Inject context variables into every log entry."""
    request_id = request_id_ctx.get("")
    tenant_id = tenant_id_ctx.get("")
    user_id = user_id_ctx.get("")

    if request_id:
        event_dict["request_id"] = request_id
    if tenant_id:
        event_dict["tenant_id"] = tenant_id
    if user_id:
        event_dict["user_id"] = user_id

    return event_dict


def setup_logging() -> None:
    """Configure structured logging for the application.

    Should be called once at application startup.

    Output format depends on LOG_FORMAT setting:
    - "json": Machine-parseable JSON to stdout (production).
    - "console": Human-readable colored output (development).
    """
    settings = get_settings()

    # Determine log level
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)

    # Shared processors for all loggers
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        add_context_fields,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.PositionalArgumentsFormatter(),
    ]

    if settings.logging.format == "console" and settings.is_development:
        # Development: colored console output
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=settings.logging.colorize),
        ]
    else:
        # Production: JSON to stdout
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(serializer=__json_serializer),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Set root logger level
    logging.getLogger().setLevel(log_level)

    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def __json_serializer(data: Any, **kwargs: Any) -> str:
    """Serialize log data to JSON using orjson when available."""
    try:
        import orjson

        return orjson.dumps(data, default=str).decode("utf-8")
    except ImportError:
        import json

        return json.dumps(data, default=str)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a structured logger for the given module name.

    Usage:
        logger = get_logger(__name__)
        logger.info("booking_created", booking_id="b_123")
    """
    return structlog.get_logger(name)


def generate_request_id() -> str:
    """Generate a unique request ID for tracing.

    Uses UUID7 (time-ordered) for better index locality in logs.
    """
    try:
        import uuid7

        return str(uuid7.uuid7())
    except ImportError:
        return str(uuid.uuid4())


# Pre-configured loggers for different concerns
app_logger = structlog.get_logger("app")
security_logger = structlog.get_logger("security")
audit_logger = structlog.get_logger("audit")
performance_logger = structlog.get_logger("performance")
