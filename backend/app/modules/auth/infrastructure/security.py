"""Auth Security — Password hashing (Argon2id) + JWT + token generation."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError

from app.core.config import get_settings

# Argon2id hasher — vencedor do Password Hashing Competition
# Parâmetros: time_cost=3, memory_cost=65536 (64MB), parallelism=4
_ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)


def hash_password(password: str) -> str:
    """Hash de senha usando Argon2id.

    Argon2id é recomendado pelo OWASP ASVS v4 (2.1.3)
    e venceu o Password Hashing Competition em 2015.
    Resistente a GPU, ASIC e side-channel attacks.
    """
    return _ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica senha contra hash Argon2id.

    Retorna False (não levanta exceção) para evitar
    timing attacks na verificação.
    """
    try:
        return _ph.verify(hashed, plain)
    except (VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    """Verifica se o hash precisa ser atualizado (parâmetros mudaram)."""
    return _ph.check_needs_rehash(password_hash)


def generate_secure_token(length: int = 32) -> str:
    """Gera token criptograficamente seguro (bytes hex)."""
    return secrets.token_hex(length)


def hash_token(token: str) -> str:
    """Hash SHA-256 de token (para armazenamento).

    Tokens são armazenados como hash, nunca em texto puro.
    """
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(
    subject: str,
    tenant_id: str | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Cria JWT access token (curta duração: 15 min).

    Claims padrão: sub, iat, exp, type, jti
    Claims customizados: tenant_id, permissions, role
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)

    claims: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=settings.security.access_token_expire_minutes),
        "type": "access",
        "jti": generate_secure_token(16),
    }

    if tenant_id:
        claims["tenant_id"] = tenant_id
    if extra_claims:
        claims.update(extra_claims)

    key = settings.security.secret_key.get_secret_value() if hasattr(settings.security.secret_key, 'get_secret_value') else str(settings.security.secret_key)
    return jwt.encode(
        claims,
        key,
        algorithm=settings.security.jwt_algorithm,
    )


def create_refresh_token(subject: str, tenant_id: str | None = None) -> str:
    """Gera refresh token opaque (não JWT).

    O refresh token é uma string aleatória de 64 bytes (128 hex chars).
    Armazenado como SHA-256 hash no banco.
    """
    return generate_secure_token(64)


def decode_token(token: str) -> dict[str, Any]:
    """Decodifica e valida JWT access token.

    Valida:
    - Assinatura (HS256/RS256)
    - Expiração (exp)
    - Tipo (type == "access")
    - Algoritmo fixo (não aceita 'none')

    Raises:
        jwt.ExpiredSignatureError: Token expirado
        jwt.InvalidTokenError: Token inválido
    """
    settings = get_settings()
    key = settings.security.secret_key.get_secret_value() if hasattr(settings.security.secret_key, 'get_secret_value') else str(settings.security.secret_key)
    return jwt.decode(
        token,
        key,
        algorithms=[settings.security.jwt_algorithm],
        options={"require": ["exp", "sub", "type"]},
    )
