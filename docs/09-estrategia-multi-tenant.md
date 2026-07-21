# 09 — Estratégia Multi-Tenant

---

## 9.1 Modelo Escolhido: Banco Compartilhado com Row-Level Security

```
┌──────────────────────────────────────────────────────────────────┐
│              MODELO MULTI-TENANT                                  │
│                                                                   │
│  Schema ÚNICO + tenant_id em todas as tabelas + RLS (PostgreSQL) │
│                                                                   │
│  tenants          bookings              services                  │
│  ┌──────────────┐ ┌──────────────────┐ ┌──────────────────┐      │
│  │ id           │ │ id               │ │ id               │      │
│  │ name         │ │ tenant_id ───────┼─┼→ tenant_id       │      │
│  │ subdomain    │ │ customer_name    │ │ name             │      │
│  │ status       │ │ professional_id  │ │ price            │      │
│  │ created_at   │ │ service_id       │ │ duration         │      │
│  └──────────────┘ │ date             │ │ created_at       │      │
│        ↑          │ status           │ └──────────────────┘      │
│        │          │ created_at       │                            │
│        └──────────┤ tenant_id        │  TODAS as tabelas de      │
│                   └──────────────────┘  negócio possuem           │
│                                         tenant_id como FK         │
│                                                                   │
│  RLS: cada query é automaticamente                                │
│  filtrada por tenant_id = current_tenant_id                       │
└──────────────────────────────────────────────────────────────────┘
```

### Por que este modelo?

| Critério | Schema Compartilhado | Schema por Tenant | Banco por Tenant |
|----------|:--------------------:|:-----------------:|:----------------:|
| Complexidade operacional | ⭐ Baixa | ⭐⭐ Média | ⭐⭐⭐ Alta |
| Custo de infraestrutura | ⭐ Baixo | ⭐⭐ Médio | ⭐⭐⭐ Alto |
| Isolamento de dados | ⭐⭐ Médio (RLS) | ⭐⭐⭐ Alto | ⭐⭐⭐ Máximo |
| Escalabilidade | ⭐⭐⭐ Alta | ⭐⭐ Média | ⭐⭐ Média |
| Manutenção (1 dev) | ⭐ Ideal | ⭐⭐ Viável | ⭐⭐⭐ Inviável |
| Migrations | 1 vez | N vezes | N vezes |
| Backups | 1 banco | 1 banco | N bancos |

**Decisão:** Schema compartilhado com RLS. Com 1 desenvolvedor, a simplicidade operacional é o fator decisivo.

---

## 9.2 Isolamento em 3 Camadas

### Camada 1 — Aplicação (Middleware)

```python
# Todo request autenticado carrega tenant_id
# O middleware resolve o tenant e injeta no contexto

async def tenant_middleware(request, call_next):
    # Resolve tenant do subdomínio ou JWT
    tenant = await resolve_tenant(request)
    
    # Injeta no contexto da requisição
    request.state.tenant_id = tenant.id
    
    # Propaga para queries SQL
    set_current_tenant_id(tenant.id)
    
    return await call_next(request)
```

### Camada 2 — Banco de Dados (RLS)

```sql
-- Ativa RLS em todas as tabelas de negócio
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE professionals ENABLE ROW LEVEL SECURITY;
-- ... todas as tabelas

-- Política: só vê dados do seu tenant
CREATE POLICY tenant_isolation ON bookings
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Super admin bypass (acesso plataforma)
CREATE POLICY super_admin_access ON bookings
    FOR ALL
    USING (current_setting('app.is_super_admin', true) = 'true');
```

### Camada 3 — Storage (S3/R2)

```
Estrutura de Bucket:

s3://barbersaas-media/
├── t_abc123/                    # Tenant 1
│   ├── logo.png
│   ├── banner.jpg
│   ├── gallery/
│   │   ├── foto1.webp
│   │   └── foto2.webp
│   └── professionals/
│       ├── prof_1.jpg
│       └── prof_2.jpg
│
├── t_def456/                    # Tenant 2
│   ├── logo.png
│   └── ...
│
└── platform/                    # Assets da plataforma
    └── templates/

Política IAM:
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::barbersaas-media/${tenant_id}/*"
}
```

---

## 9.3 Estratégia de Domínios e Subdomínios

### Domínio Padrão (Fornecido pela Plataforma)

```
[subdomínio].barbersaas.com.br
```

