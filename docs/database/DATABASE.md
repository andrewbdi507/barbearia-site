# 🗄️ Barbershop SaaS — Documentação de Banco de Dados

> **Versão:** 1.0.0  
> **Data:** Julho 2026  
> **SGBD:** PostgreSQL 16  
> **Modelo:** Schema Compartilhado + Row-Level Security  
> **Referência:** Stripe · Shopify · Notion · Uber

---

## 📋 Índice

| # | Documento | Descrição |
|---|-----------|-----------|
| — | `DATABASE.md` | Estratégia geral, multi-tenant, performance, segurança |
| 01 | `DOMAIN_MODEL.md` | Modelagem de domínio, contextos delimitados, agregados |
| 02 | `ENTITY_CATALOG.md` | Catálogo completo de todas as entidades |
| 03 | `RELATIONSHIPS.md` | Relacionamentos, cardinalidades, dependências |
| 04 | `DATA_DICTIONARY.md` | Dicionário de dados com todos os atributos |

---

## 1. Estratégia Geral

### 1.1 Modelo Multi-Tenant

**Decisão:** Schema compartilhado com `tenant_id` em todas as tabelas de negócio + Row-Level Security (RLS).

```
┌──────────────────────────────────────────────────────────────────┐
│              ARQUITETURA MULTI-TENANT                             │
│                                                                   │
│  Schema: public (único)                                           │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  TABELAS DE PLATAFORMA (sem tenant_id)                      │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │  │tenants   │ │plans     │ │subscript.│ │platform_ │      │ │
│  │  │          │ │          │ │          │ │users     │      │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  TABELAS DE NEGÓCIO (com tenant_id + RLS)                   │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │  │users     │ │customers │ │services  │ │profession│      │ │
│  │  │tenant_id │ │tenant_id │ │tenant_id │ │tenant_id │      │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │  │bookings  │ │payments  │ │schedules │ │notificat.│      │ │
│  │  │tenant_id │ │tenant_id │ │tenant_id │ │tenant_id │      │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Justificativa do Modelo

| Fator | Schema Compartilhado | Schema por Tenant | Banco por Tenant |
|-------|:--------------------:|:-----------------:|:----------------:|
| Complexidade operacional | ✅ Baixa | ⚠️ Média | ❌ Alta |
| Custo (1 dev) | ✅ Ideal | ⚠️ Viável | ❌ Inviável |
| Migrations | ✅ 1 vez | ❌ N vezes | ❌ N vezes |
| Backups | ✅ 1 banco | ✅ 1 banco | ❌ N bancos |
| Isolamento | ⚠️ RLS | ✅ Schema | ✅ Banco |
| Escalabilidade | ✅ Alta | ⚠️ Média | ⚠️ Média |

**Conclusão:** Schema compartilhado + RLS é a única opção viável para 1 desenvolvedor. O isolamento é garantido por 3 camadas: aplicação (middleware), banco (RLS), storage (prefixo S3).

---

## 1.3 Convenções de Nomenclatura

| Convenção | Exemplo | Justificativa |
|-----------|---------|---------------|
| **Tabelas:** snake_case, plural | `customers`, `bookings` | Padrão PostgreSQL |
| **Colunas:** snake_case, singular | `created_at`, `tenant_id` | Clareza e consistência |
| **PK:** `id` (UUID v7) | `id UUID PRIMARY KEY` | Ordenável temporalmente, seguro contra enumeração |
| **FK:** `{entidade}_id` | `tenant_id`, `customer_id` | Rastreabilidade imediata |
| **Datas:** `{ação}_at` | `created_at`, `updated_at`, `deleted_at` | Consistência temporal |
| **Booleanos:** `is_{estado}` | `is_active`, `is_verified` | Autoexplicativo |
| **JSONB:** `{nome}_data` | `metadata`, `settings_data` | Dados semiestruturados |
| **Enums:** snake_case | `booking_status`, `user_role` | Tipagem forte no PostgreSQL |

---

## 1.4 Estratégia de Chaves Primárias

**UUID v7 (time-ordered):**

- **Vantagens:** Não sequencial (seguro contra enumeração), gerado no servidor, ordenável temporalmente, compatível com sistemas distribuídos
- **Desvantagens:** 16 bytes vs 4/8 bytes do serial (diferença irrelevante para o volume previsto)
- **Decisão:** UUID v7 para todas as entidades. Segurança > economia de bytes.

---

## 1.5 Estratégia de Soft Delete

| Entidade | Soft Delete? | Justificativa |
|----------|:-----------:|---------------|
| `tenants` | ✅ Sim | Compliance LGPD, possibilidade de reativação |
| `users` | ✅ Sim | Auditoria, histórico de ações |
| `customers` | ✅ Sim | LGPD — exclusão lógica primeiro, física após 30 dias |
| `bookings` | ❌ Não | Cancelamento é status, não deleção |
| `services` | ✅ Sim | Histórico de agendamentos referencia serviço |
| `professionals` | ✅ Sim | Histórico de agendamentos referencia profissional |
| `payments` | ❌ Não | Registro financeiro imutável |

**Implementação:** Coluna `deleted_at TIMESTAMPTZ` (NULL = ativo, preenchido = deletado). Índice parcial para queries: `WHERE deleted_at IS NULL`.

---

## 1.6 Estratégia de Versionamento

Para entidades que exigem rastreamento de alterações:

| Entidade | Versionamento | Método |
|----------|:------------:|--------|
| `services` | ✅ Sim | Tabela `service_versions` com snapshot JSONB |
| `tenant_settings` | ✅ Sim | Tabela `settings_history` com diff |
| `booking_status` | ✅ Sim | Tabela `booking_status_log` (log de transições) |
| `payment_status` | ✅ Sim | Tabela `payment_events` (event sourcing) |

Demais entidades utilizam apenas `updated_at` + `audit_logs` (tabela genérica de auditoria).

---

## 1.7 Módulos do Banco de Dados (Contextos)

```
┌──────────────────────────────────────────────────────────────────┐
│                   CONTEXTOS DELIMITADOS                           │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Platform │  │Tenant    │  │Scheduling│  │Payment   │        │
│  │ Context  │  │Context   │  │Context   │  │Context   │        │
│  │          │  │          │  │          │  │          │        │
│  │ tenants  │  │settings  │  │bookings  │  │payments  │        │
│  │ plans    │  │branding  │  │schedules │  │transact. │        │
│  │ subscript│  │business  │  │services  │  │refunds   │        │
│  │ platform │  │hours     │  │profess.  │  │webhooks  │        │
│  │ _users   │  │galleries │  │customers │  │gateways  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │Notific.  │  │Marketing │  │Auth      │  │Audit     │        │
│  │Context   │  │Context   │  │Context   │  │Context   │        │
│  │          │  │          │  │          │  │          │        │
│  │templates │  │coupons   │  │users     │  │audit_logs│        │
│  │messages  │  │campaigns │  │roles     │  │login_logs│        │
│  │channels  │  │promotions│  │sessions  │  │change_log│        │
│  │delivery  │  │loyalty   │  │tokens    │  │security  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Normalização

