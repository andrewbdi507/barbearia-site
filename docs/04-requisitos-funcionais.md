# 04 — Requisitos Funcionais

> Lista exaustiva de funcionalidades agrupadas por módulo.  
> Cada funcionalidade é uma unidade atômica de valor para o usuário.

---

## 4.1 Módulo: Site Público (Vitrine)

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-001 | Página inicial com banner e logo do tenant | P0 | ✅ |
| RF-002 | Listagem de serviços com preços e duração | P0 | ✅ |
| RF-003 | Listagem de profissionais com foto, bio e avaliações | P0 | ✅ |
| RF-004 | Grid de horários disponíveis em tempo real | P0 | ✅ |
| RF-005 | Fluxo de agendamento (profissional → serviço → data → horário) | P0 | ✅ |
| RF-006 | Formulário de cadastro/identificação do cliente | P0 | ✅ |
| RF-007 | Confirmação de agendamento com resumo | P0 | ✅ |
| RF-008 | Pagamento de sinal (PIX, cartão) via gateway | P1 | ❌ |
| RF-009 | Página "Sobre" da empresa | P1 | ❌ |
| RF-010 | Galeria de fotos (trabalhos realizados) | P1 | ❌ |
| RF-011 | Depoimentos e avaliações públicas | P2 | ❌ |
| RF-012 | Links para redes sociais | P1 | ❌ |
| RF-013 | Mapa e endereço com Google Maps embed | P1 | ❌ |
| RF-014 | Página de promoções ativas | P2 | ❌ |
| RF-015 | Blog da barbearia | P3 | ❌ |
| RF-016 | FAQ personalizável | P3 | ❌ |
| RF-017 | SEO por tenant (meta tags, sitemap, structured data) | P1 | ❌ |
| RF-018 | Domínio próprio do tenant (não só subdomínio) | P1 | ❌ |
| RF-019 | Chat widget (WhatsApp flutuante) | P1 | ❌ |
| RF-020 | Tema customizável (cores, fontes, layout) | P1 | ❌ |

---

## 4.2 Módulo: Agendamento

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-021 | Seleção de profissional pelo cliente | P0 | ✅ |
| RF-022 | Seleção de serviço (com preço e duração) | P0 | ✅ |
| RF-023 | Visualização de horários disponíveis em grid | P0 | ✅ |
| RF-024 | Agendamento com dados do cliente (nome, telefone, e-mail) | P0 | ✅ |
| RF-025 | Validação de telefone (SMS/WhatsApp) | P2 | ❌ |
| RF-026 | Validação de e-mail | P2 | ❌ |
| RF-027 | Limite de agendamentos futuros por cliente | P2 | ❌ |
| RF-028 | Bloqueio de horário durante o fluxo (reserva temporária de 10 min) | P1 | ❌ |
| RF-029 | Cancelamento pelo cliente (com prazo limite) | P1 | ❌ |
| RF-030 | Reagendamento pelo cliente | P2 | ❌ |
| RF-031 | Lista de espera para horários lotados | P3 | ❌ |
| RF-032 | Agendamento recorrente (ex: "toda sexta 15h") | P3 | ❌ |
| RF-033 | Agendamento de múltiplos serviços na mesma visita | P2 | ❌ |
| RF-034 | Duração dinâmica (serviço A + B = soma dos tempos) | P2 | ❌ |
| RF-035 | Intervalo entre agendamentos configurável | P1 | ❌ |
| RF-036 | Horário de funcionamento por profissional | P0 | ✅ |
| RF-037 | Horário de funcionamento por dia da semana | P0 | ✅ |
| RF-038 | Bloqueio de datas especiais (feriados, férias) | P1 | ❌ |
| RF-039 | Agendamento como visitante (sem cadastro) | P0 | ✅ |
| RF-040 | Agendamento com conta (histórico salvo) | P2 | ❌ |

---

## 4.3 Módulo: Pagamentos

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-041 | Integração com gateway de pagamento (Stripe/PagSeguro/MercadoPago) | P1 | ❌ |
| RF-042 | Pagamento de sinal (valor fixo ou percentual) | P1 | ❌ |
| RF-043 | Pagamento via PIX | P0 | ❌ |
| RF-044 | Pagamento via cartão de crédito | P1 | ❌ |
| RF-045 | Webhook de confirmação de pagamento | P1 | ❌ |
| RF-046 | Reembolso automático em caso de cancelamento | P2 | ❌ |
| RF-047 | Histórico de pagamentos do cliente | P2 | ❌ |
| RF-048 | Relatório de pagamentos para o dono | P2 | ❌ |
| RF-049 | Split de pagamento (comissão para barbeiro) | P3 | ❌ |
| RF-050 | Política de cancelamento e reembolso configurável | P2 | ❌ |

