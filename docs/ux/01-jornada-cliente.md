# 01 — Jornada Completa do Cliente

> **Persona:** João, 28 anos · **Dispositivo:** Smartphone (90%) / Desktop (10%)  
> **Objetivo:** Agendar um corte em < 2 minutos  
> **Princípio:** Mobile-first, zero fricção, sem cadastro obrigatório

---

## 1.1 Mapa da Jornada (End-to-End)

```
                    TEMPO TOTAL: ~1 min 50 seg
                    
FASE 1          FASE 2         FASE 3        FASE 4         FASE 5
DESCOBERTA      EXPLORAÇÃO     AGENDAMENTO   PAGAMENTO      PÓS
(15s)           (25s)          (40s)         (20s)          (10s)
─────           ─────          ────          ────           ────
Instagram       Site da        Escolhe       PIX /         Confirmação
→ Link bio      barbearia      barbeiro      Cartão        WhatsApp
                → Home         → Serviço     → QR Code     → Google Cal
                → Serviços     → Horário     → Pago        → Lembrete
                → Equipe       → Dados       → Confirmado  → Avaliação
                                                    ↓
                                            FASE 6 (30 dias depois)
                                            RETORNO AUTOMÁTICO
                                            ─────────────────
                                            WhatsApp: "Faz 1 mês!"
                                            → Reagendar em 1 clique
```

---

## 1.2 Detalhamento Tela por Tela

### TELA 1 — Descoberta (Instagram)

```
┌────────────────────────────────────┐
│  📱 INSTAGRAM (app nativo)         │
│                                    │
│  [Post no feed / Story / Anúncio]  │
│                                    │
│  Foto de um corte incrível         │
│  ┌──────────────────────────┐     │
│  │     📸 Corte Moderno      │     │
│  │     @barbeariastudio27    │     │
│  │                          │     │
│  │  Curtido por 234 pessoas  │     │
│  └──────────────────────────┘     │
│                                    │
│  Clique no perfil → Link na bio    │
│  ┌──────────────────────────┐     │
│  │  studio27barber.com.br   │     │
│  │  [Agende seu horário]    │ ←─── CTA principal     │
│  └──────────────────────────┘     │
│                                    │
│  CLIQUE → Redireciona ao site     │
└────────────────────────────────────┘

Emoção: 😊 Curiosidade → "Que corte bonito, quero também"
Problema possível: Link quebrado → página 404 customizada com WhatsApp
```

---

### TELA 2 — Home (Primeira Impressão)

```
┌────────────────────────────────────┐
│  📱 SITE DA BARBEARIA (mobile)     │
│  8:41                             │
│  ┌──────────────────────────────┐ │
│  │         LOGO                 │ │
│  │    Studio 27 Barbearia       │ │
│  │    Tradição desde 2018       │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │                              │ │
│  │     BANNER PRINCIPAL         │ │
│  │   Foto ambiente barbearia    │ │
│  │   "Seu estilo, nossa arte"   │ │
│  │                              │ │
│  │   [AGENDAR AGORA] ← CTA      │ │
│  │                              │ │
│  └──────────────────────────────┘ │
│                                    │
│  ● Serviços                        │
│  ┌─────────┐ ┌─────────┐         │
│  │ Corte   │ │ Barba   │         │
│  │ R$45    │ │ R$30    │         │
│  │ 30 min  │ │ 20 min  │         │
│  └─────────┘ └─────────┘         │
│  ┌──────────────┐                  │
│  │ Corte+Barba  │                  │
│  │ R$65 · 45min │                  │
│  └──────────────┘                  │
│                                    │
│  ● Nossa Equipe                    │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐        │
│  │ 📷│ │ 📷│ │ 📷│ │ 📷│        │
│  │Mar│ │Ped│ │Luc│ │Raf│        │
│  │4.9│ │4.7│ │4.8│ │4.9│        │
│  └───┘ └───┘ └───┘ └───┘        │
│  [Ver todos] →                     │
│                                    │
│  ● Onde Estamos                    │
│  ┌──────────────────────────────┐ │
│  │     [Google Maps embed]       │ │
│  │  Rua Augusta, 1234           │ │
│  └──────────────────────────────┘ │
│                                    │
│  ● Footer                          │
│  🟢 WhatsApp  📷 Instagram        │
│  Seg-Sex: 9h-19h · Sáb: 9h-14h   │
│                                    │
│  ┌──────────────────────────────┐ │
│  │   [AGENDAR AGORA] ← Fixo     │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘

Emoção: 🤩 "Site profissional, me passa confiança"
Scroll: Vertical, máximo 4 rolagens até o CTA
Botão fixo: "Agendar Agora" sempre visível no bottom
```

