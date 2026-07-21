"""API routes — public API.

All routes are registered here via the main router.
"""

from fastapi import APIRouter

from src.presentation.api.health import router as health_router
from src.presentation.api.system import router as system_router

# Main v1 API router — all endpoints are prefixed with /api/v1
router = APIRouter(prefix="/api/v1")

# Health check routes (no /api/v1 prefix — exposed at root)
# Registered directly on the app in app.py

# System routes
router.include_router(system_router, prefix="/system", tags=["system"])

# Future route registrations:
# router.include_router(auth_router, prefix="/auth", tags=["auth"])
# router.include_router(tenant_router, prefix="/tenants", tags=["tenants"])
# router.include_router(booking_router, prefix="/bookings", tags=["bookings"])

# Also expose the health router at the API level
router.include_router(health_router, prefix="/health", tags=["health"])
