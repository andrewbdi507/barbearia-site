# RELATÓRIO UAT — CLIENTE DA BARBEARIA

**Testador:** Lucas Ferreira, 29 anos, Cliente comum
**Conhecimento técnico:** Muito baixo
**Objetivo:** Marcar um corte de cabelo
**Data:** 27/07/2026

---

## ETAPA 1 — PRIMEIRA IMPRESSÃO

### O que vi
Abri o site. Apareceu "Barbearia" no topo com links: Início, Serviços, Equipe, Galeria, Agendar. No centro: ícone 🔧 e "Site em construção".

### Avaliação
| Item | Nota |
|------|------|
| Tempo de carregamento | Rápido (~2s) |
| Layout | Limpo, profissional |
| Cores | Neutras, agradáveis |
| Navegação | Clara, links visíveis |
| **Geral** | **3/10** — O site parece profissional mas está vazio. |

> "Parece um site de verdade, mas diz 'em construção'. Não confio ainda."

### Nota: 3/10

---

## ETAPA 2 — IDENTIDADE DA BARBEARIA

| Item | Visível? |
|------|----------|
| Logo | ❌ Não |
| Banner | ❌ Não |
| Nome | ⚠️ "Barbearia" (genérico) |
| Descrição | ❌ Não |
| Telefone | ❌ Não |
| WhatsApp | ❌ Não |
| Instagram | ❌ Não |
| Endereço | ❌ Não |
| Mapa | ❌ Não |
| Horário | ❌ Não |

**Avaliação:** Não tem informação nenhuma sobre a barbearia. Não sei onde fica, não sei o telefone, não sei nada.

---

## ETAPA 3 — TEMA