Exemplos:
- `studio27.barbersaas.com.br` → Site público
- `studio27.barbersaas.com.br/admin` → Painel admin
- `studio27.barbersaas.com.br/api` → API (transparente)

### Domínio Próprio (V1+)

```
[www].barbeariadocliente.com.br
```

- Tenant configura DNS (CNAME ou A record)
- SSL automático via Let's Encrypt / Cloudflare
- Plataforma detecta domínio e resolve tenant

### Implementação Técnica

```
1. Tenant configura domínio próprio no painel:
   meudominio.com.br

2. Sistema gera instruções DNS:
   CNAME  meudominio.com.br  →  sites.barbersaas.com.br

3. Tenant configura DNS (provavelmente com ajuda)

4. Sistema verifica propagação DNS

5. SSL provisionado automaticamente

6. Domínio ativo ✅
```

---

## 9.4 Onboarding de Tenant (Self-Service)

```
1. Usuário acessa landing page da plataforma
2. Clica em "Criar minha barbearia"
3. Preenche cadastro (nome, e-mail, senha)
4. Escolhe subdomínio (validado em tempo real)
5. Conta criada → Redirecionado para wizard
6. Wizard: logo, serviços, profissionais, horários
7. Site no ar em menos de 10 minutos
```

---

## 9.5 Gerenciamento do Ciclo de Vida do Tenant

| Estado | Descrição | Ações |
|--------|-----------|-------|
| **trial** | Período gratuito (14 dias) | Acesso total, banner "Plano trial — restam X dias" |
| **active** | Assinatura paga ativa | Acesso total |
| **past_due** | Pagamento atrasado | Acesso normal por 7 dias de graça, notificações de cobrança |
| **suspended** | Sem pagamento > 7 dias | Site pausado (página de "volte logo"), admin acessível para reativar |
| **cancelled** | Cancelamento voluntário | Dados preservados por 90 dias, depois deletados |
| **deleted** | Exclusão definitiva | Dados anonimizados ou removidos conforme LGPD |

---

## 9.6 Segurança do Isolamento

### Proteções Implementadas

1. **Row-Level Security** — Última linha de defesa no banco
2. **Middleware de tenant** — Primeira linha de defesa na aplicação
3. **Validação de pertencimento** — Toda operação valida se recurso pertence ao tenant
4. **Testes de cross-tenant** — Suite de testes específica tentando acessar dados de outro tenant
5. **Auditoria** — Toda tentativa de acesso cross-tenant é logada como evento de segurança
6. **Rate limit por tenant** — Um tenant não pode degradar a experiência de outros

### O que NÃO fazer (anti-padrões)

- ❌ Passar `tenant_id` como parâmetro no frontend
- ❌ Confiar apenas no middleware sem RLS
- ❌ Queries sem filtro de tenant_id
- ❌ Endpoints que não verificam pertencimento do recurso

---

## 9.7 Escalabilidade do Modelo Multi-Tenant

### Até 1.000 tenants
- PostgreSQL único com RLS é suficiente
- Índices com `tenant_id` como primeira coluna
- Connection pooling (PgBouncer)

### 1.000–10.000 tenants
- Read replicas para queries de leitura (site público)
- Escrita no primary, leitura nas replicas
- Hot standby para failover

### 10.000–100.000 tenants
- Considerar sharding por faixa de tenant_id
- Ou migrar para schema por tenant (ainda no mesmo cluster)
- Ou separar tenants enterprise em clusters dedicados

### Decisão: Começar simples (schema único + RLS) e evoluir conforme necessidade. Não otimizar prematuramente.

---

## 9.8 Métricas de Tenant

Cada tenant terá métricas de uso para:
- Identificar tenants com alto crescimento (precisam de atenção)
- Identificar tenants inativos (churn risk)
- Planejar capacidade

| Métrica | Descrição |
|---------|-----------|
| Agendamentos/dia | Volume transacional |
| Clientes ativos | Clientes com pelo menos 1 agendamento nos últimos 90 dias |
| Profissionais ativos | Profissionais com agenda disponível |
| Storage usado | Total de mídia armazenada (limitar por plano) |
| API calls/dia | Volume de requisições |

---

> **Princípio:** Multi-tenancy é a fundação do modelo SaaS. Acertar aqui significa segurança, escalabilidade e baixo custo operacional. Errar aqui significa vazamento de dados e falência do produto. RLS + middleware + testes cross-tenant = defesa em profundidade.
