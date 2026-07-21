# 08 — Arquitetura Modular

---

## 8.1 Filosofia de Modularização

Cada módulo é uma unidade independente com:

- **Domínio próprio** (entidades, regras de negócio)
- **API bem definida** (contratos de entrada e saída)
- **Banco isolado logicamente** (schema ou tabelas próprias)
- **Baixo acoplamento** com outros módulos (via interfaces)
- **Alta coesão interna** (tudo que pertence ao módulo está nele)

A comunicação entre módulos segue o princípio: **síncrono via interface (para operações que exigem resposta) e assíncrono via eventos (para side effects).**

---

## 8.2 Módulos do MVP (Versão 0)

### Módulo 1: Tenant & White-Label
```
┌─────────────────────────────┐
│     TENANT & WHITE-LABEL    │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • CRUD de tenants           │
│ • Configurações por tenant  │
│ • Personalização visual     │
│ • Domínios e subdomínios    │
│ • Resolução de tenant       │
│                             │
│ Entidades:                  │
│ • Tenant                    │
│ • TenantSettings            │
│ • TenantBranding            │
│ • TenantDomain              │
│                             │
│ Dependências:               │
│ • Nenhuma (módulo raiz)     │
└─────────────────────────────┘
```

### Módulo 2: Auth & RBAC
```
┌─────────────────────────────┐
│       AUTH & RBAC           │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • Login / Logout            │
│ • Registro de usuários      │
│ • JWT (access + refresh)    │
│ • RBAC (roles, permissions) │
│ • Recuperação de senha      │
│ • Verificação de e-mail     │
│                             │
│ Entidades:                  │
│ • User                      │
│ • Role                      │
│ • Permission                │
│ • Session                   │
│ • RefreshToken              │
│                             │
│ Dependências:               │
│ • Tenant (cada user ∈ 1 tenant)│
└─────────────────────────────┘
```

### Módulo 3: Scheduling (Agendamento)
```
┌─────────────────────────────┐
│        SCHEDULING           │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • Grid de horários          │
│ • Criação de agendamento    │
│ • Conflito de horários      │
│ • Cancelamento              │
│ • Reagendamento             │
│ • Status do agendamento     │
│ • Duração dinâmica          │
│                             │
│ Entidades:                  │
│ • Service                   │
│ • Professional              │
│ • Schedule (horários)       │
│ • Booking                   │
│ • BookingStatus             │
│ • Customer                  │
│                             │
│ Dependências:               │
│ • Tenant (isolamento)       │
│ • Auth (identificação)      │
│                             │
│ Eventos emitidos:           │
│ • booking.created           │
│ • booking.cancelled         │
│ • booking.reminded          │
└─────────────────────────────┘
```

### Módulo 4: Notification
```
┌─────────────────────────────┐
│       NOTIFICATION          │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • Consumo de eventos        │
│ • Envio WhatsApp            │
│ • Envio E-mail              │
│ • Templates de mensagem     │
│ • Retry e DLQ               │
│ • Status de entrega         │
│                             │
│ Entidades:                  │
│ • Notification              │
│ • NotificationTemplate      │
│ • NotificationChannel       │
│                             │
│ Dependências:               │
│ • Tenant (templates por tenant)│
│ • Serviços externos:        │
│   - Evolution API (WhatsApp)│
│   - AWS SES / Resend (Email)│
│                             │
│ Eventos consumidos:         │
│ • booking.created           │
│ • booking.cancelled         │
│ • booking.reminder          │
└─────────────────────────────┘
```

---

## 8.3 Módulos da V1 (0–6 meses)

