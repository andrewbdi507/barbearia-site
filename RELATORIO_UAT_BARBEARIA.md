# RELATÓRIO UAT — BLACK HOUSE BARBEARIA

**Testador:** João Silva, 35 anos, Dono da Black House Barbearia
**Conhecimento técnico:** Baixo (usuário típico de SaaS)
**Data:** 27/07/2026 — **SEGUNDA TENTATIVA (pós-correções)**
**Horário:** 12:40 - 13:10

---

## EXPERIÊNCIA GERAL

| Categoria | Nota (0-10) |
|-----------|-------------|
| Primeiro acesso | 4 |
| Configuração da barbearia | 6 |
| Serviços | 2 |
| Funcionários | 7 |
| Agenda | 5 |
| Site público | 2 |
| Agendamento | 3 |
| Uso diário | 6 |
| Configurações | 8 |
| **GERAL** | **5/10** |

---

## ETAPA 1 — PRIMEIRO ACESSO

### ✅ Funcionou
- Tela de login carregou rápido
- Login funcionou — entrei no sistema!

### ❌ Problemas

| # | Problema | Gravidade |
|---|----------|-----------|
| P1 | **Não existe botão "Criar conta"** — como crio meu acesso? | 🔴 CRÍTICO |
| P2 | **Nenhum onboarding** — sem tour, checklist, ou boas-vindas personalizadas | 🔴 CRÍTICO |
| P3 | Dashboard existe e tem dados, mas não é MEU negócio — aparece "Carlos Oliveira", "Barbearia Teste" | 🟡 MÉDIA |

### Nota: **4/10** — Entrei, mas não sei de quem é essa barbearia.

---

## ETAPA 2 — CONFIGURAR MINHA BARBEARIA

### O que funciona
- Abri Configurações → tem seções: Empresa, Usuários, Notificações, Segurança
- Abri Aparência → **incrível!** Consigo trocar tema, cores, fontes, logo, banner, favicon. Preview em tempo real!

### ❌ Problemas

| # | Problema | Gravidade |
|---|----------|-----------|
| P4 | Não achei onde mudar o nome da barbearia de "Barbearia Teste" para "Black House Barbearia" | 🟡 MÉDIA |
| P5 | Não achei onde colocar endereço, telefone, WhatsApp | 🟡 MÉDIA |
| P6 | Upload de logo/banner pede para escolher arquivo, mas não testei se funciona | 🟢 BAIXA |

### Nota: **6/10** — Achei a parte visual, mas não a parte de dados cadastrais.

---

## ETAPA 3 — CONFIGURAR SERVIÇOS

### O que aconteceu
Abri "Serviços" e vi: **"0 serviços — Nenhum serviço. Cadastre via API."**

### ❌ Problema

| # | Problema | Gravidade |
|---|----------|-----------|
| P7 | Tela de Serviços está vazia e diz "Cadastre via API" — **eu não sei o que é API!** | 🔴 CRÍTICO |

### Nota: **2/10** — Isso trava completamente minha operação.

---

## ETAPA 4 — ADICIONAR FUNCIONÁRIOS

### O que funciona
- Abri "Equipe" → vejo 3 barbeiros: **Marcos Silva, Ricardo Santos, Lucas Oliveira**
- Cada um tem foto (iniciais), cargo "Barbeiro", especialidades "Barba" e "Corte"
- Dá para ver quem é quem rapidamente

### ❌ Problemas

| # | Problema | Gravidade |
|---|----------|-----------|
| P8 | Não achei botão "Adicionar funcionário" ou "Novo profissional" | 🟡 MÉDIA |
| P9 | Os barbeiros que aparecem não são os meus (Carlos Souza, Pedro Oliveira) | 🟡 MÉDIA |

### Nota: **7/10** — Consigo ver a equipe, mas não sei como cadastrar os meus.

---

## ETAPA 5 — CONFIGURAR AGENDA

### O que funciona
- Abri "Agenda" → vejo visualização Hoje/Semana/Mês
- Mostra "Grid de agenda multi-profissional (em breve)"

### ❌ Problema

| # | Problema | Gravidade |
|---|----------|-----------|
| P10 | Agenda mostra placeholder "em breve" — não consigo configurar horários dos barbeiros | 🟡 MÉDIA |

### Nota: **5/10** — Promissor, mas não funcional ainda.

---

## ETAPA 6 — VER MEU SITE

### O que aconteceu
Abri o site público. Continua mostrando **"Carregando..."** (o rebuild do frontend estático ainda não concluiu no Render).

### Nota: **2/10** — Sem site, sem clientes.

---

## ETAPA 7 — SIMULAR CLIENTE (AGENDAMENTO)

### ❌ Não consegui
Serviços está vazio ("Cadastre via API"). Não tenho como criar agendamento sem serviços cadastrados.

### Nota: **3/10**

---

## ETAPA 8 — DIA REAL

