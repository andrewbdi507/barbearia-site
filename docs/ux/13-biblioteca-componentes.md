# 13 — Biblioteca de Componentes

> Catálogo completo de componentes reutilizáveis do Barbershop Design System.

---

## 13.1 Botões

### Variantes

| Variante | Uso | Exemplo Visual |
|----------|-----|---------------|
| **Primary** | Ação principal (CTA) | `[█ AGENDAR AGORA █]` — fundo primary, texto branco |
| **Secondary** | Ação secundária | `[═ Ver mais ═]` — borda primary, fundo transparente |
| **Ghost** | Ação terciária, navegação | `[ Cancelar ]` — sem fundo, sem borda |
| **Danger** | Ação destrutiva | `[█ EXCLUIR █]` — fundo error, texto branco |
| **Success** | Confirmação | `[█ SALVAR █]` — fundo success |
| **Icon** | Apenas ícone | `[🔍]` — 40×40px, circular |

### Tamanhos

| Tamanho | Height | Padding H | Font | Uso |
|---------|:------:|:---------:|------|-----|
| `sm` | 32px | 12px | text-sm | Tabelas, cards compactos |
| `md` | 40px | 16px | text-sm | Padrão |
| `lg` | 48px | 24px | text-base | CTAs principais |
| `xl` | 56px | 32px | text-lg | Hero |

### Estados

```
Default: [█ AGENDAR █]  (cor primary)
Hover:   [█ AGENDAR █]  (primary, 10% mais escuro)
Active:  [█ AGENDAR █]  (primary, 15% mais escuro, escala 0.98)
Focus:   [█ AGENDAR █]  (com outline 2px primary + offset 2px)
Loading: [◌ Processando...]  (spinner 16px + texto, desabilitado)
Disabled:[▒ AGENDAR ▒]  (opacidade 40%, cursor not-allowed)
```

---

## 13.2 Inputs

### Variantes

```
┌────────────────────────────────────┐
│ Label *                            │
│ ┌────────────────────────────────┐ │
│ │ Digite aqui...            📋  │ │  ← input com ícone à direita
│ └────────────────────────────────┘ │
│ ⓘ Texto de ajuda                  │
│ ❌ Mensagem de erro                │
└────────────────────────────────────┘
```

### Estados

```
Default:  borda `--color-border`, fundo branco
Hover:    borda `--color-text-secondary`
Focus:    borda `--color-primary`, box-shadow primary 0 0 0 3px
Error:    borda `--color-error`, ícone ❌, mensagem abaixo
Success:  borda `--color-success`, ícone ✅
Disabled: opacidade 50%, cursor not-allowed
```

### Tipos de Input

| Tipo | Descrição |
|------|-----------|
| **Text** | Campo de texto simples |
| **Textarea** | Múltiplas linhas (observações, bio) |
| **Select** | Dropdown nativo estilizado |
| **Phone** | Com máscara: (99) 99999-9999 |
| **Currency** | Prefixo R$, máscara decimal |
| **Search** | Ícone de lupa à esquerda |
| **Color Picker** | Input type="color" + campo hex |
| **Date Picker** | Calendário popover |
| **Time Select** | Grid de horários (componente customizado) |
| **File Upload** | Drag & drop + preview |

---

## 13.3 Cards

### Card Padrão

```
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │           IMAGEM (opcional)       │ │
│ └──────────────────────────────────┘ │
│                                      │
│  Título do Card                      │
│  Descrição secundária em             │
│  até 2 linhas de texto...            │
│                                      │
│  ┌──────────┐    ┌──────────┐       │
│  │  Ação 1  │    │  Ação 2  │       │
│  └──────────┘    └──────────┘       │
└──────────────────────────────────────┘
```

Recomendado: padding 16px, border-radius 8px, sombra-md

### Variantes de Card

| Variante | Uso |
|----------|-----|
| **Default** | Listagem de serviços, profissionais |
| **Selectable** | Com radio/checkbox para seleção |
| **Horizontal** | Imagem à esquerda, conteúdo à direita |
| **Stat** | Número grande + label (dashboard) |
| **Interactive** | Hover com elevação, cursor pointer |
| **Selected** | Borda primary, fundo primary-light |