### Comportamento Responsivo (Desktop)

```
┌─────────────────────────────────────────────────────────────┐
│  🖥️ DESKTOP (≥1024px)                                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ LOGO        Serviços  Equipe  Galeria  Contato  [AGENDAR]││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │                                                          ││
│  │              BANNER PRINCIPAL (full-width)                ││
│  │          "Seu estilo, nossa arte"                         ││
│  │              [AGENDAR AGORA]                              ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  ● Serviços                    ● Nossa Equipe                │
│  ┌──────┐ ┌──────┐ ┌──────┐   ┌────┐ ┌────┐ ┌────┐ ┌────┐  │
│  │Corte │ │Barba │ │Combo │   │Mar │ │Ped │ │Luc │ │Raf │  │
│  └──────┘ └──────┘ └──────┘   └────┘ └────┘ └────┘ └────┘  │
│                                                              │
│  Google Maps (lateral direita)                               │
└─────────────────────────────────────────────────────────────┘
```

---

### TELA 3 — Agendamento: Profissional

```
┌────────────────────────────────────┐
│  📱 AGENDAR — PASSO 1 DE 4         │
│  8:42                             │
│  ┌──────────────────────────────┐ │
│  │ ← Voltar    Agendamento       │ │
│  │            ● ○ ○ ○            │ │  ← indicador de progresso
│  └──────────────────────────────┘ │
│                                    │
│  Escolha seu barbeiro              │
│  (Ou pule para "qualquer um")     │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 🟢 Qualquer profissional      │ │  ← Opção padrão (destaque)
│  │    Disponível mais cedo       │ │
│  │                          →   │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ 📷│ Marcos     ⭐ 4.9       │ │
│  │ │   │ Especialista em        │ │  ← Card com foto
│  │ └────┘ degradê e tesoura     │ │
│  │ Próx. horário: 09:30         │ │
│  │                          →   │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ 📷│ Ricardo    ⭐ 4.7       │ │
│  │ │   │ Cortes clássicos       │ │
│  │ └────┘ e barba tradicional    │ │
│  │ Próx. horário: 10:00         │ │
│  │                          →   │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ 📷│ Lucas      ⭐ 4.8       │ │
│  │ │   │ Cortes modernos         │ │
│  │ └────┘ e design               │ │
│  │ Próx. horário: 11:00         │ │
│  │                          →   │ │
│  └──────────────────────────────┘ │
│                                    │
│  [Pular etapa →]   ← Opção ágil   │
└────────────────────────────────────┘

Emoção: 🤔 "Quero o Marcos, ele é bem avaliado"
Problema: Barbeiro favorito sem horário → Sugerir "qualquer um" ou "lista de espera"
Microinteração: Card expande com leve scale (1.02) ao toque
```

### TELA 3B — Desktop (2 colunas)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Voltar      AGENDAMENTO      ● ○ ○ ○                      │
│                                                              │
│  ┌──────────────────────────┐  ┌───────────────────────────┐│
│  │                          │  │                           ││
│  │  Lista de barbeiros      │  │  Preview do perfil        ││
│  │                          │  │  (ao selecionar)          ││
│  │  🟢 Qualquer profissional │  │                           ││
│  │                          │  │  ┌────────┐               ││
│  │  📷 Marcos      ⭐4.9    │  │  │  FOTO  │  Marcos       ││
│  │  📷 Ricardo     ⭐4.7    │  │  │ GRANDE │  ⭐4.9        ││
│  │  📷 Lucas       ⭐4.8    │  │  └────────┘               ││
│  │                          │  │                           ││
│  │                          │  │  Especialista em degradê  ││
│  │                          │  │  e tesoura                ││
│  │                          │  │                           ││
│  │                          │  │  1.2k cortes realizados   ││
│  │                          │  │  "O melhor degradê da    ││
│  │                          │  │   cidade!" — João         ││
│  │                          │  │                           ││
│  └──────────────────────────┘  └───────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

### TELA 4 — Agendamento: Serviço

