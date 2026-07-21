# 07 — Fluxos do Sistema

---

## 7.1 Fluxo do Cliente (Agendamento Completo)

```
┌──────────────────────────────────────────────────────────────────┐
│                    JORNADA DO CLIENTE                             │
│                    (~2 minutos)                                    │
└──────────────────────────────────────────────────────────────────┘

ETAPA 1: DESCOBERTA
─────────────────────
  Instagram / Google / Indicação
      │
      ▼
  Entra no site da barbearia (domínio próprio)
      │
      ├── Vê banner, logo, identidade visual da barbearia
      ├── Vê serviços com preços e duração
      ├── Vê equipe com fotos e avaliações
      └── Decide agendar
      │
      ▼

ETAPA 2: ESCOLHA DO PROFISSIONAL (opcional)
────────────────────────────────────────────
  [ ] Qualquer profissional disponível (recomendado)
  [ ] Barbeiro específico
      │
      ▼

ETAPA 3: ESCOLHA DO SERVIÇO
─────────────────────────────
  Seleciona 1 ou mais serviços:
  □ Corte (R$ 45, 30 min)
  □ Barba (R$ 30, 20 min)
  □ Corte + Barba (R$ 65, 45 min)
  Total: R$ __ | Duração: __ min
      │
      ▼

ETAPA 4: ESCOLHA DO HORÁRIO
─────────────────────────────
  Calendário → Seleciona data
      │
      ▼
  Grid de horários disponíveis:
  ┌──────┬──────┬──────┬──────┐
  │ 09:00│ 09:30│ 10:00│ 10:30│
  │  Livre│ Livre│  Ocup │ Livre│
  └──────┴──────┴──────┴──────┘
  Seleciona slot → Confirmar
      │
      ▼

ETAPA 5: IDENTIFICAÇÃO
───────────────────────
  Nome: __________________
  Telefone: ______________ (WhatsApp)
  E-mail: ________________ (opcional)
  Observação: ____________ (opcional)
      │
      ▼

ETAPA 6: PAGAMENTO (futuro)
─────────────────────────────
  Valor do sinal: R$ 10,00
  [ ] PIX → QR Code / Copia e Cola
  [ ] Cartão de Crédito
  Aguardando pagamento...
  Pagamento confirmado ✓
      │
      ▼

ETAPA 7: CONFIRMAÇÃO
─────────────────────
  ✅ Agendamento Confirmado!
  ┌────────────────────────────┐
  │ Barbearia: Studio X        │
  │ Barbeiro: Marcos           │
  │ Serviço: Corte             │
  │ Data: 25/07/2026           │
  │ Horário: 14:30             │
  │ Sinal: R$ 10,00 (PIX)      │
  │ Endereço: Rua X, 123       │
  │                            │
  │ [Adicionar ao Google Cal]  │
  │ [Adicionar ao Apple Cal]   │
  └────────────────────────────┘
      │
      ▼

ETAPA 8: PÓS-AGENDAMENTO
──────────────────────────
  ✓ WhatsApp: "Agendamento confirmado para 25/07 às 14:30"
  ✓ WhatsApp (24h antes): "Lembrete: amanhã às 14:30"
  ✓ WhatsApp (1h antes): "Seu horário é daqui 1h!"
      │
      ▼

ETAPA 9: ATENDIMENTO
─────────────────────
  Chegada → Check-in → Atendimento → Conclusão
      │
      ▼

ETAPA 10: PÓS-ATENDIMENTO
───────────────────────────
  WhatsApp: "Como foi seu corte? Avalie de 1 a 5 ⭐"
      │
      ▼
  (30 dias depois)
  WhatsApp: "Já faz 1 mês! Que tal agendar de novo?"
  Link direto para reagendamento com mesmo barbeiro.
```

---

## 7.2 Fluxo do Barbeiro / Profissional