---

## 13.4 Modal

```
┌──────────────────────────────────────────────────────────────┐
│                      OVERLAY (semi-transparente)              │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Título do Modal                              [✕ Fechar] ││
│  │  ─────────────────────────────────────────────────────── ││
│  │                                                          ││
│  │  Conteúdo do modal...                                    ││
│  │  Pode conter formulários, confirmações,                  ││
│  │  informações detalhadas.                                 ││
│  │                                                          ││
│  │  ─────────────────────────────────────────────────────── ││
│  │                    [Cancelar]    [Confirmar]              ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

### Comportamento
- Abre com animação fade + scale (200ms)
- Fecha com ESC, clique no overlay, ou botão ✕
- Foco aprisionado dentro do modal (acessibilidade)
- Scroll no conteúdo se maior que viewport
- Mobile: full-screen (bottom sheet em algumas situações)

---

## 13.5 Toast / Notificação

```
┌────────────────────────────────────┐
│ ✅ Sucesso!                        │
│ Agendamento confirmado para        │
│ 20/07 às 14:30.                    │
│                          [✕]      │
│ ─────────────────────────────      │
│ ⏳ 5s (barra de progresso)         │
└────────────────────────────────────┘
```

### Variantes

| Tipo | Ícone | Cor | Uso |
|------|:-----:|-----|-----|
| Success | ✅ | success | Operação concluída |
| Error | ❌ | error | Falha na operação |
| Warning | ⚠️ | warning | Atenção necessária |
| Info | ℹ️ | info | Informação neutra |

### Comportamento
- Posição: bottom-right (desktop) / top-center (mobile)
- Duração: 5 segundos (configurável)
- Swipe para dispensar (mobile)
- Empilha até 3 toasts visíveis
- Barra de progresso animada mostrando tempo restante

---

## 13.6 Tabela

```
┌──────────────────────────────────────────────────────────────┐
│  Título da Tabela                    🔍 Buscar  [Exportar]   │
├──────────────────────────────────────────────────────────────┤
│  ┌────────┬──────────────┬─────────┬────────┬─────────────┐ │
│  │ Nome ▲ │ Serviço      │ Data    │ Status │ Ações       │ │
│  ├────────┼──────────────┼─────────┼────────┼─────────────┤ │
│  │João S. │ Corte        │20/07 09 │ ✅     │ [···]       │ │
│  │Pedro L.│ Barba        │20/07 09 │ 🟡     │ [···]       │ │
│  │Ana C.  │ Corte+Barba  │20/07 10 │ 🔵     │ [···]       │ │
│  └────────┴──────────────┴─────────┴────────┴─────────────┘ │
│                                                              │
│  Mostrando 1-3 de 25    [◀ Anterior] [1] [2] [3] [Próximo ▶]│
└──────────────────────────────────────────────────────────────┘
```

### Comportamento
- Cabeçalho fixo ao scrollar
- Ordenação por coluna (clique no header)
- Linhas zebradas (alternância sutil de cor)
- Hover na linha (highlight)
- Menu de ações (···) com dropdown
- Paginação inferior
- Responsivo: mobile vira cards empilhados

---

## 13.7 Calendário (Date Picker)

```
┌──────────────────────────────────────┐
│         Julho 2026                    │
│     ◀            ▶                   │
│                                       │
│  Dom Seg Ter Qua Qui Sex Sáb         │
│             1   2   3   4            │
│   5   6   7   8   9  10  11          │
│  12  13  14  15  16  17  18          │
│  19 [20] 21  22  23  24  25          │  ← dia selecionado (círculo primary)
│  26  27  28  29  30  31              │
│                                       │
│  Hoje: 20 Jul │ Selecionado: 20 Jul  │
└──────────────────────────────────────┘
```

### Comportamento
- Dias passados: opacidade 30%, não clicáveis
- Hoje: texto bold
- Selecionado: fundo primary, texto branco
- Dias com agendamento: bolinha sutil abaixo da data
- Swipe horizontal para mudar mês (mobile)

---

## 13.8 Grid de Horários (Time Slot Picker)

```
┌──────────────────────────────────────┐
│  MANHÃ ☀️                             │
│  ┌──────┬──────┬──────┬──────┐       │
│  │ 09:00│ 09:30│ 10:00│ 10:30│       │
│  │ Livre│ Livre│ Ocup │ Livre│       │
│  └──────┴──────┴──────┴──────┘       │
│                                       │
│  TARDE 🌤️                             │
│  ┌──────┬──────┬──────┬──────┐       │
│  │ 14:00│ 14:30│ 15:00│ 15:30│       │
│  │ Sel. │ Livre│ Livre│ Livre│       │  ← "Sel." = selecionado (fundo primary)
│  └──────┴──────┴──────┴──────┘       │
└──────────────────────────────────────┘
```

### Estados dos Slots

| Estado | Aparência | Interação |
|--------|-----------|-----------|
| **Livre** | Fundo surface, borda sutil | Clicável → seleciona |
| **Selecionado** | Fundo primary, texto branco | Clicável → deseleciona |
| **Ocupado** | Fundo cinza, texto riscado | Não clicável |
| **Indisponível** | Fundo listrado, opaco | Não clicável |
| **Bloqueado** | Fundo vermelho claro, ícone 🔒 | Não clicável |

---

## 13.9 Avatar / Foto de Perfil

```
┌────┐
│ 📷 │  48×48px (padrão)
│    │  circular, border 2px surface
└────┘

