"""Media Module — Storage Providers.

LocalStorage, S3Storage, R2Storage.
Provider Pattern: trocar provedor via config.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path
from typing import Any

from app.modules.media.domain.interfaces import StorageProvider, StorageProviderFactory


class LocalStorageProvider(StorageProvider):
    """Armazenamento local — desenvolvimento."""

    def __init__(self, base_path: str = "./media") -> None:
        self._base = Path(base_path)

    async def upload(self, file_data: bytes, path: str, content_type: str, **kwargs: Any) -> str:
        full_path = self._base / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(file_data)
        return f"/media/{path}"

    async def delete(self, path: str) -> bool:
        full_path = self._base / path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        return f"/media/{path}"

    async def exists(self, path: str) -> bool:
        return (self._base / path).exists()


class S3StorageProvider(StorageProvider):
    """Amazon S3 — produção."""

    def __init__(self, bucket: str = "", region: str = "us-east-1", **kwargs: Any) -> None:
        self._bucket = bucket
        self._region = region

    async def upload(self, file_data: bytes, path: str, content_type: str, **kwargs: Any) -> str:
        # Mock: em produção usa boto3
        return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{path}"

    async def delete(self, path: str) -> bool:
        return True

    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{path}"

    async def exists(self, path: str) -> bool:
        return True


class R2StorageProvider(StorageProvider):
    """Cloudflare R2 — compatível com S3."""

    def __init__(self, bucket: str = "", account_id: str = "", **kwargs: Any) -> None:
        self._bucket = bucket
        self._account_id = account_id

    async def upload(self, file_data: bytes, path: str, content_type: str, **kwargs: Any) -> str:
        return f"https://{self._bucket}.{self._account_id}.r2.cloudflarestorage.com/{path}"

    async def delete(self, path: str) -> bool:
        return True

    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        return f"https://{self._bucket}.{self._account_id}.r2.cloudflarestorage.com/{path}"

    async def exists(self, path: str) -> bool:
        return True


def register_storage_providers() -> None:
    StorageProviderFactory.register("local", LocalStorageProvider)
    StorageProviderFactory.register("s3", S3StorageProvider)
    StorageProviderFactory.register("r2", R2StorageProvider)