```
┌──────────────────────────────────────────────────────────────────┐
│                    JORNADA DO BARBEIRO                            │
└──────────────────────────────────────────────────────────────────┘

DIÁRIO
──────
  Abre painel
      │
      ▼
  Vê agenda do dia:
  ┌──────────────────────────────────┐
  │ Hoje — 25/07/2026                │
  │                                  │
  │ 09:00  João Silva    Corte       │
  │ 09:30  Pedro Lima    Barba       │
  │ 10:00  — Livre —                 │
  │ 10:30  Carlos Souza  Corte+Barba │
  │ ...                              │
  └──────────────────────────────────┘
      │
      ▼
  Cliente chega → Marca check-in ✓
      │
      ▼
  Atende → Ao finalizar, marca "Concluído" ✓
      │
      ▼
  (Opcional) Adiciona observação:
  "Cliente pediu degradê baixo, gosta de finalizar com pomada"

NOTIFICAÇÕES
────────────
  • Novo agendamento: notificação push + WhatsApp
  • Cancelamento: notificação imediata
  • Lembrete de agenda do dia: 7h da manhã

VISUALIZAÇÕES
─────────────
  • Agenda do dia (padrão)
  • Agenda da semana (visão semanal)
  • Próximos agendamentos
  • Histórico de atendimentos

  • Ver perfil público (como cliente vê)
  • Ver avaliações recebidas
  • Ver faturamento pessoal (se comissionado)
```

---

## 7.3 Fluxo do Administrador (Dono/Gerente)

```
┌──────────────────────────────────────────────────────────────────┐
│                 JORNADA DO ADMINISTRADOR                          │
└──────────────────────────────────────────────────────────────────┘

ONBOARDING (PRIMEIRO ACESSO)
─────────────────────────────
  Cadastro na plataforma
      │
      ▼
  Escolhe subdomínio: minhabarbearia.barbersaas.com
      │
      ▼
  Wizard de configuração inicial:
  ┌─────────────────────────────────────┐
  │ 1. Nome da barbearia               │
  │ 2. Logo (upload)                   │
  │ 3. Telefone / WhatsApp             │
  │ 4. Endereço                        │
  │ 5. Horário de funcionamento        │
  │ 6. Serviços (nome, preço, duração) │
  │ 7. Profissionais (nome, foto)      │
  └─────────────────────────────────────┘
      │
      ▼
  Site no ar! 🚀

DIÁRIO/SEMANAL
───────────────
  Dashboard:
  ┌─────────────────────────────────────┐
  │ Faturamento Hoje:      R$ 450,00    │
  │ Agendamentos Hoje:     12           │
  │ Ocupação:              75%          │
  │                                     │
  │ Profissionais:                      │
  │ Marcos:  8 agend. | R$ 320 | 80%   │
  │ Ricardo: 4 agend. | R$ 130 | 40%   │
  └─────────────────────────────────────┘

GESTÃO (QUANDO PRECISAR)
──────────────────────────
  Serviços:
  • Adicionar novo serviço
  • Alterar preço ou duração
  • Desativar serviço temporariamente
  • Reordenar exibição no site

  Equipe:
  • Adicionar profissional
  • Alterar foto, bio, especialidades
  • Remover profissional
  • Configurar horários individuais

  Site:
  • Trocar logo
  • Trocar banner
  • Alterar cores
  • Adicionar fotos na galeria
  • Ver preview do site

  Promoções:
  • Criar cupom de desconto
  • Definir validade
  • Promoção em serviço específico

  Relatórios:
  • Faturamento por período
  • Comparativo mês a mês
  • Profissional mais produtivo
  • Serviço mais vendido
  • Taxa de retorno
  • Exportar (PDF/Excel)
```

---

## 7.4 Fluxo de Pagamentos

