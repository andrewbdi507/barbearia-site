"""Application exception hierarchy.

All exceptions extend AppException, which carries:
- A unique error code (machine-readable)
- A user-facing message
- An HTTP status code for API responses
- Optional details payload

Design principles:
- Never expose internal errors to clients.
- Every exception is catchable by type.
- Error codes follow the pattern: DOMAIN_REASON (e.g., AUTH_INVALID_CREDENTIALS).
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any


class AppException(Exception):
    """Base exception for all application errors.

    All custom exceptions MUST extend this class.

    Attributes:
        error_code: Machine-readable error identifier (e.g., "VALIDATION_ERROR").
        message: Human-readable error message.
        status_code: HTTP status code for API responses.
        details: Optional payload with additional error context.
    """

    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


# ============================================================
# Validation Errors (400)
# ============================================================


class ValidationError(AppException):
    """Request validation failed."""

    error_code = "VALIDATION_ERROR"
    message = "Validation error."
    status_code = HTTPStatus.BAD_REQUEST


# ============================================================
# Authentication Errors (401)
# ============================================================


class AuthenticationError(AppException):
    """Authentication failed — invalid or missing credentials."""

    error_code = "AUTHENTICATION_ERROR"
    message = "Authentication required."
    status_code = HTTPStatus.UNAUTHORIZED


class InvalidCredentialsError(AuthenticationError):
    """Invalid username/password combination."""

    error_code = "AUTH_INVALID_CREDENTIALS"
    message = "Invalid email or password."


class TokenExpiredError(AuthenticationError):
    """JWT or refresh token has expired."""

    error_code = "AUTH_TOKEN_EXPIRED"
    message = "Token has expired. Please log in again."


class TokenInvalidError(AuthenticationError):
    """Token is malformed or has been tampered with."""

    error_code = "AUTH_TOKEN_INVALID"
    message = "Invalid token."


# ============================================================
# Authorization Errors (403)
# ============================================================


class AuthorizationError(AppException):
    """User does not have required permissions."""

    error_code = "AUTHORIZATION_ERROR"
    message = "You do not have permission to perform this action."
    status_code = HTTPStatus.FORBIDDEN


class TenantAccessDeniedError(AuthorizationError):
    """Attempted cross-tenant access."""

    error_code = "TENANT_ACCESS_DENIED"
    message = "Access to this resource is denied."


# ============================================================
# Not Found Errors (404)
# ============================================================


class NotFoundError(AppException):
    """Requested resource does not exist."""

    error_code = "NOT_FOUND"
    message = "The requested resource was not found."
    status_code = HTTPStatus.NOT_FOUND


# ============================================================
# Conflict Errors (409)
# ============================================================


class ConflictError(AppException):
    """Resource state conflict."""

    error_code = "CONFLICT"
    message = "Resource conflict."
    status_code = HTTPStatus.CONFLICT


class DuplicateError(ConflictError):
    """Resource already exists."""

    error_code = "DUPLICATE"
    message = "This resource already exists."


class SlotUnavailableError(ConflictError):
    """The requested time slot is no longer available."""

    error_code = "SLOT_UNAVAILABLE"
    message = "This time slot is no longer available."


# ============================================================
# Rate Limit Errors (429)
# ============================================================


class RateLimitError(AppException):
    """Too many requests."""

    error_code = "RATE_LIMIT_EXCEEDED"
    message = "Too many requests. Please try again later."
    status_code = HTTPStatus.TOO_MANY_REQUESTS


# ============================================================
# Service Errors (502/503)
# ============================================================


class ServiceUnavailableError(AppException):
    """External service is unavailable."""

    error_code = "SERVICE_UNAVAILABLE"
    message = "Service temporarily unavailable. Please try again."
    status_code = HTTPStatus.SERVICE_UNAVAILABLE


class ExternalServiceError(AppException):
    """Error communicating with an external service."""

    error_code = "EXTERNAL_SERVICE_ERROR"
    message = "An external service error occurred."
    status_code = HTTPStatus.BAD_GATEWAY


# ============================================================
# Business Logic Errors (422)
# ============================================================


class BusinessRuleError(AppException):
    """A business rule was violated."""

    error_code = "BUSINESS_RULE_VIOLATION"
    message = "This action violates business rules."
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