Tamanhos: sm (32px), md (48px), lg (64px), xl (96px)
Fallback: iniciais do nome (fundo primary-light, texto primary)
```

---

## 13.10 Badge / Tag

```
┌──────────┐
│ Ativo 🟢 │  fundo semitransparente da cor, texto da cor
└──────────┘

Variantes: success, warning, error, info, primary, secondary
Formatos: pill (border-radius full), rounded (border-radius md)
```

---

## 13.11 Skeleton (Loading State)

```
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │ ████████████████████████████████ │ │  ← Animação shimmer
│ └──────────────────────────────────┘ │
│ ┌──────────────────┐                 │
│ │ ████████████████ │                 │
│ └──────────────────┘                 │
│ ┌──────────────────────────────┐     │
│ │ ████████████████████████████ │     │
│ └──────────────────────────────┘     │
└──────────────────────────────────────┘
```

Uso: enquanto dados carregam, mostra esqueleto com animação shimmer (onda de brilho). Formato similar ao conteúdo real para evitar layout shift.

---

## 13.12 Empty State

```
┌──────────────────────────────────────┐
│                                      │
│              ┌──────┐                │
│              │  🎨  │                │  ← Ilustração ou ícone grande
│              └──────┘                │
│                                      │
│        Nenhum agendamento            │
│        para este dia ainda           │
│                                      │
│   ┌────────────────────────────┐    │
│   │   + Novo Agendamento       │    │  ← CTA principal
│   └────────────────────────────┘    │
└──────────────────────────────────────┘
```

---

## 13.13 Progress Indicator

```
┌──────────────────────────────────────┐
│  Agendamento                          │
│  ● ─── ● ─── ● ─── ○                 │
│ Prof.  Serv.  Data   Dados           │
│                                       │
│ Passo 3 de 4                          │
└──────────────────────────────────────┘

Cada passo: círculo preenchido (concluído) | atual (primary) | vazio (futuro)
Linhas conectando: cinza (pendente) ou primary (concluído)
```

---

## 13.14 Tabs

```
┌──────────────────────────────────────┐
│  ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │  Hoje   │ │ Semana  │ │  Mês   │ │
│  │ ████████│ │         │ │        │ │  ← Tab ativa com underline primary
│  └─────────┘ └─────────┘ └────────┘ │
│  ──────────────────────────────────── │
│  Conteúdo da tab...                   │
└──────────────────────────────────────┘
```

---

## 13.15 Dropdown / Select

```
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │ Selecionar...              ▾     │ │  ← Trigger
│ └──────────────────────────────────┘ │
│                                       │
│  ┌──────────────────────────────────┐ │
│  │ 🔍 Buscar...                     │ │  ← Search (opcional)
│  │ ──────────────────────────────── │ │
│  │ ██ Opção 1               ✅     │ │  ← Selecionada (highlight)
│  │    Opção 2                       │ │
│  │    Opção 3                       │ │
│  │    Opção 4                       │ │
│  └──────────────────────────────────┘ │
└──────────────────────────────────────┘

