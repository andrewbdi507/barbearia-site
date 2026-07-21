# 04 — API Pública

> Estratégia para a futura API pública do Barbershop SaaS.  
> Voltada para parceiros, desenvolvedores e marketplace de apps.  
> **Status:** V3+ (Mês 18-36)

---

## 1. Visão

A API Pública transforma o Barbershop SaaS de um produto fechado em uma **plataforma**. Desenvolvedores poderão criar apps, integrações e automações que expandem o ecossistema.

### Exemplos de Uso

- App de "Relatórios Avançados" que consome dados via API
- Integração com ERP/sistema de gestão financeira
- Sincronização com Google Sheets
- Automações no n8n/Zapier/Make
- App mobile customizado para uma rede de barbearias

---

## 2. Arquitetura da API Pública

```
┌──────────────────────────────────────────────────────────────────┐
│                       API PÚBLICA                                 │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   API GATEWAY                                │ │
│  │                                                              │ │
│  │  api.barbersaas.com/public/v1/                               │ │
│  │                                                              │ │
│  │  Middleware:                                                  │ │
│  │  ├── Authentication (API Key / OAuth 2.0)                   │ │
│  │  ├── Rate Limiting (por app, por tenant)                     │ │
│  │  ├── Tenant Resolution (X-Tenant-ID ou subdomínio)          │ │
│  │  ├── Request Validation (OpenAPI schema)                     │ │
│  │  ├── Logging (audit trail)                                   │ │
│  │  └── Response Caching (quando aplicável)                     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   PUBLIC API ROUTES                          │ │
│  │                                                              │ │
│  │  /bookings      → Agendamentos (read/write)                  │ │
│  │  /services      → Serviços (read)                            │ │
│  │  /professionals  → Profissionais (read)                      │ │
│  │  /customers     → Clientes (read/write)                      │ │
│  │  /reviews       → Avaliações (read)                          │ │
│  │  /webhooks      → Configuração de webhooks outbound          │ │
│  │  /tenant        → Informações do tenant (read)               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Autenticação

### Métodos

| Método | Uso | Fluxo |
|--------|-----|-------|
| **API Key** | Server-to-server, automações | Header `X-API-Key: {key}` |
| **OAuth 2.0** | Apps de terceiros (marketplace) | Authorization Code + PKCE |

### API Key

```
┌──────────────────────────────────────────────────────────────────┐
│              API KEY AUTHENTICATION                               │
│                                                                   │
│  Criação (painel admin do tenant):                                │
│  - Nome: "Meu App de Relatórios"                                  │
│  - Permissões: ["bookings:read", "customers:read"]                │
│  - Key gerada: bsk_live_abc123def456...                           │
│  - Prefixos: bsk_live_ (produção), bsk_test_ (sandbox)           │
│                                                                   │
│  Uso:                                                             │
│  curl -H "X-API-Key: bsk_live_abc123..."                          │
│       -H "X-Tenant-ID: t_001"                                     │
│       https://api.barbersaas.com/public/v1/bookings               │
│                                                                   │
│  Segurança:                                                       │
│  - Key armazenada como SHA-256 hash no banco                     │
│  - Key exibida UMA ÚNICA vez na criação                           │
│  - Rotação: novo par key/secret, revogar antigo                   │
│  - Rate limit: 1.000 req/min por API key                          │
└──────────────────────────────────────────────────────────────────┘
```

### OAuth 2.0 (Marketplace)

```
┌──────────────────────────────────────────────────────────────────┐
│              OAUTH 2.0 FLOW (Authorization Code + PKCE)          │
│                                                                   │
│  1. App registrado no Marketplace:                                │
│     - client_id, client_secret, redirect_uri                      │
│     - Scopes solicitados: ["bookings:read", "customers:write"]    │
│                                                                   │
│  2. Tenant instala o app → OAuth flow inicia:                     │
│     GET /oauth/authorize?client_id=...&scope=...&redirect_uri=... │
│                                                                   │
│  3. Tenant autoriza os scopes                                     │
│                                                                   │
│  4. Redirect com authorization_code                               │
│                                                                   │
│  5. App troca code por access_token:                              │
│     POST /oauth/token                                             │
│     { code, client_id, client_secret, code_verifier }             │
│                                                                   │
│  6. Resposta:                                                     │
│     {                                                             │
│       "access_token": "eyJ...",      // JWT, expira 1h           │
│       "refresh_token": "rt_...",     // expira 90 dias            │
│       "scope": "bookings:read customers:write",                   │
│       "tenant_id": "t_001"                                        │
│     }                                                             │
│                                                                   │
│  Uso:                                                             │
│  curl -H "Authorization: Bearer eyJ..."                           │
│       https://api.barbersaas.com/public/v1/bookings               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Rate Limiting

