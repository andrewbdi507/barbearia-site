"""Security foundation.

Provides:
- Password hashing (bcrypt via passlib)
- JWT token creation and verification
- Placeholder for RBAC/permission checking

Note: This module provides the BUILDING BLOCKS for security.
Authentication flows and middleware are implemented in the
presentation layer and infrastructure layer respectively.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import get_settings

# Password hashing context — bcrypt with cost factor >= 12
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        The bcrypt hash string.
    """
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: The password to verify.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches.
    """
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    tenant_id: str | None = None,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token.

    Args:
        subject: The subject claim (typically user ID).
        tenant_id: Optional tenant context for the token.
        extra_claims: Additional claims to include in the token.
        expires_delta: Custom expiration time.

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.security.access_token_expire_minutes)

    now = datetime.now(timezone.utc)
    claims: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
        "type": "access",
    }

    if tenant_id:
        claims["tenant_id"] = tenant_id
    if extra_claims:
        claims.update(extra_claims)

    return jwt.encode(
        claims,
        settings.security.secret_key,
        algorithm=settings.security.jwt_algorithm,
    )


def create_refresh_token(
    subject: str,
    tenant_id: str | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT refresh token (longer-lived).

    Args:
        subject: The subject claim (typically user ID).
        tenant_id: Optional tenant context.
        expires_delta: Custom expiration time.

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()

    if expires_delta is None:
        expires_delta = timedelta(days=settings.security.refresh_token_expire_days)

    now = datetime.now(timezone.utc)
    claims: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
        "type": "refresh",
    }

    if tenant_id:
        claims["tenant_id"] = tenant_id

    return jwt.encode(
        claims,
        settings.security.secret_key,
        algorithm=settings.security.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded token claims.

    Raises:
        JWTError: If the token is invalid, expired, or malformed.
    """
    settings = get_settings()
    return jwt.decode(
        token,
        settings.security.secret_key,
        algorithms=[settings.security.jwt_algorithm],
    )
