# 🎭 RBAC — Role-Based Access Control

> **Versão:** 1.0.0 | **Data:** Julho 2026

---

## 1. Modelo de Autorização

O Barbershop SaaS implementa **RBAC (Role-Based Access Control)** com permissões granulares armazenadas no banco de dados.

```
┌──────────────┐       ┌──────────────┐       ┌─────────────────┐
│    User      │───N:M──│     Role     │───1:M──│   Permission    │
│              │       │              │       │ (JSONB array)   │
│ id           │       │ id           │       │                 │
│ email        │       │ name         │       │ [               │
│ tenant_id    │       │ tenant_id    │       │   "booking:*",  │
│              │       │ is_system    │       │   "service:r",  │
└──────────────┘       └──────────────┘       │   ...           │
       │                                       │ ]               │
       │  UserRole (pivot)                    └─────────────────┘
       │  ┌──────────────┐
       └──│ user_id      │
          │ role_id      │
          └──────────────┘
```

---

## 2. Roles do Sistema

### 2.1 Tabela de Roles

| # | Role | Slug | Escopo | Tipo | Descrição |
|---|------|------|--------|------|-----------|
| 1 | **Super Admin** | `super_admin` | Global | Sistema | Administrador da plataforma SaaS |
| 2 | **Dono** | `owner` | Tenant | Sistema | Dono/proprietário da barbearia |
| 3 | **Administrador** | `admin` | Tenant | Sistema | Gerente da barbearia |
| 4 | **Barbeiro** | `barber` | Tenant | Sistema | Profissional que atende |
| 5 | **Recepcionista** | `receptionist` | Tenant | Sistema | Atendente/recepcionista |
| 6 | **Cliente** | `customer` | Tenant | Sistema | Cliente final |

Roles `is_system=True` não podem ser deletadas. Tenants podem criar roles customizadas (`is_system=False`).

---

## 3. Matriz de Permissões

### 3.1 Convenção de Nomenclatura

```
recurso:verbo[:escopo]

Exemplos:
  booking:read              → ler qualquer agendamento
  booking:read:own          → ler apenas os próprios agendamentos
  booking:read:assigned     → ler agendamentos atribuídos a mim
  booking:write             → criar/editar qualquer agendamento
  booking:write:own         → criar/editar apenas os próprios
  booking:delete            → cancelar qualquer agendamento
  booking:*                 → todas as ações em agendamentos
```

### 3.2 Permissões por Role

#### Super Admin (`super_admin`)

```json
["*"]  // Acesso total — bypass em todas as verificações
```

#### Owner (`owner`)

```json
[
  "booking:*",
  "service:*",
  "professional:*",
  "customer:read",
  "customer:write",
  "report:*",
  "settings:*",
  "billing:*",
  "tenant:*"
]
```

#### Admin (`admin`)

```json
[
  "booking:read",
  "booking:write",
  "booking:delete",
  "service:read",
  "service:write",
  "professional:read",
  "professional:write",
  "customer:read",
  "report:read",
  "settings:read",
  "settings:write"
]
```

#### Barber (`barber`)

```json
[
  "booking:read:assigned",
  "booking:write:own",
  "schedule:read:own",
  "customer:read",
  "service:read",
  "profile:read:own",
  "profile:write:own"
]
```

#### Receptionist (`receptionist`)

```json
[
  "booking:read",
  "booking:write",
  "customer:read",
  "customer:write",
  "service:read",
  "professional:read",
  "schedule:read",
  "profile:read:own"
]
```

#### Customer (`customer`)

```json
[
  "booking:read:own",
  "booking:write:own",
  "profile:read:own",
  "profile:write:own",
  "service:read"
]
```

---

## 4. Uso no Código

### 4.1 Protegendo Rotas

```python
from app.modules.auth.presentation.dependencies import require_permissions

# Requer UMA permissão específica
@router.get("/admin/reports")
async def reports(
    user: Annotated[dict, Depends(require_permissions("report:read"))]
):
    ...

# Requer MÚLTIPLAS permissões (AND)
@router.delete("/admin/bookings/{id}")
async def cancel_booking(
    user: Annotated[dict, Depends(require_permissions("booking:delete", "booking:read"))]
):
    ...
```

### 4.2 Verificação Programática

```python
from app.modules.auth.application.auth_service import AuthService

if await auth_service.has_permission(user_id, "settings:write"):
    # permitir ação
```

### 4.3 Verificação no Frontend

```typescript
// Hook usePermissions
const { hasPermission, hasAllPermissions } = usePermissions();

if (hasPermission("settings:write")) {
  // renderizar botão de configurações
}
```

---

## 5. Tenant Isolation

Além do RBAC, toda operação é isolada por `tenant_id`:

```python
# Dependency que verifica se o usuário pertence ao tenant do recurso
@router.get("/tenants/{tenant_id}/bookings")
async def list_bookings(
    tenant_id: str,
    user: Annotated[dict, Depends(require_tenant_match)],
):
    ...
```

Isso previne que o owner do Tenant A acesse dados do Tenant B, mesmo tendo a mesma role.

---

## 6. Roles Customizadas (Futuro)

Tenants poderão criar roles customizadas:

```sql
-- Exemplo: "Supervisor" — mais que barber, menos que admin
INSERT INTO roles (tenant_id, name, permissions) VALUES (
  't_001',
  'supervisor',
  '["booking:read", "booking:write:own", "professional:read", "report:read", "customer:read"]'
);

INSERT INTO user_roles (user_id, role_id) VALUES ('u_789', 'r_custom_001');
```

---

## 7. Boas Práticas

1. **Sempre usar a dependência `require_permissions`** — nunca verificar manualmente no corpo da rota
2. **Permissões seguem least privilege** — dar apenas o que a role precisa
3. **Super Admin é exceção** — não criar lógica especial para ele, usar `"*"` como bypass
4. **Nunca confiar no frontend** — toda verificação é repetida no backend
5. **Auditar mudanças de permissão** — registrar quem alterou qual role e quando
