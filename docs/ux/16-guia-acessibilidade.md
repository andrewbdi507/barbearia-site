# 16 — Guia de Acessibilidade (WCAG 2.1 AA)

> O sistema deve ser utilizável por TODOS, independentemente de deficiências visuais, motoras, auditivas ou cognitivas.

---

## 16.1 Princípios WCAG (POUR)

| Princípio | Significado | Como Aplicamos |
|-----------|-------------|---------------|
| **P**erceivable | Perceptível | Texto alternativo, contraste, legendas |
| **O**perable | Operável | Navegação por teclado, tempo suficiente, sem convulsões |
| **U**nderstandable | Compreensível | Linguagem clara, comportamento previsível, ajuda contra erros |
| **R**obust | Robusto | Compatível com leitores de tela, HTML semântico |

---

## 16.2 Contraste de Cor

### Requisitos (AA)

| Elemento | Ratio | Como Verificar |
|----------|:-----:|---------------|
| Texto normal (<18px) | ≥ 4.5:1 | Chrome DevTools / axe |
| Texto grande (≥18px bold ou ≥24px) | ≥ 3:1 | Chrome DevTools / axe |
| Ícones e gráficos informativos | ≥ 3:1 | Inspeção manual |
| Estados de foco | ≥ 3:1 | Inspeção manual |
| Bordas de inputs | ≥ 3:1 | Inspeção manual |

### Combinações de Cor Aprovadas

| Background | Texto | Ratio | Status |
|-----------|-------|:-----:|:------:|
| `#ffffff` (branco) | `#1a1a2e` (primary) | 15.4:1 | ✅ AAA |
| `#fafafa` (bg) | `#666680` (secondary) | 5.2:1 | ✅ AA |
| `#1a1a2e` (primary) | `#ffffff` (branco) | 15.4:1 | ✅ AAA |
| `#e94560` (secondary) | `#ffffff` (branco) | 4.6:1 | ✅ AA |
| `#27ae60` (success) | `#ffffff` (branco) | 4.4:1 | ⚠️ AA (borda) |

---

## 16.3 Navegação por Teclado

### Ordem de Tab

```
1. Skip to main content (link invisível, visível no focus)
2. Header / Logo (link para home)
3. Navegação principal
4. Conteúdo da página
5. Sidebar (admin)
6. Footer
```

### Focus Indicators

- **Outline:** 2px solid `--color-primary`, offset 2px
- **Visível:** em TODOS os elementos interativos
- **Nunca removido:** `outline: none` só com alternativa visível

### Atalhos de Teclado (Admin)

| Atalho | Ação |
|--------|------|
| `Ctrl+K` / `Cmd+K` | Busca global |
| `Esc` | Fechar modal / dropdown |
| `Tab` | Próximo elemento |
| `Shift+Tab` | Elemento anterior |
| `Enter` / `Space` | Ativar botão/link |
| `↑↓` | Navegar lista/dropdown |
| `N` | Novo agendamento |
| `D` | Dashboard |
| `C` | Clientes |

---

## 16.4 Leitores de Tela (Screen Readers)

### Labels e ARIA

| Elemento | Implementação |
|----------|--------------|
| **Imagens** | `alt` descritivo: "Foto de Marcos, barbeiro especialista em degradê" |
| **Ícones decorativos** | `aria-hidden="true"` |
| **Ícones funcionais** | `aria-label="Agendar horário"` |
| **Formulários** | `<label>` associado ao `<input>` via `for`/`id` |
| **Erros** | `aria-describedby` ligando input à mensagem de erro |
| **Modais** | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| **Tabelas** | `<th scope="col">` ou `<th scope="row">` |
| **Navegação** | `<nav aria-label="Navegação principal">` |
| **Progresso** | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| **Status** | `role="status"` ou `aria-live="polite"` para atualizações dinâmicas |

### Live Regions

```html
<!-- Toast notifications -->
<div role="status" aria-live="polite" aria-atomic="true">
  Agendamento confirmado para 20/07 às 14:30.
</div>

<!-- Loading state -->
<div role="alert" aria-live="assertive" aria-busy="true">
  Processando pagamento...
</div>
```

---

## 16.5 Formulários Acessíveis

### Estrutura

```
┌──────────────────────────────────────┐
│ <label for="name">Nome completo *</label>│
│ <input id="name"                     │
│        type="text"                   │
│        aria-required="true"          │
│        aria-describedby="name-help   │
│                         name-error"> │
│                                      │
│ <span id="name-help">                │
│   ⓘ Como você gostaria de ser       │
│      chamado                         │
│ </span>                              │
│                                      │
│ <span id="name-error" role="alert">  │
│   ❌ Nome é obrigatório              │
│ </span>                              │
└──────────────────────────────────────┘
```

### Boas Práticas

- Campos obrigatórios: asterisco + `aria-required="true"` + texto "obrigatório"
- Erros: próximos ao campo, com `role="alert"`
- Autocomplete: atributo `autocomplete` adequado (name, tel, email)
- Máscaras: não quebram navegação por teclado

---

## 16.6 Toque e Interação (Mobile)

### Áreas de Toque

- **Mínimo:** 44×44px (WCAG AAA recomenda)
- **Ideal:** 48×48px (Google Material)
- **Espaçamento entre alvos:** ≥ 8px

### Gestos

- **Swipe:** Sempre com alternativa (botão também funciona)
- **Pull-to-refresh:** Alternativa: botão "Atualizar"
- **Long press:** Não depender de long press para ações essenciais

---

## 16.7 Conteúdo e Legibilidade

### Linguagem

- Nível de leitura: 6ª a 8ª série (ensino fundamental)
- Evitar jargão técnico: "Agendar" não "Criar booking"
- Frases curtas: ≤ 20 palavras
- Voz ativa: "Você agendou" não "O agendamento foi realizado"

### Tipografia para Legibilidade

```
✓ Bom: 16px, line-height 1.6, max-width 65ch
✗ Ruim: 12px, line-height 1.2, texto justificado
```

---

## 16.8 Redução de Movimento

Respeitar `prefers-reduced-motion: reduce`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- Animações decorativas são desabilitadas
- Animações funcionais (progresso, loading) permanecem mas mais sutis
- Auto-play de carrossel é pausado

---

## 16.9 Checklist de Acessibilidade (Por Tela)

- [ ] Todo `<img>` tem `alt` apropriado
- [ ] Todo `<input>` tem `<label>` associado
- [ ] Contraste de texto ≥ 4.5:1 (AA)
- [ ] Navegação por teclado funciona (Tab, Enter, Esc)
- [ ] Focus indicator visível em todos elementos
- [ ] Modal aprisiona foco
- [ ] Toast é anunciado por screen reader
- [ ] Tabelas têm headers (`<th>`)
- [ ] Página tem `<h1>` único e hierarquia de headings correta
- [ ] `lang="pt-BR"` no `<html>`
- [ ] Skip link presente
- [ ] Formulários têm validação acessível
- [ ] Erros são anunciados (`role="alert"`)

---

> **Resumo:** Acessibilidade não é um "extra" — é parte fundamental do design. 15% da população mundial tem alguma deficiência. Um sistema que exclui 15% dos usuários é um sistema incompleto. Seguimos WCAG 2.1 AA como baseline e buscamos AAA onde possível.
