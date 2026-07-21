"""Marketing Module — Tests."""

import pytest
from datetime import date, datetime, timedelta, timezone

from app.modules.marketing.domain.entities import (
    Coupon, Promotion, Campaign, AutomationRule, GiftCard,
)
from app.modules.marketing.application.marketing_service import MarketingService


class TestCoupon:
    def test_fixed_discount(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="DESC10", coupon_type="fixed", value=1000)
        assert c.calculate_discount(5000) == 1000

    def test_percentage_discount(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="DESC20", coupon_type="percentage", value=20)
        assert c.calculate_discount(5000) == 1000

    def test_discount_cannot_exceed_amount(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="DESC100", coupon_type="fixed", value=10000)
        assert c.calculate_discount(5000) == 5000

    def test_valid_coupon(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="OK", expires_at=datetime.now(timezone.utc) + timedelta(days=30))
        assert c.is_valid

    def test_expired_coupon(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="EXPIRED", expires_at=datetime.now(timezone.utc) - timedelta(days=1))
        assert not c.is_valid

    def test_exhausted_coupon(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="FULL", max_uses=10, current_uses=10)
        assert not c.is_valid

    def test_apply_increments_uses(self) -> None:
        c = Coupon(id="c1", tenant_id="t1", code="INC")
        c.apply()
        assert c.current_uses == 1


class TestPromotion:
    def test_valid_now(self) -> None:
        p = Promotion(id="p1", tenant_id="t1", name="Promo Ativa",
                      starts_at=datetime.now(timezone.utc) - timedelta(days=1),
                      ends_at=datetime.now(timezone.utc) + timedelta(days=1))
        assert p.is_valid_now

    def test_expired(self) -> None:
        p = Promotion(id="p1", tenant_id="t1", name="Expirada",
                      ends_at=datetime.now(timezone.utc) - timedelta(days=1))
        assert not p.is_valid_now

    def test_inactive(self) -> None:
        p = Promotion(id="p1", tenant_id="t1", name="Inativa", is_active=False)
        assert not p.is_valid_now


class TestGiftCard:
    def test_redeem_partial(self) -> None:
        gc = GiftCard(id="g1", tenant_id="t1", code="GC123", initial_amount=10000, current_balance=10000)
        result = gc.redeem(3000)
        assert result
        assert gc.current_balance == 7000
        assert not gc.is_redeemed

    def test_redeem_full(self) -> None:
        gc = GiftCard(id="g1", tenant_id="t1", code="GC456", initial_amount=5000, current_balance=5000)
        result = gc.redeem(5000)
        assert result
        assert gc.current_balance == 0
        assert gc.is_redeemed

    def test_redeem_insufficient(self) -> None:
        gc = GiftCard(id="g1", tenant_id="t1", code="GC789", initial_amount=1000, current_balance=1000)
        result = gc.redeem(5000)
        assert not result
        assert gc.current_balance == 1000


class TestRuleEngine:
    def test_evaluate_conditions_equals(self) -> None:
        result = MarketingService._evaluate_conditions(
            [{"field": "status", "operator": "equals", "value": "cancelled"}],
            {"status": "cancelled", "customer_id": "c1"},
        )
        assert result

    def test_evaluate_conditions_fails(self) -> None:
        result = MarketingService._evaluate_conditions(
            [{"field": "status", "operator": "equals", "value": "completed"}],
            {"status": "cancelled"},
        )
        assert not result

    def test_evaluate_conditions_greater_than(self) -> None:
        result = MarketingService._evaluate_conditions(
            [{"field": "amount", "operator": "greater_than", "value": 5000}],
            {"amount": 10000},
        )
        assert result

    def test_evaluate_empty_conditions(self) -> None:
        result = MarketingService._evaluate_conditions([], {"any": "data"})
        assert result  # Sem condições = sempre true

    def test_evaluate_contains(self) -> None:
        result = MarketingService._evaluate_conditions(
            [{"field": "tags", "operator": "contains", "value": "VIP"}],
            {"tags": "VIP, Premium"},
        )
        assert result


class TestSmartSegments:
    def test_vip_segment(self) -> None:
        segments = MarketingService.calculate_segment_type({"total_spent": 150000, "total_visits": 10})
        assert "vip" in segments

    def test_lapsed_segment(self) -> None:
        old_date = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()
        segments = MarketingService.calculate_segment_type({"last_visit_at": old_date, "total_spent": 0, "total_visits": 1})
        assert "lapsed_30d" in segments

    def test_new_segment(self) -> None:
        recent = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
        segments = MarketingService.calculate_segment_type({"created_at": recent, "total_spent": 0, "total_visits": 0})
        assert "new" in segments

    def test_birthday_segment(self) -> None:
        today_month = date.today().month
        bday = date(1990, today_month, 15)
        segments = MarketingService.calculate_segment_type({"birth_date": bday, "total_spent": 0, "total_visits": 0})
        assert "birthday" in segments

    def test_empty_customer(self) -> None:
        segments = MarketingService.calculate_segment_type({})
        assert segments == []
