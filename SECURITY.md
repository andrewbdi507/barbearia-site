# SECURITY.md — AGENDA OS Security Guide

## 🔒 Princípios

- **Zero Trust:** Nenhum serviço confia em outro implicitamente
- **Least Privilege:** Cada container tem acesso mínimo necessário
- **Defense in Depth:** Múltiplas camadas de proteção
- **OWASP Top 10:** Seguimos as melhores práticas
- **Logs sem PII:** Dados sensíveis nunca vão para logs

---

## 🛡️ Camadas de Segurança

### 1. Rede

```bash
# Firewall (UFW)
ufw default deny incoming
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Fail2ban
apt install fail2ban -y
# Config: /etc/fail2ban/jail.local
[jail]
enabled = true
bantime = 3600
maxretry = 5

# Docker — portas internas apenas
# docker-compose.prod.yml já configura:
# - PostgreSQL: 127.0.0.1:5432 (não exposto)
# - Redis: apenas rede interna
# - Backend: 127.0.0.1:8000 (via Nginx)
```

### 2. Autenticação

- **JWT** com Argon2id (state-of-art password hashing)
- Tokens curtos: 7 dias access, 30 dias refresh
- Brute force protection: 5 tentativas → bloqueio 15 min
- Rate limiting: 100 req/min por IP
- CORS restrito a domínios explícitos

### 3. Dados

- **Senhas:** Argon2id (memory-hard, resistente a GPU)
- **PII:** Criptografado em repouso (campo `encrypted_*`)
- **Backups:** Criptografados antes do upload (AES-256)
- **Logs:** Mascaramento automático de emails, telefones, CPF
- **HTTPS:** TLS 1.2+ apenas, HTTP → HTTPS redirect forçado

### 4. Aplicação

```python
# Headers de segurança (configurados no Nginx)
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Permissions-Policy "geolocation=(), camera=(), microphone=()";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 5. Container Security

```yaml
# docker-compose.prod.yml
services:
  backend:
    security_opt:
      - no-new-privileges:true
    read_only: true  # Sistema de arquivos somente leitura
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

---

## 🔑 Gerenciamento de Chaves

| Chave | Rotação | Armazenamento |
|-------|---------|---------------|
| SECRET_KEY | 90 dias | .env.production |
| JWT keys | 30 dias | .env.production |
| API keys (Stripe, etc.) | Conforme provedor | Variáveis de ambiente |
| Senhas de banco | 90 dias | .env.production |

**✅ NUNCA:**
- Commitar `.env.production` no Git
- Hardcodear credenciais no código
- Compartilhar chaves em chat/e-mail
- Usar senhas padrão em produção

---

## 🚨 Plano de Resposta a Incidentes

### Vazamento de Dados
1. Isolar sistema (modo manutenção)
2. Rotacionar TODAS as chaves
3. Identificar origem do vazamento
4. Notificar usuários afetados
5. Reportar à ANPD (LGPD, se aplicável)

### Ataque de Força Bruta
1. Fail2ban bloqueia automaticamente
2. Rate limiting previne abuso
3. Monitorar logs (`docker compose logs backend | grep "failed_login"`)

### Vulnerabilidade Crítica
1. Aplicar patch de segurança
2. Testar em staging
3. Deploy com `./scripts/deploy.sh`
4. Verificar health checks

---

## ✅ Checklist de Segurança (Go Live)

- [ ] `.env.production` com valores reais (não placeholders)
- [ ] `SECRET_KEY` com 64+ caracteres aleatórios
- [ ] `DB_PASSWORD` forte (32+ caracteres)
- [ ] SSL/HTTPS ativo e renovação automática
- [ ] Firewall (UFW) configurado
- [ ] Fail2ban ativo
- [ ] Headers de segurança no Nginx
- [ ] CORS restrito a domínios de produção
- [ ] Rate limiting ativo
- [ ] Brute force protection ativa
- [ ] Logs sem dados sensíveis
- [ ] Backup automático e criptografado
- [ ] Monitoramento ativo (UptimeRobot)
- [ ] Dependências atualizadas (`pip list --outdated`)
- [ ] Docker images sem vulnerabilidades críticas (`docker scout`)
