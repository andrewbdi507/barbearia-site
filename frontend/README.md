# 🎨 Barbershop SaaS — Frontend

> **Stack:** React 19 · TypeScript · Vite · TailwindCSS · Radix UI · Framer Motion  
> **Architecture:** Monorepo (pnpm workspaces) · Design System compartilhado  
> **Products:** Painel Administrativo + Site Público da Barbearia

---

## 📁 Estrutura do Monorepo

```
frontend/
├── packages/
│   └── design-system/              # UI Library compartilhada
│       └── src/
│           ├── components/         # Button, Input, Card, Modal, Toast, etc.
│           ├── tokens/             # Design tokens (cores, spacing, motion)
│           ├── themes/             # 5 temas (Urban, Luxury, Minimal, Classic, Modern)
│           ├── hooks/              # Hooks compartilhados
│           └── utils/              # cn(), helpers
│
├── apps/
│   ├── admin/                      # Painel Administrativo (SPA)
│   │   └── src/
│   │       ├── layouts/            # AdminLayout (sidebar + header)
│   │       ├── pages/              # Dashboard, Agenda, Clientes, Serviços, etc.
│   │       ├── components/         # Componentes específicos do admin
│   │       └── providers/          # Context providers
│   │
│   └── site/                       # Site Público da Barbearia (White-label)
│       └── src/
│           ├── layouts/            # PublicLayout (header + footer)
│           ├── pages/              # Home, Serviços, Equipe, Booking, Confirmação
│           ├── features/booking/   # Fluxo de agendamento
│           └── components/         # Componentes do site público
│
├── tooling/                        # Configurações compartilhadas
│   └── tailwind.config.ts
│
├── package.json                    # Workspace root
├── tsconfig.json                   # TypeScript base
└── README.md
```

---

## 🚀 Quick Start

### Pré-requisitos
- Node.js 20+
- pnpm 9+

### Instalação

```bash
cd frontend
pnpm install
```

### Desenvolvimento

```bash
# Painel Administrativo (http://localhost:5173)
pnpm dev:admin

# Site Público (http://localhost:3000)
pnpm dev:site
```

### Build

```bash
pnpm build:design-system
pnpm build:admin
pnpm build:site
```

---

## 🎨 Design System

O `@barbershop/design-system` é o coração visual da aplicação. Contém:

| Módulo | Descrição |
|--------|-----------|
| **Tokens** | Cores, tipografia, espaçamento, sombras, motion |
| **Temas** | 5 temas white-label (Urban, Luxury, Minimal, Classic, Modern) |
| **Componentes** | Button, Input, Card, Modal, Toast, Badge, Avatar, Skeleton, EmptyState, Spinner |
| **Utilitários** | `cn()` para merge de classes Tailwind |

### Temas Disponíveis

| Tema | Público | Cores |
|------|---------|-------|
| **Urban** | Barbearia moderna | Preto + vermelho |
| **Luxury** | Premium | Preto + dourado |
| **Minimal** | Clean | Cinza + branco |
| **Classic** | Tradicional | Marrom + bege |
| **Modern** | Jovem | Roxo + rosa |

---

## 📄 Páginas Implementadas

### Painel Admin (10 páginas)
- `/dashboard` — Dashboard com métricas
- `/agenda` — Agenda multi-profissional
- `/clients` — Lista de clientes
- `/professionals` — Equipe
- `/services` — Serviços (CRUD visual)
- `/financial` — Financeiro
- `/reports` — Relatórios
- `/settings` — Configurações
- `/settings/theme` — **Tema configurável** (5 temas + custom colors)

### Site Público (7 páginas)
- `/` — Home (hero, serviços, equipe, mapa)
- `/servicos` — Lista de serviços
- `/equipe` — Equipe
- `/galeria` — Galeria de fotos
- `/agendar` — **Fluxo de agendamento em 4 passos**
- `/confirmacao/:id` — Tela de confirmação
- `/perfil` — Perfil do cliente

---

## 🏗️ Arquitetura de Componentes

```
Design System (packages/design-system)
  ├── Primitives (Radix UI — sem estilo)
  ├── Styled Components (Tailwind + CVA)
  └── Compound Components (Card.Header, Card.Title, etc.)

Apps (apps/*)
  ├── Layouts (AdminLayout, PublicLayout)
  ├── Pages (composição de componentes do DS)
  └── Features (booking, upload, etc.)
```

---

## 🎯 Princípios

1. **Mobile First** — Todo componente nasce no mobile
2. **Composição > Configuração** — Compound components
3. **Acessibilidade** — WCAG 2.1 AA, Radix UI como base
4. **Performance** — Lazy loading, code splitting, memoização
5. **Dark Mode** — Suporte nativo via CSS custom properties
6. **White-Label** — Temas customizáveis por tenant
7. **TypeScript Strict** — Zero `any`, 100% cobertura de tipos

---

## 🔧 Comandos

```bash
pnpm lint           # Lint todos os pacotes
pnpm typecheck      # Type check todos os pacotes
pnpm format         # Formatar com Prettier
```
