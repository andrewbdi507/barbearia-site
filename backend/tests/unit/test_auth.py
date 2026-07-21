"""Auth Module — Tests.

Testes para autenticação, autorização, RBAC e segurança.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.config import get_settings
from app.modules.auth.application.auth_service import AuthService
from app.modules.auth.infrastructure import security as sec
from app.modules.auth.infrastructure.models.auth_models import UserModel
from app.modules.auth.infrastructure.repository import AuthRepository


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def mock_repo() -> AuthRepository:
    """Repository mockado para testes unitários."""
    repo = MagicMock(spec=AuthRepository)
    return repo


@pytest.fixture
def auth_service(mock_repo: AuthRepository) -> AuthService:
    return AuthService(mock_repo)


@pytest.fixture
def test_user() -> UserModel:
    user = UserModel(
        id="u_test_123",
        email="test@barbershop.com",
        password_hash=sec.hash_password("StrongP@ss1"),
        name="Test User",
        tenant_id="t_001",
        is_active=True,
        is_verified=True,
    )
    return user


# ============================================================
# Password Hashing Tests
# ============================================================

class TestPasswordHashing:
    def test_hash_is_argon2(self) -> None:
        result = sec.hash_password("mypassword")
        assert result.startswith("$argon2id$")

    def test_verify_correct(self) -> None:
        hashed = sec.hash_password("correct")
        assert sec.verify_password("correct", hashed) is True

    def test_verify_wrong(self) -> None:
        hashed = sec.hash_password("correct")
        assert sec.verify_password("wrong", hashed) is False

    def test_hash_unique_each_time(self) -> None:
        h1 = sec.hash_password("same")
        h2 = sec.hash_password("same")
        assert h1 != h2  # Salt diferente

    def test_needs_rehash_new_params(self) -> None:
        hashed = sec.hash_password("test")
        assert sec.needs_rehash(hashed) is False


# ============================================================
# Token Tests
# ============================================================

class TestTokens:
    def test_create_access_token(self) -> None:
        token = sec.create_access_token(subject="u_123", tenant_id="t_001")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self) -> None:
        token = sec.create_access_token(
            subject="u_456",
            tenant_id="t_001",
            extra_claims={"permissions": ["read"], "role": "admin"},
        )
        claims = sec.decode_token(token)
        assert claims["sub"] == "u_456"
        assert claims["tenant_id"] == "t_001"
        assert claims["type"] == "access"
        assert claims["permissions"] == ["read"]

    def test_decode_expired_token(self) -> None:
        import jwt
        from datetime import timedelta

        settings = get_settings()
        now = datetime.now(timezone.utc)
        claims = {
            "sub": "u_123",
            "iat": now - timedelta(hours=1),
            "exp": now - timedelta(minutes=1),
            "type": "access",
        }
        token = jwt.encode(claims, settings.security.secret_key, algorithm="HS256")

        with pytest.raises(jwt.ExpiredSignatureError):
            sec.decode_token(token)

    def test_refresh_token_is_opaque(self) -> None:
        token = sec.create_refresh_token("u_123")
        assert len(token) == 128  # 64 bytes hex
        # Não deve ser JWT (não tem pontos)
        assert "." not in token

    def test_hash_token(self) -> None:
        token = "abc123secret"
        hashed = sec.hash_token(token)
        assert len(hashed) == 64  # SHA-256 hex
        assert hashed != token


# ============================================================
# AuthService — Login Tests
# ============================================================

class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        mock_repo.get_user_by_email.return_value = test_user
        mock_repo.get_user_permissions.return_value = ["booking:read", "booking:write"]
        mock_repo.get_user_roles.return_value = [MagicMock(name="admin")]

        user_info, access, refresh = await auth_service.login(
            email="test@barbershop.com",
            password="StrongP@ss1",
            tenant_id="t_001",
        )

        assert user_info["email"] == "test@barbershop.com"
        assert user_info["permissions"] == ["booking:read", "booking:write"]
        assert isinstance(access, str)
        assert len(refresh) == 128
        mock_repo.reset_failed_attempts.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        mock_repo.get_user_by_email.return_value = test_user
        mock_repo.increment_failed_attempts.return_value = 1

        from app.core.exceptions import InvalidCredentialsError
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login("test@barbershop.com", "wrong", "t_001")

        mock_repo.increment_failed_attempts.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_user_by_email.return_value = None

        from app.core.exceptions import InvalidCredentialsError
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login("ghost@test.com", "pass", "t_001")

    @pytest.mark.asyncio
    async def test_login_account_locked(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        test_user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=10)
        mock_repo.get_user_by_email.return_value = test_user

        from app.core.exceptions import BusinessRuleError
        with pytest.raises(BusinessRuleError):
            await auth_service.login("test@barbershop.com", "pass", "t_001")

    @pytest.mark.asyncio
    async def test_login_inactive_account(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        test_user.is_active = False
        mock_repo.get_user_by_email.return_value = test_user

        from app.core.exceptions import BusinessRuleError
        with pytest.raises(BusinessRuleError):
            await auth_service.login("test@barbershop.com", "StrongP@ss1", "t_001")

    @pytest.mark.asyncio
    async def test_login_locks_after_max_attempts(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        test_user.failed_login_attempts = 0
        mock_repo.get_user_by_email.return_value = test_user
        mock_repo.increment_failed_attempts.return_value = 5  # MAX

        from app.core.exceptions import InvalidCredentialsError
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login("test@barbershop.com", "wrong", "t_001")

        mock_repo.lock_user.assert_called_once()


# ============================================================
# AuthService — Refresh Token Tests
# ============================================================

class TestRefresh:
    @pytest.mark.asyncio
    async def test_refresh_success(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        from app.modules.auth.infrastructure.models.auth_models import RefreshTokenModel

        stored = RefreshTokenModel(
            id="rt_001",
            user_id="u_test_123",
            token_hash=sec.hash_token("raw_refresh_token_1234567890abcdef"),
            family_id="fam_001",
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        mock_repo.get_refresh_token.return_value = stored
        mock_repo.get_user_by_id.return_value = test_user
        mock_repo.get_user_permissions.return_value = ["read"]
        mock_repo.get_user_roles.return_value = [MagicMock(name="admin")]

        access, new_refresh = await auth_service.refresh("raw_refresh_token_1234567890abcdef")

        assert isinstance(access, str)
        assert len(new_refresh) == 128
        mock_repo.revoke_refresh_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_refresh_token.return_value = None

        from app.core.exceptions import TokenInvalidError
        with pytest.raises(TokenInvalidError):
            await auth_service.refresh("invalid_token")


# ============================================================
# AuthService — Password Reset Tests
# ============================================================

class TestPasswordReset:
    @pytest.mark.asyncio
    async def test_request_reset_user_found(self, auth_service: AuthService, mock_repo: MagicMock, test_user: UserModel) -> None:
        mock_repo.get_user_by_email.return_value = test_user
        token = await auth_service.request_password_reset("test@test.com", "t_001")
        assert token is not None
        assert len(token) == 64  # 32 bytes hex

    @pytest.mark.asyncio
    async def test_request_reset_user_not_found(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_user_by_email.return_value = None
        token = await auth_service.request_password_reset("ghost@test.com", "t_001")
        assert token is None  # Anti-enumeração


# ============================================================
# RBAC Tests
# ============================================================

class TestRBAC:
    @pytest.mark.asyncio
    async def test_get_permissions(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_user_permissions.return_value = ["booking:read", "booking:write", "service:read"]
        perms = await auth_service.get_user_permissions("u_123")
        assert "booking:read" in perms
        assert "admin:access" not in perms

    @pytest.mark.asyncio
    async def test_has_permission_true(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_user_permissions.return_value = ["admin:access", "reports:read"]
        assert await auth_service.has_permission("u_123", "admin:access") is True

    @pytest.mark.asyncio
    async def test_has_permission_false(self, auth_service: AuthService, mock_repo: MagicMock) -> None:
        mock_repo.get_user_permissions.return_value = ["booking:read"]
        assert await auth_service.has_permission("u_123", "admin:access") is False
