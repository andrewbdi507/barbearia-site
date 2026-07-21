# 05 — Requisitos Não Funcionais

---

## 5.1 Performance

| Requisito | Métrica | Observação |
|-----------|---------|------------|
| Tempo de carregamento do site público | LCP < 2.5s, FID < 100ms, CLS < 0.1 | Lighthouse score ≥ 90 |
| Tempo de resposta da API (P95) | < 200ms | Medido no backend, excluindo latência de rede |
| Tempo de resposta da API (P99) | < 500ms | Picos aceitáveis |
| Tempo de carregamento do painel admin (SPA) | First load < 3s, navegação < 500ms | Code splitting por rota |
| Grid de horários (consulta de disponibilidade) | < 100ms | Cache de slots disponíveis |
| Throughput da API | ≥ 100 req/s por instância | Escala horizontal resolve |
| Tamanho de bundle JS (site público) | < 150KB gzip | Critical CSS inline, lazy load |
| Cache de assets estáticos | 1 ano (com hash no nome) | Cloudflare CDN |
| Otimização de imagens | WebP/AVIF automático, lazy loading | CDN com transformação on-the-fly |
| Conexões simultâneas | 1.000 por instância | WebSocket para notificações |

---

## 5.2 Segurança

| Requisito | Descrição |
|-----------|-----------|
| Criptografia em trânsito | TLS 1.3 obrigatório, HSTS, certificados automáticos |
| Criptografia em repouso | Dados sensíveis criptografados (AES-256-GCM) |
| Autenticação | JWT com refresh token, expiração curta (15 min access, 7 dias refresh) |
| Autorização | RBAC em nível de API (middleware por rota) |
| Proteção contra SQL Injection | ORM com parameterized queries (SQLAlchemy) |
| Proteção contra XSS | CSP headers, sanitização de input, escaping de output |
| Proteção contra CSRF | SameSite cookies, CSRF tokens em formulários |
| Rate limiting | Por IP, por tenant, por endpoint (Redis) |
| Headers de segurança | CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| Upload seguro | Validação de tipo MIME, scan de malware, armazenamento isolado (S3) |
| Gestão de segredos | Variáveis de ambiente + Vault (produção) |
| Sessões | HTTP-only, Secure, SameSite cookies |
| Isolamento multi-tenant | Row-level security + política de acesso por tenant |
| Testes de segurança | SAST, DAST, dependency scanning no CI/CD |
| Pentest | Anual por empresa externa |

---

## 5.3 Disponibilidade

| Requisito | SLA | Observação |
|-----------|-----|------------|
| Uptime geral | 99.5% (MVP) → 99.9% (V1) → 99.95% (V2+) | ~4.3h de downtime/mês no MVP |
| Janela de manutenção | Domingo 02:00–04:00 (horário local) | Comunicação com 48h de antecedência |
| Recuperação de falha (RTO) | < 1 hora | Estratégia de failover automático |
| Perda de dados (RPO) | < 5 minutos | Backup contínuo + point-in-time recovery |
| Health checks | A cada 30 segundos | Kubernetes liveness/readiness probes |
| Degradação graciosa | Site público funciona mesmo se API de agendamento cair | CDN + páginas estáticas |

---

## 5.4 Escalabilidade

| Requisito | Descrição |
|-----------|-----------|
| Escalabilidade horizontal | Todos os serviços stateless (API, workers, frontend) |
| Banco de dados | Read replicas para queries de leitura pesada |
| Cache distribuído | Redis cluster para sessões, cache, rate limiting |
| CDN global | Cloudflare para assets estáticos e páginas cacheadas |
| Fila de mensagens | Processamento assíncrono de notificações, e-mails, webhooks |
| Auto-scaling | Kubernetes HPA baseado em CPU/memória |
| Multi-região | A partir de 10.000 tenants (Brasil + América Latina) |

---

## 5.5 LGPD (Lei Geral de Proteção de Dados)

