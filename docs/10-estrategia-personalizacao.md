# 10 — Estratégia de Personalização (White-Label)

---

## 10.1 Filosofia

> "O cliente NUNCA deve sentir que está usando um sistema. Ele deve sentir que entrou no site oficial da barbearia."

Para isso, cada tenant deve ter controle total sobre a aparência e conteúdo do seu site público, **sem nenhuma dependência de desenvolvedor**.

---

## 10.2 O que é Personalizável

### Identidade Visual

| Elemento | Como Personaliza | Preview | MVP |
|----------|-----------------|---------|:---:|
| Logo | Upload de imagem (PNG/SVG recomendado) | Header do site | ✅ |
| Favicon | Upload de ícone | Aba do navegador | ❌ |
| Banner Principal | Upload de imagem full-width | Hero section | ✅ |
| Cor Primária | Color picker | Botões, links, destaque | ✅ |
| Cor Secundária | Color picker | Fundos, cards | ✅ |
| Cor de Texto | Color picker | Textos | ❌ |
| Fonte (Títulos) | Google Fonts dropdown | Headings | ❌ |
| Fonte (Corpo) | Google Fonts dropdown | Parágrafos | ❌ |

### Conteúdo

| Elemento | Como Personaliza | Preview | MVP |
|----------|-----------------|---------|:---:|
| Nome da Empresa | Campo de texto | Header, SEO | ✅ |
| Slogan | Campo de texto | Hero section | ❌ |
| Texto "Sobre" | Editor rich text | Página Sobre | ❌ |
| Serviços | CRUD completo | Página Serviços | ✅ |
| Equipe | CRUD com foto | Página Equipe | ✅ |
| Endereço | Campo de texto + Google Maps | Footer, página Contato | ✅ |
| Telefone/WhatsApp | Campo de texto | Header, footer, botão flutuante | ✅ |
| Redes Sociais | Links (Instagram, Facebook, TikTok, YouTube) | Ícones no footer | ❌ |
| Galeria de Fotos | Upload múltiplo com grid | Página Galeria | ❌ |
| FAQ | CRUD de perguntas | Página FAQ | ❌ |
| Política de Privacidade | Editor rich text | Link no footer | ❌ |
| Termos de Uso | Editor rich text | Link no footer | ❌ |

### SEO

| Elemento | Como Personaliza | MVP |
|----------|-----------------|:---:|
| Meta Título | Campo de texto | ❌ |
| Meta Descrição | Campo de texto | ❌ |
| Google Analytics ID | Campo de texto | ❌ |
| Facebook Pixel ID | Campo de texto | ❌ |
| Sitemap | Automático | ❌ |
| robots.txt | Automático | ❌ |

### Agendamento

| Elemento | Como Personaliza | MVP |
|----------|-----------------|:---:|
| Horário de Funcionamento | Grid dia × hora | ✅ |
| Horário por Profissional | Por profissional | ✅ |
| Intervalo entre Agendamentos | Campo de minutos | ❌ |
| Antecedência Mínima | Campo de horas | ❌ |
| Limite de Agendamentos Futuros | Campo numérico | ❌ |

---

## 10.3 Arquitetura de Temas

### Sistema de Design Tokens

Cada tenant tem um conjunto de **design tokens** armazenados como JSONB no banco:

```json
{
  "theme": {
    "colors": {
      "primary": "#1a1a2e",
      "primaryHover": "#16213e",
      "secondary": "#e94560",
      "background": "#f5f5f5",
      "surface": "#ffffff",
      "text": "#333333",
      "textLight": "#666666",
      "success": "#27ae60",
      "error": "#e74c3c",
      "warning": "#f39c12"
    },
    "typography": {
      "headingFont": "Inter",
      "bodyFont": "Inter",
      "baseSize": "16px",
      "scale": "1.25"
    },
    "spacing": {
      "unit": "8px"
    },
    "borderRadius": "8px",
    "shadows": {
      "card": "0 2px 8px rgba(0,0,0,0.1)",
      "button": "0 4px 12px rgba(233,69,96,0.3)"
    }
  },
  "branding": {
    "logo_url": "t_abc123/logo.png",
    "favicon_url": "t_abc123/favicon.ico",
    "banner_url": "t_abc123/banner.jpg",
    "company_name": "Studio 27 Barbearia",
    "slogan": "Tradição e estilo se encontram aqui"
  }
}
```

