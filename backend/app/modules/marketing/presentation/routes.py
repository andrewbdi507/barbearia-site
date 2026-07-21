"""Marketing Module — API Routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.marketing.application.marketing_service import MarketingService
from app.modules.marketing.infrastructure.repository import MarketingRepository
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/marketing", tags=["Marketing"])


def _get_service(session: AsyncSession) -> MarketingService:
    return MarketingService(MarketingRepository(session))


# ============================================================
# COUPONS
# ============================================================

@router.get("/coupons")
async def list_coupons(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    coupons = await svc.list_coupons(tenant["id"])
    return [{"id": c.id, "code": c.code, "coupon_type": c.coupon_type,
             "value": c.value, "max_uses": c.max_uses, "current_uses": c.current_uses,
             "is_valid": c.is_valid} for c in coupons]


@router.post("/coupons", status_code=201)
async def create_coupon(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    c = await svc.create_coupon(tenant["id"], **body)
    return {"id": c.id, "code": c.code, "coupon_type": c.coupon_type, "value": c.value}


@router.post("/coupons/validate")
async def validate_coupon(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    return await svc.validate_coupon(
        tenant["id"],
        code=str(body["code"]),
        amount=int(body.get("amount", 0)),
        service_id=str(body.get("service_id", "")),
        customer_id=str(body.get("customer_id", "")),
    )


# ============================================================
# PROMOTIONS
# ============================================================

@router.get("/promotions")
async def list_promotions(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    service_id: str | None = Query(default=None),
) -> list[dict]:
    svc = _get_service(session)
    if service_id:
        promos = await svc.get_active_promotions(tenant["id"], service_id)
    else:
        promos = await svc.list_promotions(tenant["id"])
    return [{"id": p.id, "name": p.name, "promotion_type": p.promotion_type,
             "discount_type": p.discount_type, "discount_value": p.discount_value,
             "is_valid_now": p.is_valid_now} for p in promos]


@router.post("/promotions", status_code=201)
async def create_promotion(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    p = await svc.create_promotion(tenant["id"], **body)
    return {"id": p.id, "name": p.name, "promotion_type": p.promotion_type}


# ============================================================
# CAMPAIGNS
# ============================================================

@router.get("/campaigns")
async def list_campaigns(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    campaigns = await svc.list_campaigns(tenant["id"])
    return [{"id": c.id, "name": c.name, "channel": c.channel, "status": c.status,
             "segment_type": c.segment_type, "total_sent": c.total_sent} for c in campaigns]


@router.post("/campaigns", status_code=201)
async def create_campaign(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    c = await svc.create_campaign(tenant["id"], **body)
    return {"id": c.id, "name": c.name, "channel": c.channel, "status": c.status}


# ============================================================
# AUTOMATIONS (Rule Engine)
# ============================================================

@router.get("/automations")
async def list_automations(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    rules = await svc.list_automations(tenant["id"])
    return [{"id": r.id, "name": r.name, "trigger": r.trigger,
             "conditions": r.conditions, "actions": r.actions} for r in rules]


@router.post("/automations", status_code=201)
async def create_automation(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    r = await svc.create_automation(tenant["id"], **body)
    return {"id": r.id, "name": r.name, "trigger": r.trigger}


@router.post("/automations/evaluate")
async def evaluate_trigger(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    return await svc.evaluate_trigger(
        tenant["id"],
        trigger=str(body["trigger"]),
        event_data=body.get("event_data", {}),
    )


# ============================================================
# SMART SEGMENTS
# ============================================================

@router.post("/segments/calculate")
async def calculate_segments(body: dict) -> dict:
    segments = MarketingService.calculate_segment_type(body.get("customer_data", {}))
    return {"segments": segments}


# ============================================================
# GIFT CARDS
# ============================================================

@router.post("/gift-cards", status_code=201)
async def create_gift_card(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    gc = await svc.create_gift_card(tenant["id"], **body)
    return {"id": gc.id, "code": gc.code, "current_balance": gc.current_balance}
