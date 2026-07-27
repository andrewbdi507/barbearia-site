"""Media Module — Storage Providers.

LocalStorage, S3Compatible (base), S3Storage, R2Storage.
Provider Pattern: trocar provedor via config.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import BotoCoreError, ClientError, EndpointConnectionError, NoCredentialsError

from app.modules.media.domain.interfaces import StorageProvider, StorageProviderFactory


# ============================================================
# Local Storage (dev)
# ============================================================

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


# ============================================================
# S3-Compatible Base (boto3)
# ============================================================

class S3CompatibleStorageProvider(StorageProvider):
    """Classe base para providers compatíveis com API S3.

    Subclasses devem implementar:
        _build_public_url(path) -> str

    E opcionalmente sobrescrever:
        _get_client_kwargs() -> dict
    """

    def __init__(
        self,
        bucket: str,
        region: str = "us-east-1",
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._bucket = bucket
        self._region = region
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key
        self._client = self._create_client()

    # ---- Subclass hooks ----

    def _build_public_url(self, path: str) -> str:
        """Constrói URL pública do objeto. Sobrescrever nas subclasses."""
        raise NotImplementedError

    def _get_client_kwargs(self) -> dict[str, Any]:
        """Argumentos extras para boto3.client('s3', ...)."""
        kwargs: dict[str, Any] = {
            "region_name": self._region,
            "config": BotoConfig(
                retries={"max_attempts": 2, "mode": "standard"},
                connect_timeout=10,
                read_timeout=30,
            ),
        }
        if self._endpoint_url:
            kwargs["endpoint_url"] = self._endpoint_url
        if self._access_key:
            kwargs["aws_access_key_id"] = self._access_key
        if self._secret_key:
            kwargs["aws_secret_access_key"] = self._secret_key
        return kwargs

    def _create_client(self):
        """Cria o client boto3 S3."""
        try:
            return boto3.client("s3", **self._get_client_kwargs())
        except NoCredentialsError:
            raise ValueError("Credenciais de storage não configuradas.")
        except BotoCoreError as e:
            raise ConnectionError(f"Falha ao conectar ao storage: {e}")

    # ---- StorageProvider interface ----

    async def upload(self, file_data: bytes, path: str, content_type: str, **kwargs: Any) -> str:
        """Upload para bucket S3-compatible."""
        try:
            self._client.put_object(
                Bucket=self._bucket,
                Key=path,
                Body=file_data,
                ContentType=content_type,
            )
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "NoSuchBucket":
                raise ValueError(f"Bucket '{self._bucket}' não encontrado.")
            if code == "AccessDenied" or code == "403":
                raise PermissionError(f"Acesso negado ao bucket '{self._bucket}'.")
            raise ConnectionError(f"Falha no upload: {e}")
        except EndpointConnectionError:
            raise ConnectionError(f"Não foi possível conectar ao storage em '{self._endpoint_url or 'aws'}'.")
        except BotoCoreError as e:
            raise ConnectionError(f"Falha no upload: {e}")

        return self._build_public_url(path)

    async def exists(self, path: str) -> bool:
        """Verifica existência via head_object."""
        try:
            self._client.head_object(Bucket=self._bucket, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise ConnectionError(f"Falha ao verificar existência: {e}")
        except BotoCoreError as e:
            raise ConnectionError(f"Falha ao verificar existência: {e}")

    async def delete(self, path: str) -> bool:
        """Remoção ainda não implementada — será tratada em fase futura."""
        raise NotImplementedError("StorageProvider.delete() não implementado.")

    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        """URL pública (não assinada)."""
        return self._build_public_url(path)


# ============================================================
# Amazon S3
# ============================================================

class S3StorageProvider(S3CompatibleStorageProvider):
    """Amazon S3."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            bucket=kwargs.get("bucket") or os.getenv("STORAGE_S3_BUCKET", ""),
            region=kwargs.get("region") or os.getenv("STORAGE_S3_REGION", "us-east-1"),
            access_key=kwargs.get("access_key") or os.getenv("STORAGE_S3_ACCESS_KEY"),
            secret_key=kwargs.get("secret_key") or os.getenv("STORAGE_S3_SECRET_KEY"),
        )

    def _build_public_url(self, path: str) -> str:
        return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{path}"


# ============================================================
# Cloudflare R2
# ============================================================

class R2StorageProvider(S3CompatibleStorageProvider):
    """Cloudflare R2 — API compatível com S3."""

    def __init__(self, **kwargs: Any) -> None:
        account_id = kwargs.get("account_id") or os.getenv("STORAGE_R2_ACCOUNT_ID", "")
        super().__init__(
            bucket=kwargs.get("bucket") or os.getenv("STORAGE_R2_BUCKET", ""),
            region="auto",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com" if account_id else None,
            access_key=kwargs.get("access_key") or os.getenv("STORAGE_R2_ACCESS_KEY"),
            secret_key=kwargs.get("secret_key") or os.getenv("STORAGE_R2_SECRET_KEY"),
        )

    def _build_public_url(self, path: str) -> str:
        account_id = os.getenv("STORAGE_R2_ACCOUNT_ID", "")
        if self._endpoint_url and "/" in self._endpoint_url:
            # R2 custom domain: https://pub-xxx.r2.dev
            return f"{self._endpoint_url}/{self._bucket}/{path}"
        return f"https://{self._bucket}.{account_id}.r2.cloudflarestorage.com/{path}"


def register_storage_providers() -> None:
    StorageProviderFactory.register("local", LocalStorageProvider)
    StorageProviderFactory.register("s3", S3StorageProvider)
    StorageProviderFactory.register("r2", R2StorageProvider)
