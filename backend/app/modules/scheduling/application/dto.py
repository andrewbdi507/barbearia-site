"""Scheduling Module — DTOs."""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# ServiceCategory
# ============================================================

class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    color_tag: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")
    sort_order: int = 0


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    color_tag: str
    is_active: bool
    sort_order: int


# ============================================================
# Service
# ============================================================

class ServiceCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    category_id: str | None = None
    description: str = ""
    duration_minutes: int = Field(default=30, ge=5, le=480)
    buffer_minutes: int = Field(default=0, ge=0, le=120)
    base_price: int = Field(default=0, ge=0)
    promotional_price: int | None = Field(default=None, ge=0)
    color_tag: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")
    is_active: bool = True
    sort_order: int = 0
    min_advance_minutes: int = Field(default=0, ge=0)
    max_advance_days: int = Field(default=90, ge=1, le=365)
    notes: str | None = None


class ServiceUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    category_id: str | None = None
    description: str | None = None
    duration_minutes: int | None = Field(default=None, ge=5, le=480)
    buffer_minutes: int | None = Field(default=None, ge=0, le=120)
    base_price: int | None = Field(default=None, ge=0)
    promotional_price: int | None = Field(default=None, ge=0)
    color_tag: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    is_active: bool | None = None
    sort_order: int | None = None
    notes: str | None = None


class ServiceResponse(BaseModel):
    id: str
    name: str
    category_id: str | None = None
    description: str
    duration_minutes: int
    buffer_minutes: int
    base_price: int
    promotional_price: int | None = None
    effective_price: int
    total_duration: int
    color_tag: str
    image_url: str | None = None
    is_active: bool
    sort_order: int
    notes: str | None = None


# ============================================================
# ProfessionalService
# ============================================================

class ProfessionalServiceLinkRequest(BaseModel):
    service_id: str
    custom_price: int | None = None
    custom_duration: int | None = None
    is_active: bool = True


class ProfessionalServiceBatchRequest(BaseModel):
    services: list[ProfessionalServiceLinkRequest]


# ============================================================
# Booking
# ============================================================

class BookingCreateRequest(BaseModel):
    professional_id: str
    booking_date: date
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    service_ids: list[str] = Field(..., min_length=1)
    customer_id: str | None = None
    guest_name: str | None = Field(default=None, max_length=200)
    guest_phone: str | None = Field(default=None, max_length=30)
    guest_email: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    source: str = "website"
    idempotency_key: str | None = None


class BookingRescheduleRequest(BaseModel):
    new_date: date
    new_start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    professional_id: str | None = None
    reason: str = ""


class BookingCancelRequest(BaseModel):
    reason: str = "Cancelado pelo cliente."
    notify_waitlist: bool = True


class BookingResponse(BaseModel):
    id: str
    professional_id: str
    booking_date: date
    start_time: str
    end_time: str
    status: str
    customer_id: str | None = None
    guest_name: str | None = None
    guest_phone: str | None = None
    notes: str | None = None
    total_amount: int
    total_duration_minutes: int
    discount_amount: int
    source: str
    checked_in_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    cancellation_reason: str | None = None
    service_ids: list[str] = Field(default_factory=list)
    created_at: datetime | None = None


class BookingListResponse(BaseModel):
    items: list[BookingResponse]
    total: int
    offset: int
    limit: int


# ============================================================
# Availability
# ============================================================

class AvailabilitySlotResponse(BaseModel):
    date: str
    start_time: str
    end_time: str
    duration_minutes: int


class AvailabilityResponse(BaseModel):
    date: str
    professional_id: str
    slots: list[AvailabilitySlotResponse]


class SmartSuggestionResponse(BaseModel):
    date: str
    start_time: str
    end_time: str
    professional_id: str
    professional_name: str
    total_price: int
    total_duration: int
    suggested: bool = True


# ============================================================
# BlockedDate
# ============================================================

class BlockedDateCreateRequest(BaseModel):
    blocked_date: date
    professional_id: str | None = None
    block_type: str = "full_day"
    reason: str = ""
    start_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    end_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    is_recurring: bool = False
    recurring_pattern: str | None = None
    recurring_until: date | None = None


class BlockedDateResponse(BaseModel):
    id: str
    blocked_date: date
    professional_id: str | None = None
    block_type: str
    reason: str
    start_time: str | None = None
    end_time: str | None = None


# ============================================================
# Waitlist
# ============================================================

class WaitlistCreateRequest(BaseModel):
    professional_id: str | None = None
    service_id: str | None = None
    guest_name: str | None = Field(default=None, max_length=200)
    guest_phone: str | None = Field(default=None, max_length=30)
    desired_date: date | None = None
    desired_period: str = "any"


class WaitlistResponse(BaseModel):
    id: str
    professional_id: str | None = None
    service_id: str | None = None
    guest_name: str | None = None
    guest_phone: str | None = None
    desired_date: date | None = None
    desired_period: str
    status: str
    position: int
    created_at: datetime | None = None
