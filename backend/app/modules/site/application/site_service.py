"""Site Module — Site Service.

Serviço que agrega dados de TODOS os módulos para o site público.
SiteResolver: subdomínio → tenant → todos os dados do site.
CSS Variable Generator: branding JSONB → CSS custom properties.
SEO Generator: dados do tenant → meta tags + JSON-LD.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.core.exceptions import NotFoundError
from app.modules.site.domain.entities import SEOSettings, SiteContent, SitePage
from app.modules.site.domain.interfaces import ISEORepository, ISiteContentRepository, ISitePageRepository


class SiteService:
    """Serviço do site público — agregador de dados multi-módulo.

    Responsável por:
    - Resolver todos os dados do site a partir do tenant_id
    - Gerar CSS custom properties do branding
    - Gerar meta tags SEO + JSON-LD Schema.org
    - Servir páginas de conteúdo (Sobre, Privacidade, Termos)
    - Gerenciar conteúdo editável da home
    """

    def __init__(
        self,
        page_repo: ISitePageRepository,
        seo_repo: ISEORepository,
        content_repo: ISiteContentRepository,
    ) -> None:
        self._pages = page_repo
        self._seo = seo_repo
        self._content = content_repo

    # ============================================================
    # Aggregated Site Data (GET /site)
    # ============================================================

    async def get_site_data(
        self,
        tenant_id: str,
        tenant_data: dict[str, Any],
        branding_data: dict[str, Any] | None,
        services: list[dict[str, Any]] | None = None,
        staff: list[dict[str, Any]] | None = None,
        reviews: list[dict[str, Any]] | None = None,
        business_hours: list[dict[str, Any]] | None = None,
        social_media: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Retorna TODOS os dados do site em uma única chamada.

        Esta é a API principal do frontend público.
        """
        content = await self._content.get_for_tenant(tenant_id)
        seo = await self._seo.get_for_tenant(tenant_id)
        pages = await self._pages.list_by_tenant(tenant_id)

        # Gerar CSS variables
        css_vars = self.generate_css_variables(branding_data or {})

        # Gerar SEO metadata
        seo_metadata = self.generate_seo_metadata(
            tenant_data, branding_data or {}, seo,
        )

        # Gerar JSON-LD Schema.org
        json_ld = self.generate_json_ld(tenant_data, branding_data or {})

        return {
            "tenant": {
                "id": tenant_data.get("id"),
                "name": tenant_data.get("name", ""),
                "subdomain": tenant_data.get("subdomain", ""),
                "status": tenant_data.get("status", ""),
            },
            "branding": branding_data or {},
            "css_variables": css_vars,
            "seo": seo_metadata,
            "json_ld": json_ld,
            "content": {
                "hero_title": content.hero_title if content else "",
                "hero_subtitle": content.hero_subtitle if content else "",
                "hero_cta_text": content.hero_cta_text if content else "Agende Agora",
                "hero_banner_url": content.hero_banner_url if content else None,
                "hero_video_url": content.hero_video_url if content else None,
                "about_title": content.about_title if content else "Sobre Nós",
                "about_text": content.about_text if content else "",
                "promotions": content.promotions if content else [],
                "highlights": content.highlights if content else [],
                "show_services": content.show_services if content else True,
                "show_team": content.show_team if content else True,
                "show_reviews": content.show_reviews if content else True,
                "show_gallery": content.show_gallery if content else True,
            },
            "services": services or [],
            "team": staff or [],
            "reviews": reviews or [],
            "business_hours": business_hours or [],
            "social_media": social_media or [],
            "pages": [
                {"slug": p.slug, "title": p.title, "is_published": p.is_published}
                for p in pages
            ],
        }

    # ============================================================
    # CSS Variable Generator
    # ============================================================

    @staticmethod
    def generate_css_variables(branding: dict[str, Any]) -> dict[str, str]:
        """Gera CSS custom properties do branding JSONB.

        Exemplo de saída:
        {
            "--color-primary": "#1a1a2e",
            "--color-primary-hover": "#16213e",
            "--color-secondary": "#e94560",
            "--font-heading": "Inter, sans-serif",
            "--font-body": "Inter, sans-serif",
            "--border-radius": "8px",
            "--logo-url": "url('https://...')",
        }
        """
        vars_: dict[str, str] = {
            "--color-primary": branding.get("primary_color", "#1a1a2e"),
            "--color-secondary": branding.get("secondary_color", "#e94560"),
            "--color-background": branding.get("background_color", "#f5f5f5"),
            "--color-surface": branding.get("surface_color", "#ffffff"),
            "--color-text": branding.get("text_color", "#333333"),
            "--color-text-light": branding.get("text_light_color", "#666666"),
            "--font-heading": f"'{branding.get('heading_font', 'Inter')}', sans-serif",
            "--font-body": f"'{branding.get('body_font', 'Inter')}', sans-serif",
            "--font-size-base": branding.get("base_font_size", "16px"),
            "--border-radius": branding.get("border_radius", "8px"),
        }

        logo = branding.get("logo_url")
        if logo:
            vars_["--logo-url"] = f"url('{logo}')"

        banner = branding.get("banner_url")
        if banner:
            vars_["--banner-url"] = f"url('{banner}')"

        return vars_

    # ============================================================
    # SEO Generator
    # ============================================================

    @staticmethod
    def generate_seo_metadata(
        tenant: dict[str, Any],
        branding: dict[str, Any],
        seo: SEOSettings | None,
    ) -> dict[str, Any]:
        """Gera meta tags SEO completas."""
        company_name = tenant.get("name", "")
        description = seo.meta_description if seo and seo.meta_description else f"{company_name} — Agende seu horário online."

        return {
            "title": seo.meta_title if seo and seo.meta_title else company_name,
            "description": description,
            "keywords": seo.meta_keywords if seo else "",
            "canonical": seo.canonical_url if seo else None,
            "robots": seo.robots_txt if seo else "index, follow",
            "og": {
                "title": seo.meta_title if seo and seo.meta_title else company_name,
                "description": description,
                "image": seo.og_image_url if seo else (branding.get("banner_url") or branding.get("logo_url")),
                "type": "website",
                "site_name": company_name,
            },
            "twitter": {
                "card": "summary_large_image",
                "title": seo.meta_title if seo and seo.meta_title else company_name,
                "description": description,
                "image": seo.og_image_url if seo else (branding.get("banner_url") or branding.get("logo_url")),
                "site": seo.twitter_handle if seo else None,
            },
            "analytics": {
                "google": seo.google_analytics_id if seo else None,
                "facebook": seo.facebook_pixel_id if seo else None,
            },
            "custom_header": seo.custom_header_code if seo else None,
            "custom_footer": seo.custom_footer_code if seo else None,
        }

    # ============================================================
    # JSON-LD Schema.org Generator
    # ============================================================

    @staticmethod
    def generate_json_ld(tenant: dict[str, Any], branding: dict[str, Any]) -> dict[str, Any]:
        """Gera JSON-LD Schema.org para LocalBusiness."""
        return {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": tenant.get("name", ""),
            "url": f"https://{tenant.get('subdomain', '')}.barbeariaos.com.br",
            "image": branding.get("logo_url", ""),
            "telephone": branding.get("phone", ""),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": branding.get("address", ""),
                "addressLocality": branding.get("city", ""),
                "addressRegion": branding.get("state", ""),
            },
        }

    # ============================================================
    # Content Pages
    # ============================================================

    async def get_page(self, tenant_id: str, slug: str) -> SitePage:
        page = await self._pages.get_by_slug(tenant_id, slug)
        if page is None or not page.is_published:
            raise NotFoundError(message="Página não encontrada.")
        return page

    async def list_pages(self, tenant_id: str) -> list[SitePage]:
        return await self._pages.list_by_tenant(tenant_id)

    async def upsert_page(self, tenant_id: str, **kwargs: object) -> SitePage:
        existing = await self._pages.get_by_slug(tenant_id, str(kwargs.get("slug", "")))
        page = existing or SitePage(id=str(uuid4()), tenant_id=tenant_id, slug=str(kwargs.get("slug", "")))

        for k, v in kwargs.items():
            if hasattr(page, k) and v is not None:
                setattr(page, k, v)

        return await self._pages.upsert(page)

    # ============================================================
    # SEO Settings
    # ============================================================

    async def get_seo(self, tenant_id: str) -> SEOSettings | None:
        return await self._seo.get_for_tenant(tenant_id)

    async def update_seo(self, tenant_id: str, **kwargs: object) -> SEOSettings:
        existing = await self._seo.get_for_tenant(tenant_id)
        seo = existing or SEOSettings(id=str(uuid4()), tenant_id=tenant_id)

        for k, v in kwargs.items():
            if hasattr(seo, k) and v is not None:
                setattr(seo, k, v)

        return await self._seo.upsert(seo)

    # ============================================================
    # Site Content (Home editing)
    # ============================================================

    async def get_content(self, tenant_id: str) -> SiteContent:
        content = await self._content.get_for_tenant(tenant_id)
        return content or SiteContent(id=str(uuid4()), tenant_id=tenant_id)

    async def update_content(self, tenant_id: str, **kwargs: object) -> SiteContent:
        existing = await self._content.get_for_tenant(tenant_id)
        content = existing or SiteContent(id=str(uuid4()), tenant_id=tenant_id)

        for k, v in kwargs.items():
            if hasattr(content, k) and v is not None:
                setattr(content, k, v)

        return await self._content.upsert(content)
