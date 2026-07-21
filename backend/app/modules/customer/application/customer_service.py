"""Customer Module — Application Service."""

from __future__ import annotations

import secrets
from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.customer.domain.entities import (
    Consent,
    Customer,
    CustomerPreference,
    CustomerTag,
    LoyaltyAccount,
    Referral,
    Review,
)
from app.modules.customer.domain.enums import (
    ConsentType,
    CustomerStatus,
    LoyaltyTier,
    LoyaltyTransactionType,
    ReferralStatus,
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


class CustomerService:
    """Serviço de CRM — orquestração completa."""

    def __init__(
        self,
        customer_repo: ICustomerRepository,
        pref_repo: ICustomerPreferenceRepository,
        tag_repo: ICustomerTagRepository,
        review_repo: IReviewRepository,
        consent_repo: IConsentRepository,
        loyalty_repo: ILoyaltyRepository,
        referral_repo: IReferralRepository,
    ) -> None:
        self._customers = customer_repo
        self._prefs = pref_repo
        self._tags = tag_repo
        self._reviews = review_repo
        self._consents = consent_repo
        self._loyalty = loyalty_repo
        self._referrals = referral_repo

    # ============================================================
    # Customer CRUD
    # ============================================================

    async def create_customer(self, tenant_id: str, **kwargs: object) -> Customer:
        phone = str(kwargs.get("phone", "")) if kwargs.get("phone") else None
        if phone:
            existing = await self._customers.get_by_phone(tenant_id, phone)
            if existing:
                raise BusinessRuleError(message="Já existe cliente com este telefone.")

        c = Customer(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            phone=phone,
            email=str(kwargs.get("email", "")) if kwargs.get("email") else None,
            birth_date=kwargs.get("birth_date"),
            gender=str(kwargs.get("gender", "")) if kwargs.get("gender") else None,
            notes=str(kwargs.get("notes", "")) if kwargs.get("notes") else None,
            tags=list(kwargs.get("tags", [])),
            source=str(kwargs.get("source", "admin")),
        )
        created = await self._customers.create(c)

        # Criar loyalty account automaticamente
        await self._loyalty.create(LoyaltyAccount(
            id=str(uuid4()), tenant_id=tenant_id, customer_id=created.id,
        ))

        return created

    async def get_customer(self, customer_id: str) -> Customer:
        c = await self._customers.get_by_id(customer_id)
        if c is None:
            raise NotFoundError(message="Cliente não encontrado.")
        return c

    async def search_customers(self, tenant_id: str, query: str, *, offset: int = 0, limit: int = 50) -> tuple[list[Customer], int]:
        return await self._customers.search(tenant_id, query, offset=offset, limit=limit)

    async def list_customers(self, tenant_id: str, *, status: str | None = None, tag: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Customer], int]:
        return await self._customers.list_by_tenant(tenant_id, status=status, tag=tag, offset=offset, limit=limit)

    async def update_customer(self, customer_id: str, **kwargs: object) -> Customer:
        existing = await self.get_customer(customer_id)
        for k, v in kwargs.items():
            if hasattr(existing, k) and v is not None:
                setattr(existing, k, v)
        return await self._customers.update(existing)

    async def delete_customer(self, customer_id: str) -> None:
        await self._customers.soft_delete(customer_id)

    # ============================================================
    # Customer 360° Profile
    # ============================================================

    async def get_profile(self, customer_id: str) -> dict[str, Any]:
        """Customer 360° View — agrega dados de todos os módulos."""
        customer = await self.get_customer(customer_id)
        prefs = await self._prefs.get_for_customer(customer_id)
        loyalty = await self._loyalty.get_for_customer(customer_id)
        reviews = await self._reviews.list_for_customer(customer_id)
        referrals = await self._referrals.list_for_referrer(customer_id)
        consents = await self._consents.get_for_customer(customer_id)

        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0

        return {
            "customer": customer.__dict__,
            "preferences": prefs.__dict__ if prefs else None,
            "loyalty": {
                "points": loyalty.points if loyalty else 0,
                "total_earned": loyalty.total_earned if loyalty else 0,
                "total_redeemed": loyalty.total_redeemed if loyalty else 0,
                "tier": loyalty.tier if loyalty else "bronze",
                "visit_count": loyalty.visit_count if loyalty else 0,
            },
            "reviews": [r.__dict__ for r in reviews],
            "referrals": [r.__dict__ for r in referrals],
            "consents": [c.__dict__ for c in consents],
            "stats": {
                "total_visits": customer.total_visits,
                "total_spent": customer.total_spent,
                "avg_ticket": customer.total_spent // customer.total_visits if customer.total_visits > 0 else 0,
                "avg_rating": round(avg_rating, 1),
                "last_visit_at": customer.last_visit_at.isoformat() if customer.last_visit_at else None,
            },
        }

    # ============================================================
    # Preferences
    # ============================================================

    async def update_preferences(self, customer_id: str, **kwargs: object) -> CustomerPreference:
        existing = await self._prefs.get_for_customer(customer_id)
        pref = existing or CustomerPreference(id=str(uuid4()), customer_id=customer_id)
        for k, v in kwargs.items():
            if hasattr(pref, k) and v is not None:
                setattr(pref, k, v)
        return await self._prefs.upsert(pref)

    async def get_preferences(self, customer_id: str) -> CustomerPreference | None:
        return await self._prefs.get_for_customer(customer_id)

    # ============================================================
    # Tags
    # ============================================================

    async def list_tags(self, tenant_id: str) -> list[CustomerTag]:
        return await self._tags.list_by_tenant(tenant_id)

    async def create_tag(self, tenant_id: str, **kwargs: object) -> CustomerTag:
        tag = CustomerTag(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            color_tag=str(kwargs.get("color_tag", "#cccccc")),
            description=str(kwargs.get("description", "")),
        )
        return await self._tags.create(tag)

    async def delete_tag(self, tag_id: str) -> None:
        await self._tags.delete(tag_id)

    # ============================================================
    # Reviews
    # ============================================================

    async def create_review(self, tenant_id: str, **kwargs: object) -> Review:
        booking_id = str(kwargs["booking_id"])
        existing = await self._reviews.get_by_booking(booking_id)
        if existing:
            raise BusinessRuleError(message="Este agendamento já foi avaliado.")

        review = Review(
            id=str(uuid4()), tenant_id=tenant_id,
            booking_id=booking_id,
            customer_id=str(kwargs.get("customer_id", "")),
            professional_id=str(kwargs.get("professional_id", "")),
            rating=int(kwargs.get("rating", 5)),
            comment=str(kwargs.get("comment", "")) if kwargs.get("comment") else None,
            tags=list(kwargs.get("tags", [])),
            is_anonymous=bool(kwargs.get("is_anonymous", False)),
            is_visible=False,  # Requer moderação
        )
        return await self._reviews.create(review)

    async def moderate_review(self, review_id: str, approved: bool) -> Review:
        review = await self._reviews.list_for_customer("")  # workaround
        # Find by id
        r = None
        # Use list for tenant approach
        r = await self._reviews.list_for_tenant("", visible_only=False, offset=0, limit=1000)
        found = next((x for x in r[0] if x.id == review_id), None)
        if found is None:
            raise NotFoundError(message="Avaliação não encontrada.")
        found.moderate(approved)
        return await self._reviews.update(found)

    async def respond_to_review(self, review_id: str, response: str) -> Review:
        r = await self._reviews.list_for_tenant("", visible_only=False, offset=0, limit=1000)
        found = next((x for x in r[0] if x.id == review_id), None)
        if found is None:
            raise NotFoundError(message="Avaliação não encontrada.")
        found.respond(response)
        return await self._reviews.update(found)

    async def list_reviews(self, tenant_id: str, *, visible_only: bool = True, offset: int = 0, limit: int = 50) -> tuple[list[Review], int]:
        return await self._reviews.list_for_tenant(tenant_id, visible_only=visible_only, offset=offset, limit=limit)

    # ============================================================
    # Consent (LGPD)
    # ============================================================

    async def grant_consent(self, tenant_id: str, customer_id: str, **kwargs: object) -> Consent:
        consent = Consent(
            id=str(uuid4()), tenant_id=tenant_id, customer_id=customer_id,
            consent_type=str(kwargs["consent_type"]),
            is_granted=bool(kwargs.get("is_granted", True)),
            consent_version=str(kwargs.get("consent_version", "1.0")),
        )
        return await self._consents.grant(consent)

    async def revoke_all_consents(self, customer_id: str) -> None:
        await self._consents.revoke_all(customer_id)

    async def get_consents(self, customer_id: str) -> list[Consent]:
        return await self._consents.get_for_customer(customer_id)

    # ============================================================
    # LGPD — Export / Anonymize
    # ============================================================

    async def export_data(self, customer_id: str) -> dict[str, Any]:
        """Exporta TODOS os dados do cliente (LGPD Art. 18)."""
        profile = await self.get_profile(customer_id)
        consents = await self._consents.get_for_customer(customer_id)
        profile["consents_full"] = [c.__dict__ for c in consents]
        profile["exported_at"] = datetime.now(timezone.utc).isoformat()
        profile["export_type"] = "LGPD_DATA_PORTABILITY"
        return profile

    async def anonymize_customer(self, customer_id: str) -> None:
        """Anonimiza dados pessoais (LGPD Art. 18, IV)."""
        await self._customers.anonymize(customer_id)
        await self._consents.revoke_all(customer_id)

    # ============================================================
    # Loyalty
    # ============================================================

    async def get_loyalty(self, customer_id: str) -> LoyaltyAccount | None:
        return await self._loyalty.get_for_customer(customer_id)

    async def earn_points(self, customer_id: str, points: int, visit: bool = False, description: str = "") -> dict:
        account = await self._loyalty.get_for_customer(customer_id)
        if account is None:
            account = LoyaltyAccount(id=str(uuid4()), tenant_id="", customer_id=customer_id)
            account = await self._loyalty.create(account)

        txn = account.earn(points, visit=visit)
        txn.description = description or "Pontos ganhos"
        await self._loyalty.update(account)
        await self._loyalty.add_transaction(txn)

        return {"points": account.points, "tier": account.tier, "added": points}

    async def redeem_points(self, customer_id: str, points: int, description: str = "") -> dict:
        account = await self._loyalty.get_for_customer(customer_id)
        if account is None:
            raise BusinessRuleError(message="Conta de fidelidade não encontrada.")
        if points > account.points:
            raise BusinessRuleError(message=f"Pontos insuficientes. Saldo: {account.points}")

        txn = account.redeem(points, description)
        await self._loyalty.update(account)
        await self._loyalty.add_transaction(txn)

        return {"points": account.points, "tier": account.tier, "redeemed": points}

    async def get_loyalty_transactions(self, customer_id: str, *, offset: int = 0, limit: int = 50) -> tuple[list, int]:
        account = await self._loyalty.get_for_customer(customer_id)
        if account is None:
            return [], 0
        txns, total = await self._loyalty.get_transactions(account.id, offset=offset, limit=limit)
        return [t.__dict__ for t in txns], total

    # ============================================================
    # Referrals
    # ============================================================

    async def create_referral_code(self, tenant_id: str, referrer_id: str) -> Referral:
        code = secrets.token_hex(4)[:8].upper()
        ref = Referral(
            id=str(uuid4()), tenant_id=tenant_id, referrer_id=referrer_id,
            referral_code=code, status=ReferralStatus.PENDING,
        )
        return await self._referrals.create(ref)

    async def get_referrals(self, customer_id: str) -> list[Referral]:
        return await self._referrals.list_for_referrer(customer_id)

    async def resolve_referral(self, code: str, referred_customer_id: str) -> Referral | None:
        ref = await self._referrals.get_by_code(code)
        if ref and ref.status == ReferralStatus.PENDING:
            ref.mark_registered(referred_customer_id)
            await self._referrals.update(ref)
        return ref

    async def reward_referral(self, code: str) -> Referral | None:
        ref = await self._referrals.get_by_code(code)
        if ref and ref.status in {ReferralStatus.REGISTERED, ReferralStatus.BOOKED}:
            ref.mark_rewarded()
            await self._referrals.update(ref)
        return ref

    # ============================================================
    # Block / Blacklist
    # ============================================================

    async def block_customer(self, customer_id: str, reason: str) -> Customer:
        c = await self.get_customer(customer_id)
        c.block(reason)
        return await self._customers.update(c)

    async def unblock_customer(self, customer_id: str) -> Customer:
        c = await self.get_customer(customer_id)
        c.unblock()
        return await self._customers.update(c)