O site mostra apenas a tela "Site em construção", sem tema aplicado. O background é escuro (#111), texto em cinza claro.

**Nota: 1/10** — Não há tema visível para avaliar.

---

## ETAPA 4 — SERVIÇOS

Cliquei em "Serviços" no menu. A URL mudou para `/servicos`. A página continua mostrando "Site em construção".

❌ **Nenhum serviço visível.** Não sei o que a barbearia oferece, nem preços, nem duração.

---

## ETAPA 5 — BARBEIROS

Cliquei em "Equipe". URL mudou para `/equipe`. Continua "Site em construção".

❌ **Nenhum barbeiro visível.** Não sei quem trabalha lá.

---

## ETAPA 6 — GALERIA

Cliquei em "Galeria". URL mudou para `/galeria`. Continua "Site em construção".

❌ **Nenhuma foto.** Não sei como é o ambiente.

---

## ETAPA 7 — FAQ

Não encontrei link de FAQ na navegação.

❌ **FAQ inacessível.**

---

## ETAPA 8 — AGENDAR HORÁRIO

Cliquei em "Agendar". Continua "Site em construção".

❌ **Impossível agendar.** O fluxo está completamente bloqueado.

---

## ETAPA 9 — ALTERAÇÃO PELO DONO (Admin → Site)

**Mudei para o papel de João (dono).** Acessei o Admin em `agendaos-frontend.onrender.com`.

### O que tentei
1. Abri Aparência (/settings/theme)
2. Vi 5 temas: Urban, Luxury, Modern, Classic, Minimal
3. Tentei trocar de Minimal para Urban
4. Cliquei em "Salvar Alterações"

### Resultado
- O tema mudou no Admin ✅
- Voltei ao site público e atualizei
- Site continua mostrando "Site em construção" ❌

| Alteração | Refletiu no Site? | Tempo | Observações |
|-----------|-------------------|-------|-------------|
| Tema (Urban) | ❌ Não | — | Site sem dados de tenant |

---

## ETAPA 10 — TESTAR TODOS OS TEMAS

❌ Bloqueado — o site público não carrega dados de tenant. Sem dados, nenhum tema renderiza.

---

## ETAPA 11 — BRANDING

Tentei alterar logo, banner, telefone, WhatsApp no Admin:
- Abri Aparência → tem campos de upload para logo e banner ✅
- Campos de telefone, WhatsApp, endereço: **não encontrados** ❌
- A descrição da barbearia: **não encontrada** ❌

| Alteração | Refletiu no Site? | Observações |
|-----------|-------------------|-------------|
| Logo | ❌ | Upload de arquivo pede para selecionar |
| Banner | ❌ | Idem |
| Telefone | ❌ | Campo não existe na UI |
| WhatsApp | ❌ | Campo não existe na UI |
| Endereço | ❌ | Campo não existe na UI |

---

## ETAPA 12 — SERVIÇOS (Admin)

Tentei criar serviço "Corte Premium R$60" no Admin:
- Abri Serviços → mostra "0 serviços — Cadastre via API"

❌ **Impossível cadastrar serviço pela interface.** A mensagem "Cadastre via API" não faz sentido para um dono de barbearia.

---

## ETAPA 13 — FUNCIONÁRIOS (Admin)

- Abri Equipe → 3 barbeiros visíveis (Marcos, Ricardo, Lucas)
- ❌ Não achei botão "Adicionar" ou "Novo profissional"

---

## ETAPA 14 — SEO

### Verificado via API:

| Elemento | Status |
|----------|--------|
| OpenAPI | ✅ 3.1.0, "BarbershopOS" |
| JSON-LD | ✅ Gerado pelo backend (schema.org LocalBusiness) |
| Sitemap | ✅ XML gerado dinamicamente |
| Title dinâmico | ✅ Backend retorna SEO metadata |
| OG tags | ✅ Backend gera OpenGraph |
| Twitter Cards | ✅ Backend gera |

⚠️ **Porém**, como o site está "em construção", o `<title>` é "Studio 27 Barbearia" (hardcoded no index.html), não o nome real do tenant.

---

## ETAPA 15 — RESPONSIVIDADE (Admin)

Testado no Admin (viewport 1280x960):

| Elemento | Status |
|----------|--------|
| Sidebar | ✅ Visível, links clicáveis |
| Breadcrumb | ✅ Funcional |
| Header | ✅ Busca, tema, notificações, perfil |
| Dashboard | ✅ Cards responsivos |
| Planos | ✅ Grid de 4 cards |
| Temas | ✅ Grid de 5 cards |

⚠️ Não testado em viewports menores (mobile/tablet).

---

## ETAPA 16 — PERFORMANCE

Métricas aproximadas (Network tab):

| Métrica | Valor |
|---------|-------|
| TTFB (API) | ~200-400ms |
| Bundle Admin | ~500KB (com chunks) |
| Bundle Site | ~300KB (com chunks) |
| React.lazy | ✅ Funcional |
| Code splitting | ✅ Chunks separados |

---

## ETAPA 17 — ACESSIBILIDADE

⚠️ Não testado profundamente.

| Elemento | Status |
|----------|--------|
| Alt em imagens | ✅ (admin) |
| Labels em inputs | ✅ |
| Tab navigation | ⚠️ Não testado |
| ARIA | ⚠️ Não testado |
| Contraste | ⚠️ Não medido |

---

## ETAPA 18 — EXPERIÊNCIA DO CLIENTE

### Respostas do Lucas:

1. **Eu conseguiria marcar horário sozinho?** Não. O site não tem serviços nem horários.

2. **Fiquei perdido?** Um pouco. O site parece profissional mas está vazio.

3. **Existe alguma tela confusa?** A tela "Site em construção" é clara — diz exatamente o que está acontecendo. Melhor que "Carregando..." infinito.

4. **Eu voltaria a usar?** Se tivesse serviços e horários, sim. O visual é bom.

5. **Eu indicaria este sistema?** Não no estado atual. Mas parece promissor.

6. **Nota: 2/10** — O site carrega e é bonito, mas não tem conteúdo.

---

## ETAPA 19 — SINCRONIZAÇÃO ADMIN ↔ SITE

| Alteração | Refletiu no Site? | Tempo | Observações |
|-----------|-------------------|-------|-------------|
| Tema | ❌ | — | Site sem dados de tenant |
| Logo | ❌ | — | Idem |
| Banner | ❌ | — | Idem |
| Serviços | ❌ | — | Não foi possível criar |
| Equipe | ❌ | — | Não foi possível adicionar |
| Horários | ❌ | — | Não testado |
| Contato | ❌ | — | Campos não disponíveis na UI |
| Galeria | ❌ | — | Não testado |
| FAQ | ❌ | — | Não testado |
| Redes sociais | ❌ | — | Não encontrado na UI |
| SEO | ⚠️ | — | Backend gera, frontend não renderiza |

**Conclusão:** A sincronização Admin → Site **não pode ser validada** porque o site público não carrega dados de tenant. O backend tem os dados, o frontend tem o código para exibi-los, mas a ponte (tenant no banco) está faltando.

---

## RESUMO DE PROBLEMAS

| # | Problema | Área | Gravidade |
|---|----------|------|-----------|
| C1 | Site público sem dados — "Site em construção" | Site | 🔴 CRÍTICO |
| C2 | Nenhum serviço visível para agendamento | Site | 🔴 CRÍTICO |
| C3 | Impossível cadastrar serviços pelo Admin — "Cadastre via API" | Admin | 🔴 CRÍTICO |
| C4 | Sem campos de contato (telefone, WhatsApp, endereço) na UI | Admin | 🔴 CRÍTICO |
| C5 | Sem botão "Adicionar funcionário" | Admin | 🟡 MÉDIA |
| C6 | Site não tem logo, banner, nem identidade visual | Site | 🟡 MÉDIA |
| C7 | Nome da barbearia é genérico ("Barbearia") | Site | 🟡 MÉDIA |
| C8 | FAQ inacessível pelo site | Site | 🟡 MÉDIA |
| C9 | URLs diretas do site retornam "Site em construção" | Site | 🟡 MÉDIA |
| C10 | Sincronização Admin→Site não validável | Geral | 🟡 MÉDIA |

---

## NOTA GERAL: 2/10

### Como cliente:
"Não consigo agendar. O site é bonito mas não tem nada dentro."

### Como dono:
"Consigo ver dados, trocar tema, navegar. Mas não consigo cadastrar o essencial: serviços."

---

## VEREDITO FINAL

```
████████████████████████████████████████████████
█                                              █
█   ❌ NÃO APROVADO PARA CLIENTES REAIS        █
█                                              █
█   Um cliente não consegue agendar.           █
█   Um dono não consegue cadastrar serviços.   █
█   O site não tem identidade da barbearia.     █
█                                              █
█   NOTA: 2/10                                 █
████████████████████████████████████████████████
```

### O que falta para aprovação:

1. **Criar tenant "demo" com dados reais** (serviços, equipe, contato)
2. **Formulário de criação de serviço** no Admin (remover "Cadastre via API")
3. **Formulário de dados cadastrais** (nome, telefone, WhatsApp, endereço)
4. **Botão "Adicionar funcionário"** na tela de Equipe

---

**Assinatura do testador:**

*Lucas Ferreira*
*Cliente — tentando agendar um corte*
