# 11 — Estratégia de Segurança

---

## 11.1 Princípios Fundamentais

1. **Defense in Depth** — Múltiplas camadas de proteção
2. **Least Privilege** — Cada componente acessa apenas o que precisa
3. **Secure by Default** — Configurações padrão são as mais seguras
4. **Zero Trust** — Nenhuma confiança implícita, sempre verificar
5. **Fail Secure** — Falhas resultam em negação de acesso, nunca em permissão
6. **Auditability** — Toda ação sensível é registrada

---

## 11.2 Autenticação

### Fluxo de Login

```
  Cliente
    │
    ├── POST /api/v1/auth/login
    │   Body: { email, password, tenant_id? }
    │
    ▼
  Auth Service
    │
    ├── Valida credenciais (bcrypt compare)
    ├── Verifica se usuário pertence ao tenant
    ├── Verifica se conta está ativa
    │
    ▼
  Resposta:
    {
      "access_token": "eyJ...",     // JWT, expira em 15 min
      "refresh_token": "rt_...",    // Opaque, expira em 7 dias
      "expires_in": 900,
      "user": { ... }
    }
```

### JWT Claims

```json
{
  "sub": "user_789",
  "tenant_id": "t_123",
  "role": "admin",
  "permissions": ["booking:*", "service:*", "professional:*"],
  "iat": 1690000000,
  "exp": 1690000900,
  "jti": "unique-token-id"
}
```

### Refresh Token

- Opaque string (não JWT)
- Armazenado em httpOnly, Secure, SameSite=Strict cookie
- Rotacionado a cada uso (refresh token rotation)
- Reuse detection: se um token já usado for reapresentado, invalida toda a família

### Segurança de Senhas

- Hash: bcrypt com cost factor ≥ 12
- Política: mínimo 8 caracteres, sem requisitos complexos (NIST 800-63)
- Verificação contra lista de senhas comuns (Have I Been Pwned API)
- Lockout: 5 tentativas → bloqueio de 15 minutos

---

## 11.3 Autorização (RBAC)

### Modelo

```
User ──┬── Role ──┬── Permissions
       │           │
       │           ├── booking:read
       │           ├── booking:write:own
       │           ├── booking:write:any
       │           ├── service:read
       │           ├── service:write
       │           ├── professional:read
       │           ├── professional:write
       │           ├── report:read
       │           ├── settings:read
       │           ├── settings:write
       │           └── ...
       │
       └── tenant_id (escopo)
```

### Roles Pré-definidas

| Role | Permissões | Quem |
|------|-----------|------|
| **customer** | booking:read:own, booking:write:own, profile:read:own | Cliente final |
| **barber** | booking:read:assigned, schedule:read:own, customer:read | Barbeiro |
| **receptionist** | booking:*, schedule:read:any, customer:read, checkin | Recepcionista |
| **admin** | *:* (dentro do tenant) | Dono/Gerente |
| **super_admin** | *:*:* (cross-tenant) | Nós (CTO) |

### Enforcement

- **Middleware de autorização** em cada rota
- Decorators/Policies que verificam permissão necessária
- Fallback: se permissão não especificada → negar (deny by default)

---

## 11.4 Proteção contra Ataques Comuns (OWASP Top 10)

### A01 — Broken Access Control
- RBAC implementado em middleware, não no frontend
- Validação de pertencimento de recurso ao tenant em TODA query
- Testes automatizados para cross-tenant access

### A02 — Cryptographic Failures
- TLS 1.3 everywhere
- Dados sensíveis criptografados em repouso (campo `encrypted_data` via AES-256-GCM)
- Chaves gerenciadas via Vault / environment variables

### A03 — Injection
- **SQL Injection:** ORM com parameterized queries (SQLAlchemy) — NUNCA string interpolation
- **NoSQL Injection:** Validação de tipos com Pydantic
- **Command Injection:** Nenhuma execução de comandos do sistema com input do usuário

### A04 — Insecure Design
- Threat modeling antes de implementar features sensíveis
- Security review em PRs que envolvem auth, pagamentos, dados pessoais

### A05 — Security Misconfiguration
- Headers de segurança obrigatórios:
  ```
  Content-Security-Policy: default-src 'self'; ...
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  ```
- CORS configurado explicitamente (sem wildcard `*`)

### A06 — Vulnerable Components
- Dependabot / Renovate para atualização automática de dependências
- `pip-audit` / `npm audit` no CI/CD
- Política: atualizar em até 7 dias após divulgação de CVE crítico

### A07 — Authentication Failures
- JWT com expiração curta (15 min)
- Refresh token rotation
- Rate limit em endpoints de login (5 req/min por IP)
- Sem "username enumeration" (mensagem genérica: "Credenciais inválidas")

### A08 — Software and Data Integrity Failures
- Verificação de assinatura HMAC em webhooks
- Checksum de uploads (não confiar em Content-Type)
- Dependências pinadas com hash (pip: `--require-hashes`)

### A09 — Logging and Monitoring Failures
- Logs estruturados em JSON (veja doc 12 — Estratégia de Logs)
- Alertas para anomalias (múltiplas falhas de login, acesso cross-tenant)
- Logs NUNCA contêm senhas, tokens ou dados de cartão

### A10 — Server-Side Request Forgery (SSRF)
- Validação de URLs fornecidas pelo usuário
- Bloqueio de IPs internos/privados
- Timeout em requisições externas

---

## 11.5 LGPD — Privacy by Design

