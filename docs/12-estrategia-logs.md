# 12 — Estratégia de Logs e Auditoria

---

## 12.1 Filosofia

> "Se não está logado, não aconteceu."

Todo evento relevante do sistema deve ser registrado de forma estruturada, imutável e consultável. Logs são a primeira linha de investigação em incidentes de segurança, disputas de clientes e debugging.

---

## 12.2 O que é Logado

### Eventos de Negócio (Audit Log)

| Categoria | Eventos |
|-----------|---------|
| **Agendamentos** | Criado, cancelado, reagendado, concluído, no-show, check-in |
| **Clientes** | Cadastro, atualização de dados, exclusão (LGPD) |
| **Pagamentos** | Payment intent criado, pago, reembolsado, falhou |
| **Serviços** | Criado, atualizado, removido |
| **Profissionais** | Adicionado, atualizado, removido |
| **Configurações** | Qualquer alteração nas configurações do tenant |
| **Personalização** | Upload de logo, alteração de cores, fontes |

### Eventos de Segurança (Security Log)

| Evento | Dados |
|--------|-------|
| Login (sucesso) | user_id, IP, user_agent, tenant_id |
| Login (falha) | e-mail tentado, IP, user_agent, motivo |
| Logout | user_id, IP |
| Refresh token usado | user_id, IP |
| Refresh token reuso detectado | user_id, IP (possível ataque) |
| Senha alterada | user_id, IP |
| Senha reset solicitada | e-mail, IP |
| Permissão negada (403) | user_id, IP, rota tentada, permissão requerida |
| Cross-tenant access tentado | user_id, tenant_id original, tenant_id alvo |
| Rate limit atingido | IP, endpoint, contagem |

### Eventos de Sistema (System Log)

| Evento | Dados |
|--------|-------|
| Erro 500 | Stack trace, request ID, tenant_id, user_id |
| Timeout | Endpoint, duração, parâmetros |
| Circuit breaker aberto | Serviço, motivo |
| Webhook recebido | Gateway, evento, payload hash |
| Job batch concluído | Tipo de job, registros processados, falhas |
| Deploy realizado | Versão, ambiente, timestamp |

---

## 12.3 Estrutura do Log (JSON)

Todo log segue um schema padronizado:

```json
{
  "timestamp": "2026-07-20T14:30:00.123Z",
  "level": "INFO",
  "logger": "app.booking.service",
  "event": "booking.created",
  "request_id": "req_abc123",
  "tenant_id": "t_xyz",
  "user_id": "user_789",
  "user_role": "admin",
  "ip_address": "189.54.32.10",
  "user_agent": "Mozilla/5.0...",
  "resource_type": "booking",
  "resource_id": "b_456",
  "action": "create",
  "changes": {
    "professional_id": "prof_1",
    "service_id": "svc_2",
    "date": "2026-07-25",
    "time": "14:30"
  },
  "metadata": {
    "source": "admin_panel",
    "duration_ms": 45
  }
}
```

### Campos Obrigatórios

| Campo | Descrição |
|-------|-----------|
| `timestamp` | ISO 8601 com timezone |
| `level` | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `event` | Nome único do evento (snake_case) |
| `request_id` | UUID gerado no API Gateway, propagado em todo o request |
| `tenant_id` | Identificador do tenant (ou "platform") |

### Campos Proibidos (NUNCA logar)

- ✗ Senhas (mesmo hash)
- ✗ Tokens de acesso (JWT)
- ✗ Refresh tokens
- ✗ Números de cartão de crédito
- ✗ CVV
- ✗ Dados completos de pagamento
- ✗ Dados pessoais sensíveis (RG, CPF) — se houver

---

## 12.4 Infraestrutura de Logging

### Stack (MVP)

```
Aplicação
    │
    ├── stdout (structured JSON) ─── Docker logging driver
    │                                      │
    │                                      ▼
    │                              Promtail (log agent)
    │                                      │
    │                                      ▼
    │                              Loki (log aggregation)
    │                                      │
    │                                      ▼
    │                              Grafana (visualization)
    │
    └── Audit DB (PostgreSQL) ─── tabela audit_logs
                                       │
                                       ▼
                                  Painel de auditoria
                                  (admin visualiza logs do seu tenant)
```

### Por que duas abordagens?

| Abordagem | Uso |
|-----------|-----|
| **stdout → Loki** | Logs de sistema, debugging, métricas, alertas |
| **Audit DB → PostgreSQL** | Logs de negócio, auditoria, compliance, consulta pelo admin |

**Logs em stdout** são efêmeros (retidos por 30 dias).  
**Logs em banco** são permanentes (retidos por 5 anos).

---

## 12.5 Retenção de Logs

| Tipo | Local | Retenção | Justificativa |
|------|-------|----------|---------------|
| Application logs | Loki | 30 dias | Debugging e operação |
| Audit logs (negócio) | PostgreSQL | 5 anos | Compliance, disputas |
| Security logs | PostgreSQL | 5 anos | LGPD, investigações |
| Access logs (CDN) | Cloudflare | 30 dias | Análise de tráfego |
| Backup de logs | S3/R2 | 5 anos | Recuperação de desastres |

### Política de Expurgo (Automático)

- **Audit logs > 5 anos** → Exportar para S3 Glacier (cold storage) e deletar do banco
- **Application logs > 30 dias** → Deletados automaticamente pelo Loki
- **Logs de tenants deletados** → Excluídos junto com os dados do tenant (após 90 dias de grace period)

---

## 12.6 Consulta de Logs

### Pelo Admin do Tenant
- Acessa apenas logs do seu próprio tenant
- Filtros: data, tipo de evento, usuário
- Exportação: CSV (limitado a 10.000 registros)

### Pelo Super Admin
- Acesso a todos os tenants
- Filtros avançados (cross-tenant)
- Exportação sem limite
- Visualização de métricas agregadas

### Via Grafana (Operação)
- Dashboards de erro rate, latência, volume de requests
- Alertas baseados em padrões de log
- Busca full-text com Loki (LogQL)

---

## 12.7 Auditoria e Compliance

### Trilha de Auditoria Imutável

- Registros de auditoria são **append-only** (sem UPDATE ou DELETE)
- Qualquer tentativa de modificação é detectada (checksum/hash chain opcional)
- Em caso de investigação, logs podem ser exportados com assinatura digital

### Registro de Consentimento (LGPD)

Quando um cliente aceita termos/política de privacidade:

```json
{
  "event": "consent.granted",
  "tenant_id": "t_xyz",
  "user_id": "user_789",
  "consent_type": "privacy_policy",
  "consent_version": "2.1",
  "ip_address": "...",
  "user_agent": "...",
  "timestamp": "..."
}
```

Este registro é a prova legal de que o consentimento foi dado.

---

## 12.8 Exemplo: Fluxo de um Evento de Auditoria

```
1. Admin cria novo serviço via painel
2. BFF Admin recebe request (request_id gerado)
3. BFF chama Scheduler Service
4. Scheduler Service:
   a. Valida entrada
   b. Cria registro no banco
   c. Emite log:
      logger.info("service.created",
                   tenant_id=..., user_id=...,
                   resource_id=..., changes=...)
   d. Insere na tabela audit_logs:
      INSERT INTO audit_logs (...)
   e. Retorna sucesso
5. BFF retorna para o frontend

6. (Paralelo) Promtail coleta stdout → Loki
7. Admin pode ver a ação no painel de auditoria
```

---

> **Princípio:** Logs não são apenas para debugging. São a memória do sistema, a prova em disputas, o escudo em investigações e o requisito legal para compliance. Um sistema sem logs é um sistema cego.
