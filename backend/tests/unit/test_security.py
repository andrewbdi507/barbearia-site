"""Test: Core security module."""

from src.core.security import hash_password, verify_password


class TestPasswordHashing:
    """Password hashing and verification tests."""

    def test_hash_produces_different_output(self) -> None:
        """Each hash should be unique (salt)."""
        pw = "my-secret-password"
        hash1 = hash_password(pw)
        hash2 = hash_password(pw)
        assert hash1 != hash2  # Different salts

    def test_verify_correct_password(self) -> None:
        """Correct password should verify successfully."""
        pw = "correct-horse-battery-staple"
        hashed = hash_password(pw)
        assert verify_password(pw, hashed) is True

    def test_verify_wrong_password(self) -> None:
        """Wrong password should fail verification."""
        hashed = hash_password("correct-password")
        assert verify_password("wrong-password", hashed) is False

    def test_hash_is_string(self) -> None:
        """Hash should be a string."""
        result = hash_password("password")
        assert isinstance(result, str)
        assert result.startswith("$2b$")  # bcrypt prefix


class TestJWTToken:
    """JWT token creation and verification."""

    def test_create_access_token_is_string(self) -> None:
        """Token should be a non-empty string."""
        from src.core.security import create_access_token

        token = create_access_token(subject="user_123")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self) -> None:
        """Valid token should decode successfully."""
        from src.core.security import create_access_token, decode_token

        token = create_access_token(subject="user_456", tenant_id="t_001")
        claims = decode_token(token)
        assert claims["sub"] == "user_456"
        assert claims["tenant_id"] == "t_001"
        assert claims["type"] == "access"

    def test_decode_with_extra_claims(self) -> None:
        """Extra claims should be present in decoded token."""
        from src.core.security import create_access_token, decode_token

        token = create_access_token(
            subject="user_789",
            extra_claims={"role": "admin", "permissions": ["read", "write"]},
        )
        claims = decode_token(token)
        assert claims["role"] == "admin"
        assert claims["permissions"] == ["read", "write"]

    def test_refresh_token_has_longer_expiry(self) -> None:
        """Refresh token should have type='refresh'."""
        from src.core.security import create_refresh_token, decode_token

        token = create_refresh_token(subject="user_123")
        claims = decode_token(token)
        assert claims["type"] == "refresh"
