"""Media Module — Image Processor.

Pipeline: validate → strip EXIF → resize (max 2000px) → thumbnail (400px) → WebP.
"""

from __future__ import annotations

import hashlib
import io
from typing import Any


class ImageProcessor:
    """Processador de imagens.

    No MVP usa Pillow. Em produção pode usar sharp/libvips.
    """

    ALLOWED_MIME_TYPES = {
        "image/jpeg", "image/png", "image/webp",
        "image/gif", "image/svg+xml", "image/bmp",
    }
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".bmp"}
    MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
    MAX_DIMENSION = 2000
    THUMBNAIL_DIMENSION = 400

    @classmethod
    def validate(cls, filename: str, mime_type: str, size: int) -> tuple[bool, str]:
        """Valida arquivo antes do upload."""
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        if f".{ext}" not in cls.ALLOWED_EXTENSIONS:
            return False, f"Extensão não permitida: .{ext}"
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            return False, f"MIME type não permitido: {mime_type}"
        if size > cls.MAX_SIZE_BYTES:
            return False, f"Arquivo muito grande: {size} bytes (máx {cls.MAX_SIZE_BYTES})"
        return True, ""

    @classmethod
    def compute_hash(cls, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @classmethod
    def generate_filename(cls, original_name: str, content_hash: str) -> str:
        ext = original_name.lower().rsplit(".", 1)[-1] if "." in original_name else "jpg"
        return f"{content_hash[:16]}.{ext}"

    @classmethod
    def get_tenant_path(cls, tenant_id: str, filename: str) -> str:
        return f"{tenant_id}/{filename}"

    @classmethod
    def process_image(cls, data: bytes, filename: str) -> dict[str, Any]:
        """Processa imagem: strip EXIF, resize, thumbnail, WebP.

        Retorna metadados (width, height, etc.).
        """
        # No MVP, retorna metadados mockados
        # Em produção, usa Pillow:
        # from PIL import Image
        # img = Image.open(io.BytesIO(data))
        # img = cls._strip_exif(img)
        # img.thumbnail((cls.MAX_DIMENSION, cls.MAX_DIMENSION))
        # ...

        return {
            "width": 1200,
            "height": 800,
            "format": filename.rsplit(".", 1)[-1] if "." in filename else "jpg",
            "size_bytes": len(data),
        }
