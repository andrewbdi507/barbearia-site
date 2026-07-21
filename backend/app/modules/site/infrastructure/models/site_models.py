"""Site Module — SQLAlchemy Models."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, BaseModel


class SitePageModel(Base, BaseModel):
    __tablename__ = "site_pages"

    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="")
    content: Mapped[str] = mapped_column(Text, default="")
    meta_title: Mapped[str] = mapped_column(String(200), default="")
    meta_description: Mapped[str] = mapped_column(String(500), default="")
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("tenant_id", "slug", name="uq_sitepage_tenant_slug"),)


class SEOSettingsModel(Base, BaseModel):
    __tablename__ = "site_seo"

    tenant_id_override: Mapped[str | None] = mapped_column(String(36), unique=True, nullable=True)
    meta_title: Mapped[str] = mapped_column(String(200), default="")
    meta_description: Mapped[str] = mapped_column(String(500), default="")
    meta_keywords: Mapped[str] = mapped_column(String(500), default="")
    og_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    twitter_handle: Mapped[str | None] = mapped_column(String(50), nullable=True)
    google_analytics_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    facebook_pixel_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    custom_header_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    custom_footer_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    robots_txt: Mapped[str] = mapped_column(Text, default="User-agent: *\\nAllow: /")
    canonical_url: Mapped[str | None] = mapped_column(Text, nullable=True)


class SiteContentModel(Base, BaseModel):
    __tablename__ = "site_content"

    hero_title: Mapped[str] = mapped_column(String(255), default="")
    hero_subtitle: Mapped[str] = mapped_column(String(500), default="")
    hero_cta_text: Mapped[str] = mapped_column(String(50), default="Agende Agora")
    hero_banner_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    about_title: Mapped[str] = mapped_column(String(200), default="Sobre Nós")
    about_text: Mapped[str] = mapped_column(Text, default="")
    promotions: Mapped[list] = mapped_column(JSONB, default=list)
    highlights: Mapped[list] = mapped_column(JSONB, default=list)
    show_services: Mapped[bool] = mapped_column(Boolean, default=True)
    show_team: Mapped[bool] = mapped_column(Boolean, default=True)
    show_reviews: Mapped[bool] = mapped_column(Boolean, default=True)
    show_gallery: Mapped[bool] = mapped_column(Boolean, default=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