### Módulo 5: Payment
```
┌─────────────────────────────┐
│         PAYMENT             │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • Integração com gateways   │
│ • Payment Intent            │
│ • Webhook handler           │
│ • Conciliação               │
│ • Reembolso                 │
│ • Histórico de pagamentos   │
│                             │
│ Entidades:                  │
│ • Payment                   │
│ • PaymentMethod             │
│ • PaymentGateway            │
│ • Refund                    │
│                             │
│ Dependências:               │
│ • Tenant                    │
│ • Scheduling (booking)      │
│                             │
│ Eventos emitidos:           │
│ • payment.succeeded         │
│ • payment.failed            │
│ • payment.refunded          │
└─────────────────────────────┘
```

### Módulo 6: CRM
```
┌─────────────────────────────┐
│           CRM               │
├─────────────────────────────┤
│ Responsabilidades:          │
│ • Ficha do cliente          │
│ • Histórico de visitas      │
│ • Preferências              │
│ • Segmentação               │
│ • Anotações internas        │
│ • Última visita             │
│ • Frequência                │
│                             │
│ Entidades:                  │
│ • CustomerProfile           │
│ • VisitHistory              │
│ • CustomerNote              │
│ • CustomerPreference        │
│ • CustomerSegment           │
│                             │
│ Dependências:               │
│ • Tenant                    │
│ • Scheduling                │
└─────────────────────────────┘
```

---

## 8.4 Módulos da V2 (6–18 meses)

### Módulo 7: Reports & Analytics
### Módulo 8: Promotions & Loyalty
### Módulo 9: Media Gallery

---

## 8.5 Módulos da V3 (18–36 meses)

### Módulo 10: Multi-Unit (Franquias)
### Módulo 11: Marketplace & Integrações
### Módulo 12: Public API

---

## 8.6 Módulos da V4 (36–60 meses)

### Módulo 13: AI / ML (Precificação, Previsão de Demanda)
### Módulo 14: Expansão Internacional (i18n, moedas, gateways locais)

---

## 8.7 Matriz de Dependências entre Módulos

```
                    ┌─────────┐
                    │ Tenant  │ (módulo raiz)
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │   Auth    │  │ Scheduler │  │  Media    │
    └─────┬─────┘  └─────┬─────┘  └───────────┘
          │              │
          │      ┌───────┼───────┐
          │      │       │       │
    ┌─────▼──────▼┐ ┌────▼────┐ ┌▼──────────┐
    │     CRM     │ │Payment │ │Notification│
    └─────────────┘ └────────┘ └────────────┘
                         │
                         ▼
                   ┌──────────┐
                   │ Reports  │
                   └──────────┘
```

---

## 8.8 Resumo de Módulos por Versão

| Módulo | MVP | V1 | V2 | V3 | V4 |
|--------|:---:|:--:|:--:|:--:|:--:|
| Tenant & White-Label | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auth & RBAC | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scheduling | ✅ | ✅ | ✅ | ✅ | ✅ |
| Notification | ✅ | ✅ | ✅ | ✅ | ✅ |
| Payment | ❌ | ✅ | ✅ | ✅ | ✅ |
| CRM | ❌ | ✅ | ✅ | ✅ | ✅ |
| Reports & Analytics | ❌ | ❌ | ✅ | ✅ | ✅ |
| Promotions & Loyalty | ❌ | ❌ | ✅ | ✅ | ✅ |
| Media Gallery | ❌ | ❌ | ✅ | ✅ | ✅ |
| Multi-Unit | ❌ | ❌ | ❌ | ✅ | ✅ |
| Marketplace | ❌ | ❌ | ❌ | ✅ | ✅ |
| Public API | ❌ | ❌ | ❌ | ✅ | ✅ |
| AI / ML | ❌ | ❌ | ❌ | ❌ | ✅ |
| i18n | ❌ | ❌ | ❌ | ❌ | ✅ |

---

> **Princípio:** Cada módulo é pequeno o suficiente para ser compreendido por uma pessoa e grande o suficiente para entregar valor de negócio independente. Módulos são deployáveis separadamente quando necessário, mas compartilham o mesmo banco de dados (schema lógico) para simplicidade operacional.
