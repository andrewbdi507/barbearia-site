# 05 — Go-Live Checklist

> Pré-condições para o MVP ser exposto a clientes reais.  
> Este checklist DEVE estar 100% concluído antes do primeiro beta tester.

---

## 1. Segurança (CRÍTICO — Bloqueia Go-Live)

- [ ] R1: Row-Level Security ativado em todas tabelas de negócio
- [ ] R2: Rate limiting implementado (Redis sliding window)
- [ ] R3: SECRET_KEY único e ≥ 32 caracteres (não é o default)
- [ ] R4: Redis com autenticação (senha)
- [ ] R5: Payload size limit (5 MB global)
- [ ] R6: JWT algorithm validado explicitamente
- [ ] R7: CSRF protection em formulários state-changing
- [ ] R8: Login lockout (5 tentativas / 15 min)
- [ ] R9: PII sanitizada nos logs
- [ ] R10: Testes cross-tenant passando

---

## 2. Infraestrutura

- [ ] VPS provisionada e acessível
- [ ] Docker Compose funcionando (postgres + redis + backend)
- [ ] PostgreSQL com backups automáticos configurados
- [ ] Backup testado (restore completo verificado)
- [ ] Domínio configurado (barbersaas.com.br)
- [ ] DNS propagado e resolvendo
- [ ] Cloudflare proxy ativo (laranja)
- [ ] TLS 1.3 válido (verificar com SSL Labs)
- [ ] Health checks funcionando (/live, /ready)
- [ ] Monitoramento básico ativo (UptimeRobot ou similar)

---

## 3. Aplicação

- [ ] API de serviços (CRUD) funcionando
- [ ] API de profissionais (CRUD) funcionando
- [ ] API de tenant (criar, resolver subdomínio) funcionando
- [ ] API de disponibilidade (grid de horários) funcionando
- [ ] API de agendamento (criar, cancelar) funcionando
- [ ] Autenticação (login admin + barbeiro) funcionando
- [ ] Site público acessível no subdomínio do tenant
- [ ] Painel admin acessível em /admin
- [ ] Fluxo de agendamento ponta-a-ponta testado
- [ ] Notificações WhatsApp (confirmação + lembrete) funcionando

---

## 4. Frontend

- [ ] Site público: Home carregando corretamente
- [ ] Site público: Fluxo de agendamento (4 passos) funcional
- [ ] Site público: Tela de confirmação exibindo dados corretos
- [ ] Site público: Mobile-first verificado (iPhone SE, iPhone 14, Android)
- [ ] Site público: Performance Lighthouse ≥ 90
- [ ] Painel admin: Dashboard carregando com dados
- [ ] Painel admin: CRUD de serviços funcional
- [ ] Painel admin: CRUD de profissionais funcional
- [ ] Painel admin: Configuração de tema (cores, logo) funcional
- [ ] Painel admin: Dark mode funcional

---

## 5. LGPD & Legal

- [ ] Política de Privacidade publicada e acessível
- [ ] Termos de Uso publicados e acessíveis
- [ ] Checkbox de consentimento no fluxo de agendamento
- [ ] Registro de consentimento (tabela consents)
- [ ] Canal do DPO visível (privacidade@...)

---

## 6. Operações

- [ ] Script de deploy documentado e testado
- [ ] Procedimento de rollback documentado e testado
- [ ] Logs acessíveis (Docker logs + stdout)
- [ ] Alertas configurados (erro 500, health check falha)
- [ ] Procedimento de backup verificado
- [ ] Procedimento de restore testado

---

## 7. Beta Testers

- [ ] 5 barbearias confirmadas para beta
- [ ] Roteiro de onboarding preparado
- [ ] Canal de feedback configurado (WhatsApp grupo)
- [ ] Métricas de sucesso definidas e instrumentadas

---

## 8. Verificação Final

- [ ] Teste de fumaça: agendar → confirmar → receber WhatsApp
- [ ] Teste de fumaça: admin criar serviço → aparecer no site público
- [ ] Teste de fumaça: admin alterar cor → refletir no site
- [ ] Teste de segurança: tentar acessar dados de outro tenant → 403
- [ ] Teste de segurança: brute force login → lockout após 5 tentativas
- [ ] Teste de segurança: upload de arquivo não-imagem → rejeitado
- [ ] Teste de carga: 20 agendamentos simultâneos sem erros

---

## Status do Go-Live

```
Progresso: ░░░░░░░░░░░░░░░░░░░░ 0%

Resolva as 10 ressalvas + complete os checklists acima
antes de expor o sistema a clientes reais.
```

---

> **Nota:** Este checklist é condição necessária para o go-live. Nenhum item pode ser pulado ou adiado. A segurança dos dados dos clientes beta é tão importante quanto a dos clientes pagantes.