```
┌────────────────────────────────────┐
│  📱 AGENDAR — PASSO 2 DE 4         │
│  8:42                             │
│  ┌──────────────────────────────┐ │
│  │ ← Voltar    Agendamento       │ │
│  │            ○ ● ○ ○            │ │
│  └──────────────────────────────┘ │
│                                    │
│  Barbeiro: Marcos ✅               │
│  [Alterar]                         │
│                                    │
│  Escolha o serviço                 │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Corte              R$ 45,00  │ │
│  │ Tesoura, máquina e           │ │
│  │ finalização com pomada       │ │
│  │ ⏱ 30 min                    │ │
│  │                    [Escolher]│ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Barba              R$ 30,00  │ │
│  │ Toalha quente, balm e        │ │
│  │ navalhete                    │ │
│  │ ⏱ 20 min                    │ │
│  │                    [Escolher]│ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Corte + Barba      R$ 65,00  │ │
│  │ Combo completo               │ │
│  │ ⏱ 45 min        🏷 Mais pop  │ │
│  │                    [Escolher]│ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Hidratação         R$ 40,00  │ │
│  │ Tratamento capilar           │ │
│  │ ⏱ 25 min                    │ │
│  └──────────────────────────────┘ │
│                                    │
│  Total: R$ 0,00 | Duração: 0 min  │
│  (atualiza conforme seleção)       │
└────────────────────────────────────┘

Emoção: 💰 "Corte + Barba por R$ 65? Preço justo!"
Microinteração: Cards com leve elevação no hover/touch
Seleção múltipla: Check verde no card selecionado; total e duração atualizam com animação
```

---

### TELA 5 — Agendamento: Data e Horário

```
┌────────────────────────────────────┐
│  📱 AGENDAR — PASSO 3 DE 4         │
│  8:43                             │
│  ┌──────────────────────────────┐ │
│  │ ← Voltar    Agendamento       │ │
│  │            ○ ○ ● ○            │ │
│  └──────────────────────────────┘ │
│                                    │
│  Resumo: Marcos · Corte · R$45    │
│  [Alterar]                         │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     📅 CALENDÁRIO             │ │
│  │                              │ │
│  │  Julho 2026           ◀ ▶    │ │
│  │                              │ │
│  │  Dom Seg Ter Qua Qui Sex Sáb │ │
│  │             1   2   3   4    │ │
│  │   5   6   7   8   9  10  11  │ │
│  │  12  13  14  15  16  17  18  │ │
│  │  19 [20] 21  22  23  24  25  │ │  ← hoje selecionado
│  │  26  27  28  29  30  31      │ │
│  └──────────────────────────────┘ │
│                                    │
│  Segunda, 20 de Julho              │
│                                    │
│  MANHÃ                            │
│  ┌──────┬──────┬──────┬──────┐   │
│  │ 09:00│ 09:30│ 10:00│ 10:30│   │
│  │ Livre│ Livre│ Ocup │ Livre│   │
│  └──────┴──────┴──────┴──────┘   │
│                                    │
│  TARDE                            │
│  ┌──────┬──────┬──────┬──────┐   │
│  │ 13:00│ 13:30│ 14:00│ 14:30│   │
│  │ Livre│ Livre│ Livre│ Livre│   │
│  └──────┴──────┴──────┴──────┘   │
│                                    │
│  ┌──────┬──────┬──────┬──────┐   │
│  │ 15:00│ 15:30│ 16:00│ 16:30│   │
│  │ Livre│ Livre│ Livre│  ─── │   │
│  └──────┴──────┴──────┴──────┘   │
│                                    │
│  NOITE                             │
│  ┌──────┬──────┬──────┐           │
│  │ 17:00│ 17:30│ 18:00│           │
│  │ Livre│ Livre│ Indisp│          │
│  └──────┴──────┴──────┘           │
│                                    │
│  🟢 Livre  🔴 Ocupado  ⬜ Indisp. │
└────────────────────────────────────┘

Emoção: ⏰ "Tem amanhã às 14h, perfeito!"
Comportamento:
- Calendário: swipe horizontal para mudar mês
- Dias passados: opacidade 30%, não clicáveis
- Hoje: destaque com círculo na cor primária
- Slots: grid de 4 colunas, altura confortável para dedo (≥44px)
- Slot selecionado: preenchido com cor primária, animação de escala

Desktop:
- Calendário à esquerda (maior, com 2 meses visíveis)
- Grid de horários à direita
```

---

### TELA 6 — Agendamento: Dados do Cliente

