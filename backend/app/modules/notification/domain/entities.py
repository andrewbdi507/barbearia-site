"""Notification Module — Domain Entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.modules.notification.domain.enums import (
    NotificationCategory,
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
    TemplateStatus,
)


@dataclass
class NotificationTemplate:
    """Template de mensagem versionado.

    Suporta variáveis: {{customer.name}}, {{booking.date}}, {{company.logo_url}}.
    """

    id: str
    tenant_id: str
    name: str
    category: NotificationCategory = NotificationCategory.CUSTOM
    channel: NotificationChannel = NotificationChannel.WHATSAPP
    language: str = "pt-BR"
    version: int = 1
    subject: str = ""  # Assunto (email) ou título (push)
    body_template: str = ""  # Corpo com {{variaveis}}
    variables: list[str] = field(default_factory=list)  # Lista de variáveis usadas
    is_default: bool = False  # Template padrão do sistema
    status: TemplateStatus = TemplateStatus.ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Notification:
    """Notificação — registro completo de envio."""

    id: str
    tenant_id: str
    event_id: str | None = None  # ID do evento que gerou (anti-duplicidade)
    template_id: str | None = None
    template_version: int = 1
    channel: NotificationChannel = NotificationChannel.WHATSAPP
    category: NotificationCategory = NotificationCategory.CUSTOM
    priority: NotificationPriority = NotificationPriority.NORMAL

    # Destinatário
    customer_id: str | None = None
    recipient_email: str | None = None
    recipient_phone: str | None = None
    recipient_device_token: str | None = None

    # Conteúdo
    subject: str = ""
    body: str = ""  # Corpo já renderizado (template + variáveis resolvidas)
    rendered_content: dict[str, Any] = field(default_factory=dict)

    # Status e entrega
    status: NotificationStatus = NotificationStatus.PENDING
    provider_message_id: str | None = None
    attempt_count: int = 0
    max_attempts: int = 5
    next_retry_at: datetime | None = None
    last_error: str | None = None
    error_code: str | None = None

    # Timestamps
    queued_at: datetime | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    failed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_queued(self) -> None:
        self.status = NotificationStatus.QUEUED
        self.queued_at = datetime.now(timezone.utc)

    def mark_sending(self) -> None:
        self.status = NotificationStatus.SENDING
        self.attempt_count += 1

    def mark_sent(self, provider_message_id: str) -> None:
        self.status = NotificationStatus.SENT
        self.provider_message_id = provider_message_id
        self.sent_at = datetime.now(timezone.utc)

    def mark_delivered(self) -> None:
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = datetime.now(timezone.utc)

    def mark_read(self) -> None:
        self.status = NotificationStatus.READ
        self.read_at = datetime.now(timezone.utc)

    def mark_failed(self, error: str, error_code: str | None = None) -> None:
        self.last_error = error
        self.error_code = error_code
        if self.attempt_count >= self.max_attempts:
            self.status = NotificationStatus.DEAD
            self.failed_at = datetime.now(timezone.utc)
        else:
            self.status = NotificationStatus.RETRYING
            self._schedule_retry()

    def _schedule_retry(self) -> None:
        """Exponential backoff: 1min, 5min, 15min, 1h, 6h."""
        delays = [1, 5, 15, 60, 360]
        idx = min(self.attempt_count - 1, len(delays) - 1)
        from datetime import timedelta
        self.next_retry_at = datetime.now(timezone.utc) + timedelta(minutes=delays[idx])

    def mark_cancelled(self) -> None:
        self.status = NotificationStatus.CANCELLED


@dataclass
class ChannelConfig:
    """Configuração de canal por tenant."""

    id: str
    tenant_id: str
    channel: NotificationChannel = NotificationChannel.WHATSAPP
    is_active: bool = True
    provider: str = ""  # "twilio", "sendgrid", "resend", "ses"
    credentials_encrypted: str = ""  # API keys criptografadas
    settings: dict[str, Any] = field(default_factory=dict)
    quiet_hours_enabled: bool = False
    quiet_start: str = "22:00"
    quiet_end: str = "08:00"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
