"""Staff Module — SQLAlchemy ORM Models.

8 modelos que implementam o schema de equipe interna.
Todos herdam tenant_id do BaseModel.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, BaseModel


# ============================================================
# Position (Cargo)
# ============================================================

class PositionModel(Base, BaseModel):
    """Cargo configurável — NUNCA hardcoded."""

    __tablename__ = "staff_positions"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_position_tenant_name"),
    )

    # Relationships
    staff_members: Mapped[list["StaffProfileModel"]] = relationship("StaffProfileModel", back_populates="position", lazy="selectin")


# ============================================================
# Specialty
# ============================================================

class SpecialtyModel(Base, BaseModel):
    """Especialidade configurável por tenant."""

    __tablename__ = "staff_specialties"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color_tag: Mapped[str] = mapped_column(String(7), default="#cccccc")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_specialty_tenant_name"),
    )


# ============================================================
# StaffProfile
# ============================================================

class StaffProfileModel(Base, BaseModel):
    """Perfil profissional — estende User (auth module) com dados do workspace."""

    __tablename__ = "staff_profiles"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, unique=True, index=True,
    )
    position_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_positions.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    professional_name: Mapped[str] = mapped_column(String(255), default="")
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    specialties: Mapped[list] = mapped_column(JSONB, default=list)
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    is_visible_on_site: Mapped[bool] = mapped_column(Boolean, default=True)
    commission_type: Mapped[str] = mapped_column(String(20), default="none")
    commission_value: Mapped[int] = mapped_column(Integer, default=0)
    hire_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    termination_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relationships
    position: Mapped[PositionModel | None] = relationship("PositionModel", back_populates="staff_members", lazy="selectin")
    schedules: Mapped[list["StaffScheduleModel"]] = relationship(
        "StaffScheduleModel", back_populates="staff", lazy="selectin",
    )
    time_offs: Mapped[list["TimeOffModel"]] = relationship(
        "TimeOffModel", back_populates="staff", lazy="selectin",
    )
    team_memberships: Mapped[list["TeamMemberModel"]] = relationship(
        "TeamMemberModel", back_populates="staff", lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", name="uq_staff_tenant_user"),
    )


# ============================================================
# Team
# ============================================================

class TeamModel(Base, BaseModel):
    """Equipe — agrupamento de profissionais."""

    __tablename__ = "staff_teams"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color_tag: Mapped[str] = mapped_column(String(7), default="#cccccc")
    leader_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="SET NULL"), nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_team_tenant_name"),
    )

    # Relationships
    members: Mapped[list["TeamMemberModel"]] = relationship(
        "TeamMemberModel", back_populates="team", lazy="selectin",
    )


class TeamMemberModel(Base, BaseModel):
    """Associação N:N entre Team e StaffProfile."""

    __tablename__ = "staff_team_members"

    team_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_teams.id", ondelete="CASCADE"), primary_key=True,
    )
    staff_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="CASCADE"), primary_key=True,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    team: Mapped["TeamModel"] = relationship("TeamModel", back_populates="members", lazy="selectin")
    staff: Mapped["StaffProfileModel"] = relationship("StaffProfileModel", back_populates="team_memberships", lazy="selectin")


# ============================================================
# StaffSchedule
# ============================================================

class StaffScheduleModel(Base, BaseModel):
    """Jornada de trabalho do profissional por dia da semana."""

    __tablename__ = "staff_schedules"

    staff_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    is_working: Mapped[bool] = mapped_column(Boolean, default=True)
    start_time: Mapped[str] = mapped_column(String(5), default="09:00")
    end_time: Mapped[str] = mapped_column(String(5), default="19:00")
    lunch_start: Mapped[str | None] = mapped_column(String(5), nullable=True)
    lunch_end: Mapped[str | None] = mapped_column(String(5), nullable=True)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=30)

    __table_args__ = (
        UniqueConstraint("staff_id", "day_of_week", name="uq_staff_schedule_day"),
    )

    # Relationships
    staff: Mapped["StaffProfileModel"] = relationship("StaffProfileModel", back_populates="schedules", lazy="selectin")


# ============================================================
# TimeOff
# ============================================================

class TimeOffModel(Base, BaseModel):
    """Ausência: férias, folga, licença."""

    __tablename__ = "staff_time_offs"

    staff_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    time_off_type: Mapped[str] = mapped_column(String(30), default="day_off", index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    start_time: Mapped[str | None] = mapped_column(String(5), nullable=True)
    end_time: Mapped[str | None] = mapped_column(String(5), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_full_day: Mapped[bool] = mapped_column(Boolean, default=True)
    approved_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    staff: Mapped["StaffProfileModel"] = relationship("StaffProfileModel", back_populates="time_offs", lazy="selectin")


# ============================================================
# Invitation
# ============================================================

class InvitationModel(Base, BaseModel):
    """Convite por email para novo membro."""

    __tablename__ = "staff_invitations"

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    position_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("staff_positions.id", ondelete="SET NULL"), nullable=True,
    )
    invited_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    declined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "email", "status", name="uq_invitation_tenant_email_status"),
    )


# ============================================================
# StaffAuditLog
# ============================================================

class StaffAuditLogModel(Base, BaseModel):
    """Registro de auditoria do módulo de equipe."""

    __tablename__ = "staff_audit_logs"

    actor_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    target_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    changes: Mapped[dict] = mapped_column(JSONB, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
