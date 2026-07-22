"""Site Module — Public & Admin API Routes.

Rotas PÚBLICAS (sem auth):
- GET /site — dados agregados do site (branding, serviços, equipe, etc.)
- GET /site/pages/{slug} — páginas de conteúdo (sobre, privacidade, termos)

Rotas ADMIN (com auth):
- CRUD de páginas, SEO, conteúdo da home
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.site.application.dto import (
    PageResponse,
    PageUpdateRequest,
    SEOUpdateRequest,
    SiteContentResponse,
    SiteContentUpdateRequest,
)
from app.modules.site.application.site_service import SiteService
from app.modules.site.infrastructure.repository import (
    SEORepository,
    SiteContentRepository,
    SitePageRepository,
)
from app.modules.tenant.infrastructure.repository import TenantRepository
from app.modules.tenant.presentation.dependencies import get_current_tenant

# Router público — sem auth
public_router = APIRouter(prefix="/site", tags=["Site Público"])

# Router admin — com auth
admin_router = APIRouter(prefix="/admin/site", tags=["Site Admin"])


def _get_service(session: AsyncSession) -> SiteService:
    return SiteService(
        page_repo=SitePageRepository(session),
        seo_repo=SEORepository(session),
        content_repo=SiteContentRepository(session),
    )


# ============================================================
# PUBLIC API — GET /site
# ============================================================

@public_router.get("")
async def get_site(
    session: AsyncSession = Depends(get_async_session),
    subdomain: str | None = Query(default=None, description="Subdomínio do tenant"),
    tenant_id: str | None = Query(default=None, description="ID direto do tenant"),
) -> dict:
    """Endpoint público principal do site.

    Retorna TODOS os dados necessários para renderizar o site:
    branding, CSS vars, SEO, JSON-LD, serviços, equipe, reviews, etc.

    Resolve tenant por subdomínio ou tenant_id direto.
    """
    if subdomain:
        tenant_repo = TenantRepository(session)
        tenant = await tenant_repo.get_by_subdomain(subdomain.lower())
        if tenant is None:
            from app.core.exceptions import TenantNotFoundError
            raise TenantNotFoundError()
        tid = tenant.id
    elif tenant_id:
        tid = tenant_id
    else:
        from app.core.exceptions import TenantNotFoundError
        raise TenantNotFoundError(message="Forneça subdomain ou tenant_id.")

    # Buscar dados dos módulos
    tenant_repo = TenantRepository(session)
    tenant = await tenant_repo.get_by_id(tid)
    if tenant is None:
        from app.core.exceptions import TenantNotFoundError
        raise TenantNotFoundError()

    # Buscar serviços, staff, reviews dos módulos
    from app.modules.scheduling.infrastructure.repository import ServiceRepository
    from app.modules.staff.infrastructure.repository import StaffRepository
    from app.modules.customer.infrastructure.repository import ReviewRepository

    svc_repo = ServiceRepository(session)
    staff_repo = StaffRepository(session)
    review_repo = ReviewRepository(session)

    services = await svc_repo.list_by_tenant(tid, active_only=True)
    staff_list, _ = await staff_repo.list_by_tenant(tid, status="active")
    reviews_list, _ = await review_repo.list_for_tenant(tid, visible_only=True)

    site_svc = _get_service(session)

    tenant_data = {
        "id": tenant.id,
        "name": tenant.name,
        "subdomain": tenant.subdomain.value,
        "status": tenant.status,
    }

    branding = {}
    if tenant.branding:
        branding = {
            "theme": getattr(tenant.branding, "theme", None) or "urban",
            "logo_url": tenant.branding.logo_url,
            "logo_dark_url": tenant.branding.logo_dark_url,
            "favicon_url": tenant.branding.favicon_url,
            "banner_url": tenant.branding.banner_url,
            "primary_color": tenant.branding.primary_color,
            "secondary_color": tenant.branding.secondary_color,
            "background_color": tenant.branding.background_color,
            "surface_color": tenant.branding.surface_color,
            "text_color": tenant.branding.text_color,
            "text_light_color": tenant.branding.text_light_color,
            "heading_font": tenant.branding.heading_font,
            "body_font": tenant.branding.body_font,
            "base_font_size": tenant.branding.base_font_size,
            "border_radius": tenant.branding.border_radius,
        }

    bh_data = [
        {"day_of_week": bh.day_of_week, "is_closed": bh.is_closed,
         "open_time": bh.open_time, "close_time": bh.close_time}
        for bh in tenant.business_hours
    ]

    sm_data = [
        {"platform": sm.platform, "url": sm.url, "is_visible": sm.is_visible}
        for sm in tenant.social_media
    ]

    result = await site_svc.get_site_data(
        tid, tenant_data, branding,
        services=[{"id": s.id, "name": s.name, "description": s.description,
                    "base_price": s.base_price, "effective_price": s.effective_price,
                    "duration_minutes": s.duration_minutes, "color_tag": s.color_tag}
                   for s in services],
        staff=[{"id": s.id, "professional_name": s.professional_name,
                 "photo_url": s.photo_url, "bio": s.bio,
                 "specialties": s.specialties, "experience_years": s.experience_years}
                for s in staff_list],
        reviews=[{"id": r.id, "rating": r.rating, "comment": r.comment,
                   "tags": r.tags, "is_anonymous": r.is_anonymous,
                   "business_response": r.business_response,
                   "created_at": r.created_at.isoformat() if r.created_at else None}
                  for r in reviews_list],
        business_hours=bh_data,
        social_media=sm_data,
    )

    return result


# ============================================================
# PUBLIC API — Content Pages
# ============================================================

@public_router.get("/pages/{slug}")
async def get_page(
    slug: str,
    session: AsyncSession = Depends(get_async_session),
    tenant_id: str = Query(..., description="ID do tenant"),
) -> PageResponse:
    svc = _get_service(session)
    page = await svc.get_page(tenant_id, slug)
    return PageResponse(**page.__dict__)


# ============================================================
# PUBLIC API — Sitemap
# ============================================================

@public_router.get("/sitemap.xml")
async def get_sitemap(
    session: AsyncSession = Depends(get_async_session),
    tenant_id: str = Query(..., description="ID do tenant"),
) -> str:
    from fastapi.responses import PlainTextResponse
    tenant_repo = TenantRepository(session)
    tenant = await tenant_repo.get_by_id(tenant_id)
    if tenant is None:
        return PlainTextResponse("", status_code=404)

    svc = _get_service(session)
    pages = await svc.list_pages(tenant_id)

    base = f"https://{tenant.subdomain.value}.barbeariaos.com.br"
    urls = [
        f"  <url><loc>{base}</loc><priority>1.0</priority></url>",
        f"  <url><loc>{base}/servicos</loc><priority>0.8</priority></url>",
        f"  <url><loc>{base}/equipe</loc><priority>0.7</priority></url>",
    ]
    for p in pages:
        if p.is_published:
            urls.append(f"  <url><loc>{base}/{p.slug}</loc><priority>0.5</priority></url>")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>"
    return PlainTextResponse(xml, media_type="application/xml")


# ============================================================
# ADMIN API — Pages
# ============================================================

@admin_router.get("/pages", response_model=list[PageResponse])
async def admin_list_pages(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[PageResponse]:
    svc = _get_service(session)
    pages = await svc.list_pages(tenant["id"])
    return [PageResponse(**p.__dict__) for p in pages]


@admin_router.put("/pages", response_model=PageResponse)
async def admin_upsert_page(
    body: PageUpdateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> PageResponse:
    svc = _get_service(session)
    p = await svc.upsert_page(tenant["id"], **body.model_dump())
    return PageResponse(**p.__dict__)


# ============================================================
# ADMIN API — SEO
# ============================================================

@admin_router.get("/seo")
async def admin_get_seo(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    seo = await svc.get_seo(tenant["id"])
    if seo is None:
        return {"meta_title": "", "meta_description": "", "meta_keywords": ""}
    return seo.__dict__


@admin_router.put("/seo")
async def admin_update_seo(
    body: SEOUpdateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    seo = await svc.update_seo(tenant["id"], **body.model_dump(exclude_none=True))
    return seo.__dict__


# ============================================================
# ADMIN API — Site Content
# ============================================================

@admin_router.get("/content", response_model=SiteContentResponse)
async def admin_get_content(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> SiteContentResponse:
    svc = _get_service(session)
    c = await svc.get_content(tenant["id"])
    return SiteContentResponse(**c.__dict__)


@admin_router.put("/content", response_model=SiteContentResponse)
async def admin_update_content(
    body: SiteContentUpdateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> SiteContentResponse:
    svc = _get_service(session)
    c = await svc.update_content(tenant["id"], **body.model_dump(exclude_none=True))
    return SiteContentResponse(**c.__dict__)
