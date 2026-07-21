# 18 — Guia de Microinterações

> Pequenos momentos que transformam "funcional" em "encantador".

---

## 18.1 Filosofia

Microinterações são os **detalhes que fazem a diferença**. Não são enfeites — são feedback, orientação e personalidade.

Cada microinteração responde a 4 perguntas:
1. **Trigger:** O que iniciou? (clique, hover, scroll, sistema)
2. **Rules:** O que acontece? (a lógica)
3. **Feedback:** O que o usuário vê/sente? (visual, tátil, som)
4. **Loops & Modes:** O que acontece depois? (repetição, estado)

---

## 18.2 Catálogo de Microinterações

### 1. Botão — Hover e Click

```
TRIGGER: Hover (desktop) / Touch down (mobile)
FEEDBACK:
  - Cor escurece 10% em 100ms
  - Sombra aumenta sutilmente
  - Cursor: pointer

TRIGGER: Click / Tap
FEEDBACK:
  - Scale: 0.97 em 100ms (pressionado)
  - Scale: 1.0 em 200ms (solto, com bounce sutil)
  - Ripple effect do centro (mobile, opcional)

TRIGGER: Loading state
FEEDBACK:
  - Texto substituído por spinner (200ms fade)
  - Botão desabilitado
  - Largura mantida (evitar layout shift)
```

### 2. Card — Hover e Seleção

```
TRIGGER: Hover (desktop)
FEEDBACK:
  - Elevação: translateY(-2px) + shadow-lg (200ms)
  - Borda destaca levemente
  - Cursor: pointer (se clicável)

TRIGGER: Seleção (click/tap)
FEEDBACK:
  - Borda primary (2px) aparece com animação
  - Background: primary-light (100ms)
  - Checkmark ✅ aparece no canto (se seleção)
```

### 3. Input — Focus e Validação

```
TRIGGER: Focus
FEEDBACK:
  - Borda: border → primary (200ms)
  - Box-shadow: 0 0 0 3px primary com opacidade 20%
  - Label sobe e diminui (se floating label)

TRIGGER: Validação inline (ao digitar)
FEEDBACK:
  - Sucesso: borda verde + ✅ no canto direito (200ms)
  - Erro: borda vermelha + shake horizontal (300ms, 2 oscilações)
  - Mensagem de erro: fade in de cima (200ms)
```

### 4. Checkmark de Confirmação (Tela de Sucesso)

```
TRIGGER: Agendamento confirmado / Pagamento aprovado
ANIMAÇÃO:
  1. Círculo desenha (300ms, stroke-dashoffset)
  2. Checkmark desenha dentro do círculo (200ms delay, 300ms duração)
  3. Partículas sutis (3-5) explodem do centro (opcional)
  4. Cor: success (#27ae60)
  
DURAÇÃO TOTAL: ~800ms
```

### 5. Toast Notification

```
TRIGGER: Sistema (pós-ação)
FEEDBACK:
  1. Toast desliza de baixo (mobile) ou da direita (desktop)
     - Animação: translate + opacity (300ms, ease-out)
  2. Ícone + mensagem visível
  3. Barra de progresso no bottom (5s duração)
  4. Swipe right para dispensar (mobile, com resistência)
  5. Auto-dismiss: slide out + fade (200ms)
  6. Ou: clique no ✕ para fechar imediatamente
```

### 6. Modal — Abrir e Fechar

```
TRIGGER: Abrir
FEEDBACK:
  1. Overlay: fade in (200ms, opacity 0 → 0.5)
  2. Modal: scale(0.95) + opacity(0) → scale(1) + opacity(1)
     - 300ms, ease-out (cubic-bezier 0.34, 1.56, 0.64, 1)
     - Leve bounce no final

TRIGGER: Fechar
FEEDBACK:
  1. Modal: scale(1) → scale(0.95) + opacity(0) (150ms)
  2. Overlay: fade out (150ms)
```

### 7. Skeleton Loading

