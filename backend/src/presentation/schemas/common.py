"""API Schemas (Pydantic Models).

Standard response schemas for the API.
All request/response models should be defined using Pydantic v2.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema for all API models.

    Configures:
    - ORM mode for SQLAlchemy integration
    - Extra fields forbidden (strict)
    - JSON serialization defaults
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        populate_by_name=True,
    )


class PaginationParams(BaseModel):
    """Standard pagination query parameters."""

    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(
        default=20, ge=1, le=100, description="Items per page (max 100)"
    )

    @property
    def offset(self) -> int:
        """Calculate SQL offset from page and page_size."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Return the SQL limit."""
        return self.page_size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Standard paginated response wrapper."""

    items: list[T] = Field(default_factory=list)
    total: int = Field(default=0, description="Total number of items")
    page: int = Field(default=1)
    page_size: int = Field(default=20)
    total_pages: int = Field(default=0)

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[T]:
        """Create a paginated response."""
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size if total > 0 else 0,
        )


class TimestampMixin(BaseModel):
    """Mixin that adds timestamp fields to a schema."""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MessageResponse(BaseSchema):
    """Simple message response for acknowledgements."""

    message: str = Field(..., description="Response message")
    status: str = Field(default="ok")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ErrorResponse(BaseSchema):
    """Standard error response (RFC 7807 compatible)."""

    type_: str = Field(alias="type")
    title: str
    status: int
    detail: str
    instance: str | None = None
    error_code: str | None = None
    errors: list[dict[str, Any]] | None = None
