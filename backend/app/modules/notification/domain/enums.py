"""Notification Module — Domain Enums."""

from __future__ import annotations

from enum import StrEnum


class NotificationChannel(StrEnum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    SMS = "sms"
    PUSH_WEB = "push_web"
    PUSH_MOBILE = "push_mobile"


class NotificationStatus(StrEnum):
    PENDING = "pending"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD = "dead"  # DLQ — falha definitiva
    CANCELLED = "cancelled"


class NotificationCategory(StrEnum):
    BOOKING_CONFIRMATION = "booking_confirmation"
    BOOKING_REMINDER = "booking_reminder"
    BOOKING_CANCELLED = "booking_cancelled"
    BOOKING_RESCHEDULED = "booking_rescheduled"
    PAYMENT_APPROVED = "payment_approved"
    PAYMENT_DECLINED = "payment_declined"
    WELCOME = "welcome"
    BIRTHDAY = "birthday"
    SATISFACTION_SURVEY = "satisfaction_survey"
    CUSTOM = "custom"


class TemplateStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class NotificationPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
