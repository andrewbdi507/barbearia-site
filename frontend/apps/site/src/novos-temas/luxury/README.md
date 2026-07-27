# 👑 Luxury Theme — AgendaOS

Tema **Luxury** para o SaaS AgendaOS. Elegância premium com paleta preto e dourado, tipografia serifada refinada e animações suaves.

---

## 🎨 Identidade Visual

| Token | Valor |
|-------|-------|
| **Mood** | Elegante, sofisticado, exclusivo |
| **Background** | `#080808` |
| **Primary** | `#C9A84C` (dourado) |
| **Heading Font** | Playfair Display / Cormorant Garamond |
| **Body Font** | Lora / Cormorant Garamond |
| **Border Radius** | 2-8px (sutil) |
| **Animations** | Lentas, deliberadas (0.7-1.5s) |

---

## 🧩 Estrutura

```
luxury/
├── index.tsx
├── components/ (Hero, About, Services, Professionals, Gallery, Testimonials, FAQ, BookingCTA, Contact, Footer)
├── constants/tokens.ts
├── theme.json
└── README.md
```

## 🚀 Integração

```tsx
import { LuxuryTheme } from "./themes/luxury";
// switch(tenant.theme) { case "luxury": return <LuxuryTheme tenant={data} />; }
```

## 📋 Dependências

`react` ^18/19, `framer-motion` ^11, `lucide-react` ^0.400
