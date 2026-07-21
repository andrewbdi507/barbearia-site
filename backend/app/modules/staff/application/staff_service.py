"""Staff Module — Staff Service.

Orquestra todos os casos de uso da equipe interna:
- Gerenciamento de funcionários (CRUD, status, comissão)
- Cargos e especialidades configuráveis
- Equipes com membros
- Jornada de trabalho por profissional
- Ausências (férias, folgas, licenças)
- Convites por email
- Auditoria completa
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.exceptions import (
    BusinessRuleError,
    NotFoundError,
    PlanLimitExceededError,
)
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
from app.modules.staff.domain.enums import (
    AuditAction,
    InvitationStatus,
    StaffStatus,
    TimeOffStatus,
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
from app.modules.tenant.domain.interfaces import ITenantRepository


class StaffService:
    """Serviço de orquestração da equipe interna."""

    def __init__(
        self,
        staff_repo: IStaffRepository,
        position_repo: IPositionRepository,
        specialty_repo: ISpecialtyRepository,
        team_repo: ITeamRepository,
        schedule_repo: IScheduleRepository,
        timeoff_repo: ITimeOffRepository,
        invitation_repo: IInvitationRepository,
        audit_repo: IStaffAuditRepository,
        tenant_repo: ITenantRepository,
    ) -> None:
        self._staff = staff_repo
        self._positions = position_repo
        self._specialties = specialty_repo
        self._teams = team_repo
        self._schedules = schedule_repo
        self._timeoffs = timeoff_repo
        self._invitations = invitation_repo
        self._audit = audit_repo
        self._tenants = tenant_repo

    # ============================================================
    # Staff Profile
    # ============================================================

    async def create_staff(self, tenant_id: str, actor_id: str, **kwargs: object) -> StaffProfile:
        """Cria perfil de funcionário vinculado a um User existente."""
        # Verificar limite do plano
        tenant = await self._tenants.get_by_id(tenant_id)
        if tenant and tenant.plan_id:
            count = await self._staff.count_active(tenant_id)
            # Validate via plan limits (importado do tenant module)
            from app.modules.tenant.application.tenant_service import TenantService
            # Simplified: check directly
            if count >= 100:  # Placeholder — integração real via PlanLimits
                raise PlanLimitExceededError(
                    message="Limite de funcionários do plano excedido.",
                    details={"current": count, "resource": "max_professionals"},
                )

        # Verificar duplicidade user_id no tenant
        existing = await self._staff.get_by_user_id(str(kwargs.get("user_id", "")))
        if existing:
            raise BusinessRuleError(message="Este usuário já possui perfil de funcionário.")

        staff = StaffProfile(
            id=str(uuid4()),
            tenant_id=tenant_id,
            user_id=str(kwargs.get("user_id", "")),
            position_id=str(kwargs.get("position_id", "")) if kwargs.get("position_id") else None,
            professional_name=str(kwargs.get("professional_name", "")),
            photo_url=str(kwargs.get("photo_url", "")) if kwargs.get("photo_url") else None,
            bio=str(kwargs.get("bio", "")) if kwargs.get("bio") else None,
            specialties=list(kwargs.get("specialties", [])),
            experience_years=int(kwargs.get("experience_years", 0)),
            commission_type=str(kwargs.get("commission_type", "none")),
            commission_value=int(kwargs.get("commission_value", 0)),
            hire_date=kwargs.get("hire_date") or datetime.now(timezone.utc),
        )

        created = await self._staff.create(staff)

        # Auditoria
        await self._log(tenant_id, actor_id, created.id, AuditAction.STAFF_CREATED,
                        {"user_id": created.user_id, "name": created.professional_name})

        # Criar schedule padrão (Seg-Sex 09-19, Sab 09-14, Dom off)
        await self._create_default_schedule(tenant_id, created.id)

        return created

    async def get_staff(self, staff_id: str) -> StaffProfile:
        s = await self._staff.get_by_id(staff_id)
        if s is None:
            raise NotFoundError(message="Funcionário não encontrado.")
        return s

    async def get_staff_by_user(self, user_id: str) -> StaffProfile:
        s = await self._staff.get_by_user_id(user_id)
        if s is None:
            raise NotFoundError(message="Perfil de funcionário não encontrado.")
        return s

    async def list_staff(
        self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[StaffProfile], int]:
        return await self._staff.list_by_tenant(tenant_id, status=status, offset=offset, limit=limit)

    async def update_staff(
        self, staff_id: str, actor_id: str, **kwargs: object
    ) -> StaffProfile:
        existing = await self.get_staff(staff_id)
        for key, value in kwargs.items():
            if hasattr(existing, key) and value is not None:
                setattr(existing, key, value)
        updated = await self._staff.update(existing)
        await self._log(existing.tenant_id, actor_id, staff_id, AuditAction.STAFF_UPDATED,
                        dict(kwargs))
        return updated

    async def deactivate_staff(self, staff_id: str, actor_id: str) -> None:
        existing = await self.get_staff(staff_id)
        existing.deactivate()
        await self._staff.update_status(staff_id, StaffStatus.INACTIVE)
        await self._log(existing.tenant_id, actor_id, staff_id, AuditAction.STAFF_DEACTIVATED)

    async def reactivate_staff(self, staff_id: str, actor_id: str) -> None:
        existing = await self.get_staff(staff_id)
        existing.activate()
        await self._staff.update_status(staff_id, StaffStatus.ACTIVE)
        await self._log(existing.tenant_id, actor_id, staff_id, AuditAction.STAFF_ACTIVATED)

    async def terminate_staff(self, staff_id: str, actor_id: str) -> None:
        existing = await self.get_staff(staff_id)
        existing.terminate()
        await self._staff.update_status(staff_id, StaffStatus.TERMINATED)
        await self._log(existing.tenant_id, actor_id, staff_id, AuditAction.STAFF_TERMINATED)

    # ============================================================
    # Positions
    # ============================================================

    async def list_positions(self, tenant_id: str) -> list[Position]:
        return await self._positions.list_by_tenant(tenant_id)

    async def create_position(self, tenant_id: str, **kwargs: object) -> Position:
        position = Position(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            description=str(kwargs.get("description", "")),
            sort_order=int(kwargs.get("sort_order", 0)),
        )
        return await self._positions.create(position)

    async def update_position(self, position_id: str, **kwargs: object) -> Position:
        existing = await self._positions.get_by_id(position_id)
        if existing is None:
            raise NotFoundError(message="Cargo não encontrado.")
        for k, v in kwargs.items():
            if hasattr(existing, k) and v is not None:
                setattr(existing, k, v)
        return await self._positions.update(existing)

    async def delete_position(self, position_id: str) -> None:
        await self._positions.delete(position_id)

    # ============================================================
    # Specialties
    # ============================================================

    async def list_specialties(self, tenant_id: str) -> list[Specialty]:
        return await self._specialties.list_by_tenant(tenant_id)

    async def create_specialty(self, tenant_id: str, **kwargs: object) -> Specialty:
        spec = Specialty(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            description=str(kwargs.get("description", "")),
            color_tag=str(kwargs.get("color_tag", "#cccccc")),
            sort_order=int(kwargs.get("sort_order", 0)),
        )
        return await self._specialties.create(spec)

    async def update_specialty(self, specialty_id: str, **kwargs: object) -> Specialty:
        existing = await self._specialties.list_by_tenant("")
        # Find by id
        spec = next((s for s in existing if s.id == specialty_id), None)
        if spec is None:
            raise NotFoundError(message="Especialidade não encontrada.")
        for k, v in kwargs.items():
            if hasattr(spec, k) and v is not None:
                setattr(spec, k, v)
        return await self._specialties.update(spec)

    async def delete_specialty(self, specialty_id: str) -> None:
        await self._specialties.delete(specialty_id)

    # ============================================================
    # Teams
    # ============================================================

    async def list_teams(self, tenant_id: str) -> list[Team]:
        return await self._teams.list_by_tenant(tenant_id)

    async def get_team(self, team_id: str) -> Team:
        t = await self._teams.get_by_id(team_id)
        if t is None:
            raise NotFoundError(message="Equipe não encontrada.")
        return t

    async def create_team(self, tenant_id: str, actor_id: str, **kwargs: object) -> Team:
        team = Team(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            description=str(kwargs.get("description", "")),
            color_tag=str(kwargs.get("color_tag", "#cccccc")),
            leader_id=str(kwargs.get("leader_id", "")) if kwargs.get("leader_id") else None,
            member_ids=list(kwargs.get("member_ids", [])),
            sort_order=int(kwargs.get("sort_order", 0)),
        )
        created = await self._teams.create(team)
        await self._log(tenant_id, actor_id, created.id, AuditAction.TEAM_CREATED,
                        {"name": created.name})
        return created

    async def update_team(self, team_id: str, actor_id: str, **kwargs: object) -> Team:
        existing = await self.get_team(team_id)
        for k, v in kwargs.items():
            if hasattr(existing, k) and v is not None:
                setattr(existing, k, v)
        updated = await self._teams.update(existing)
        await self._log(existing.tenant_id, actor_id, team_id, AuditAction.TEAM_UPDATED)
        return updated

    async def delete_team(self, team_id: str, actor_id: str) -> None:
        team = await self.get_team(team_id)
        await self._teams.delete(team_id)
        await self._log(team.tenant_id, actor_id, team_id, AuditAction.TEAM_DELETED)

    async def add_team_member(self, team_id: str, staff_id: str, actor_id: str) -> None:
        team = await self.get_team(team_id)
        await self._teams.add_member(team_id, staff_id)
        await self._log(team.tenant_id, actor_id, staff_id, AuditAction.MEMBER_ADDED,
                        {"team_id": team_id})

    async def remove_team_member(self, team_id: str, staff_id: str, actor_id: str) -> None:
        team = await self.get_team(team_id)
        await self._teams.remove_member(team_id, staff_id)
        await self._log(team.tenant_id, actor_id, staff_id, AuditAction.MEMBER_REMOVED,
                        {"team_id": team_id})

    # ============================================================
    # Schedules
    # ============================================================

    async def get_schedule(self, staff_id: str) -> list[StaffSchedule]:
        return await self._schedules.get_for_staff(staff_id)

    async def update_schedule(
        self, staff_id: str, tenant_id: str, schedules: list[dict],
    ) -> list[StaffSchedule]:
        entities = [
            StaffSchedule(
                id=str(uuid4()), tenant_id=tenant_id, staff_id=staff_id,
                day_of_week=s["day_of_week"], is_working=s.get("is_working", True),
                start_time=s.get("start_time", "09:00"),
                end_time=s.get("end_time", "19:00"),
                lunch_start=s.get("lunch_start"),
                lunch_end=s.get("lunch_end"),
                slot_duration_minutes=s.get("slot_duration_minutes", 30),
            )
            for s in schedules
        ]
        return await self._schedules.upsert_batch(staff_id, entities)

    # ============================================================
    # Time Off
    # ============================================================

    async def request_time_off(
        self, tenant_id: str, staff_id: str, actor_id: str, **kwargs: object
    ) -> TimeOff:
        to = TimeOff(
            id=str(uuid4()), tenant_id=tenant_id, staff_id=staff_id,
            time_off_type=str(kwargs.get("time_off_type", "day_off")),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            start_time=str(kwargs.get("start_time", "")) if kwargs.get("start_time") else None,
            end_time=str(kwargs.get("end_time", "")) if kwargs.get("end_time") else None,
            reason=str(kwargs.get("reason", "")),
            is_full_day=bool(kwargs.get("is_full_day", True)),
        )
        created = await self._timeoffs.create(to)
        await self._log(tenant_id, actor_id, staff_id, AuditAction.TIME_OFF_REQUESTED,
                        {"type": to.time_off_type, "dates": f"{to.start_date}→{to.end_date}"})
        return created

    async def approve_time_off(self, time_off_id: str, approver_id: str) -> None:
        to = await self._timeoffs.get_by_id(time_off_id)
        if to is None:
            raise NotFoundError(message="Ausência não encontrada.")
        to.approve(approver_id)
        await self._timeoffs.update_status(time_off_id, TimeOffStatus.APPROVED, approver_id)
        await self._log(to.tenant_id, approver_id, to.staff_id,
                        AuditAction.TIME_OFF_APPROVED, {"time_off_id": time_off_id})

    async def reject_time_off(self, time_off_id: str, approver_id: str) -> None:
        to = await self._timeoffs.get_by_id(time_off_id)
        if to is None:
            raise NotFoundError(message="Ausência não encontrada.")
        to.reject(approver_id)
        await self._timeoffs.update_status(time_off_id, TimeOffStatus.REJECTED, approver_id)
        await self._log(to.tenant_id, approver_id, to.staff_id,
                        AuditAction.TIME_OFF_REJECTED, {"time_off_id": time_off_id})

    async def list_time_offs(
        self, tenant_id: str, *, staff_id: str | None = None,
        status: str | None = None, offset: int = 0, limit: int = 50,
    ) -> tuple[list[TimeOff], int]:
        if staff_id:
            items = await self._timeoffs.list_for_staff(staff_id, status=status)
            return items, len(items)
        return await self._timeoffs.list_for_tenant(tenant_id, status=status, offset=offset, limit=limit)

    async def get_blocked_dates(self, staff_id: str, start: str, end: str) -> list[str]:
        return await self._timeoffs.get_blocked_dates_for_staff(staff_id, start, end)

    # ============================================================
    # Invitations
    # ============================================================

    async def invite_staff(
        self, tenant_id: str, invited_by: str, email: str,
        position_id: str | None = None, message: str = "",
    ) -> Invitation:
        """Cria convite por email."""
        # Cancelar convites pendentes anteriores para este email
        await self._invitations.cancel_all_pending_for_email(tenant_id, email)

        import hashlib, secrets
        raw_token = secrets.token_hex(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        invitation = Invitation(
            id=str(uuid4()), tenant_id=tenant_id, email=email,
            position_id=position_id, invited_by=invited_by,
            token_hash=token_hash,
            status=InvitationStatus.PENDING,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            message=message,
        )
        created = await self._invitations.create(invitation)
        await self._log(tenant_id, invited_by, created.id, AuditAction.INVITATION_SENT,
                        {"email": email})

        # TODO: Enviar email com raw_token
        return created

    async def accept_invitation(self, token_hash: str) -> Invitation:
        invitation = await self._invitations.get_by_token_hash(token_hash)
        if invitation is None or not invitation.is_pending:
            raise BusinessRuleError(message="Convite inválido ou expirado.")
        await self._invitations.update_status(invitation.id, InvitationStatus.ACCEPTED)
        return invitation

    async def decline_invitation(self, token_hash: str) -> None:
        invitation = await self._invitations.get_by_token_hash(token_hash)
        if invitation is None:
            raise NotFoundError(message="Convite não encontrado.")
        await self._invitations.update_status(invitation.id, InvitationStatus.DECLINED)

    async def cancel_invitation(self, invitation_id: str, actor_id: str) -> None:
        invitation = await self._invitations.get_by_id(invitation_id)
        if invitation is None:
            raise NotFoundError(message="Convite não encontrado.")
        await self._invitations.update_status(invitation_id, InvitationStatus.CANCELLED)
        await self._log(invitation.tenant_id, actor_id, invitation_id,
                        AuditAction.INVITATION_CANCELLED)

    async def list_pending_invitations(self, tenant_id: str) -> list[Invitation]:
        return await self._invitations.list_pending_for_tenant(tenant_id)

    # ============================================================
    # Audit
    # ============================================================

    async def list_audit_logs(
        self, tenant_id: str, *, target_id: str | None = None,
        action: str | None = None, offset: int = 0, limit: int = 50,
    ) -> tuple[list[StaffAuditLog], int]:
        return await self._audit.list_for_tenant(
            tenant_id, target_id=target_id, action=action, offset=offset, limit=limit,
        )

    # ============================================================
    # Helpers
    # ============================================================

    async def _log(
        self, tenant_id: str, actor_id: str | None,
        target_id: str | None, action: str, changes: dict | None = None,
    ) -> None:
        await self._audit.log(StaffAuditLog(
            id=str(uuid4()), tenant_id=tenant_id,
            actor_id=actor_id, target_id=target_id,
            action=action, changes=changes or {},
        ))

    async def _create_default_schedule(self, tenant_id: str, staff_id: str) -> None:
        defaults = [
            (0, True, "09:00", "19:00"),   # Mon
            (1, True, "09:00", "19:00"),   # Tue
            (2, True, "09:00", "19:00"),   # Wed
            (3, True, "09:00", "19:00"),   # Thu
            (4, True, "09:00", "19:00"),   # Fri
            (5, True, "09:00", "14:00"),   # Sat
            (6, False, "00:00", "00:00"),  # Sun
        ]
        entities = [
            StaffSchedule(
                id=str(uuid4()), tenant_id=tenant_id, staff_id=staff_id,
                day_of_week=dow, is_working=working,
                start_time=st, end_time=et,
            )
            for dow, working, st, et in defaults
        ]
        await self._schedules.upsert_batch(staff_id, entities)