### Tiers

| Tier | Rate Limit | Descrição |
|------|:---------:|-----------|
| **Free** | 100 req/min | Apps em desenvolvimento |
| **Basic** | 1.000 req/min | Apps publicados |
| **Premium** | 10.000 req/min | Apps de alto volume |
| **Enterprise** | Customizado | Contrato dedicado |

### Headers de Rate Limit

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1690000000
Retry-After: 60 (quando 429)
```

---

## 5. Versionamento

### URL-Based Versioning

```
https://api.barbersaas.com/public/v1/bookings
https://api.barbersaas.com/public/v2/bookings
```

### Política

- **Major versions:** v1, v2, v3 (mudanças breaking)
- **Minor updates:** Dentro da mesma major, backward-compatible
- **Depreciação:** 12 meses de coexistência entre versões
- **Sunset:** Anunciado com 6 meses de antecedência

### Headers de Versão

```
Response:
  X-API-Version: 2026-07-20
  X-API-Deprecation: 2027-07-20 (se deprecada)
  Sunset: Sat, 20 Jul 2027 00:00:00 GMT
```

---

## 6. Scopes & Permissões (RBAC)

| Scope | Descrição | Tipo |
|-------|-----------|:----:|
| `bookings:read` | Listar agendamentos | Read |
| `bookings:write` | Criar/editar agendamentos | Write |
| `customers:read` | Listar clientes | Read |
| `customers:write` | Criar/editar clientes | Write |
| `services:read` | Listar serviços | Read |
| `professionals:read` | Listar profissionais | Read |
| `reviews:read` | Listar avaliações | Read |
| `analytics:read` | Acessar métricas e relatórios | Read |
| `webhooks:write` | Configurar webhooks | Write |
| `tenant:read` | Informações do tenant | Read |

---

## 7. Webhooks (Event Subscriptions)

### Configuração

```
POST /public/v1/webhooks/subscriptions
{
  "url": "https://meuapp.com/hooks/barbershop",
  "events": ["booking.created", "booking.completed"],
  "secret": "whsec_...",
  "api_version": "2026-07-20"
}
```

### Eventos Disponíveis para Inscrição

| Evento | Descrição |
|--------|-----------|
| `booking.created` | Novo agendamento |
| `booking.cancelled` | Cancelamento |
| `booking.completed` | Atendimento concluído |
| `customer.registered` | Novo cliente |
| `review.created` | Nova avaliação |
| `payment.succeeded` | Pagamento confirmado |

---

## 8. SDKs & Developer Experience

### SDKs Planejados (V3+)

| Linguagem | Pacote |
|-----------|--------|
| JavaScript/TypeScript | `npm install @barbershop/api` |
| Python | `pip install barbershop-api` |
| PHP | `composer require barbershop/api` |

### Developer Portal (V3+)

```
developers.barbersaas.com
├── Getting Started (guia rápido)
├── API Reference (OpenAPI / Redoc)
├── Guides (tutoriais)
├── SDKs (links + docs)
├── Changelog
└── Community (fórum)
```

---

## 9. Segurança da API Pública

| Camada | Implementação |
|--------|--------------|
| **Transporte** | TLS 1.3 obrigatório |
| **Autenticação** | API Key (SHA-256 hash) + OAuth 2.0 |
| **Autorização** | Scopes + Tenant ID (RLS) |
| **Rate Limiting** | Por API key, por IP, por tenant |
| **Input Validation** | OpenAPI schema validation |
| **Output Sanitization** | JSON encoding, sem dados sensíveis |
| **Logging** | Audit log de toda chamada de API |
| **CORS** | Apenas origens registradas (para SDK browser) |
| **DPoP** | (futuro) Demonstrating Proof-of-Possession |

---

## 10. Roadmap da API Pública

| Fase | Quando | Entregas |
|------|:------:|----------|
| **Preparação** | V1 (Mês 3-9) | OpenAPI spec interna, endpoints RESTful |
| **Beta Fechado** | V2 (Mês 9-18) | API Keys, 5 parceiros, documentação básica |
| **Lançamento** | V3 (Mês 18-36) | OAuth 2.0, Developer Portal, SDKs, Marketplace |
| **Escala** | V4 (Mês 36-60) | GraphQL, gRPC (opcional), 100+ apps no marketplace |

---

> **Resumo:** A API Pública é a evolução natural do produto para plataforma. Autenticação via API Key (simples) ou OAuth 2.0 (marketplace). Rate limiting por tier. Versionamento via URL com política de depreciação clara. Scopes granulares para permissões mínimas. Webhooks para eventos em tempo real. SDKs e Developer Portal para developer experience de primeira classe.
