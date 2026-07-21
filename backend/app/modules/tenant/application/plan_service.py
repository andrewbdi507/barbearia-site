"""Tenant Module — Plan & Subscription Service.

Gerencia planos, assinaturas e billing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.tenant.domain.entities import Plan, Subscription
from app.modules.tenant.domain.enums import BillingCycle, SubscriptionStatus
from app.modules.tenant.domain.interfaces import (
    IPlanRepository,
    ISubscriptionRepository,
    ITenantCache,
    ITenantRepository,
)
from app.modules.tenant.domain.value_objects import PlanLimits


class PlanService:
    """Serviço para gerenciamento de planos e assinaturas."""

    def __init__(
        self,
        plan_repo: IPlanRepository,
        sub_repo: ISubscriptionRepository,
        tenant_repo: ITenantRepository,
        cache: ITenantCache,
    ) -> None:
        self._plans = plan_repo
        self._subscriptions = sub_repo
        self._tenants = tenant_repo
        self._cache = cache

    # ============================================================
    # Plans
    # ============================================================

    async def list_active_plans(self) -> list[Plan]:
        return await self._plans.list_active()

    async def list_all_plans(self) -> list[Plan]:
        return await self._plans.list_all()

    async def get_plan(self, plan_id: str) -> Plan:
        # Check cache
        cached = await self._cache.get_plan(plan_id)
        if cached:
            return Plan(**cached)

        plan = await self._plans.get_by_id(plan_id)
        if plan is None:
            raise NotFoundError(message="Plano não encontrado.")
        await self._cache.set_plan(plan_id, {
            "id": plan.id, "name": plan.name, "slug": plan.slug,
            "limits": plan.limits.to_dict(), "features": plan.features,
        })
        return plan

    async def create_plan(self, **kwargs: object) -> Plan:
        plan_id = str(uuid4())
        limits_data = kwargs.pop("limits", {})
        limits = PlanLimits.from_dict(limits_data if isinstance(limits_data, dict) else {})

        plan = Plan(id=plan_id, limits=limits, **kwargs)
        return await self._plans.create(plan)

    async def update_plan(self, plan_id: str, **kwargs: object) -> Plan:
        existing = await self.get_plan(plan_id)
        for key, value in kwargs.items():
            if hasattr(existing, key) and value is not None:
                setattr(existing, key, value)
        updated = await self._plans.update(existing)
        await self._cache.set_plan(plan_id, {
            "id": updated.id, "name": updated.name, "slug": updated.slug,
            "limits": updated.limits.to_dict(), "features": updated.features,
        })
        return updated

    # ============================================================
    # Subscriptions
    # ============================================================

    async def get_active_subscription(self, tenant_id: str) -> Subscription | None:
        return await self._subscriptions.get_active_for_tenant(tenant_id)

    async def get_history(self, tenant_id: str) -> list[Subscription]:
        return await self._subscriptions.get_history_for_tenant(tenant_id)

    async def change_plan(
        self, tenant_id: str, new_plan_slug: str, billing_cycle: str = "monthly"
    ) -> Subscription:
        """Upgrade ou downgrade de plano."""
        plan = await self._plans.get_by_slug(new_plan_slug)
        if plan is None:
            raise NotFoundError(message=f"Plano '{new_plan_slug}' não encontrado.")

        current = await self._subscriptions.get_active_for_tenant(tenant_id)
        if current is None:
            raise BusinessRuleError(message="Nenhuma assinatura ativa encontrada.")

        # Cancelar assinatura atual
        await self._subscriptions.update_status(current.id, SubscriptionStatus.CANCELLED)

        # Criar nova assinatura
        now = datetime.now(timezone.utc)
        new_sub = Subscription(
            id=str(uuid4()),
            tenant_id=tenant_id,
            plan_id=plan.id,
            status=SubscriptionStatus.ACTIVE,
            billing_cycle=billing_cycle,
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
        )
        created = await self._subscriptions.create(new_sub)

        # Atualizar tenant
        await self._tenants.update_status(tenant_id, "active")

        return created