```
TRIGGER: Página / componente carregando
FEEDBACK:
  1. Skeleton com mesma forma do conteúdo real (evitar CLS)
  2. Animação shimmer (onda de brilho):
     - Gradiente linear se move da esquerda para direita
     - Duração: 1.5s, loop infinito
     - Cores: surface → surface-hover → surface
  3. Quando dados chegam: fade out skeleton (200ms) → fade in conteúdo (200ms)
```

### 8. Pull-to-Refresh

```
TRIGGER: Pull down no topo da lista (mobile)
FEEDBACK:
  1. Indicador de pull: círculo que preenche conforme distância
  2. Ao atingir threshold (> 80px): círculo completo
  3. Soltar: spinner gira (800ms típico)
  4. Dados atualizados: lista desliza para posição (300ms)
```

### 9. Swipe Actions (Lista)

```
TRIGGER: Swipe left no card
FEEDBACK:
  1. Card desliza revelando ações abaixo
  2. Resistência elástica (não desliza infinito)
  3. Snap: ou abre ações ou volta (depende da distância)
  4. Ações: [Check-in ✅] [No-show ❌]
  5. Background das ações colorido (verde/vermelho)
```

### 10. Número Subindo (Dashboard)

```
TRIGGER: Dados do dashboard carregam
FEEDBACK:
  1. Número anima de 0 até valor real
  2. Duração: 800ms, ease-out
  3. Ex: "R$ 450,00" sobe como um odômetro
  4. Só na primeira carga (não em atualizações)
```

### 11. Progress Indicator (Steps)

```
TRIGGER: Avançar/voltar no fluxo de agendamento
FEEDBACK:
  1. Círculo preenche da esquerda para direita
  2. Linha entre círculos: cinza → primary (300ms)
  3. Círculo atual: pulsa sutilmente (scale 1 → 1.1 → 1, 400ms)
  4. Passo concluído: checkmark aparece dentro do círculo
```

### 12. QR Code — Copiado

```
TRIGGER: Clicar "Copiar código PIX"
FEEDBACK:
  1. Texto do botão muda: "Copiar código" → "✅ Copiado!" (200ms)
  2. Ícone de check verde aparece
  3. Após 2s: volta ao texto original
  4. Código pisca brevemente (highlight)
```

### 13. Estrelas de Avaliação

```
TRIGGER: Hover / Tap nas estrelas
FEEDBACK:
  1. Hover: estrelas preenchem progressivamente (da esquerda para direita)
     - Cor: warning (#f39c12)
     - Animação: scale(1.2) na estrela atual (150ms bounce)
  2. Click: estrelas fixam na seleção
  3. Cada estrela: 32px, espaçamento 4px
```

### 14. WhatsApp Flutuante

```
TRIGGER: Scroll / Idle
FEEDBACK:
  1. Botão verde 🟢 no canto inferior direito (56×56px)
  2. Pulse sutil a cada 5 segundos (scale 1 → 1.05 → 1, 1s)
  3. Hover: tooltip "Fale conosco no WhatsApp"
  4. Click: abre WhatsApp (mesma aba ou app)
```

### 15. Toggle / Switch

```
TRIGGER: Click/tap no switch
FEEDBACK:
  1. Background: cinza → primary (200ms)
  2. Thumb (bolinha): desliza da esquerda para direita (200ms, ease)
  3. Ripple no centro (Android-like)
```

---

## 18.3 Regras de Ouro das Microinterações

1. **Duração ≤ 300ms** para UI responses (exceto page transitions)
2. **Nunca bloquear** a interface durante animação
3. **Respeitar `prefers-reduced-motion`** — desabilitar animações decorativas
4. **Consistência** — mesma interação = mesma animação em todo o sistema
5. **Propósito** — toda animação comunica algo (não é só "bonito")
6. **Performance** — usar `transform` e `opacity` (GPU acelerado), nunca `width`/`height`
7. **Easing natural** — cubic-bezier, não linear

---

> **Resumo:** Microinterações são o "tempero" do design. Sem elas, o sistema funciona mas é sem graça. Com elas, o sistema encanta. Mas como tempero: use com moderação. Menos é mais.
