"""Media Module — Application Service.

Upload, Media Library, CMS, SEO management.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.media.domain.entities import CMSPage, CMSBlock, MediaAsset
from app.modules.media.domain.interfaces import StorageProvider, StorageProviderFactory
from app.modules.media.domain.repository_interfaces import ICMSPageRepository, IMediaRepository
from app.modules.media.infrastructure.image_processor import ImageProcessor
from app.modules.media.infrastructure.storage_providers import register_storage_providers


class MediaService:
    """Serviço de upload e biblioteca de mídia."""

    def __init__(self, media_repo: IMediaRepository) -> None:
        self._media = media_repo
        register_storage_providers()

    async def upload(
        self, tenant_id: str, file_data: bytes, filename: str,
        mime_type: str, uploaded_by: str | None = None,
        media_type: str = "gallery",
    ) -> MediaAsset:
        """Pipeline completo de upload."""

        # 1. Validate
        valid, error = ImageProcessor.validate(filename, mime_type, len(file_data))
        if not valid:
            raise BusinessRuleError(message=error)

        # 2. Compute hash (anti-duplicata)
        content_hash = ImageProcessor.compute_hash(file_data)

        # 3. Check duplicate
        existing = await self._media.get_by_hash(tenant_id, content_hash)
        if existing:
            return existing  # Já existe — retorna existente

        # 4. Generate unique filename
        safe_filename = ImageProcessor.generate_filename(filename, content_hash)

        # 5. Process image (resize, strip EXIF, etc.)
        meta = ImageProcessor.process_image(file_data, safe_filename) if mime_type.startswith("image/") else {}

        # 6. Upload to storage provider
        storage_path = ImageProcessor.get_tenant_path(tenant_id, safe_filename)
        provider = self._get_storage_provider()
        url = await provider.upload(file_data, storage_path, mime_type)

        # 7. Create media asset
        asset = MediaAsset(
            id=str(uuid4()), tenant_id=tenant_id,
            filename=safe_filename, original_name=filename,
            mime_type=mime_type, size_bytes=len(file_data),
            url=url, content_hash=content_hash,
            media_type=media_type,
            width=meta.get("width"), height=meta.get("height"),
            uploaded_by=uploaded_by,
            metadata={"processor_version": "1.0"},
        )
        return await self._media.create(asset)

    async def get_asset(self, asset_id: str) -> MediaAsset:
        a = await self._media.get_by_id(asset_id)
        if a is None:
            raise NotFoundError(message="Arquivo não encontrado.")
        return a

    async def list_assets(self, tenant_id: str, *, media_type: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[MediaAsset], int]:
        return await self._media.list_by_tenant(tenant_id, media_type=media_type, offset=offset, limit=limit)

    async def update_asset(self, asset_id: str, **kwargs: object) -> MediaAsset:
        a = await self.get_asset(asset_id)
        for k, v in kwargs.items():
            if hasattr(a, k) and v is not None:
                setattr(a, k, v)
        return await self._media.update(a)

    async def delete_asset(self, asset_id: str) -> None:
        await self._media.soft_delete(asset_id)

    def _get_storage_provider(self, provider_name: str = "local") -> StorageProvider:
        return StorageProviderFactory.create(provider_name)


class CMSService:
    """Serviço de CMS — páginas compostas de blocos."""

    def __init__(self, cms_repo: ICMSPageRepository) -> None:
        self._cms = cms_repo

    async def get_page(self, tenant_id: str, slug: str) -> CMSPage:
        page = await self._cms.get_by_slug(tenant_id, slug)
        if page is None:
            raise NotFoundError(message="Página não encontrada.")
        return page

    async def list_pages(self, tenant_id: str) -> list[CMSPage]:
        return await self._cms.list_by_tenant(tenant_id)

    async def upsert_page(self, tenant_id: str, slug: str, **kwargs: object) -> CMSPage:
        existing = await self._cms.get_by_slug(tenant_id, slug)
        page = existing or CMSPage(id=str(uuid4()), tenant_id=tenant_id, slug=slug)

        if "title" in kwargs:
            page.title = str(kwargs["title"])
        if "blocks" in kwargs:
            blocks_data = kwargs["blocks"]
            if isinstance(blocks_data, list):
                page.blocks = [
                    CMSBlock(**b) if isinstance(b, dict) else b
                    for b in blocks_data
                ]
        for field in ("meta_title", "meta_description", "meta_keywords", "og_image_url", "is_published"):
            if field in kwargs:
                setattr(page, field, kwargs[field])

        return await self._cms.upsert(page)

    def analyze_seo(self, page: CMSPage) -> dict[str, Any]:
        """SEO Score Analyzer — analisa página e sugere melhorias."""
        score = 100
        suggestions: list[str] = []

        if not page.meta_title:
            score -= 20
            suggestions.append("Meta título ausente.")
        elif len(page.meta_title) < 10:
            score -= 5
            suggestions.append("Meta título muito curto (mín. 10 caracteres).")
        elif len(page.meta_title) > 70:
            score -= 5
            suggestions.append("Meta título muito longo (máx. 70 caracteres).")

        if not page.meta_description:
            score -= 20
            suggestions.append("Meta descrição ausente.")
        elif len(page.meta_description) < 50:
            score -= 5
            suggestions.append("Meta descrição muito curta (mín. 50 caracteres).")
        elif len(page.meta_description) > 160:
            score -= 5
            suggestions.append("Meta descrição muito longa (máx. 160 caracteres).")

        if not page.og_image_url:
            score -= 10
            suggestions.append("Imagem Open Graph ausente.")

        has_h1 = any(b.block_type == "hero" for b in page.blocks)
        if not has_h1:
            score -= 10
            suggestions.append("Página sem bloco Hero (H1).")

        return {
            "score": max(0, score),
            "suggestions": suggestions,
            "checks": {
                "meta_title": bool(page.meta_title),
                "meta_description": bool(page.meta_description),
                "og_image": bool(page.og_image_url),
                "has_h1": has_h1,
            },
        }
