"""Notification Module — Channel Providers.

WhatsAppProvider, EmailProvider, SMSProvider, PushProvider.
Provider Pattern: para adicionar novo canal, implemente NotificationChannelProvider.
"""

from __future__ import annotations

from typing import Any

from app.modules.notification.domain.interfaces import NotificationChannelProvider, NotificationProviderFactory


class WhatsAppProvider(NotificationChannelProvider):
    """WhatsApp Business API / Cloud API."""

    async def send(self, to: str, subject: str, body: str, **kwargs: Any) -> dict[str, Any]:
        # MVP: Simula envio. Produção: integrar com WhatsApp Cloud API
        return {
            "provider_message_id": f"wa_msg_{__import__('uuid').uuid4().hex[:12]}",
            "status": "sent",
            "raw_response": {"to": to, "body": body[:100]},
        }

    async def get_status(self, provider_message_id: str) -> dict[str, Any]:
        return {"provider_message_id": provider_message_id, "status": "delivered"}


class EmailProvider(NotificationChannelProvider):
    """Email — suporta SMTP, SendGrid, Resend, Amazon SES."""

    async def send(self, to: str, subject: str, body: str, **kwargs: Any) -> dict[str, Any]:
        return {
            "provider_message_id": f"em_{__import__('uuid').uuid4().hex[:12]}",
            "status": "sent",
            "raw_response": {"to": to, "subject": subject},
        }

    async def get_status(self, provider_message_id: str) -> dict[str, Any]:
        return {"provider_message_id": provider_message_id, "status": "delivered"}


class SMSProvider(NotificationChannelProvider):
    """SMS — via Twilio, TotalVoice, Zenvia."""

    async def send(self, to: str, subject: str, body: str, **kwargs: Any) -> dict[str, Any]:
        return {
            "provider_message_id": f"sms_{__import__('uuid').uuid4().hex[:12]}",
            "status": "sent",
            "raw_response": {"to": to},
        }

    async def get_status(self, provider_message_id: str) -> dict[str, Any]:
        return {"provider_message_id": provider_message_id, "status": "delivered"}


class PushProvider(NotificationChannelProvider):
    """Push Web + Mobile — via Firebase Cloud Messaging."""

    async def send(self, to: str, subject: str, body: str, **kwargs: Any) -> dict[str, Any]:
        return {
            "provider_message_id": f"push_{__import__('uuid').uuid4().hex[:12]}",
            "status": "sent",
            "raw_response": {"device_token": to[:20] + "..."},
        }

    async def get_status(self, provider_message_id: str) -> dict[str, Any]:
        return {"provider_message_id": provider_message_id, "status": "delivered"}


def register_providers() -> None:
    NotificationProviderFactory.register("whatsapp", WhatsAppProvider)
    NotificationProviderFactory.register("email", EmailProvider)
    NotificationProviderFactory.register("sms", SMSProvider)
    NotificationProviderFactory.register("push_web", PushProvider)
    NotificationProviderFactory.register("push_mobile", PushProvider)
