"""Test: Core exceptions."""

from http import HTTPStatus

from src.core.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    ConflictError,
    RateLimitError,
    TenantAccessDeniedError,
    BusinessRuleError,
    InvalidCredentialsError,
    SlotUnavailableError,
)


class TestAppException:
    """Base exception behavior."""

    def test_default_values(self) -> None:
        """Base exception should have sensible defaults."""
        exc = AppException()
        assert exc.error_code == "INTERNAL_ERROR"
        assert exc.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_custom_message(self) -> None:
        """Custom message should override default."""
        exc = AppException(message="Custom error")
        assert exc.message == "Custom error"

    def test_details_payload(self) -> None:
        """Details should be accessible."""
        exc = AppException(details={"field": "name", "reason": "required"})
        assert exc.details == {"field": "name", "reason": "required"}

    def test_str_representation(self) -> None:
        """str() should return the message."""
        exc = AppException(message="Something went wrong")
        assert str(exc) == "Something went wrong"


class TestExceptionHierarchy:
    """Exception type hierarchy correctness."""

    def test_all_extend_app_exception(self) -> None:
        """All custom exceptions should extend AppException."""
        exceptions = [
            ValidationError(),
            AuthenticationError(),
            AuthorizationError(),
            NotFoundError(),
            ConflictError(),
            RateLimitError(),
            BusinessRuleError(),
        ]
        for exc in exceptions:
            assert isinstance(exc, AppException)

    def test_authentication_errors_extend_authentication(self) -> None:
        """Token and credential errors should extend AuthenticationError."""
        assert isinstance(InvalidCredentialsError(), AuthenticationError)
        assert isinstance(TenantAccessDeniedError(), AuthorizationError)

    def test_http_status_codes(self) -> None:
        """Status codes should match HTTP semantics."""
        assert ValidationError().status_code == HTTPStatus.BAD_REQUEST
        assert AuthenticationError().status_code == HTTPStatus.UNAUTHORIZED
        assert AuthorizationError().status_code == HTTPStatus.FORBIDDEN
        assert NotFoundError().status_code == HTTPStatus.NOT_FOUND
        assert ConflictError().status_code == HTTPStatus.CONFLICT
        assert RateLimitError().status_code == HTTPStatus.TOO_MANY_REQUESTS
        assert SlotUnavailableError().status_code == HTTPStatus.CONFLICT
