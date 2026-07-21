# 12 — Design System

> **Nome:** Barbershop Design System (BDS)  
> **Versão:** 1.0.0  
> **Referências:** Material Design 3 · Radix UI · shadcn/ui · Shopify Polaris

---

## 12.1 Princípios do Design System

1. **Consistente** — Mesmo componente em todo o ecossistema (site público + admin)
2. **Acessível** — WCAG 2.1 AA como baseline
3. **Customizável** — Design tokens permitem white-label por tenant
4. **Mobile-First** — Todo componente nasce no mobile e escala para desktop
5. **Performático** — Zero dependências pesadas, CSS custom properties

---

## 12.2 Design Tokens

### Cores — Base (Light Mode)

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-primary` | `#1a1a2e` | Botões principais, links, destaque |
| `--color-primary-hover` | `#16213e` | Hover de botões primários |
| `--color-primary-light` | `#e8e8f0` | Background de tags, badges |
| `--color-secondary` | `#e94560` | CTAs, ofertas, alertas |
| `--color-secondary-hover` | `#d63851` | Hover secundário |
| `--color-success` | `#27ae60` | Confirmação, status positivo |
| `--color-warning` | `#f39c12` | Alertas, atenção |
| `--color-error` | `#e74c3c` | Erros, perigo |
| `--color-info` | `#3498db` | Informação |

### Cores — Superfície & Texto

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-bg` | `#fafafa` | Fundo da página |
| `--color-surface` | `#ffffff` | Cards, modais, inputs |
| `--color-surface-hover` | `#f5f5f5` | Hover em linhas, cards |
| `--color-border` | `#e0e0e0` | Bordas de cards, inputs |
| `--color-border-focus` | `--color-primary` | Borda em foco |
| `--color-text-primary` | `#1a1a2e` | Texto principal |
| `--color-text-secondary` | `#666680` | Texto secundário, labels |
| `--color-text-disabled` | `#9e9eb0` | Texto desabilitado |
| `--color-text-inverse` | `#ffffff` | Texto sobre fundo escuro |

### Cores — Tenant Customizável

| Token | Default | Tenant pode alterar? |
|-------|---------|:--------------------:|
| `--color-primary` | `#1a1a2e` | ✅ Sim |
| `--color-secondary` | `#e94560` | ✅ Sim |
| `--color-bg` | `#fafafa` | ✅ Sim |
| `--color-surface` | `#ffffff` | ✅ Sim |

### Dark Mode (Painel Admin — V1+)

```
┌────────────────────────────────────┐
│ Modo claro/escuro: toggle no       │
│ header do painel admin             │
│                                    │
│ ☀️ Claro  │  🌙 Escuro            │
│           │                        │
│ Respeita preferência do sistema    │
│ (prefers-color-scheme)             │
└────────────────────────────────────┘
```

---

## 12.3 Tipografia

### Font Family

| Uso | Família | Fallback |
|-----|---------|----------|
| **Títulos** | Inter | system-ui, sans-serif |
| **Corpo** | Inter | system-ui, sans-serif |
| **Mono** | JetBrains Mono | monospace |

### Escala Tipográfica

| Nome | Size | Line Height | Weight | Uso |
|------|------|:----------:|:------:|-----|
| `text-xs` | 12px | 1.5 | 400 | Badges, labels pequenos |
| `text-sm` | 14px | 1.5 | 400 | Texto secundário, legendas |
| `text-base` | 16px | 1.6 | 400 | Corpo de texto padrão |
| `text-lg` | 18px | 1.5 | 500 | Subtítulos, cards |
| `text-xl` | 20px | 1.4 | 600 | Títulos de seção |
| `text-2xl` | 24px | 1.3 | 700 | Títulos de página |
| `text-3xl` | 32px | 1.2 | 700 | Hero titles (site público) |
| `text-4xl` | 40px | 1.1 | 800 | Hero (desktop) |

---

## 12.4 Espaçamentos

