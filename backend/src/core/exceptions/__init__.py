"""Application exceptions — public API."""

from src.core.exceptions.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    BusinessRuleError,
    ConflictError,
    DuplicateError,
    ExternalServiceError,
    InvalidCredentialsError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    SlotUnavailableError,
    TenantAccessDeniedError,
    TokenExpiredError,
    TokenInvalidError,
    ValidationError,
)

__all__ = [
    "AppException",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessRuleError",
    "ConflictError",
    "DuplicateError",
    "ExternalServiceError",
    "InvalidCredentialsError",
    "NotFoundError",
    "RateLimitError",
    "ServiceUnavailableError",
    "SlotUnavailableError",
    "TenantAccessDeniedError",
    "TokenExpiredError",
    "TokenInvalidError",
    "ValidationError",
]
