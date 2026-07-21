# 🌐 Site Público White-Label — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.site`

---

## 1. Visão Geral

Cada tenant tem automaticamente um site público completo. Zero deploy. Toda personalização é carregada do banco.

### Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                    SITE RESOLVER                          │
│                                                           │
│  studio27.barbeariaos.com.br                              │
│         │                                                 │
│         ▼                                                 │
│  ┌──────────────┐                                        │
│  │ Tenant ID    │ → t_abc123                             │
│  │ Branding     │ → cores, fontes, logos                  │
│  │ CSS Vars     │ → --color-primary, etc.                 │
│  │ SEO Metadata │ → title, OG, JSON-LD                    │
│  │ Services     │ → catálogo de serviços                  │
│  │ Staff        │ → equipe com fotos                      │
│  │ Reviews      │ → avaliações moderadas                  │
│  │ Pages        │ → Sobre, Privacidade, Termos            │
│  │ Sitemap      │ → XML automático                        │
│  └──────────────┘                                        │
│         │                                                 │
│         ▼                                                 │
│  GET /site?subdomain=studio27 → JSON completo            │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Como o Sistema Carrega Identidade Visual

```
1. Cliente acessa: studio27.barbeariaos.com.br
2. Frontend chama: GET /site?subdomain=studio27
3. Backend resolve tenant, busca branding
4. SiteService.generate_css_variables() converte branding → CSS vars
5. Frontend injeta no :root
6. Página renderiza COM A CARA DA BARBEARIA
```

**CSS Variables geradas automaticamente:**
```css
:root {
  --color-primary: #1a1a2e;
  --color-secondary: #e94560;
  --color-background: #f5f5f5;
  --color-surface: #ffffff;
  --color-text: #333333;
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
  --border-radius: 8px;
  --logo-url: url('https://cdn.example.com/t_abc123/logo.png');
  --banner-url: url('https://cdn.example.com/t_abc123/banner.jpg');
}
```

O tenant altera a cor no painel → branding é atualizado → CSS vars mudam → site reflete instantaneamente.

---

## 3. SEO Automático

| Elemento | Fonte |
|----------|-------|
| `<title>` | `seo.meta_title` ou `tenant.name` |
| `<meta description>` | `seo.meta_description` ou auto-gerado |
| Open Graph | `og:title`, `og:image` (logo/banner), `og:type=website` |
| Twitter Cards | `twitter:card=summary_large_image` |
| JSON-LD | Schema.org `LocalBusiness` gerado do tenant |
| Sitemap | `GET /site/sitemap.xml?tenant_id=...` |
| Google Analytics | `seo.google_analytics_id` |
| Facebook Pixel | `seo.facebook_pixel_id` |

---

## 4. Performance

| Técnica | Descrição |
|---------|-----------|
| **Aggregated API** | 1 chamada = todos os dados. Sem N+1 |
| **Cache Redis** | Branding, serviços, equipe com TTL |
| **CSS Variables** | Zero recompilação. Tema muda instantaneamente |
| **CDN Ready** | Assets estáticos via CDN com `/{tenant_id}/` prefix |
| **Lazy loading** | Imagens com `loading="lazy"` |
| **Sitemap** | XML leve, gerado em <10ms |

---

## 5. Escalabilidade

| Estratégia | Descrição |
|------------|-----------|
| **Cache CDN** | Site público cacheado por 5 min (invalida ao editar) |
| **Redis** | Branding, SEO, site content com TTL |
| **Single API call** | Sem waterfall de requisições |
| **Static generation** (futuro) | Next.js ISR com revalidate a cada 5 min |
