"""Site Module — Repository."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.site.domain.entities import SEOSettings, SiteContent, SitePage
from app.modules.site.domain.interfaces import ISEORepository, ISiteContentRepository, ISitePageRepository
from app.modules.site.infrastructure.models.site_models import SEOSettingsModel, SiteContentModel, SitePageModel


def _page_to_entity(m: SitePageModel) -> SitePage:
    return SitePage(
        id=m.id, tenant_id=m.tenant_id or "", slug=m.slug,
        title=m.title, content=m.content,
        meta_title=m.meta_title, meta_description=m.meta_description,
        is_published=m.is_published, version=m.version,
        published_at=m.published_at, created_at=m.created_at, updated_at=m.updated_at,
    )


def _seo_to_entity(m: SEOSettingsModel) -> SEOSettings:
    return SEOSettings(
        id=m.id, tenant_id=m.tenant_id or "",
        meta_title=m.meta_title, meta_description=m.meta_description,
        meta_keywords=m.meta_keywords, og_image_url=m.og_image_url,
        twitter_handle=m.twitter_handle,
        google_analytics_id=m.google_analytics_id,
        facebook_pixel_id=m.facebook_pixel_id,
        custom_header_code=m.custom_header_code,
        custom_footer_code=m.custom_footer_code,
        robots_txt=m.robots_txt, canonical_url=m.canonical_url,
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _content_to_entity(m: SiteContentModel) -> SiteContent:
    return SiteContent(
        id=m.id, tenant_id=m.tenant_id or "",
        hero_title=m.hero_title, hero_subtitle=m.hero_subtitle,
        hero_cta_text=m.hero_cta_text, hero_banner_url=m.hero_banner_url,
        hero_video_url=m.hero_video_url,
        about_title=m.about_title, about_text=m.about_text,
        promotions=m.promotions or [], highlights=m.highlights or [],
        show_services=m.show_services, show_team=m.show_team,
        show_reviews=m.show_reviews, show_gallery=m.show_gallery,
        metadata=m.metadata or {}, created_at=m.created_at, updated_at=m.updated_at,
    )


class SitePageRepository(ISitePageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_slug(self, tenant_id: str, slug: str) -> SitePage | None:
        r = await self._s.execute(
            select(SitePageModel).where(
                SitePageModel.tenant_id == tenant_id, SitePageModel.slug == slug,
            )
        )
        m = r.scalar_one_or_none()
        return _page_to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str) -> list[SitePage]:
        r = await self._s.execute(
            select(SitePageModel).where(SitePageModel.tenant_id == tenant_id)
        )
        return [_page_to_entity(m) for m in r.scalars().all()]

    async def upsert(self, page: SitePage) -> SitePage:
        r = await self._s.execute(
            select(SitePageModel).where(
                SitePageModel.tenant_id == page.tenant_id, SitePageModel.slug == page.slug,
            )
        )
        m = r.scalar_one_or_none()
        if m:
            m.title = page.title
            m.content = page.content
            m.meta_title = page.meta_title
            m.meta_description = page.meta_description
            m.is_published = page.is_published
            m.version = page.version + 1
            m.published_at = datetime.now(timezone.utc) if page.is_published else None
            m.updated_at = datetime.now(timezone.utc)
        else:
            m = SitePageModel(
                id=page.id, tenant_id=page.tenant_id, slug=page.slug,
                title=page.title, content=page.content,
                meta_title=page.meta_title, meta_description=page.meta_description,
                is_published=page.is_published, version=1,
            )
            self._s.add(m)
        await self._s.flush()
        return _page_to_entity(m)


class SEORepository(ISEORepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_tenant(self, tenant_id: str) -> SEOSettings | None:
        r = await self._s.execute(
            select(SEOSettingsModel).where(SEOSettingsModel.tenant_id == tenant_id)
        )
        m = r.scalar_one_or_none()
        return _seo_to_entity(m) if m else None

    async def upsert(self, seo: SEOSettings) -> SEOSettings:
        r = await self._s.execute(
            select(SEOSettingsModel).where(SEOSettingsModel.tenant_id == seo.tenant_id)
        )
        m = r.scalar_one_or_none()
        if m:
            for f in ("meta_title", "meta_description", "meta_keywords", "og_image_url",
                       "twitter_handle", "google_analytics_id", "facebook_pixel_id",
                       "custom_header_code", "custom_footer_code", "robots_txt", "canonical_url"):
                setattr(m, f, getattr(seo, f))
            m.updated_at = datetime.now(timezone.utc)
        else:
            m = SEOSettingsModel(
                id=seo.id, tenant_id=seo.tenant_id,
                meta_title=seo.meta_title, meta_description=seo.meta_description,
                meta_keywords=seo.meta_keywords, og_image_url=seo.og_image_url,
                twitter_handle=seo.twitter_handle,
                google_analytics_id=seo.google_analytics_id,
                facebook_pixel_id=seo.facebook_pixel_id,
                custom_header_code=seo.custom_header_code,
                custom_footer_code=seo.custom_footer_code,
                robots_txt=seo.robots_txt, canonical_url=seo.canonical_url,
            )
            self._s.add(m)
        await self._s.flush()
        return seo


class SiteContentRepository(ISiteContentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_tenant(self, tenant_id: str) -> SiteContent | None:
        r = await self._s.execute(
            select(SiteContentModel).where(SiteContentModel.tenant_id == tenant_id)
        )
        m = r.scalar_one_or_none()
        return _content_to_entity(m) if m else None

    async def upsert(self, content: SiteContent) -> SiteContent:
        r = await self._s.execute(
            select(SiteContentModel).where(SiteContentModel.tenant_id == content.tenant_id)
        )
        m = r.scalar_one_or_none()
        if m:
            for f in ("hero_title", "hero_subtitle", "hero_cta_text", "hero_banner_url",
                       "hero_video_url", "about_title", "about_text", "promotions",
                       "highlights", "show_services", "show_team", "show_reviews",
                       "show_gallery", "metadata"):
                setattr(m, f, getattr(content, f))
            m.updated_at = datetime.now(timezone.utc)
        else:
            m = SiteContentModel(
                id=content.id, tenant_id=content.tenant_id,
                hero_title=content.hero_title, hero_subtitle=content.hero_subtitle,
                hero_cta_text=content.hero_cta_text,
                hero_banner_url=content.hero_banner_url,
                about_title=content.about_title, about_text=content.about_text,
            )
            self._s.add(m)
        await self._s.flush()
        return content
