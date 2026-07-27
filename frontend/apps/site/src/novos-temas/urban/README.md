# 🏙️ Urban Theme — AgendaOS

Tema **Urban** para o SaaS AgendaOS. Visual ousado, streetwear, cinematográfico com alto contraste e neon vermelho.

---

## 📸 Preview

![Urban Theme Preview](./preview.png)

---

## 🎨 Identidade Visual

| Token | Valor |
|-------|-------|
| **Mood** | Ousado, energético, cinematográfico |
| **Background** | `#0A0A0A` (preto profundo) |
| **Primary** | `#E63946` (vermelho neon) |
| **Surface** | `#141414` |
| **Text** | `#F1F1F1` |
| **Heading Font** | Bebas Neue / Anton |
| **Body Font** | Inter / DM Sans |
| **Border Radius** | 0px (cantos retos, estilo brutalista) |
| **Shadows** | Sombras sólidas com offset (efeito brutalism) |

---

## 🧩 Estrutura

```
urban/
├── index.tsx                 # Componente principal <UrbanTheme />
├── components/
│   ├── index.ts              # Barrel export
│   ├── Hero.tsx              # Hero fullscreen com parallax e neon
│   ├── About.tsx             # Sobre com layout split
│   ├── Services.tsx          # Grid de cards de serviços
│   ├── Professionals.tsx     # Grid de cards da equipe
│   ├── Gallery.tsx           # Galeria masonry + lightbox
│   ├── Testimonials.tsx      # Cards de depoimentos
│   ├── FAQ.tsx               # Accordion de perguntas
│   ├── BookingCTA.tsx        # CTA de agendamento
│   ├── Contact.tsx           # Contato com mapa
│   └── Footer.tsx            # Footer com links
├── constants/
│   └── tokens.ts             # Design tokens do tema
├── theme.json                # Metadados do tema
├── preview.png               # Imagem de preview
└── README.md                 # Esta documentação
```

---

## 🚀 Como Integrar

1. Copie a pasta `urban/` para `frontend/apps/site/src/themes/urban/`
2. Importe o tema:

```tsx
import { UrbanTheme } from "./themes/urban";
```

3. Use no switch de temas:

```tsx
switch (tenant.theme) {
  case "urban":
    return <UrbanTheme tenant={tenantData} />;
  // ...
}
```

---

## 📋 Dependências

- `react` ^18.0 || ^19.0
- `framer-motion` ^11.0
- `lucide-react` ^0.400

---

## 🎬 Animações

- Parallax no background do Hero
- Scroll-triggered reveals (fadeUp, slideIn)
- Hover effects (lift, scale, glow)
- Accordion com height animation
- Orbs flutuantes com blur
- Stagger children nos grids
- Lightbox com transição suave

---

## ♿ Acessibilidade

- HTML semântico (`<section>`, `<article>`, `<nav>`, `<footer>`)
- `aria-label` em botões e links
- `aria-expanded` no accordion
- Contraste AA+ garantido
- `alt` em todas as imagens
- Navegação por teclado (focus-visible)
- `prefers-reduced-motion` respeitado

---

## 📐 Responsividade

Breakpoints:
- **320px** — Mobile pequeno
- **375px** — Mobile médio
- **768px** — Tablet
- **1024px** — Desktop
- **1280px** — Desktop largo
- **1536px** — Ultrawide

Layout 100% responsivo, mobile-first, sem quebra de layout.

---

## 🎯 Performance

- `loading="lazy"` em imagens abaixo da dobra
- `fetchPriority="high"` na hero image
- Animações com `whileInView` (só anima quando visível)
- `viewport={{ once: true }}` para evitar re-animações
- `requestAnimationFrame` nos listeners de scroll
- Sem dependências externas pesadas
