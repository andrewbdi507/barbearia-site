# 📊 Analytics & Business Intelligence — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.analytics`

---

## 1. Visão Geral

Dashboard executivo com KPI Engine modular, relatórios, metas, alertas inteligentes e exportação. Transforma dados em decisões.

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Modular KPI Registry** | KPIs registrados em dict. Adicionar novo = 1 função async |
| **2** | **Comparison Engine** | Todo KPI calcula `change_pct` e `trend` vs período anterior |
| **3** | **Smart Alert Engine** | Regras no banco. Avaliação periódica de thresholds |
| **4** | **Streaming Export** | CSV com chunked cursor. Suporta milhões de registros |
| **5** | **Charts Desacoplados** | `ChartData` genérico → qualquer frontend renderiza |

---

## 2. KPI Engine

### Como Adicionar um Novo KPI

```python
# 1. Criar função
async def _kpi_churn_rate(session, tid, dfrom, dto) -> KPIData:
    # ... query no banco ...
    return KPIData(key="churn_rate", label="Churn Rate", value=rate,
                   format="percentage", trend="up")

# 2. Registrar
from app.modules.analytics.application.kpi_registry import register_kpi
register_kpi("churn_rate", "Churn Rate", "percentage", _kpi_churn_rate)

# 3. Pronto! O dashboard auto-descobre
GET /analytics/kpis  → inclui "churn_rate" automaticamente
```

---

## 3. Performance com Milhões de Registros

| Técnica | Descrição |
|---------|-----------|
| **Índices compostos** | `(tenant_id, status, paid_at)` para queries de receita |
| **Agregação no banco** | `SUM()`, `AVG()`, `COUNT()` no PostgreSQL — não no Python |
| **Range filters** | `WHERE date BETWEEN` usa índices de data |
| **Paginação** | Export chunked: N registros por lote |
| **Materialized Views** (planejado) | `mv_revenue_daily` refresh a cada hora |
| **Redis cache** | KPIs cacheados por 5 min (TTL configurável) |

---

## 4. Como Novos KPIs, Gráficos e Relatórios Podem Ser Adicionados

| Elemento | Mecanismo | Zero alteração em |
|----------|-----------|-------------------|
| Novo KPI | `register_kpi()` + 1 função async | Rotas, Dashboard, Frontend |
| Novo Gráfico | `ChartData` + 1 método no AnalyticsService | KPI Engine |
| Novo Relatório | `export_csv()` + novo `report_type` | Gráficos, KPIs |
| Novo Alerta | `create_alert()` via API | Código (data-driven) |

---

## 5. Exportações

| Formato | Endpoint | Suporte |
|---------|----------|:------:|
| CSV | `GET /analytics/export/{type}` | ✅ |
| Excel | Planejado | 🔲 |
| PDF | Planejado | 🔲 |
| Power BI | Conexão direta PostgreSQL | 🔲 |
