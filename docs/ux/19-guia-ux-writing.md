# 19 — Guia de UX Writing

> As palavras certas, nos lugares certos, no tom certo.

---

## 19.1 Tom de Voz

### Personalidade da Marca

| Característica | Descrição | Exemplo |
|---------------|-----------|---------|
| **Amigável** | Como um barbeiro falando com um cliente | "E aí, bora renovar o visual?" |
| **Claro** | Sem jargão técnico, sem ambiguidade | "Agendar" não "Iniciar processo de reserva" |
| **Confiante** | Transmite segurança, não arrogância | "Agendamento confirmado!" não "Seu agendamento foi processado com sucesso." |
| **Respeitoso** | Formalidade adequada ao contexto brasileiro | "Senha" não "Password" |
| **Útil** | Cada palavra tem um propósito | "Celular (para confirmação)" não apenas "Celular" |

### O que NÃO somos

- ❌ Robótico: "Sua solicitação foi processada com êxito."
- ❌ Infantil: "Uhuuuul! Seu cortinho foi marcado!"
- ❌ Vago: "Algo deu errado."
- ❌ Culposo: "Você não preencheu o campo corretamente."
- ❌ Técnico demais: "Erro 500 — Internal Server Error"

---

## 19.2 Textos por Contexto

### Botões (CTAs)

| Contexto | Texto | Evitar |
|----------|-------|--------|
| Agendar | **"Agendar agora"** | "Criar reserva", "Iniciar agendamento" |
| Confirmar | **"Confirmar agendamento"** | "Submit", "Enviar" |
| Cancelar | **"Cancelar agendamento"** | "Deletar", "Remover" |
| Salvar | **"Salvar alterações"** | "Apply", "OK" |
| Pagar | **"Pagar R$ 10,00"** | "Processar pagamento" |
| Próximo | **"Continuar"** | "Próximo passo", "Avançar" |
| Voltar | **"Voltar"** | "Retornar", "Passo anterior" |
| Fechar | **"Fechar"** ou **✕** | "Dismiss", "Cancel" |
| Excluir | **"Excluir"** (com confirmação) | "Deletar permanentemente" |

### Mensagens de Sucesso

| Contexto | Texto |
|----------|-------|
| Agendamento confirmado | **"Agendamento confirmado! 🎉"** com resumo abaixo |
| Pagamento aprovado | **"Pagamento aprovado! Seu horário está garantido."** |
| Cadastro criado | **"Conta criada! Bem-vindo à plataforma."** |
| Dados salvos | **"Alterações salvas com sucesso."** |
| Upload concluído | **"Foto enviada! Já está no seu site."** |
| Convite enviado | **"Convite enviado! O profissional receberá um e-mail."** |

### Mensagens de Erro

| Contexto | Texto |
|----------|-------|
| Campo obrigatório vazio | **"Preencha seu nome para continuar."** (não "Campo obrigatório") |
| E-mail inválido | **"Este e-mail não parece válido. Confira e tente de novo."** |
| Telefone inválido | **"Este número não parece certo. Use DDD + número."** |
| Senha fraca | **"Senha muito curta. Use pelo menos 8 caracteres."** |
| Pagamento recusado | **"Pagamento não aprovado. Tente outro cartão ou PIX."** |
| Horário indisponível | **"Ops! Este horário acabou de ser reservado. Escolha outro?"** |
| Sessão expirada | **"Você ficou um tempo sem usar. Faça login novamente."** |
| Erro do servidor | **"Algo deu errado aqui. Já estamos verificando. Tente em instantes."** |

### Mensagens de Alerta / Confirmação

| Contexto | Texto |
|----------|-------|
| Cancelar agendamento | **"Tem certeza que quer cancelar? Seu sinal de R$ 10,00 será reembolsado se cancelar até 2h antes."** |
| Excluir serviço | **"Tem certeza? Agendamentos futuros deste serviço serão afetados."** |
| Sair sem salvar | **"Você tem alterações não salvas. Quer salvar antes de sair?"** |
| Excluir conta | **"Esta ação não pode ser desfeita. Todos os dados serão perdidos."** |

### Empty States

| Contexto | Título | Subtítulo | CTA |
|----------|--------|-----------|-----|
| Sem agendamentos | **"Nenhum agendamento ainda"** | "Compartilhe o link do seu site e comece a receber clientes!" | **"Compartilhar link"** |
| Sem serviços | **"Nenhum serviço cadastrado"** | "Adicione os serviços que sua barbearia oferece." | **"Adicionar serviço"** |
| Sem profissionais | **"Nenhum profissional na equipe"** | "Adicione os barbeiros que trabalham com você." | **"Adicionar profissional"** |
| Sem avaliações | **"Nenhuma avaliação ainda"** | "As avaliações aparecem aqui depois que os clientes avaliarem." | — |
| Sem fotos na galeria | **"Galeria vazia"** | "Mostre seus melhores trabalhos! Fotos atraem mais clientes." | **"Adicionar fotos"** |
| Sem notificações | **"Nenhuma notificação"** | "Tudo em ordem! Notificações aparecerão aqui." | — |
| Busca sem resultados | **"Nada encontrado"** | "Tente outros termos ou limpe os filtros." | **"Limpar filtros"** |

