# 06 — Security Checklist (Checklist de Produção)

> Checklist de verificação de segurança antes de cada deploy em produção.  
> Baseado em: OWASP ASVS, CIS Controls, NIST CSF.

---

## 1. Antes do Primeiro Deploy (MVP)

### Autenticação e Sessões
- [ ] SECRET_KEY é única, aleatória e ≥ 32 caracteres (não é o default)
- [ ] JWT `algorithm` é validado explicitamente (rejeita `alg: none`)
- [ ] Access token expira em ≤ 15 minutos
- [ ] Refresh token é opaque (hash SHA-256 armazenado), não JWT
- [ ] Senhas hash com bcrypt (cost ≥ 12)
- [ ] Login retorna mensagem genérica: "Credenciais inválidas" (sem distinguir email vs senha)
- [ ] Lockout após 5 tentativas de login (bloqueio de 15 minutos)

### Autorização
- [ ] RBAC implementado em middleware (não apenas no frontend)
- [ ] Row-Level Security ativado em TODAS as tabelas de negócio
- [ ] Testes cross-tenant implementados e passando
- [ ] Tentativa de acesso cross-tenant gera log de segurança

### API Security
- [ ] Rate limiting implementado (Redis sliding window)
- [ ] Tamanho máximo de payload: 5 MB (global), 10 MB (upload)
- [ ] CORS configurado com origens explícitas (sem wildcard `*`)
- [ ] Todos os endpoints state-changing exigem CSRF token (ou SameSite=Strict)
- [ ] Input validation com Pydantic (extra=forbid)
- [ ] Output encoding adequado (FastAPI + JSON)

### Headers de Segurança
- [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY`
- [ ] `Content-Security-Policy` (com nonce, sem unsafe-inline em produção)
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy: camera=(), microphone=(), geolocation=()`

### Banco de Dados
- [ ] PostgreSQL: `ssl=on` para conexões
- [ ] Usuário da aplicação tem privilégios mínimos (sem SUPERUSER, sem DROP TABLE)
- [ ] RLS policies testadas
- [ ] Connection pooling configurado (PgBouncer ou built-in)
- [ ] Backups automáticos configurados e testados

### Infraestrutura
- [ ] Redis com senha (`requirepass`)
- [ ] PostgreSQL com senha forte
- [ ] Docker: containers sem `--privileged`
- [ ] Docker: imagens com tag específica (não `latest`)
- [ ] `.env` NÃO versionado no Git
- [ ] `.gitignore` inclui `.env`, `*.pem`, `*.key`
- [ ] Portas expostas apenas as necessárias (80, 443)
- [ ] Firewall: VPS com apenas SSH, HTTP, HTTPS

### CI/CD
- [ ] `bandit` (SAST) no pipeline
- [ ] `pip-audit` / `npm audit` no pipeline
- [ ] Tests passam antes do deploy
- [ ] Não é possível fazer push direto na `main` (requer PR)
- [ ] Variáveis de ambiente injetadas pelo CI, não hardcoded

### Logs
- [ ] Logs em JSON estruturado
- [ ] Logs NUNCA contêm: senhas, tokens, dados de cartão
- [ ] PII sanitizada (telefone: `+5511****9999`, email: `j***@email.com`)
- [ ] Audit log (tabela `audit_logs`) para ações sensíveis
- [ ] Log level: INFO em produção (DEBUG apenas em dev)

### LGPD
- [ ] Política de Privacidade publicada
- [ ] Checkbox de consentimento no fluxo de agendamento (não pré-marcado)
- [ ] Registro de consentimento (tabela `consents`)
- [ ] Canal do DPO visível (privacidade@...)

### Deploy
- [ ] TLS 1.3 ativo (verificar com SSL Labs)
- [ ] Health checks respondendo (`/health/live`, `/health/ready`)
- [ ] DNS propagado e resolvendo
- [ ] Cloudflare proxy ativo (laranja)
- [ ] Backup executado com sucesso nas últimas 24h

---

## 2. Checklist Recorrente (Mensal)

- [ ] Revisar logs de segurança (cross-tenant, falhas de login)
- [ ] Testar restore de backup
- [ ] Atualizar dependências com CVEs (Dependabot)
- [ ] Revisar permissões de usuários (princípio do menor privilégio)
- [ ] Verificar expiração de certificados SSL
- [ ] Revisar rate limits (ajustar se necessário)
- [ ] Verificar espaço em disco do servidor (> 20% livre)
- [ ] Rodar `pip-audit` e `npm audit` manualmente

---

## 3. Checklist Trimestral

- [ ] Revisar Risk Register (atualizar scores)
- [ ] Atualizar Threat Model (novas features?)
- [ ] Simular incidente (tabletop exercise)
- [ ] Revisar política de senhas
- [ ] Rotacionar secrets (API keys, webhook secrets)
- [ ] Revisar configurações do Cloudflare
- [ ] Atualizar documentação de segurança

---

## 4. Checklist Anual

- [ ] Pentest externo (empresa terceira)
- [ ] Revisão completa de conformidade LGPD
- [ ] Atualizar DPIA (Relatório de Impacto)
- [ ] Treinamento de segurança (mesmo que solo)
- [ ] Revisão de arquitetura de segurança
- [ ] Teste de disaster recovery completo
- [ ] Atualizar plano de continuidade do negócio

---

## 5. Pré-Deploy (Cada Release)

- [ ] Todos os testes passam
- [ ] Lint + Type Check sem erros
- [ ] SAST scan sem issues críticas
- [ ] Dependency audit sem vulnerabilidades HIGH/CRITICAL
- [ ] Migration testada em staging
- [ ] Rollback planejado documentado
- [ ] CHANGELOG atualizado

---

> **Resumo:** O checklist cobre todas as fases do ciclo de vida: antes do primeiro deploy (52 itens), manutenção recorrente (mensal/trimestral/anual), e pré-deploy de cada release. Seguir este checklist reduz significativamente o risco de incidentes de segurança em produção.
