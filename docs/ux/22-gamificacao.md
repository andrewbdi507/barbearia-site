# 22 — Gamificação & Fidelidade

> Transformar clientes em fãs através de recompensas e reconhecimento.

---

## 22.1 Sistema de Conquistas (Badges)

### Badges para Clientes

| Badge | Nome | Como Ganhar | Ícone |
|-------|------|-------------|:-----:|
| 🆕 | **Primeira vez** | 1º agendamento concluído | 🌱 |
| 🔄 | **Fiel** | 5 agendamentos | ⭐ |
| 💎 | **VIP** | 20 agendamentos | 💎 |
| 📅 | **Pontual** | 10 agendamentos sem atraso | ⏰ |
| 🗓️ | **Mensal** | Agendou todo mês por 6 meses | 📆 |
| 👥 | **Influencer** | 3 amigos indicados | 📣 |
| 🎂 | **Aniversariante** | Agendou no mês do aniversário | 🎂 |
| 💬 | **Avaliador** | 10 avaliações escritas | ✍️ |
| 🏆 | **Lendário** | 50 agendamentos | 👑 |

### Exibição no Perfil do Cliente

```
┌──────────────────────────────────────┐
│  👤 João Silva                        │
│                                      │
│  ┌──────────────────────────────────┐│
│  │ 💎 VIP — 24 agendamentos         ││
│  │                                  ││
│  │ Conquistas:                      ││
│  │ 🌱 ⭐ 💎 ⏰ 📆 💬                ││
│  │                                  ││
│  │ Próximo nível:                   ││
│  │ 🏆 Lendário (50 agendamentos)    ││
│  │ ████████████░░░░░░ 48%          ││
│  └──────────────────────────────────┘│
└──────────────────────────────────────┘
```

---

## 22.2 Programa de Fidelidade (Pontos)

### Como Funciona

```
Cada R$ 1 gasto = 1 ponto

┌──────────────────────────────────────┐
│  Benefícios por pontos:              │
│                                      │
│  100 pts  →  10% desconto            │
│  250 pts  →  Barba grátis            │
│  500 pts  →  Corte grátis            │
│  1000 pts →  Combo grátis + bebida   │
└──────────────────────────────────────┘
```

### Tela do Cliente: Meus Pontos

```
┌──────────────────────────────────────┐
│  ⭐ Meus Pontos                       │
│                                      │
│  ┌──────────────────────────────────┐│
│  │        ⭐ 340 pontos              ││
│  │                                  ││
│  │  ████████████████░░░░ 68%       ││
│  │        para 500 pts               ││
│  └──────────────────────────────────┘│
│                                      │
│  Resgate disponível:                 │
│  ┌──────────────────────────────────┐│
│  │ ✅ 10% desconto (100 pts)        ││
│  │ ✅ Barba grátis (250 pts)        ││
│  │ ⬜ Corte grátis (500 pts)        ││
│  └──────────────────────────────────┘│
│                                      │
│  Histórico de pontos:                │
│  20/07  Corte R$45  +45 pts         │
│  20/06  Combo R$65  +65 pts         │
│  20/05  Resgate -100 pts             │
└──────────────────────────────────────┘
```

---

## 22.3 Programa de Indicação

### Tela: Indicar Amigos

```
┌──────────────────────────────────────┐
│  👥 Indique e Ganhe                   │
│                                      │
│  ┌──────────────────────────────────┐│
│  │  Indique um amigo e ambos         ││
│  │  ganham R$ 10 de desconto!       ││
│  └──────────────────────────────────┘│
│                                      │
│  Seu link de indicação:              │
│  ┌──────────────────────────────────┐│
│  │ studio27.barbersaas.com.br/      ││
│  │ agendar?ref=JOAO123             ││
│  │                    [COPIAR LINK] ││
│  └──────────────────────────────────┘│
│                                      │
│  ┌──────────────────────────────────┐│
│  │     [COMPARTILHAR WHATSAPP]      ││
│  └──────────────────────────────────┘│
│                                      │
│  Amigos indicados: 3                 │
│  Créditos ganhos: R$ 30,00           │
│                                      │
│  ┌──────────────────────────────────┐│
│  │ ✅ Pedro — agendou (R$ 10)       ││
│  │ ✅ Lucas — agendou (R$ 10)       ││
│  │ ✅ Gabriel — agendou (R$ 10)     ││
│  └──────────────────────────────────┘│
└──────────────────────────────────────┘
```

---

## 22.4 Aniversário

### Tela: Benefício de Aniversário

O cliente recebe automaticamente um cupom no mês do aniversário:

```
┌──────────────────────────────────────┐
│  🎂 Feliz Aniversário, João!          │
│                                      │
│  ┌──────────────────────────────────┐│
│  │     🎁 PRESENTE PARA VOCÊ        ││
│  │                                  ││
│  │     20% de desconto              ││
│  │     em qualquer serviço          ││
│  │                                  ││
│  │  Código: ANIVER25               ││
│  │  Válido até: 31/07              ││
│  │                                  ││
│  │     [AGENDAR COM DESCONTO]       ││
│  └──────────────────────────────────┘│
└──────────────────────────────────────┘
```

Disparado via WhatsApp 7 dias antes do aniversário.

---

## 22.5 Ranking (Opcional — Gamificação Interna)

### Para Profissionais

```
┌──────────────────────────────────────────────────────────────┐
│  🏆 Ranking do Mês — Julho                                    │
│                                                               │
│  ┌────┬──────────────────┬──────────┬────────┬────────────┐ │
│  │ 🥇 │ Marcos           │ 120 cort │ ⭐4.9  │ R$ 5.400   │ │
│  │ 🥈 │ Lucas            │ 105 cort │ ⭐4.8  │ R$ 4.725   │ │
│  │ 🥉 │ Ricardo          │  85 cort │ ⭐4.7  │ R$ 3.825   │ │
│  │ 4º │ Rafael           │  72 cort │ ⭐4.9  │ R$ 3.240   │ │
│  └────┴──────────────────┴──────────┴────────┴────────────┘ │
│                                                               │
│  🎯 Meta do mês: 100 agendamentos                             │
│  🏅 Prêmio: R$ 200 bônus                                     │
└──────────────────────────────────────────────────────────────┘
```

Opcional — configurável pelo dono. Pode ser desligado.

---

## 22.6 Notificações de Gamificação

| Gatilho | Mensagem |
|---------|----------|
| Nova conquista | **"🏆 Conquista desbloqueada: Fiel (5 agendamentos)!"** |
| Pontos suficientes | **"⭐ Você tem 250 pontos! Que tal resgatar uma Barba grátis?"** |
| Indicação convertida | **"👥 Pedro agendou com seu link! Você ganhou R$ 10!"** |
| Aniversário | **"🎂 Seu aniversário está chegando! Um presente te espera..."** |
| Quase VIP | **"💎 Faltam 3 agendamentos para você virar VIP!"** |

---

> **Resumo:** Gamificação não é sobre pontos e badges — é sobre fazer o cliente se sentir valorizado e reconhecido. O programa de fidelidade incentiva retorno. As conquistas geram compartilhamento social. A indicação reduz CAC. Tudo integrado de forma natural, sem parecer forçado.
