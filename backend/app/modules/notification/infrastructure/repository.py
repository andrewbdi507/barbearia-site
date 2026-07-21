"""Notification Module — Repository."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.domain.entities import ChannelConfig, Notification, NotificationTemplate
from app.modules.notification.domain.repository_interfaces import (
    IChannelConfigRepository,
    INotificationRepository,
    ITemplateRepository,
)
from app.modules.notification.infrastructure.models.notification_models import (
    ChannelConfigModel,
    NotificationModel,
    NotificationTemplateModel,
)


def _tpl_to_entity(m: NotificationTemplateModel) -> NotificationTemplate:
    return NotificationTemplate(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        category=m.category, channel=m.channel, language=m.language,
        version=m.version, subject=m.subject, body_template=m.body_template,
        variables=m.variables or [], is_default=m.is_default, status=m.status,
        metadata=m.metadata or {}, created_at=m.created_at, updated_at=m.updated_at,
    )


def _notif_to_entity(m: NotificationModel) -> Notification:
    return Notification(
        id=m.id, tenant_id=m.tenant_id or "", event_id=m.event_id,
        template_id=m.template_id, template_version=m.template_version,
        channel=m.channel, category=m.category, priority=m.priority,
        customer_id=m.customer_id, recipient_email=m.recipient_email,
        recipient_phone=m.recipient_phone, recipient_device_token=m.recipient_device_token,
        subject=m.subject, body=m.body, rendered_content=m.rendered_content or {},
        status=m.status, provider_message_id=m.provider_message_id,
        attempt_count=m.attempt_count, max_attempts=m.max_attempts,
        next_retry_at=m.next_retry_at, last_error=m.last_error, error_code=m.error_code,
        queued_at=m.queued_at, sent_at=m.sent_at, delivered_at=m.delivered_at,
        read_at=m.read_at, failed_at=m.failed_at, created_at=m.created_at,
    )


class TemplateRepository(ITemplateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, template_id: str) -> NotificationTemplate | None:
        r = await self._s.execute(select(NotificationTemplateModel).where(NotificationTemplateModel.id == template_id))
        m = r.scalar_one_or_none()
        return _tpl_to_entity(m) if m else None

    async def get_by_category(self, tenant_id: str, category: str, channel: str) -> NotificationTemplate | None:
        r = await self._s.execute(
            select(NotificationTemplateModel).where(
                NotificationTemplateModel.tenant_id == tenant_id,
                NotificationTemplateModel.category == category,
                NotificationTemplateModel.channel == channel,
                NotificationTemplateModel.status == "active",
            ).order_by(NotificationTemplateModel.version.desc()).limit(1)
        )
        m = r.scalar_one_or_none()
        return _tpl_to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str) -> list[NotificationTemplate]:
        r = await self._s.execute(
            select(NotificationTemplateModel)
            .where(NotificationTemplateModel.tenant_id == tenant_id)
            .order_by(NotificationTemplateModel.category, NotificationTemplateModel.version.desc())
        )
        return [_tpl_to_entity(m) for m in r.scalars().all()]

    async def create(self, template: NotificationTemplate) -> NotificationTemplate:
        m = NotificationTemplateModel(
            id=template.id, tenant_id=template.tenant_id, name=template.name,
            category=template.category, channel=template.channel,
            language=template.language, version=template.version,
            subject=template.subject, body_template=template.body_template,
            variables=template.variables, is_default=template.is_default,
            status=template.status, metadata=template.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return _tpl_to_entity(m)

    async def update(self, template: NotificationTemplate) -> NotificationTemplate:
        m = await self._s.get(NotificationTemplateModel, template.id)
        if not m:
            raise ValueError(f"Template {template.id} not found")
        m.subject = template.subject
        m.body_template = template.body_template
        m.variables = template.variables
        m.status = template.status
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _tpl_to_entity(m)


class NotificationRepository(INotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, notification_id: str) -> Notification | None:
        r = await self._s.execute(select(NotificationModel).where(NotificationModel.id == notification_id))
        m = r.scalar_one_or_none()
        return _notif_to_entity(m) if m else None

    async def exists_by_event(self, event_id: str, channel: str, customer_id: str) -> bool:
        if not event_id:
            return False
        r = await self._s.execute(
            select(func.count()).select_from(NotificationModel).where(
                NotificationModel.event_id == event_id,
                NotificationModel.channel == channel,
                NotificationModel.customer_id == customer_id,
            )
        )
        return (r.scalar() or 0) > 0

    async def create(self, n: Notification) -> Notification:
        m = NotificationModel(
            id=n.id, tenant_id=n.tenant_id, event_id=n.event_id,
            template_id=n.template_id, template_version=n.template_version,
            channel=n.channel, category=n.category, priority=n.priority,
            customer_id=n.customer_id, recipient_email=n.recipient_email,
            recipient_phone=n.recipient_phone, recipient_device_token=n.recipient_device_token,
            subject=n.subject, body=n.body, rendered_content=n.rendered_content,
            status=n.status, max_attempts=n.max_attempts,
        )
        self._s.add(m)
        await self._s.flush()
        return _notif_to_entity(m)

    async def update(self, n: Notification) -> Notification:
        m = await self._s.get(NotificationModel, n.id)
        if not m:
            raise ValueError(f"Notification {n.id} not found")
        for f in ("status", "provider_message_id", "attempt_count", "next_retry_at",
                   "last_error", "error_code", "queued_at", "sent_at", "delivered_at",
                   "read_at", "failed_at"):
            setattr(m, f, getattr(n, f))
        await self._s.flush()
        return _notif_to_entity(m)

    async def list_for_customer(self, customer_id: str, *, offset: int = 0, limit: int = 50) -> tuple[list[Notification], int]:
        base = select(NotificationModel).where(NotificationModel.customer_id == customer_id)
        count_q = select(func.count()).select_from(NotificationModel).where(NotificationModel.customer_id == customer_id)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(NotificationModel.created_at.desc()).offset(offset).limit(limit))
        return [_notif_to_entity(m) for m in r.scalars().all()], total

    async def list_for_tenant(self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Notification], int]:
        base = select(NotificationModel).where(NotificationModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(NotificationModel).where(NotificationModel.tenant_id == tenant_id)
        if status:
            base = base.where(NotificationModel.status == status)
            count_q = count_q.where(NotificationModel.status == status)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(NotificationModel.created_at.desc()).offset(offset).limit(limit))
        return [_notif_to_entity(m) for m in r.scalars().all()], total

    async def get_pending_retries(self, *, limit: int = 100) -> list[Notification]:
        r = await self._s.execute(
            select(NotificationModel)
            .where(NotificationModel.status == "retrying")
            .where(NotificationModel.next_retry_at <= datetime.now(timezone.utc))
            .order_by(NotificationModel.next_retry_at)
            .limit(limit)
        )
        return [_notif_to_entity(m) for m in r.scalars().all()]


class ChannelConfigRepository(IChannelConfigRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_tenant(self, tenant_id: str, channel: str) -> ChannelConfig | None:
        r = await self._s.execute(
            select(ChannelConfigModel).where(
                ChannelConfigModel.tenant_id == tenant_id, ChannelConfigModel.channel == channel,
            )
        )
        m = r.scalar_one_or_none()
        if not m:
            return None
        return ChannelConfig(
            id=m.id, tenant_id=m.tenant_id or "", channel=m.channel,
            is_active=m.is_active, provider=m.provider,
            credentials_encrypted=m.credentials_encrypted, settings=m.settings or {},
            quiet_hours_enabled=m.quiet_hours_enabled,
            quiet_start=m.quiet_start, quiet_end=m.quiet_end, created_at=m.created_at,
        )

    async def upsert(self, config: ChannelConfig) -> ChannelConfig:
        r = await self._s.execute(
            select(ChannelConfigModel).where(
                ChannelConfigModel.tenant_id == config.tenant_id,
                ChannelConfigModel.channel == config.channel,
            )
        )
        m = r.scalar_one_or_none()
        if m:
            m.provider = config.provider
            m.credentials_encrypted = config.credentials_encrypted
            m.is_active = config.is_active
            m.settings = config.settings
            m.quiet_hours_enabled = config.quiet_hours_enabled
            m.quiet_start = config.quiet_start
            m.quiet_end = config.quiet_end
        else:
            m = ChannelConfigModel(
                id=config.id, tenant_id=config.tenant_id, channel=config.channel,
                provider=config.provider, credentials_encrypted=config.credentials_encrypted,
                is_active=config.is_active, settings=config.settings,
                quiet_hours_enabled=config.quiet_hours_enabled,
                quiet_start=config.quiet_start, quiet_end=config.quiet_end,
            )
            self._s.add(m)
        await self._s.flush()
        return config
