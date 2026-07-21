"""Customer Module — API Routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.customer.application.dto import (
    ConsentGrantRequest,
    ConsentResponse,
    CustomerCreateRequest,
    CustomerListResponse,
    CustomerProfileResponse,
    CustomerResponse,
    CustomerUpdateRequest,
    PreferenceResponse,
    PreferenceUpdateRequest,
    ReferralCreateRequest,
    ReferralResponse,
    ReviewCreateRequest,
    ReviewModerateRequest,
    ReviewRespondRequest,
    ReviewResponse,
    TagCreateRequest,
    TagResponse,
)
from app.modules.customer.application.customer_service import CustomerService
from app.modules.customer.infrastructure.repository import (
    ConsentRepository,
    CustomerPreferenceRepository,
    CustomerRepository,
    CustomerTagRepository,
    LoyaltyRepository,
    ReferralRepository,
    ReviewRepository,
)
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/customers", tags=["Customers"])


def _get_service(session: AsyncSession) -> CustomerService:
    return CustomerService(
        customer_repo=CustomerRepository(session),
        pref_repo=CustomerPreferenceRepository(session),
        tag_repo=CustomerTagRepository(session),
        review_repo=ReviewRepository(session),
        consent_repo=ConsentRepository(session),
        loyalty_repo=LoyaltyRepository(session),
        referral_repo=ReferralRepository(session),
    )


# ============================================================
# CUSTOMERS
# ============================================================

@router.get("", response_model=CustomerListResponse)
async def list_customers(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    status: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    search: str | None = Query(default=None, description="Busca por nome, telefone ou email"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> CustomerListResponse:
    svc = _get_service(session)
    if search:
        items, total = await svc.search_customers(tenant["id"], search, offset=offset, limit=limit)
    else:
        items, total = await svc.list_customers(tenant["id"], status=status, tag=tag, offset=offset, limit=limit)
    return CustomerListResponse(
        items=[CustomerResponse(**c.__dict__) for c in items],
        total=total, offset=offset, limit=limit,
    )


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    body: CustomerCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> CustomerResponse:
    svc = _get_service(session)
    c = await svc.create_customer(tenant["id"], **body.model_dump())
    return CustomerResponse(**c.__dict__)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> CustomerResponse:
    svc = _get_service(session)
    c = await svc.get_customer(customer_id)
    return CustomerResponse(**c.__dict__)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    body: CustomerUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> CustomerResponse:
    svc = _get_service(session)
    c = await svc.update_customer(customer_id, **body.model_dump(exclude_none=True))
    return CustomerResponse(**c.__dict__)


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_customer(customer_id)
    return {"message": "Cliente removido."}


# ============================================================
# CUSTOMER 360° PROFILE
# ============================================================

@router.get("/{customer_id}/profile")
async def get_profile(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    return await svc.get_profile(customer_id)


# ============================================================
# PREFERENCES
# ============================================================

@router.get("/{customer_id}/preferences", response_model=PreferenceResponse)
async def get_preferences(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> PreferenceResponse:
    svc = _get_service(session)
    p = await svc.get_preferences(customer_id)
    if p is None:
        return PreferenceResponse()
    return PreferenceResponse(**p.__dict__)


@router.put("/{customer_id}/preferences", response_model=PreferenceResponse)
async def update_preferences(
    customer_id: str,
    body: PreferenceUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> PreferenceResponse:
    svc = _get_service(session)
    p = await svc.update_preferences(customer_id, **body.model_dump(exclude_none=True))
    return PreferenceResponse(**p.__dict__)


# ============================================================
# TAGS
# ============================================================

@router.get("/tags/list", response_model=list[TagResponse])
async def list_tags(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[TagResponse]:
    svc = _get_service(session)
    tags = await svc.list_tags(tenant["id"])
    return [TagResponse(**t.__dict__) for t in tags]


@router.post("/tags", response_model=TagResponse, status_code=201)
async def create_tag(
    body: TagCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> TagResponse:
    svc = _get_service(session)
    t = await svc.create_tag(tenant["id"], **body.model_dump())
    return TagResponse(**t.__dict__)


@router.delete("/tags/{tag_id}")
async def delete_tag(
    tag_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_tag(tag_id)
    return {"message": "Tag removida."}


# ============================================================
# REVIEWS
# ============================================================

@router.get("/reviews", response_model=list[ReviewResponse])
async def list_reviews(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    visible_only: bool = Query(default=True),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> list[ReviewResponse]:
    svc = _get_service(session)
    items, _ = await svc.list_reviews(tenant["id"], visible_only=visible_only, offset=offset, limit=limit)
    return [ReviewResponse(**r.__dict__) for r in items]


@router.post("/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    body: ReviewCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> ReviewResponse:
    svc = _get_service(session)
    r = await svc.create_review(tenant["id"], **body.model_dump())
    return ReviewResponse(**r.__dict__)


@router.post("/reviews/{review_id}/moderate", response_model=ReviewResponse)
async def moderate_review(
    review_id: str,
    body: ReviewModerateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> ReviewResponse:
    svc = _get_service(session)
    r = await svc.moderate_review(review_id, body.is_visible)
    return ReviewResponse(**r.__dict__)


@router.post("/reviews/{review_id}/respond", response_model=ReviewResponse)
async def respond_to_review(
    review_id: str,
    body: ReviewRespondRequest,
    session: AsyncSession = Depends(get_async_session),
) -> ReviewResponse:
    svc = _get_service(session)
    r = await svc.respond_to_review(review_id, body.business_response)
    return ReviewResponse(**r.__dict__)


# ============================================================
# CONSENT (LGPD)
# ============================================================

@router.get("/{customer_id}/consents", response_model=list[ConsentResponse])
async def get_consents(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[ConsentResponse]:
    svc = _get_service(session)
    consents = await svc.get_consents(customer_id)
    return [ConsentResponse(**c.__dict__) for c in consents]


@router.post("/{customer_id}/consents", response_model=ConsentResponse, status_code=201)
async def grant_consent(
    customer_id: str,
    body: ConsentGrantRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> ConsentResponse:
    svc = _get_service(session)
    c = await svc.grant_consent(tenant["id"], customer_id, **body.model_dump())
    return ConsentResponse(**c.__dict__)


@router.post("/{customer_id}/consents/revoke-all")
async def revoke_all_consents(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.revoke_all_consents(customer_id)
    return {"message": "Todos os consentimentos revogados."}


# ============================================================
# LGPD EXPORT / ANONYMIZE
# ============================================================

@router.get("/{customer_id}/lgpd/export")
async def export_lgpd(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    return await svc.export_data(customer_id)


@router.post("/{customer_id}/lgpd/anonymize")
async def anonymize_lgpd(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.anonymize_customer(customer_id)
    return {"message": "Dados anonimizados conforme LGPD."}


# ============================================================
# LOYALTY
# ============================================================

@router.get("/{customer_id}/loyalty")
async def get_loyalty(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    acc = await svc.get_loyalty(customer_id)
    if acc is None:
        return {"points": 0, "tier": "bronze", "visit_count": 0}
    return {"points": acc.points, "tier": acc.tier, "total_earned": acc.total_earned, "total_redeemed": acc.total_redeemed, "visit_count": acc.visit_count}


@router.post("/{customer_id}/loyalty/earn")
async def earn_points(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
    points: int = Query(..., ge=1),
    visit: bool = Query(default=False),
    description: str = Query(default="Pontos ganhos"),
) -> dict:
    svc = _get_service(session)
    return await svc.earn_points(customer_id, points, visit=visit, description=description)


@router.post("/{customer_id}/loyalty/redeem")
async def redeem_points(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
    points: int = Query(..., ge=1),
    description: str = Query(default="Resgate de pontos"),
) -> dict:
    svc = _get_service(session)
    return await svc.redeem_points(customer_id, points, description=description)


@router.get("/{customer_id}/loyalty/transactions")
async def get_loyalty_transactions(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict:
    svc = _get_service(session)
    items, total = await svc.get_loyalty_transactions(customer_id, offset=offset, limit=limit)
    return {"items": items, "total": total}


# ============================================================
# REFERRALS
# ============================================================

@router.get("/{customer_id}/referrals", response_model=list[ReferralResponse])
async def list_referrals(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[ReferralResponse]:
    svc = _get_service(session)
    refs = await svc.get_referrals(customer_id)
    return [ReferralResponse(**r.__dict__) for r in refs]


@router.post("/{customer_id}/referrals", response_model=ReferralResponse, status_code=201)
async def create_referral_code(
    customer_id: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> ReferralResponse:
    svc = _get_service(session)
    ref = await svc.create_referral_code(tenant["id"], customer_id)
    return ReferralResponse(**ref.__dict__)


# ============================================================
# BLACKLIST / BLOCK
# ============================================================

@router.post("/{customer_id}/block")
async def block_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
    reason: str = Query(default="Cliente bloqueado."),
) -> dict:
    svc = _get_service(session)
    await svc.block_customer(customer_id, reason)
    return {"message": "Cliente bloqueado.", "reason": reason}


@router.post("/{customer_id}/unblock")
async def unblock_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.unblock_customer(customer_id)
    return {"message": "Cliente desbloqueado."}
