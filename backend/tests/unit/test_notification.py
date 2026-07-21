"""Notification Module — Tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from app.modules.notification.domain.entities import (
    ChannelConfig,
    Notification,
    NotificationTemplate,
)
from app.modules.notification.domain.enums import (
    NotificationCategory,
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
)
from app.modules.notification.domain.interfaces import (
    EventBus,
    NotificationEvent,
    NotificationProviderFactory,
)
from app.modules.notification.application.template_engine import TemplateEngine
from app.modules.notification.infrastructure.providers import register_providers


class TestNotificationEntity:
    def test_mark_queued(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP)
        n.mark_queued()
        assert n.status == NotificationStatus.QUEUED

    def test_mark_sending_increments_attempt(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP)
        n.mark_sending()
        assert n.status == NotificationStatus.SENDING
        assert n.attempt_count == 1

    def test_mark_sent(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP)
        n.mark_sent("wa_msg_123")
        assert n.status == NotificationStatus.SENT
        assert n.provider_message_id == "wa_msg_123"

    def test_mark_failed_retry(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP, attempt_count=1)
        n.mark_failed("Timeout", "TIMEOUT")
        assert n.status == NotificationStatus.RETRYING
        assert n.next_retry_at is not None

    def test_mark_failed_dead(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP, attempt_count=5)
        n.mark_failed("Permanent error")
        assert n.status == NotificationStatus.DEAD

    def test_mark_cancelled(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP)
        n.mark_cancelled()
        assert n.status == NotificationStatus.CANCELLED

    def test_exponential_backoff(self) -> None:
        n = Notification(id="n1", tenant_id="t1", channel=NotificationChannel.WHATSAPP, attempt_count=1)
        n.mark_failed("Err")
        # 2nd attempt (index 1) = 5 min delay
        n.attempt_count = 2
        n.mark_failed("Err")
        assert n.next_retry_at is not None
        # 3rd attempt (index 2) = 15 min delay
        n.attempt_count = 3
        n.mark_failed("Err")
        assert n.next_retry_at is not None


class TestTemplateEngine:
    def test_render_simple(self) -> None:
        result = TemplateEngine.render(
            "Olá {{name}}, seu horário é {{time}}",
            {"name": "João", "time": "14:30"},
        )
        assert result == "Olá João, seu horário é 14:30"

    def test_render_nested(self) -> None:
        result = TemplateEngine.render(
            "{{customer.name}} agendou com {{professional.name}}",
            {"customer": {"name": "João"}, "professional": {"name": "Maria"}},
        )
        assert result == "João agendou com Maria"

    def test_extract_variables(self) -> None:
        vars_ = TemplateEngine.extract_variables("Olá {{customer.name}}, seu {{booking.date}}")
        assert "customer.name" in vars_
        assert "booking.date" in vars_

    def test_validate_success(self) -> None:
        ok, missing = TemplateEngine.validate(
            "{{customer.name}}", {"customer": {"name": "João"}},
        )
        assert ok
        assert len(missing) == 0

    def test_validate_missing(self) -> None:
        ok, missing = TemplateEngine.validate(
            "{{customer.name}} {{booking.date}}", {"customer": {"name": "João"}},
        )
        assert not ok
        assert "booking.date" in missing


class TestEventBus:
    @pytest.mark.asyncio
    async def test_publish_and_handle(self) -> None:
        bus = EventBus()
        received: list[NotificationEvent] = []

        async def handler(event: NotificationEvent) -> None:
            received.append(event)

        bus.subscribe("test_event", handler)

        event = NotificationEvent(
            event_id="evt1", tenant_id="t1", category="test_event",
            payload={"msg": "hello"},
        )
        await bus.publish(event)
        assert len(received) == 1
        assert received[0].event_id == "evt1"

    @pytest.mark.asyncio
    async def test_unsubscribe(self) -> None:
        bus = EventBus()
        received: list[NotificationEvent] = []

        async def handler(event: NotificationEvent) -> None:
            received.append(event)

        bus.subscribe("test", handler)
        bus.unsubscribe("test", handler)

        event = NotificationEvent(event_id="e1", tenant_id="t1", category="test", payload={})
        await bus.publish(event)
        assert len(received) == 0


class TestProviders:
    def test_factory_register(self) -> None:
        register_providers()
        p = NotificationProviderFactory.create("whatsapp")
        assert p is not None

    def test_factory_email(self) -> None:
        register_providers()
        p = NotificationProviderFactory.create("email")
        assert p is not None

    @pytest.mark.asyncio
    async def test_whatsapp_send(self) -> None:
        register_providers()
        p = NotificationProviderFactory.create("whatsapp")
        result = await p.send("5511999999999", "", "Olá!")
        assert "provider_message_id" in result

    @pytest.mark.asyncio
    async def test_email_send(self) -> None:
        register_providers()
        p = NotificationProviderFactory.create("email")
        result = await p.send("test@test.com", "Assunto", "Corpo")
        assert "provider_message_id" in result


class TestDTOs:
    def test_template_create(self) -> None:
        from app.modules.notification.application.dto import TemplateCreateRequest
        req = TemplateCreateRequest(
            name="Confirmação de Agendamento",
            category="booking_confirmation",
            channel="whatsapp",
            body_template="Olá {{customer.name}}, seu horário é {{booking.time}}",
            variables=["customer.name", "booking.time"],
        )
        assert req.category == "booking_confirmation"

    def test_send_manual(self) -> None:
        from app.modules.notification.application.dto import NotificationSendRequest
        req = NotificationSendRequest(
            channel="email", recipient_email="test@test.com",
            subject="Teste", body="Mensagem de teste",
        )
        assert req.channel == "email"
