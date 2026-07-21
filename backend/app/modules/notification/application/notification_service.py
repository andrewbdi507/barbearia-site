"""Notification Module — Application Service.

Central de Notificações — orquestra templates, envio, retry, preferências.
Nenhum módulo envia mensagens diretamente. Todos publicam eventos no EventBus.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.notification.domain.entities import (
    ChannelConfig,
    Notification,
    NotificationTemplate,
)
from app.modules.notification.domain.enums import (
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
)
from app.modules.notification.domain.interfaces import (
    EventBus,
    NotificationChannelProvider,
    NotificationEvent,
    NotificationProviderFactory,
    event_bus,
)
from app.modules.notification.domain.repository_interfaces import (
    IChannelConfigRepository,
    INotificationRepository,
    ITemplateRepository,
)
from app.modules.notification.application.template_engine import TemplateEngine
from app.modules.notification.infrastructure.providers import register_providers


class NotificationService:
    """Central de Notificações — Provider Pattern + Event-Driven.

    Fluxo:
    1. Evento chega via EventBus ou chamada direta
    2. Busca template pelo category+channel
    3. Renderiza template com payload
    4. Verifica preferências do cliente (opt-in)
    5. Verifica quiet hours da empresa
    6. Verifica idempotência (event_id único)
    7. Cria Notification (status=pending → queued)
    8. Envia via Provider (WhatsApp/Email/SMS/Push)
    9. Registra resultado (sent/failed/retry)
    """

    def __init__(
        self,
        template_repo: ITemplateRepository,
        notification_repo: INotificationRepository,
        channel_config_repo: IChannelConfigRepository,
    ) -> None:
        self._templates = template_repo
        self._notifications = notification_repo
        self._channel_configs = channel_config_repo
        register_providers()

        # Inscrever no EventBus para processar automaticamente
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Inscreve-se em todos os eventos do sistema."""
        event_bus.subscribe("booking_confirmation", self._handle_event)
        event_bus.subscribe("booking_reminder", self._handle_event)
        event_bus.subscribe("booking_cancelled", self._handle_event)
        event_bus.subscribe("booking_rescheduled", self._handle_event)
        event_bus.subscribe("payment_approved", self._handle_event)
        event_bus.subscribe("payment_declined", self._handle_event)
        event_bus.subscribe("welcome", self._handle_event)
        event_bus.subscribe("birthday", self._handle_event)

    async def _handle_event(self, event: NotificationEvent) -> None:
        """Handler de evento — chamado pelo EventBus."""
        await self.process_event(event)

    # ============================================================
    # Event Processing
    # ============================================================

    async def process_event(self, event: NotificationEvent) -> list[Notification]:
        """Processa evento e envia notificações por TODOS os canais ativos.

        Cada canal gera uma notificação independente.
        """
        results: list[Notification] = []

        # Buscar configurações do tenant
        channels = [NotificationChannel.WHATSAPP, NotificationChannel.EMAIL]

        for channel in channels:
            # Verificar se canal está configurado e ativo
            config = await self._channel_configs.get_for_tenant(event.tenant_id, channel.value)
            if config is None or not config.is_active:
                continue

            # Verificar quiet hours
            if self._is_quiet_time(config):
                # Agenda para depois do quiet time
                continue

            # Verificar preferências do cliente (opt-in)
            # No MVP, assumimos opt-in padrão

            # Idempotência: mesmo evento não gera 2 notificações
            if event.event_id and event.customer_id:
                exists = await self._notifications.exists_by_event(
                    event.event_id, channel.value, event.customer_id,
                )
                if exists:
                    continue

            # Buscar template
            template = await self._templates.get_by_category(
                event.tenant_id, event.category, channel.value,
            )

            subject = ""
            body = ""
            if template:
                # Renderizar template
                subject = TemplateEngine.render(template.subject, event.payload)
                body = TemplateEngine.render(template.body_template, event.payload)
            else:
                # Fallback: mensagem genérica
                body = self._fallback_body(event)

            # Criar notificação
            notif = Notification(
                id=str(uuid4()), tenant_id=event.tenant_id,
                event_id=event.event_id,
                template_id=template.id if template else None,
                template_version=template.version if template else 1,
                channel=channel,
                category=event.category,
                priority=NotificationPriority(event.priority),
                customer_id=event.customer_id,
                recipient_email=event.recipient_email,
                recipient_phone=event.recipient_phone,
                subject=subject, body=body,
                rendered_content={"payload": event.payload},
                status=NotificationStatus.PENDING,
            )

            created = await self._notifications.create(notif)

            # Enfileirar para envio
            await self._dispatch(created)
            results.append(created)

        return results

    # ============================================================
    # Manual Send
    # ============================================================

    async def send_manual(self, tenant_id: str, **kwargs: object) -> Notification:
        """Envio manual de notificação (via API)."""
        notif = Notification(
            id=str(uuid4()), tenant_id=tenant_id,
            channel=NotificationChannel(str(kwargs.get("channel", "whatsapp"))),
            category=str(kwargs.get("category", "custom")),
            customer_id=str(kwargs.get("customer_id", "")) if kwargs.get("customer_id") else None,
            recipient_email=str(kwargs.get("recipient_email", "")) if kwargs.get("recipient_email") else None,
            recipient_phone=str(kwargs.get("recipient_phone", "")) if kwargs.get("recipient_phone") else None,
            subject=str(kwargs.get("subject", "")),
            body=str(kwargs.get("body", "")),
            event_id=str(kwargs.get("event_id", "")) if kwargs.get("event_id") else None,
        )
        created = await self._notifications.create(notif)
        await self._dispatch(created)
        return created

    # ============================================================
    # Dispatch
    # ============================================================

    async def _dispatch(self, notification: Notification) -> None:
        """Envia notificação via provider do canal."""
        notification.mark_queued()
        await self._notifications.update(notification)

        try:
            provider = self._get_provider(notification.channel.value)
            to = self._resolve_recipient(notification)
            if not to:
                notification.mark_failed("Destinatário não definido.", "NO_RECIPIENT")
                await self._notifications.update(notification)
                return

            notification.mark_sending()
            await self._notifications.update(notification)

            result = await provider.send(to, notification.subject, notification.body)

            notification.mark_sent(result.get("provider_message_id", ""))
            await self._notifications.update(notification)

        except Exception as e:
            notification.mark_failed(str(e), "PROVIDER_ERROR")
            await self._notifications.update(notification)

    # ============================================================
    # Retry
    # ============================================================

    async def retry_pending(self, *, limit: int = 100) -> int:
        """Processa notificações pendentes de retry."""
        items = await self._notifications.get_pending_retries(limit=limit)
        count = 0
        for n in items:
            await self._dispatch(n)
            count += 1
        return count

    # ============================================================
    # Templates
    # ============================================================

    async def list_templates(self, tenant_id: str) -> list[NotificationTemplate]:
        return await self._templates.list_by_tenant(tenant_id)

    async def create_template(self, tenant_id: str, **kwargs: object) -> NotificationTemplate:
        body = str(kwargs.get("body_template", ""))
        variables = TemplateEngine.extract_variables(body)
        tpl = NotificationTemplate(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            category=str(kwargs.get("category", "custom")),
            channel=str(kwargs.get("channel", "whatsapp")),
            language=str(kwargs.get("language", "pt-BR")),
            subject=str(kwargs.get("subject", "")),
            body_template=body,
            variables=variables,
            is_default=bool(kwargs.get("is_default", False)),
        )
        return await self._templates.create(tpl)

    async def update_template(self, template_id: str, **kwargs: object) -> NotificationTemplate:
        existing = await self._templates.get_by_id(template_id)
        if existing is None:
            raise NotFoundError(message="Template não encontrado.")
        for k, v in kwargs.items():
            if hasattr(existing, k) and v is not None:
                setattr(existing, k, v)
        if "body_template" in kwargs:
            existing.variables = TemplateEngine.extract_variables(str(kwargs["body_template"]))
        return await self._templates.update(existing)

    async def preview_template(self, template_id: str, sample_data: dict) -> dict:
        tpl = await self._templates.get_by_id(template_id)
        if tpl is None:
            raise NotFoundError(message="Template não encontrado.")
        return {
            "subject": TemplateEngine.render(tpl.subject, sample_data),
            "body": TemplateEngine.render(tpl.body_template, sample_data),
            "channel": tpl.channel,
        }

    # ============================================================
    # Queries
    # ============================================================

    async def get_notification(self, notification_id: str) -> Notification:
        n = await self._notifications.get_by_id(notification_id)
        if n is None:
            raise NotFoundError(message="Notificação não encontrada.")
        return n

    async def list_notifications(self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Notification], int]:
        return await self._notifications.list_for_tenant(tenant_id, status=status, offset=offset, limit=limit)

    async def get_customer_notifications(self, customer_id: str, *, offset: int = 0, limit: int = 50) -> tuple[list[Notification], int]:
        return await self._notifications.list_for_customer(customer_id, offset=offset, limit=limit)

    # ============================================================
    # Channel Config
    # ============================================================

    async def configure_channel(self, tenant_id: str, **kwargs: object) -> ChannelConfig:
        config = ChannelConfig(
            id=str(uuid4()), tenant_id=tenant_id,
            channel=NotificationChannel(str(kwargs.get("channel", "whatsapp"))),
            provider=str(kwargs.get("provider", "")),
            credentials_encrypted=str(kwargs.get("credentials", "")),
            is_active=bool(kwargs.get("is_active", True)),
            quiet_hours_enabled=bool(kwargs.get("quiet_hours_enabled", False)),
            quiet_start=str(kwargs.get("quiet_start", "22:00")),
            quiet_end=str(kwargs.get("quiet_end", "08:00")),
        )
        return await self._channel_configs.upsert(config)

    # ============================================================
    # Helpers
    # ============================================================

    def _get_provider(self, channel: str) -> NotificationChannelProvider:
        return NotificationProviderFactory.create(channel)

    @staticmethod
    def _resolve_recipient(n: Notification) -> str:
        if n.recipient_phone:
            return n.recipient_phone
        if n.recipient_email:
            return n.recipient_email
        if n.recipient_device_token:
            return n.recipient_device_token
        return ""

    @staticmethod
    def _is_quiet_time(config: ChannelConfig) -> bool:
        if not config.quiet_hours_enabled:
            return False
        now = datetime.now(timezone.utc).strftime("%H:%M")
        return config.quiet_start <= now or now <= config.quiet_end

    @staticmethod
    def _fallback_body(event: NotificationEvent) -> str:
        return f"Notificação: {event.category}"
