# 13 — Estratégia de Backup e Recuperação de Desastres

---

## 13.1 Objetivos (RPO / RTO)

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **RPO** (Recovery Point Objective) | < 5 minutos | Máximo de dados perdidos em caso de falha |
| **RTO** (Recovery Time Objective) | < 1 hora | Tempo máximo para restaurar operação |
| **Retenção de backups** | 30 dias (diários) + 12 meses (mensais) | Capacidade de restaurar versões antigas |
| **Backup de segurança** | 5 anos (logs de auditoria) | Compliance e LGPD |

---

## 13.2 O que é Backupeado

| Componente | O que | Método | Frequência |
|------------|-------|--------|------------|
| **PostgreSQL** | Banco inteiro | `pg_dump` custom format + WAL archiving | Contínuo (WAL) + Diário (full) |
| **Redis** | Não backupeado | Dados são efêmeros/cacheáveis | N/A (reconstruível) |
| **S3/R2 (Mídia)** | Todos os objetos | Versionamento de bucket + replicação cross-region | Contínuo |
| **Configurações** | Kubernetes manifests, Terraform | Git (IaC) | A cada deploy |
| **Logs de auditoria** | Tabela `audit_logs` | Incluído no backup do banco | Contínuo |

### O que NÃO é backupeado (e por quê)

| Componente | Motivo |
|------------|--------|
| Sessões (Redis) | Efêmeras, expiram em 15 min |
| Cache de consultas (Redis) | Reconstruível |
| Arquivos temporários | Efêmeros |
| Build artifacts | Reconstruíveis via CI/CD |

---

## 13.3 Estratégia de Backup do PostgreSQL

### Níveis de Backup

```
Camada 1: WAL Archiving (Contínuo)
──────────────────────────────────
  • Write-Ahead Logs enviados continuamente para S3
  • Permite Point-in-Time Recovery (PITR)
  • RPO: segundos (depende da latência do archive)
  • Custo: baixo (apenas diffs)

Camada 2: Full Backup (Diário)
──────────────────────────────────
  • pg_dump -Fc (custom format, compressed)
  • Horário: 03:00 UTC (baixa utilização)
  • Retenção: 30 versões diárias
  • Tamanho estimado (1.000 tenants): ~5 GB/dia

Camada 3: Backup Mensal (Arquivo)
──────────────────────────────────
  • Cópia do full backup do dia 1º de cada mês
  • Retenção: 12 versões
  • Armazenamento: S3 Glacier (cold storage)
```

### Comandos de Referência

```
# Full backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -Fc -f backup_$(date +%Y%m%d).dump

# Restore
pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -j 4 backup_20260720.dump

# WAL-based PITR recovery
# Configurado no postgresql.conf:
# archive_mode = on
# archive_command = 'aws s3 cp %p s3://backups/wal/%f'
```

---

## 13.4 Estratégia de Backup do S3/R2 (Mídia)

| Funcionalidade | Como |
|---------------|------|
| Versionamento | Ativado no bucket (mantém versões anteriores de arquivos) |
| Replicação | Cross-region replication (SP → Virginia, por exemplo) |
| Proteção contra deleção | MFA Delete habilitado (evita exclusão acidental) |
| Lifecycle policies | Versões antigas → Glacier após 90 dias |

---

## 13.5 Procedimento de Restore (Runbook)

### Cenário 1: Corrupção de Dados (PITR)

```
1. Identificar o timestamp exato antes da corrupção
2. Restaurar último full backup em instância nova
3. Aplicar WAL até o timestamp desejado
4. Validar integridade dos dados
5. Promover instância nova como primary
6. Atualizar DNS / connection strings
7. Verificar operação dos serviços
```

**Tempo estimado:** 30-60 minutos (depende do volume de WAL)

### Cenário 2: Perda Total do Banco (Disaster Recovery)

```
1. Criar nova instância PostgreSQL
2. Restaurar último full backup (pg_restore)
3. Aplicar WAL archives (se disponíveis)
4. Validar integridade
5. Redirecionar aplicação
```

**Tempo estimado:** 1-2 horas

### Cenário 3: Exclusão Acidental de Arquivo (S3)

```
1. Identificar o objeto deletado
2. Listar versões disponíveis (versioning)
3. Restaurar versão anterior
4. Verificar integridade
```

**Tempo estimado:** 5 minutos

---

## 13.6 Testes de Restore

| Frequência | O que testar |
|------------|-------------|
| **Mensal** | Restore de backup full em ambiente de staging |
| **Trimestral** | Simulação completa de disaster recovery |
| **Anual** | Teste de restore de backup de 12 meses atrás |

Testes são **obrigatórios**. Um backup que nunca foi restaurado não é um backup — é uma esperança.

---

## 13.7 Automação

### Script de Backup (Executado via CronJob / GitHub Actions)

```
0 3 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1
```

Fluxo do script:
1. Verificar conectividade com banco
2. Executar pg_dump
3. Verificar integridade do dump (pg_restore --list)
4. Upload para S3 com checksum
5. Registrar metadados (tamanho, timestamp, checksum)
6. Rotacionar backups antigos (excluir > 30 dias)
7. Notificar sucesso/falha (e-mail/WhatsApp)

---

## 13.8 Monitoramento de Backup

Alertas:
- **Backup não executado** nas últimas 25 horas
- **Tamanho do backup** com variação > 50% (possível problema)
- **Falha no upload** para S3
- **Espaço em disco** do servidor de backup < 20%

---

## 13.9 Custos de Backup (Estimativa)

| Clientes | Volume do Banco | Backup Diário | Custo Mensal (S3) |
|----------|:--------------:|:-------------:|:-----------------:|
| 10 | ~50 MB | 25 MB | ~R$ 2 |
| 100 | ~500 MB | 250 MB | ~R$ 10 |
| 1.000 | ~5 GB | 2.5 GB | ~R$ 50 |
| 10.000 | ~50 GB | 25 GB | ~R$ 300 |

---

## 13.10 Política de Retenção para Tenants Deletados

Quando um tenant cancela:
1. Dados mantidos por **90 dias** (período de recuperação)
2. Após 90 dias: backup final único
3. Backup final armazenado por **5 anos** (S3 Glacier)
4. Após 5 anos: exclusão definitiva

---

> **Princípio:** Backups são a última linha de defesa. Não importa quão boa seja sua arquitetura — se você perder os dados, você perdeu o negócio. Backups testados regularmente são a diferença entre um incidente e uma catástrofe.
