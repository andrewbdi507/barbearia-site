# 05 — Disaster Recovery & Business Continuity

> Plano de continuidade do negócio e recuperação de desastres.  
> Adaptado para SaaS com 1 desenvolvedor.

---

## 1. Objetivos de Recuperação

| Métrica | MVP | V1 (100 clientes) | V2 (1.000 clientes) |
|---------|:---:|:---:|:---:|
| **RPO** (Recovery Point Objective) | < 1 hora | < 5 minutos | < 1 minuto |
| **RTO** (Recovery Time Objective) | < 4 horas | < 1 hora | < 15 minutos |
| **Backup diário** | Sim (script cron) | Sim (automático) | Sim (WAL contínuo) |
| **Disaster Recovery Site** | Não | Read replica | Multi-AZ + cross-region |

---

## 2. Cenários de Desastre e Resposta

### Cenário 1: Falha do Banco de Dados

```
Causas: Corrupção de dados, falha de hardware, erro humano (DROP TABLE)

Detecção:
  - Health check /ready falha
  - Erros 500 generalizados
  - Alerta: "database connection refused"

Resposta:
  1. Verificar se é falha de conexão ou corrupção
  2. Se conexão: verificar processo PostgreSQL, reiniciar se necessário
  3. Se corrupção: INICIAR PROCEDIMENTO DE RESTORE

Procedimento de Restore:
  a. Provisionar nova instância PostgreSQL
  b. Restaurar último backup full (pg_restore)
  c. Aplicar WAL archives até ponto desejado (PITR)
  d. Validar integridade (contagem de registros críticos)
  e. Apontar aplicação para nova instância
  f. Verificar operação normal

Tempo estimado: 1-4 horas (MVP) / 30 min (V2 com read replica)
RPO: < 1 hora (MVP com backup diário + bin logs)
```

### Cenário 2: Falha do Redis

```
Causas: Memória esgotada, crash do processo

Detecção:
  - Rate limiting para de funcionar
  - Sessões inválidas (usuários deslogados)
  - Cache misses generalizados

Impacto:
  - Rate limiting: ❌ offline (risco de abuso)
  - Sessões: ❌ usuários precisam reautenticar
  - Cache: ⚠️ performance degradada (banco assume)
  - Filas (Streams): ❌ notificações não enviadas

Resposta Imediata:
  1. Reiniciar Redis (docker compose restart redis)
  2. Verificar saúde (redis-cli PING)
  3. Se não resolver: provisionar nova instância

Aplicação sem Redis:
  - Rate limiting: desabilitado (⚠️ risco)
  - Autenticação: fallback para validação JWT sem cache
  - Notificações: reconectar consumers ao novo Redis

Mitigação (V1+):
  - Redis sentinel para failover automático
  - Managed Redis (AWS ElastiCache / DigitalOcean)
```

### Cenário 3: Falha do Gateway de Pagamento

```
Causas: Indisponibilidade do Stripe/MercadoPago, bloqueio de conta

Detecção:
  - Erros em chamadas de API do gateway
  - Webhooks não recebidos
  - Circuit breaker aberto

Resposta:
  1. Verificar status page do gateway
  2. Se gateway offline:
     a. Agendamento SEM pagamento (MVP — sem pagamento)
     b. V1+: ativar gateway secundário (fallback automático)
     c. Modo "pague depois": agendamento confirmado com pagamento pendente
  3. Comunicar tenants no painel admin: "Pagamentos temporariamente indisponíveis"
  4. Quando gateway voltar: processar pagamentos pendentes

Mitigação (V1+):
  - 2+ gateways configurados (Stripe + MercadoPago)
  - Modo offline: agendamento confirmado, pagamento em até 24h
  - Circuit breaker evita cascata de erros
```

### Cenário 4: Falha do WhatsApp (Meta Cloud API)

```
Causas: API da Meta offline, token expirado, bloqueio de conta

Detecção:
  - Notificações WhatsApp falhando
  - Métrica: whatsapp_failure_rate > 10%

Impacto:
  - Clientes não recebem confirmação/lembrete
  - Experiência degradada (mas agendamento funciona)

Resposta:
  1. Verificar status da Meta API
  2. Verificar validade do token
  3. Se falha temporária: mensagens entram na fila (retry)
  4. Se falha prolongada (> 1h):
     a. Notificar tenants: "WhatsApp temporariamente indisponível"
     b. Clientes podem ver agendamento no site (perfil)
     c. Fallback para SMS (se configurado)

Mitigação (V2+):
  - Multicanal: WhatsApp + Email + SMS
  - Se WhatsApp falha, email e SMS continuam funcionando
```

### Cenário 5: Falha do Servidor (VPS)

```
Causas: Crash do servidor, falha de hardware, ataque

Detecção:
  - Monitoramento externo (UptimeRobot/Cloudflare) detecta offline
  - Health checks param de responder

Resposta:
  1. Acessar console do provedor (DigitalOcean/Hostinger)
  2. Tentar reiniciar servidor
  3. Se não recuperar: provisionar nova VPS
  4. Restaurar via Docker Compose + backup
  5. Apontar DNS para novo IP
  6. Restaurar banco de dados do backup

Tempo estimado: 1-4 horas (MVP com VPS única)

Mitigação (V2+):
  - Kubernetes com múltiplos nós
  - Multi-AZ no AWS
  - Infraestrutura como Código (Terraform) para rebuild rápido
```

