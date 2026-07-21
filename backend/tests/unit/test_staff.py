"""Staff Module — Tests.

Cobertura: entities, value objects, service, DTOs.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.modules.staff.domain.entities import (
    CommissionRule,
    Invitation,
    Position,
    Specialty,
    StaffProfile,
    StaffSchedule,
    Team,
    TimeOff,
)
from app.modules.staff.domain.enums import (
    CommissionType,
    InvitationStatus,
    StaffStatus,
    TimeOffStatus,
    TimeOffType,
)


# ============================================================
# Value Objects
# ============================================================

class TestCommissionRule:
    def test_none_returns_zero(self) -> None:
        rule = CommissionRule(commission_type="none")
        assert rule.calculate(5000) == 0

    def test_percentage(self) -> None:
        rule = CommissionRule(commission_type="percentage", value=30)
        assert rule.calculate(10000) == 3000  # 30% de R$100

    def test_fixed(self) -> None:
        rule = CommissionRule(commission_type="fixed", value=1500)
        assert rule.calculate(5000) == 1500  # R$15 fixo
        assert rule.calculate(20000) == 1500  # sempre o mesmo


# ============================================================
# Entity Tests
# ============================================================

class TestStaffProfile:
    def test_new_staff_is_active(self) -> None:
        s = StaffProfile(id="s1", tenant_id="t1", user_id="u1", status=StaffStatus.ACTIVE)
        assert s.is_active

    def test_deactivate(self) -> None:
        s = StaffProfile(id="s1", tenant_id="t1", user_id="u1", status=StaffStatus.ACTIVE)
        s.deactivate()
        assert s.status == StaffStatus.INACTIVE
        assert not s.is_active

    def test_reactivate(self) -> None:
        s = StaffProfile(id="s1", tenant_id="t1", user_id="u1", status=StaffStatus.INACTIVE)
        s.activate()
        assert s.status == StaffStatus.ACTIVE

    def test_terminate(self) -> None:
        s = StaffProfile(id="s1", tenant_id="t1", user_id="u1", status=StaffStatus.ACTIVE)
        s.terminate()
        assert s.status == StaffStatus.TERMINATED
        assert s.termination_date is not None


class TestTeam:
    def test_create_team(self) -> None:
        t = Team(id="t1", tenant_id="t1", name="Equipe Manhã")
        assert t.name == "Equipe Manhã"
        assert t.member_ids == []

    def test_with_members(self) -> None:
        t = Team(id="t1", tenant_id="t1", name="Equipe A", member_ids=["s1", "s2"])
        assert len(t.member_ids) == 2


class TestTimeOff:
    def test_approve(self) -> None:
        t = TimeOff(id="to1", tenant_id="t1", staff_id="s1", time_off_type=TimeOffType.VACATION,
                    start_date=datetime.now(timezone.utc), end_date=datetime.now(timezone.utc))
        t.approve("admin1")
        assert t.status == TimeOffStatus.APPROVED
        assert t.approved_by == "admin1"

    def test_reject(self) -> None:
        t = TimeOff(id="to1", tenant_id="t1", staff_id="s1", time_off_type=TimeOffType.DAY_OFF,
                    start_date=datetime.now(timezone.utc), end_date=datetime.now(timezone.utc))
        t.reject("admin1")
        assert t.status == TimeOffStatus.REJECTED


class TestInvitation:
    def test_pending_not_expired(self) -> None:
        inv = Invitation(
            id="i1", tenant_id="t1", email="test@test.com",
            status=InvitationStatus.PENDING,
            expires_at=datetime.now(timezone.utc) + timedelta(days=3),
        )
        assert inv.is_pending

    def test_expired(self) -> None:
        inv = Invitation(
            id="i1", tenant_id="t1", email="test@test.com",
            status=InvitationStatus.PENDING,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        assert inv.is_expired
        assert not inv.is_pending


# ============================================================
# Service Tests
# ============================================================

class TestStaffService:
    @pytest.mark.asyncio
    async def test_create_staff_success(self) -> None:
        from app.modules.staff.application.staff_service import StaffService

        staff_repo = MagicMock()
        staff_repo.get_by_user_id.return_value = None
        created = StaffProfile(
            id="s_new", tenant_id="t1", user_id="u1",
            professional_name="João Barbeiro", status=StaffStatus.ACTIVE,
        )
        staff_repo.create.return_value = created
        staff_repo.count_active.return_value = 3

        tenant_repo = MagicMock()
        tenant_repo.get_by_id.return_value = None  # no plan check

        position_repo = MagicMock()
        specialty_repo = MagicMock()
        team_repo = MagicMock()
        schedule_repo = MagicMock()
        timeoff_repo = MagicMock()
        invitation_repo = MagicMock()
        audit_repo = MagicMock()

        svc = StaffService(
            staff_repo, position_repo, specialty_repo, team_repo,
            schedule_repo, timeoff_repo, invitation_repo, audit_repo, tenant_repo,
        )

        result = await svc.create_staff(
            "t1", "actor1", user_id="u1", professional_name="João Barbeiro",
        )
        assert result.professional_name == "João Barbeiro"
        assert result.status == "active"

    @pytest.mark.asyncio
    async def test_create_staff_duplicate(self) -> None:
        from app.modules.staff.application.staff_service import StaffService
        from app.core.exceptions import BusinessRuleError

        staff_repo = MagicMock()
        staff_repo.get_by_user_id.return_value = StaffProfile(
            id="existing", tenant_id="t1", user_id="u1", status="active",
        )
        staff_repo.count_active.return_value = 1

        svc = StaffService(
            staff_repo, MagicMock(), MagicMock(), MagicMock(),
            MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(),
        )

        with pytest.raises(BusinessRuleError):
            await svc.create_staff("t1", "actor1", user_id="u1")

    @pytest.mark.asyncio
    async def test_approve_time_off(self) -> None:
        from app.modules.staff.application.staff_service import StaffService

        timeoff_repo = MagicMock()
        to = TimeOff(
            id="to1", tenant_id="t1", staff_id="s1",
            time_off_type=TimeOffType.VACATION,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=10),
        )
        timeoff_repo.get_by_id.return_value = to

        svc = StaffService(
            MagicMock(), MagicMock(), MagicMock(), MagicMock(),
            MagicMock(), timeoff_repo, MagicMock(), MagicMock(), MagicMock(),
        )

        await svc.approve_time_off("to1", "admin1")
        assert to.status == TimeOffStatus.APPROVED


# ============================================================
# DTO Tests
# ============================================================

class TestDTOs:
    def test_position_create(self) -> None:
        from app.modules.staff.application.dto import PositionCreateRequest
        req = PositionCreateRequest(name="Gerente", description="Gerente da unidade")
        assert req.name == "Gerente"

    def test_schedule_day_invalid(self) -> None:
        from app.modules.staff.application.dto import ScheduleDayRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            ScheduleDayRequest(day_of_week=7)  # inválido

    def test_staff_create_valid(self) -> None:
        from app.modules.staff.application.dto import StaffCreateRequest
        req = StaffCreateRequest(
            user_id="u1", professional_name="João",
            commission_type="percentage", commission_value=30,
        )
        assert req.commission_type == "percentage"

    def test_commission_invalid_type(self) -> None:
        from app.modules.staff.application.dto import StaffCreateRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            StaffCreateRequest(user_id="u1", commission_type="invalid")

    def test_team_create(self) -> None:
        from app.modules.staff.application.dto import TeamCreateRequest
        req = TeamCreateRequest(name="Equipe Premium", member_ids=["s1", "s2"])
        assert len(req.member_ids) == 2
