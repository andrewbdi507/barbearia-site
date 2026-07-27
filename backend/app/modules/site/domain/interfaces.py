"""Site Module — Repository Interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.site.domain.entities import FAQItem, SEOSettings, SiteContent, SitePage


class ISitePageRepository(ABC):
    @abstractmethod
    async def get_by_slug(self, tenant_id: str, slug: str) -> SitePage | None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[SitePage]: ...
    @abstractmethod
    async def upsert(self, page: SitePage) -> SitePage: ...


class ISEORepository(ABC):
    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> SEOSettings | None: ...
    @abstractmethod
    async def upsert(self, seo: SEOSettings) -> SEOSettings: ...


class ISiteContentRepository(ABC):
    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> SiteContent | None: ...
    @abstractmethod
    async def upsert(self, content: SiteContent) -> SiteContent: ...


class IFAQRepository(ABC):
    @abstractmethod
    async def list_for_tenant(self, tenant_id: str) -> list[FAQItem]: ...
    @abstractmethod
    async def upsert(self, faq: FAQItem) -> FAQItem: ...
    @abstractmethod
    async def delete(self, faq_id: str) -> None: ...
