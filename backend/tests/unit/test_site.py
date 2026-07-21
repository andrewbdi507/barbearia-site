"""Site Module — Tests."""

import pytest

from app.modules.site.domain.entities import SEOSettings, SiteContent, SitePage
from app.modules.site.application.site_service import SiteService


class TestCSSVariableGenerator:
    def test_generates_colors(self) -> None:
        branding = {
            "primary_color": "#ff0000",
            "secondary_color": "#00ff00",
            "heading_font": "Roboto",
            "body_font": "Open Sans",
            "border_radius": "12px",
            "logo_url": "https://cdn.example.com/logo.png",
        }
        vars_ = SiteService.generate_css_variables(branding)
        assert vars_["--color-primary"] == "#ff0000"
        assert vars_["--color-secondary"] == "#00ff00"
        assert vars_["--font-heading"] == "'Roboto', sans-serif"
        assert vars_["--border-radius"] == "12px"
        assert "--logo-url" in vars_

    def test_defaults(self) -> None:
        vars_ = SiteService.generate_css_variables({})
        assert vars_["--color-primary"] == "#1a1a2e"
        assert vars_["--color-secondary"] == "#e94560"


class TestSEOGenerator:
    def test_generates_metadata(self) -> None:
        tenant = {"name": "Studio 27"}
        branding = {"banner_url": "https://cdn.example.com/banner.jpg"}
        seo = SEOSettings(
            id="s1", tenant_id="t1",
            meta_title="Studio 27 — Barbearia Premium",
            meta_description="A melhor barbearia de São Paulo.",
            google_analytics_id="UA-123",
        )
        meta = SiteService.generate_seo_metadata(tenant, branding, seo)
        assert meta["title"] == "Studio 27 — Barbearia Premium"
        assert meta["og"]["title"] == "Studio 27 — Barbearia Premium"
        assert meta["analytics"]["google"] == "UA-123"

    def test_defaults_when_no_seo(self) -> None:
        tenant = {"name": "Barbearia Teste"}
        meta = SiteService.generate_seo_metadata(tenant, {}, None)
        assert "Barbearia Teste" in meta["title"]


class TestJSONLDGenerator:
    def test_generates_local_business(self) -> None:
        tenant = {"name": "Studio 27", "subdomain": "studio27"}
        branding = {"logo_url": "https://cdn.example.com/logo.png", "phone": "11999999999"}
        ld = SiteService.generate_json_ld(tenant, branding)
        assert ld["@type"] == "LocalBusiness"
        assert ld["name"] == "Studio 27"
        assert "studio27.barbeariaos.com.br" in ld["url"]


class TestSitePage:
    def test_create_page(self) -> None:
        p = SitePage(id="p1", tenant_id="t1", slug="about", title="Sobre Nós", content="# Sobre")
        assert p.slug == "about"
        assert p.version == 1

    def test_published(self) -> None:
        from datetime import datetime, timezone
        p = SitePage(id="p1", tenant_id="t1", slug="privacy", is_published=True,
                     published_at=datetime.now(timezone.utc))
        assert p.is_published


class TestDTOs:
    def test_page_update(self) -> None:
        from app.modules.site.application.dto import PageUpdateRequest
        req = PageUpdateRequest(
            slug="about", title="Sobre Nós", content="## Quem somos",
            meta_title="Sobre — Studio 27", is_published=True,
        )
        assert req.slug == "about"

    def test_seo_update(self) -> None:
        from app.modules.site.application.dto import SEOUpdateRequest
        req = SEOUpdateRequest(
            meta_title="Studio 27 — Barbearia",
            google_analytics_id="G-XXXXXXXXXX",
        )
        assert req.google_analytics_id == "G-XXXXXXXXXX"
