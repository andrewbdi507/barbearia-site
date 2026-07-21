"""Analytics Module — Repository."""

from datetime import date, datetime, timezone

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.domain.entities import AlertRule, Goal
from app.modules.analytics.infrastructure.models.analytics_models import AlertRuleModel, GoalModel


def _goal_to_entity(m: GoalModel) -> Goal:
    return Goal(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        metric=m.metric, target_value=m.target_value, current_value=m.current_value,
        period_start=m.period_start, period_end=m.period_end,
        professional_id=m.professional_id, is_active=m.is_active,
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _alert_to_entity(m: AlertRuleModel) -> AlertRule:
    return AlertRule(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        metric=m.metric, condition=m.condition, threshold=m.threshold,
        is_active=m.is_active, last_triggered_at=m.last_triggered_at,
        notification_channels=m.notification_channels or [],
        created_at=m.created_at,
    )


class GoalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def list_by_tenant(self, tenant_id: str) -> list[Goal]:
        r = await self._s.execute(
            select(GoalModel).where(GoalModel.tenant_id == tenant_id).where(GoalModel.is_active.is_(True))
        )
        return [_goal_to_entity(m) for m in r.scalars().all()]

    async def create(self, goal: Goal) -> Goal:
        m = GoalModel(
            id=goal.id, tenant_id=goal.tenant_id, name=goal.name,
            metric=goal.metric, target_value=goal.target_value,
            period_start=goal.period_start, period_end=goal.period_end,
            professional_id=goal.professional_id,
        )
        self._s.add(m)
        await self._s.flush()
        return _goal_to_entity(m)

    async def update_current(self, goal_id: str, value: int) -> None:
        await self._s.execute(
            update(GoalModel).where(GoalModel.id == goal_id).values(
                current_value=value, updated_at=datetime.now(timezone.utc),
            )
        )

    async def delete(self, goal_id: str) -> None:
        await self._s.execute(
            update(GoalModel).where(GoalModel.id == goal_id).values(is_active=False)
        )


class AlertRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def list_active(self, tenant_id: str) -> list[AlertRule]:
        r = await self._s.execute(
            select(AlertRuleModel).where(
                AlertRuleModel.tenant_id == tenant_id, AlertRuleModel.is_active.is_(True),
            )
        )
        return [_alert_to_entity(m) for m in r.scalars().all()]

    async def create(self, alert: AlertRule) -> AlertRule:
        m = AlertRuleModel(
            id=alert.id, tenant_id=alert.tenant_id, name=alert.name,
            metric=alert.metric, condition=alert.condition, threshold=alert.threshold,
            notification_channels=alert.notification_channels,
        )
        self._s.add(m)
        await self._s.flush()
        return _alert_to_entity(m)

    async def mark_triggered(self, alert_id: str) -> None:
        await self._s.execute(
            update(AlertRuleModel).where(AlertRuleModel.id == alert_id).values(
                last_triggered_at=datetime.now(timezone.utc),
            )
        )

    async def delete(self, alert_id: str) -> None:
        await self._s.execute(
            update(AlertRuleModel).where(AlertRuleModel.id == alert_id).values(is_active=False)
        )