### Cenário 6: Ataque DDoS

```
Causas: Ataque volumétrico ou de camada 7

Detecção:
  - Cloudflare analytics: spike de tráfego
  - Latência elevada
  - Erros 502/503

Resposta:
  - MVP: Cloudflare Free oferece proteção DDoS básica
  - Ativar "Under Attack Mode" no Cloudflare
  - Bloquear países/regiões de origem do ataque
  - Rate limiting agressivo
  - Se necessário: escalar para Cloudflare Pro

Mitigação (V2+):
  - Cloudflare Pro/Enterprise com WAF
  - AWS Shield Advanced (se em AWS)
```

### Cenário 7: Ransomware

```
Causas: Malware que criptografa dados do servidor

Detecção:
  - Arquivos com extensão desconhecida
  - Sistema lento ou inacessível
  - Mensagem de resgate

Resposta:
  1. ISOLAR IMEDIATAMENTE: desligar servidor da rede
  2. NÃO PAGAR RESGATE
  3. Provisionar nova VPS limpa
  4. Restaurar backup mais recente
  5. Verificar integridade dos dados
  6. Apontar DNS para novo servidor
  7. Investigar vetor de entrada (log, vulnerabilidade)

Prevenção:
  - Backups imutáveis (S3 Object Lock)
  - MFA em todos os acessos (VPS, GitHub, Cloudflare)
  - Atualizações automáticas de segurança
  - Princípio do menor privilégio (sem root desnecessário)
```

### Cenário 8: Erro Humano (DELETE/UPDATE sem WHERE)

```
Causas: Comando SQL executado incorretamente, migration mal testada

Detecção:
  - Dados desaparecem
  - Clientes reportam perda de informações

Resposta:
  1. Identificar momento exato do erro (logs)
  2. Restaurar banco para ponto anterior (PITR via WAL)
  3. Verificar dados restaurados
  4. Se necessário: mesclar dados novos (pós-erro) com restore

Prevenção:
  - SEMPRE testar migrations em staging
  - Backup antes de qualquer operação manual no banco
  - Usar transações (BEGIN/ROLLBACK) para operações manuais
  - Configurar `SAFE_UPDATES` no MySQL ou equivalente
```

---

## 3. Procedimento de Restore Completo (Runbook)

```
EM CASO DE DESASTRE TOTAL (servidor + banco perdidos):

1. PROVISIONAR (30 min)
   □ Nova VPS (DigitalOcean / Hostinger)
   □ Instalar Docker + Docker Compose
   □ Clonar repositório (git clone)
   □ Configurar .env com secrets

2. RESTAURAR BANCO (30 min)
   □ Baixar último backup do S3/R2
   □ pg_restore no PostgreSQL
   □ Aplicar WAL archives (se disponíveis)
   □ Verificar integridade (SELECT count em tabelas principais)

3. INICIAR SERVIÇOS (10 min)
   □ docker compose up -d
   □ Verificar health checks
   □ Verificar conectividade com Redis

4. RESTAURAR MÍDIA (10 min)
   □ Sincronizar S3/R2 (já está lá — apenas verificar acesso)
   □ Limpar cache CDN

5. DNS (5-30 min)
   □ Apontar DNS para novo IP (Cloudflare)
   □ Aguardar propagação

6. VALIDAR (15 min)
   □ Acessar site público
   □ Fazer agendamento de teste
   □ Verificar painel admin
   □ Verificar notificações

TEMPO TOTAL ESTIMADO: 1h40min - 2h30min
```

---

## 4. Estratégia de Backups (Revisão)

| O Que | Frequência | Local | Retenção |
|-------|:----------:|-------|:--------:|
| Banco (pg_dump -Fc) | Diário (03:00 UTC) | S3/R2 | 30 versões |
| WAL Archives | Contínuo | S3/R2 | 30 dias |
| Arquivos de mídia | Contínuo (S3) | S3/R2 | Versionamento |
| Configuração (Infra as Code) | Git | GitHub | Indefinido |
| Secrets (.env) | Manual | Gerenciador de senhas | Indefinido |

### Validação de Backups

- **Mensal:** Restore de backup em staging
- **Trimestral:** Simulação de desastre completo
- **Automatizado:** Script de verificação de integridade do dump

---

## 5. Comunicação de Crise

### Status Page (V1+)

```
status.barbersaas.com.br

🟢 Todos os sistemas operacionais
🟡 Performance degradada (latência elevada)
🔴 Indisponível (fora do ar)

Histórico de incidentes (90 dias)
Tempo de atividade: 99.9%
```

### Comunicação com Clientes

- **E-mail** para todos os admins de tenant (database de contatos)
- **Painel admin:** Banner de notificação
- **WhatsApp:** Para incidentes críticos que afetam agendamentos

---

> **Resumo:** O plano de recuperação de desastres cobre 8 cenários com procedimentos específicos. Para 1 desenvolvedor, a simplicidade é crucial: VPS única + backups no S3 + Docker Compose permitem restore em ~2 horas. Conforme o sistema escala, infraestrutura gerenciada (managed DB, K8s, multi-AZ) reduz RTO e RPO para minutos. Backups testados regularmente são a única garantia real contra desastres.