### 2.1 Conformidade com Formas Normais

**1FN (Primeira Forma Normal):** ✅
- Todos os atributos são atômicos
- Sem arrays ou estruturas aninhadas em colunas (exceto JSONB para dados semiestruturados como `metadata`)
- Cada coluna contém um único valor

**2FN (Segunda Forma Normal):** ✅
- 1FN atendida
- Todos os atributos não-chave dependem da chave primária completa
- Sem dependências parciais

**3FN (Terceira Forma Normal):** ✅
- 2FN atendida
- Sem dependências transitivas
- Exemplo: `bookings` tem `customer_id` (FK), não `customer_name` e `customer_phone` (dados do customer)

### 2.2 Casos de Desnormalização Planejada (Futuro)

| Caso | Quando Desnormalizar | Gatilho |
|------|---------------------|---------|
| **Contadores** (ex: `total_bookings` no customer) | > 100K customers | Consultas de agregação frequentes |
| **Materialized Views** (dashboard) | > 50 tenants consultando relatórios simultaneamente | Performance de dashboards |
| **Cache de slots** (Redis) | > 100 consultas/s no grid de horários | Hot path do agendamento |
| **Sharding** | > 50K tenants | Tamanho do banco > 500 GB |
| **Event Sourcing** (pagamentos) | > 1K transações/dia | Necessidade de audit trail imutável |