```
┌────────────────────────────────────┐
│  📱 AGENDAR — PASSO 4 DE 4         │
│  8:43                             │
│  ┌──────────────────────────────┐ │
│  │ ← Voltar    Agendamento       │ │
│  │            ○ ○ ○ ●            │ │
│  └──────────────────────────────┘ │
│                                    │
│  Resumo:                            │
│  ┌──────────────────────────────┐ │
│  │ Barbeiro: Marcos              │ │
│  │ Serviço: Corte — R$ 45,00    │ │
│  │ Data: 20/07 (Segunda)         │ │
│  │ Horário: 14:30                │ │
│  │ Duração: 30 min               │ │
│  └──────────────────────────────┘ │
│                                    │
│  Seus dados                        │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 👤 Nome completo *            │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ João Silva               │ │ │
│  │ └──────────────────────────┘ │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 📱 WhatsApp *                 │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ (11) 99999-9999          │ │ │
│  │ └──────────────────────────┘ │ │
│  │ ⓘ Confirmação e lembrete     │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 📧 E-mail (opcional)          │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ joao@email.com           │ │ │
│  │ └──────────────────────────┘ │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 💬 Observação (opcional)      │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ Prefiro degradê baixo    │ │ │
│  │ └──────────────────────────┘ │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ✅ Li e aceito os termos     │ │
│  │ [ ] Quero receber promoções  │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     [CONFIRMAR AGENDAMENTO]  │ │
│  └──────────────────────────────┘ │
│                                    │
│  🔒 Seus dados estão seguros      │
│  ⏱ Tempo médio: 45 segundos       │
└────────────────────────────────────┘

Emoção: 😌 "Só meu nome e WhatsApp? Rápido!"
Campos: Mínimo de digitação. Máscara de telefone automática.
Validação: Em tempo real, com feedback visual positivo (check verde).
Termos: Checkbox LGPD obrigatório. Promoções opcional, não pré-marcado.
```

---

### TELA 7 — Pagamento (V1+)

```
┌────────────────────────────────────┐
│  📱 PAGAMENTO                       │
│  8:44                             │
│  ┌──────────────────────────────┐ │
│  │ ← Voltar    Pagamento         │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     💳 SINAL DE RESERVA       │ │
│  │                              │ │
│  │       R$ 10,00               │ │
│  │  (abatido no valor total)    │ │
│  └──────────────────────────────┘ │
│                                    │
│  Forma de pagamento                │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ PIX│  PIX                   │ │
│  │ │    │  Aprovação imediata    │ │
│  │ └────┘                  →    │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ 💳│  Cartão de Crédito     │ │
│  │ │    │  Visa, Mastercard...   │ │
│  │ └────┘                  →    │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ ┌────┐                        │ │
│  │ │ 💳│  Cartão de Débito      │ │
│  │ └────┘                  →    │ │
│  └──────────────────────────────┘ │
│                                    │
│  🔒 Pagamento seguro · Gateway X  │
└────────────────────────────────────┘

TELA 7B — PIX:
┌────────────────────────────────────┐
│  📱 PAGAMENTO — PIX                │
│  8:44                             │
│                                    │
│  R$ 10,00 — Studio 27 Barbearia   │
│                                    │
│  ┌──────────────────────────────┐ │
│  │                              │ │
│  │     ┌──────────────┐         │ │
│  │     │              │         │ │
│  │     │   QR CODE    │         │ │
│  │     │    PIX       │         │ │
│  │     │              │         │ │
│  │     └──────────────┘         │ │
│  │                              │ │
│  │  Abra seu app do banco       │ │
│  │  e escaneie o QR Code        │ │
│  │                              │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ PIX Copia e Cola              │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ 00020126360014BR.GOV...  │ │ │
│  │ └──────────────────────────┘ │ │
│  │         [COPIAR CÓDIGO]      │ │
│  └──────────────────────────────┘ │
│                                    │
│  ⏳ Aguardando pagamento...        │
│  ┌──────────────────────────────┐ │
│  │ ████████░░░░░░░░ 40%        │ │  ← animação de espera
│  │ ⏱ ~30 segundos              │ │
│  └──────────────────────────────┘ │
│                                    │
│  [Cancelar]                        │
└────────────────────────────────────┘

Emoção: 😰 Ansiedade leve → 😌 Confirmado!
UX Crítico:
- Loading amigável (não só spinner — barra animada)
- Timeout: 5 minutos. Depois, "Pagamento não detectado. Tente novamente."
- Polling a cada 2 segundos
- Se fechar sem querer: WhatsApp com link para retomar pagamento
```