### Estados de Loading

| Contexto | Texto |
|----------|-------|
| Carregando página | **"Carregando..."** (com skeleton) |
| Processando pagamento | **"Processando pagamento... Isso leva até 30 segundos."** |
| Enviando dados | **"Salvando..."** |
| Buscando horários | **"Buscando horários disponíveis..."** |
| Upload de imagem | **"Enviando imagem... 65%"** |

---

## 19.3 Microcopy — Placeholders e Labels

### Labels de Formulário

| Campo | Label | Placeholder |
|-------|-------|-------------|
| Nome | **"Nome completo"** | "Seu nome" |
| WhatsApp | **"WhatsApp"** (com ícone 📱) | "(11) 99999-9999" |
| E-mail | **"E-mail (opcional)"** | "seu@email.com" |
| Senha | **"Senha"** | "Mínimo 8 caracteres" |
| Observação | **"Observação para o barbeiro (opcional)"** | "Ex: prefiro degradê baixo" |
| Endereço | **"Endereço da barbearia"** | "Rua, número, bairro" |
| Nome do serviço | **"Nome do serviço"** | "Ex: Corte social" |
| Preço | **"Preço (R$)"** | "45,00" |

### Textos de Ajuda (Helper Text)

| Contexto | Texto |
|----------|-------|
| WhatsApp | "Enviaremos a confirmação e o lembrete por aqui." |
| E-mail | "Usado para recuperação de senha e promoções." |
| Observação | "O barbeiro verá antes do atendimento." |
| Subdomínio | "Este será o endereço do seu site. Depois você pode usar um domínio próprio." |
| Duração do serviço | "Tempo estimado de atendimento. O cliente verá antes de agendar." |

---

## 19.4 Mensagens do Sistema (Notificações)

### WhatsApp (Cliente)

| Gatilho | Mensagem |
|---------|----------|
| Agendamento confirmado | **"✅ Agendamento confirmado, [Nome]!\n\n📅 [Data] às [Hora]\n💇 [Barbeiro]\n✂️ [Serviço]\n💰 Sinal: R$ [valor]\n📍 [Endereço]\n\nAté lá! 😊"** |
| Lembrete 24h | **"⏰ Lembrete: amanhã às [Hora] você tem [Serviço] com [Barbeiro]!\n\n📍 [Endereço]\n\nConfirma? 👍"** |
| Lembrete 1h | **"🪒 Seu horário é daqui a 1h!\n\n[Barbeiro] está te esperando às [Hora].\n📍 [Endereço]"** |
| Pós-atendimento | **"E aí, [Nome]! Como foi o [Serviço] com [Barbeiro]? ⭐\n\n[link de avaliação]"** |
| Retorno 30 dias | **"Já faz 1 mês, [Nome]! 🪒\n\nQue tal renovar o visual? [Barbeiro] está com horários essa semana:\n\n[link reagendamento]"** |

### Push Notification (Barbeiro)

| Gatilho | Mensagem |
|---------|----------|
| Novo agendamento | **"📅 Novo: [Nome] — [Serviço] — [Data] [Hora]"** |
| Cancelamento | **"❌ Cancelado: [Nome] — [Serviço] — [Data] [Hora]"** |
| Lembrete do dia | **"Bom dia! 🌅 Hoje: [N] agendamentos a partir das [Hora]."** |

---

## 19.5 Princípios de UX Writing

1. **Clareza acima de criatividade** — O usuário precisa entender em 1 segundo
2. **Ação no final** — "Agendar agora" não "Agora agendar"
3. **Específico > Genérico** — "Enviaremos WhatsApp em 5 min" não "Você receberá notificações"
4. **Presente > Futuro** — "Agendamento confirmado" não "Seu agendamento será confirmado"
5. **Ativo > Passivo** — "Você agendou" não "O agendamento foi realizado"
6. **Positivo > Negativo** — "Use 8 caracteres" não "Não use menos de 8 caracteres"
7. **Consistência** — Sempre "agendamento", nunca "booking"/"reserva"/"compromisso"

---

> **Resumo:** UX Writing é design com palavras. Cada texto é uma oportunidade de guiar, tranquilizar ou encantar o usuário. Palavras erradas geram dúvida, frustração e abandono. Palavras certas geram confiança, clareza e conversão.