### Resolução de Tema

```
1. Request chega: studio27.barbersaas.com.br
2. Tenant resolvido do subdomínio: t_abc123
3. Design tokens carregados (cache Redis, TTL 5 min)
4. Next.js aplica tokens via CSS Custom Properties:

   :root {
     --color-primary: #1a1a2e;
     --color-secondary: #e94560;
     --font-heading: 'Inter', sans-serif;
     ...
   }

5. Página renderizada com a identidade do tenant
6. Cache na CDN (5 min ou até próxima atualização)
```

---

## 10.4 Preview em Tempo Real (V1+)

```
┌─────────────────────────────────────────┐
│          PAINEL DE PERSONALIZAÇÃO        │
├─────────────────────────────────────────┤
│                                         │
│  ┌─ Configurações ───┐ ┌─ Preview ───┐ │
│  │                    │ │              │ │
│  │ Logo: [upload]     │ │  ┌────────┐  │ │
│  │                    │ │  │  LOGO   │  │ │
│  │ Cor Primária:      │ │  │ Banner  │  │ │
│  │ [#1a1a2e] ████    │ │  └────────┘  │ │
│  │                    │ │              │ │
│  │ Cor Secundária:    │ │  Serviços    │ │
│  │ [#e94560] ████    │ │  [cards]     │ │
│  │                    │ │              │ │
│  │ Fonte: [Inter ▾]   │ │  Equipe      │ │
│  │                    │ │  [fotos]     │ │
│  └────────────────────┘ └──────────────┘ │
│                                         │
│          [Salvar]  [Descartar]           │
└─────────────────────────────────────────┘
```

Preview usa **iframe** ou renderização lado a lado. Mudanças são aplicadas em tempo real via state management, sem necessidade de salvar para ver.

---

## 10.5 Templates de Layout (V2+)

No futuro, oferecer **2–3 templates de layout** que reorganizam as seções:

| Template | Descrição |
|----------|-----------|
| **Classic** | Hero → Serviços → Equipe → Localização |
| **Modern** | Hero full-screen → Serviços em cards → Equipe carrossel |
| **Minimal** | Hero compacto → Grade de horários prioritária → Serviços |

Cada template usa os **mesmos design tokens**, apenas reorganiza o layout. Isso mantém a complexidade baixa.

---

## 10.6 CSS Customizado (V3+ — Enterprise)

Para tenants Enterprise, permitir **CSS customizado**:

- Campo de código com syntax highlighting
- Preview em tempo real
- Sandboxed (não afeta outros tenants)
- Review de segurança para evitar injeção de scripts maliciosos

---

## 10.7 Armazenamento de Assets

### Estrutura no S3/R2

```
s3://barbersaas-media/{tenant_id}/
├── branding/
│   ├── logo.png          (original)
│   ├── logo_200w.webp    (thumbnail)
│   ├── banner.jpg        (original)
│   └── banner_1200w.webp (optimized)
├── gallery/
│   ├── img_001.webp
│   ├── img_001_thumb.webp
│   └── ...
└── professionals/
    ├── prof_001.webp
    └── ...
```

### Processamento de Imagens

1. Upload → S3 (arquivo original)
2. Evento → Fila → Worker de processamento
3. Worker gera versões WebP/AVIF em múltiplos tamanhos
4. CDN serve tamanho apropriado via `srcset` / transformação on-the-fly

---

## 10.8 Personalização por Plano

Nem todas as features de personalização estão disponíveis em todos os planos:

| Feature | Starter | Pro | Business | Enterprise |
|---------|:-------:|:---:|:--------:|:----------:|
| Logo | ✅ | ✅ | ✅ | ✅ |
| Cores | ❌ | ✅ | ✅ | ✅ |
| Fontes | ❌ | ❌ | ✅ | ✅ |
| Galeria | ❌ | ✅ | ✅ | ✅ |
| Templates | ❌ | ❌ | ✅ | ✅ |
| Domínio próprio | ❌ | ❌ | ✅ | ✅ |
| CSS customizado | ❌ | ❌ | ❌ | ✅ |
| SEO avançado | ❌ | ❌ | ✅ | ✅ |

---

> **Princípio:** A personalização é o coração do produto. Um tenant deve conseguir transformar completamente a aparência do seu site em minutos, sem tocar em uma linha de código. A plataforma fornece a infraestrutura; o dono fornece a identidade.