---

### TELA 8 — Confirmação

```
┌────────────────────────────────────┐
│  📱 CONFIRMAÇÃO ✅                  │
│  8:44                             │
│                                    │
│  ┌──────────────────────────────┐ │
│  │                              │ │
│  │         ✅                   │ │  ← Animação: checkmark desenha
│  │     Agendamento              │ │
│  │     Confirmado!              │ │
│  │                              │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │                              │ │
│  │  📋 RESUMO                   │ │
│  │                              │ │
│  │  Barbearia  Studio 27        │ │
│  │  Barbeiro   Marcos           │ │
│  │  Serviço    Corte            │ │
│  │  Data       20/07/2026       │ │
│  │  Horário    14:30            │ │
│  │  Duração    30 min           │ │
│  │  Sinal      R$ 10,00 (PIX)  │ │
│  │  Endereço   Rua Augusta, 1234│ │
│  │                              │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ 📅 Adicionar ao Google Cal   │ │
│  └──────────────────────────────┘ │
│  ┌──────────────────────────────┐ │
│  │ 📅 Adicionar ao Apple Cal    │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     [VER MEUS AGENDAMENTOS]  │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     [VOLTAR AO SITE]         │ │
│  └──────────────────────────────┘ │
│                                    │
│  🟢 WhatsApp enviado com          │
│     confirmação e lembrete        │
└────────────────────────────────────┘

Emoção: 🎉 "Pronto! Rápido e fácil!"
Microinteração: Confetti sutil (3-5 partículas) na animação de checkmark
Ações pós-confirmação: Google Calendar, Apple Calendar, ver outros agendamentos
```

---

### TELA 9 — Pós-Atendimento: Avaliação

```
┌────────────────────────────────────┐
│  📱 MENSAGEM WHATSAPP               │
│  15:00 (logo após horário)         │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Studio 27 Barbearia          │ │
│  │                              │ │
│  │ Oi João! Como foi seu corte  │ │
│  │ com o Marcos? 😊             │ │
│  │                              │ │
│  │   ⭐ ⭐ ⭐ ⭐ ⭐              │ │  ← 5 estrelas interativas
│  │                              │ │
│  │ Deixe um comentário:         │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │ ________________________ │ │ │
│  │ └──────────────────────────┘ │ │
│  │                              │ │
│  │       [ENVIAR AVALIAÇÃO]     │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘

Emoção: 😊 "O corte ficou bom, vou dar 5 estrelas"

TELA 9B — Web (caso abra link):
┌──────────────────────────────────────────────┐
│  🖥️ Avalie seu atendimento                    │
│                                               │
│  ┌───────────────────────────────────────────┐│
│  │ ┌────┐                                    ││
│  │ │ 📷│  Marcos                             ││
│  │ └────┘  Corte — 20/07/2026                ││
│  └───────────────────────────────────────────┘│
│                                               │
│  Como foi sua experiência?                    │
│  ⭐ ⭐ ⭐ ⭐ ⭐  ← hover preenche com animação  │
│                                               │
│  O que achou?                                 │
│  ┌───────────────────────────────────────────┐│
│  │ [TAGS SUGERIDAS]                          ││
│  │ "Pontual" "Atendimento ótimo" "Preço bom" ││
│  │ "Corte perfeito" "Ambiente limpo"         ││
│  │                                           ││
│  │ ┌───────────────────────────────────────┐ ││
│  │ │ Comentário (opcional)                 │ ││
│  │ └───────────────────────────────────────┘ ││
│  └───────────────────────────────────────────┘│
│                                               │
│  ┌───────────────────────────────────────────┐│
│  │       [ENVIAR AVALIAÇÃO] 🚀               ││
│  └───────────────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

---

### TELA 10 — Retorno Automático (30 dias depois)

```
┌────────────────────────────────────┐
│  📱 WHATSAPP — D+30                 │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Studio 27 Barbearia          │ │
│  │                              │ │
│  │ Já faz 1 mês, João! 🪒       │ │
│  │                              │ │
│  │ Que tal renovar o visual?    │ │
│  │ O Marcos está com horário     │ │
│  │ disponível essa semana!       │ │
│  │                              │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │  Agendar novamente com   │ │ │
│  │ │  Marcos → Corte R$45     │ │ │
│  │ └──────────────────────────┘ │ │  ← Link direto, pré-preenchido
│  │                              │ │
│  │ ┌──────────────────────────┐ │ │
│  │ │  Ver outros horários     │ │ │
│  │ └──────────────────────────┘ │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘

UX Crítico:
- Link leva direto ao passo 3 (data/hora) — pula profissional e serviço
- Tudo pré-preenchido: mesmo barbeiro, mesmo serviço
- 1 clique → Tela de confirmação
- Tempo total: 15 segundos
```

---

## 1.3 Mapa de Emoções da Jornada

```
Emoção
  ↑
😍 │                  ████████
   │                 █        █
😊 │     ████████████          ████████
   │    █                            ██████
😐 │   █                                  ██████
   │  █                                         ████
😟 │ █                                              ██
   │ █                                                █
😰 │█                                                  ██
   └──┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──→ Tempo
     Instagram  Home  Prof.  Serv.  Data  Dados  Pgto  Confirm.
     
Momentos de fricção:
- Instagram → Site (transição de app; link precisa funcionar)
- Pagamento (ansiedade até confirmação)
- Dados pessoais (preocupação com privacidade)

Momentos de prazer:
- Confirmação ✅ (maior pico de satisfação)
- Avaliação ⭐ (fechamento positivo)
- Retorno 30 dias ("lembraram de mim!")
```

---

## 1.4 Estados e Edge Cases

### Estado: Barbeiro sem horário disponível
```
┌──────────────────────────────────┐
│ 😔 Marcos está sem horário esta  │
│    semana                        │
│                                  │
│ Sugestões:                       │
│ • Ver outro profissional         │
│ • Entrar na lista de espera      │
│ • Ser notificado quando abrir    │
└──────────────────────────────────┘
```

### Estado: Erro no pagamento
```
┌──────────────────────────────────┐
│ ❌ Pagamento não aprovado        │
│                                  │
│ Possíveis motivos:               │
│ • Saldo insuficiente             │
│ • Cartão bloqueado               │
│ • Tempo excedido                 │
│                                  │
│ [Tentar novamente]               │
│ [Outra forma de pagamento]       │
│ [Agendar sem pagamento]          │
└──────────────────────────────────┘
```

### Estado: Cancelamento pelo cliente
```
┌──────────────────────────────────┐
│ Cancelar agendamento?            │
│                                  │
│ Data: 20/07 às 14:30             │
│ Barbeiro: Marcos                 │
│ Serviço: Corte                   │
│                                  │
│ ⚠️ Cancelamentos até 2h antes    │
│    têm reembolso do sinal.       │
│                                  │
│ [Manter agendamento]             │
│ [Cancelar mesmo assim]           │
└──────────────────────────────────┘
```

### Estado: Lista de espera
```
┌──────────────────────────────────┐
│ 📋 Entrar na lista de espera     │
│                                  │
│ Caso alguém cancele, você será   │
│ notificado automaticamente.      │
│                                  │
│ Data preferida: 20/07            │
│ Horário preferido: Tarde         │
│                                  │
│ [ENTRAR NA LISTA]                │
│                                  │
│ 3 pessoas na sua frente 🟡       │
└──────────────────────────────────┘
```

### Estado: Cliente novo vs. recorrente
```
CLIENTE NOVO (sem conta):
- Formulário completo (nome, WhatsApp, e-mail)
- Sem histórico
- Oferecer "Criar conta para agilizar próximas vezes"

CLIENTE RECORRENTE (com conta / telefone reconhecido):
- Campos pré-preenchidos
- "Repetir último agendamento?" com 1 clique
- Histórico de barbeiros favoritos
- "Marcos é seu barbeiro favorito — agendar com ele?"
```

---

## 1.5 Métricas de Sucesso da Jornada

| Métrica | Alvo |
|---------|------|
| Tempo total até confirmação | < 2 minutos |
| Taxa de abandono no fluxo | < 30% |
| Taxa de conclusão (visita → agendamento) | > 15% |
| Cliques até agendar | < 10 cliques/toques |
| Campos de texto preenchidos | ≤ 3 (nome, WhatsApp, observação opcional) |
| Avaliações coletadas | > 40% dos atendimentos |
| Reagendamento via link de retorno | > 25% |

---

> **Resumo:** A jornada do cliente é o coração do produto. Cada milissegundo conta. Cada campo a mais reduz a conversão. Mobile-first não é opcional — é a realidade de 90% dos usuários. O fluxo deve ser tão simples que o cliente nem percebe que "usou um sistema".
