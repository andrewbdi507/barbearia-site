"""Site Module — DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PageUpdateRequest(BaseModel):
    slug: str = Field(..., min_length=2, max_length=100)
    title: str = ""
    content: str = ""
    meta_title: str = ""
    meta_description: str = ""
    is_published: bool = False


class PageResponse(BaseModel):
    slug: str
    title: str
    content: str
    meta_title: str
    meta_description: str
    is_published: bool
    version: int


class SEOUpdateRequest(BaseModel):
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: str | None = None
    og_image_url: str | None = None
    twitter_handle: str | None = None
    google_analytics_id: str | None = None
    facebook_pixel_id: str | None = None
    custom_header_code: str | None = None
    custom_footer_code: str | None = None
    robots_txt: str | None = None
    canonical_url: str | None = None


class SEOResponse(BaseModel):
    meta_title: str
    meta_description: str
    meta_keywords: str
    og_image_url: str | None = None
    google_analytics_id: str | None = None
    facebook_pixel_id: str | None = None
    robots_txt: str


class SiteContentUpdateRequest(BaseModel):
    hero_title: str | None = None
    hero_subtitle: str | None = None
    hero_cta_text: str | None = None
    hero_banner_url: str | None = None
    about_title: str | None = None
    about_text: str | None = None
    promotions: list[dict[str, Any]] | None = None
    highlights: list[str] | None = None
    show_services: bool | None = None
    show_team: bool | None = None
    show_reviews: bool | None = None
    show_gallery: bool | None = None


class SiteContentResponse(BaseModel):
    hero_title: str
    hero_subtitle: str
    hero_cta_text: str
    hero_banner_url: str | None = None
    about_title: str
    about_text: str
    promotions: list[dict[str, Any]]
    highlights: list[str]
    show_services: bool
    show_team: bool
    show_reviews: bool
    show_gallery: bool