**Regra de ouro:** Nunca desnormalizar preventivamente. Medir primeiro, otimizar depois.

---

## 3. Estratégia de Índices (Conceitual)

### 3.1 Índices Primários (Obrigatórios)

| Tabela | Índice | Tipo | Justificativa |
|--------|--------|------|---------------|
| **Todas de negócio** | `(tenant_id)` | B-tree | Isolamento multi-tenant (toda query filtra por tenant) |
| **Todas** | `(id)` | PK (B-tree) | Lookup por chave primária |
| **Todas com FK** | `(fk_column)` | B-tree | JOINs frequentes |
| **Todas com soft delete** | `(tenant_id, deleted_at)` | Partial | "WHERE deleted_at IS NULL" é a query mais comum |

### 3.2 Índices de Performance

| Tabela | Índice | Justificativa |
|--------|--------|---------------|
| `bookings` | `(tenant_id, professional_id, date, start_time)` | Grid de horários: consulta mais crítica do sistema |
| `bookings` | `(tenant_id, customer_id, date)` | Histórico do cliente |
| `bookings` | `(tenant_id, date, status)` | Dashboard e relatórios |
| `customers` | `(tenant_id, phone)` | Busca por telefone (check-in, CRM) |
| `customers` | `(tenant_id, email)` | Autenticação, busca |
| `users` | `(tenant_id, email)` | Login |
| `payments` | `(tenant_id, booking_id)` | Relatório financeiro por agendamento |
| `audit_logs` | `(tenant_id, created_at DESC)` | Consulta de auditoria |
| `notifications` | `(tenant_id, user_id, created_at)` | Central de notificações |

### 3.3 Índices Full-Text (Busca)

| Tabela | Colunas | Tipo | Justificativa |
|--------|---------|------|---------------|
| `customers` | `(name, phone, email)` | GIN + tsvector | Busca de clientes |
| `services` | `(name, description)` | GIN + tsvector | Busca de serviços |
| `professionals` | `(name, bio, specialties)` | GIN + tsvector | Busca de profissionais |

PostgreSQL `tsvector` nativo é suficiente até ~50K tenants. Meilisearch/Elasticsearch apenas em V2+.

### 3.4 Índices Únicos (Constraints)

| Tabela | Colunas | Justificativa |
|--------|---------|---------------|
| `tenants` | `(subdomain)` | Subdomínio único globalmente |
| `users` | `(tenant_id, email)` | Email único por tenant |
| `customers` | `(tenant_id, phone)` | Telefone único por tenant |
| `services` | `(tenant_id, name)` | Nome de serviço único por tenant |
| `bookings` | `(tenant_id, professional_id, date, start_time)` | Sem double-booking |

---

## 4. Particionamento

### 4.1 Estratégia

| Tabela | Particionamento | Critério | Quando Ativar |
|--------|:--------------:|----------|:-------------:|
| `bookings` | Por range | `date` (mensal) | > 1M registros |
| `audit_logs` | Por range | `created_at` (mensal) | > 5M registros |
| `notifications` | Por range | `created_at` (mensal) | > 10M registros |
| `login_logs` | Por range | `created_at` (mensal) | > 1M registros |

### 4.2 Benefícios do Particionamento

- **Consulta mais rápida:** Partition pruning elimina partições irrelevantes
- **Manutenção facilitada:** DROP PARTITION em vez de DELETE para expurgo
- **Vacuum mais eficiente:** Por partição, não na tabela inteira
- **Arquivamento:** Partições antigas podem ser movidas para tablespaces mais baratos

### 4.3 Arquivamento

- **Bookings > 2 anos:** Mover para tabela `bookings_archive` ou tablespace em storage mais lento
- **Audit logs > 5 anos:** Exportar para S3 Glacier (Parquet), deletar do banco
- **Login logs > 1 ano:** Deletar (retenção definida por compliance)

---

## 5. Performance

### 5.1 Consultas Críticas (Hot Path)

