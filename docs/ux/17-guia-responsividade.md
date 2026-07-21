# 17 — Guia de Responsividade

> Mobile-first: projete para 375px, adapte para cima.

---

## 17.1 Filosofia Mobile-First

```
1. PROJETAR → Mobile (375px)
2. ADAPTAR → Tablet (768px)
3. EXPANDIR → Desktop (1024px)
4. OTIMIZAR → Wide (1440px+)
```

**Nunca:** projetar desktop e "espremer" para mobile.

---

## 17.2 Breakpoints

| Nome | Min Width | Dispositivo Típico |
|------|:--------:|-------------------|
| `xs` | 0px | Smartphone retrato |
| `sm` | 640px | Smartphone paisagem / Tablet pequeno |
| `md` | 768px | Tablet retrato |
| `lg` | 1024px | Tablet paisagem / Desktop pequeno |
| `xl` | 1280px | Desktop padrão |
| `2xl` | 1536px | Desktop grande |

### Container

```css
.container {
  width: 100%;
  padding: 0 16px; /* mobile */
}

@media (min-width: 640px) {
  .container { padding: 0 24px; }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 32px;
  }
}
```

---

## 17.3 Padrões de Adaptação

### Navegação

| Breakpoint | Site Público | Painel Admin |
|-----------|-------------|-------------|
| **xs-mobile** | Menu hamburger + CTA fixo bottom | Bottom tab bar (5 itens) + hamburger |
| **md-tablet** | Menu hamburger ou nav reduzida | Sidebar colapsada (ícones) |
| **lg-desktop** | Nav horizontal completa | Sidebar expandida (240px) + conteúdo |

### Grid de Cards

| Breakpoint | Site Público | Painel Admin |
|-----------|-------------|-------------|
| **xs** | 1 coluna | 1 coluna |
| **sm** | 2 colunas | 2 colunas |
| **md** | 2 colunas | 2-3 colunas |
| **lg** | 3 colunas | 3 colunas |
| **xl** | 4 colunas | 4 colunas |

### Tabelas

| Breakpoint | Comportamento |
|-----------|--------------|
| **xs-sm** | Tabela vira cards empilhados (cada linha = 1 card) |
| **md+** | Tabela normal com scroll horizontal se necessário |

---

## 17.4 Comportamentos Específicos

### Hero Section

```
Mobile:
┌────────────────────┐
│       LOGO         │
│                    │
│  Banner (100% vw)  │
│  Altura: 60vh      │
│  Overlay de texto  │
│       [CTA]        │
└────────────────────┘

Desktop:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  Banner (100% vw, altura: 80vh)                              │
│                                                              │
│  ┌──────────────────────┐                                    │
│  │ Texto + CTA alinhado │                                    │
│  │ à esquerda           │                                    │
│  └──────────────────────┘                                    │
└──────────────────────────────────────────────────────────────┘
```

### Agenda Multi-Profissional (Recepção)

```
Mobile (xs-md):
┌────────────────────┐
│ [Todos ▾]          │
│                    │
│ ┌────────────────┐ │
│ │ 09:00          │ │
│ │ Marcos: Corte  │ │
│ │ Ricardo: Livre │ │
│ │ Lucas: Barba   │ │
│ └────────────────┘ │
│ ┌────────────────┐ │
│ │ 09:30          │ │
│ │ ...            │ │
│ └────────────────┘ │
└────────────────────┘

Desktop (lg+):
Tabela multi-coluna com scroll horizontal
(ver wireframe da recepcionista)
```

### Modal

```
Mobile: Full-screen (100vw × 100vh)
Tablet/Desktop: Centralizado (max-width 560px, max-height 90vh)
```

### Sidebar (Admin)

```
Mobile: Drawer (overlay, abre da esquerda com swipe/botão)
Desktop: Fixa (240px), sempre visível
```

---

## 17.5 Imagens Responsivas

```html
<img
  src="hero-mobile.webp"
  srcset="
    hero-mobile.webp   640w,
    hero-tablet.webp  1024w,
    hero-desktop.webp 1920w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 80vw,
    1200px
  "
  alt="Studio 27 Barbearia"
  loading="lazy"
/>
```

---

## 17.6 Tipografia Responsiva

```css
/* Mobile (padrão) */
h1 { font-size: 24px; }
h2 { font-size: 20px; }
body { font-size: 16px; }

/* Tablet */
@media (min-width: 768px) {
  h1 { font-size: 28px; }
  h2 { font-size: 22px; }
}

/* Desktop */
@media (min-width: 1024px) {
  h1 { font-size: 32px; }
  h2 { font-size: 24px; }
}
```

---

## 17.7 Touch vs. Mouse

| Comportamento | Touch (Mobile) | Mouse (Desktop) |
|--------------|---------------|-----------------|
| **Hover** | Não existe | Efeitos visuais (elevação, cor) |
| **Click** | Tap (≥48px alvo) | Click (≥24px alvo) |
| **Scroll** | Swipe vertical | Scroll wheel / barra |
| **Menu** | Hamburger / Bottom tab | Nav horizontal / Sidebar fixa |
| **Dropdown** | Bottom sheet | Popover abaixo do trigger |

### Regra: Todo elemento interativo deve funcionar com touch E mouse.

---

## 17.8 Teste de Responsividade

### Checklist por Breakpoint

- [ ] **375px (iPhone SE):** Layout não quebra, texto legível, botões tocáveis
- [ ] **414px (iPhone 14):** " — espaçamento adequado
- [ ] **768px (iPad Mini):** Sidebar aparece, grid 2 colunas
- [ ] **1024px (iPad Pro):** Layout desktop funcional
- [ ] **1440px (Desktop):** Conteúdo centralizado, não estica infinitamente
- [ ] **1920px (Desktop Largo):** Max-width container funciona

---

## 17.9 PWA — Considerações Mobile

- **Safe areas:** Respeitar `env(safe-area-inset-*)` para iPhones com notch
- **Bottom nav:** Posicionar acima da home indicator
- **Pull-to-refresh:** Comportamento nativo do navegador
- **Tap highlight:** `-webkit-tap-highlight-color: transparent` com alternativa de focus
- **Zoom:** Não desabilitar (acessibilidade)
- **Orientation:** Funcionar em retrato E paisagem

---

> **Resumo:** Responsividade não é "funcionar no celular" — é "nascer no celular". Toda decisão de layout começa na tela de 375px. Se funciona ali, vai funcionar em qualquer lugar. Mobile-first é a única abordagem que faz sentido quando 90% dos usuários estão no celular.
