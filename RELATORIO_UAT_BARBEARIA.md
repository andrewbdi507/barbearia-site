# RELATÓRIO UAT — BLACK HOUSE BARBEARIA

**Testador:** João Silva, 35 anos, Dono da Black House Barbearia
**Conhecimento técnico:** Baixo (usuário típico de SaaS)
**Data:** 27/07/2026
**Horário:** 12:00 - 12:30

---

## EXPERIÊNCIA GERAL

| Categoria | Nota (0-10) |
|-----------|-------------|
| Primeiro acesso | 2 |
| Configuração da barbearia | 0 |
| Serviços | 0 |
| Funcionários | 0 |
| Agenda | 0 |
| Site público | 3 |
| Agendamento | 0 |
| Uso diário | 0 |
| Configurações | 0 |
| **GERAL** | **0.5** |

---

## ETAPA 1 — PRIMEIRO ACESSO

### O que fiz
Acessei o link que me enviaram. Vi uma tela de login limpa com os campos Email e Senha.

### ✅ Funcionou
- Tela de login carregou rápido
- Placeholder "admin@barbearia.com" ajudou a entender o formato
- Login funcionou com minhas credenciais

### ❌ Problemas

| # | Problema | Gravidade |
|---|----------|-----------|
| P1 | **Não existe botão "Criar conta" ou "Registrar"** — como eu criaria meu acesso? | 🔴 CRÍTICO |
| P2 | **Dashboard completamente vazio** após login. Nenhum KPI, nenhuma instrução, nenhum card. Só o menu lateral e um espaço em branco no centro. | 🔴 CRÍTICO |
| P3 | **Nenhum onboarding** — não tem tour guiado, checklist de configuração, ou mensagem de boas-vindas. | 🔴 CRÍTICO |
| P4 | **Menu lateral não responde** — cliquei em "Configurações", "Agenda", "Equipe"... nada acontece. O sistema travou. | 🔴 CRÍTICO |
| P5 | **Erro técnico visível** no console: "Minified React error #306" | 🔴 CRÍTICO |
| P6 | Se eu digitar o endereço direto (ex: /agenda) o site mostra "Not Found". Não posso usar favoritos. | 🔴 CRÍTICO |

### O que pensei
> "Loguei. E agora? Tem um menu aqui do lado, cliquei em Configurações e nada aconteceu. O sistema quebrou? Vou ter que ligar pro suporte..."

### Nota: **2/10**

---

## ETAPA 2 — CONFIGURAR MINHA BARBEARIA

### O que tentei fazer
Queria colocar o nome "Black House Barbearia", subir minha logo, banner, telefone e horários.

### ❌ Não consegui fazer NADA
O painel travou após o login. Nenhum link do menu funciona. O espaço central (onde imagino que deveria aparecer o conteúdo) está completamente vazio.

### Nota: **0/10**

---

## ETAPA 3 — CONFIGURAR SERVIÇOS

### O que tentei fazer
Criar Corte Masculino (R$40 / 30min), Barba (R$30 / 20min), Combo Corte+Barba (R$60 / 50min).

### ❌ Não consegui
Painel travado. Impossível acessar a seção de Serviços.

### Nota: **0/10**

---

## ETAPA 4 — ADICIONAR FUNCIONÁRIOS

### O que tentei fazer
Cadastrar Carlos Souza e Pedro Oliveira, barbeiros.

### ❌ Não consegui
Painel travado.

### Nota: **0/10**

---

## ETAPA 5 — CONFIGURAR AGENDA

### ❌ Não consegui
Painel travado.

### Nota: **0/10**

---

## ETAPA 6 — VER MEU SITE

### O que fiz
Abri o link do site público que me passaram.

### O que vi
- ✅ Aparece o nome "Barbearia" no topo
- ✅ Tem links: Início, Serviços, Equipe, Galeria, Agendar
- ✅ Botão "Agendar" visível

### ❌ Problemas

| # | Problema | Gravidade |
|---|----------|-----------|
| P7 | O conteúdo principal mostra **"Carregando..."** e nunca termina de carregar. | 🔴 CRÍTICO |
| P8 | O nome da barbearia aparece como "Barbearia" genérico, não "Black House Barbearia". | 🟡 MÉDIA |
| P9 | Nenhum serviço, funcionário, ou foto aparece. | 🟡 MÉDIA |
| P10 | Não tem telefone, WhatsApp, nem endereço visível. | 🟡 MÉDIA |

### O que pensei
> "Mostraria esse link pros meus clientes? Nem pensar. Tá escrito 'Carregando...' e não tem nada."

### Nota: **3/10**

---

## ETAPA 7 — SIMULAR CLIENTE (AGENDAMENTO)

### ❌ Não consegui
Site público está em "Carregando...", sem serviços visíveis para agendar. Painel admin travado.

