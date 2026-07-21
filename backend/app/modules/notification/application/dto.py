"""Notification Module — DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TemplateCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    category: str
    channel: str = Field(default="whatsapp", pattern=r"^(whatsapp|email|sms|push_web|push_mobile)$")
    language: str = "pt-BR"
    subject: str = ""
    body_template: str = Field(..., min_length=1)
    variables: list[str] = Field(default_factory=list)
    is_default: bool = False


class TemplateUpdateRequest(BaseModel):
    subject: str | None = None
    body_template: str | None = None
    variables: list[str] | None = None
    status: str | None = Field(default=None, pattern=r"^(draft|active|archived)$")


class TemplateResponse(BaseModel):
    id: str
    name: str
    category: str
    channel: str
    language: str
    version: int
    subject: str
    body_template: str
    variables: list[str]
    is_default: bool
    status: str


class TemplatePreviewRequest(BaseModel):
    sample_data: dict[str, Any] = Field(default_factory=dict)


class TemplatePreviewResponse(BaseModel):
    subject: str
    body: str
    channel: str


class NotificationSendRequest(BaseModel):
    template_id: str | None = None
    channel: str = "whatsapp"
    customer_id: str | None = None
    recipient_email: str | None = None
    recipient_phone: str | None = None
    subject: str = ""
    body: str = ""
    event_id: str | None = None
    category: str = "custom"


class NotificationResponse(BaseModel):
    id: str
    channel: str
    category: str
    customer_id: str | None = None
    recipient_phone: str | None = None
    recipient_email: str | None = None
    subject: str
    body: str
    status: str
    attempt_count: int
    last_error: str | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    created_at: datetime | None = None


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    offset: int
    limit: int


class ChannelConfigRequest(BaseModel):
    channel: str
    provider: str = ""
    credentials: str = ""
    is_active: bool = True
    quiet_hours_enabled: bool = False
    quiet_start: str = "22:00"
    quiet_end: str = "08:00"
