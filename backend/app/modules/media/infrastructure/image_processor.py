"""Media Module — Image Processor.

Pipeline: validate → strip EXIF → resize (max 2000px) → thumbnail (400px).
"""

from __future__ import annotations

import hashlib
import io
from typing import Any

from PIL import Image


class ImageProcessor:
    """Processador de imagens com Pillow."""

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
    def _strip_exif(cls, img: Image.Image) -> Image.Image:
        """Remove dados EXIF da imagem.

        Cria uma nova imagem sem metadados, preservando os pixels.
        """
        data = list(img.getdata())
        clean = Image.new(img.mode, img.size)
        clean.putdata(data)
        return clean

    @classmethod
    def _resize_proportional(cls, img: Image.Image, max_dimension: int) -> Image.Image:
        """Redimensiona mantendo proporção — lado maior ≤ max_dimension."""
        w, h = img.size
        if w <= max_dimension and h <= max_dimension:
            return img.copy()
        ratio = max_dimension / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        return img.resize(new_size, Image.LANCZOS)

    @classmethod
    def _to_bytes(cls, img: Image.Image, fmt: str) -> bytes:
        """Converte imagem PIL para bytes no formato original."""
        buf = io.BytesIO()
        save_fmt = "JPEG" if fmt.lower() in ("jpg", "jpeg") else fmt.upper()
        if save_fmt == "JPEG":
            img = img.convert("RGB")  # JPEG não suporta RGBA
        img.save(buf, format=save_fmt, quality=90, optimize=True)
        return buf.getvalue()

    @classmethod
    def process_image(cls, data: bytes, filename: str) -> dict[str, Any]:
        """Pipeline completo de processamento de imagem.

        1. Abre a imagem com Pillow
        2. Detecta largura, altura e formato reais
        3. Remove EXIF
        4. Redimensiona (max 2000px, proporcional)
        5. Gera thumbnail (max 400px, proporcional)

        Returns:
            {
                "metadata": {width, height, format, size_bytes},
                "processed_image": bytes,
                "thumbnail": bytes,
            }
        """
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "jpg"

        img = Image.open(io.BytesIO(data))

        # Metadados reais da imagem original
        original_w, original_h = img.size
        img_format = img.format or ext.upper()

        # Strip EXIF
        img = cls._strip_exif(img)

        # Resize proporcional (max 2000px)
        main_img = cls._resize_proportional(img, cls.MAX_DIMENSION)

        # Gerar thumbnail (max 400px)
        thumb_img = cls._resize_proportional(img, cls.THUMBNAIL_DIMENSION)

        # Converter para bytes
        main_bytes = cls._to_bytes(main_img, img_format)
        thumb_bytes = cls._to_bytes(thumb_img, img_format)

        return {
            "metadata": {
                "width": main_img.width,
                "height": main_img.height,
                "original_width": original_w,
                "original_height": original_h,
                "format": img_format.lower(),
                "size_bytes": len(main_bytes),
            },
            "processed_image": main_bytes,
            "thumbnail": thumb_bytes,
        }
