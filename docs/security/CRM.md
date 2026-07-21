# 👤 Módulo de CRM — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.customer`

---

## 1. Visão Geral

CRM completo para gestão de clientes, histórico, fidelização e conformidade LGPD. Inspirado em **HubSpot** (customer 360°), **Starbucks Rewards** (loyalty tiers), **Google Reviews** (review + response) e **Mailchimp** (smart segments).

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Customer 360° View** | `GET /customers/{id}/profile` agrega dados de TODOS os módulos em 1 endpoint |
| **2** | **Dynamic Smart Segments** | Filtros por tag, status, comportamento — base para marketing automatizado |
| **3** | **Loyalty Tiers Auto-Promotion** | Bronze→Silver→Gold→Diamond automático por visitas |
| **4** | **LGPD by Design** | Consentimentos versionados, exportação completa, anonimização |
| **5** | **Review + Business Response** | Moderação antes de publicar, resposta da empresa |

---

## 2. Arquitetura

```
app/modules/customer/
├── domain/
│   ├── entities.py     # Customer (AR), Preference, Tag, Review, Consent, Loyalty, Referral
│   ├── enums.py        # Status, Source, LoyaltyTier, ConsentType, ReferralStatus
│   └── interfaces.py   # 7 ports
├── application/
│   ├── customer_service.py  # CustomerService — orquestração completa
│   └── dto.py               # 15+ DTOs
├── infrastructure/
│   ├── models/         # 8 modelos SQLAlchemy
│   └── repository.py   # 7 repositórios
└── presentation/
    └── routes.py       # 25+ endpoints REST
```

---

## 3. Customer 360° View

`GET /customers/{id}/profile` retorna:

```json
{
  "customer": { "name": "João", "total_visits": 12, "total_spent": 54000 },
  "preferences": { "favorite_professional_id": "p1", "favorite_service_ids": ["s1"] },
  "loyalty": { "points": 540, "tier": "silver", "visit_count": 12 },
  "reviews": [{ "rating": 5, "comment": "Ótimo atendimento!" }],
  "referrals": [{ "referral_code": "ABC12345", "status": "rewarded" }],
  "stats": { "avg_ticket": 4500, "avg_rating": 4.8, "last_visit_at": "..." }
}
```

---

## 4. Loyalty Tiers

| Tier | Visitas | Benefício |
|------|:-------:|-----------|
| Bronze | 0-4 | 1 ponto por R$1 |
| Silver | 5-14 | 1.2 pontos por R$1 + 10% desconto aniversário |
| Gold | 15-29 | 1.5 pontos por R$1 + 20% desconto + prioridade |
| Diamond | 30+ | 2 pontos por R$1 + 30% desconto + serviço VIP |

Tiers são recalculados automaticamente a cada visita (`earn_points(visit=True)`).

---

## 5. LGPD Compliance

| Funcionalidade | Endpoint | Descrição |
|----------------|----------|-----------|
| Consentimento | `POST /{id}/consents` | Registra consentimento versionado |
| Revogação | `POST /{id}/consents/revoke-all` | Revoga todos os consentimentos |
| Exportação | `GET /{id}/lgpd/export` | Exporta TODOS os dados do cliente (JSON) |
| Anonimização | `POST /{id}/lgpd/anonymize` | Substitui PII por valores anônimos |

---

## 6. Como Outros Módulos Usam

```python
# Módulo de Agendamento → registra visita + pontos
customer = await customer_service.get_customer(customer_id)
customer.record_visit(amount=4500)
await customer_service.earn_points(customer_id, 45, visit=True)

# Módulo de Marketing → segmenta clientes
vips, _ = await customer_service.list_customers(tenant_id, tag="VIP")
lapsed, _ = await customer_service.list_customers(tenant_id, tag="Lapsed30d")

# Site Público → exibe avaliações
reviews, _ = await customer_service.list_reviews(tenant_id, visible_only=True)
```

---

## 7. Escalabilidade

| Estratégia | Impacto |
|------------|---------|
| Índices em `phone`, `email`, `tenant_id` | Busca O(log n) |
| Full-text search via `ILIKE` com paginação | Pesquisa rápida por nome |
| Tags como JSONB array | Filtro sem JOIN |
| Loyalty transactions append-only | Histórico imutável e rápido |
| Particionamento futuro por `tenant_id` | Isolamento físico |
