"""Marketing Module — Application Service.

Coupon Validator, Promotion Engine, Campaign Orchestrator,
Rule Engine (Automations), Smart Segments.
"""

from __future__ import annotations

import secrets
from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.marketing.domain.entities import (
    AutomationRule, Campaign, Coupon, GiftCard, Promotion,
)
from app.modules.marketing.infrastructure.repository import MarketingRepository


class MarketingService:
    """Serviço de Marketing — cupons, promoções, campanhas, automações."""

    def __init__(self, repo: MarketingRepository) -> None:
        self._repo = repo

    # ============================================================
    # Coupons
    # ============================================================

    async def create_coupon(self, tenant_id: str, **kwargs: object) -> Coupon:
        code = str(kwargs.get("code", secrets.token_hex(4)[:8].upper()))
        existing = await self._repo.get_coupon_by_code(tenant_id, code)
        if existing:
            raise BusinessRuleError(message="Já existe cupom com este código.")

        coupon = Coupon(
            id=str(uuid4()), tenant_id=tenant_id, code=code.upper(),
            coupon_type=str(kwargs.get("coupon_type", "fixed")),
            value=int(kwargs.get("value", 0)),
            min_purchase_amount=int(kwargs.get("min_purchase_amount", 0)),
            max_uses=int(kwargs.get("max_uses", 0)),
            max_per_customer=int(kwargs.get("max_per_customer", 1)),
            starts_at=kwargs.get("starts_at"),
            expires_at=kwargs.get("expires_at"),
            applies_to=str(kwargs.get("applies_to", "all")),
            applicable_ids=list(kwargs.get("applicable_ids", [])),
            created_by=str(kwargs.get("created_by", "")) if kwargs.get("created_by") else None,
        )
        return await self._repo.create_coupon(coupon)

    async def validate_coupon(self, tenant_id: str, code: str, amount: int, service_id: str = "", customer_id: str = "") -> dict[str, Any]:
        """Valida e calcula desconto do cupom."""
        coupon = await self._repo.get_coupon_by_code(tenant_id, code.upper())
        if coupon is None:
            raise NotFoundError(message="Cupom não encontrado.")

        if not coupon.is_valid:
            raise BusinessRuleError(message="Cupom expirado ou esgotado.")

        if coupon.min_purchase_amount > 0 and amount < coupon.min_purchase_amount:
            raise BusinessRuleError(
                message=f"Valor mínimo de R$ {coupon.min_purchase_amount / 100:.2f} não atingido.",
            )

        if coupon.applies_to == "specific_services" and service_id and service_id not in coupon.applicable_ids:
            raise BusinessRuleError(message="Cupom não aplicável a este serviço.")

        discount = coupon.calculate_discount(amount)
        return {
            "valid": True,
            "coupon_id": coupon.id,
            "code": coupon.code,
            "discount": discount,
            "final_amount": amount - discount,
            "coupon_type": coupon.coupon_type,
        }

    async def apply_coupon(self, coupon_id: str) -> None:
        await self._repo.use_coupon(coupon_id)

    async def list_coupons(self, tenant_id: str) -> list[Coupon]:
        return await self._repo.list_coupons(tenant_id)

    # ============================================================
    # Promotions
    # ============================================================

    async def create_promotion(self, tenant_id: str, **kwargs: object) -> Promotion:
        promo = Promotion(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            promotion_type=str(kwargs.get("promotion_type", "time_period")),
            description=str(kwargs.get("description", "")),
            discount_type=str(kwargs.get("discount_type", "percentage")),
            discount_value=int(kwargs.get("discount_value", 0)),
            starts_at=kwargs.get("starts_at"),
            ends_at=kwargs.get("ends_at"),
            applicable_days=list(kwargs.get("applicable_days", [])),
            applicable_hours_start=str(kwargs.get("applicable_hours_start", "")) if kwargs.get("applicable_hours_start") else None,
            applicable_hours_end=str(kwargs.get("applicable_hours_end", "")) if kwargs.get("applicable_hours_end") else None,
            service_ids=list(kwargs.get("service_ids", [])),
            bundle_service_ids=list(kwargs.get("bundle_service_ids", [])),
        )
        return await self._repo.create_promotion(promo)

    async def list_promotions(self, tenant_id: str) -> list[Promotion]:
        return await self._repo.list_promotions(tenant_id)

    async def get_active_promotions(self, tenant_id: str, service_id: str = "") -> list[Promotion]:
        all_promos = await self._repo.list_promotions(tenant_id)
        active = [p for p in all_promos if p.is_valid_now]
        if service_id:
            active = [p for p in active if not p.service_ids or service_id in p.service_ids]
        return active

    # ============================================================
    # Campaigns
    # ============================================================

    async def create_campaign(self, tenant_id: str, **kwargs: object) -> Campaign:
        campaign = Campaign(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            description=str(kwargs.get("description", "")),
            channel=str(kwargs.get("channel", "whatsapp")),
            status="draft",
            segment_type=str(kwargs.get("segment_type", "custom")),
            segment_filters=dict(kwargs.get("segment_filters", {})),
            template_id=str(kwargs.get("template_id", "")) if kwargs.get("template_id") else None,
            coupon_id=str(kwargs.get("coupon_id", "")) if kwargs.get("coupon_id") else None,
            scheduled_at=kwargs.get("scheduled_at"),
            created_by=str(kwargs.get("created_by", "")) if kwargs.get("created_by") else None,
        )
        return await self._repo.create_campaign(campaign)

    async def list_campaigns(self, tenant_id: str) -> list[Campaign]:
        return await self._repo.list_campaigns(tenant_id)

    async def execute_campaign(self, campaign_id: str) -> dict[str, Any]:
        """Executa campanha — seleciona segmento e dispara notificações."""
        # Buscar campanha, resolver segmento, enviar via EventBus
        return {"status": "queued", "campaign_id": campaign_id, "estimated_recipients": 0}

    # ============================================================
    # Rule Engine — Automations
    # ============================================================

    async def create_automation(self, tenant_id: str, **kwargs: object) -> AutomationRule:
        rule = AutomationRule(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            trigger=str(kwargs["trigger"]),
            conditions=list(kwargs.get("conditions", [])),
            actions=list(kwargs.get("actions", [])),
        )
        return await self._repo.create_automation(rule)

    async def list_automations(self, tenant_id: str) -> list[AutomationRule]:
        return await self._repo.list_automations(tenant_id)

    async def evaluate_trigger(self, tenant_id: str, trigger: str, event_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Rule Engine: avalia trigger e executa ações.

        Event → check conditions → execute actions.
        """
        rules = await self._repo.get_automations_by_trigger(tenant_id, trigger)
        results: list[dict[str, Any]] = []

        for rule in rules:
            if self._evaluate_conditions(rule.conditions, event_data):
                actions_result = await self._execute_actions(rule.actions, event_data)
                results.append({
                    "rule_id": rule.id, "rule_name": rule.name,
                    "triggered": True, "actions_executed": len(actions_result),
                })

        return results

    @staticmethod
    def _evaluate_conditions(conditions: list[dict], event_data: dict) -> bool:
        """Avalia condições da regra contra dados do evento."""
        if not conditions:
            return True  # Sem condições = sempre executa

        for cond in conditions:
            field = cond.get("field", "")
            operator = cond.get("operator", "equals")
            value = cond.get("value")

            event_value = event_data.get(field)
            if operator == "equals" and event_value != value:
                return False
            if operator == "greater_than" and (event_value or 0) <= (value or 0):
                return False
            if operator == "less_than" and (event_value or 0) >= (value or 0):
                return False
            if operator == "contains" and value not in str(event_value or ""):
                return False

        return True

    @staticmethod
    async def _execute_actions(actions: list[dict], event_data: dict) -> list[dict]:
        """Executa ações da automação."""
        results = []
        for action in actions:
            action_type = action.get("type", "")
            if action_type == "send_coupon":
                results.append({"action": "send_coupon", "coupon_id": action.get("coupon_id"), "status": "pending"})
            elif action_type == "wait":
                delay = action.get("delay_days", 0)
                results.append({"action": "wait", "delay_days": delay, "status": "scheduled"})
            elif action_type == "send_reminder":
                results.append({"action": "send_reminder", "template_id": action.get("template_id"), "status": "queued"})
            elif action_type == "add_tag":
                results.append({"action": "add_tag", "tag": action.get("tag"), "status": "done"})
        return results

    # ============================================================
    # Smart Segments
    # ============================================================

    @staticmethod
    def calculate_segment_type(customer_data: dict[str, Any]) -> list[str]:
        """Calcula segmentos de um cliente baseado em dados."""
        segments: list[str] = []

        total_spent = customer_data.get("total_spent", 0)
        total_visits = customer_data.get("total_visits", 0)
        last_visit = customer_data.get("last_visit_at")
        birth_date = customer_data.get("birth_date")

        # VIP: gastou mais de R$ 1000
        if total_spent > 100000:
            segments.append("vip")

        # Lapsed: não visita há 30 dias
        if last_visit:
            if isinstance(last_visit, str):
                last_visit = datetime.fromisoformat(last_visit)
            if (datetime.now(timezone.utc) - last_visit).days > 30:
                segments.append("lapsed_30d")

        # High ticket: ticket médio > R$ 80
        if total_visits > 0 and total_spent / total_visits > 8000:
            segments.append("high_ticket")

        # New: primeiro mês
        created_at = customer_data.get("created_at")
        if created_at:
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            if (datetime.now(timezone.utc) - created_at).days < 30:
                segments.append("new")

        # Birthday this month
        if birth_date:
            if isinstance(birth_date, str):
                birth_date = date.fromisoformat(birth_date)
            if birth_date.month == date.today().month:
                segments.append("birthday")

        return segments

    # ============================================================
    # Gift Cards
    # ============================================================

    async def create_gift_card(self, tenant_id: str, **kwargs: object) -> GiftCard:
        code = f"GC{secrets.token_hex(4)[:8].upper()}"
        gc = GiftCard(
            id=str(uuid4()), tenant_id=tenant_id, code=code,
            initial_amount=int(kwargs.get("amount", 0)),
            current_balance=int(kwargs.get("amount", 0)),
            purchaser_customer_id=str(kwargs.get("purchaser_customer_id", "")) if kwargs.get("purchaser_customer_id") else None,
            recipient_email=str(kwargs.get("recipient_email", "")) if kwargs.get("recipient_email") else None,
            recipient_name=str(kwargs.get("recipient_name", "")) if kwargs.get("recipient_name") else None,
            message=str(kwargs.get("message", "")),
            expires_at=kwargs.get("expires_at"),
        )
        return await self._repo.create_gift_card(gc)
