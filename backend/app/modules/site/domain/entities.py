"""Site Module — Domain Entities.

Entidades para o site público white-label de cada tenant.
SitePage, SEOSettings, SiteContent, GalleryItem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class SitePage:
    """Página de conteúdo editável (Sobre, Privacidade, Termos, FAQ)."""

    id: str
    tenant_id: str
    slug: str  # "about", "privacy", "terms", "faq"
    title: str = ""
    content: str = ""  # Markdown / rich text
    meta_title: str = ""
    meta_description: str = ""
    is_published: bool = False
    version: int = 1
    published_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SEOSettings:
    """Configurações de SEO do site público (1:1 com tenant)."""

    id: str
    tenant_id: str
    meta_title: str = ""  # Default: tenant.name
    meta_description: str = ""
    meta_keywords: str = ""
    og_image_url: str | None = None
    twitter_handle: str | None = None
    google_analytics_id: str | None = None
    facebook_pixel_id: str | None = None
    custom_header_code: str | None = None  # Sanitizado
    custom_footer_code: str | None = None
    robots_txt: str = "User-agent: *\nAllow: /"
    canonical_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SiteContent:
    """Conteúdo editável da home page (hero, seções, etc.)."""

    id: str
    tenant_id: str
    hero_title: str = ""
    hero_subtitle: str = ""
    hero_cta_text: str = "Agende Agora"
    hero_banner_url: str | None = None
    hero_video_url: str | None = None
    about_title: str = "Sobre Nós"
    about_text: str = ""
    promotions: list[dict[str, Any]] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    show_services: bool = True
    show_team: bool = True
    show_reviews: bool = True
    show_gallery: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
