"""Staff Module — Repository Implementation."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select, update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.staff.domain.entities import (
    Invitation,
    Position,
    Specialty,
    StaffAuditLog,
    StaffProfile,
    StaffSchedule,
    Team,
    TimeOff,
)
from app.modules.staff.domain.interfaces import (
    IInvitationRepository,
    IPositionRepository,
    IScheduleRepository,
    ISpecialtyRepository,
    IStaffAuditRepository,
    IStaffRepository,
    ITeamRepository,
    ITimeOffRepository,
)
from app.modules.staff.infrastructure.models.staff_models import (
    InvitationModel,
    PositionModel,
    SpecialtyModel,
    StaffAuditLogModel,
    StaffProfileModel,
    StaffScheduleModel,
    TeamMemberModel,
    TeamModel,
    TimeOffModel,
)


# ============================================================
# Mappers: Model → Entity
# ============================================================

def _position_to_entity(m: PositionModel) -> Position:
    return Position(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        description=m.description or "", is_system=m.is_system,
        sort_order=m.sort_order, created_at=m.created_at, updated_at=m.updated_at,
    )


def _specialty_to_entity(m: SpecialtyModel) -> Specialty:
    return Specialty(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        description=m.description or "", color_tag=m.color_tag,
        is_active=m.is_active, sort_order=m.sort_order, created_at=m.created_at,
    )


def _staff_to_entity(m: StaffProfileModel) -> StaffProfile:
    return StaffProfile(
        id=m.id, tenant_id=m.tenant_id or "", user_id=m.user_id,
        position_id=m.position_id, professional_name=m.professional_name,
        photo_url=m.photo_url, bio=m.bio,
        specialties=m.specialties or [], experience_years=m.experience_years,
        status=m.status, is_visible_on_site=m.is_visible_on_site,
        commission_type=m.commission_type, commission_value=m.commission_value,
        hire_date=m.hire_date, termination_date=m.termination_date,
        metadata=m.metadata or {}, created_at=m.created_at, updated_at=m.updated_at,
    )


def _team_to_entity(m: TeamModel) -> Team:
    member_ids = [tm.staff_id for tm in (m.members or [])]
    return Team(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        description=m.description or "", color_tag=m.color_tag,
        leader_id=m.leader_id, is_active=m.is_active, sort_order=m.sort_order,
        member_ids=member_ids, metadata=m.metadata or {},
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _schedule_to_entity(m: StaffScheduleModel) -> StaffSchedule:
    return StaffSchedule(
        id=m.id, tenant_id=m.tenant_id or "", staff_id=m.staff_id,
        day_of_week=m.day_of_week, is_working=m.is_working,
        start_time=m.start_time, end_time=m.end_time,
        lunch_start=m.lunch_start, lunch_end=m.lunch_end,
        slot_duration_minutes=m.slot_duration_minutes,
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _timeoff_to_entity(m: TimeOffModel) -> TimeOff:
    return TimeOff(
        id=m.id, tenant_id=m.tenant_id or "", staff_id=m.staff_id,
        time_off_type=m.time_off_type, status=m.status,
        start_date=m.start_date, end_date=m.end_date,
        start_time=m.start_time, end_time=m.end_time,
        reason=m.reason or "", is_full_day=m.is_full_day,
        approved_by=m.approved_by, approved_at=m.approved_at,
        created_at=m.created_at,
    )


def _invitation_to_entity(m: InvitationModel) -> Invitation:
    return Invitation(
        id=m.id, tenant_id=m.tenant_id or "", email=m.email,
        position_id=m.position_id, invited_by=m.invited_by,
        token_hash=m.token_hash, status=m.status,
        expires_at=m.expires_at, accepted_at=m.accepted_at,
        declined_at=m.declined_at, message=m.message or "",
        created_at=m.created_at,
    )


def _audit_to_entity(m: StaffAuditLogModel) -> StaffAuditLog:
    return StaffAuditLog(
        id=m.id, tenant_id=m.tenant_id or "", actor_id=m.actor_id,
        target_id=m.target_id, action=m.action, changes=m.changes or {},
        ip_address=m.ip_address, created_at=m.created_at,
    )


# ============================================================
# StaffRepository
# ============================================================

class StaffRepository(IStaffRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, staff_id: str) -> StaffProfile | None:
        r = await self._s.execute(
            select(StaffProfileModel)
            .where(StaffProfileModel.id == staff_id)
            .options(selectinload(StaffProfileModel.position))
        )
        m = r.scalar_one_or_none()
        return _staff_to_entity(m) if m else None

    async def get_by_user_id(self, user_id: str) -> StaffProfile | None:
        r = await self._s.execute(
            select(StaffProfileModel)
            .where(StaffProfileModel.user_id == user_id)
            .options(selectinload(StaffProfileModel.position))
        )
        m = r.scalar_one_or_none()
        return _staff_to_entity(m) if m else None

    async def list_by_tenant(
        self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[StaffProfile], int]:
        base = select(StaffProfileModel).where(StaffProfileModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(StaffProfileModel).where(
            StaffProfileModel.tenant_id == tenant_id
        )
        if status:
            base = base.where(StaffProfileModel.status == status)
            count_q = count_q.where(StaffProfileModel.status == status)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(
            base.order_by(StaffProfileModel.professional_name)
            .offset(offset).limit(limit)
            .options(selectinload(StaffProfileModel.position))
        )
        return [_staff_to_entity(m) for m in r.scalars().all()], total

    async def list_by_team(self, team_id: str) -> list[StaffProfile]:
        r = await self._s.execute(
            select(StaffProfileModel)
            .join(TeamMemberModel, TeamMemberModel.staff_id == StaffProfileModel.id)
            .where(TeamMemberModel.team_id == team_id)
            .where(StaffProfileModel.status == "active")
            .options(selectinload(StaffProfileModel.position))
        )
        return [_staff_to_entity(m) for m in r.scalars().all()]

    async def create(self, staff: StaffProfile) -> StaffProfile:
        m = StaffProfileModel(
            id=staff.id, tenant_id=staff.tenant_id, user_id=staff.user_id,
            position_id=staff.position_id, professional_name=staff.professional_name,
            photo_url=staff.photo_url, bio=staff.bio,
            specialties=staff.specialties, experience_years=staff.experience_years,
            status=staff.status, is_visible_on_site=staff.is_visible_on_site,
            commission_type=staff.commission_type, commission_value=staff.commission_value,
            hire_date=staff.hire_date, metadata=staff.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return _staff_to_entity(m)

    async def update(self, staff: StaffProfile) -> StaffProfile:
        m = await self._s.get(StaffProfileModel, staff.id)
        if not m:
            raise ValueError(f"Staff {staff.id} not found")
        for f in ("professional_name", "photo_url", "bio", "specialties",
                   "experience_years", "is_visible_on_site", "commission_type",
                   "commission_value", "position_id", "metadata"):
            setattr(m, f, getattr(staff, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _staff_to_entity(m)

    async def update_status(self, staff_id: str, status: str) -> None:
        vals: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if status == "terminated":
            vals["termination_date"] = datetime.now(timezone.utc)
        elif status == "active":
            vals["termination_date"] = None
        await self._s.execute(
            update(StaffProfileModel).where(StaffProfileModel.id == staff_id).values(**vals)
        )

    async def count_active(self, tenant_id: str) -> int:
        r = await self._s.execute(
            select(func.count()).select_from(StaffProfileModel).where(
                StaffProfileModel.tenant_id == tenant_id,
                StaffProfileModel.status == "active",
            )
        )
        return (r.scalar() or 0)


# ============================================================
# PositionRepository
# ============================================================

class PositionRepository(IPositionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, position_id: str) -> Position | None:
        r = await self._s.execute(select(PositionModel).where(PositionModel.id == position_id))
        m = r.scalar_one_or_none()
        return _position_to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str) -> list[Position]:
        r = await self._s.execute(
            select(PositionModel)
            .where(PositionModel.tenant_id == tenant_id)
            .order_by(PositionModel.sort_order)
        )
        return [_position_to_entity(m) for m in r.scalars().all()]

    async def create(self, position: Position) -> Position:
        m = PositionModel(
            id=position.id, tenant_id=position.tenant_id, name=position.name,
            description=position.description, is_system=position.is_system,
            sort_order=position.sort_order,
        )
        self._s.add(m)
        await self._s.flush()
        return _position_to_entity(m)

    async def update(self, position: Position) -> Position:
        m = await self._s.get(PositionModel, position.id)
        if not m:
            raise ValueError(f"Position {position.id} not found")
        m.name = position.name
        m.description = position.description
        m.sort_order = position.sort_order
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _position_to_entity(m)

    async def delete(self, position_id: str) -> None:
        m = await self._s.get(PositionModel, position_id)
        if m and m.is_system:
            raise ValueError("Não é possível deletar cargo de sistema.")
        await self._s.execute(sa_delete(PositionModel).where(PositionModel.id == position_id))


# ============================================================
# SpecialtyRepository
# ============================================================

class SpecialtyRepository(ISpecialtyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def list_by_tenant(self, tenant_id: str) -> list[Specialty]:
        r = await self._s.execute(
            select(SpecialtyModel)
            .where(SpecialtyModel.tenant_id == tenant_id)
            .order_by(SpecialtyModel.sort_order)
        )
        return [_specialty_to_entity(m) for m in r.scalars().all()]

    async def create(self, specialty: Specialty) -> Specialty:
        m = SpecialtyModel(
            id=specialty.id, tenant_id=specialty.tenant_id, name=specialty.name,
            description=specialty.description, color_tag=specialty.color_tag,
            sort_order=specialty.sort_order,
        )
        self._s.add(m)
        await self._s.flush()
        return _specialty_to_entity(m)

    async def update(self, specialty: Specialty) -> Specialty:
        m = await self._s.get(SpecialtyModel, specialty.id)
        if not m:
            raise ValueError(f"Specialty {specialty.id} not found")
        for f in ("name", "description", "color_tag", "is_active", "sort_order"):
            setattr(m, f, getattr(specialty, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _specialty_to_entity(m)

    async def delete(self, specialty_id: str) -> None:
        await self._s.execute(sa_delete(SpecialtyModel).where(SpecialtyModel.id == specialty_id))


# ============================================================
# TeamRepository
# ============================================================

class TeamRepository(ITeamRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, team_id: str) -> Team | None:
        r = await self._s.execute(
            select(TeamModel)
            .where(TeamModel.id == team_id)
            .options(selectinload(TeamModel.members))
        )
        m = r.scalar_one_or_none()
        return _team_to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str) -> list[Team]:
        r = await self._s.execute(
            select(TeamModel)
            .where(TeamModel.tenant_id == tenant_id)
            .options(selectinload(TeamModel.members))
            .order_by(TeamModel.sort_order)
        )
        return [_team_to_entity(m) for m in r.scalars().all()]

    async def create(self, team: Team) -> Team:
        m = TeamModel(
            id=team.id, tenant_id=team.tenant_id, name=team.name,
            description=team.description, color_tag=team.color_tag,
            leader_id=team.leader_id, sort_order=team.sort_order, metadata=team.metadata,
        )
        self._s.add(m)
        if team.member_ids:
            for sid in team.member_ids:
                self._s.add(TeamMemberModel(team_id=team.id, staff_id=sid))
        await self._s.flush()
        return _team_to_entity(m)

    async def update(self, team: Team) -> Team:
        m = await self._s.get(TeamModel, team.id)
        if not m:
            raise ValueError(f"Team {team.id} not found")
        for f in ("name", "description", "color_tag", "leader_id", "is_active", "sort_order", "metadata"):
            setattr(m, f, getattr(team, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()

        # Sync members
        await self._s.execute(
            sa_delete(TeamMemberModel).where(TeamMemberModel.team_id == team.id)
        )
        for sid in team.member_ids:
            self._s.add(TeamMemberModel(team_id=team.id, staff_id=sid))
        await self._s.flush()
        return await self.get_by_id(team.id)  # type: ignore[return-value]

    async def delete(self, team_id: str) -> None:
        await self._s.execute(sa_delete(TeamMemberModel).where(TeamMemberModel.team_id == team_id))
        await self._s.execute(sa_delete(TeamModel).where(TeamModel.id == team_id))

    async def add_member(self, team_id: str, staff_id: str) -> None:
        exists = await self._s.execute(
            select(TeamMemberModel).where(
                TeamMemberModel.team_id == team_id, TeamMemberModel.staff_id == staff_id
            )
        )
        if not exists.scalar_one_or_none():
            self._s.add(TeamMemberModel(team_id=team_id, staff_id=staff_id))
            await self._s.flush()

    async def remove_member(self, team_id: str, staff_id: str) -> None:
        await self._s.execute(
            sa_delete(TeamMemberModel).where(
                TeamMemberModel.team_id == team_id, TeamMemberModel.staff_id == staff_id
            )
        )

    async def get_member_ids(self, team_id: str) -> list[str]:
        r = await self._s.execute(
            select(TeamMemberModel.staff_id).where(TeamMemberModel.team_id == team_id)
        )
        return [row[0] for row in r.all()]


# ============================================================
# ScheduleRepository
# ============================================================

class ScheduleRepository(IScheduleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_staff(self, staff_id: str) -> list[StaffSchedule]:
        r = await self._s.execute(
            select(StaffScheduleModel)
            .where(StaffScheduleModel.staff_id == staff_id)
            .order_by(StaffScheduleModel.day_of_week)
        )
        return [_schedule_to_entity(m) for m in r.scalars().all()]

    async def upsert_batch(
        self, staff_id: str, schedules: list[StaffSchedule]
    ) -> list[StaffSchedule]:
        await self._s.execute(
            sa_delete(StaffScheduleModel).where(StaffScheduleModel.staff_id == staff_id)
        )
        models = [
            StaffScheduleModel(
                id=s.id, tenant_id=s.tenant_id, staff_id=staff_id,
                day_of_week=s.day_of_week, is_working=s.is_working,
                start_time=s.start_time, end_time=s.end_time,
                lunch_start=s.lunch_start, lunch_end=s.lunch_end,
                slot_duration_minutes=s.slot_duration_minutes,
            )
            for s in schedules
        ]
        self._s.add_all(models)
        await self._s.flush()
        return [_schedule_to_entity(m) for m in models]


# ============================================================
# TimeOffRepository
# ============================================================

class TimeOffRepository(ITimeOffRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, time_off_id: str) -> TimeOff | None:
        r = await self._s.execute(select(TimeOffModel).where(TimeOffModel.id == time_off_id))
        m = r.scalar_one_or_none()
        return _timeoff_to_entity(m) if m else None

    async def list_for_staff(
        self, staff_id: str, *, status: str | None = None
    ) -> list[TimeOff]:
        stmt = select(TimeOffModel).where(TimeOffModel.staff_id == staff_id)
        if status:
            stmt = stmt.where(TimeOffModel.status == status)
        r = await self._s.execute(stmt.order_by(TimeOffModel.start_date.desc()))
        return [_timeoff_to_entity(m) for m in r.scalars().all()]

    async def list_for_tenant(
        self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[TimeOff], int]:
        base = select(TimeOffModel).where(TimeOffModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(TimeOffModel).where(
            TimeOffModel.tenant_id == tenant_id
        )
        if status:
            base = base.where(TimeOffModel.status == status)
            count_q = count_q.where(TimeOffModel.status == status)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(
            base.order_by(TimeOffModel.start_date.desc()).offset(offset).limit(limit)
        )
        return [_timeoff_to_entity(m) for m in r.scalars().all()], total

    async def create(self, time_off: TimeOff) -> TimeOff:
        m = TimeOffModel(
            id=time_off.id, tenant_id=time_off.tenant_id, staff_id=time_off.staff_id,
            time_off_type=time_off.time_off_type, status=time_off.status,
            start_date=time_off.start_date, end_date=time_off.end_date,
            start_time=time_off.start_time, end_time=time_off.end_time,
            reason=time_off.reason, is_full_day=time_off.is_full_day,
        )
        self._s.add(m)
        await self._s.flush()
        return _timeoff_to_entity(m)

    async def update_status(self, time_off_id: str, status: str, approver_id: str | None = None) -> None:
        vals: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if approver_id:
            vals["approved_by"] = approver_id
            vals["approved_at"] = datetime.now(timezone.utc)
        await self._s.execute(
            update(TimeOffModel).where(TimeOffModel.id == time_off_id).values(**vals)
        )

    async def get_blocked_dates_for_staff(
        self, staff_id: str, start: str, end: str
    ) -> list[str]:
        r = await self._s.execute(
            select(TimeOffModel.start_date, TimeOffModel.end_date)
            .where(TimeOffModel.staff_id == staff_id)
            .where(TimeOffModel.status == "approved")
            .where(TimeOffModel.start_date >= start)
            .where(TimeOffModel.end_date <= end)
        )
        dates: list[str] = []
        for row in r.all():
            # Expandir range de datas
            from datetime import timedelta
            d = row[0]
            while d <= row[1]:
                dates.append(d.strftime("%Y-%m-%d"))
                d += timedelta(days=1)
        return dates


# ============================================================
# InvitationRepository
# ============================================================

class InvitationRepository(IInvitationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, invitation_id: str) -> Invitation | None:
        r = await self._s.execute(select(InvitationModel).where(InvitationModel.id == invitation_id))
        m = r.scalar_one_or_none()
        return _invitation_to_entity(m) if m else None

    async def get_by_token_hash(self, token_hash: str) -> Invitation | None:
        r = await self._s.execute(
            select(InvitationModel).where(InvitationModel.token_hash == token_hash)
        )
        m = r.scalar_one_or_none()
        return _invitation_to_entity(m) if m else None

    async def list_pending_for_tenant(self, tenant_id: str) -> list[Invitation]:
        r = await self._s.execute(
            select(InvitationModel)
            .where(InvitationModel.tenant_id == tenant_id)
            .where(InvitationModel.status == "pending")
            .order_by(InvitationModel.created_at.desc())
        )
        return [_invitation_to_entity(m) for m in r.scalars().all()]

    async def create(self, invitation: Invitation) -> Invitation:
        m = InvitationModel(
            id=invitation.id, tenant_id=invitation.tenant_id, email=invitation.email,
            position_id=invitation.position_id, invited_by=invitation.invited_by,
            token_hash=invitation.token_hash, status=invitation.status,
            expires_at=invitation.expires_at, message=invitation.message,
        )
        self._s.add(m)
        await self._s.flush()
        return _invitation_to_entity(m)

    async def update_status(self, invitation_id: str, status: str) -> None:
        vals: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if status == "accepted":
            vals["accepted_at"] = datetime.now(timezone.utc)
        elif status == "declined":
            vals["declined_at"] = datetime.now(timezone.utc)
        await self._s.execute(
            update(InvitationModel).where(InvitationModel.id == invitation_id).values(**vals)
        )

    async def cancel_all_pending_for_email(self, tenant_id: str, email: str) -> None:
        await self._s.execute(
            update(InvitationModel)
            .where(InvitationModel.tenant_id == tenant_id)
            .where(InvitationModel.email == email)
            .where(InvitationModel.status == "pending")
            .values(status="cancelled", updated_at=datetime.now(timezone.utc))
        )


# ============================================================
# StaffAuditRepository
# ============================================================

class StaffAuditRepository(IStaffAuditRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def log(self, entry: StaffAuditLog) -> StaffAuditLog:
        m = StaffAuditLogModel(
            id=entry.id, tenant_id=entry.tenant_id, actor_id=entry.actor_id,
            target_id=entry.target_id, action=entry.action,
            changes=entry.changes, ip_address=entry.ip_address,
        )
        self._s.add(m)
        await self._s.flush()
        return entry

    async def list_for_tenant(
        self, tenant_id: str, *, target_id: str | None = None,
        action: str | None = None, offset: int = 0, limit: int = 50,
    ) -> tuple[list[StaffAuditLog], int]:
        base = select(StaffAuditLogModel).where(StaffAuditLogModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(StaffAuditLogModel).where(
            StaffAuditLogModel.tenant_id == tenant_id
        )
        if target_id:
            base = base.where(StaffAuditLogModel.target_id == target_id)
            count_q = count_q.where(StaffAuditLogModel.target_id == target_id)
        if action:
            base = base.where(StaffAuditLogModel.action == action)
            count_q = count_q.where(StaffAuditLogModel.action == action)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(
            base.order_by(StaffAuditLogModel.created_at.desc()).offset(offset).limit(limit)
        )
        return [_audit_to_entity(m) for m in r.scalars().all()], total
