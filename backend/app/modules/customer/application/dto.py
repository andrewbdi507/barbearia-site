"""Customer Module — DTOs."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# Customer DTOs
# ============================================================

class CustomerCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=255)
    birth_date: date | None = None
    gender: str | None = None
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)
    source: str = "admin"


class CustomerUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=255)
    birth_date: date | None = None
    gender: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    notes: str | None = None
    tags: list[str] | None = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    phone: str | None = None
    email: str | None = None
    photo_url: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    notes: str | None = None
    tags: list[str]
    status: str
    source: str
    total_visits: int
    total_spent: int
    last_visit_at: datetime | None = None
    created_at: datetime | None = None


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    offset: int
    limit: int


# ============================================================
# Customer 360° View
# ============================================================

class CustomerProfileResponse(BaseModel):
    """Customer 360° — visão completa agregada."""
    customer: CustomerResponse
    preferences: "PreferenceResponse | None" = None
    loyalty: "LoyaltyResponse | None" = None
    recent_bookings: list[Any] = Field(default_factory=list)
    reviews: list["ReviewResponse"] = Field(default_factory=list)
    referrals: list["ReferralResponse"] = Field(default_factory=list)
    stats: dict[str, Any] = Field(default_factory=dict)


# ============================================================
# Preference DTOs
# ============================================================

class PreferenceUpdateRequest(BaseModel):
    favorite_professional_id: str | None = None
    favorite_service_ids: list[str] | None = None
    preferred_time: str | None = None
    preferred_day: int | None = Field(default=None, ge=0, le=6)
    communication_preferences: dict[str, bool] | None = None


class PreferenceResponse(BaseModel):
    favorite_professional_id: str | None = None
    favorite_service_ids: list[str]
    preferred_time: str | None = None
    preferred_day: int | None = None


# ============================================================
# Tag DTOs
# ============================================================

class TagCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    color_tag: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")
    description: str = ""


class TagResponse(BaseModel):
    id: str
    name: str
    color_tag: str
    description: str


# ============================================================
# Review DTOs
# ============================================================

class ReviewCreateRequest(BaseModel):
    booking_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
    tags: list[str] = Field(default_factory=list)
    is_anonymous: bool = False


class ReviewModerateRequest(BaseModel):
    is_visible: bool


class ReviewRespondRequest(BaseModel):
    business_response: str = Field(..., min_length=2, max_length=1000)


class ReviewResponse(BaseModel):
    id: str
    booking_id: str
    customer_id: str
    professional_id: str
    rating: int
    comment: str | None = None
    tags: list[str]
    is_visible: bool
    is_anonymous: bool
    business_response: str | None = None
    created_at: datetime | None = None


# ============================================================
# Consent DTOs
# ============================================================

class ConsentGrantRequest(BaseModel):
    consent_type: str
    is_granted: bool = True
    consent_version: str = "1.0"


class ConsentResponse(BaseModel):
    id: str
    consent_type: str
    is_granted: bool
    consent_version: str
    granted_at: datetime | None = None
    revoked_at: datetime | None = None


# ============================================================
# Loyalty DTOs
# ============================================================

class LoyaltyResponse(BaseModel):
    points: int
    total_earned: int
    total_redeemed: int
    tier: str
    visit_count: int


class LoyaltyTransactionResponse(BaseModel):
    id: str
    transaction_type: str
    points: int
    description: str
    created_at: datetime | None = None


# ============================================================
# Referral DTOs
# ============================================================

class ReferralCreateRequest(BaseModel):
    referred_name: str | None = Field(default=None, max_length=200)
    referred_phone: str | None = Field(default=None, max_length=30)


class ReferralResponse(BaseModel):
    id: str
    referral_code: str
    referred_name: str | None = None
    referred_phone: str | None = None
    status: str
    reward_granted_at: datetime | None = None
    created_at: datetime | None = None
