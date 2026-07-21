"""Auth Routes — User Registration endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, field_validator

from app.infrastructure.database.session import get_async_session
from app.modules.auth.application.auth_service import AuthService
from app.modules.auth.infrastructure.repository import AuthRepository
from app.modules.auth.infrastructure import security as sec

register_router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    tenant_id: str  # UUID do tenant (obrigatório para registro)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")
        return v


class RegisterResponse(BaseModel):
    id: str
    email: str
    name: str
    message: str = "Usuário criado com sucesso. Faça login."


@register_router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(
    body: RegisterRequest,
    session: AsyncSession = Depends(get_async_session),
) -> RegisterResponse:
    """Registra novo usuário administrador para um tenant.

    Cria o usuário com senha hash (Argon2id).
    """
    from uuid import uuid4
    from datetime import datetime, timezone
    from app.modules.auth.infrastructure.models.auth_models import UserModel
    from app.core.exceptions import ConflictError

    # Verificar se email já existe
    repo = AuthRepository(session)
    existing = await repo.get_user_by_email(body.email, body.tenant_id)
    if existing:
        raise ConflictError(message="Email já cadastrado neste tenant.")

    hashed = sec.hash_password(body.password)
    user = UserModel(
        id=str(uuid4()),
        email=body.email,
        name=body.name,
        password_hash=hashed,
        tenant_id=body.tenant_id,
        is_active=True,
        is_verified=True,
        failed_login_attempts=0,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(user)
    await session.commit()

    return RegisterResponse(id=user.id, email=user.email, name=user.name)
