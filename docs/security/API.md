# 📡 Auth API — Referência

> **Base URL:** `/api/v1/auth` | **Versão:** 1.0.0

---

## Endpoints

| Método | Path | Auth | Descrição |
|--------|------|:----:|-----------|
| POST | `/auth/login` | ❌ | Login — retorna tokens |
| POST | `/auth/refresh` | 🍪 | Rotaciona refresh token |
| POST | `/auth/logout` | ✅ | Revoga sessão atual |
| POST | `/auth/logout-all` | ✅ | Revoga TODAS as sessões |
| GET | `/auth/me` | ✅ | Dados do usuário autenticado |
| GET | `/auth/sessions` | ✅ | Lista sessões ativas |
| DELETE | `/auth/sessions/{id}` | ✅ | Revoga sessão específica |
| POST | `/auth/forgot-password` | ❌ | Solicita recuperação de senha |
| POST | `/auth/reset-password` | ❌ | Redefine senha com token |
| POST | `/auth/change-password` | ✅ | Altera senha (autenticado) |

> ❌ = Público | ✅ = Requer Bearer Token | 🍪 = Requer cookie refresh_token

---

## POST /auth/login

Autentica usuário e retorna access token + refresh token (cookie).

**Request:**
```json
{
  "email": "joao@barbearia.com",
  "password": "minha-senha",
  "tenant_id": "t_001"
}
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "u_abc123",
    "email": "joao@barbearia.com",
    "name": "João Silva",
    "tenant_id": "t_001",
    "role": "admin",
    "permissions": ["booking:*", "service:*", "..."]
  }
}
```
> Também define cookie `refresh_token` (HttpOnly, Secure, SameSite=Strict)

**Erros:**
| Código | Mensagem | Causa |
|:------:|----------|-------|
| 401 | `Credenciais inválidas.` | Email/senha errados OU conta bloqueada OU conta inativa |
| 422 | `Validation error` | Campo ausente ou formato inválido |
| 429 | `Muitas requisições.` | Rate limit excedido (planejado) |

---

## POST /auth/refresh

Rotaciona refresh token e retorna novo access token.

**Request (opcional):**
```json
{
  "refresh_token": "a1b2c3..."
}
```
> Se não enviado no corpo, usa o cookie `refresh_token`.

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```
> Também define novo cookie `refresh_token`.

**Erros:**
| Código | Mensagem | Causa |
|:------:|----------|-------|
| 401 | `Refresh token não fornecido.` | Token não enviado |
| 401 | `Token inválido ou expirado.` | Token já usado (possível roubo) ou expirado |

> ⚠️ Se um refresh token já utilizado for reusado, **toda a família é revogada** (detecção de roubo).

---

## POST /auth/logout

**Headers:**
```
Authorization: Bearer eyJhbGciOi...
```

**Response `200`:**
```json
{
  "message": "Logout realizado com sucesso."
}
```
> Também remove cookie `refresh_token`.

---

## POST /auth/logout-all

**Response `200`:**
```json
{
  "message": "Todas as sessões foram encerradas."
}
```
> Revoga TODOS os refresh tokens + TODAS as sessões do usuário.

---

## GET /auth/me

**Response `200`:**
```json
{
  "user_id": "u_abc123",
  "tenant_id": "t_001",
  "email": "joao@barbearia.com",
  "name": "João Silva",
  "permissions": ["booking:*", "service:read"],
  "role": "admin"
}
```

---

## GET /auth/sessions

**Response `200`:**
```json
{
  "sessions": [
    {
      "id": "sess_001",
      "ip_address": "189.54.32.10",
      "user_agent": "Mozilla/5.0 ...",
      "device_type": "web",
      "is_current": true,
      "created_at": "2026-07-20T14:30:00Z",
      "expires_at": "2026-07-27T14:30:00Z"
    },
    {
      "id": "sess_002",
      "ip_address": "189.54.32.10",
      "user_agent": "BarberApp/1.0 (Android)",
      "device_type": "android",
      "is_current": false,
      "created_at": "2026-07-19T09:00:00Z",
      "expires_at": "2026-07-26T09:00:00Z"
    }
  ]
}
```

---

## DELETE /auth/sessions/{session_id}

**Response `200`:**
```json
{
  "message": "Sessão revogada."
}
```

**Erros:**
| Código | Mensagem |
|:------:|----------|
| 404 | Sessão não encontrada ou não pertence ao usuário |

---

## POST /auth/forgot-password

**Request:**
```json
{
  "email": "joao@barbearia.com"
}
```

**Response `200` (sempre):**
```json
{
  "message": "Se o email existir, enviaremos instruções de recuperação."
}
```
> ⚠️ Sempre retorna 200 — anti-enumeração de usuários.  
> No MVP, o token é logado no console. Em produção: enviado por email.

---

## POST /auth/reset-password

**Request:**
```json
{
  "token": "a1b2c3d4e5f6...",
  "new_password": "NovaSenhaForte123"
}
```

**Response `200`:**
```json
{
  "message": "Senha redefinida com sucesso."
}
```

**Erros:**
| Código | Mensagem |
|:------:|----------|
| 400 | Token inválido ou expirado |
| 422 | Senha não atende política (mín. 8 caracteres) |

---

## POST /auth/change-password

**Request:**
```json
{
  "current_password": "senha-atual",
  "new_password": "nova-senha-forte"
}
```

**Response `200`:**
```json
{
  "message": "Senha alterada com sucesso."
}
```

**Erros:**
| Código | Mensagem |
|:------:|----------|
| 400 | Senha atual incorreta |
| 422 | Nova senha igual à atual ou não atende política |

---

## Headers Comuns

### Request
```
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json
```

### Response
```
Content-Type: application/json
Set-Cookie: refresh_token=...; HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth; Max-Age=604800
```

---

## Rate Limiting (planejado)

| Endpoint | Limite | Janela | Código |
|----------|--------|--------|:------:|
| `/auth/login` | 5/min | 60s | 429 |
| `/auth/forgot-password` | 3/min | 60s | 429 |
| Demais `/auth/*` | 60/min | 60s | 429 |