```
┌──────────────────────────────────────────────────────────────────┐
│                    FLUXO DE PAGAMENTOS                            │
└──────────────────────────────────────────────────────────────────┘

NOSSO SISTEMA (NUNCA TOCA DADOS DE CARTÃO):
────────────────────────────────────────────

  Cliente seleciona "Pagar Sinal"
      │
      ▼
  Backend cria Payment Intent:
  {
    "payment_id": "pay_abc123",
    "amount": 1000,           // centavos (R$ 10,00)
    "currency": "BRL",
    "tenant_id": "t_xyz",
    "status": "pending"
  }
      │
      ▼
  Frontend redireciona para Gateway (Stripe Checkout / PagSeguro)
      │
      ▼
  Cliente interage APENAS com o Gateway:
  • Digita dados do cartão
  • Ou escaneia QR Code PIX
  • Gateway processa pagamento
      │
      ▼
  Gateway envia Webhook para nosso sistema:
  POST /api/v1/webhooks/payment
  {
    "event": "payment.succeeded",
    "payment_id": "pay_abc123",
    "gateway": "stripe",
    "status": "paid",
    "amount": 1000,
    "paid_at": "2026-07-20T14:30:00Z"
  }
      │
      ▼
  Nosso sistema:
  • Verifica assinatura do webhook (HMAC)
  • Atualiza status: pending → paid
  • Confirma agendamento
  • Dispara notificações (cliente + barbeiro)

DADOS QUE ARMAZENAMOS:
───────────────────────
  ✓ payment_id (gateway)
  ✓ status (pending, paid, refunded, failed)
  ✓ amount
  ✓ gateway (stripe, pagseguro, mercadopago)
  ✓ paid_at
  ✓ refunded_at (se aplicável)

DADOS QUE NUNCA ARMAZENAMOS:
─────────────────────────────
  ✗ Número do cartão
  ✗ CVV
  ✗ Data de validade
  ✗ Nome no cartão
  ✗ Chave PIX do cliente

REEMBOLSO:
──────────
  Admin solicita reembolso via painel
      │
      ▼
  Sistema chama API do Gateway: refund(payment_id)
      │
      ▼
  Gateway processa → Webhook confirmando
      │
      ▼
  Sistema atualiza: paid → refunded
  Agendamento é cancelado automaticamente
```

---

## 7.5 Fluxo de Notificações

```
┌──────────────────────────────────────────────────────────────────┐
│                 FLUXO DE NOTIFICAÇÕES (Assíncrono)                │
└──────────────────────────────────────────────────────────────────┘

  Evento ocorre (ex: agendamento criado)
      │
      ▼
  Serviço publica evento no Redis Stream:
  {
    "event_type": "booking.created",
    "tenant_id": "t_123",
    "payload": {
      "booking_id": "b_456",
      "customer_name": "João",
      "customer_phone": "+5511999999999",
      "customer_email": "joao@email.com",
      "barber_name": "Marcos",
      "service": "Corte",
      "date": "2026-07-25",
      "time": "14:30"
    }
  }
      │
      ▼
  Notification Service consome o evento:
      │
      ├── WhatsApp (Evolution API / WPPConnect)
      │   └── "Olá João! Seu corte com Marcos está confirmado..."
      │
      ├── E-mail (AWS SES / Mailgun / Resend)
      │   └── Template HTML com detalhes + botão "Adicionar ao calendário"
      │
      ├── Push Notification (PWA — Service Worker)
      │   └── "Agendamento confirmado para 25/07 às 14:30"
      │
      └── SMS (futuro, via Twilio / Zenvia)
          └── "Barbearia X: Agendamento confirmado 25/07 14:30"

STATUS DE ENTREGA:
──────────────────
  Cada notificação registra:
  • Canal (whatsapp, email, push, sms)
  • Status (sent, delivered, read, failed)
  • Timestamp
  • Retries (se falhou)

FALHAS:
───────
  • Retry com backoff (1min, 5min, 15min, 1h)
  • Máximo 5 tentativas
  • Após falha total → Dead Letter Queue
  • Admin notificado se taxa de falha > 5%
```

