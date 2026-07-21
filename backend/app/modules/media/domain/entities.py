"""Media Module — Domain Entities.

MediaAsset (arquivo), CMSBlock, CMSContent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class MediaAsset:
    """Arquivo de mídia — imagem, vídeo, documento."""

    id: str
    tenant_id: str
    filename: str  # Nome único (hash)
    original_name: str
    mime_type: str = "image/jpeg"
    size_bytes: int = 0
    url: str = ""
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None
    content_hash: str = ""  # SHA-256 — anti-duplicata
    media_type: str = "gallery"  # logo, banner, gallery, professional_photo, service_photo
    alt_text: str | None = None
    title: str | None = None
    sort_order: int = 0
    is_visible: bool = True
    uploaded_by: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None


@dataclass
class CMSBlock:
    """Bloco de conteúdo do CMS."""

    block_type: str  # "hero", "text", "image", "cta", "gallery", "team", "services", "contact"
    data: dict[str, Any] = field(default_factory=dict)
    order: int = 0
    id: str = ""


@dataclass
class CMSPage:
    """Página do CMS — composta de blocos."""

    id: str
    tenant_id: str
    slug: str  # "home", "about", "services", "contact"
    title: str = ""
    blocks: list[CMSBlock] = field(default_factory=list)
    meta_title: str = ""
    meta_description: str = ""
    meta_keywords: str = ""
    og_image_url: str | None = None
    is_published: bool = False
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
