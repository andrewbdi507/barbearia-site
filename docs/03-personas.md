# 03 — Personas

---

## 3.1 Persona 1 — Cliente Final (João, 28 anos)

### Perfil
- Homem, 25–40 anos, classe B/C
- Trabalha durante a semana (horário comercial)
- Usa Instagram e WhatsApp diariamente
- Valoriza praticidade e agilidade
- Não quer perder tempo ligando ou esperando

### Dores
- "Não sei se o barbeiro está disponível"
- "Tenho que mandar mensagem e esperar resposta"
- "Chego lá e tenho que esperar"
- "Não sei quanto custa o corte antes de ir"

### Jornada Ideal
1. Vê anúncio/post no Instagram
2. Clica no link da bio
3. Cai no site da barbearia (personalizado, profissional)
4. Vê serviços, preços e equipe com fotos
5. Escolhe barbeiro → serviço → horário
6. Paga sinal de R$ 10 via PIX
7. Recebe confirmação imediata no WhatsApp
8. Recebe lembrete 1h antes
9. É atendido no horário
10. Recebe link de avaliação
11. 30 dias depois recebe "Faz 1 mês, que tal voltar?"

**Tempo total: < 2 minutos.**

---

## 3.2 Persona 2 — Barbeiro / Profissional (Marcos, 32 anos)

### Perfil
- Homem, 22–45 anos
- Trabalha com agenda lotada
- Usa celular o dia todo
- Usa WhatsApp para agendamento pessoal
- Tem dificuldade de organizar horários

### Dores
- "Esqueço agendamentos"
- "Cliente marca e não vem"
- "Não sei quanto faturo por mês"
- "Perco tempo respondendo WhatsApp fora do expediente"
- "Não tenho como mostrar meu trabalho online"

### Funcionalidades Essenciais
- Ver agenda do dia ao abrir o app
- Receber notificações de novos agendamentos
- Ver histórico do cliente (cortes anteriores, preferências)
- Bloquear horários de almoço/folga
- Marcar cliente como "não compareceu"
- Ver quanto faturou no dia/semana/mês
- Ter perfil público com fotos e avaliações

---

## 3.3 Persona 3 — Recepcionista (Ana, 24 anos)

### Perfil
- Mulher, 20–35 anos
- Gerencia múltiplos profissionais
- Atende telefone, WhatsApp, presencial
- Faz agendamentos para os barbeiros
- Lida com remarcações e cancelamentos

### Dores
- "Perco agendamentos no meio da bagunça"
- "Cliente liga e não sei a agenda do barbeiro"
- "Tenho que ligar confirmando um por um"
- "Não sei quem já pagou ou não"

### Funcionalidades Essenciais
- Visão de agenda de todos os profissionais simultaneamente
- Agendar para qualquer profissional
- Reagendar/cancelar com um clique
- Ver status de pagamento
- Check-in do cliente quando chega
- Fila de espera automática
- Lista de clientes com busca rápida

---

## 3.4 Persona 4 — Gerente / Dono (Carlos, 38 anos)

### Perfil
- Homem, 30–50 anos
- Dono de 1–3 barbearias
- Não é técnico (não sabe programar)
- Quer controle total do negócio
- Toma decisões baseadas em números

### Dores
- "Não sei quanto faturo direito"
- "Não sei qual barbeiro vende mais"
- "Não sei qual serviço dá mais lucro"
- "Quero mudar o site, mas dependo de programador"
- "Não sei quantos clientes voltam"
- "Não consigo fazer promoções segmentadas"

### Funcionalidades Essenciais
- Dashboard de faturamento (diário, semanal, mensal)
- Relatório por profissional (ticket médio, ocupação, avaliação)
- Relatório por serviço (mais vendidos, margem)
- Taxa de retorno de clientes
- Personalizar o site (logo, banner, fotos, cores, textos)
- Criar promoções e cupons
- Gerenciar equipe (adicionar, remover, comissões)
- Exportar relatórios (PDF, Excel)
- Múltiplas unidades (se tiver mais de uma barbearia)

---

## 3.5 Persona 5 — Administrador do Sistema (Super Admin)

### Perfil
- O próprio desenvolvedor / CTO (você)
- Única pessoa com acesso ao sistema como um todo
- Gerencia tenants, planos, cobranças
- Monitora saúde da plataforma

### Funcionalidades Essenciais
- Dashboard global (tenants ativos, MRR, churn, novos)
- Gerenciar tenants (criar, suspender, excluir)
- Gerenciar planos e assinaturas
- Visualizar logs de auditoria
- Monitorar saúde do sistema (métricas, alertas)
- Gerenciar templates de e-mail globais
- Configurar feature flags
- Impersonar tenant (para suporte)

---

## 3.6 Tabela de Permissões (RBAC)

| Funcionalidade | Cliente | Barbeiro | Recepcionista | Gerente | Super Admin |
|---------------|---------|----------|---------------|---------|-------------|
| Agendar horário | ✅ | ✅ | ✅ | ✅ | — |
| Ver própria agenda | ✅ | ✅ | ✅ | ✅ | — |
| Ver todas as agendas | ❌ | ❌ | ✅ | ✅ | — |
| Gerenciar serviços | ❌ | ❌ | ❌ | ✅ | — |
| Gerenciar profissionais | ❌ | ❌ | ❌ | ✅ | — |
| Ver relatórios | ❌ | Parcial | ❌ | ✅ | ✅ |
| Personalizar site | ❌ | ❌ | ❌ | ✅ | — |
| Gerenciar assinatura | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gerenciar tenants | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver logs de auditoria | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 3.7 Mapa de Empatia (Cliente Final)

### O que PENSA e SENTE?
- "Quero cortar o cabelo rápido e sem stress"
- "Será que tem horário hoje?"
- "Tomara que não tenha fila"
- "Espero que o barbeiro seja bom"

### O que VÊ?
- Posts no Instagram de cortes bonitos
- Amigos com cortes legais marcando a barbearia
- Anúncios de barbearias concorrentes

### O que OUVE?
- "Corta lá, o cara é fera"
- "Tem que marcar, senão não consegue"
- "É caro, mas vale a pena"

### O que FALA e FAZ?
- Manda WhatsApp perguntando preço e horário
- Olha Instagram antes de decidir
- Pergunta para amigos onde cortam

### DORES
- Falta de transparência de preços
- Incerteza sobre disponibilidade
- Processo de agendamento demorado
- Medo de ser mal atendido

### GANHOS
- Agendamento rápido (2 min)
- Transparência total (preços, horários, equipe)
- Segurança de horário reservado
- Possibilidade de escolher o profissional
