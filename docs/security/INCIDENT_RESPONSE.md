# 04 — Incident Response Plan

> Plano de resposta a incidentes de segurança.  
> Adaptado para equipe de 1 desenvolvedor.

---

## 1. Classificação de Incidentes

### Severidade

| Nível | Definição | Exemplos | Tempo de Resposta |
|:-----:|-----------|----------|:-----------------:|
| **P0 — Crítico** | Dados de clientes comprometidos, sistema fora do ar, ataque ativo | Cross-tenant data leak, ransomware, breach confirmado | Imediato (any hour) |
| **P1 — Alto** | Funcionalidade crítica indisponível, vulnerabilidade explorável | Gateway de pagamento offline, SQLi encontrado | < 4 horas |
| **P2 — Médio** | Incidente contido, baixo impacto em dados | XSS em área logada, CSRF explorável | < 24 horas |
| **P3 — Baixo** | Incidente menor, sem risco imediato | Informação em headers, falta de rate limit pontual | Próximo sprint |

### Tipos

| Tipo | Descrição |
|------|-----------|
| **Data Breach** | Acesso não autorizado a dados pessoais |
| **Service Outage** | Indisponibilidade do sistema |
| **Account Compromise** | Conta de usuário/admin comprometida |
| **Malicious Code** | Código malicioso detectado (upload, dependência) |
| **Abuse** | Uso abusivo da plataforma (spam, fraude) |

---

## 2. Processo de Resposta (6 Fases)

### Fase 1: Detecção

**Fontes de detecção:**
- Alertas automáticos (Grafana/Prometheus — planejado)
- Logs de segurança (cross-tenant access, múltiplas falhas de login)
- Reporte de usuário (canal de suporte)
- Scan de vulnerabilidades (CI/CD)
- Notificação de gateway de pagamento

**Ação:** Registrar incidente com timestamp, fonte, e descrição inicial.

### Fase 2: Contenção

**Objetivo:** Impedir que o incidente se agrave.

| Cenário | Ação de Contenção |
|---------|-------------------|
| Cross-tenant access detectado | Suspender tenant ofensor + vítima, revogar todos os tokens |
| Ataque de força bruta | Bloquear IP no Cloudflare WAF, aumentar rate limit |
| Upload malicioso detectado | Remover arquivo do S3, revogar acesso do uploader |
| Comprometimento de conta admin | Resetar senha, revogar todas as sessões, revisar logs |
| Serviço fora do ar | Rollback para última versão estável |

### Fase 3: Investigação

**Perguntas a responder:**
- O que aconteceu? (timeline)
- Como aconteceu? (vetor de ataque)
- Quem foi afetado? (escopo: tenants, clientes, dados)
- Quando começou? (primeiro evento)
- Ainda está acontecendo? (contenção efetiva?)

**Ferramentas:**
- Logs estruturados (Loki/PostgreSQL)
- Audit logs (tabela audit_logs)
- Webhook logs (tabela webhook_logs)
- Traces (OpenTelemetry/Tempo — planejado)

### Fase 4: Remediação

**Ações técnicas:**
- Corrigir vulnerabilidade (patch de código)
- Aplicar security headers faltantes
- Atualizar dependência vulnerável
- Rotacionar secrets comprometidos
- Reforçar rate limiting

**Validação:**
- Testar correção em staging
- Verificar se o vetor de ataque foi fechado

### Fase 5: Recuperação

- Restaurar tenants suspensos (após verificação)
- Restaurar dados de backup (se necessário)
- Reativar funcionalidades desligadas
- Monitorar por 48h após recuperação

### Fase 6: Post-Mortem

**Documento de post-mortem (template):**

```
INCIDENTE: [Título]
Data: [Data] | Severidade: [P0-P3] | Duração: [X horas]

1. RESUMO
   O que aconteceu em 2-3 frases.

2. TIMELINE
   - HH:MM — Primeiro alerta
   - HH:MM — Investigação iniciada
   - HH:MM — Causa raiz identificada
   - HH:MM — Contenção aplicada
   - HH:MM — Correção deployada
   - HH:MM — Sistema normalizado

3. CAUSA RAIZ
   O que permitiu que o incidente ocorresse.

4. IMPACTO
   - Tenants afetados: [N]
   - Clientes afetados: [N]
   - Dados comprometidos: [Sim/Não — quais]
   - Tempo de downtime: [X minutos]

5. AÇÕES CORRETIVAS
   - [ ] Ação 1 (imediata)
   - [ ] Ação 2 (este sprint)
   - [ ] Ação 3 (roadmap)

6. LIÇÕES APRENDIDAS
   O que faremos diferente.
```

---

## 3. Comunicação

### Notificação de Clientes (Tenants)

**Quando notificar:**
- **Sempre:** Incidentes P0 e P1 que afetam dados ou disponibilidade
- **Avaliar:** Incidentes P2 com impacto visível
- **Não:** Incidentes P3 contidos internamente

**Template de notificação:**

```
Assunto: Incidente de segurança — [Breve descrição]

Prezado(a) [Nome do Admin],

Identificamos e contivemos um incidente de segurança
que pode ter afetado sua conta em [DATA/HORA].

O que aconteceu: [Descrição clara, sem jargão técnico]
O que fizemos: [Ações de contenção]
O que você precisa fazer: [Ações para o cliente, se houver]
Impacto nos seus dados: [Nenhum / Parcial / Descrição]

Estamos à disposição para esclarecimentos.
[Contato do suporte]
```

### Notificação à ANPD (LGPD)

**Obrigatória quando:** Incidente envolver dados pessoais com risco relevante aos titulares.

**Prazo:** 48 horas úteis da ciência do incidente.

**Conteúdo mínimo (Art. 48, §1º):**
- Descrição da natureza dos dados afetados
- Informações sobre os titulares envolvidos
- Indicação das medidas técnicas e de segurança utilizadas
- Riscos relacionados ao incidente
- Medidas que foram ou serão adotadas
- Contato do DPO

---

## 4. Contatos de Emergência

| Papel | Contato | Quando Acionar |
|-------|---------|---------------|
| Dev / CTO | [PRINCIPAL] | Todos os incidentes |
| Cloud Provider Support | [AWS/DO] | Infraestrutura |
| Gateway de Pagamento | [Stripe/MercadoPago] | Incidentes de pagamento |
| DPO (Encarregado LGPD) | [Futuro] | Data breach |
| Suporte Cloudflare | [Cloudflare] | DDoS / CDN |

---

## 5. Ferramentas e Recursos

| Recurso | MVP (Manual) | V1+ |
|---------|:-----------:|-----|
| Detecção | Logs + alertas Grafana | SIEM / WAF |
| Comunicação | WhatsApp / E-mail | Status Page |
| Investigação | Grafana + PostgreSQL queries | Ferramenta SIEM |
| On-Call | Celular do dev | PagerDuty |
| Post-Mortem | Markdown no repo | Ferramenta dedicada |

---

## 6. Simulações (Tabletop Exercises)

| Frequência | Cenário |
|:----------:|---------|
| Trimestral | Cross-tenant data leak simulado |
| Semestral | Ataque DDoS + serviço offline |
| Anual | Ransomware simulado (com restore de backup) |

---

> **Resumo:** O plano de resposta a incidentes define um processo claro de 6 fases (Detecção → Contenção → Investigação → Remediação → Recuperação → Post-Mortem). Para 1 desenvolvedor, a chave é automação: alertas, logs centralizados, e runbooks documentados. A comunicação transparente com clientes afetados é obrigatória (LGPD) e constrói confiança.