---

## 4.4 Módulo: Painel Administrativo

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-051 | Dashboard de faturamento | P1 | ✅ |
| RF-052 | Dashboard de agendamentos (hoje, semana, mês) | P1 | ✅ |
| RF-053 | Dashboard de ocupação por profissional | P2 | ❌ |
| RF-054 | CRUD de serviços (nome, preço, duração, descrição, foto) | P0 | ✅ |
| RF-055 | CRUD de profissionais (nome, foto, bio, especialidades) | P0 | ✅ |
| RF-056 | Configuração de horários de funcionamento | P0 | ✅ |
| RF-057 | Configuração de horários por profissional | P1 | ✅ |
| RF-058 | Visualização de agenda (calendário) | P0 | ✅ |
| RF-059 | Filtro de agenda por profissional | P0 | ✅ |
| RF-060 | Registro manual de agendamento (walk-in) | P1 | ✅ |
| RF-061 | Check-in de cliente (marcar como presente) | P1 | ❌ |
| RF-062 | Marcar como "não compareceu" (no-show) | P1 | ❌ |
| RF-063 | Marcar como concluído | P1 | ❌ |
| RF-064 | Histórico de agendamentos do cliente | P2 | ❌ |
| RF-065 | Cadastro manual de cliente | P2 | ❌ |
| RF-066 | Busca de clientes (nome, telefone, e-mail) | P2 | ❌ |

---

## 4.5 Módulo: Personalização do Site (White-Label)

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-067 | Upload de logo | P0 | ✅ |
| RF-068 | Upload de banner principal | P1 | ✅ |
| RF-069 | Upload de fotos da galeria | P2 | ❌ |
| RF-070 | Alteração de cores primárias/secundárias | P1 | ✅ |
| RF-071 | Alteração de fontes | P2 | ❌ |
| RF-072 | Alteração de textos institucionais | P2 | ❌ |
| RF-073 | Configuração de redes sociais | P1 | ❌ |
| RF-074 | Configuração de SEO (título, descrição) | P2 | ❌ |
| RF-075 | Configuração de endereço e mapa | P1 | ❌ |
| RF-076 | Configuração de telefone e WhatsApp | P0 | ✅ |
| RF-077 | Preview em tempo real das alterações | P1 | ❌ |
| RF-078 | Templates de site (múltiplos layouts) | P3 | ❌ |
| RF-079 | CSS customizado (avançado) | P3 | ❌ |
| RF-080 | Página de links estilo Linktree | P3 | ❌ |

---

## 4.6 Módulo: Notificações

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-081 | Confirmação de agendamento por WhatsApp | P0 | ✅ |
| RF-082 | Confirmação de agendamento por e-mail | P2 | ❌ |
| RF-083 | Lembrete 24h antes por WhatsApp | P1 | ✅ |
| RF-084 | Lembrete 1h antes por WhatsApp | P2 | ❌ |
| RF-085 | Notificação de cancelamento | P1 | ❌ |
| RF-086 | Notificação de reagendamento | P2 | ❌ |
| RF-087 | Notificação para o barbeiro (novo agendamento) | P1 | ✅ |
| RF-088 | Notificação para o barbeiro (cancelamento) | P2 | ❌ |
| RF-089 | Campanha de retorno automático ("Faz 30 dias...") | P3 | ❌ |
| RF-090 | Notificação de aniversário com desconto | P3 | ❌ |
| RF-091 | Templates de mensagem personalizáveis | P2 | ❌ |
| RF-092 | Notificações push (PWA) | P3 | ❌ |
| RF-093 | Central de preferências (cliente escolhe canais) | P3 | ❌ |

---

## 4.7 Módulo: CRM e Fidelização

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-094 | Ficha do cliente (histórico de cortes, preferências) | P2 | ❌ |
| RF-095 | Última visita e frequência | P2 | ❌ |
| RF-096 | Ticket médio do cliente | P3 | ❌ |
| RF-097 | Segmentação de clientes (frequentes, inativos, novos) | P3 | ❌ |
| RF-098 | Programa de fidelidade (a cada X cortes, desconto) | P3 | ❌ |
| RF-099 | Indicação (cliente indica e ganha desconto) | P3 | ❌ |
| RF-100 | Anotações internas sobre o cliente (visível só para equipe) | P2 | ❌ |
| RF-101 | Preferências do cliente (barbeiro favorito, serviços) | P3 | ❌ |
| RF-102 | Registro de alergias/observações importantes | P3 | ❌ |

---