### O que funciona
- Dashboard mostra agenda do dia: 09:00 João S. (Corte), 09:30 Pedro L. (Barba), 10:00 Livre, 10:30 Ana C. (Combo)
- Dá pra ver rapidamente quem está agendado

### ❌ Problema
Não consegui clicar nos agendamentos para mudar status ou adicionar observação.

### Nota: **6/10** — Visão geral boa, mas não interativa.

---

## ETAPA 9 — CONFIGURAÇÕES DO NEGÓCIO

### Pontos positivos
- **Planos**: tela LINDA! 4 planos (Starter R$49, Pro R$99, Premium R$199, Enterprise sob consulta). Meu plano atual é Premium.
- **Aparência/Tema**: 5 temas com preview. Muito intuitivo!
- **Financeiro**: receita R$4.580, 127 pagamentos, ticket R$36. Dados reais!

### Pontos confusos
- "IA & Agentes" — não faço ideia do que seja
- "Galeria" e "Avaliações" — não testei

### Nota: **8/10** — Muito bom! A parte de planos e aparência é excelente.

---

## ETAPA 10 — VISÃO DO DONO

### 1. Eu conseguiria usar sozinho?
**Mais ou menos.** Consigo navegar, ver dados, trocar tema. Mas não consigo cadastrar serviços (minha principal necessidade). Se tivesse serviços, conseguiria operar.

### 2. Eu precisaria chamar suporte?
**Sim, para o cadastro inicial.** Depois de configurado, acho que usaria sozinho.

### 3. Qual tela mais confunde?
**Serviços** — "Cadastre via API" não faz sentido para mim. E **IA & Agentes** — não sei o que é.

### 4. Qual funcionalidade mais importante?
**Agenda + Serviços.** Sem serviços cadastrados, nada funciona.

### 5. O que impediria eu pagar R$99/mês?
- Não conseguir cadastrar meus serviços sozinho
- O site público não carregar para meus clientes
- Não ter botão "Criar conta" na primeira visita

### 6. Qual melhoria aumentaria o valor percebido?
- Um **assistente de configuração inicial**: "Vamos configurar sua barbearia em 5 minutos"
- Poder **cadastrar serviços com formulário** (não API)
- Ver o **site público funcionando** com minha marca

---

## RESUMO DE PROBLEMAS (ATUALIZADO)

| # | Problema | Área | Gravidade | Status |
|---|----------|------|-----------|--------|
| P1 | Sem botão "Criar conta" | Login | 🔴 CRÍTICO | Persiste |
| P2 | Sem onboarding/tutorial | Geral | 🔴 CRÍTICO | Persiste |
| P7 | Serviços: "Cadastre via API" — inutilizável para leigo | Serviços | 🔴 CRÍTICO | **NOVO** |
| P4 | Não achei onde mudar nome da barbearia | Config | 🟡 MÉDIA | **NOVO** |
| P5 | Não achei campos de endereço/telefone/WhatsApp | Config | 🟡 MÉDIA | **NOVO** |
| P8 | Sem botão "Adicionar funcionário" | Equipe | 🟡 MÉDIA | **NOVO** |
| P10 | Agenda: placeholder "em breve" | Agenda | 🟡 MÉDIA | **NOVO** |
| P3 | Dados não são da minha barbearia | Geral | 🟡 MÉDIA | Persiste |
| P9 | Barbeiros não são os meus | Equipe | 🟡 MÉDIA | **NOVO** |
| P11 | Site público não carrega | Site | 🔴 CRÍTICO | Aguardando rebuild |

## COMPARATIVO: ANTES × DEPOIS

| Indicador | 1ª tentativa (12:00) | 2ª tentativa (12:40) |
|-----------|----------------------|----------------------|
| Dashboard | ❌ Vazio + erro #306 | ✅ KPIs, bookings, equipe |
| Menu lateral | ❌ Travado | ✅ 10/10 páginas navegam |
| React errors | ❌ #306 | ✅ Zero |
| Planos | ❌ Inacessível | ✅ 4 planos com preços |
| Temas | ❌ Inacessível | ✅ 5 temas com preview |
| Equipe | ❌ Inacessível | ✅ 3 barbeiros visíveis |
| Clientes | ❌ Inacessível | ✅ 145 clientes |
| Financeiro | ❌ Inacessível | ✅ Receita, pagamentos |

---

## APROVAÇÃO

```
████████████████████████████████████████████████
█                                              █
█   ⚠️ PRECISA AJUSTES (mas melhorou muito)    █
█                                              █
█   3 bugs críticos restantes:                 █
█   1. Serviços inacessível para leigos         █
█   2. Sem onboarding                          █
█   3. Sem botão Criar conta                   █
█                                              █
█   NOTA: 5/10 (vs 0.5/10 na 1ª tentativa)     █
████████████████████████████████████████████████
```

---

**Assinatura do testador:**

*João Silva*
*Dono — Black House Barbearia*

*"Melhorou BASTANTE da última vez. Consigo ver que tem potencial. Se eu conseguisse cadastrar meus serviços e ver meu site no ar, fecharia o plano Pro."*
