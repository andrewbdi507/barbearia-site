"""Staff Module — API Routes.

Endpoints REST para gerenciamento completo da equipe interna:
- Funcionários (CRUD, status, comissão)
- Cargos configuráveis
- Especialidades
- Equipes
- Jornada de trabalho
- Ausências (férias, folgas)
- Convites
- Auditoria
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.staff.application.dto import (
    AuditLogListResponse,
    AuditLogResponse,
    InvitationCreateRequest,
    InvitationResponse,
    PositionCreateRequest,
    PositionResponse,
    ScheduleBatchRequest,
    ScheduleResponse,
    SpecialtyCreateRequest,
    SpecialtyResponse,
    StaffCreateRequest,
    StaffListResponse,
    StaffResponse,
    StaffUpdateRequest,
    TeamCreateRequest,
    TeamResponse,
    TeamUpdateRequest,
    TimeOffCreateRequest,
    TimeOffResponse,
    TimeOffUpdateStatusRequest,
)
from app.modules.staff.application.staff_service import StaffService
from app.modules.staff.infrastructure.repository import (
    InvitationRepository,
    PositionRepository,
    ScheduleRepository,
    SpecialtyRepository,
    StaffAuditRepository,
    StaffRepository as StaffRepoImpl,
    TeamRepository,
    TimeOffRepository,
)
from app.modules.tenant.infrastructure.repository import TenantRepository
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/staff", tags=["Staff"])


def _get_service(session: AsyncSession) -> StaffService:
    return StaffService(
        staff_repo=StaffRepoImpl(session),
        position_repo=PositionRepository(session),
        specialty_repo=SpecialtyRepository(session),
        team_repo=TeamRepository(session),
        schedule_repo=ScheduleRepository(session),
        timeoff_repo=TimeOffRepository(session),
        invitation_repo=InvitationRepository(session),
        audit_repo=StaffAuditRepository(session),
        tenant_repo=TenantRepository(session),
    )


def _actor_id(request: Request) -> str | None:
    return getattr(request.state, "user_id", None)


# ============================================================
# POSITIONS
# ============================================================

@router.get("/positions", response_model=list[PositionResponse])
async def list_positions(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[PositionResponse]:
    svc = _get_service(session)
    positions = await svc.list_positions(tenant["id"])
    return [PositionResponse(**p.__dict__) for p in positions]


@router.post("/positions", response_model=PositionResponse, status_code=201)
async def create_position(
    body: PositionCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> PositionResponse:
    svc = _get_service(session)
    p = await svc.create_position(tenant["id"], **body.model_dump())
    return PositionResponse(**p.__dict__)


@router.put("/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: str,
    body: PositionCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> PositionResponse:
    svc = _get_service(session)
    p = await svc.update_position(position_id, **body.model_dump())
    return PositionResponse(**p.__dict__)


@router.delete("/positions/{position_id}")
async def delete_position(
    position_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_position(position_id)
    return {"message": "Cargo removido."}


# ============================================================
# SPECIALTIES
# ============================================================

@router.get("/specialties", response_model=list[SpecialtyResponse])
async def list_specialties(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[SpecialtyResponse]:
    svc = _get_service(session)
    specs = await svc.list_specialties(tenant["id"])
    return [SpecialtyResponse(**s.__dict__) for s in specs]


@router.post("/specialties", response_model=SpecialtyResponse, status_code=201)
async def create_specialty(
    body: SpecialtyCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> SpecialtyResponse:
    svc = _get_service(session)
    s = await svc.create_specialty(tenant["id"], **body.model_dump())
    return SpecialtyResponse(**s.__dict__)


@router.put("/specialties/{specialty_id}", response_model=SpecialtyResponse)
async def update_specialty(
    specialty_id: str,
    body: SpecialtyCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> SpecialtyResponse:
    svc = _get_service(session)
    s = await svc.update_specialty(specialty_id, **body.model_dump())
    return SpecialtyResponse(**s.__dict__)


@router.delete("/specialties/{specialty_id}")
async def delete_specialty(
    specialty_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_specialty(specialty_id)
    return {"message": "Especialidade removida."}


# ============================================================
# STAFF PROFILES
# ============================================================

@router.get("", response_model=StaffListResponse)
async def list_staff(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    status: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> StaffListResponse:
    svc = _get_service(session)
    items, total = await svc.list_staff(tenant["id"], status=status, offset=offset, limit=limit)
    return StaffListResponse(
        items=[StaffResponse(**s.__dict__) for s in items],
        total=total, offset=offset, limit=limit,
    )


@router.post("", response_model=StaffResponse, status_code=201)
async def create_staff(
    body: StaffCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> StaffResponse:
    svc = _get_service(session)
    s = await svc.create_staff(tenant["id"], _actor_id(request) or "", **body.model_dump())
    return StaffResponse(**s.__dict__)


@router.get("/me", response_model=StaffResponse)
async def get_my_profile(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> StaffResponse:
    # Get staff by the authenticated user_id from request.state
    # This needs integration with auth's get_current_user
    from fastapi import Request as FastapiReq
    # For MVP: we use tenant context
    svc = _get_service(session)
    # The auth module injects user_id into request.state
    return StaffResponse(**({"id": "", "user_id": "", "professional_name": "", "specialties": [], "experience_years": 0, "status": "active", "is_visible_on_site": False, "commission_type": "none", "commission_value": 0}))


@router.get("/{staff_id}", response_model=StaffResponse)
async def get_staff(
    staff_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StaffResponse:
    svc = _get_service(session)
    s = await svc.get_staff(staff_id)
    return StaffResponse(**s.__dict__)


@router.patch("/{staff_id}", response_model=StaffResponse)
async def update_staff(
    staff_id: str,
    body: StaffUpdateRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> StaffResponse:
    svc = _get_service(session)
    s = await svc.update_staff(staff_id, _actor_id(request) or "", **body.model_dump(exclude_none=True))
    return StaffResponse(**s.__dict__)


@router.post("/{staff_id}/deactivate")
async def deactivate_staff(
    staff_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.deactivate_staff(staff_id, _actor_id(request) or "")
    return {"message": "Funcionário desativado."}


@router.post("/{staff_id}/reactivate")
async def reactivate_staff(
    staff_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.reactivate_staff(staff_id, _actor_id(request) or "")
    return {"message": "Funcionário reativado."}


# ============================================================
# TEAMS
# ============================================================

@router.get("/teams", response_model=list[TeamResponse])
async def list_teams(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[TeamResponse]:
    svc = _get_service(session)
    teams = await svc.list_teams(tenant["id"])
    return [TeamResponse(
        **t.__dict__, member_count=len(t.member_ids),
        members=[],
    ) for t in teams]


@router.post("/teams", response_model=TeamResponse, status_code=201)
async def create_team(
    body: TeamCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    svc = _get_service(session)
    t = await svc.create_team(tenant["id"], _actor_id(request) or "", **body.model_dump())
    return TeamResponse(**t.__dict__, member_count=len(t.member_ids), members=[])


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    svc = _get_service(session)
    t = await svc.get_team(team_id)
    return TeamResponse(**t.__dict__, member_count=len(t.member_ids), members=[])


@router.put("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    body: TeamUpdateRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    svc = _get_service(session)
    t = await svc.update_team(team_id, _actor_id(request) or "", **body.model_dump(exclude_none=True))
    return TeamResponse(**t.__dict__, member_count=len(t.member_ids), members=[])


@router.delete("/teams/{team_id}")
async def delete_team(
    team_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_team(team_id, _actor_id(request) or "")
    return {"message": "Equipe removida."}


@router.post("/teams/{team_id}/members/{staff_id}")
async def add_team_member(
    team_id: str,
    staff_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.add_team_member(team_id, staff_id, _actor_id(request) or "")
    return {"message": "Membro adicionado."}


@router.delete("/teams/{team_id}/members/{staff_id}")
async def remove_team_member(
    team_id: str,
    staff_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.remove_team_member(team_id, staff_id, _actor_id(request) or "")
    return {"message": "Membro removido."}


# ============================================================
# SCHEDULES
# ============================================================

@router.get("/{staff_id}/schedule", response_model=list[ScheduleResponse])
async def get_schedule(
    staff_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[ScheduleResponse]:
    svc = _get_service(session)
    schedules = await svc.get_schedule(staff_id)
    return [ScheduleResponse(**s.__dict__) for s in schedules]


@router.put("/{staff_id}/schedule", response_model=list[ScheduleResponse])
async def update_schedule(
    staff_id: str,
    body: ScheduleBatchRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[ScheduleResponse]:
    svc = _get_service(session)
    schedules = await svc.update_schedule(
        staff_id, tenant["id"], [s.model_dump() for s in body.schedules],
    )
    return [ScheduleResponse(**s.__dict__) for s in schedules]


# ============================================================
# TIME OFFS
# ============================================================

@router.get("/time-offs", response_model=list[TimeOffResponse])
async def list_time_offs(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    staff_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> list[TimeOffResponse]:
    svc = _get_service(session)
    items, _ = await svc.list_time_offs(
        tenant["id"], staff_id=staff_id, status=status, offset=offset, limit=limit,
    )
    return [TimeOffResponse(**t.__dict__) for t in items]


@router.post("/time-offs", response_model=TimeOffResponse, status_code=201)
async def request_time_off(
    body: TimeOffCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> TimeOffResponse:
    svc = _get_service(session)
    staff_id = body.staff_id or ""
    t = await svc.request_time_off(
        tenant["id"], staff_id, _actor_id(request) or "", **body.model_dump(exclude={"staff_id"}),
    )
    return TimeOffResponse(**t.__dict__)


@router.post("/time-offs/{time_off_id}/approve")
async def approve_time_off(
    time_off_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.approve_time_off(time_off_id, _actor_id(request) or "")
    return {"message": "Ausência aprovada."}


@router.post("/time-offs/{time_off_id}/reject")
async def reject_time_off(
    time_off_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.reject_time_off(time_off_id, _actor_id(request) or "")
    return {"message": "Ausência rejeitada."}


# ============================================================
# INVITATIONS
# ============================================================

@router.get("/invitations", response_model=list[InvitationResponse])
async def list_invitations(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[InvitationResponse]:
    svc = _get_service(session)
    items = await svc.list_pending_invitations(tenant["id"])
    return [InvitationResponse(**i.__dict__) for i in items]


@router.post("/invitations", response_model=InvitationResponse, status_code=201)
async def create_invitation(
    body: InvitationCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> InvitationResponse:
    svc = _get_service(session)
    inv = await svc.invite_staff(
        tenant["id"], _actor_id(request) or "", body.email,
        body.position_id, body.message,
    )
    return InvitationResponse(**inv.__dict__)


@router.post("/invitations/{invitation_id}/cancel")
async def cancel_invitation(
    invitation_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.cancel_invitation(invitation_id, _actor_id(request) or "")
    return {"message": "Convite cancelado."}


# ============================================================
# AUDIT
# ============================================================

@router.get("/audit", response_model=AuditLogListResponse)
async def list_audit_logs(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    target_id: str | None = Query(default=None),
    action: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> AuditLogListResponse:
    svc = _get_service(session)
    items, total = await svc.list_audit_logs(
        tenant["id"], target_id=target_id, action=action, offset=offset, limit=limit,
    )
    return AuditLogListResponse(
        items=[AuditLogResponse(**a.__dict__) for a in items],
        total=total, offset=offset, limit=limit,
    )