## 4.8 Módulo: Relatórios

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-103 | Relatório de faturamento (diário, semanal, mensal) | P1 | ✅ |
| RF-104 | Relatório por profissional | P2 | ❌ |
| RF-105 | Relatório por serviço | P2 | ❌ |
| RF-106 | Relatório de ocupação (taxa de slots preenchidos) | P2 | ❌ |
| RF-107 | Relatório de no-show (taxa de faltas) | P2 | ❌ |
| RF-108 | Relatório de retenção (clientes que voltam) | P3 | ❌ |
| RF-109 | Relatório de ticket médio | P3 | ❌ |
| RF-110 | Relatório de origem (Instagram, Google, direto) | P3 | ❌ |
| RF-111 | Exportação de relatórios (PDF, Excel) | P2 | ❌ |
| RF-112 | Dashboard customizável (widgets arrastáveis) | P3 | ❌ |

---

## 4.9 Módulo: Promoções e Marketing

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-113 | Criação de cupom de desconto (% ou valor fixo) | P2 | ❌ |
| RF-114 | Validade de cupom (data ou quantidade) | P2 | ❌ |
| RF-115 | Promoção em serviço específico | P2 | ❌ |
| RF-116 | Promoção em horário específico (happy hour) | P3 | ❌ |
| RF-117 | Promoção para primeira visita | P2 | ❌ |
| RF-118 | Promoção para aniversariantes | P3 | ❌ |
| RF-119 | Link de agendamento com desconto aplicado | P2 | ❌ |
| RF-120 | Pixel de conversão (Facebook/Google Ads) | P3 | ❌ |

---

## 4.10 Módulo: Multi-Unidade (Franquias/Redes)

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-121 | Gerenciamento de múltiplas unidades | P3 | ❌ |
| RF-122 | Visão consolidada de todas as unidades | P3 | ❌ |
| RF-123 | Relatórios consolidados | P3 | ❌ |
| RF-124 | Profissional vinculado a unidade(s) | P3 | ❌ |
| RF-125 | Agendamento por unidade (cliente escolhe a mais próxima) | P3 | ❌ |

---

## 4.11 Módulo: Super Admin (Plataforma)

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-126 | Dashboard de métricas da plataforma | P1 | ✅ |
| RF-127 | CRUD de tenants | P1 | ✅ |
| RF-128 | Ativar/suspender tenant | P1 | ✅ |
| RF-129 | Gerenciar planos de assinatura | P1 | ✅ |
| RF-130 | Visualizar faturamento por tenant | P1 | ✅ |
| RF-131 | Visualizar logs de auditoria | P1 | ✅ |
| RF-132 | Impersonar tenant (login como admin do tenant) | P2 | ❌ |
| RF-133 | Feature flags (liberar features por tenant ou % de tenants) | P2 | ❌ |
| RF-134 | Enviar comunicado para todos os tenants | P2 | ❌ |
| RF-135 | Gerenciar templates globais (e-mails, notificações) | P2 | ❌ |
| RF-136 | Configurar integrações globais (gateways de pagamento) | P1 | ✅ |
| RF-137 | Logs de acesso e segurança | P1 | ✅ |
| RF-138 | Métricas de performance do sistema | P2 | ❌ |

---

## 4.12 Módulo: Autenticação e Conta

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-139 | Login com e-mail e senha | P0 | ✅ |
| RF-140 | Login com Google | P2 | ❌ |
| RF-141 | Recuperação de senha | P0 | ✅ |
| RF-142 | Confirmação de e-mail no cadastro | P1 | ❌ |
| RF-143 | 2FA (Two-Factor Authentication) | P2 | ❌ |
| RF-144 | Gerenciamento de sessões ativas | P2 | ❌ |
| RF-145 | Logout de todos os dispositivos | P2 | ❌ |
| RF-146 | Alteração de senha | P1 | ✅ |
| RF-147 | Convite para membro da equipe (com role) | P2 | ❌ |
| RF-148 | Definição de senha via link mágico | P2 | ❌ |

---

## 4.13 Funcionalidades Transversais

| ID | Funcionalidade | Prioridade | MVP |
|----|---------------|-----------|-----|
| RF-149 | Log de auditoria para todas ações sensíveis | P1 | ✅ |
| RF-150 | Exportação de dados do cliente (LGPD — portabilidade) | P2 | ❌ |
| RF-151 | Exclusão de dados do cliente (LGPD — direito ao esquecimento) | P2 | ❌ |
| RF-152 | Termos de uso e política de privacidade | P1 | ✅ |
| RF-153 | Consentimento de cookies (LGPD) | P1 | ❌ |
| RF-154 | Rate limiting por IP e por tenant | P1 | ✅ |
| RF-155 | Modo escuro no painel admin | P3 | ❌ |

---

> **Total de requisitos funcionais: 155**  
> **MVP: ~35 funcionalidades (P0 + P1 essenciais)**  
> **V1: ~70 funcionalidades**  
> **V2+: ~120 funcionalidades**
