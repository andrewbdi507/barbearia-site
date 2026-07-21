# 06 — Sitemap & Navegação

---

## 6.1 Sitemap Completo

```
barbersaas.com.br (Landing Page Plataforma)
│
├── /login
├── /cadastro
├── /precos
├── /blog
│
└── [subdomínio].barbersaas.com.br (Site Público do Tenant)
    │
    ├── / (Home)
    ├── /servicos
    ├── /equipe
    ├── /galeria
    ├── /sobre
    ├── /avaliacoes
    ├── /promocoes
    ├── /contato
    ├── /faq
    ├── /blog (futuro)
    │
    ├── /agendar
    │   ├── /agendar?step=1 (Profissional)
    │   ├── /agendar?step=2 (Serviço)
    │   ├── /agendar?step=3 (Data/Hora)
    │   └── /agendar?step=4 (Dados)
    │
    ├── /pagamento
    │   ├── /pagamento/pix
    │   ├── /pagamento/cartao
    │   └── /pagamento/confirmacao
    │
    ├── /confirmacao/:booking_id
    ├── /cancelar/:token
    ├── /reagendar/:token
    ├── /avaliar/:booking_id
    │
    └── /admin (Painel Administrativo do Tenant)
        │
        ├── /admin/dashboard
        ├── /admin/agenda
        │   ├── /admin/agenda/dia
        │   ├── /admin/agenda/semana
        │   └── /admin/agenda/mes
        │
        ├── /admin/clientes
        │   └── /admin/clientes/:id
        │
        ├── /admin/profissionais
        │   └── /admin/profissionais/:id
        │
        ├── /admin/servicos
        │
        ├── /admin/financeiro
        │   ├── /admin/financeiro/faturamento
        │   ├── /admin/financeiro/pagamentos
        │   └── /admin/financeiro/comissoes
        │
        ├── /admin/promocoes
        │   └── /admin/promocoes/cupons
        │
        ├── /admin/relatorios
        │
        ├── /admin/marketing
        │
        ├── /admin/avaliacoes
        │
        ├── /admin/configuracoes
        │   ├── /admin/configuracoes/geral
        │   ├── /admin/configuracoes/tema
        │   ├── /admin/configuracoes/horarios
        │   ├── /admin/configuracoes/notificacoes
        │   ├── /admin/configuracoes/dominio
        │   ├── /admin/configuracoes/permissoes
        │   └── /admin/configuracoes/integracoes
        │
        ├── /admin/logs
        │
        └── /admin/suporte
│
├── /app (PWA — Área do Barbeiro)
│   ├── /app/agenda
│   ├── /app/clientes
│   ├── /app/ganhos
│   ├── /app/perfil
│   └── /app/configuracoes
│
├── /recepcao (Painel da Recepcionista)
│   ├── /recepcao/agenda
│   ├── /recepcao/checkin
│   ├── /recepcao/clientes
│   └── /recepcao/espera
│
└── /super-admin (Plataforma SaaS)
    ├── /super-admin/dashboard
    ├── /super-admin/tenants
    ├── /super-admin/planos
    ├── /super-admin/financeiro
    ├── /super-admin/logs
    ├── /super-admin/metricas
    └── /super-admin/configuracoes
```

---

## 6.2 Fluxograma de Navegação

### Fluxo Principal: Agendamento

```
                    ┌─────────────┐
                    │  Instagram  │
                    │  Google     │
                    │  Indicação  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Home Site  │
                    │  (Tenant)   │
                    └──┬──┬──┬───┘
                       │  │  │
          ┌────────────┘  │  └────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐    ┌──────────┐
    │ Serviços │   │  Equipe  │    │ Galeria  │
    └────┬─────┘   └────┬─────┘    └──────────┘
         │              │
         └──────┬───────┘
                ▼
         ┌────────────┐
         │  AGENDAR   │
         │  Passo 1   │  Profissional
         │  Passo 2   │  Serviço
         │  Passo 3   │  Data/Hora
         │  Passo 4   │  Dados
         └─────┬──────┘
               │
               ▼
         ┌────────────┐
         │ Pagamento  │ (V1+)
         │ PIX/Cartão │
         └─────┬──────┘
               │
               ▼
         ┌────────────┐
         │Confirmação │
         └─────┬──────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
  ┌──────┐ ┌──────┐ ┌──────┐
  │Google│ │Apple │ │Voltar│
  │ Cal  │ │ Cal  │ │ Home │
  └──────┘ └──────┘ └──────┘
```

### Fluxo: Painel Admin (Dono)

