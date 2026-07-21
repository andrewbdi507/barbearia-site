"""Media Module — API Routes.

Upload, Media Library, CMS pages, SEO analysis.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.media.application.media_service import CMSService, MediaService
from app.modules.media.infrastructure.repository import CMSPageRepository, MediaRepository
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/media", tags=["Media & CMS"])


def _media_svc(session: AsyncSession) -> MediaService:
    return MediaService(MediaRepository(session))


def _cms_svc(session: AsyncSession) -> CMSService:
    return CMSService(CMSPageRepository(session))


# ============================================================
# UPLOAD
# ============================================================

@router.post("/upload")
async def upload_file(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(...),
    media_type: str = Form(default="gallery"),
) -> dict:
    svc = _media_svc(session)
    file_data = await file.read()
    asset = await svc.upload(
        tenant["id"], file_data,
        filename=file.filename or "unknown",
        mime_type=file.content_type or "application/octet-stream",
        media_type=media_type,
    )
    return {
        "id": asset.id, "url": asset.url, "filename": asset.filename,
        "size_bytes": asset.size_bytes, "content_hash": asset.content_hash,
        "width": asset.width, "height": asset.height,
    }


# ============================================================
# MEDIA LIBRARY
# ============================================================

@router.get("/library")
async def list_media(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    media_type: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict:
    svc = _media_svc(session)
    items, total = await svc.list_assets(tenant["id"], media_type=media_type, offset=offset, limit=limit)
    return {
        "items": [
            {"id": a.id, "url": a.url, "filename": a.filename, "original_name": a.original_name,
             "mime_type": a.mime_type, "size_bytes": a.size_bytes, "media_type": a.media_type,
             "width": a.width, "height": a.height, "created_at": a.created_at.isoformat() if a.created_at else None}
            for a in items
        ],
        "total": total, "offset": offset, "limit": limit,
    }


@router.get("/library/{asset_id}")
async def get_media(
    asset_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _media_svc(session)
    a = await svc.get_asset(asset_id)
    return {"id": a.id, "url": a.url, "filename": a.filename, "media_type": a.media_type}


@router.patch("/library/{asset_id}")
async def update_media(
    asset_id: str,
    body: dict,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _media_svc(session)
    a = await svc.update_asset(asset_id, **body)
    return {"id": a.id, "title": a.title, "alt_text": a.alt_text}


@router.delete("/library/{asset_id}")
async def delete_media(
    asset_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _media_svc(session)
    await svc.delete_asset(asset_id)
    return {"message": "Arquivo removido."}


# ============================================================
# CMS PAGES
# ============================================================

@router.get("/cms/pages")
async def list_cms_pages(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _cms_svc(session)
    pages = await svc.list_pages(tenant["id"])
    return [{"slug": p.slug, "title": p.title, "is_published": p.is_published, "version": p.version} for p in pages]


@router.get("/cms/pages/{slug}")
async def get_cms_page(
    slug: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _cms_svc(session)
    page = await svc.get_page(tenant["id"], slug)
    return {
        "slug": page.slug, "title": page.title,
        "blocks": [b.__dict__ for b in page.blocks],
        "meta_title": page.meta_title, "meta_description": page.meta_description,
        "og_image_url": page.og_image_url, "is_published": page.is_published,
        "version": page.version,
    }


@router.put("/cms/pages/{slug}")
async def upsert_cms_page(
    slug: str,
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _cms_svc(session)
    page = await svc.upsert_page(tenant["id"], slug, **body)
    return {"slug": page.slug, "title": page.title, "is_published": page.is_published, "version": page.version}


# ============================================================
# SEO ANALYSIS
# ============================================================

@router.get("/cms/pages/{slug}/seo-analysis")
async def analyze_seo(
    slug: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _cms_svc(session)
    page = await svc.get_page(tenant["id"], slug)
    return svc.analyze_seo(page)
