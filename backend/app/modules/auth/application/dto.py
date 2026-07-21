"""Auth Module — Application DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


# ============================================================
# Request DTOs
# ============================================================

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1)
    tenant_id: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class CreateUserRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=2, max_length=255)
    phone: str | None = None
    role_name: str = Field(default="professional")


# ============================================================
# Response DTOs
# ============================================================

class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    phone: str | None
    avatar_url: str | None
    is_active: bool
    is_verified: bool
    permissions: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    last_login_at: datetime | None = None


class SessionResponse(BaseModel):
    id: str
    ip_address: str | None
    user_agent: str | None
    device_info: dict[str, Any] | None
    is_active: bool
    last_activity_at: datetime
    created_at: datetime


class MessageResponse(BaseModel):
    message: str
