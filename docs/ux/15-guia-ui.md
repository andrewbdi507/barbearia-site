# 15 — Guia de UI (Interface Design)

> Princípios de design visual, layout e composição.

---

## 15.1 Filosofia Visual

O Barbershop SaaS segue uma estética **clean, moderna e funcional**, inspirada em:

- **Stripe:** Cores vibrantes em CTAs, bastante espaço em branco
- **Shopify:** Organização clara, hierarquia forte, foco no conteúdo do usuário
- **Notion:** Minimalismo, tipografia como elemento principal de design
- **Apple:** Cantos arredondados, sombras sutis, glass effect onde apropriado

---

## 15.2 Hierarquia Visual (Padrão de Leitura)

### Mobile (Padrão F → Padrão Z simplificado)

```
┌────────────────────┐
│ LOGO          [CTA]│  ← Zona 1: Identidade + Ação principal
├────────────────────┤
│                    │
│   BANNER / HERO    │  ← Zona 2: Maior impacto visual
│                    │
├────────────────────┤
│ Serviço 1          │
│ Serviço 2          │  ← Zona 3: Conteúdo (scroll vertical)
│ Serviço 3          │
│ ...                │
├────────────────────┤
│        [CTA]       │  ← Zona 4: CTA persistente (bottom)
└────────────────────┘
```

### Desktop (Padrão Z)

```
┌──────────────────────────────────────────────────────────────┐
│ LOGO      Nav 1  Nav 2  Nav 3  Nav 4          [ENTRAR] [CTA]│ ← Linha 1
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                    HERO / BANNER                             │ ← Diagonal
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Card 1    │  Card 2    │  Card 3    │  Card 4                │ ← Linha 2
└──────────────────────────────────────────────────────────────┘
```

---

## 15.3 Layout — Painel Admin

```
┌──────────────────────────────────────────────────────────────┐
│ ┌──────────┐ ┌──────────────────────────────────────────────┐│
│ │          │ │  HEADER (56px)                                ││
│ │          │ │  Breadcrumb + Título + Ações                 ││
│ │ SIDEBAR  │ ├──────────────────────────────────────────────┤│
│ │          │ │                                              ││
│ │ 240px    │ │                                              ││
│ │          │ │  CONTEÚDO PRINCIPAL                          ││
│ │ Navegação│ │                                              ││
│ │          │ │  Cards, tabelas, formulários                 ││
│ │          │ │                                              ││
│ │          │ │                                              ││
│ │          │ │                                              ││
│ └──────────┘ └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘

Sidebar: fixa, scroll independente
Header: fixo, com breadcrumb + título da página + ações
Conteúdo: scroll vertical, padding 24px
```

---

## 15.4 Layout — Site Público

### Mobile (Single Column Stack)

```
┌────────────────────┐
│      HEADER        │  ← Logo + Menu hamburger
├────────────────────┤
│      HERO          │  ← Banner full-width + CTA
├────────────────────┤
│    SERVIÇOS        │  ← Cards 1 coluna
├────────────────────┤
│     EQUIPE         │  ← Avatares 2 colunas
├────────────────────┤
│   DEPOIMENTOS      │  ← Carrossel horizontal
├────────────────────┤
│   LOCALIZAÇÃO      │  ← Mapa + endereço
├────────────────────┤
│      FOOTER        │
├────────────────────┤
│ [AGENDAR] ← fixo   │  ← CTA sticky bottom
└────────────────────┘
```

### Desktop (Multi Column)

```
┌──────────────────────────────────────────────────────────────┐
│                     HEADER (nav horizontal)                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                     HERO (full-width)                         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│    SERVIÇOS (2-3 colunas)      │    EQUIPE (4 colunas)       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│    DEPOIMENTOS (3 colunas)     │    LOCALIZAÇÃO (mapa)       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                     FOOTER (4 colunas)                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 15.5 Espaço em Branco

### Regra dos 3 respiros:

1. **Micro (8-16px):** Entre elementos relacionados (label + input, ícone + texto)
2. **Médio (24-32px):** Entre seções de uma página
3. **Macro (48-64px):** Entre blocos principais (hero → serviços)

"Não tenha medo do espaço vazio. Ele guia o olho e dá descanso visual."

---

## 15.6 Cor e Contraste

### Regras de Uso de Cor

- **Primary:** Máximo 10% da tela (CTAs, links, elementos interativos)
- **Neutros:** 80% da tela (backgrounds, textos, bordas)
- **Semânticas:** 10% da tela (success, error, warning — pontuais)

### Contraste Mínimo (WCAG AA)

| Elemento | Ratio Mínimo |
|----------|:-----------:|
| Texto normal | 4.5:1 |
| Texto grande (≥18px bold) | 3:1 |
| Ícones, bordas | 3:1 |
| Componentes interativos | 3:1 |

---

## 15.7 Tipografia na Prática

### Regras

- Máximo 2 font families (Inter para tudo + mono para código)
- Máximo 3 tamanhos visíveis em qualquer tela
- Comprimento de linha: 50-75 caracteres (desktop), 35-45 (mobile)
- Parágrafos: ≤ 3 linhas sempre que possível
- Títulos: sentence case ("Agende seu horário" não "Agende Seu Horário")

### Escala Prática por Contexto

| Contexto | Título | Corpo | Secundário |
|----------|:------:|:-----:|:----------:|
| Hero (site) | 32px | 18px | 14px |
| Seção (site) | 24px | 16px | 14px |
| Dashboard | 20px | 14px | 12px |
| Modal | 18px | 14px | — |
| Toast | — | 14px | — |

---

## 15.8 Imagens e Mídia

### Regras

- **Fotos de profissionais:** Retrato (3:4), fundo neutro, bem iluminado
- **Banner:** 1200×600px, formato horizontal, com overlay de texto
- **Galeria:** Grid masonry, WebP, lazy loading
- **Logo:** SVG preferencialmente, altura máxima 48px no header

### Placeholders

- Foto de profissional não enviada: Avatar com iniciais (fundo primary-light)
- Serviço sem foto: Ícone representativo (✂️, 💈, 🪒)
- Galeria vazia: Ilustração "Adicione fotos dos seus trabalhos"

---

## 15.9 Feedback Visual de Status

| Status | Cor | Ícone | Componente |
|--------|-----|:-----:|-----------|
| Sucesso | Green (#27ae60) | ✅ | Toast verde + check animado |
| Erro | Red (#e74c3c) | ❌ | Toast vermelho + borda no input |
| Alerta | Orange (#f39c12) | ⚠️ | Banner amarelo no topo |
| Info | Blue (#3498db) | ℹ️ | Toast azul |
| Loading | Primary | ◌ | Spinner / Skeleton |
| Vazio | Gray | 📭 | Empty state com CTA |

---

## 15.10 Glass Effect (Painel Admin — Opcional)

Para modais e dropdowns no painel admin:

```
┌──────────────────────────────────────┐
│ backdrop-filter: blur(12px)          │
│ background: rgba(255,255,255,0.8)   │
│ border: 1px solid rgba(0,0,0,0.08) │
│ border-radius: 12px                  │
│ box-shadow: 0 8px 32px rgba(0,0,0,0.12)│
└──────────────────────────────────────┘
```

Uso restrito (excesso cansa):
- Modal de confirmação
- Dropdown de perfil
- Tooltip

---

> **Resumo:** O design visual deve ser invisível. O usuário não deve notar "que fonte bonita" ou "que sombra bem feita" — ele deve simplesmente sentir que tudo está no lugar certo. UI boa é aquela que você não percebe.
