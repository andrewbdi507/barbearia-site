# SECURITY_OPERATIONS.md — Operações de Segurança

## Política de Segurança

A plataforma Barbershop SaaS segue princípios de **Security by Design** e **Defense in Depth**.

---

## 1. HTTPS e TLS

### Configuração

| Configuração | Valor |
|-------------|-------|
| TLS mínimo | 1.2 (1.3 preferencial) |
| Ciphers | TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256 |
| HSTS | max-age=63072000; includeSubDomains; preload |
| Certificado | Let's Encrypt (origin) + Cloudflare (edge) |
| Renovação | Automática (certbot renew cron) |

### Verificação

```bash
# Testar SSL
curl -I https://app.barbershop.com | grep -i strict
# Deve retornar: Strict-Transport-Security: max-age=63072000; includeSubDomains; preload

# SSL Labs
# https://www.ssllabs.com/ssltest/analyze.html?d=app.barbershop.com
```

---

## 2. Security Headers

| Header | Valor |
|--------|-------|
| `Strict-Transport-Security` | max-age=63072000; includeSubDomains; preload |
| `X-Content-Type-Options` | nosniff |
| `X-Frame-Options` | DENY |
| `X-XSS-Protection` | 1; mode=block |
| `Referrer-Policy` | strict-origin-when-cross-origin |
| `Permissions-Policy` | camera=(), microphone=(), geolocation=() |
| `Content-Security-Policy` | default-src 'self'; script-src 'self' 'unsafe-inline' ... |
| `Server` | (removido) |

**Arquivo:** `docker/nginx/default.conf`

---

## 3. Rate Limiting

| Zona | Limite | Descrição |
|------|--------|-----------|
| `api_limit` | 100 req/s por IP | API geral |
| `auth_limit` | 5 req/min por IP | Login/Registro |
| `webhook_limit` | 50 req/s por IP | Webhooks de pagamento |

Implementado via Nginx `limit_req_zone`. Futuro: Redis sliding window para limites por tenant.

---

## 4. Secrets Management

### Princípios

- **NUNCA** commitar secrets no repositório
- Usar `.env.production` como template (valores placeholder)
- Secrets reais via:
  - HashiCorp Vault (produção)
  - AWS Secrets Manager (AWS)
  - GitHub Secrets (CI/CD)
  - Docker secrets (Swarm)

### Rotação de Chaves

| Chave | Frequência | Procedimento |
|-------|:----------:|-------------|
| SECRET_KEY | 90 dias | 1. Gerar nova chave 2. Atualizar .env 3. Restart API 4. Invalidar tokens antigos |
| JWT signing key | 90 dias | Rotação gradual (aceitar chave antiga + nova por 24h) |
| DB password | 180 dias | 1. Criar novo user 2. Migrar conexões 3. Remover user antigo |
| API keys (gateways) | 365 dias | Atualizar no dashboard do gateway → atualizar .env |

---

## 5. Proteção contra Ataques

### Brute Force (Login)

```python
# app/modules/auth/security/rate_limiter.py
- 5 tentativas por IP a cada 15 minutos
- Bloqueio progressivo: 1min → 5min → 15min → 1h
- Notificação ao admin após 20 falhas
```

### SQL Injection

- SQLAlchemy ORM com parâmetros bind ($1, $2) — prevenção nativa
- NUNCA concatenar strings em queries SQL

### XSS

- CSP header restritivo (inline scripts bloqueados em produção)
- React escapa output por padrão
- Validação de input em todos os endpoints

### CSRF

- SameSite=Strict nos cookies de refresh token
- Double-submit cookie pattern (planejado fase 2)

---

## 6. LGPD / Compliance

### Dados Pessoais

| Dado | Armazenamento | Retenção |
|------|:------------:|:--------:|
| Nome, email, telefone | PostgreSQL (encriptado em disco) | Até deleção da conta |
| Senha | Argon2id hash | — |
| Logs de auditoria | `audit_logs` table | 5 anos |
| Dados de pagamento | Gateway (NUNCA no nosso banco) | — |

### Direitos do Titular

- **Exportação**: `GET /api/v1/customers/{id}/export` — JSON com todos os dados
- **Anonimização**: `POST /api/v1/customers/{id}/anonymize` — Substitui PII por hash
- **Deleção**: `DELETE /api/v1/customers/{id}` — Soft delete + anonimização

---

## 7. Auditoria

### Eventos Auditados

Todo evento de auditoria registra:
```json
{
  "timestamp": "2026-07-20T14:30:00Z",
  "workspace_id": "ws_...",
  "user_id": "usr_...",
  "action": "booking.cancelled",
  "ip": "203.0.113.1",
  "user_agent": "Mozilla/5.0...",
  "details": {"booking_id": "bkg_...", "reason": "customer_request"}
}
```

### Consulta

```sql
SELECT * FROM audit_logs
WHERE workspace_id = 'ws_...'
AND created_at > now() - interval '30 days'
ORDER BY created_at DESC;
```

---

## 8. Firewall e Rede

### Regras (IPTables / Security Group)

| Porta | Origem | Destino | Ação |
|-------|--------|---------|------|
| 80, 443 | 0.0.0.0/0 | server | ALLOW |
| 22 | IPs internos | server | ALLOW |
| 5432, 6379 | 127.0.0.1 | server | ALLOW |
| 9090, 3000 | IPs internos | server | ALLOW |
| Todas outras | 0.0.0.0/0 | server | DENY |

---

## 9. Checklist de Segurança (Mensal)

- [ ] Revisar dependências (`pip-audit`, `pnpm audit`)
- [ ] Verificar certificados SSL (expiração)
- [ ] Rodar scan de vulnerabilidades (Trivy)
- [ ] Revisar logs de auditoria (ações suspeitas)
- [ ] Testar restore de backup
- [ ] Rotacionar secrets (se necessário)
- [ ] Revisar acessos (quem tem acesso ao servidor?)
- [ ] Verificar configurações de CORS
- [ ] Testar rate limiting
