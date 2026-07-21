# 18 — Riscos Técnicos

---

## 18.1 Matriz de Riscos

Cada risco é avaliado em:
- **Probabilidade** (1–5): chance de ocorrer
- **Impacto** (1–5): dano se ocorrer
- **Score** = Probabilidade × Impacto

---

## 18.2 Riscos Identificados

### R1 — Vazamento de Dados Cross-Tenant

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 5 (Catastrófico) |
| **Score** | 15 🔴 |
| **Descrição** | Um tenant acessa dados de outro tenant por falha no isolamento |
| **Mitigação** | RLS no PostgreSQL, middleware de tenant, testes cross-tenant automatizados, auditoria de acessos suspeitos |
| **Contingência** | Desligar tenant afetado, notificar afetados, investigar logs, corrigir漏洞, reportar à ANPD (LGPD) |

### R2 — Sobrecarga do Banco de Dados

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 4 (Alto) |
| **Score** | 12 🟠 |
| **Descrição** | PostgreSQL não escala com crescimento de tenants, causando lentidão generalizada |
| **Mitigação** | Índices otimizados, connection pooling (PgBouncer), cache agressivo (Redis), read replicas |
| **Contingência** | Provisionar read replica, otimizar queries lentas, aumentar instância temporariamente |

### R3 — Indisponibilidade do Gateway de Pagamento

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 2 (Baixa) |
| **Impacto** | 4 (Alto) |
| **Score** | 8 🟡 |
| **Descrição** | Stripe/PagSeguro fica indisponível, impedindo pagamentos |
| **Mitigação** | Circuit breaker, múltiplos gateways (fallback), agendamento sem pagamento como fallback |
| **Contingência** | Ativar gateway secundário, modo "pague depois" temporário |

### R4 — Complexidade Acidental

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 3 (Médio) |
| **Score** | 12 🟠 |
| **Descrição** | Arquiteto over-engineer o sistema, adicionando complexidade desnecessária para 1 dev |
| **Mitigação** | Começar simples (VPS + Docker), evoluir apenas quando necessário, YAGNI, KISS |
| **Contingência** | Refatoração para simplificar, remover abstrações desnecessárias |

### R5 — Burnout do Desenvolvedor Único

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 4 (Alta) |
| **Impacto** | 5 (Catastrófico) |
| **Score** | 20 🔴 |
| **Descrição** | Único desenvolvedor fica sobrecarregado, doente, ou desmotivado |
| **Mitigação** | Escopo realista, automação máxima, documentação clara, pausas regulares, health checks pessoais |
| **Contingência** | Documentação para onboarding rápido de substituto, código limpo e bem documentado |

### R6 — Migração de Banco de Dados Problemática

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 3 (Médio) |
| **Score** | 9 🟡 |
| **Descrição** | Migration causa corrupção de dados ou downtime prolongado |
| **Mitigação** | Migrations testadas em staging, backup antes de cada migration, rollback scripts |
| **Contingência** | Rollback + restore backup, corrigir migration, reaplicar |

### R7 — Falha no Backup / Restore

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 2 (Baixa) |
| **Impacto** | 5 (Catastrófico) |
| **Score** | 10 🟠 |
| **Descrição** | Backup não funciona quando necessário, perda de dados permanente |
| **Mitigação** | Testes mensais de restore, alertas de falha de backup, backup em múltiplos storages |
| **Contingência** | Restaurar do storage secundário, reconstruir dados de logs se possível |

### R8 — Ataque de Segurança (Injeção, XSS, CSRF)

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 2 (Baixa) |
| **Impacto** | 5 (Catastrófico) |
| **Score** | 10 🟠 |
| **Descrição** | Vulnerabilidade explorada por atacante externo |
| **Mitigação** | OWASP checklist, SAST/DAST no CI/CD, headers de segurança, WAF, pentest anual |
| **Contingência** | Plano de resposta a incidentes (doc 11 — Segurança), correção emergencial |

### R9 — Dependência de Serviços de Terceiros

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 3 (Médio) |
| **Score** | 9 🟡 |
| **Descrição** | WhatsApp API, gateway de e-mail, ou outro serviço terceiro muda API / preço / encerra |
| **Mitigação** | Abstrair serviços terceiros atrás de interfaces, ter fallbacks, evitar vendor lock-in |
| **Contingência** | Trocar provedor seguindo interface padronizada |

### R10 — Problemas de Performance no Multi-Tenant

| Atributo | Valor |
|----------|-------|
| **Probabilidade** | 3 (Média) |
| **Impacto** | 3 (Médio) |
| **Score** | 9 🟡 |
| **Descrição** | Um tenant com muitos dados degrada performance para outros |
| **Mitigação** | Rate limiting por tenant, índices otimizados, queries com limite, monitoramento por tenant |
| **Contingência** | Isolar tenant problemático em recursos dedicados, otimizar queries |

---

## 18.3 Tabela Resumo (Ordenada por Score)

| # | Risco | P | I | Score |
|---|-------|---|---|-------|
| R5 | Burnout do desenvolvedor | 4 | 5 | 20 🔴 |
| R1 | Vazamento cross-tenant | 3 | 5 | 15 🔴 |
| R2 | Sobrecarga do banco | 3 | 4 | 12 🟠 |
| R4 | Complexidade acidental | 4 | 3 | 12 🟠 |
| R7 | Falha no backup | 2 | 5 | 10 🟠 |
| R8 | Ataque de segurança | 2 | 5 | 10 🟠 |
| R6 | Migration problemática | 3 | 3 | 9 🟡 |
| R9 | Dependência terceiros | 3 | 3 | 9 🟡 |
| R10 | Performance multi-tenant | 3 | 3 | 9 🟡 |
| R3 | Indisponibilidade gateway | 2 | 4 | 8 🟡 |

---

## 18.4 Riscos Técnicos — Recomendações

1. **Prioridade #1:** Cuide da sua saúde. O projeto depende de 1 pessoa. Automatize tudo que puder.
2. **Prioridade #2:** Teste cross-tenant rigorosamente. Um vazamento de dados é game-over.
3. **Prioridade #3:** Mantenha a arquitetura simples. Resista ao impulso de "usar a tecnologia legal nova".
4. **Backups testados são a única garantia real contra desastres.**
5. **Segurança não é opcional — é fundamento. Invista tempo nisso desde o dia 1.**

---

> **Princípio:** Riscos não são para serem evitados — são para serem gerenciados. O pior risco é aquele que você não viu chegar. Esta lista deve ser revisada trimestralmente.
