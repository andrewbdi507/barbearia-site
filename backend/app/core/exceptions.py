"""Core Domain Exceptions.

Hierarquia de exceções HTTP-friendly para todo o sistema.
Cada exceção carrega seu próprio status_code e mensagem.
"""

from __future__ import annotations

from typing import Any


class AppError(Exception):
    """Base para todas as exceções da aplicação."""

    message: str = "Erro interno."
    status_code: int = 500
    code: str = "internal_error"
    details: dict[str, Any] | None = None

    def __init__(
        self,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "error": self.code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result


# ============================================================
# 4xx — Erros do Cliente
# ============================================================


class ValidationError(AppError):
    """Erro de validação (422)."""
    status_code = 422
    code = "validation_error"
    message = "Dados inválidos."


class AuthenticationError(AppError):
    """Usuário não autenticado (401)."""
    status_code = 401
    code = "authentication_error"
    message = "Token de acesso inválido ou expirado."


class InvalidCredentialsError(AppError):
    """Credenciais inválidas (401) — genérico, anti-enumeração."""
    status_code = 401
    code = "invalid_credentials"
    message = "Credenciais inválidas."


class AuthorizationError(AppError):
    """Usuário sem permissão (403)."""
    status_code = 403
    code = "authorization_error"
    message = "Permissões insuficientes."


class TokenInvalidError(AppError):
    """Refresh token inválido, expirado ou revogado (401)."""
    status_code = 401
    code = "token_invalid"
    message = "Token inválido ou expirado."


class TokenExpiredError(AppError):
    """Access token expirado — o cliente deve usar o refresh token (401)."""
    status_code = 401
    code = "token_expired"
    message = "Token expirado. Utilize o refresh token."


class NotFoundError(AppError):
    """Recurso não encontrado (404)."""
    status_code = 404
    code = "not_found"
    message = "Recurso não encontrado."


class ConflictError(AppError):
    """Conflito de estado (409)."""
    status_code = 409
    code = "conflict"
    message = "Conflito de estado."


class BusinessRuleError(AppError):
    """Violação de regra de negócio (400)."""
    status_code = 400
    code = "business_rule_violation"
    message = "Operação não permitida."


class RateLimitExceededError(AppError):
    """Rate limit excedido (429)."""
    status_code = 429
    code = "rate_limit_exceeded"
    message = "Muitas requisições. Aguarde um momento."


# ============================================================
# Multi-Tenant Exceptions
# ============================================================


class TenantNotFoundError(NotFoundError):
    """Tenant não encontrado (404)."""
    code = "tenant_not_found"
    message = "Empresa não encontrada."


class TenantAccessDeniedError(AuthorizationError):
    """Acesso cross-tenant bloqueado (403)."""
    code = "tenant_access_denied"
    message = "Acesso não permitido a este workspace."


class TenantSuspendedError(BusinessRuleError):
    """Tenant suspenso (403)."""
    code = "tenant_suspended"
    message = "Conta suspensa. Entre em contato com o suporte."


class DomainAlreadyTakenError(ConflictError):
    """Subdomínio já registrado (409)."""
    code = "domain_already_taken"
    message = "Este subdomínio já está em uso."


class PlanLimitExceededError(BusinessRuleError):
    """Limite do plano excedido (400)."""
    code = "plan_limit_exceeded"
    message = "Limite do plano atual excedido."


class SubscriptionRequiredError(BusinessRuleError):
    """Assinatura necessária para ação (402)."""
    status_code = 402
    code = "subscription_required"
    message = "Assinatura ativa necessária para esta operação."
