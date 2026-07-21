# 01 — Threat Model (STRIDE)

> Modelagem de ameaças do Barbershop SaaS.  
> Metodologia: STRIDE (Microsoft)  
> Sistema: Plataforma SaaS multi-tenant de agendamento

---

## 1. Diagrama de Fluxo de Dados (DFD) — Nível 0

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Cliente  │────►│ Site Público │────►│   Backend    │
│ Final    │     │ (Next.js)    │     │  (FastAPI)   │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌─────────────────────────┼─────────────────────┐
                    │                         │                     │
              ┌─────▼─────┐           ┌──────▼──────┐      ┌──────▼──────┐
              │ PostgreSQL │           │    Redis    │      │  S3 / R2    │
              │ (Primary)  │           │Cache / Queue│      │  Storage    │
              └────────────┘           └─────────────┘      └─────────────┘
                    │
              ┌─────▼─────┐
              │  Gateway  │  ← Stripe, WhatsApp, Email
              │  Externo  │
              └───────────┘

Trust Boundaries (limites de confiança):
  ═══ Internet (não confiável)
  ─── CDN/WAF (semi-confiável)
  ─── Backend (confiável)
  ─── Banco/Dados (altamente confiável)
```

---

## 2. STRIDE por Componente

### T1 — Spoofing (Falsificação de Identidade)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T1.1 | Atacante falsifica identidade de outro tenant | Auth Service | 🔴 5 | 3 | 15 |
| T1.2 | Atacante reutiliza JWT de outro usuário (token theft) | Auth Service | 🔴 5 | 2 | 10 |
| T1.3 | Atacante forja webhook de gateway de pagamento | Payment Webhook | 🔴 5 | 2 | 10 |
| T1.4 | Atacante falsifica subdomínio de outro tenant | DNS / Tenant Resolution | 🟠 4 | 2 | 8 |
| T1.5 | Atacante usa credenciais vazadas de funcionário | Auth Service | 🟠 4 | 3 | 12 |

**Mitigações existentes:**
- T1.1: Middleware de tenant + RLS (planejado)
- T1.2: Refresh token rotation + família de tokens
- T1.3: HMAC-SHA256 webhook signature
- T1.4: Validação de subdomínio no banco
- T1.5: Lockout após 5 tentativas (planejado)

**Recomendações adicionais:**
- T1.1: Implementar RLS antes de qualquer cliente real
- T1.2: Adicionar device fingerprinting no refresh token
- T1.3: IP allowlist para webhooks de gateways em produção
- T1.5: Implementar MFA para admins (V3+)

---

### T2 — Tampering (Violação de Integridade)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T2.1 | Atacante modifica JWT claims (escalada de privilégio) | Auth Service | 🔴 5 | 2 | 10 |
| T2.2 | Atacante modifica preço/duração no fluxo de agendamento | Booking API | 🟠 4 | 3 | 12 |
| T2.3 | Atacante modifica webhook payload para forjar pagamento | Payment Webhook | 🔴 5 | 2 | 10 |
| T2.4 | Atacante modifica arquivo durante upload (path traversal) | Media Service | 🟠 4 | 3 | 12 |
| T2.5 | Atacante modifica CSP headers via injection | Frontend | 🟡 3 | 2 | 6 |

**Mitigações existentes:**
- T2.1: JWT signature verification (HMAC/RSA)
- T2.2: Preços validados no backend (servidor é fonte da verdade)
- T2.3: HMAC webhook signature + idempotency
- T2.4: Nome de arquivo UUID, sem user input no path
- T2.5: CSP definido no middleware do backend

**Recomendações adicionais:**
- T2.2: Implementar "price snapshot" no booking — o preço pago é o do momento do agendamento
- T2.4: Adicionar ClamAV scan (ou Cloudflare Images sanitization)
- T2.1: Usar RS256 (chave assimétrica) em vez de HS256 para JWT em produção (V3+)

---

### T3 — Repudiation (Repúdio)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T3.1 | Admin nega ter alterado preço/serviço | Admin Panel | 🟡 3 | 3 | 9 |
| T3.2 | Cliente nega ter feito agendamento | Booking API | 🟡 3 | 3 | 9 |
| T3.3 | Cliente nega ter autorizado pagamento | Payment | 🟠 4 | 2 | 8 |
| T3.4 | Barbeiro nega ter marcado no-show | Professional App | 🟢 2 | 3 | 6 |

**Mitigações existentes:**
- T3.1: Audit logs planejados (append-only)
- T3.2: Booking status log (máquina de estados)
- T3.3: Gateway de pagamento como terceiro confiável (webhook assinado)
- T3.4: Audit log de ações do barbeiro

**Recomendações adicionais:**
- T3.1: Implementar audit_logs antes dos primeiros clientes
- T3.2: Enviar confirmação por WhatsApp como "recibo digital"
- T3.3: Armazenar webhook payload bruto (assinado) como prova

---

### T4 — Information Disclosure (Vazamento de Informação)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T4.1 | Tenant acessa dados de outro tenant (cross-tenant) | Database | 🔴 5 | 3 | **15** |
| T4.2 | Dados de cliente vazam via API (IDOR) | Booking API | 🔴 5 | 3 | **15** |
| T4.3 | Dados pessoais expostos em logs | Logging | 🟠 4 | 4 | **16** |
| T4.4 | Stack trace exposto em erros 500 | Error Handler | 🟡 3 | 3 | 9 |
| T4.5 | Dados sensíveis em URL (GET com query params) | API Design | 🟡 3 | 2 | 6 |
| T4.6 | Enumeração de usuários via forgot password | Auth Service | 🟡 3 | 3 | 9 |
| T4.7 | Dados expostos via Google Calendar (evento público) | Calendar Integration | 🟡 3 | 2 | 6 |

**Mitigações existentes:**
- T4.1: RLS + middleware de tenant (3 camadas)
- T4.2: Validação de pertencimento em toda query
- T4.3: Logs NUNCA contêm senhas, tokens, dados de cartão (documentado)
- T4.4: Exception handler retorna mensagem genérica para 500
- T4.5: Dados sensíveis via POST/PUT, não GET

**Recomendações adicionais:**
- T4.3: **URGENTE** — Adicionar sanitização automática de PII nos logs (mascarar telefone, email parcial)
- T4.6: Mensagem genérica: "Se o email existir, enviaremos instruções"
- T4.7: Google Calendar: eventos criados como "private" por padrão

---

### T5 — Denial of Service (Negação de Serviço)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T5.1 | Atacante sobrecarrega API com requisições | API Gateway | 🟠 4 | 4 | **16** |
| T5.2 | Atacante esgota pool de conexões do banco | Database | 🟠 4 | 2 | 8 |
| T5.3 | Atacante faz uploads massivos (storage exhaustion) | Media Service | 🟡 3 | 3 | 9 |
| T5.4 | Atacante causa lentidão via queries complexas | Database | 🟡 3 | 2 | 6 |
| T5.5 | Ataque DDoS volumétrico | Infraestrutura | 🔴 5 | 2 | 10 |

**Mitigações existentes:**
- T5.1: Rate limiting planejado (Redis sliding window)
- T5.2: Connection pooling (PgBouncer) + pool limits
- T5.3: Limite de 10 MB por upload, 20 uploads/hora/tenant
- T5.5: Cloudflare Free (DDoS básico)

**Recomendações adicionais:**
- T5.1: **URGENTE** — Implementar rate limiting antes de expor a API
- T5.2: Configurar statement_timeout no PostgreSQL (30s)
- T5.3: Implementar quota de storage por plano
- T5.5: Cloudflare Pro (WAF + DDoS avançado) a partir de 100 clientes

---

### T6 — Elevation of Privilege (Escalação de Privilégio)

| ID | Ameaça | Componente | Impacto | Prob. | Risco |
|----|--------|-----------|:------:|:-----:|:-----:|
| T6.1 | Barbeiro acessa funções de admin (BOLA) | RBAC | 🔴 5 | 3 | **15** |
| T6.2 | Cliente modifica agendamento de outro cliente | Booking API | 🟠 4 | 3 | 12 |
| T6.3 | SQL Injection permite bypass de RLS | Database | 🔴 5 | 1 | 5 |
| T6.4 | Atacante explora JWT `alg: none` para forjar token | Auth Service | 🔴 5 | 2 | 10 |
| T6.5 | Atacante escala privilégio via mass assignment | API | 🟡 3 | 2 | 6 |

**Mitigações existentes:**
- T6.1: RBAC implementado como middleware (roles + permissions)
- T6.2: Validação de customer_id no booking
- T6.3: SQLAlchemy ORM — parameterized queries
- T6.4: JWT library (python-jose) — validação de assinatura
- T6.5: Pydantic v2 — extra=forbid (rejeita campos não definidos)

**Recomendações adicionais:**
- T6.4: **URGENTE** — Adicionar validação explícita: `algorithms=[settings.jwt_algorithm]` (não aceitar lista vazia)

---

## 3. Matriz Consolidada STRIDE

| ID | Ameaça | S | T | R | I | D | E | Risco |
|----|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-----:|
| T4.1 | Cross-tenant data leak | | | | ✅ | | | 🔴 15 |
| T4.2 | IDOR via API | | | | ✅ | | | 🔴 15 |
| T6.1 | Barber escalates to admin | | | | | | ✅ | 🔴 15 |
| T1.1 | Tenant impersonation | ✅ | | | | | | 🔴 15 |
| T4.3 | PII in logs | | | | ✅ | | | 🔴 16 |
| T5.1 | API overload (no rate limit) | | | | | ✅ | | 🔴 16 |
| T2.2 | Price tampering in booking | | ✅ | | | | | 🟠 12 |
| T2.4 | Path traversal in upload | | ✅ | | | | | 🟠 12 |
| T6.2 | Customer modifies other's booking | | | | | | ✅ | 🟠 12 |
| T1.2 | JWT token theft | ✅ | | | | | | 🟠 10 |
| T1.3 | Forged payment webhook | ✅ | | | | | | 🟠 10 |
| T1.5 | Credential stuffing | ✅ | | | | | | 🟠 12 |
| T2.1 | JWT claim tampering | | ✅ | | | | | 🟠 10 |
| T2.3 | Webhook payload forgery | | ✅ | | | | | 🟠 10 |
| T5.5 | Volumetric DDoS | | | | | ✅ | | 🟠 10 |
| T6.4 | JWT alg:none attack | | | | | | ✅ | 🟠 10 |

---

## 4. Recomendações por Prioridade

### 🔴 Críticas (Antes do MVP)
1. Implementar **rate limiting** (Redis sliding window) — T5.1
2. Sanitizar **PII nos logs** (máscara de telefone/email) — T4.3
3. Implementar **RLS** no PostgreSQL — T4.1, T4.2
4. Validar **JWT algorithm** explicitamente — T6.4

### 🟠 Altas (Antes de clientes pagantes)
5. Implementar **CSRF tokens** — T2.2
6. Implementar **audit_logs** append-only — T3.1, T3.2
7. Adicionar **IP allowlist** para webhooks — T1.3
8. Implementar **lockout de login** — T1.5
9. Configurar **Cloudflare WAF** — T5.5

### 🟡 Médias (Escala)
10. Implementar **MFA** para admins — T1.1
11. Usar **RS256** (chave assimétrica) para JWT — T2.1
12. Implementar **device fingerprinting** — T1.2
13. **Bug bounty program** privado — Todos

---

> **Resumo:** A modelagem STRIDE identificou 16 ameaças significativas. As 4 mais críticas (rate limit, PII em logs, RLS, JWT alg) devem ser resolvidas antes do MVP. O modelo de defesa em profundidade da arquitetura mitiga a maioria das ameaças, mas a implementação concreta dos controles é o gap principal.
