# 05 — Jornada do Super Administrador (SaaS)

> **Persona:** Você (CTO / Fundador) — O único com acesso à plataforma  
> **Dispositivo:** Desktop (80%) / Mobile (20%)  
> **Objetivo:** Gerenciar tenants, assinaturas, saúde da plataforma

---

## 5.1 Tela Principal: Dashboard da Plataforma

```
┌──────────────────────────────────────────────────────────────┐
│  🖥️ BARBERSAAS — SUPER ADMIN                                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ ☰ │ Dashboard │ Tenants │ Planos │ Financeiro │ Logs ⚙️  ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Tenants  │ │ MRR      │ │ Churn    │ │ Trials   │        │
│  │   847    │ │ R$ 84.7K │ │  3,2%    │ │  +23     │        │
│  │  ↑12     │ │ ↑8%      │ │ ↓0.5%    │ │ esta sem │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                               │
│  ┌──────────────────────────┐ ┌─────────────────────────────┐│
│  │ MRR Growth (6 meses)     │ │ Tenants por Plano            ││
│  │         📈                │ │        🍩                    ││
│  │    ██░░░░░░░░░░░░░░░░░░  │ │ Starter:  320 (38%)         ││
│  │    ███░░░░░░░░░░░░░░░░░  │ │ Pro:      380 (45%)         ││
│  │    ████████████████████  │ │ Business: 120 (14%)          ││
│  └──────────────────────────┘ │ Enterprise: 27 (3%)          ││
│                               └─────────────────────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Últimas Atividades                                       ││
│  │ 🟢 Novo tenant: Studio 28 Barbearia — Plano Pro          ││
│  │ 🟡 Trial expirando: Barbearia do Zé — 2 dias             ││
│  │ 🔴 Pagamento recusado: Corte's Club — 3ª tentativa       ││
│  │ 🟢 Upgrade: Vintage Barber (Starter → Pro)               ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## 5.2 Tela: Gestão de Tenants

```
┌──────────────────────────────────────────────────────────────┐
│  🏪 TENANTS (847)                           [+ Novo Tenant]   │
│                                                               │
│  🔍 Buscar...  │ Plano: [Todos ▾] │ Status: [Ativo ▾]       │
│                                                               │
│  ┌──────┬──────────────────┬─────────┬────────┬────────────┐ │
│  │Tenant│ Nome             │ Plano   │ Status │ MRR        │ │
│  ├──────┼──────────────────┼─────────┼────────┼────────────┤ │
│  │ t_001│ Studio 27        │ Pro     │ 🟢 Atv │ R$ 99,90   │ │
│  │ t_002│ Vintage Barber   │Business │ 🟢 Atv │ R$ 199,90  │ │
│  │ t_003│ Barbearia do Zé  │ Starter │ 🟡 Trl │ R$ 0       │ │
│  │ t_004│ Corte's Club      │ Pro     │ 🔴 Susp│ R$ 0       │ │
│  │ ...  │ ...              │ ...     │ ...    │ ...        │ │
│  └──────┴──────────────────┴─────────┴────────┴────────────┘ │
│                                                               │
│  Ações por tenant: [Ver] [Editar] [Suspender] [Impersonar]   │
└──────────────────────────────────────────────────────────────┘
```

### Modal: Detalhes do Tenant

```
┌──────────────────────────────────────────────────────────────┐
│  Studio 27 Barbearia                          t_001           │
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                  │
│  │ 👤 Admin         │  │ 📊 Uso           │                  │
│  │ Carlos Oliveira  │  │ Agendamentos: 320 │                  │
│  │ carlos@...       │  │ Clientes: 145    │                  │
│  │ (11) 99999-9999  │  │ Profissionais: 4 │                  │
│  └──────────────────┘  │ Storage: 45 MB   │                  │
│                         └──────────────────┘                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Assinatura                                               ││
│  │ Plano: Pro — R$ 99,90/mês                                ││
│  │ Desde: 15/01/2026                                        ││
│  │ Próx. cobrança: 15/08/2026                               ││
│  │ Status: 🟢 Ativo                                         ││
│  │                                      [Alterar Plano ▾]   ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ Ações                                                    ││
│  │ [Impersonar] [Suspender] [Resetar Senha] [Excluir]       ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## 5.3 Tela: Planos e Assinaturas

