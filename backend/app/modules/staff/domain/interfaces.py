"""Staff Module — Repository Interfaces (Ports)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

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


class IStaffRepository(ABC):
    """Contrato para persistência de StaffProfile."""

    @abstractmethod
    async def get_by_id(self, staff_id: str) -> StaffProfile | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> StaffProfile | None: ...

    @abstractmethod
    async def list_by_tenant(
        self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[StaffProfile], int]: ...

    @abstractmethod
    async def list_by_team(self, team_id: str) -> list[StaffProfile]: ...

    @abstractmethod
    async def create(self, staff: StaffProfile) -> StaffProfile: ...

    @abstractmethod
    async def update(self, staff: StaffProfile) -> StaffProfile: ...

    @abstractmethod
    async def update_status(self, staff_id: str, status: str) -> None: ...

    @abstractmethod
    async def count_active(self, tenant_id: str) -> int: ...


class IPositionRepository(ABC):
    """Contrato para persistência de Position."""

    @abstractmethod
    async def get_by_id(self, position_id: str) -> Position | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[Position]: ...

    @abstractmethod
    async def create(self, position: Position) -> Position: ...

    @abstractmethod
    async def update(self, position: Position) -> Position: ...

    @abstractmethod
    async def delete(self, position_id: str) -> None: ...


class ISpecialtyRepository(ABC):
    """Contrato para persistência de Specialty."""

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[Specialty]: ...

    @abstractmethod
    async def create(self, specialty: Specialty) -> Specialty: ...

    @abstractmethod
    async def update(self, specialty: Specialty) -> Specialty: ...

    @abstractmethod
    async def delete(self, specialty_id: str) -> None: ...


class ITeamRepository(ABC):
    """Contrato para persistência de Team."""

    @abstractmethod
    async def get_by_id(self, team_id: str) -> Team | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[Team]: ...

    @abstractmethod
    async def create(self, team: Team) -> Team: ...

    @abstractmethod
    async def update(self, team: Team) -> Team: ...

    @abstractmethod
    async def delete(self, team_id: str) -> None: ...

    @abstractmethod
    async def add_member(self, team_id: str, staff_id: str) -> None: ...

    @abstractmethod
    async def remove_member(self, team_id: str, staff_id: str) -> None: ...

    @abstractmethod
    async def get_member_ids(self, team_id: str) -> list[str]: ...


class IScheduleRepository(ABC):
    """Contrato para persistência de StaffSchedule."""

    @abstractmethod
    async def get_for_staff(self, staff_id: str) -> list[StaffSchedule]: ...

    @abstractmethod
    async def upsert_batch(
        self, staff_id: str, schedules: list[StaffSchedule]
    ) -> list[StaffSchedule]: ...


class ITimeOffRepository(ABC):
    """Contrato para persistência de TimeOff."""

    @abstractmethod
    async def get_by_id(self, time_off_id: str) -> TimeOff | None: ...

    @abstractmethod
    async def list_for_staff(
        self, staff_id: str, *, status: str | None = None
    ) -> list[TimeOff]: ...

    @abstractmethod
    async def list_for_tenant(
        self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[TimeOff], int]: ...

    @abstractmethod
    async def create(self, time_off: TimeOff) -> TimeOff: ...

    @abstractmethod
    async def update_status(self, time_off_id: str, status: str, approver_id: str | None = None) -> None: ...

    @abstractmethod
    async def get_blocked_dates_for_staff(
        self, staff_id: str, start: str, end: str
    ) -> list[str]: ...


class IInvitationRepository(ABC):
    """Contrato para persistência de Invitation."""

    @abstractmethod
    async def get_by_id(self, invitation_id: str) -> Invitation | None: ...

    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> Invitation | None: ...

    @abstractmethod
    async def list_pending_for_tenant(self, tenant_id: str) -> list[Invitation]: ...

    @abstractmethod
    async def create(self, invitation: Invitation) -> Invitation: ...

    @abstractmethod
    async def update_status(self, invitation_id: str, status: str) -> None: ...

    @abstractmethod
    async def cancel_all_pending_for_email(self, tenant_id: str, email: str) -> None: ...


class IStaffAuditRepository(ABC):
    """Contrato para registro de auditoria."""

    @abstractmethod
    async def log(self, entry: StaffAuditLog) -> StaffAuditLog: ...

    @abstractmethod
    async def list_for_tenant(
        self, tenant_id: str, *, target_id: str | None = None,
        action: str | None = None, offset: int = 0, limit: int = 50,
    ) -> tuple[list[StaffAuditLog], int]: ...