**Grid de Horários (consulta mais frequente do sistema):**
- Frequência: ~100 consultas/min por tenant em horário de pico
- Complexidade: JOIN de schedules + bookings + professionals + services
- Estratégia: Cache Redis (30s TTL) + índice composto otimizado
- Alvo: < 50ms

**Dashboard do Dono:**
- Frequência: ~1 consulta/min por tenant
- Complexidade: Agregações (COUNT, SUM, GROUP BY)
- Estratégia: Materialized views refresh a cada 5 minutos (V2+)
- Alvo: < 200ms

### 5.2 Connection Pooling

- **PgBouncer** em modo transaction pooling
- Pool size: 50 conexões (MVP) → 200 (V1) → 500 (V2+)
- Timeout de conexão ociosa: 10 minutos

### 5.3 Read Replicas

- **V1+ (500+ tenants):** 1 read replica para queries do site público
- **V2+ (5.000+ tenants):** 2-3 read replicas com load balancing
- Write: primary apenas. Read: replicas (site público, relatórios)

---

## 6. Segurança

### 6.1 Row-Level Security

Todas as tabelas de negócio com RLS ativado:

- **Policy padrão:** `USING (tenant_id = current_setting('app.current_tenant_id')::UUID)`
- **Super admin bypass:** `USING (current_setting('app.is_super_admin', true) = 'true')`
- **Aplicado em:** SELECT, INSERT, UPDATE, DELETE

### 6.2 Criptografia

| Dado | Criptografia | Método |
|------|:-----------:|--------|
| Dados em trânsito | ✅ | TLS 1.3 (obrigatório) |
| Dados em repouso (disco) | ✅ | PostgreSQL TDE ou LUKS (cloud provider) |
| Senhas | ✅ | bcrypt (cost ≥ 12) — hash, não criptografia |
| Tokens (refresh) | ✅ | SHA-256 hash armazenado |
| Dados sensíveis (campo) | ✅ | pgcrypto + AES-256-GCM (colunas específicas) |

### 6.3 Dados que NUNCA são Armazenados

- ✗ Números de cartão de crédito
- ✗ CVV/CVC
- ✗ Data de validade do cartão
- ✗ Senhas em texto plano
- ✗ Tokens de acesso JWT (só o hash do refresh token)

### 6.4 Mascaramento de Dados (LGPD)

Colunas com dados pessoais marcadas com comentários para:
- Identificação em processos de exportação (LGPD — direito de acesso)
- Identificação em processos de exclusão (LGPD — direito ao esquecimento)
- Mascaramento em ambientes de desenvolvimento/staging

---

## 7. Backup & Recovery

### 7.1 Estratégia (Alinhada ao Doc 13 de Arquitetura)

| Tipo | Método | Frequência | Retenção |
|------|--------|:----------:|:--------:|
| WAL Archiving | Contínuo (archive_mode) | Tempo real | 30 dias |
| Full Backup | pg_dump -Fc | Diário (03:00 UTC) | 30 dias |
| Mensal | Cópia do full backup | Mensal | 12 meses |
| Logs de auditoria | Incluso no backup full | Diário | 5 anos |

### 7.2 RPO / RTO

- **RPO:** < 5 minutos (WAL contínuo)
- **RTO:** < 1 hora (restore full + apply WAL)

---

## 8. Migrations

### 8.1 Estratégia

- **Ferramenta:** Alembic (SQLAlchemy)
- **Direção:** Sempre forward + rollback script
- **Teste:** Toda migration testada em staging antes de produção
- **Lock:** Migrations com lock avaliadas (usar `CREATE INDEX CONCURRENTLY`)
- **Rollback:** Script de reversão testado e documentado

### 8.2 Regras

1. Nunca fazer migration em horário de pico
2. Sempre ter backup antes de migration estrutural
3. Migrations são versionadas no Git
4. Nunca usar `DROP COLUMN` sem antes `SET DEFAULT` + período de transição
5. Adicionar colunas como nullable primeiro, popular dados, depois NOT NULL

---

> **Resumo:** O banco de dados é a "fonte da verdade" do sistema. A estratégia de schema compartilhado + RLS permite que 1 desenvolvedor mantenha milhares de tenants com segurança e performance. Índices são pensados para o hot path (grid de horários). Particionamento e replicação são previstos mas não implementados prematuramente.
