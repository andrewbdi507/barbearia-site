"""Media Module — Storage Provider Interface (ABC).

Provider Pattern para armazenamento de arquivos.
Trocar S3 → R2 → GCS via configuração, sem alterar código.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, BinaryIO


class StorageProvider(ABC):
    """Interface abstrata para provedor de armazenamento.

    Implementações:
    - LocalStorageProvider (dev)
    - S3StorageProvider (AWS)
    - R2StorageProvider (Cloudflare)
    - GCSStorageProvider (Google Cloud)
    - AzureBlobStorageProvider (Azure)
    """

    @abstractmethod
    async def upload(
        self, file_data: bytes, path: str, content_type: str, **kwargs: Any,
    ) -> str:
        """Faz upload e retorna URL pública."""
        ...

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Remove arquivo."""
        ...

    @abstractmethod
    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        """Gera URL (assinada se necessário)."""
        ...

    @abstractmethod
    async def exists(self, path: str) -> bool:
        """Verifica se arquivo existe."""
        ...


class StorageProviderFactory:
    """Factory de provedores de armazenamento."""

    _providers: dict[str, type[StorageProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[StorageProvider]) -> None:
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> StorageProvider:
        provider_class = cls._providers.get(name)
        if provider_class is None:
            raise ValueError(f"Storage provider '{name}' não registrado.")
        return provider_class(**kwargs)