Base: 4px grid

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` | 4px | Ícone + texto |
| `--space-2` | 8px | Entre elementos internos |
| `--space-3` | 12px | Padding de cards pequenos |
| `--space-4` | 16px | Padding padrão de cards |
| `--space-5` | 20px | Padding de modais |
| `--space-6` | 24px | Entre seções |
| `--space-8` | 32px | Margem de página (mobile) |
| `--space-10` | 40px | Margem de página (desktop) |
| `--space-12` | 48px | Hero padding |
| `--space-16` | 64px | Seções grandes |

---

## 12.5 Bordas e Sombras

### Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-sm` | 4px | Inputs, badges |
| `--radius-md` | 8px | Cards, botões |
| `--radius-lg` | 12px | Modais, imagens |
| `--radius-xl` | 16px | Cards de destaque |
| `--radius-full` | 9999px | Pills, avatares |

### Sombras

| Token | Valor | Uso |
|-------|-------|-----|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Cards sutis |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.08)` | Cards padrão |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.12)` | Modais, dropdowns |
| `--shadow-xl` | `0 12px 48px rgba(0,0,0,0.15)` | Hero overlay |

---

## 12.6 Breakpoints

| Nome | Min Width | Dispositivo | Layout |
|------|:--------:|-------------|--------|
| `xs` | 0 | Smartphone (retrato) | 1 coluna, stack |
| `sm` | 640px | Smartphone (paisagem) | 1-2 colunas |
| `md` | 768px | Tablet | 2 colunas, sidebar |
| `lg` | 1024px | Desktop pequeno | Sidebar visível, 2-3 colunas |
| `xl` | 1280px | Desktop | 3-4 colunas, conteúdo máximo |
| `2xl` | 1536px | Desktop grande | Max-width container (1200px) |

### Container

```
Mobile: 100% width - 32px padding (16px cada lado)
Desktop: max-width 1200px, centralizado
```

---

## 12.7 Motion & Timing

| Token | Valor | Uso |
|-------|-------|-----|
| `--duration-instant` | 100ms | Hover, focus |
| `--duration-fast` | 200ms | Transições de UI |
| `--duration-normal` | 300ms | Modal abrir/fechar |
| `--duration-slow` | 500ms | Animações de entrada |
| `--ease-default` | `cubic-bezier(0.4, 0, 0.2, 1)` | Padrão Material |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Entrada |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Saída |
| `--ease-bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Impacto (confirmação) |

---

## 12.8 Grid System

### Mobile (0-767px)
- 4 colunas
- Gutter: 16px
- Margin: 16px

### Tablet (768-1023px)
- 8 colunas
- Gutter: 24px
- Margin: 24px

### Desktop (1024px+)
- 12 colunas
- Gutter: 24px
- Margin: auto (max 1200px)

---

## 12.9 Ícones

### Biblioteca: Lucide Icons

- 1000+ ícones
- SVG puro
- Customizável (cor, tamanho, stroke)
- Tree-shakeable (só importa o que usa)

### Tamanhos

| Nome | Size | Uso |
|------|------|-----|
| `icon-sm` | 16px | Badges, inline |
| `icon-md` | 20px | Botões, inputs |
| `icon-lg` | 24px | Headers, navegação |
| `icon-xl` | 32px | Hero, empty states |

---

## 12.10 Elevação (Z-Index)

| Camada | z-index | Componentes |
|--------|:------:|-------------|
| Base | 0 | Conteúdo da página |
| Dropdown | 10 | Dropdowns, selects |
| Sticky | 20 | Header fixo, sidebar |
| Overlay | 30 | Overlay de modal |
| Modal | 40 | Modal, drawer |
| Toast | 50 | Notificações toast |
| Tooltip | 60 | Tooltips |

---

> **Resumo:** O Design System é a "single source of truth" visual. Cada componente, cada cor, cada espaço é um token. Isso garante consistência em todas as telas (site público, admin, barbeiro, recepção) e permite personalização por tenant sem quebrar o sistema.
