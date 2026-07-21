# 02 — Risk Register (Matriz de Risco)

> Registro completo de riscos de segurança.  
> 30+ vulnerabilidades e ameaças catalogadas com impacto, probabilidade e prioridade.

---

## 1. Metodologia de Classificação

### Impacto (I)
| Nível | Valor | Descrição |
|-------|:-----:|-----------|
| **Catastrófico** | 5 | Vazamento de dados, perda financeira massiva, falência do negócio |
| **Alto** | 4 | Comprometimento de tenant, perda de dados, impacto reputacional grave |
| **Médio** | 3 | Degradação de serviço, incidente contido, impacto limitado |
| **Baixo** | 2 | Incidente menor, sem impacto em dados |
| **Mínimo** | 1 | Sem impacto real |

### Probabilidade (P)
| Nível | Valor | Descrição |
|-------|:-----:|-----------|
| **Quase Certo** | 5 | Acontecerá em < 1 mês sem mitigação |
| **Provável** | 4 | Acontecerá em < 6 meses |
| **Possível** | 3 | Acontecerá em < 2 anos |
| **Improvável** | 2 | Acontecerá em < 5 anos |
| **Raro** | 1 | Pode nunca acontecer |

### Score de Risco = I × P
| Score | Classificação |
|:-----:|--------------|
| 20-25 | 🔴 Crítico |
| 12-19 | 🟠 Alto |
| 6-11  | 🟡 Médio |
| 1-5   | 🟢 Baixo |

---

## 2. Registro de Riscos

### 🔴 Riscos Críticos (Score ≥ 20)

| ID | Risco | I | P | Score | Descrição |
|----|-------|:---:|:---:|:-----:|-----------|
| **R01** | **Vazamento Cross-Tenant** | 5 | 4 | **20** | Um tenant acessa dados de outro tenant. RLS não implementado. Se ocorrer, notificação obrigatória à ANPD (LGPD) + perda de confiança. |
| **R02** | **API Rate Limit Inexistente** | 5 | 4 | **20** | Sem proteção contra abuso. Um atacante pode fazer brute force de senhas, enumerar recursos, ou causar DoS com poucos recursos. |

### 🟠 Riscos Altos (Score 12-19)

| ID | Risco | I | P | Score |
|----|-------|:---:|:---:|:-----:|
| **R03** | PII em Logs | 4 | 4 | **16** |
| **R04** | JWT Secret Key Hardcoded Default | 5 | 3 | **15** |
| **R05** | Redis Sem Autenticação | 4 | 4 | **16** |
| **R06** | CSRF Não Implementado | 4 | 3 | **12** |
| **R07** | SQL Injection via FTS | 5 | 2 | **10** |
| **R08** | IDOR em Booking API | 4 | 3 | **12** |
| **R09** | Upload sem Scan de Malware | 3 | 4 | **12** |
| **R10** | Refresh Token como JWT (não opaque) | 4 | 3 | **12** |
| **R11** | Credential Stuffing (sem lockout) | 4 | 4 | **16** |
| **R12** | JWT `alg:none` Attack | 5 | 2 | **10** |
| **R13** | Mass Assignment via API | 3 | 3 | **9** |
| **R14** | Webhook Replay Attack | 4 | 2 | **8** |
| **R15** | CSP `unsafe-inline` | 3 | 3 | **9** |
| **R16** | Enumeração de Usuários | 3 | 3 | **9** |
| **R17** | Ataque DDoS Volumétrico | 5 | 2 | **10** |
| **R18** | Falha de Backup | 5 | 2 | **10** |
| **R19** | Comprometimento de Dependência | 4 | 3 | **12** |
| **R20** | SSRF via HTTP Client | 3 | 2 | **6** |

### 🟡 Riscos Médios (Score 6-11)

| ID | Risco | I | P | Score |
|----|-------|:---:|:---:|:-----:|
| **R21** | Falta de MFA para Admins | 4 | 2 | **8** |
| **R22** | Exposição de Stack Trace | 3 | 3 | **9** |
| **R23** | Path Traversal em Upload | 4 | 2 | **8** |
| **R24** | Comprometimento de Segredo de Webhook | 4 | 2 | **8** |
| **R25** | Google Calendar Evento Público | 2 | 3 | **6** |
| **R26** | Docker Image com Vulnerabilidades | 3 | 3 | **9** |
| **R27** | Ausência de SBOM | 2 | 3 | **6** |
| **R28** | CI/CD sem Security Scanning | 3 | 4 | **12** |

