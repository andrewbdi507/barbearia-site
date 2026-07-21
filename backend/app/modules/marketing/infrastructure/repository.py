"""Marketing Module — SQLAlchemy Models + Repository."""

from __future__ import annotations

from datetime import date as date_type, datetime, timezone

from sqlalchemy import (
    Boolean, Date, DateTime, Integer, String, Text, UniqueConstraint, func, select, update,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import BaseModel
from app.modules.marketing.domain.entities import (
    AutomationRule, Campaign, Coupon, GiftCard, Promotion,
)


class CouponModel(BaseModel):
    __tablename__ = "marketing_coupons"

    code: Mapped[str] = mapped_column(String(50), nullable=False)
    coupon_type: Mapped[str] = mapped_column(String(20), default="fixed")
    value: Mapped[int] = mapped_column(Integer, default=0)
    min_purchase_amount: Mapped[int] = mapped_column(Integer, default=0)
    max_uses: Mapped[int] = mapped_column(Integer, default=0)
    current_uses: Mapped[int] = mapped_column(Integer, default=0)
    max_per_customer: Mapped[int] = mapped_column(Integer, default=1)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    applies_to: Mapped[str] = mapped_column(String(30), default="all")
    applicable_ids: Mapped[list] = mapped_column(JSONB, default=list)
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)

    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_coupon_tenant_code"),)


class PromotionModel(BaseModel):
    __tablename__ = "marketing_promotions"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    promotion_type: Mapped[str] = mapped_column(String(30), default="time_period")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    discount_type: Mapped[str] = mapped_column(String(20), default="percentage")
    discount_value: Mapped[int] = mapped_column(Integer, default=0)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    applicable_days: Mapped[list] = mapped_column(JSONB, default=list)
    applicable_hours_start: Mapped[str | None] = mapped_column(String(5), nullable=True)
    applicable_hours_end: Mapped[str | None] = mapped_column(String(5), nullable=True)
    service_ids: Mapped[list] = mapped_column(JSONB, default=list)
    bundle_service_ids: Mapped[list] = mapped_column(JSONB, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class CampaignModel(BaseModel):
    __tablename__ = "marketing_campaigns"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    channel: Mapped[str] = mapped_column(String(20), default="whatsapp")
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    segment_type: Mapped[str] = mapped_column(String(30), default="custom")
    segment_filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    template_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    coupon_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_sent: Mapped[int] = mapped_column(Integer, default=0)
    total_opened: Mapped[int] = mapped_column(Integer, default=0)
    total_converted: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)


class AutomationRuleModel(BaseModel):
    __tablename__ = "marketing_automations"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    trigger: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    conditions: Mapped[list] = mapped_column(JSONB, default=list)
    actions: Mapped[list] = mapped_column(JSONB, default=list)


class GiftCardModel(BaseModel):
    __tablename__ = "marketing_gift_cards"

    code: Mapped[str] = mapped_column(String(50), nullable=False)
    initial_amount: Mapped[int] = mapped_column(Integer, default=0)
    current_balance: Mapped[int] = mapped_column(Integer, default=0)
    purchaser_customer_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    recipient_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_redeemed: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_giftcard_tenant_code"),)


# ============================================================
# Repository
# ============================================================

class MarketingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    # Coupons
    async def get_coupon_by_code(self, tenant_id: str, code: str) -> Coupon | None:
        r = await self._s.execute(
            select(CouponModel).where(CouponModel.tenant_id == tenant_id, CouponModel.code == code.upper())
        )
        m = r.scalar_one_or_none()
        return self._coupon_to_entity(m) if m else None

    async def create_coupon(self, c: Coupon) -> Coupon:
        m = CouponModel(id=c.id, tenant_id=c.tenant_id, code=c.code.upper(),
                        coupon_type=c.coupon_type, value=c.value,
                        min_purchase_amount=c.min_purchase_amount,
                        max_uses=c.max_uses, max_per_customer=c.max_per_customer,
                        starts_at=c.starts_at, expires_at=c.expires_at,
                        applies_to=c.applies_to, applicable_ids=c.applicable_ids, created_by=c.created_by)
        self._s.add(m)
        await self._s.flush()
        return c

    async def use_coupon(self, coupon_id: str) -> None:
        await self._s.execute(
            update(CouponModel).where(CouponModel.id == coupon_id)
            .values(current_uses=CouponModel.current_uses + 1)
        )

    async def list_coupons(self, tenant_id: str) -> list[Coupon]:
        r = await self._s.execute(select(CouponModel).where(CouponModel.tenant_id == tenant_id))
        return [self._coupon_to_entity(m) for m in r.scalars().all()]

    # Promotions
    async def create_promotion(self, p: Promotion) -> Promotion:
        m = PromotionModel(id=p.id, tenant_id=p.tenant_id, name=p.name,
                           promotion_type=p.promotion_type, discount_type=p.discount_type,
                           discount_value=p.discount_value, starts_at=p.starts_at, ends_at=p.ends_at,
                           applicable_days=p.applicable_days,
                           applicable_hours_start=p.applicable_hours_start,
                           applicable_hours_end=p.applicable_hours_end,
                           service_ids=p.service_ids, bundle_service_ids=p.bundle_service_ids)
        self._s.add(m)
        await self._s.flush()
        return p

    async def list_promotions(self, tenant_id: str) -> list[Promotion]:
        r = await self._s.execute(select(PromotionModel).where(PromotionModel.tenant_id == tenant_id))
        return [self._promo_to_entity(m) for m in r.scalars().all()]

    # Campaigns
    async def create_campaign(self, c: Campaign) -> Campaign:
        m = CampaignModel(id=c.id, tenant_id=c.tenant_id, name=c.name,
                          channel=c.channel, status=c.status,
                          segment_type=c.segment_type, segment_filters=c.segment_filters,
                          template_id=c.template_id, coupon_id=c.coupon_id,
                          scheduled_at=c.scheduled_at, created_by=c.created_by)
        self._s.add(m)
        await self._s.flush()
        return c

    async def list_campaigns(self, tenant_id: str) -> list[Campaign]:
        r = await self._s.execute(select(CampaignModel).where(CampaignModel.tenant_id == tenant_id))
        return [self._campaign_to_entity(m) for m in r.scalars().all()]

    # Automations
    async def create_automation(self, a: AutomationRule) -> AutomationRule:
        m = AutomationRuleModel(id=a.id, tenant_id=a.tenant_id, name=a.name,
                                trigger=a.trigger, conditions=a.conditions, actions=a.actions)
        self._s.add(m)
        await self._s.flush()
        return a

    async def list_automations(self, tenant_id: str) -> list[AutomationRule]:
        r = await self._s.execute(select(AutomationRuleModel).where(AutomationRuleModel.tenant_id == tenant_id))
        return [self._auto_to_entity(m) for m in r.scalars().all()]

    async def get_automations_by_trigger(self, tenant_id: str, trigger: str) -> list[AutomationRule]:
        r = await self._s.execute(
            select(AutomationRuleModel).where(
                AutomationRuleModel.tenant_id == tenant_id,
                AutomationRuleModel.trigger == trigger,
                AutomationRuleModel.is_active.is_(True),
            )
        )
        return [self._auto_to_entity(m) for m in r.scalars().all()]

    # Gift Cards
    async def create_gift_card(self, gc: GiftCard) -> GiftCard:
        m = GiftCardModel(id=gc.id, tenant_id=gc.tenant_id, code=gc.code.upper(),
                          initial_amount=gc.initial_amount, current_balance=gc.current_balance,
                          purchaser_customer_id=gc.purchaser_customer_id,
                          recipient_email=gc.recipient_email, recipient_name=gc.recipient_name,
                          message=gc.message, expires_at=gc.expires_at)
        self._s.add(m)
        await self._s.flush()
        return gc

    # Mappers
    @staticmethod
    def _coupon_to_entity(m: CouponModel) -> Coupon:
        return Coupon(
            id=m.id, tenant_id=m.tenant_id or "", code=m.code,
            coupon_type=m.coupon_type, value=m.value,
            min_purchase_amount=m.min_purchase_amount,
            max_uses=m.max_uses, current_uses=m.current_uses,
            max_per_customer=m.max_per_customer,
            starts_at=m.starts_at, expires_at=m.expires_at,
            is_active=m.is_active, applies_to=m.applies_to,
            applicable_ids=m.applicable_ids or [], created_by=m.created_by,
            created_at=m.created_at,
        )

    @staticmethod
    def _promo_to_entity(m: PromotionModel) -> Promotion:
        return Promotion(
            id=m.id, tenant_id=m.tenant_id or "", name=m.name,
            promotion_type=m.promotion_type, description=m.description or "",
            discount_type=m.discount_type, discount_value=m.discount_value,
            starts_at=m.starts_at, ends_at=m.ends_at,
            applicable_days=m.applicable_days or [],
            applicable_hours_start=m.applicable_hours_start,
            applicable_hours_end=m.applicable_hours_end,
            service_ids=m.service_ids or [], bundle_service_ids=m.bundle_service_ids or [],
            is_active=m.is_active, created_at=m.created_at,
        )

    @staticmethod
    def _campaign_to_entity(m: CampaignModel) -> Campaign:
        return Campaign(
            id=m.id, tenant_id=m.tenant_id or "", name=m.name,
            description=m.description or "", channel=m.channel, status=m.status,
            segment_type=m.segment_type, segment_filters=m.segment_filters or {},
            template_id=m.template_id, coupon_id=m.coupon_id,
            scheduled_at=m.scheduled_at, started_at=m.started_at, completed_at=m.completed_at,
            total_sent=m.total_sent, total_opened=m.total_opened, total_converted=m.total_converted,
            created_by=m.created_by, created_at=m.created_at,
        )

    @staticmethod
    def _auto_to_entity(m: AutomationRuleModel) -> AutomationRule:
        return AutomationRule(
            id=m.id, tenant_id=m.tenant_id or "", name=m.name,
            trigger=m.trigger, is_active=m.is_active,
            conditions=m.conditions or [], actions=m.actions or [],
            created_at=m.created_at,
        )