### Dados Pessoais Coletados

| Dado | Finalidade | Base Legal | Retenção |
|------|-----------|------------|----------|
| Nome | Identificação no agendamento | Execução de contrato | 5 anos após última interação |
| Telefone | Confirmação e lembretes | Execução de contrato + Consentimento | 5 anos |
| E-mail | Confirmação e marketing | Consentimento | 5 anos ou até revogação |
| Histórico de agendamentos | Operação do negócio | Legítimo interesse | 5 anos |
| Fotos (galeria) | Portfólio do profissional | Consentimento (do profissional) | Até exclusão |
| IP / Logs de acesso | Segurança | Legítimo interesse | 1 ano |
| Cookies de analytics | Medição de audiência | Consentimento | 13 meses |

### Direitos do Titular (Implementados)

| Direito | Implementação |
|---------|--------------|
| Acesso | Botão "Exportar meus dados" → JSON/CSV |
| Correção | Cliente edita dados no perfil |
| Exclusão | Soft delete → Hard delete após 30 dias (jobs batch) |
| Portabilidade | Exportação estruturada (.json) |
| Revogação de consentimento | Central de preferências |
| Explicação de decisão automatizada | Não aplicável (sem decisões automatizadas) |

### Encarregado de Dados (DPO)

- Canal: `privacidade@barbersaas.com.br`
- Exibido na política de privacidade
- Responsável por responder requisições em até 15 dias

---

## 11.6 Segurança de Uploads

### Política de Upload

| Regra | Valor |
|-------|-------|
| Tipos permitidos (imagens) | PNG, JPG, JPEG, WebP, SVG, GIF |
| Tipos permitidos (docs) | Nenhum (apenas imagens) |
| Tamanho máximo | 10 MB por arquivo |
| Validação de tipo | Magic bytes (não confiar em extensão ou MIME type) |
| Scan de malware | ClamAV (opcional, se disponível) |
| Armazenamento | S3/R2 com acesso não-público direto |
| Nome do arquivo | UUID gerado pelo servidor (não usar nome original) |
| Processamento | Assíncrono via fila |

### SVG (caso especial)

- SVGs são perigosos (podem conter JavaScript)
- Sanitização obrigatória via `defusedxml` + whitelist de tags
- Ou: converter SVG para PNG no upload e descartar original

---

## 11.7 Rate Limiting

| Endpoint | Limite | Janela | Motivo |
|----------|--------|--------|--------|
| POST /auth/login | 5 | 1 min | Anti brute-force |
| POST /auth/forgot-password | 3 | 10 min | Anti enumeração |
| POST /bookings (público) | 10 | 1 min por IP | Anti spam |
| Todas as APIs | 100 | 1 min por IP | Proteção geral |
| APIs admin | 300 | 1 min por tenant | Uso legítimo mais alto |
| Upload | 20 | 1 hora por tenant | Anti abuso de storage |

Implementado via Redis (sliding window ou token bucket).

---

## 11.8 Gestão de Segredos

### Ambiente de Desenvolvimento
- `.env` (não versionado — está no `.gitignore`)
- `.env.example` (template versionado sem valores reais)

### Ambiente de Produção
- Secrets injetados via Kubernetes Secrets
- Ou: HashiCorp Vault (para escala maior)
- Rotação: tokens de API rotacionados a cada 90 dias

### O que NUNCA fazer
- ❌ Secrets hardcoded no código
- ❌ Secrets no repositório Git
- ❌ Secrets em logs
- ❌ Secrets compartilhados entre ambientes
- ❌ Secrets em mensagens de erro

---

## 11.9 Testes de Segurança

### No CI/CD (Automático)

| Ferramenta | O que verifica |
|------------|---------------|
| `bandit` | Vulnerabilidades em código Python |
| `safety` / `pip-audit` | Dependências Python com CVEs |
| `npm audit` | Dependências JS com CVEs |
| `trivy` | Vulnerabilidades em imagem Docker |
| `zap-baseline` | OWASP ZAP scan (DAST leve) |

### Antes de Release Maior

- OWASP ZAP full scan
- Revisão manual de segurança em mudanças de auth/pagamento
- Verificação de headers de segurança

### Anual

- Pentest externo (empresa especializada)
- Revisão de conformidade LGPD

---

## 11.10 Resposta a Incidentes

### Classificação

| Severidade | Exemplo | Tempo de Resposta |
|-----------|---------|-------------------|
| **Crítica** | Vazamento de dados, acesso cross-tenant | Imediato (qualquer hora) |
| **Alta** | Bypass de autenticação, SQLi | < 4 horas |
| **Média** | XSS, CSRF em área logada | < 24 horas |
| **Baixa** | Informação em headers, falta de rate limit | Próximo sprint |

### Processo

1. **Detecção** — Alerta ou reporte
2. **Contenção** — Isolar sistema afetado, revogar tokens
3. **Investigação** — Logs, timeline, escopo
4. **Remediação** — Corrigir vulnerabilidade
5. **Recuperação** — Restaurar operação normal
6. **Post-mortem** — Documentar aprendizado, melhorar processos
7. **Notificação** — ANPD (LGPD) em até 48h se dados pessoais envolvidos

---

> **Princípio:** Segurança não é um checklist, é um processo contínuo. Cada linha de código é escrita com a mentalidade: "O que um atacante poderia fazer com isso?" A arquitetura foi desenhada para que uma falha em uma camada seja contida pelas outras (defense in depth).
