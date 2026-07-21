# DEPLOY.md — AGENDA OS Deployment Guide

## 📋 Pré-requisitos

### Servidor
- **SO:** Ubuntu 22.04 LTS (ou superior)
- **CPU:** 1 vCPU (mínimo) | 2+ vCPU (recomendado)
- **RAM:** 2 GB (mínimo) | 4 GB (recomendado)
- **Disco:** 30 GB SSD
- **Provedores:** Hostinger KVM 1 (R$ 29,99/mês), DigitalOcean (US$ 6/mês), Oracle Cloud (Always Free)

### Domínio & DNS
- Domínio registrado (ex: `agendaos.com.br`)
- Acesso ao painel DNS do provedor

### Contas de Serviço
- [Mercado Pago](https://mercadopago.com.br) — Gateway de pagamento
- [Resend](https://resend.com) — E-mail transacional
- [Meta Developers](https://developers.facebook.com) — WhatsApp Cloud API
- [Cloudflare R2](https://cloudflare.com) — Storage
- [UptimeRobot](https://uptimerobot.com) — Monitoramento

---

## 🚀 Deploy Passo a Passo

### 1. Preparar o Servidor

```bash
# Conectar via SSH
ssh root@<IP_DO_SERVIDOR>

# Atualizar sistema
apt update && apt upgrade -y

# Instalar dependências
apt install -y curl git ufw fail2ban ntp

# Instalar Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker --now

# Instalar Docker Compose
apt install -y docker-compose-plugin

# Verificar
docker --version    # >= 24
docker compose version  # >= 2.0
```

### 2. Configurar Firewall

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### 3. Clonar o Projeto

```bash
mkdir -p /opt/agendaos
cd /opt/agendaos
git clone https://github.com/seu-usuario/agendaos.git .
```

### 4. Configurar Variáveis de Ambiente

```bash
# Criar .env.production
cp .env.production.example .env.production
nano .env.production

# ⚠️ Preencher TODOS os placeholders com valores reais
# ⚠️ NUNCA comitar .env.production
```

### 5. Configurar SSL (Let's Encrypt)

```bash
# Instalar certbot
apt install -y certbot

# Parar Nginx se estiver rodando
docker compose -f docker-compose.prod.yml stop nginx 2>/dev/null || true

# Gerar certificado standalone
certbot certonly --standalone -d agendaos.com.br -d *.agendaos.com.br

# Copiar certificados
mkdir -p docker/nginx/ssl
cp /etc/letsencrypt/live/agendaos.com.br/fullchain.pem docker/nginx/ssl/
cp /etc/letsencrypt/live/agendaos.com.br/privkey.pem docker/nginx/ssl/
chmod 600 docker/nginx/ssl/*.pem

# Agendar renovação automática (crontab)
echo "0 0 * * * certbot renew --quiet --post-hook 'docker compose -f /opt/agendaos/docker-compose.prod.yml restart nginx'" | crontab -
```

### 6. Deploy

```bash
cd /opt/agendaos
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 7. Configurar Backup

```bash
chmod +x scripts/backup.sh

# Agendar backup diário às 2h
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/agendaos/scripts/backup.sh >> /var/log/agendaos-backup.log 2>&1") | crontab -
```

### 8. Configurar Monitoramento

1. Acesse [uptimerobot.com](https://uptimerobot.com) → Criar conta gratuita
2. Adicionar monitor:
   - URL: `https://agendaos.com.br/api/v1/health`
   - Intervalo: 5 minutos
   - Alertas: E-mail + Telegram

### 9. Verificar Deploy

```bash
# Status dos containers
docker compose -f docker-compose.prod.yml ps

# Logs
docker compose -f docker-compose.prod.yml logs -f backend

# Health check
curl https://agendaos.com.br/api/v1/health
# → {"status":"healthy","version":"1.1.0"}

# Agentes
curl https://agendaos.com.br/api/v1/agents/health
```

---

## 🔄 Atualizar o Sistema

```bash
cd /opt/agendaos
git pull origin main
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml --profile agents up -d
docker system prune -f
```

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| Container não sobe | `docker compose logs backend` |
| Banco não conecta | Verificar `DB_HOST` no .env.production |
| SSL expirado | `certbot renew --force-renewal` |
| Disco cheio | `docker system prune -af` |
| API lenta | Aumentar `WORKERS` no .env.production |