---

## 7.6 Fluxo de Permissões (RBAC)

```
┌──────────────────────────────────────────────────────────────────┐
│                    FLUXO DE AUTORIZAÇÃO                           │
└──────────────────────────────────────────────────────────────────┘

  Request chega ao API Gateway
      │
      ▼
  Extrai JWT do header Authorization
      │
      ▼
  Valida assinatura + expiração
      │
      ├── Inválido → 401 Unauthorized
      │
      ▼ (válido)
  Extrai claims do JWT:
  {
    "sub": "user_789",
    "tenant_id": "t_123",
    "role": "barber",       // ou "admin", "receptionist", "super_admin"
    "permissions": [
      "booking:read",
      "booking:write:own",
      "schedule:read:own"
    ]
  }
      │
      ▼
  Middleware de autorização:
  Rota: PUT /api/v1/bookings/b_456
  Required: booking:write_own OR booking:write_any
      │
      ├── Sem permissão → 403 Forbidden
      │
      ▼ (tem permissão)
  Tenant isolation check:
  O recurso b_456 pertence ao tenant t_123?
      │
      ├── Não → 403 Forbidden (tentativa de acesso cross-tenant)
      │
      ▼ (pertence)
  ✅ Request processado

SUPER ADMIN:
────────────
  • Não tem tenant_id (ou tem tenant_id = "platform")
  • Acessa endpoints do BFF Super Admin
  • Pode impersonar tenant (feature futura)
  • Todas ações são logadas com flag is_super_admin = true
```

---

## 7.7 Fluxo de Onboarding do Tenant

```
┌──────────────────────────────────────────────────────────────────┐
│                 JORNADA DE ONBOARDING DO TENANT                   │
└──────────────────────────────────────────────────────────────────┘

  Dono acessa: barbersaas.com.br
      │
      ▼
  Landing page da plataforma:
  • Vídeo de apresentação
  • Funcionalidades
  • Preços
  • Depoimentos
  [Botão: Começar Grátis]
      │
      ▼
  Cadastro:
  • Nome completo
  • E-mail
  • Senha
  • Nome da barbearia
  • Subdomínio desejado (minhabarbearia.barbersaas.com)
  [Botão: Criar conta]
      │
      ▼
  E-mail de verificação (futuro)
  Por enquanto: login direto
      │
      ▼
  Wizard de configuração (5 passos):
  ┌─────────────────────────────────────┐
  │ Passo 1: Identidade                 │
  │ • Upload do logo                    │
  │ • Nome da barbearia                 │
  │ • Slogan (opcional)                 │
  │                                     │
  │ Passo 2: Contato                    │
  │ • WhatsApp                          │
  │ • Telefone fixo (opcional)          │
  │ • Endereço                          │
  │ • Link Google Maps                  │
  │                                     │
  │ Passo 3: Horários                   │
  │ □ Seg: 09:00-19:00                  │
  │ □ Ter: 09:00-19:00                  │
  │ ...                                 │
  │                                     │
  │ Passo 4: Serviços                   │
  │ + Adicionar serviço:                │
  │   Nome: Corte                       │
  │   Preço: R$ 45,00                   │
  │   Duração: 30 min                   │
  │                                     │
  │ Passo 5: Equipe                     │
  │ + Adicionar profissional:           │
  │   Nome: Marcos                      │
  │   Foto: [upload]                    │
  └─────────────────────────────────────┘
      │
      ▼
  ✅ Site no ar!
  URL: minhabarbearia.barbersaas.com
  Painel: minhabarbearia.barbersaas.com/admin
```

---

> **Resumo dos fluxos:** Todos os caminhos críticos foram mapeados. O sistema é orientado a eventos para operações assíncronas (notificações) e síncrono para operações que exigem resposta imediata (agendamento). O RBAC garante que cada perfil veja e faça apenas o que seu papel permite.
