# 02 — MVP Review

> Análise crítica do escopo do MVP.  
> O que está certo, o que sobra, o que falta.

---

## 1. Escopo Atual do MVP

Baseado nos requisitos funcionais (Doc 04) e na implementação atual:

| Módulo | Funcionalidades MVP | Status |
|--------|---------------------|:------:|
| **Tenant** | Cadastro, subdomínio, configuração básica | ⚠️ Documentado, não implementado |
| **Site Público** | Home, serviços, equipe, agendamento (4 passos) | ⚠️ Frontend parcial, sem backend |
| **Agendamento** | Profissional → Serviço → Horário → Dados | ⚠️ UI implementada, sem API |
| **Painel Admin** | Dashboard, agenda, CRUD serviços/profissionais | ⚠️ Layout pronto, páginas placeholder |
| **Auth** | Login, recuperação de senha, RBAC | ⚠️ JWT implementado, sem endpoints |
| **Notificações** | WhatsApp confirmação + lembrete | ❌ Não implementado |

---

## 2. Análise: O Que SOBRA no MVP

### ❌ Itens que DEVEM ser REMOVIDOS do MVP

| Item | Motivo |
|------|--------|
| **Pagamentos** | Não é necessário para validar o core. Clientes beta não pagarão. Adiar para V1. |
| **Galerias de fotos** | Feature de engajamento, não de validação. Adiar para V1. |
| **Relatórios financeiros** | Sem pagamentos, sem relatórios. Placeholder suficiente. |
| **Múltiplos temas** | 1 tema (Urban) é suficiente para MVP. Outros 4 são V1+. |
| **Google Calendar** | "Adicionar ao calendário" é premium. MVP: link .ics download. |
| **Instagram feed embed** | Não essencial para agendamento. Adiar. |

### ⚠️ Itens que DEVEM ser SIMPLIFICADOS

| Item | Simplificação |
|------|--------------|
| **Painel Admin** | Reduzir sidebar para 5 itens: Dashboard, Agenda, Clientes, Serviços, Config |
| **Onboarding Wizard** | 3 passos em vez de 5: Identidade → Serviços → Equipe |
| **Notificações** | Apenas WhatsApp. Email e SMS são V1+. |
| **Design System** | 10 componentes core. Os outros 18+ podem ser V1. |
| **Páginas do site público** | Home + Agendamento + Confirmação. Serviços/Equipe/Galeria podem ser seções na Home. |

---

## 3. Análise: O Que FALTA no MVP

### 🔴 Itens CRÍTICOS que faltam

| Item | Por que é crítico |
|------|-------------------|
| **API de agendamento** | Sem API, o fluxo de agendamento não funciona. É o core. |
| **API de disponibilidade** | Grid de horários depende de lógica de slots. |
| **CRUD de serviços (API)** | Admin precisa cadastrar serviços. |
| **CRUD de profissionais (API)** | Admin precisa cadastrar equipe. |
| **Endpoints de tenant** | Criação de tenant, resolução de subdomínio. |
| **RLS no banco** | Isolamento multi-tenant. Ressalva #1. |
| **Rate limiting** | Proteção básica. Ressalva #2. |

### 🟡 Itens IMPORTANTES que faltam

| Item | Por que é importante |
|------|---------------------|
| **Testes cross-tenant** | Garantia de isolamento. Ressalva #10. |
| **WhatsApp integration** | Notificações de confirmação. |
| **Audit logs** | Rastreabilidade desde o dia 1. |

---

## 4. MVP Redefinido (Recomendação do Comitê)

### MVP Core (O que DEVE estar funcionando)

```
┌──────────────────────────────────────────────────────────────────┐
│                    MVP REDEFINIDO                                  │
│                                                                   │
│  SITE PÚBLICO:                                                    │
│  ✅ Home (com seções de serviços e equipe inline)                 │
│  ✅ Fluxo de agendamento (4 passos)                               │
│  ✅ Tela de confirmação                                           │
│  ❌ Galeria, Sobre, FAQ, Blog, Promoções (V1)                     │
│                                                                   │
│  PAINEL ADMIN:                                                    │
│  ✅ Dashboard (métricas básicas)                                   │
│  ✅ CRUD de Serviços (nome, preço, duração)                       │
│  ✅ CRUD de Profissionais (nome, foto)                             │
│  ✅ Configuração de horários                                      │
│  ✅ Personalização básica (logo, cores)                           │
│  ❌ Relatórios, Financeiro, Marketing, Logs (V1+)                │
│                                                                   │
│  BACKEND:                                                         │
│  ✅ API de agendamento (criar, cancelar, disponibilidade)         │
│  ✅ API de serviços/profissionais (CRUD)                          │
│  ✅ Autenticação (login, JWT, RBAC)                               │
│  ✅ Multi-tenant (RLS + middleware)                               │
│  ✅ Rate limiting                                                 │
│  ❌ Pagamentos, WhatsApp, Email (V1)                              │
│                                                                   │
│  SEGURANÇA:                                                       │
│  ✅ 10 ressalvas resolvidas                                       │
│  ✅ Backup automático testado                                     │
│  ✅ Deploy com HTTPS                                              │
└──────────────────────────────────────────────────────────────────┘
```

### Métricas de Sucesso do MVP

| Métrica | Alvo |
|---------|:----:|
| Tempo para agendar | < 2 minutos |
| Tempo de onboarding (admin) | < 10 minutos |
| NPS (dono da barbearia) | ≥ 60 |
| NPS (cliente final) | ≥ 70 |
| Uptime | ≥ 99.5% |
| Bugs críticos | 0 |

---

## 5. Roadmap Imediato (Próximas 4 Semanas)

### Semana 1: Segurança + Infraestrutura
- [x] Resolver 10 ressalvas críticas
- [ ] Configurar backup automático + testar restore
- [ ] Criar ambiente de staging
- [ ] Deploy inicial em VPS

### Semana 2: Core API
- [ ] API de serviços (CRUD)
- [ ] API de profissionais (CRUD)
- [ ] API de tenant (criar, resolver subdomínio)
- [ ] API de disponibilidade (grid de horários)

### Semana 3: Core Features
- [ ] API de agendamento (criar, cancelar)
- [ ] Integração frontend ↔ backend (booking flow)
- [ ] Autenticação (login admin + barbeiro)
- [ ] WhatsApp (confirmação + lembrete básico)

### Semana 4: Polish + Beta
- [ ] Onboarding wizard (3 passos)
- [ ] Testes end-to-end
- [ ] Documentação de API (OpenAPI)
- [ ] Lançamento com 5 barbearias beta

---

## 6. O Que NÃO Entra no MVP (Parking Lot)

Estes itens estão documentados e planejados, mas NÃO serão implementados no MVP:

| Item | Quando |
|------|:------:|
| Pagamentos (PIX, cartão) | V1 |
| WhatsApp templates avançados | V1 |
| E-mail transacional | V1 |
| Galeria de fotos | V1 |
| Relatórios financeiros | V1 |
| Programa de fidelidade | V2 |
| Multi-unidade | V3 |
| Marketplace / API pública | V3 |
| IA / ML | V4 |

---

> **Nota Final (MVP): 7.0/10** — O MVP atual tem escopo adequado em termos de funcionalidades, mas está desbalanceado: muito esforço em documentação/design e pouco em implementação funcional. O foco das próximas 4 semanas deve ser exclusivamente em fazer o core funcionar. Remover itens não-essenciais do MVP libera ~40% do esforço para o que realmente importa: o fluxo de agendamento funcionando ponta-a-ponta.
