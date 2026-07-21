# 14 — Guia de UX

> Princípios, padrões e heurísticas que guiam cada decisão de design.

---

## 14.1 Os 10 Mandamentos da Experiência

### 1. Mobile First, Sempre
Toda tela é projetada primeiro para uma tela de 375px de largura. Depois escala para tablet e desktop. Se não funciona no mobile, o design está errado.

### 2. Zero Fricção
Cada campo removido aumenta a conversão. Cada clique removido melhora a experiência. O agendamento deve ter no máximo 10 interações (toques/cliques) do início ao fim.

### 3. Óbvio > Inteligente
O usuário não lê manual. Não assiste tutorial. A interface deve ser autoexplicativa. Um botão "Agendar" é melhor que "Iniciar jornada de agendamento".

### 4. Feedback Imediato
Toda ação do usuário deve ter resposta visível em menos de 100ms. Botão pressionado → muda cor. Formulário enviado → loading. Pagamento confirmado → celebração visual.

### 5. Perdoar Erros
Desfazer é melhor que confirmar. O usuário deve poder voltar, cancelar, corrigir sem medo. Nenhuma ação é irreversível sem confirmação explícita.

### 6. Consistência Visual
O mesmo botão tem a mesma cor em todas as telas. O mesmo ícone significa a mesma coisa. A mesma posição tem a mesma função. Consistência gera confiança.

### 7. Hierarquia Clara
O mais importante é maior, mais colorido, mais acima. O secundário é menor, mais neutro, mais abaixo. O olho do usuário deve ser guiado, não confundido.

### 8. Pouca Digitação
Prefira seleção a digitação. Use autocomplete, sugestões, máscaras. O teclado virtual do celular é a pior interface do mundo. Evite-o.

### 9. Contexto Sempre Visível
O usuário nunca deve se perguntar "onde estou?" ou "o que está acontecendo?". Breadcrumbs, indicadores de progresso, títulos claros.

### 10. Encantar nos Detalhes
Uma microinteração bem feita, um texto amigável, uma animação sutil — são esses detalhes que transformam "funciona" em "incrível".

---

## 14.2 Heurísticas de Usabilidade (Nielsen)

| # | Heurística | Como Aplicamos |
|---|-----------|---------------|
| 1 | Visibilidade do status | Toast notifications, barra de progresso, indicador de passo |
| 2 | Correspondência com o mundo real | "Agendar" não "Criar booking"; ícones universais |
| 3 | Controle e liberdade | Botão "Voltar", "Cancelar", desfazer ações |
| 4 | Consistência e padrões | Design System, mesmos componentes em todo o sistema |
| 5 | Prevenção de erros | Validação em tempo real, slots indisponíveis não clicáveis |
| 6 | Reconhecer em vez de lembrar | Histórico visível, "Repetir último agendamento" |
| 7 | Flexibilidade e eficiência | Atalhos de teclado, "Agendar sem escolher barbeiro" |
| 8 | Design estético e minimalista | Só o essencial visível, hierarquia clara |
| 9 | Ajudar a reconhecer/diagnosticar erros | Mensagens claras: "E-mail inválido" não "Erro 400" |
| 10 | Ajuda e documentação | FAQ, tooltips, textos de ajuda inline |

---

## 14.3 Lei de Fitts Aplicada

- **Botões primários:** Grandes (≥48px altura), posicionados onde o polegar alcança naturalmente
- **CTA principal:** Bottom-center no mobile (alcance fácil do polegar)
- **Ações destrutivas:** Menores, requerem confirmação
- **Espaçamento entre botões:** ≥8px para evitar toques acidentais
- **Alvos de toque:** Mínimo 44×44px (recomendação Apple HIG) / 48×48px (recomendação Google Material)

---

## 14.4 Lei de Hick Aplicada

- **Máximo 5 opções** em qualquer lista de escolha (serviços, profissionais, horários)
- Se houver mais, agrupar por categoria ou usar busca
- **Opção padrão** sempre destacada ("Qualquer profissional" como primeira opção)
- **Grid de horários:** Máximo 4 colunas para decisão rápida

---

## 14.5 Carga Cognitiva

### Reduzimos carga cognitiva com:

- Progress indicator (sei em que passo estou)
- Resumo sempre visível durante o fluxo
- Preview em tempo real ao personalizar o site
- Validação inline (erro aparece ao lado do campo, não no topo)
- Mensagens curtas (máximo 2 linhas)
- Ícones + texto (reconhecimento mais rápido que só texto)

---

## 14.6 Design Patterns

### Progressive Disclosure
Mostrar apenas o essencial. Revelar complexidade sob demanda.
- Configurações avançadas em "expandir"
- Filtros de busca em dropdown colapsável
- Wizard com 5 passos simples em vez de 1 formulário gigante

### Recognition over Recall
- Histórico de barbeiros favoritos visível
- "Repetir último agendamento" com 1 clique
- Autocomplete de clientes na recepção
- Tags sugeridas na avaliação (não precisa pensar)

### Smart Defaults
- "Qualquer profissional" pré-selecionado
- Data: hoje pré-selecionado
- Serviço: último serviço usado (se recorrente)
- Pagamento: PIX (mais comum no Brasil)

---

## 14.7 Tratamento de Erros

### Níveis de Erro

| Nível | Exemplo | UX |
|-------|---------|-----|
| **Prevenido** | Dia passado não é clicável | Erro não acontece |
| **Validado inline** | E-mail inválido → borda vermelha + mensagem | Erro corrigido antes de enviar |
| **Recuperável** | Pagamento falhou → tente de novo | Solução oferecida |
| **Escalável** | Erro do servidor → tente novamente + suporte | Caminho de saída claro |

---

## 14.8 Performance Percebida

- **Skeleton screens** em vez de spinner (parece mais rápido)
- **Otimistic UI:** Marcar check-in visualmente antes da resposta do servidor
- **Prefetch:** Carregar dados da próxima tela provável
- **Background sync:** Agendamento concluído mesmo offline (PWA)
- **Lazy loading:** Imagens carregam conforme scroll

---

## 14.9 Métricas de UX

| Métrica | Alvo | Como Medir |
|---------|------|-----------|
| Time to Book | < 120s | Analytics (timestamp início → confirmação) |
| Booking Abandonment | < 30% | Funil de conversão |
| Error Rate (formulário) | < 5% | Validações falhas / tentativas |
| First Contentful Paint | < 1.5s | Lighthouse / Web Vitals |
| Largest Contentful Paint | < 2.5s | Lighthouse / Web Vitals |
| Cumulative Layout Shift | < 0.1 | Lighthouse / Web Vitals |
| NPS (cliente final) | ≥ 70 | Pesquisa pós-agendamento |
| NPS (dono) | ≥ 60 | Pesquisa trimestral |

---

> **Resumo:** UX não é sobre deixar bonito — é sobre fazer funcionar sem pensar. Cada decisão neste guia tem um propósito: reduzir o esforço do usuário. Menos cliques, menos digitação, menos dúvida, mais resultado.