Abre com animação scale+fade (150ms)
Fecha com ESC ou clique fora
Navegação por teclado (↑↓ Enter)
```

---

## 13.16 Sidebar (Admin)

```
┌──────────────┐
│  ┌────────┐  │
│  │  LOGO  │  │
│  └────────┘  │
│              │
│  📊 Dashboard│ ← Item ativo: fundo primary-light, borda esquerda primary
│  📅 Agenda   │
│  👥 Clientes │
│  💇 Profiss. │
│  ✂️ Serviços │
│  💰 Financeir│
│  🎫 Promoções│
│  📈 Relatórios│
│  📣 Marketing│
│  ⭐ Avaliaç. │
│  ⚙️ Config.  │  ← Com submenu expansível
│     Tema     │
│     Horários │
│     Permiss. │
│  📋 Logs     │
│  🆘 Suporte  │
│              │
│  ────────── │
│  ⬅ Sair     │
└──────────────┘

Largura: 240px (desktop), overlay/drawer (mobile)
Comportamento: colapsável (ícone apenas) em telas menores
```

---

## 13.17 Bottom Tab Bar (Mobile)

```
┌──────────────────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ 📅  │ │ 💰  │ │ 👤  │ │ ⚙️  │   │
│  │Agenda│ │Ganhos│ │Client│ │Perfil│   │
│  │ ████ │ │     │ │     │ │     │   │  ← Ativo: ícone + label primary
│  └─────┘ └─────┘ └─────┘ └─────┘   │
└──────────────────────────────────────┘

Altura: 56px (seguro para iPhone com home indicator)
Background: surface + border-top
Ícones: 24px, labels: text-xs
```

---

## 13.18 Rating Stars

```
⭐⭐⭐⭐⭐  ← Interativo (hover preenche)
          ← Cada estrela: 32px, cor warning até selecionada

Estados:
- Vazio: outline cinza
- Hover: preenchimento amarelo progressivo
- Selecionado: amarelo sólido
- Readonly: amarelo sólido, não interativo
```

---

## 13.19 QR Code Display

```
┌──────────────────────┐
│ ┌──────────────────┐ │
│ │                  │ │
│ │    QR CODE       │ │
│ │    (200×200px)   │ │
│ │                  │ │
│ └──────────────────┘ │
│                      │
│ Abra o app do banco  │
│ e escaneie o QR Code │
│                      │
│ ┌──────────────────┐ │
│ │PIX Copia e Cola  │ │
│ │ 0002012636...    │ │
│ └──────────────────┘ │
│    [COPIAR CÓDIGO]   │
└──────────────────────┘
```

---

## 13.20 WhatsApp Flutuante

```
┌──────────────────────┐
│                      │
│                      │
│                 ┌───┐│
│                 │ 🟢││  ← Botão flutuante
│                 └───┘│     Posição: bottom-right
│                      │     Tamanho: 56×56px
│                      │     Animação: pulse sutil
└──────────────────────┘
```

---

## 13.21 Loading Spinner

```
◌  Spinner circular (24px padrão)
   Animação: rotate 360° infinito
   Cor: primary
   Tamanhos: sm (16px), md (24px), lg (32px), xl (48px)
```

### Full Page Loading

```
┌──────────────────────────────────────┐
│                                      │
│              ◌ (48px)                │
│         Carregando...                │
│                                      │
└──────────────────────────────────────┘
```

---

## 13.22 Status Indicators

```
🟢 Online / Ativo / Confirmado
🟡 Aguardando / Em andamento
🔵 Agendado / Pendente
🔴 Erro / Cancelado / No-show
⚪ Inativo / Desligado
```

---

> **Resumo:** A biblioteca de componentes cobre todos os elementos necessários para construir todas as telas do sistema. Cada componente tem estados definidos (default, hover, focus, active, disabled, loading, error), variantes, e comportamento responsivo. A consistência entre site público e painel admin é garantida pelos mesmos tokens de design.
