"""Staff Module — Data Transfer Objects."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# Position DTOs
# ============================================================

class PositionCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    sort_order: int = 0


class PositionResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    is_system: bool
    sort_order: int


# ============================================================
# Specialty DTOs
# ============================================================

class SpecialtyCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    color_tag: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")
    sort_order: int = 0


class SpecialtyResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    color_tag: str
    is_active: bool
    sort_order: int


# ============================================================
# StaffProfile DTOs
# ============================================================

class StaffCreateRequest(BaseModel):
    """Cria perfil de funcionário — vinculado a User existente."""
    user_id: str
    position_id: str | None = None
    professional_name: str = Field(default="", max_length=255)
    photo_url: str | None = None
    bio: str | None = None
    specialties: list[str] = Field(default_factory=list)
    experience_years: int = Field(default=0, ge=0, le=60)
    commission_type: str = Field(default="none", pattern=r"^(none|percentage|fixed)$")
    commission_value: int = Field(default=0, ge=0, le=100)
    hire_date: datetime | None = None


class StaffUpdateRequest(BaseModel):
    professional_name: str | None = Field(default=None, max_length=255)
    photo_url: str | None = None
    bio: str | None = None
    specialties: list[str] | None = None
    experience_years: int | None = Field(default=None, ge=0, le=60)
    position_id: str | None = None
    is_visible_on_site: bool | None = None
    commission_type: str | None = Field(default=None, pattern=r"^(none|percentage|fixed)$")
    commission_value: int | None = Field(default=None, ge=0, le=100)


class StaffResponse(BaseModel):
    id: str
    user_id: str
    position_id: str | None = None
    professional_name: str
    photo_url: str | None = None
    bio: str | None = None
    specialties: list[str]
    experience_years: int
    status: str
    is_visible_on_site: bool
    commission_type: str
    commission_value: int
    hire_date: datetime | None = None
    termination_date: datetime | None = None
    position: PositionResponse | None = None
    created_at: datetime | None = None


class StaffListResponse(BaseModel):
    items: list[StaffResponse]
    total: int
    offset: int
    limit: int


# ============================================================
# Team DTOs
# ============================================================

class TeamCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str | None = None
    color_tag: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")
    leader_id: str | None = None
    member_ids: list[str] = Field(default_factory=list)
    sort_order: int = 0


class TeamUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    color_tag: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    leader_id: str | None = None
    member_ids: list[str] | None = None
    is_active: bool | None = None
    sort_order: int | None = None


class TeamResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    color_tag: str
    leader_id: str | None = None
    is_active: bool
    sort_order: int
    member_count: int = 0
    members: list[StaffResponse] = Field(default_factory=list)


# ============================================================
# Schedule DTOs
# ============================================================

class ScheduleDayRequest(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    is_working: bool = True
    start_time: str = Field(default="09:00", pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(default="19:00", pattern=r"^\d{2}:\d{2}$")
    lunch_start: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    lunch_end: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    slot_duration_minutes: int = Field(default=30, ge=5, le=120)


class ScheduleResponse(BaseModel):
    id: str
    staff_id: str
    day_of_week: int
    is_working: bool
    start_time: str
    end_time: str
    lunch_start: str | None = None
    lunch_end: str | None = None
    slot_duration_minutes: int


class ScheduleBatchRequest(BaseModel):
    schedules: list[ScheduleDayRequest] = Field(..., min_length=7, max_length=7)


# ============================================================
# TimeOff DTOs
# ============================================================

class TimeOffCreateRequest(BaseModel):
    staff_id: str | None = None  # Opcional na request — pega do current user
    time_off_type: str = Field(default="day_off")
    start_date: datetime
    end_date: datetime
    start_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    end_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    reason: str = ""
    is_full_day: bool = True


class TimeOffUpdateStatusRequest(BaseModel):
    status: str = Field(..., pattern=r"^(approved|rejected|cancelled)$")


class TimeOffResponse(BaseModel):
    id: str
    staff_id: str
    time_off_type: str
    status: str
    start_date: datetime
    end_date: datetime
    start_time: str | None = None
    end_time: str | None = None
    reason: str
    is_full_day: bool
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime | None = None


# ============================================================
# Invitation DTOs
# ============================================================

class InvitationCreateRequest(BaseModel):
    email: str = Field(..., max_length=255)
    position_id: str | None = None
    message: str = ""


class InvitationResponse(BaseModel):
    id: str
    email: str
    position_id: str | None = None
    status: str
    expires_at: datetime | None = None
    message: str
    created_at: datetime | None = None


# ============================================================
# Audit DTOs
# ============================================================

class AuditLogResponse(BaseModel):
    id: str
    actor_id: str | None = None
    target_id: str | None = None
    action: str
    changes: dict[str, Any]
    ip_address: str | None = None
    created_at: datetime | None = None


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    offset: int
    limit: int
