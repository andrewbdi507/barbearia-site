"""Staff Module — Domain Entities.

Entidades puras — sem dependência de ORM.
Staff (funcionário), Team, Position, Specialty, Schedule, TimeOff, Invitation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.modules.staff.domain.enums import (
    AuditAction,
    CommissionType,
    InvitationStatus,
    StaffStatus,
    TimeOffStatus,
    TimeOffType,
)
from app.modules.staff.domain.value_objects import CommissionRule


@dataclass
class Position:
    """Cargo configurável — NUNCA hardcoded.

    Exemplos: Administrador, Gerente, Recepcionista, Barbeiro, Auxiliar.
    """

    id: str
    tenant_id: str
    name: str
    description: str = ""
    is_system: bool = False  # Não pode ser deletado
    sort_order: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Specialty:
    """Especialidade configurável por tenant.

    Exemplos: Barba, Corte, Química, Coloração, Hidratação.
    """

    id: str
    tenant_id: str
    name: str
    description: str = ""
    color_tag: str = "#cccccc"
    is_active: bool = True
    sort_order: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class StaffProfile:
    """Perfil profissional do funcionário (1:1 com User).

    Estende User com dados específicos do workspace:
    - Nome profissional, bio, foto
    - Especialidades
    - Tempo de experiência
    - Comissão
    """

    id: str
    tenant_id: str
    user_id: str  # FK → User (auth module)
    position_id: str | None = None  # FK → Position
    professional_name: str = ""  # Nome de exibição profissional
    photo_url: str | None = None
    bio: str | None = None
    specialties: list[str] = field(default_factory=list)  # Specialty IDs
    experience_years: int = 0
    status: StaffStatus = StaffStatus.ACTIVE
    is_visible_on_site: bool = True
    commission_type: str = "none"
    commission_value: int = 0  # percentual ou centavos
    hire_date: datetime | None = None
    termination_date: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_active(self) -> bool:
        return self.status == StaffStatus.ACTIVE

    @property
    def commission_rule(self) -> CommissionRule:
        return CommissionRule(
            commission_type=self.commission_type,
            value=self.commission_value,
        )

    def activate(self) -> None:
        if self.status in {StaffStatus.INACTIVE, StaffStatus.SUSPENDED}:
            self.status = StaffStatus.ACTIVE
            self.termination_date = None

    def deactivate(self) -> None:
        self.status = StaffStatus.INACTIVE

    def terminate(self) -> None:
        self.status = StaffStatus.TERMINATED
        self.termination_date = datetime.now(timezone.utc)


@dataclass
class Team:
    """Equipe — agrupamento de profissionais.

    Exemplos: Equipe Manhã, Equipe Tarde, Equipe Premium, Unidade Centro.
    """

    id: str
    tenant_id: str
    name: str
    description: str = ""
    color_tag: str = "#cccccc"
    leader_id: str | None = None  # FK → StaffProfile
    is_active: bool = True
    sort_order: int = 0
    member_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class StaffSchedule:
    """Jornada de trabalho do profissional por dia da semana."""

    id: str
    tenant_id: str
    staff_id: str
    day_of_week: int  # 0=Monday (ISO)
    is_working: bool = True
    start_time: str = "09:00"
    end_time: str = "19:00"
    lunch_start: str | None = None
    lunch_end: str | None = None
    slot_duration_minutes: int = 30
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TimeOff:
    """Ausência: férias, folga, licença, etc."""

    id: str
    tenant_id: str
    staff_id: str
    time_off_type: TimeOffType = TimeOffType.DAY_OFF
    status: TimeOffStatus = TimeOffStatus.PENDING
    start_date: datetime | None = None
    end_date: datetime | None = None
    start_time: str | None = None  # Para ausências parciais
    end_time: str | None = None
    reason: str = ""
    is_full_day: bool = True
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def approve(self, approver_id: str) -> None:
        self.status = TimeOffStatus.APPROVED
        self.approved_by = approver_id
        self.approved_at = datetime.now(timezone.utc)

    def reject(self, approver_id: str) -> None:
        self.status = TimeOffStatus.REJECTED
        self.approved_by = approver_id


@dataclass
class Invitation:
    """Convite para novo membro da equipe."""

    id: str
    tenant_id: str
    email: str
    position_id: str | None = None
    invited_by: str | None = None  # FK → User
    token_hash: str = ""
    status: InvitationStatus = InvitationStatus.PENDING
    expires_at: datetime | None = None
    accepted_at: datetime | None = None
    declined_at: datetime | None = None
    message: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_pending(self) -> bool:
        return self.status == InvitationStatus.PENDING and not self.is_expired


@dataclass
class StaffAuditLog:
    """Registro de auditoria do módulo de equipe."""

    id: str
    tenant_id: str
    actor_id: str | None = None  # Quem fez a ação
    target_id: str | None = None  # Staff afetado
    action: str = ""  # AuditAction
    changes: dict[str, Any] = field(default_factory=dict)  # diff antes/depois
    ip_address: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
