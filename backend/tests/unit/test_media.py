"""Media Module — Tests."""

import hashlib
import pytest

from app.modules.media.domain.entities import MediaAsset, CMSPage, CMSBlock
from app.modules.media.domain.interfaces import StorageProviderFactory
from app.modules.media.infrastructure.image_processor import ImageProcessor
from app.modules.media.infrastructure.storage_providers import register_storage_providers


class TestImageProcessor:
    def test_validate_jpeg(self) -> None:
        ok, err = ImageProcessor.validate("foto.jpg", "image/jpeg", 50000)
        assert ok

    def test_validate_invalid_ext(self) -> None:
        ok, err = ImageProcessor.validate("virus.exe", "application/x-msdownload", 100)
        assert not ok

    def test_validate_oversized(self) -> None:
        ok, err = ImageProcessor.validate("big.jpg", "image/jpeg", 20 * 1024 * 1024)
        assert not ok

    def test_validate_invalid_mime(self) -> None:
        ok, err = ImageProcessor.validate("foto.jpg", "text/html", 1000)
        assert not ok

    def test_compute_hash(self) -> None:
        h1 = ImageProcessor.compute_hash(b"hello")
        h2 = ImageProcessor.compute_hash(b"hello")
        assert h1 == h2
        assert len(h1) == 64  # SHA-256

    def test_generate_filename(self) -> None:
        name = ImageProcessor.generate_filename("Minha Foto.JPG", "abc123def456")
        assert name == "abc123def456.jpg"
        assert name.islower()

    def test_tenant_path(self) -> None:
        path = ImageProcessor.get_tenant_path("t_abc123", "logo.png")
        assert path == "t_abc123/logo.png"


class TestStorageProviders:
    def test_factory_register(self) -> None:
        register_storage_providers()
        p = StorageProviderFactory.create("local")
        assert p is not None

    def test_factory_s3(self) -> None:
        register_storage_providers()
        p = StorageProviderFactory.create("s3", bucket="my-bucket")
        assert p is not None

    def test_factory_r2(self) -> None:
        register_storage_providers()
        p = StorageProviderFactory.create("r2", bucket="my-bucket", account_id="abc")
        assert p is not None

    @pytest.mark.asyncio
    async def test_local_upload(self) -> None:
        register_storage_providers()
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            p = StorageProviderFactory.create("local", base_path=tmp)
            url = await p.upload(b"hello world", "test/file.txt", "text/plain")
            assert url.startswith("/media/")
            exists = await p.exists("test/file.txt")
            assert exists


class TestMediaAsset:
    def test_create_asset(self) -> None:
        a = MediaAsset(
            id="m1", tenant_id="t1", filename="abc.jpg",
            original_name="Minha Foto.jpg", content_hash="sha256...",
            url="/media/t1/abc.jpg",
        )
        assert a.media_type == "gallery"
        assert a.is_visible


class TestCMSPage:
    def test_page_with_blocks(self) -> None:
        blocks = [
            CMSBlock(block_type="hero", data={"title": "Bem-vindo"}, order=0),
            CMSBlock(block_type="text", data={"content": "Texto"}, order=1),
        ]
        page = CMSPage(id="p1", tenant_id="t1", slug="home", title="Home", blocks=blocks)
        assert len(page.blocks) == 2
        assert page.blocks[0].block_type == "hero"


class TestSEOAnalyzer:
    def test_perfect_score(self) -> None:
        from app.modules.media.application.media_service import CMSService
        svc = CMSService(None)  # type: ignore
        page = CMSPage(
            id="p1", tenant_id="t1", slug="home", title="Home",
            meta_title="Barbearia Premium — Agende Online (ótimo título)",
            meta_description="A melhor barbearia da cidade com agendamento online rápido e prático. Venha nos visitar!",
            og_image_url="https://cdn.example.com/og.jpg",
            blocks=[CMSBlock(block_type="hero", data={"title": "Hero"})],
        )
        result = svc.analyze_seo(page)
        assert result["score"] >= 80

    def test_missing_everything(self) -> None:
        from app.modules.media.application.media_service import CMSService
        svc = CMSService(None)  # type: ignore
        page = CMSPage(id="p1", tenant_id="t1", slug="home")
        result = svc.analyze_seo(page)
        assert result["score"] <= 50
        assert len(result["suggestions"]) >= 3
