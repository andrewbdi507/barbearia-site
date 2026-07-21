"""Customer Module — Tests."""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.modules.customer.domain.entities import (
    Consent,
    Customer,
    CustomerPreference,
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


class TestCustomer:
    def test_create_customer(self) -> None:
        c = Customer(id="c1", tenant_id="t1", name="João Silva", phone="11999999999")
        assert c.name == "João Silva"
        assert c.status == CustomerStatus.ACTIVE
        assert c.total_visits == 0

    def test_record_visit(self) -> None:
        c = Customer(id="c1", tenant_id="t1", name="João")
        c.record_visit(amount=5000)
        assert c.total_visits == 1
        assert c.total_spent == 5000
        assert c.last_visit_at is not None

    def test_block(self) -> None:
        c = Customer(id="c1", tenant_id="t1", name="João")
        c.block("No-show recorrente")
        assert c.status == CustomerStatus.BLOCKED
        assert "BLOQUEADO" in (c.notes or "")

    def test_unblock(self) -> None:
        c = Customer(id="c1", tenant_id="t1", name="João", status=CustomerStatus.BLOCKED)
        c.unblock()
        assert c.status == CustomerStatus.ACTIVE

    def test_anonymize(self) -> None:
        c = Customer(id="c1", tenant_id="t1", name="João", email="j@t.com", phone="1199999")
        c.anonymize()
        assert c.status == CustomerStatus.ANONYMIZED
        assert c.name == "ANONYMIZED"
        assert c.email is None
        assert c.phone is None


class TestLoyalty:
    def test_earn_points(self) -> None:
        acc = LoyaltyAccount(id="l1", tenant_id="t1", customer_id="c1")
        txn = acc.earn(100, visit=True)
        assert acc.points == 100
        assert acc.visit_count == 1
        assert txn.points == 100

    def test_redeem_points(self) -> None:
        acc = LoyaltyAccount(id="l1", tenant_id="t1", customer_id="c1", points=200)
        txn = acc.redeem(50, "Corte gratuito")
        assert acc.points == 150
        assert acc.total_redeemed == 50

    def test_redeem_insufficient(self) -> None:
        acc = LoyaltyAccount(id="l1", tenant_id="t1", customer_id="c1", points=10)
        with pytest.raises(ValueError):
            acc.redeem(100)

    def test_tier_upgrade(self) -> None:
        acc = LoyaltyAccount(id="l1", tenant_id="t1", customer_id="c1", visit_count=4)
        assert acc.tier == LoyaltyTier.BRONZE
        acc.earn(10, visit=True)
        assert acc.tier == LoyaltyTier.SILVER

    def test_tier_gold(self) -> None:
        acc = LoyaltyAccount(id="l1", tenant_id="t1", customer_id="c1", visit_count=14)
        acc.earn(10, visit=True)
        assert acc.tier == LoyaltyTier.GOLD


class TestReview:
    def test_moderate_approve(self) -> None:
        r = Review(id="r1", tenant_id="t1", booking_id="b1", customer_id="c1", professional_id="p1", rating=5)
        assert not r.is_visible
        r.moderate(True)
        assert r.is_visible

    def test_respond(self) -> None:
        r = Review(id="r1", tenant_id="t1", booking_id="b1", customer_id="c1", professional_id="p1", rating=4)
        r.respond("Obrigado pela avaliação!")
        assert r.business_response == "Obrigado pela avaliação!"
        assert r.business_response_at is not None


class TestConsent:
    def test_grant(self) -> None:
        c = Consent(id="c1", tenant_id="t1", customer_id="c1", consent_type=ConsentType.MARKETING_WHATSAPP)
        assert c.is_granted

    def test_revoke(self) -> None:
        c = Consent(id="c1", tenant_id="t1", customer_id="c1")
        c.revoke()
        assert not c.is_granted
        assert c.revoked_at is not None


class TestReferral:
    def test_create(self) -> None:
        r = Referral(id="r1", tenant_id="t1", referrer_id="c1", referral_code="ABC12345")
        assert r.status == ReferralStatus.PENDING

    def test_mark_registered(self) -> None:
        r = Referral(id="r1", tenant_id="t1", referrer_id="c1", referral_code="ABC")
        r.mark_registered("c2")
        assert r.status == ReferralStatus.REGISTERED
        assert r.referred_customer_id == "c2"

    def test_mark_rewarded(self) -> None:
        r = Referral(id="r1", tenant_id="t1", referrer_id="c1", referral_code="ABC", status=ReferralStatus.BOOKED)
        r.mark_rewarded()
        assert r.status == ReferralStatus.REWARDED
        assert r.reward_granted_at is not None


class TestDTOs:
    def test_customer_create(self) -> None:
        from app.modules.customer.application.dto import CustomerCreateRequest
        req = CustomerCreateRequest(name="João", phone="11999999999", tags=["VIP"])
        assert req.name == "João"
        assert "VIP" in req.tags

    def test_review_create(self) -> None:
        from app.modules.customer.application.dto import ReviewCreateRequest
        req = ReviewCreateRequest(booking_id="b1", rating=5, tags=["Pontual", "Atendimento ótimo"])
        assert req.rating == 5

    def test_preference_update(self) -> None:
        from app.modules.customer.application.dto import PreferenceUpdateRequest
        req = PreferenceUpdateRequest(favorite_professional_id="p1", preferred_time="morning")
        assert req.preferred_time == "morning"
