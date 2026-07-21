# 04 — Jornada da Recepcionista

> **Persona:** Ana, 24 anos · Recepcionista  
> **Dispositivo:** Tablet (60%) / Desktop (30%) / Mobile (10%)  
> **Objetivo:** Gerenciar agenda de múltiplos profissionais, atender clientes

---

## 4.1 Tela Principal: Visão Multi-Profissional

```
┌──────────────────────────────────────────────────────────────┐
│  🖥️ RECEPÇÃO — Quarta, 20 Jul · 09:15                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ ☰  │ Recepção  │ 🔔5 │ 👤 Ana │ [Studio 27]             ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────┬──────────┬──────────┬──────────┐               │
│  │  Todos   │ Marcos   │ Ricardo  │ Lucas    │  ← Filtros    │
│  └──────────┴──────────┴──────────┴──────────┘               │
│                                                               │
│  ┌──────────┬──────────┬──────────┬──────────┐               │
│  │   MANHÃ  │  MARCOS  │ RICARDO  │  LUCAS   │               │
│  ├──────────┼──────────┼──────────┼──────────┤               │
│  │  09:00   │ ✅ Corte │ ⬜ Livre │ 🔵 Barba│               │
│  │          │ João S.  │          │ Carlos   │               │
│  ├──────────┼──────────┼──────────┼──────────┤               │
│  │  09:30   │ ✅ Barba │ 🔵 Corte │ ⬜ Livre │               │
│  │          │ Pedro L. │ Rafael   │          │               │
│  ├──────────┼──────────┼──────────┼──────────┤               │
│  │  10:00   │ ⬜ Livre │ ⬜ Livre │ 🔵 Combo│               │
│  │          │          │          │ Ana C.   │               │
│  ├──────────┼──────────┼──────────┼──────────┤               │
│  │  10:30   │ 🔵 Corte │ 🔵 Barba│ ⬜ Livre │               │
│  │          │ Bruno M. │ Gustavo  │          │               │
│  ├──────────┼──────────┼──────────┼──────────┤               │
│  │  11:00   │ 🔵 Corte │ ⬜ Livre │ ⬜ Livre │               │
│  └──────────┴──────────┴──────────┴──────────┘               │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ + NOVO AGENDAMENTO    │ 📋 Lista de Espera (3) │ ✅ Hoje││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘

Legenda:
✅ = Concluído (verde)
🔵 = Agendado (azul) 
⬜ = Livre (cinza claro)
🔴 = Em atraso / No-show (vermelho)
🟡 = Em andamento (amarelo)
🔒 = Bloqueado
```

---

## 4.2 Tela: Agendamento Rápido (Walk-in / Telefone)

```
┌──────────────────────────────────────────────────────────────┐
│  📋 NOVO AGENDAMENTO                                          │
│                                                               │
│  Cliente:                   Profissional:                     │
│  ┌───────────────────────┐  ┌──────────────────────────────┐ │
│  │ Buscar cliente...     │  │ Marcos ▾                     │ │
│  │ João Silva            │  └──────────────────────────────┘ │
│  │ (11) 99999-9999       │                                    │
│  └───────────────────────┘  Serviço:                          │
│                              ┌──────────────────────────────┐ │
│  Data:                       │ Corte — R$ 45 (30 min) ▾     │ │
│  ┌──────────────┐           └──────────────────────────────┘ │
│  │ 20/07/2026   │                                            │
│  └──────────────┘           Horário:                          │
│                              ┌──────────────────────────────┐ │
│  ⏱ Próximos disponíveis:    │ 14:30 ▾                      │ │
│  ┌──────┬──────┬──────┐     └──────────────────────────────┘ │
│  │ 14:00│ 14:30│ 15:00│                                      │
│  │Marcos│Marcos│Ricard│     Observação:                       │
│  └──────┴──────┴──────┘     ┌──────────────────────────────┐ │
│                              │ ................              │ │
│                              └──────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │              [AGENDAR]                                    ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘

UX pensado para agilidade:
- Busca de cliente por nome ou telefone (autocomplete em 2 chars)
- Se cliente novo: campos aparecem inline (sem modal)
- Slots disponíveis já filtrados pelo serviço + profissional
- 1 clique para agendar
```

---

## 4.3 Tela: Check-in do Cliente

```
┌──────────────────────────────────────────────────────────────┐
│  ✅ CHECK-IN                                                   │
│                                                               │
│  Cliente chegou? Busque pelo nome:                             │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ 🔍 "João"                                                ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ João Silva — Corte com Marcos — 09:00                    ││
│  │                                        [CHECK-IN ✅]     ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ João Pereira — Barba com Ricardo — 09:30                 ││
│  │                                        [CHECK-IN ✅]     ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ⏱ Aguardando (2):                                            │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ ✅ João Silva — Aguardando 5 min                          ││
│  │    Check-in: 08:55 | Enviar WhatsApp: "Já pode entrar"   ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  🟢 Em atendimento (3):                                       │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ ✅ Pedro Lima — Com Marcos desde 09:02                    ││
│  │ ✅ Ana Costa — Com Lucas desde 09:00                      ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## 4.4 Notificações da Recepcionista

| Evento | Notificação |
|--------|------------|
| Novo agendamento online | 🔔 "João S. agendou Corte com Marcos 20/07 14:30" |
| Cancelamento | 🔔 "Rafael cancelou Corte 20/07 10:00" |
| Cliente atrasado | 🔴 "João S. está 10 min atrasado. Enviar WhatsApp?" |
| Horário liberado | 🟢 "Horário 10:00 liberado! 3 pessoas na lista de espera" |
| Lembrete do dia | 📋 "Hoje: 24 agendamentos, 3 aniversariantes" |

---

## 4.5 Diferenças: Recepcionista vs. Admin

| Ação | Recepcionista | Admin (Dono) |
|------|:------------:|:------------:|
| Ver agenda de todos | ✅ | ✅ |
| Agendar para cliente | ✅ | ✅ |
| Check-in | ✅ | ✅ |
| Cancelar agendamento | ✅ (do dia) | ✅ (qualquer) |
| Alterar serviços/preços | ❌ | ✅ |
| Adicionar profissional | ❌ | ✅ |
| Ver relatórios financeiros | ❌ | ✅ |
| Personalizar site | ❌ | ✅ |
| Ver comissões | ❌ | ✅ |
| Gerenciar plano | ❌ | ✅ |

---

> **Resumo:** A recepcionista é a linha de frente. Sua interface deve ser a mais rápida do sistema — agenda multi-coluna, busca instantânea, check-in com 1 toque. Ela não precisa de relatórios ou configurações — precisa de velocidade para atender o cliente que está na frente dela.