### Nota: **0/10**

---

## ETAPA 8 — DIA REAL (CHECK-IN, STATUS)

### ❌ Não consegui
Sem acesso ao painel.

### Nota: **0/10**

---

## ETAPA 9 — CONFIGURAÇÕES DO NEGÓCIO

### ❌ Não consegui
Link de Configurações no menu não responde.

### Nota: **0/10**

---

## ETAPA 10 — VISÃO DO DONO

### 1. Eu conseguiria usar sozinho?
**Não.** O sistema quebrou logo após o login. Não consegui fazer nada além de logar.

### 2. Eu precisaria chamar suporte?
**Sim, imediatamente.** Ligaria no primeiro minuto após o login.

### 3. Qual tela mais confunde?
**O Dashboard vazio.** Entrei, vi um espaço em branco enorme, cliquei nas coisas e nada aconteceu. Não sei se é bug, se está carregando, ou se eu fiz algo errado.

### 4. Qual funcionalidade mais importante?
**Agenda** — é o motivo pelo qual contratei o sistema. Não consegui nem ver a tela.

### 5. O que impediria eu pagar R$99/mês?
- Sistema travou no primeiro uso
- Não tem onboarding
- Site público não carrega
- Não consigo configurar nada sozinho

### 6. Qual melhoria aumentaria o valor percebido?
- Um tour guiado na primeira vez
- Checklist: "① Configure sua barbearia → ② Adicione serviços → ③ Cadastre funcionários → ④ Abra sua agenda"
- Poder ver o site público funcionando em 5 minutos

---

## RESUMO DE PROBLEMAS

| # | Problema | Área | Gravidade |
|---|----------|------|-----------|
| P1 | Sem botão Registrar/Criar conta | Login | 🔴 CRÍTICO |
| P2 | Dashboard completamente vazio | Dashboard | 🔴 CRÍTICO |
| P3 | Sem onboarding/tutorial | Geral | 🔴 CRÍTICO |
| P4 | Menu lateral não responde a cliques | Admin | 🔴 CRÍTICO |
| P5 | React Error #306 no console | Admin | 🔴 CRÍTICO |
| P6 | URLs diretas retornam 404 (sem SPA fallback) | Admin | 🔴 CRÍTICO |
| P7 | Site público mostra "Carregando..." infinito | Site | 🔴 CRÍTICO |
| P8 | Nome da barbearia não personalizado | Site | 🟡 MÉDIA |
| P9 | Sem dados (serviços, equipe, fotos) no site | Site | 🟡 MÉDIA |
| P10 | Sem contato (telefone, WhatsApp, endereço) | Site | 🟡 MÉDIA |

---

## CAUSA PROVÁVEL DOS PROBLEMAS CRÍTICOS

| # | Causa Técnica |
|---|---------------|
| P4, P5 | `React.lazy()` implementado no commit `89c5ee9` — os componentes lazy não estão exportando corretamente (default vs named export). O erro #306 "React.Children.only" indica que o AdminLayout/Suspense está recebendo children inválidos. |
| P7 | `ThemeProvider` faz fetch para `/api/v1/site?subdomain=demo` — o subdomínio "demo" não existe no banco (404). O catch silencioso mantém `siteData=null` mas `isLoading` fica `true` porque o fallback do localStorage também falha. |
| P6 | O Render static site não tem regra de rewrite. Todas as URLs que não são `/` ou `/index.html` retornam 404. Precisa configurar `rewrite.rules` no render.yaml. |
| P2 | O componente `DashboardPage` renderiza mas seu conteúdo (KPIs, gráficos) depende de chamadas API — se falharem silenciosamente, a tela fica vazia. |
| P3 | Nunca foi implementado — é uma feature ausente, não um bug. |
| P1 | O fluxo de registro existe via API (`POST /api/v1/auth/register`) mas não tem link na UI de login. |

---

## APROVAÇÃO

```
████████████████████████████████████████████████
█                                              █
█   ❌ PRECISA AJUSTES                         █
█                                              █
█   O sistema NÃO está pronto para clientes    █
█   reais. Um dono de barbearia não consegue   █
█   passar da tela de login sem ajuda.         █
█                                              █
████████████████████████████████████████████████
```

### Correções mínimas para aprovação:

1. **Reverter React.lazy no Admin** — os componentes não estão exportando corretamente
2. **Criar tenant "demo"** no banco para o site público funcionar
3. **Adicionar SPA fallback** no Render static site (todas rotas → index.html)
4. **Adicionar botão "Criar conta"** na tela de login
5. **Adicionar conteúdo mínimo ao Dashboard** — mesmo que seja "Bem-vindo! Comece configurando sua barbearia."

---

**Assinatura do testador:**

*João Silva*
*Dono — Black House Barbearia*