### 🟢 Riscos Baixos (Score 1-5)

| ID | Risco | I | P | Score |
|----|-------|:---:|:---:|:-----:|
| **R29** | Abuso de Feature de Indicação | 2 | 2 | **4** |
| **R30** | Clickjacking (já mitigado por X-Frame-Options) | 3 | 1 | **3** |
| **R31** | DNS Hijacking do Subdomínio | 4 | 1 | **4** |

---

## 3. Plano de Tratamento

### 🔴 Resolver Antes do MVP (Sprint Atual)

| Risco | Ação | Responsável | Esforço |
|-------|------|:----------:|:------:|
| R01 | Criar migration RLS + testes cross-tenant | Dev | 3h |
| R02 | Implementar rate limiting (Redis) | Dev | 2h |
| R04 | Remover default secret + validar em startup | Dev | 30min |
| R05 | Configurar Redis com senha | Dev | 15min |
| R11 | Implementar lockout (5 tentativas / 15min) | Dev | 1h |
| R12 | Validar algoritmo JWT explicitamente | Dev | 15min |

### 🟠 Resolver no Beta (Próximos 2 meses)

| Risco | Ação |
|-------|------|
| R03 | Adicionar sanitização de PII nos logs |
| R06 | Implementar CSRF tokens |
| R08 | Adicionar validação de pertencimento em toda query |
| R09 | Integrar ClamAV ou Cloudflare Images |
| R10 | Refatorar refresh token para opaque string |
| R13 | Pydantic extra=forbid (já configurado) |
| R19 | Configurar Dependabot + CI audit |

---

## 4. Riscos Aceitos (Conscientemente)

| Risco | Justificativa |
|-------|--------------|
| **CSP unsafe-inline** | Necessário para TailwindCSS. Será resolvido com nonce-based CSP no V1. |
| **Sem MFA no MVP** | Custo de implementação vs. base de usuários inicial. Será implementado no V3. |
| **Redis Streams como broker** | Aceitável para notificações. Para eventos de pagamento, considerar migração futura. |
| **Single Developer** | Risco de negócio aceito. Mitigado por documentação extensa e código limpo. |
| **Sem SIEM** | Custo proibitivo para MVP. Logs estruturados em JSON são suficiente para 10 clientes. |

---

## 5. Matriz de Calor

```
Probabilidade
    5 │
      │
    4 │    🟡        🟠R03  🟠R11  🟠R05
      │                  🟠R19
    3 │          🟡R22  🟠R06  🟠R08  🟠R09
      │          🟡R15  🟠R10
    2 │    🟢     🟡R20  🟡R21  🟠R14  🟠R17  🟠R18
      │                       🟡R23
    1 │    🟢     🟢     🟢     🟢     🟡
      └─────────────────────────────────────────→ Impacto
          1      2      3      4      5

🔴 = Zona crítica (agir imediatamente)
🟠 = Zona de atenção (agir no próximo sprint)
🟡 = Zona de monitoramento (agir no roadmap)
🟢 = Zona aceitável (monitorar)
```

---

## 6. Monitoramento Contínuo

| Atividade | Frequência |
|-----------|:----------:|
| Revisão do Risk Register | Trimestral |
| Scan de vulnerabilidades (dependências) | Semanal (CI) |
| Revisão de logs de segurança | Semanal (manual) |
| Teste de restore de backup | Mensal |
| Revisão de permissões e roles | Trimestral |
| Pentest externo | Anual |
| Atualização do threat model | A cada nova feature major |

---

> **Resumo:** O Risk Register contém 31 riscos catalogados. 2 são críticos (cross-tenant leak, rate limit) e exigem ação imediata. 12 são altos e devem ser tratados antes do lançamento comercial. O restante está distribuído no roadmap de segurança. Nenhum risco foi considerado inaceitável para o MVP com as devidas mitigações.
