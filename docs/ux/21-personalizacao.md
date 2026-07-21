# 21 — Personalização (White-Label)

> O painel de personalização deve ser tão simples quanto trocar a foto de perfil do WhatsApp.

---

## 21.1 Filosofia

Inspirado no **Shopify Theme Editor**: preview em tempo real, controles intuitivos, zero necessidade de conhecimento técnico.

O dono deve conseguir transformar completamente a aparência do site sem:
- ✗ Tocar em código
- ✗ Entender de CSS
- ✗ Contratar um designer
- ✗ Falar com o desenvolvedor

---

## 21.2 Tela de Personalização (Inspiração Shopify)

```
┌──────────────────────────────────────────────────────────────┐
│  🎨 Personalizar Site                    [Ver site] [Salvar] │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐  ┌──────────────────────────────────────────┐│
│  │ ⚙️ CONFIG  │  │                                          ││
│  │            │  │         PREVIEW DO SITE 📱               ││
│  │ ▸ Logo     │  │  ┌────────────────────────────────────┐ ││
│  │ ▸ Cores    │  │  │         [LOGO]                     │ ││
│  │ ▸ Banner   │  │  │   Studio 27 Barbearia              │ ││
│  │ ▸ Fontes   │  │  │                                    │ ││
│  │ ▸ Layout   │  │  │  ┌──────────────────────────────┐  │ ││
│  │ ▸ Seções   │  │  │  │        BANNER               │  │ ││
│  │            │  │  │  │   "Seu estilo, nossa arte"   │  │ ││
│  │            │  │  │  │      [AGENDAR AGORA]         │  │ ││
│  │            │  │  │  └──────────────────────────────┘  │ ││
│  │            │  │  │                                    │ ││
│  │            │  │  │  Serviços                          │ ││
│  │            │  │  │  ┌──────┐ ┌──────┐ ┌──────┐      │ ││
│  │            │  │  │  │Corte │ │Barba │ │Combo │      │ ││
│  │            │  │  │  │R$45  │ │R$30  │ │R$65  │      │ ││
│  │            │  │  │  └──────┘ └──────┘ └──────┘      │ ││
│  │            │  │  └────────────────────────────────────┘ ││
│  │            │  │                                          ││
│  │            │  │  ┌──────┐ ┌──────┐                      ││
│  │            │  │  │  📱  │ │  🖥️  │ (toggle mobile/desk) ││
│  │            │  │  └──────┘ └──────┘                      ││
│  └────────────┘  └──────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

### Expansão da seção "Cores"

```
┌────────────┐
│ ⚙️ CONFIG  │
│            │
│ ▾ Cores    │
│            │
│  Cor        │
│  Principal  │
│  ┌────────┐ │
│  │████████│ │ ← Color picker + input hex
│  │#1a1a2e │ │
│  └────────┘ │
│             │
│  Cor         │
│  Secundária  │
│  ┌────────┐ │
│  │████████│ │
│  │#e94560 │ │
│  └────────┘ │
│             │
│  Fundo       │
│  ┌────────┐ │
│  │████████│ │
│  │#fafafa │ │
│  └────────┘ │
│             │
│  [↺ Restaurar padrão]│
└────────────┘
```

### Funcionamento do Preview em Tempo Real

1. Dono clica no color picker
2. Escolhe uma cor (ou digita hex)
3. Preview atualiza **instantaneamente** (sem salvar, sem refresh)
4. Todos os elementos que usam aquela cor mudam: botões, links, bordas, ícones
5. Dono vê exatamente como vai ficar

---

## 21.3 Seções do Editor de Personalização

### 1. Logo & Identidade

| Campo | Tipo | Preview |
|-------|------|---------|
| Logo | Upload de imagem (PNG/SVG) | Header do site |
| Logo (rodapé) | Upload ou mesmo da header | Footer |
| Favicon | Upload (32×32px) | Aba do navegador |
| Nome da empresa | Campo de texto | Header, SEO, footer |
| Slogan | Campo de texto | Abaixo do logo |

### 2. Cores

| Campo | Tipo | Preview |
|-------|------|---------|
| Cor primária | Color picker | Botões, links, destaque |
| Cor secundária | Color picker | CTAs, promoções |
| Cor de fundo | Color picker | Background da página |
| Cor de texto | Color picker | Textos |
| Cor de texto claro | Color picker | Textos secundários |

### 3. Banner / Hero

| Campo | Tipo | Preview |
|-------|------|---------|
| Imagem do banner | Upload | Hero section |
| Título do banner | Campo de texto | Sobre a imagem |
| Subtítulo | Campo de texto | Abaixo do título |
| Texto do botão | Campo de texto | CTA: "Agendar Agora" |

### 4. Tipografia

| Campo | Tipo | Preview |
|-------|------|---------|
| Fonte de títulos | Dropdown (Google Fonts) | H1, H2, H3 |
| Fonte de corpo | Dropdown (Google Fonts) | Parágrafos, labels |
| Tamanho base | Slider (14-20px) | Todo texto |

### 5. Seções (Mostrar/Ocultar/Reordenar)

```
┌────────────┐
│ ⚙️ Seções  │
│            │
│ ☰ Banner   │ ← Drag para reordenar
│ ☰ Serviços │
│ ☰ Equipe   │
│ ☰ Galeria  │
│ ☰ Depoimentos│
│ ☰ Mapa     │
│ ☰ Sobre    │
│ ☰ FAQ      │
│            │
│ [+ Adicionar seção]│
└────────────┘
```

---

## 21.4 Componente: Color Picker

```
┌──────────────────────────────┐
│ Cor Primária                 │
│                              │
│ ┌──────────────────────────┐ │
│ │ ████████████████████████ │ │ ← Barra de gradiente
│ │ ↑                        │ │ ← Slider circular
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ ████████████████████████ │ │ ← Barra de opacidade/saturação
│ └──────────────────────────┘ │
│                              │
│ ┌────────────┐ ┌───────────┐ │
│ │ ████████████│ │ #1A1A2E   │ │ ← Preview + valor hex
│ └────────────┘ └───────────┘ │
│                              │
│ Paleta de sugestões:         │
│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐   │
│ │██│ │██│ │██│ │██│ │██│   │ ← 5 cores sugeridas
│ └──┘ └──┘ └──┘ └──┘ └──┘   │
└──────────────────────────────┘
```

---

## 21.5 Componente: Upload de Imagem

```
┌──────────────────────────────────────┐
│                                      │
│        ┌────────────────────┐        │
│        │                    │        │
│        │   📷  Upload       │        │
│        │                    │        │
│        │  Arraste a imagem  │        │
│        │  ou clique aqui    │        │
│        │                    │        │
│        │  PNG, JPG ou SVG   │        │
│        │  Até 5 MB          │        │
│        └────────────────────┘        │
│                                      │
│  Após upload:                        │
│  ┌────────────────────┐             │
│  │    [PREVIEW]       │             │
│  │                    │             │
│  │  ✅ Logo enviada!  │             │
│  │  [✏ Alterar]      │             │
│  └────────────────────┘             │
│                                      │
│  💡 Recomendado: PNG com fundo       │
│     transparente, 200×80px           │
└──────────────────────────────────────┘
```

---

## 21.6 Editor de Layout (V2+)

### Templates Disponíveis

```
┌──────────────────────────────────────────────────────────────┐
│  Escolha um layout                                           │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │                  │
│  │ │      │ │  │ │██████│ │  │ │      │ │                  │
│  │ │HERO  │ │  │ │      │ │  │ │HERO  │ │                  │
│  │ └──────┘ │  │ │ HERO │ │  │ │compact│ │                  │
│  │ ┌──┐┌──┐ │  │ └──────┘ │  │ └──────┘ │                  │
│  │ │S ││E │ │  │ ┌──┐┌──┐ │  │ ┌──────┐ │                  │
│  │ └──┘└──┘ │  │ │S ││E │ │  │ │Grade │ │                  │
│  │          │  │ │  ││  │ │  │ │Horár.│ │                  │
│  │ Clássico │  │ └──┘└──┘ │  │ └──────┘ │                  │
│  │          │  │  Moderno  │  │  Agenda  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

Cada template mantém os tokens de design (cores, fontes, logo) — só reorganiza o layout.

---

## 21.7 Mobile: Painel de Personalização

```
┌────────────────────┐
│ 🎨 Personalizar     │
│ [Preview] [Config] │
├────────────────────┤
│                    │
│  PREVIEW           │
│  ┌──────────────┐  │
│  │   [LOGO]     │  │
│  │ Studio 27    │  │
│  ├──────────────┤  │
│  │   BANNER     │  │
│  └──────────────┘  │
│                    │
│  Abas inferiores:  │
│  ┌────┬────┬────┐  │
│  │ 🎨 │ 🖼️ │ ✂️ │  │
│  │Cor │Img │Seç │  │
│  └────┴────┴────┘  │
└────────────────────┘
```

Mobile: ao selecionar uma opção de edição, o preview minimiza e o editor ocupa a tela. Ao confirmar, preview volta a expandir.

---

> **Resumo:** A personalização é o que diferencia "um sistema de agenda" de "o site da minha barbearia". O editor visual com preview em tempo real permite que qualquer pessoa — sem conhecimento técnico — transforme a aparência do site em minutos. Como trocar a capinha do celular: fácil, rápido e com resultado visível instantaneamente.