```
                    ┌─────────────┐
                    │   LOGIN     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  DASHBOARD  │ ← Tela inicial
                    └──┬──┬──┬───┘
                       │  │  │
         ┌─────────────┘  │  └──────────────┐
         ▼                ▼                 ▼
   ┌──────────┐    ┌──────────┐     ┌──────────────┐
   │  Agenda  │    │Clientes  │     │ Financeiro   │
   └──────────┘    └──────────┘     └──────────────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  ┌──────────┐    ┌──────────────┐   ┌──────────────┐
  │ Serviços │    │Profissionais │   │Configurações │
  └──────────┘    └──────────────┘   └──────────────┘
                                             │
                          ┌──────────────────┼──────────────┐
                          ▼                  ▼              ▼
                    ┌──────────┐     ┌──────────┐   ┌──────────┐
                    │   Tema   │     │Horários  │   │Permissões│
                    └──────────┘     └──────────┘   └──────────┘
```

---

## 6.3 Navegação por Perfil

### Cliente Final (Site Público)

```
Header:
┌──────────────────────────────────────────────────────────────┐
│ LOGO    Serviços  Equipe  Galeria  Sobre  Contato  [AGENDAR] │
└──────────────────────────────────────────────────────────────┘

Footer:
┌──────────────────────────────────────────────────────────────┐
│ © Studio 27 · Rua Augusta, 1234                               │
│ 🟢 WhatsApp  📷 Instagram  📘 Facebook                       │
│ Seg-Sex 9h-19h · Sáb 9h-14h                                  │
│ Política de Privacidade · Termos de Uso                       │
└──────────────────────────────────────────────────────────────┘

Mobile: Menu hamburger + WhatsApp flutuante fixo
```

### Dono / Admin (Painel)

```
Sidebar (Desktop):
┌──────────────┐
│ 📊 Dashboard │
│ 📅 Agenda    │
│ 👥 Clientes  │
│ 💇 Profiss.  │
│ ✂️ Serviços  │
│ 💰 Financeiro│
│ 🎫 Promoções │
│ 📈 Relatórios│
│ 📣 Marketing │
│ ⭐ Avaliações│
│ ⚙️ Config.   │
│ 📋 Logs      │
│ 🆘 Suporte   │
└──────────────┘

Mobile: Bottom tab bar (5 principais) + hamburger para o resto
┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
│📊 │ │📅 │ │👥 │ │💰 │ │☰  │
└───┘ └───┘ └───┘ └───┘ └───┘
```

### Barbeiro (App/PWA)

```
Bottom Tab Bar (sempre visível):
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│  📅   │ │  💰   │ │  👤   │ │  ⚙️   │ │  📊   │
│Agenda │ │Ganhos │ │Clientes│ │Perfil │ │Relat. │
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

### Recepcionista

```
Top Bar: Filtros de profissional
┌──────────────────────────────────────────────────────┐
│ Todos │ Marcos │ Ricardo │ Lucas │ [+ Check-in]      │
└──────────────────────────────────────────────────────┘

Main: Agenda multi-coluna (scroll vertical + horizontal)

Bottom:
┌──────────────────────────────────────────────────────┐
│ [+ Agendamento]  [📋 Lista Espera]  [🔍 Buscar]      │
└──────────────────────────────────────────────────────┘
```

---

## 6.4 Breadcrumbs

```
Site Público:
Home > Serviços
Home > Equipe > Marcos
Home > Agendar > Confirmação

Painel Admin:
Dashboard > Clientes > João Silva
Dashboard > Configurações > Tema

Super Admin:
Dashboard > Tenants > Studio 27
```

---

## 6.5 Regras de Navegação

| Regra | Descrição |
|-------|-----------|
| **Home sempre acessível** | Logo no header = link para home |
| **CTA persistente** | "Agendar" sempre visível (header desktop, botão fixo mobile) |
| **Máximo 3 níveis** | Nenhuma página a mais de 3 cliques da home |
| **Voltar consistente** | Botão "< Voltar" para o passo anterior, não para home |
| **Breadcrumbs no admin** | Para páginas com profundidade > 2 |
| **Busca global** | No admin: `Ctrl+K / Cmd+K` abre busca |
| **Atalhos de teclado** | Admin: `N` = novo agendamento, `C` = clientes, `D` = dashboard |

---

> **Princípio:** O sitemap revela a estrutura mental do produto. Cada página tem um propósito claro. Nada está a mais de 3 cliques da home. A navegação é previsível e consistente em todos os perfis.
