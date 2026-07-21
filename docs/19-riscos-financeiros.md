# 19 — Riscos Financeiros

---

## 19.1 Estrutura de Custos

### Custos Fixos Mensais

| Item | MVP (R$) | V1 (R$) | V2 (R$) | V3 (R$) |
|------|:------:|:-----:|:-----:|:-----:|
| Infraestrutura (cloud) | 200 | 1.200 | 2.500 | 6.600 |
| Domínios | 50 | 100 | 200 | 500 |
| Ferramentas (Sentry, Grafana, etc.) | 0 | 0 | 500 | 1.500 |
| Gateway de pagamento (taxa fixa) | 0 | 100 | 200 | 500 |
| Contador | 300 | 500 | 800 | 1.500 |
| **Total Mensal** | **550** | **1.900** | **4.200** | **10.600** |

### Custos Variáveis (por transação)

| Item | Custo |
|------|-------|
| Taxa de gateway (PIX) | ~0.99% |
| Taxa de gateway (cartão) | ~3.99% |
| SMS (por mensagem) | ~R$ 0,10 |
| WhatsApp Business API (por conversa) | ~R$ 0,05–0,15 |
| E-mail (AWS SES) | ~R$ 0,0001 por e-mail |

---

## 19.2 Riscos Financeiros

### RF1 — Subprecificação

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 5 (Crítico) |
| **Descrição** | Preços baixos demais para sustentar o negócio, especialmente no Brasil onde há resistência a pagar por software |
| **Mitigação** | Pesquisa de mercado, teste A/B de preços, começar com preço mais alto e desconto de lançamento |
| **Solução** | Ajuste gradual de preços, grandfathering para clientes antigos |

### RF2 — Custo de Aquisição de Clientes (CAC) Elevado

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 4 (Alto) |
| **Descrição** | Custo de marketing e vendas para adquirir cada cliente é maior que o LTV |
| **Mitigação** | Crescimento orgânico (SEO, indicação), onboarding self-service, automação de marketing |
| **Solução** | Focar em canais de baixo CAC (indicação, conteúdo, parcerias) |

### RF3 — Churn Elevado

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 4 (Alto) |
| **Descrição** | Clientes cancelam rapidamente (antes de 3 meses), LTV < 3× CAC |
| **Mitigação** | Onboarding excepcional, suporte rápido, entregar valor na primeira semana, pesquisa de cancelamento |
| **Solução** | Identificar padrões de churn e corrigir proativamente |

### RF4 — Inadimplência

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 3 (Médio) |
| **Descrição** | Clientes não pagam assinatura, especialmente débito automático que falha |
| **Mitigação** | Cartão de crédito como método principal (recorrência), múltiplas tentativas de cobrança, notificações |
| **Solução** | Suspensão automática após 7 dias de atraso, reativação fácil |

### RF5 — Dependência de Gateway de Pagamento

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 2 (Baixa) |
| **Impacto** | 5 (Crítico) |
| **Descrição** | Único gateway bloqueia conta, aumenta taxas, ou encerra operação no Brasil |
| **Mitigação** | Abstrair gateway, ter 2+ gateways integrados, poder trocar rapidamente |
| **Solução** | Migrar base para gateway alternativo |

### RF6 — Custo de Infraestrutura Acima do Previsto

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 3 (Médio) |
| **Descrição** | Infraestrutura custa mais que o planejado, especialmente em escala |
| **Mitigação** | Monitoramento de custos desde o dia 1, alertas de orçamento, usar free tiers |
| **Solução** | Otimizar uso de recursos, migrar para opções mais baratas |

### RF7 — Concorrência Agressiva

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 4 (Alto) |
| **Descrição** | Concorrente bem financiado entra no mercado com preços predatórios |
| **Mitigação** | Foco em nicho (barbearias), comunidade, qualidade do produto, switching cost alto (dados do cliente na plataforma) |
| **Solução** | Diferenciar por qualidade e relacionamento, não por preço |

### RF8 — Custo de Suporte Não Escala

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 3 (Médio) |
| **Descrição** | Conforme tenants crescem, suporte consome tempo demais do dev |
| **Mitigação** | FAQ, base de conhecimento, onboarding self-service, tooltips in-app, automação |
| **Solução** | Contratar suporte (1ª contratação após dev) ou usar chatbot |

---

## 19.3 Ponto de Equilíbrio (Breakeven)

### MVP (sem receita)
- Custo: R$ 550/mês
- Receita: R$ 0
- **Investimento inicial: R$ 1.650 (3 meses)**

### V1 (monetizado)
- Custo: R$ 1.900/mês
- Breakeven: **22 clientes no plano Pro (R$ 89,90)**
- Com 50 clientes: lucro de ~R$ 2.500/mês
- Com 100 clientes: lucro de ~R$ 7.000/mês

---

## 19.4 Principais Recomendações Financeiras

1. **Comece cobrando.** Não espere o produto ficar "perfeito". Cobre desde o beta fechado.
2. **Precifique baseado em valor, não em custo.** Quanto tempo/dinheiro seu cliente economiza?
3. **Cobre anualmente com desconto.** Melhora cashflow e reduz churn.
4. **Mantenha custo de infra < 10% da receita.**
5. **Invista em SEO desde o início.** É o canal de aquisição mais barato no longo prazo.
6. **Tenha reserva financeira para 12 meses de operação sem receita.**

---

> **Princípio:** SaaS é um jogo de números: CAC, LTV, Churn, MRR. Se você não conhece seus números, você não tem um negócio — você tem um hobby. Financeiro é tão importante quanto técnico.
