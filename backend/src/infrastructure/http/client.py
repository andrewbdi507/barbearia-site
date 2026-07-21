"""HTTP client infrastructure.

Provides an async HTTP client (httpx) for external API calls.
Used by adapters that communicate with payment gateways,
WhatsApp API, email providers, etc.
"""

from __future__ import annotations

import httpx

from src.core.logging import app_logger

logger = app_logger


class HttpClient:
    """Async HTTP client wrapper with timeout and retry defaults.

    Example:
        client = HttpClient()
        async with client:
            response = await client.get("https://api.example.com/health")
    """

    def __init__(self, base_url: str = "", timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
            headers={"User-Agent": "Barbershop-SaaS/0.1.0"},
        )

    async def get(self, path: str, **kwargs: object) -> httpx.Response:
        """Send a GET request."""
        logger.debug("http_get", path=path)
        return await self._client.get(path, **kwargs)  # type: ignore[arg-type]

    async def post(
        self, path: str, json: dict[str, object] | None = None, **kwargs: object
    ) -> httpx.Response:
        """Send a POST request with JSON body."""
        logger.debug("http_post", path=path)
        return await self._client.post(path, json=json, **kwargs)  # type: ignore[arg-type]

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> HttpClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
