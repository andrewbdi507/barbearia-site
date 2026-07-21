"""Customer Module — Repository Implementation."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, or_, select, update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.customer.domain.entities import (
    Consent,
    Customer,
    CustomerPreference,
    CustomerTag,
    LoyaltyAccount,
    LoyaltyTransaction,
    Referral,
    Review,
)
from app.modules.customer.domain.interfaces import (
    IConsentRepository,
    ICustomerPreferenceRepository,
    ICustomerRepository,
    ICustomerTagRepository,
    ILoyaltyRepository,
    IReferralRepository,
    IReviewRepository,
)
from app.modules.customer.infrastructure.models.customer_models import (
    ConsentModel,
    CustomerModel,
    CustomerPreferenceModel,
    CustomerTagModel,
    LoyaltyAccountModel,
    LoyaltyTransactionModel,
    ReferralModel,
    ReviewModel,
)


# ============================================================
# Mappers
# ============================================================

def _c_to_entity(m: CustomerModel) -> Customer:
    return Customer(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        phone=m.phone, email=m.email, photo_url=m.photo_url,
        birth_date=m.birth_date, gender=m.gender,
        street=m.street, city=m.city, state=m.state, zip_code=m.zip_code,
        notes=m.notes, tags=m.tags or [], status=m.status, source=m.source,
        total_visits=m.total_visits, total_spent=m.total_spent,
        last_visit_at=m.last_visit_at, last_booking_at=m.last_booking_at,
        metadata=m.metadata or {}, created_at=m.created_at, updated_at=m.updated_at,
        deleted_at=m.deleted_at,
    )


def _pref_to_entity(m: CustomerPreferenceModel) -> CustomerPreference:
    return CustomerPreference(
        id=m.id, customer_id=m.customer_id,
        favorite_professional_id=m.favorite_professional_id,
        favorite_service_ids=m.favorite_service_ids or [],
        preferred_time=m.preferred_time, preferred_day=m.preferred_day,
        communication_preferences=m.communication_preferences or {},
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _tag_to_entity(m: CustomerTagModel) -> CustomerTag:
    return CustomerTag(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        color_tag=m.color_tag, description=m.description or "",
        is_system=m.is_system, created_at=m.created_at,
    )


def _review_to_entity(m: ReviewModel) -> Review:
    return Review(
        id=m.id, tenant_id=m.tenant_id or "", booking_id=m.booking_id,
        customer_id=m.customer_id, professional_id=m.professional_id,
        rating=m.rating, comment=m.comment, tags=m.tags or [],
        is_visible=m.is_visible, is_anonymous=m.is_anonymous,
        business_response=m.business_response,
        business_response_at=m.business_response_at,
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _consent_to_entity(m: ConsentModel) -> Consent:
    return Consent(
        id=m.id, tenant_id=m.tenant_id or "", customer_id=m.customer_id,
        consent_type=m.consent_type, is_granted=m.is_granted,
        consent_version=m.consent_version, ip_address=m.ip_address,
        user_agent=m.user_agent, granted_at=m.granted_at, revoked_at=m.revoked_at,
    )


def _loyalty_to_entity(m: LoyaltyAccountModel) -> LoyaltyAccount:
    return LoyaltyAccount(
        id=m.id, tenant_id=m.tenant_id or "", customer_id=m.customer_id,
        points=m.points, total_earned=m.total_earned,
        total_redeemed=m.total_redeemed, tier=m.tier,
        visit_count=m.visit_count, created_at=m.created_at, updated_at=m.updated_at,
    )


def _ltxn_to_entity(m: LoyaltyTransactionModel) -> LoyaltyTransaction:
    return LoyaltyTransaction(
        id=m.id, loyalty_id=m.loyalty_id,
        transaction_type=m.transaction_type, points=m.points,
        reference_type=m.reference_type, reference_id=m.reference_id,
        description=m.description or "", created_at=m.created_at,
    )


def _ref_to_entity(m: ReferralModel) -> Referral:
    return Referral(
        id=m.id, tenant_id=m.tenant_id or "", referrer_id=m.referrer_id,
        referral_code=m.referral_code, referred_name=m.referred_name,
        referred_phone=m.referred_phone, referred_customer_id=m.referred_customer_id,
        status=m.status, reward_granted_at=m.reward_granted_at, created_at=m.created_at,
    )


# ============================================================
# CustomerRepository
# ============================================================

class CustomerRepository(ICustomerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, customer_id: str) -> Customer | None:
        r = await self._s.execute(
            select(CustomerModel).where(CustomerModel.id == customer_id)
            .options(selectinload(CustomerModel.preferences), selectinload(CustomerModel.loyalty))
        )
        m = r.scalar_one_or_none()
        return _c_to_entity(m) if m else None

    async def get_by_phone(self, tenant_id: str, phone: str) -> Customer | None:
        r = await self._s.execute(
            select(CustomerModel).where(
                CustomerModel.tenant_id == tenant_id, CustomerModel.phone == phone,
                CustomerModel.deleted_at.is_(None),
            )
        )
        m = r.scalar_one_or_none()
        return _c_to_entity(m) if m else None

    async def get_by_email(self, tenant_id: str, email: str) -> Customer | None:
        r = await self._s.execute(
            select(CustomerModel).where(
                CustomerModel.tenant_id == tenant_id, CustomerModel.email == email,
                CustomerModel.deleted_at.is_(None),
            )
        )
        m = r.scalar_one_or_none()
        return _c_to_entity(m) if m else None

    async def search(self, tenant_id: str, query: str, *, offset: int = 0, limit: int = 50) -> tuple[list[Customer], int]:
        pattern = f"%{query}%"
        base = select(CustomerModel).where(
            CustomerModel.tenant_id == tenant_id, CustomerModel.deleted_at.is_(None),
            or_(CustomerModel.name.ilike(pattern), CustomerModel.phone.ilike(pattern), CustomerModel.email.ilike(pattern)),
        )
        count_q = select(func.count()).select_from(CustomerModel).where(
            CustomerModel.tenant_id == tenant_id, CustomerModel.deleted_at.is_(None),
            or_(CustomerModel.name.ilike(pattern), CustomerModel.phone.ilike(pattern), CustomerModel.email.ilike(pattern)),
        )
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(CustomerModel.name).offset(offset).limit(limit))
        return [_c_to_entity(m) for m in r.scalars().all()], total

    async def list_by_tenant(self, tenant_id: str, *, status: str | None = None, tag: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Customer], int]:
        base = select(CustomerModel).where(CustomerModel.tenant_id == tenant_id, CustomerModel.deleted_at.is_(None))
        count_q = select(func.count()).select_from(CustomerModel).where(CustomerModel.tenant_id == tenant_id, CustomerModel.deleted_at.is_(None))
        if status:
            base = base.where(CustomerModel.status == status)
            count_q = count_q.where(CustomerModel.status == status)
        if tag:
            base = base.where(CustomerModel.tags.contains([tag]))
            count_q = count_q.where(CustomerModel.tags.contains([tag]))
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(CustomerModel.name).offset(offset).limit(limit))
        return [_c_to_entity(m) for m in r.scalars().all()], total

    async def create(self, c: Customer) -> Customer:
        m = CustomerModel(
            id=c.id, tenant_id=c.tenant_id, name=c.name,
            phone=c.phone, email=c.email, photo_url=c.photo_url,
            birth_date=c.birth_date, gender=c.gender,
            street=c.street, city=c.city, state=c.state, zip_code=c.zip_code,
            notes=c.notes, tags=c.tags, status=c.status, source=c.source,
            metadata=c.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return _c_to_entity(m)

    async def update(self, c: Customer) -> Customer:
        m = await self._s.get(CustomerModel, c.id)
        if not m:
            raise ValueError(f"Customer {c.id} not found")
        for f in ("name", "phone", "email", "photo_url", "birth_date", "gender",
                   "street", "city", "state", "zip_code", "notes", "tags", "status", "metadata"):
            setattr(m, f, getattr(c, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _c_to_entity(m)

    async def soft_delete(self, customer_id: str) -> None:
        await self._s.execute(
            update(CustomerModel).where(CustomerModel.id == customer_id)
            .values(deleted_at=datetime.now(timezone.utc), status="inactive")
        )

    async def anonymize(self, customer_id: str) -> None:
        await self._s.execute(
            update(CustomerModel).where(CustomerModel.id == customer_id).values(
                name="ANONYMIZED", email=None, phone="00000000000", photo_url=None,
                status="anonymized", notes="[LGPD] Dados anonimizados.",
            )
        )

    async def update_visit_stats(self, customer_id: str, amount: int) -> None:
        await self._s.execute(
            update(CustomerModel).where(CustomerModel.id == customer_id).values(
                total_visits=CustomerModel.total_visits + 1,
                total_spent=CustomerModel.total_spent + amount,
                last_visit_at=datetime.now(timezone.utc),
            )
        )


# ============================================================
# Preference Repository
# ============================================================

class CustomerPreferenceRepository(ICustomerPreferenceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_customer(self, customer_id: str) -> CustomerPreference | None:
        r = await self._s.execute(
            select(CustomerPreferenceModel).where(CustomerPreferenceModel.customer_id == customer_id)
        )
        m = r.scalar_one_or_none()
        return _pref_to_entity(m) if m else None

    async def upsert(self, pref: CustomerPreference) -> CustomerPreference:
        r = await self._s.execute(
            select(CustomerPreferenceModel).where(CustomerPreferenceModel.customer_id == pref.customer_id)
        )
        m = r.scalar_one_or_none()
        if m:
            for f in ("favorite_professional_id", "favorite_service_ids", "preferred_time",
                       "preferred_day", "communication_preferences"):
                setattr(m, f, getattr(pref, f))
            m.updated_at = datetime.now(timezone.utc)
        else:
            m = CustomerPreferenceModel(
                id=pref.id, customer_id=pref.customer_id,
                favorite_professional_id=pref.favorite_professional_id,
                favorite_service_ids=pref.favorite_service_ids,
                preferred_time=pref.preferred_time, preferred_day=pref.preferred_day,
                communication_preferences=pref.communication_preferences,
            )
            self._s.add(m)
        await self._s.flush()
        return _pref_to_entity(m)


# ============================================================
# Tag Repository
# ============================================================

class CustomerTagRepository(ICustomerTagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def list_by_tenant(self, tenant_id: str) -> list[CustomerTag]:
        r = await self._s.execute(
            select(CustomerTagModel).where(CustomerTagModel.tenant_id == tenant_id).order_by(CustomerTagModel.name)
        )
        return [_tag_to_entity(m) for m in r.scalars().all()]

    async def create(self, tag: CustomerTag) -> CustomerTag:
        m = CustomerTagModel(id=tag.id, tenant_id=tag.tenant_id, name=tag.name,
                             color_tag=tag.color_tag, description=tag.description)
        self._s.add(m)
        await self._s.flush()
        return _tag_to_entity(m)

    async def delete(self, tag_id: str) -> None:
        await self._s.execute(sa_delete(CustomerTagModel).where(CustomerTagModel.id == tag_id))


# ============================================================
# Review Repository
# ============================================================

class ReviewRepository(IReviewRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_booking(self, booking_id: str) -> Review | None:
        r = await self._s.execute(select(ReviewModel).where(ReviewModel.booking_id == booking_id))
        m = r.scalar_one_or_none()
        return _review_to_entity(m) if m else None

    async def list_for_customer(self, customer_id: str) -> list[Review]:
        r = await self._s.execute(select(ReviewModel).where(ReviewModel.customer_id == customer_id).order_by(ReviewModel.created_at.desc()))
        return [_review_to_entity(m) for m in r.scalars().all()]

    async def list_for_professional(self, professional_id: str, *, offset: int = 0, limit: int = 50) -> tuple[list[Review], int]:
        base = select(ReviewModel).where(ReviewModel.professional_id == professional_id)
        count_q = select(func.count()).select_from(ReviewModel).where(ReviewModel.professional_id == professional_id)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(ReviewModel.created_at.desc()).offset(offset).limit(limit))
        return [_review_to_entity(m) for m in r.scalars().all()], total

    async def list_for_tenant(self, tenant_id: str, *, visible_only: bool = True, offset: int = 0, limit: int = 50) -> tuple[list[Review], int]:
        base = select(ReviewModel).where(ReviewModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(ReviewModel).where(ReviewModel.tenant_id == tenant_id)
        if visible_only:
            base = base.where(ReviewModel.is_visible.is_(True))
            count_q = count_q.where(ReviewModel.is_visible.is_(True))
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(ReviewModel.created_at.desc()).offset(offset).limit(limit))
        return [_review_to_entity(m) for m in r.scalars().all()], total

    async def create(self, review: Review) -> Review:
        m = ReviewModel(
            id=review.id, tenant_id=review.tenant_id, booking_id=review.booking_id,
            customer_id=review.customer_id, professional_id=review.professional_id,
            rating=review.rating, comment=review.comment, tags=review.tags,
            is_visible=review.is_visible, is_anonymous=review.is_anonymous,
        )
        self._s.add(m)
        await self._s.flush()
        return _review_to_entity(m)

    async def update(self, review: Review) -> Review:
        m = await self._s.get(ReviewModel, review.id)
        if not m:
            raise ValueError(f"Review {review.id} not found")
        m.is_visible = review.is_visible
        m.business_response = review.business_response
        m.business_response_at = review.business_response_at
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _review_to_entity(m)


# ============================================================
# Consent, Loyalty, Referral Repositories (compact)
# ============================================================

class ConsentRepository(IConsentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_customer(self, customer_id: str) -> list[Consent]:
        r = await self._s.execute(select(ConsentModel).where(ConsentModel.customer_id == customer_id))
        return [_consent_to_entity(m) for m in r.scalars().all()]

    async def grant(self, consent: Consent) -> Consent:
        m = ConsentModel(
            id=consent.id, tenant_id=consent.tenant_id, customer_id=consent.customer_id,
            consent_type=consent.consent_type, is_granted=consent.is_granted,
            consent_version=consent.consent_version,
            ip_address=consent.ip_address, user_agent=consent.user_agent,
        )
        self._s.add(m)
        await self._s.flush()
        return _consent_to_entity(m)

    async def revoke_all(self, customer_id: str) -> None:
        await self._s.execute(
            update(ConsentModel).where(ConsentModel.customer_id == customer_id).values(
                is_granted=False, revoked_at=datetime.now(timezone.utc),
            )
        )


class LoyaltyRepository(ILoyaltyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_customer(self, customer_id: str) -> LoyaltyAccount | None:
        r = await self._s.execute(
            select(LoyaltyAccountModel).where(LoyaltyAccountModel.customer_id == customer_id)
        )
        m = r.scalar_one_or_none()
        return _loyalty_to_entity(m) if m else None

    async def create(self, account: LoyaltyAccount) -> LoyaltyAccount:
        m = LoyaltyAccountModel(
            id=account.id, tenant_id=account.tenant_id, customer_id=account.customer_id,
            points=account.points, tier=account.tier,
        )
        self._s.add(m)
        await self._s.flush()
        return _loyalty_to_entity(m)

    async def update(self, account: LoyaltyAccount) -> LoyaltyAccount:
        m = await self._s.get(LoyaltyAccountModel, account.id)
        if not m:
            raise ValueError(f"LoyaltyAccount {account.id} not found")
        for f in ("points", "total_earned", "total_redeemed", "tier", "visit_count"):
            setattr(m, f, getattr(account, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _loyalty_to_entity(m)

    async def add_transaction(self, txn: LoyaltyTransaction) -> LoyaltyTransaction:
        m = LoyaltyTransactionModel(
            id=txn.id, loyalty_id=txn.loyalty_id,
            transaction_type=txn.transaction_type, points=txn.points,
            reference_type=txn.reference_type, reference_id=txn.reference_id,
            description=txn.description,
        )
        self._s.add(m)
        await self._s.flush()
        return txn

    async def get_transactions(self, loyalty_id: str, *, offset: int = 0, limit: int = 50) -> tuple[list[LoyaltyTransaction], int]:
        base = select(LoyaltyTransactionModel).where(LoyaltyTransactionModel.loyalty_id == loyalty_id)
        count_q = select(func.count()).select_from(LoyaltyTransactionModel).where(LoyaltyTransactionModel.loyalty_id == loyalty_id)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(LoyaltyTransactionModel.created_at.desc()).offset(offset).limit(limit))
        return [_ltxn_to_entity(m) for m in r.scalars().all()], total


class ReferralRepository(IReferralRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_code(self, code: str) -> Referral | None:
        r = await self._s.execute(select(ReferralModel).where(ReferralModel.referral_code == code))
        m = r.scalar_one_or_none()
        return _ref_to_entity(m) if m else None

    async def list_for_referrer(self, referrer_id: str) -> list[Referral]:
        r = await self._s.execute(select(ReferralModel).where(ReferralModel.referrer_id == referrer_id).order_by(ReferralModel.created_at.desc()))
        return [_ref_to_entity(m) for m in r.scalars().all()]

    async def create(self, ref: Referral) -> Referral:
        m = ReferralModel(
            id=ref.id, tenant_id=ref.tenant_id, referrer_id=ref.referrer_id,
            referral_code=ref.referral_code, referred_name=ref.referred_name,
            referred_phone=ref.referred_phone, status=ref.status,
        )
        self._s.add(m)
        await self._s.flush()
        return _ref_to_entity(m)

    async def update(self, ref: Referral) -> Referral:
        m = await self._s.get(ReferralModel, ref.id)
        if not m:
            raise ValueError(f"Referral {ref.id} not found")
        for f in ("status", "referred_customer_id", "reward_granted_at"):
            setattr(m, f, getattr(ref, f))
        await self._s.flush()
        return _ref_to_entity(m)
