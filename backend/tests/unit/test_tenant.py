"""Tenant Module — Tests.

Cobertura: entities, value objects, services, DTOs, middleware.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.modules.tenant.domain.entities import (
    BusinessHours,
    Domain,
    FeatureFlag,
    Plan,
    Subscription,
    Tenant,
    TenantBranding,
    TenantSettings,
)
from app.modules.tenant.domain.enums import (
    BillingCycle,
    DomainType,
    SubscriptionStatus,
    TenantStatus,
)
from app.modules.tenant.domain.value_objects import BrandingColors, PlanLimits, Subdomain


# ============================================================
# Value Objects Tests
# ============================================================

class TestSubdomain:
    def test_valid_subdomain(self) -> None:
        s = Subdomain("studio27")
        assert s.value == "studio27"

    def test_valid_with_hyphen(self) -> None:
        s = Subdomain("studio-27")
        assert s.value == "studio-27"

    def test_invalid_short(self) -> None:
        with pytest.raises(ValueError):
            Subdomain("ab")

    def test_invalid_uppercase(self) -> None:
        with pytest.raises(ValueError):
            Subdomain("Studio27")

    def test_invalid_special_chars(self) -> None:
        with pytest.raises(ValueError):
            Subdomain("studio_27")


class TestPlanLimits:
    def test_default_limits(self) -> None:
        limits = PlanLimits()
        assert limits.max_professionals == 5
        assert limits.max_customers == 500

    def test_unlimited_resource(self) -> None:
        limits = PlanLimits(max_professionals=0)
        assert limits.max_professionals == 0  # 0 = unlimited

    def test_from_dict(self) -> None:
        data = {"max_professionals": 10, "custom_domain": True, "max_customers": 1000}
        limits = PlanLimits.from_dict(data)
        assert limits.max_professionals == 10
        assert limits.custom_domain is True
        assert limits.max_customers == 1000

    def test_to_dict(self) -> None:
        limits = PlanLimits(max_professionals=3)
        d = limits.to_dict()
        assert d["max_professionals"] == 3
        assert "max_customers" in d


class TestBrandingColors:
    def test_valid_colors(self) -> None:
        c = BrandingColors(primary="#ff0000", secondary="#00ff00")
        assert c.primary == "#ff0000"

    def test_invalid_hex(self) -> None:
        with pytest.raises(ValueError):
            BrandingColors(primary="red")

    def test_defaults(self) -> None:
        c = BrandingColors()
        assert c.primary == "#1a1a2e"


# ============================================================
# Entity Tests
# ============================================================

class TestTenantLifecycle:
    def test_new_tenant_is_trial(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.TRIAL,
        )
        assert t.is_trial
        assert not t.is_active
        assert t.can_access()

    def test_activate_from_trial(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.TRIAL,
        )
        t.activate()
        assert t.status == TenantStatus.ACTIVE
        assert t.is_active

    def test_suspend_active(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.ACTIVE,
        )
        t.suspend("Violação de termos")
        assert t.status == TenantStatus.SUSPENDED
        assert t.suspended_reason == "Violação de termos"
        assert not t.can_access()

    def test_cancel_tenant(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.ACTIVE,
        )
        t.cancel()
        assert t.status == TenantStatus.CANCELLED
        assert not t.can_access()

    def test_reactivate_suspended(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.SUSPENDED,
        )
        t.activate()
        assert t.status == TenantStatus.ACTIVE

    def test_cannot_activate_deleted(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.DELETED,
        )
        with pytest.raises(ValueError):
            t.activate()

    def test_mark_past_due(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.ACTIVE,
        )
        t.mark_past_due()
        assert t.status == TenantStatus.PAST_DUE

    def test_start_trial(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.TRIAL,
        )
        t.start_trial(days=14)
        assert t.trial_ends_at is not None

    def test_trial_days_remaining(self) -> None:
        t = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.TRIAL,
            trial_ends_at=datetime.now(timezone.utc) + timedelta(days=5),
        )
        assert t.trial_days_remaining == 5


class TestPlan:
    def test_exceeds_limit_true(self) -> None:
        plan = Plan(
            id="p1", name="Starter", slug="starter", tier="starter",
            limits=PlanLimits(max_professionals=5),
        )
        assert plan.exceeds_limit("max_professionals", 5) is True

    def test_exceeds_limit_false(self) -> None:
        plan = Plan(
            id="p1", name="Starter", slug="starter", tier="starter",
            limits=PlanLimits(max_professionals=5),
        )
        assert plan.exceeds_limit("max_professionals", 3) is False

    def test_unlimited_never_exceeds(self) -> None:
        plan = Plan(
            id="p1", name="Enterprise", slug="enterprise", tier="enterprise",
            limits=PlanLimits(max_professionals=0),
        )
        assert plan.exceeds_limit("max_professionals", 999) is False

    def test_unknown_resource(self) -> None:
        plan = Plan(
            id="p1", name="Starter", slug="starter", tier="starter",
            limits=PlanLimits(),
        )
        assert plan.exceeds_limit("nonexistent", 100) is False

    def test_has_feature(self) -> None:
        plan = Plan(
            id="p1", name="Pro", slug="pro", tier="pro",
            features=["whatsapp_integration", "custom_branding"],
        )
        assert plan.has_feature("whatsapp_integration") is True
        assert plan.has_feature("api_access") is False


class TestSubscription:
    def test_is_active_when_trialing(self) -> None:
        sub = Subscription(
            id="s1", tenant_id="t1", plan_id="p1",
            status=SubscriptionStatus.TRIALING,
        )
        assert sub.is_active

    def test_is_active_when_active(self) -> None:
        sub = Subscription(
            id="s1", tenant_id="t1", plan_id="p1",
            status=SubscriptionStatus.ACTIVE,
        )
        assert sub.is_active

    def test_not_active_when_cancelled(self) -> None:
        sub = Subscription(
            id="s1", tenant_id="t1", plan_id="p1",
            status=SubscriptionStatus.CANCELLED,
        )
        assert not sub.is_active

    def test_trial_days_remaining(self) -> None:
        sub = Subscription(
            id="s1", tenant_id="t1", plan_id="p1",
            status=SubscriptionStatus.TRIALING,
            trial_ends_at=datetime.now(timezone.utc) + timedelta(days=3),
        )
        assert sub.trial_days_remaining == 3


class TestFeatureFlag:
    def test_enabled_for_all(self) -> None:
        ff = FeatureFlag(id="f1", name="new_booking_ui", enabled_for_all=True)
        assert ff.is_enabled_for("t_any") is True

    def test_enabled_for_specific_tenant(self) -> None:
        ff = FeatureFlag(
            id="f1", name="beta", enabled_tenant_ids=["t_beta", "t_test"],
        )
        assert ff.is_enabled_for("t_beta") is True
        assert ff.is_enabled_for("t_normal") is False

    def test_percentage_based_deterministic(self) -> None:
        ff = FeatureFlag(id="f1", name="rollout", enabled_percentage=50)
        # Same tenant always returns same result (deterministic hash)
        result1 = ff.is_enabled_for("t_consistent")
        result2 = ff.is_enabled_for("t_consistent")
        assert result1 == result2

    def test_disabled_by_default(self) -> None:
        ff = FeatureFlag(id="f1", name="off")
        assert ff.is_enabled_for("t_any") is False


# ============================================================
# TenantService Tests
# ============================================================

class TestTenantService:
    @pytest.mark.asyncio
    async def test_create_tenant_success(self) -> None:
        from app.modules.tenant.application.tenant_service import TenantService
        from app.modules.tenant.infrastructure.cache import TenantRedisCache

        # Mocks
        tenant_repo = MagicMock()
        tenant_repo.subdomain_exists.return_value = False
        created_tenant = Tenant(
            id="t_new", subdomain=Subdomain("nova"), name="Nova Barbearia",
            status=TenantStatus.TRIAL, plan_id="p_starter",
            settings=TenantSettings(id="s1", tenant_id="t_new"),
            branding=TenantBranding(id="b1", tenant_id="t_new"),
        )
        tenant_repo.create.return_value = created_tenant

        plan_repo = MagicMock()
        plan_repo.get_by_slug.return_value = Plan(
            id="p_starter", name="Starter", slug="starter", tier="starter",
        )

        sub_repo = MagicMock()
        domain_repo = MagicMock()
        bh_repo = MagicMock()
        settings_repo = MagicMock()
        branding_repo = MagicMock()
        cache = MagicMock(spec=TenantRedisCache)

        service = TenantService(
            tenant_repo=tenant_repo,
            plan_repo=plan_repo,
            sub_repo=sub_repo,
            settings_repo=settings_repo,
            branding_repo=branding_repo,
            bh_repo=bh_repo,
            domain_repo=domain_repo,
            cache=cache,
        )

        result = await service.create_tenant(
            subdomain="nova",
            name="Nova Barbearia",
        )

        assert result.subdomain.value == "nova"
        assert result.status == TenantStatus.TRIAL
        tenant_repo.subdomain_exists.assert_called_once_with("nova")
        sub_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_tenant_subdomain_taken(self) -> None:
        from app.modules.tenant.application.tenant_service import TenantService
        from app.core.exceptions import DomainAlreadyTakenError

        tenant_repo = MagicMock()
        tenant_repo.subdomain_exists.return_value = True

        plan_repo = MagicMock()
        plan_repo.get_by_slug.return_value = Plan(
            id="p1", name="Starter", slug="starter", tier="starter",
        )

        service = TenantService(
            tenant_repo=tenant_repo,
            plan_repo=plan_repo,
            sub_repo=MagicMock(),
            settings_repo=MagicMock(),
            branding_repo=MagicMock(),
            bh_repo=MagicMock(),
            domain_repo=MagicMock(),
            cache=MagicMock(),
        )

        with pytest.raises(DomainAlreadyTakenError):
            await service.create_tenant(subdomain="taken", name="Test")

    @pytest.mark.asyncio
    async def test_validate_limits_exceeded(self) -> None:
        from app.modules.tenant.application.tenant_service import TenantService
        from app.core.exceptions import PlanLimitExceededError

        tenant_repo = MagicMock()
        tenant_repo.get_by_id.return_value = Tenant(
            id="t1", subdomain=Subdomain("test"), name="Test",
            status=TenantStatus.ACTIVE, plan_id="p_limited",
        )

        plan_repo = MagicMock()
        plan_repo.get_by_id.return_value = Plan(
            id="p_limited", name="Starter", slug="starter", tier="starter",
            limits=PlanLimits(max_professionals=5),
        )

        service = TenantService(
            tenant_repo=tenant_repo,
            plan_repo=plan_repo,
            sub_repo=MagicMock(),
            settings_repo=MagicMock(),
            branding_repo=MagicMock(),
            bh_repo=MagicMock(),
            domain_repo=MagicMock(),
            cache=MagicMock(),
        )

        with pytest.raises(PlanLimitExceededError):
            await service.validate_limits("t1", "max_professionals", 6)

    @pytest.mark.asyncio
    async def test_check_tenant_access_suspended(self) -> None:
        from app.modules.tenant.application.tenant_service import TenantService
        from app.core.exceptions import TenantSuspendedError

        tenant_repo = MagicMock()
        tenant_repo.get_by_id.return_value = Tenant(
            id="t1", subdomain=Subdomain("bad"), name="Bad Tenant",
            status=TenantStatus.SUSPENDED, suspended_reason="Fraude",
        )

        service = TenantService(
            tenant_repo=tenant_repo,
            plan_repo=MagicMock(),
            sub_repo=MagicMock(),
            settings_repo=MagicMock(),
            branding_repo=MagicMock(),
            bh_repo=MagicMock(),
            domain_repo=MagicMock(),
            cache=MagicMock(),
        )

        with pytest.raises(TenantSuspendedError):
            await service.check_tenant_access("t1")


# ============================================================
# DTO Validation Tests
# ============================================================

class TestDTOs:
    def test_tenant_create_valid(self) -> None:
        from app.modules.tenant.application.dto import TenantCreateRequest
        req = TenantCreateRequest(
            subdomain="studio27",
            name="Studio 27",
            owner_email="dono@studio27.com",
            owner_name="João",
            owner_password="SenhaSegura123",
        )
        assert req.subdomain == "studio27"
        assert req.name == "Studio 27"

    def test_tenant_create_invalid_subdomain(self) -> None:
        from app.modules.tenant.application.dto import TenantCreateRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            TenantCreateRequest(subdomain="AB", name="Test")

    def test_branding_update_valid(self) -> None:
        from app.modules.tenant.application.dto import TenantBrandingRequest
        req = TenantBrandingRequest(
            primary_color="#ff5500",
            secondary_color="#0066ff",
        )
        assert req.primary_color == "#ff5500"

    def test_branding_invalid_color(self) -> None:
        from app.modules.tenant.application.dto import TenantBrandingRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            TenantBrandingRequest(primary_color="red")

    def test_business_hours_batch(self) -> None:
        from app.modules.tenant.application.dto import BusinessHoursBatchRequest, BusinessHoursRequest
        req = BusinessHoursBatchRequest(
            hours=[BusinessHoursRequest(day_of_week=i) for i in range(7)]
        )
        assert len(req.hours) == 7


# ============================================================
# Middleware Tests
# ============================================================

class TestTenantMiddleware:
    def test_extract_subdomain(self) -> None:
        from app.modules.tenant.presentation.middleware import TenantMiddleware
        assert TenantMiddleware._extract_subdomain("studio27.barbeariaos.com.br") == "studio27"
        assert TenantMiddleware._extract_subdomain("localhost") is None
        assert TenantMiddleware._extract_subdomain("api.barbeariaos.com.br") == "api"

    def test_public_paths_recognized(self) -> None:
        from app.modules.tenant.presentation.middleware import TenantMiddleware
        assert "/api/v1/auth/login" in TenantMiddleware.PUBLIC_PATHS
        assert "/api/v1/health" in TenantMiddleware.PUBLIC_PATHS
