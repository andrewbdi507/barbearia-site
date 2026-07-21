"""Media Module — SQLAlchemy Models + Repository."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import BaseModel
from app.modules.media.domain.entities import CMSPage, CMSBlock, MediaAsset
from app.modules.media.domain.repository_interfaces import ICMSPageRepository, IMediaRepository


class MediaAssetModel(BaseModel):
    __tablename__ = "media_assets"

    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="image/jpeg")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(Text, default="")
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), default="", index=True)
    media_type: Mapped[str] = mapped_column(String(30), default="gallery", index=True)
    alt_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CMSPageModel(BaseModel):
    __tablename__ = "cms_pages"

    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="")
    blocks: Mapped[list] = mapped_column(JSONB, default=list)
    meta_title: Mapped[str] = mapped_column(String(200), default="")
    meta_description: Mapped[str] = mapped_column(String(500), default="")
    meta_keywords: Mapped[str] = mapped_column(String(500), default="")
    og_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)

    __table_args__ = (UniqueConstraint("tenant_id", "slug", name="uq_cmspage_tenant_slug"),)


# ============================================================
# Repositories
# ============================================================

class MediaRepository(IMediaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, asset_id: str) -> MediaAsset | None:
        r = await self._s.execute(
            select(MediaAssetModel).where(MediaAssetModel.id == asset_id, MediaAssetModel.deleted_at.is_(None))
        )
        m = r.scalar_one_or_none()
        return self._to_entity(m) if m else None

    async def get_by_hash(self, tenant_id: str, content_hash: str) -> MediaAsset | None:
        r = await self._s.execute(
            select(MediaAssetModel).where(
                MediaAssetModel.tenant_id == tenant_id,
                MediaAssetModel.content_hash == content_hash,
                MediaAssetModel.deleted_at.is_(None),
            )
        )
        m = r.scalar_one_or_none()
        return self._to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str, *, media_type: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[MediaAsset], int]:
        base = select(MediaAssetModel).where(MediaAssetModel.tenant_id == tenant_id, MediaAssetModel.deleted_at.is_(None))
        count_q = select(func.count()).select_from(MediaAssetModel).where(MediaAssetModel.tenant_id == tenant_id, MediaAssetModel.deleted_at.is_(None))
        if media_type:
            base = base.where(MediaAssetModel.media_type == media_type)
            count_q = count_q.where(MediaAssetModel.media_type == media_type)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(MediaAssetModel.created_at.desc()).offset(offset).limit(limit))
        return [self._to_entity(m) for m in r.scalars().all()], total

    async def create(self, asset: MediaAsset) -> MediaAsset:
        m = MediaAssetModel(
            id=asset.id, tenant_id=asset.tenant_id,
            filename=asset.filename, original_name=asset.original_name,
            mime_type=asset.mime_type, size_bytes=asset.size_bytes,
            url=asset.url, thumbnail_url=asset.thumbnail_url,
            width=asset.width, height=asset.height,
            content_hash=asset.content_hash, media_type=asset.media_type,
            alt_text=asset.alt_text, title=asset.title,
            sort_order=asset.sort_order, is_visible=asset.is_visible,
            uploaded_by=asset.uploaded_by, metadata=asset.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return self._to_entity(m)

    async def update(self, asset: MediaAsset) -> MediaAsset:
        m = await self._s.get(MediaAssetModel, asset.id)
        if not m: raise ValueError(f"Media {asset.id} not found")
        for f in ("alt_text", "title", "sort_order", "is_visible", "metadata"):
            setattr(m, f, getattr(asset, f))
        await self._s.flush()
        return self._to_entity(m)

    async def soft_delete(self, asset_id: str) -> None:
        from sqlalchemy import update
        await self._s.execute(
            update(MediaAssetModel).where(MediaAssetModel.id == asset_id).values(deleted_at=datetime.now(timezone.utc))
        )

    @staticmethod
    def _to_entity(m: MediaAssetModel) -> MediaAsset:
        return MediaAsset(
            id=m.id, tenant_id=m.tenant_id or "",
            filename=m.filename, original_name=m.original_name,
            mime_type=m.mime_type, size_bytes=m.size_bytes,
            url=m.url, thumbnail_url=m.thumbnail_url,
            width=m.width, height=m.height,
            content_hash=m.content_hash, media_type=m.media_type,
            alt_text=m.alt_text, title=m.title,
            sort_order=m.sort_order, is_visible=m.is_visible,
            uploaded_by=m.uploaded_by, metadata=m.metadata or {},
            created_at=m.created_at, deleted_at=m.deleted_at,
        )


class CMSPageRepository(ICMSPageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_slug(self, tenant_id: str, slug: str) -> CMSPage | None:
        r = await self._s.execute(
            select(CMSPageModel).where(CMSPageModel.tenant_id == tenant_id, CMSPageModel.slug == slug)
        )
        m = r.scalar_one_or_none()
        return self._to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str) -> list[CMSPage]:
        r = await self._s.execute(select(CMSPageModel).where(CMSPageModel.tenant_id == tenant_id))
        return [self._to_entity(m) for m in r.scalars().all()]

    async def upsert(self, page: CMSPage) -> CMSPage:
        r = await self._s.execute(
            select(CMSPageModel).where(CMSPageModel.tenant_id == page.tenant_id, CMSPageModel.slug == page.slug)
        )
        m = r.scalar_one_or_none()
        if m:
            m.title = page.title
            m.blocks = [b.__dict__ for b in page.blocks]
            m.meta_title = page.meta_title
            m.meta_description = page.meta_description
            m.meta_keywords = page.meta_keywords
            m.og_image_url = page.og_image_url
            m.is_published = page.is_published
            m.version = page.version + 1
            m.updated_at = datetime.now(timezone.utc)
        else:
            m = CMSPageModel(
                id=page.id, tenant_id=page.tenant_id, slug=page.slug,
                title=page.title, blocks=[b.__dict__ for b in page.blocks],
                meta_title=page.meta_title, meta_description=page.meta_description,
                is_published=page.is_published,
            )
            self._s.add(m)
        await self._s.flush()
        return self._to_entity(m)

    @staticmethod
    def _to_entity(m: CMSPageModel) -> CMSPage:
        blocks = [CMSBlock(**b) for b in (m.blocks or [])]
        return CMSPage(
            id=m.id, tenant_id=m.tenant_id or "", slug=m.slug,
            title=m.title, blocks=blocks,
            meta_title=m.meta_title, meta_description=m.meta_description,
            meta_keywords=m.meta_keywords, og_image_url=m.og_image_url,
            is_published=m.is_published, version=m.version,
            created_at=m.created_at, updated_at=m.updated_at,
        )
