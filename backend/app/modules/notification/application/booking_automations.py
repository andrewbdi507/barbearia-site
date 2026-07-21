"""Booking Notifications — Automação de mensagens.

Conecta o ciclo de vida do booking ao sistema de notificações.
Cada evento de booking dispara uma notificação via WhatsApp/Email/SMS.

Eventos:
    booking.confirmed → confirmação de agendamento
    booking.reminder_24h → lembrete 24h antes
    booking.reminder_2h → último aviso 2h antes
    booking.cancelled → notificação de cancelamento
    booking.rescheduled → confirmação do novo horário
    payment.confirmed → pagamento aprovado
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.modules.notification.domain.interfaces import (
    NotificationEvent,
    NotificationProviderFactory,
    event_bus,
)


# ============================================================
# Message Templates
# ============================================================

TEMPLATES: dict[str, str] = {
    "booking_confirmed": (
        "✅ *Agendamento Confirmado!*\n\n"
        "Olá {{customer_name}}!\n\n"
        "📋 *{{service_name}}*\n💈 *{{professional_name}}*\n"
        "📅 *{{booking_date}}*\n🕐 *{{booking_time}}*\n\n"
        "📍 *{{tenant_name}}*\n\n"
        "Qualquer dúvida, responda esta mensagem!"
    ),
    "booking_reminder_24h": (
        "⏰ *Lembrete*\n\nOlá {{customer_name}}!\n"
        "Seu horário é amanhã:\n\n"
        "📋 *{{service_name}}* às *{{booking_time}}*\n"
        "💈 com *{{professional_name}}*\n\n"
        "Responda *SIM* para confirmar presença."
    ),
    "booking_reminder_2h": (
        "🔔 *Seu horário é daqui a 2 horas!*\n\n"
        "{{service_name}} às {{booking_time}} com {{professional_name}}\n"
        "📍 {{tenant_name}} — Te aguardamos! 😊"
    ),
    "booking_cancelled": (
        "❌ *Agendamento Cancelado*\n\n"
        "Olá {{customer_name}}.\n"
        "Seu horário foi cancelado.\n\n"
        "Para remarcar: {{booking_url}}"
    ),
    "booking_rescheduled": (
        "🔄 *Reagendado!*\n\n"
        "Novo horário: {{booking_date}} às {{booking_time}}\n"
        "📋 *{{service_name}}* com *{{professional_name}}*"
    ),
    "payment_confirmed": (
        "💰 *Pagamento Confirmado!*\n\n"
        "Olá {{customer_name}}!\n"
        "Recebemos R$ {{amount}}.\n"
        "Agendamento *CONFIRMADO* para {{booking_date}} às {{booking_time}}."
    ),
}


# ============================================================
# Handler functions
# ============================================================

async def _on_booking_confirmed(event: NotificationEvent) -> None:
    await _send(event, "booking_confirmed")


async def _on_booking_cancelled(event: NotificationEvent) -> None:
    await _send(event, "booking_cancelled")


async def _on_booking_rescheduled(event: NotificationEvent) -> None:
    await _send(event, "booking_rescheduled")


async def _on_reminder_24h(event: NotificationEvent) -> None:
    await _send(event, "booking_reminder_24h")


async def _on_reminder_2h(event: NotificationEvent) -> None:
    await _send(event, "booking_reminder_2h")


async def _on_payment_confirmed(event: NotificationEvent) -> None:
    await _send(event, "payment_confirmed")


# ============================================================
# Registration
# ============================================================

def register_booking_automations() -> None:
    """Registra handlers no EventBus. Chamado no startup."""
    event_bus.subscribe("booking.confirmed", _on_booking_confirmed)
    event_bus.subscribe("booking.cancelled", _on_booking_cancelled)
    event_bus.subscribe("booking.rescheduled", _on_booking_rescheduled)
    event_bus.subscribe("booking.reminder_24h", _on_reminder_24h)
    event_bus.subscribe("booking.reminder_2h", _on_reminder_2h)
    event_bus.subscribe("payment.confirmed", _on_payment_confirmed)