| Requisito | Descrição |
|-----------|-----------|
| Base legal | Consentimento explícito + execução de contrato + legítimo interesse |
| Finalidade | Dados coletados apenas para agendamento e comunicação |
| Consentimento | Checkbox explícito, não pré-marcado, registro de aceite |
| Direito de acesso | Cliente pode exportar todos os seus dados (JSON/CSV) |
| Direito de retificação | Cliente pode corrigir dados pessoais |
| Direito de exclusão | Exclusão lógica (soft delete) + exclusão física após 30 dias |
| Portabilidade | Exportação em formato estruturado |
| Encarregado de dados (DPO) | Canal de contato público no site |
| Retenção de dados | Dados de clientes inativos por 5 anos, depois anonimização |
| Cookies | Banner de consentimento, granularidade por categoria |
| Log de consentimento | Registro imutável de quando e como o consentimento foi dado |
| Incidentes de segurança | Notificação à ANPD em até 48h |
| Transferência internacional | Dados armazenados em território nacional (AWS São Paulo) |
| Relatório de impacto | DPIA para funcionalidades de alto risco |

---

## 5.6 Monitoramento

| Requisito | Descrição |
|-----------|-----------|
| Métricas de aplicação | Prometheus + Grafana (request rate, latency, error rate) |
| Logs centralizados | Loki + Grafana (structured JSON logs) |
| Tracing distribuído | Tempo (OpenTelemetry) |
| Alertas | AlertManager (latência > threshold, erro rate > 1%, disco > 80%) |
| Uptime monitoring | Health checks externos (Cloudflare ou UptimeRobot) |
| Error tracking | Sentry (exceções não tratadas) |
| Dashboard de negócio | Métricas SaaS (MRR, churn, novos tenants, DAU) |
| On-call | PagerDuty (ou similar gratuito) para alertas críticos |

---

## 5.7 Custos

| Requisito | Descrição |
|-----------|-----------|
| Infraestrutura mensal (MVP) | < R$ 500/mês |
| Infraestrutura mensal (100 tenants) | < R$ 1.500/mês |
| Infraestrutura mensal (1.000 tenants) | < R$ 5.000/mês |
| Ferramentas gratuitas prioritárias | Cloudflare Free, GitHub Actions, Sentry Free, Grafana Cloud Free |
| Sem custo de licenciamento | Stack 100% open source |
| Custo por tenant (infra) | < R$ 5/tenant/mês em escala |

---

## 5.8 Manutenção

| Requisito | Descrição |
|-----------|-----------|
| Atualizações de dependência | Dependabot + revisão mensal |
| Testes automatizados | ≥ 80% de cobertura, CI bloqueia merge se < threshold |
| Documentação | OpenAPI para API, Storybook para componentes, ADR para decisões |
| Versionamento | SemVer (MAJOR.MINOR.PATCH) |
| Changelog | Mantido manualmente, público para clientes |
| Deploy | Zero-downtime (rolling updates no Kubernetes) |
| Rollback | Reversível em < 5 minutos |
| Migrations de banco | Automáticas, com rollback, testadas em staging |

---

## 5.9 Compatibilidade

| Requisito | Descrição |
|-----------|-----------|
| Navegadores suportados | Chrome, Firefox, Safari, Edge (últimas 2 versões) |
| Dispositivos móveis | iOS 15+, Android 10+ |
| PWA | Instalável, offline básico (cache de páginas estáticas) |
| Acessibilidade | WCAG 2.1 nível AA |
| i18n | Preparado para múltiplos idiomas (pt-BR inicial, es, en futuros) |

---

## 5.10 Resiliência

| Requisito | Descrição |
|-----------|-----------|
| Circuit breaker | Para chamadas a serviços externos (gateway de pagamento, e-mail) |
| Retry com backoff | Exponential backoff + jitter para operações idempotentes |
| Timeout | Todas as chamadas externas com timeout máximo de 30s |
| Graceful shutdown | Sinais SIGTERM tratados, conexões drenadas |
| Bulkhead | Pools de conexão separados por serviço externo |
| Fallback | Cache de último resultado para consultas de disponibilidade |

---

> **Resumo:** O sistema é projetado para ser rápido, seguro, disponível e barato de operar. Cada requisito não funcional é tratado como funcionalidade de primeira classe, não como afterthought.
