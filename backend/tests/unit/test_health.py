"""Test: Application Health Endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.presentation.api.app import create_app
from src.core.config import Settings


@pytest.fixture
def client(settings: Settings) -> TestClient:
    """Create a test client with the application."""
    app = create_app(settings)
    return TestClient(app)


class TestHealthEndpoints:
    """Health check endpoint tests."""

    def test_liveness_returns_200(self, client: TestClient) -> None:
        """Liveness probe should always return 200."""
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}

    def test_system_info_returns_metadata(self, client: TestClient) -> None:
        """System info should return app metadata."""
        response = client.get("/api/v1/system/info")
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "barbershop-saas"
        assert "version" in data
        assert data["environment"] == "testing"

    def test_ping_returns_ok(self, client: TestClient) -> None:
        """Ping should return simple pong."""
        response = client.get("/api/v1/system/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": "ok"}

    def test_openapi_schema_generates(self, client: TestClient) -> None:
        """OpenAPI JSON should be generated successfully."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "barbershop-saas"

    def test_docs_endpoint_accessible(self, client: TestClient) -> None:
        """Swagger docs should be accessible in debug mode."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestSecurityHeaders:
    """Security header tests."""

    def test_security_headers_present(self, client: TestClient) -> None:
        """All responses should include security headers."""
        response = client.get("/api/v1/health/live")
        headers = response.headers

        assert headers.get("X-Content-Type-Options") == "nosniff"
        assert headers.get("X-Frame-Options") == "DENY"
        assert "Content-Security-Policy" in headers
        assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_request_id_header_present(self, client: TestClient) -> None:
        """Every response should have X-Request-ID header."""
        response = client.get("/api/v1/health/live")
        assert "X-Request-ID" in response.headers
        request_id = response.headers["X-Request-ID"]
        assert len(request_id) > 0