```
┌──────────────────────────────────────────────────────────────┐
│  💳 PLANOS                                                    │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ Starter  │ │ Pro      │ │ Business │ │ Enterprise   │    │
│  │ R$49,90  │ │ R$99,90  │ │R$199,90  │ │ R$499,90     │    │
│  │          │ │          │ │          │ │              │    │
│  │ 1 prof.  │ │ 5 profs. │ │20 profs. │ │ Ilimitado    │    │
│  │ Site bás │ │ CRM      │ │ White-lab│ │ Customizações│    │
│  │ Agenda   │ │ Relatórios│ │ API      │ │ SLA          │    │
│  │          │ │ Notific. │ │ Multi-un │ │ Onboarding   │    │
│  │          │ │          │ │ Domínio  │ │              │    │
│  │[Editar]  │ │[Editar]  │ │[Editar]  │ │[Editar]      │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
│                                                               │
│  [+ Criar novo plano]                                         │
│  [+ Criar cupom promocional]                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 5.4 Tela: Logs de Auditoria

```
┌──────────────────────────────────────────────────────────────┐
│  📋 LOGS DE AUDITORIA                                         │
│                                                               │
│  Filtros:                                                     │
│  Tenant: [Todos ▾]  Evento: [Todos ▾]  Período: [7 dias ▾]  │
│                                                               │
│  ┌──────┬──────────┬──────────┬──────────┬──────────────────┐│
│  │ Data │ Tenant   │ Usuário  │ Evento   │ Detalhes         ││
│  ├──────┼──────────┼──────────┼──────────┼──────────────────┤│
│  │09:15 │ t_001    │ Carlos   │ login    │ IP 189.54.32.10  ││
│  │09:14 │ t_003    │ —        │ booking  │ Cliente agendou   ││
│  │09:10 │ t_007    │ admin    │ service. │ Alterou preço     ││
│  │09:05 │ PLATFORM │ super    │ tenant.  │ Criou t_050       ││
│  └──────┴──────────┴──────────┴──────────┴──────────────────┘│
│                                                               │
│  🔴 Eventos de segurança:                                     │
│  ┌──────┬──────────┬────────────────────────────────────────┐│
│  │09:01 │ t_012    │ ⚠️ Tentativa cross-tenant detectada    ││
│  │08:45 │ t_005    │ ⚠️ 5 falhas de login                   ││
│  └──────┴──────────┴────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## 5.5 Tela: Métricas do Sistema

```
┌──────────────────────────────────────────────────────────────┐
│  📊 SAÚDE DO SISTEMA                                          │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Uptime   │ │ P95 Lat  │ │ Error Rt │ │ Requests │        │
│  │ 99.97%   │ │ 180ms    │ │ 0.02%    │ │ 1.2K/min │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                               │
│  ┌──────────────────────────┐ ┌─────────────────────────────┐│
│  │ Latência por Endpoint    │ │ DB Connections               ││
│  │ GET /bookings    120ms   │ │ ████████░░ 80% (40/50)      ││
│  │ POST /bookings   250ms   │ │                              ││
│  │ GET /services     45ms   │ │ Redis Memory                 ││
│  │ GET /schedule     85ms   │ │ ██████░░░░ 60% (600MB/1GB)  ││
│  └──────────────────────────┘ └─────────────────────────────┘│
│                                                               │
│  🔔 Alertas ativos: 0                                          │
│  💾 Último backup: 03:00 (sucesso, 2.3 GB)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 5.6 Tela: Impersonar Tenant (Suporte)

```
┌──────────────────────────────────────────────────────────────┐
│  ⚠️ MODO IMPERSONAÇÃO — Studio 27 Barbearia                   │
│                                                               │
│  Você está logado como: Carlos Oliveira (Admin)               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ ⚠️ Todas as ações serão registradas como super admin     ││
│  │    e atribuídas ao tenant. Use com responsabilidade.     ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  [SAIR DO MODO IMPERSONAÇÃO]                                  │
│                                                               │
│  ─── O painel do tenant é exibido abaixo ───                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 5.7 Mobile (Super Admin)

```
┌──────────────────────┐
│ 📱 Super Admin       │
│                      │
│ 🏪 847 tenants       │
│ 💰 R$ 84.7K MRR      │
│ 📉 3.2% churn        │
│                      │
│ 🟢 Sistema: OK       │
│ ✅ Backup: OK        │
│                      │
│ ⚠️ 2 ações pendentes │
│                      │
│ [Tenants] [Planos]   │
│ [Métricas] [Logs]    │
└──────────────────────┘
```

---

> **Resumo:** O Super Admin é o cockpit da plataforma. Dashboard com métricas de negócio (MRR, churn, trials) e saúde técnica (uptime, latência, erros). Capacidade de impersonar tenants para suporte. Logs de auditoria para segurança e compliance. Tudo que o CTO precisa para dormir tranquilo.
