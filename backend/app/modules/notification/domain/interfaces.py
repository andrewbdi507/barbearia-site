"""Notification Module — Provider Interface + Event Bus.

Double Provider Pattern:
1. NotificationChannelProvider — envia por canal específico (WhatsApp, Email, etc.)
2. EventBus — módulos publicam eventos, NotificationCenter escuta
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class NotificationChannelProvider(ABC):
    """Interface para canal de envio (WhatsApp, Email, SMS, Push).

    Provider Pattern: para adicionar novo canal, implemente esta interface.
    """

    @abstractmethod
    async def send(
        self, to: str, subject: str, body: str, **kwargs: Any,
    ) -> dict[str, Any]:
        """Envia mensagem pelo canal.

        Returns:
            {"provider_message_id": "msg_123", "status": "sent", "raw_response": {...}}
        """
        ...

    @abstractmethod
    async def get_status(self, provider_message_id: str) -> dict[str, Any]:
        """Consulta status de entrega no provedor."""
        ...


class NotificationProviderFactory:
    """Factory de canais de notificação."""

    _providers: dict[str, type[NotificationChannelProvider]] = {}

    @classmethod
    def register(cls, channel: str, provider_class: type[NotificationChannelProvider]) -> None:
        cls._providers[channel] = provider_class

    @classmethod
    def create(cls, channel: str, **deps: Any) -> NotificationChannelProvider:
        provider_class = cls._providers.get(channel)
        if provider_class is None:
            raise ValueError(f"Canal '{channel}' não registrado.")
        return provider_class(**deps)


# ============================================================
# Event System
# ============================================================

class NotificationEvent:
    """Evento que dispara notificação.

    Módulos NUNCA enviam mensagens diretamente.
    Eles publicam NotificationEvent no EventBus.
    """

    def __init__(
        self,
        event_id: str,
        tenant_id: str,
        category: str,
        payload: dict[str, Any],
        customer_id: str | None = None,
        recipient_email: str | None = None,
        recipient_phone: str | None = None,
        priority: str = "normal",
    ) -> None:
        self.event_id = event_id
        self.tenant_id = tenant_id
        self.category = category
        self.payload = payload
        self.customer_id = customer_id
        self.recipient_email = recipient_email
        self.recipient_phone = recipient_phone
        self.priority = priority


EventHandler = Callable[[NotificationEvent], Any]


class EventBus:
    """Barramento de eventos in-process.

    Módulos publicam eventos.
    NotificationCenter se inscreve para processar.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, category: str, handler: EventHandler) -> None:
        self._handlers.setdefault(category, []).append(handler)

    def unsubscribe(self, category: str, handler: EventHandler) -> None:
        if category in self._handlers:
            self._handlers[category] = [h for h in self._handlers[category] if h != handler]

    async def publish(self, event: NotificationEvent) -> None:
        """Publica evento para todos os handlers inscritos."""
        handlers = self._handlers.get(event.category, [])
        for handler in handlers:
            await handler(event)


# Singleton global
event_bus = EventBus()
