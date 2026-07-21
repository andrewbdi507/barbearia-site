"""Notification Module — API Routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.notification.application.dto import (
    ChannelConfigRequest,
    NotificationListResponse,
    NotificationResponse,
    NotificationSendRequest,
    TemplateCreateRequest,
    TemplatePreviewRequest,
    TemplatePreviewResponse,
    TemplateResponse,
    TemplateUpdateRequest,
)
from app.modules.notification.application.notification_service import NotificationService
from app.modules.notification.infrastructure.repository import (
    ChannelConfigRepository,
    NotificationRepository,
    TemplateRepository,
)
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def _get_service(session: AsyncSession) -> NotificationService:
    return NotificationService(
        template_repo=TemplateRepository(session),
        notification_repo=NotificationRepository(session),
        channel_config_repo=ChannelConfigRepository(session),
    )


# ============================================================
# TEMPLATES
# ============================================================

@router.get("/templates", response_model=list[TemplateResponse])
async def list_templates(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[TemplateResponse]:
    svc = _get_service(session)
    templates = await svc.list_templates(tenant["id"])
    return [TemplateResponse(**t.__dict__) for t in templates]


@router.post("/templates", response_model=TemplateResponse, status_code=201)
async def create_template(
    body: TemplateCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> TemplateResponse:
    svc = _get_service(session)
    t = await svc.create_template(tenant["id"], **body.model_dump())
    return TemplateResponse(**t.__dict__)


@router.patch("/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    body: TemplateUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> TemplateResponse:
    svc = _get_service(session)
    t = await svc.update_template(template_id, **body.model_dump(exclude_none=True))
    return TemplateResponse(**t.__dict__)


@router.post("/templates/{template_id}/preview", response_model=TemplatePreviewResponse)
async def preview_template(
    template_id: str,
    body: TemplatePreviewRequest,
    session: AsyncSession = Depends(get_async_session),
) -> TemplatePreviewResponse:
    svc = _get_service(session)
    result = await svc.preview_template(template_id, body.sample_data)
    return TemplatePreviewResponse(**result)


# ============================================================
# NOTIFICATIONS
# ============================================================

@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    status: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> NotificationListResponse:
    svc = _get_service(session)
    items, total = await svc.list_notifications(tenant["id"], status=status, offset=offset, limit=limit)
    return NotificationListResponse(
        items=[NotificationResponse(**n.__dict__) for n in items],
        total=total, offset=offset, limit=limit,
    )


@router.post("", response_model=NotificationResponse, status_code=201)
async def send_notification(
    body: NotificationSendRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> NotificationResponse:
    svc = _get_service(session)
    n = await svc.send_manual(tenant["id"], **body.model_dump())
    return NotificationResponse(**n.__dict__)


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> NotificationResponse:
    svc = _get_service(session)
    n = await svc.get_notification(notification_id)
    return NotificationResponse(**n.__dict__)


@router.get("/customers/{customer_id}", response_model=NotificationListResponse)
async def get_customer_notifications(
    customer_id: str,
    session: AsyncSession = Depends(get_async_session),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> NotificationListResponse:
    svc = _get_service(session)
    items, total = await svc.get_customer_notifications(customer_id, offset=offset, limit=limit)
    return NotificationListResponse(
        items=[NotificationResponse(**n.__dict__) for n in items],
        total=total, offset=offset, limit=limit,
    )


# ============================================================
# RETRY
# ============================================================

@router.post("/retry")
async def retry_pending(
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=100, ge=1, le=500),
) -> dict:
    svc = _get_service(session)
    count = await svc.retry_pending(limit=limit)
    return {"retried": count}


# ============================================================
# CHANNEL CONFIG
# ============================================================

@router.post("/channels/config")
async def configure_channel(
    body: ChannelConfigRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.configure_channel(tenant["id"], **body.model_dump())
    return {"message": "Canal configurado."}
