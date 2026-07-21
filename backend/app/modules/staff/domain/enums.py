"""Staff Module — Domain Enums.

Define TODOS os estados, tipos e categorias do módulo de equipe.
"""

from __future__ import annotations

from enum import StrEnum


class StaffStatus(StrEnum):
    """Status do profissional no workspace."""

    INVITED = "invited"
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class TimeOffType(StrEnum):
    """Tipos de ausência."""

    VACATION = "vacation"
    DAY_OFF = "day_off"
    SICK_LEAVE = "sick_leave"
    MATERNITY_LEAVE = "maternity_leave"
    PATERNITY_LEAVE = "paternity_leave"
    BEREAVEMENT = "bereavement"
    TRAINING = "training"
    OTHER = "other"


class TimeOffStatus(StrEnum):
    """Status da solicitação de ausência."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class CommissionType(StrEnum):
    """Tipo de comissão."""

    NONE = "none"
    PERCENTAGE = "percentage"  # % sobre o valor do serviço
    FIXED = "fixed"  # valor fixo por serviço


class InvitationStatus(StrEnum):
    """Status do convite."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class WeekDay(StrEnum):
    """Dias da semana."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @property
    def iso_number(self) -> int:
        mapping = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
        }
        return mapping[self.value]


class AuditAction(StrEnum):
    """Ações auditadas no módulo de equipe."""

    STAFF_CREATED = "staff_created"
    STAFF_UPDATED = "staff_updated"
    STAFF_ACTIVATED = "staff_activated"
    STAFF_DEACTIVATED = "staff_deactivated"
    STAFF_TERMINATED = "staff_terminated"
    ROLE_CHANGED = "role_changed"
    PERMISSION_CHANGED = "permission_changed"
    TEAM_CREATED = "team_created"
    TEAM_UPDATED = "team_updated"
    TEAM_DELETED = "team_deleted"
    MEMBER_ADDED = "member_added"
    MEMBER_REMOVED = "member_removed"
    SCHEDULE_UPDATED = "schedule_updated"
    TIME_OFF_REQUESTED = "time_off_requested"
    TIME_OFF_APPROVED = "time_off_approved"
    TIME_OFF_REJECTED = "time_off_rejected"
    INVITATION_SENT = "invitation_sent"
    INVITATION_RESENT = "invitation_resent"
    INVITATION_CANCELLED = "invitation_cancelled"
    COMMISSION_UPDATED = "commission_updated"
    POSITION_CHANGED = "position_changed"
