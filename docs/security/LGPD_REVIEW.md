# 03 — LGPD Compliance Review

> Revisão de conformidade com a Lei Geral de Proteção de Dados (Lei 13.709/2018).  
> Foco: adequação do sistema Barbershop SaaS aos princípios e obrigações da LGPD.

---

## 1. Status Geral

| Artigo LGPD | Tema | Status | Observação |
|:-----------:|------|:------:|-----------|
| Art. 6º | Princípios | ✅ Alinhado | Finalidade, necessidade, transparência documentados |
| Art. 7º | Bases Legais | ✅ Alinhado | Consentimento + Execução de Contrato + Legítimo Interesse |
| Art. 8º | Consentimento | ⚠️ Parcial | Documentado, não implementado (sem registro granular) |
| Art. 9º | Titular de Dados | ✅ Alinhado | Direitos do titular mapeados |
| Art. 10º | Legítimo Interesse | ✅ Alinhado | Uso para operação do negócio (agendamentos) |
| Art. 11º | Dados Sensíveis | ✅ Não Coletado | Não coleta dados sensíveis (saúde, religião, etc.) |
| Art. 14º | Dados de Crianças | ✅ Não Aplicável | Não direcionado a menores |
| Art. 15º | Confirmação de Tratamento | ⚠️ Parcial | Sem endpoint automatizado |
| Art. 16º | Acesso aos Dados | ⚠️ Parcial | Exportação planejada, não implementada |
| Art. 17º | Correção | ✅ Planejado | Cliente edita perfil |
| Art. 18º | Exclusão (Direito ao Esquecimento) | ⚠️ Parcial | Soft delete + hard delete 30d — não implementado |
| Art. 19º | Portabilidade | ⚠️ Parcial | JSON/CSV export planejado |
| Art. 20º | Decisões Automatizadas | ✅ Não Aplicável | Sem decisões automatizadas |
| Art. 37º | Encarregado (DPO) | ⚠️ Parcial | Canal documentado, sem pessoa designada formalmente |
| Art. 41º | Relatório de Impacto | ❌ Pendente | DPIA não elaborado |
| Art. 46º | Segurança dos Dados | ⚠️ Parcial | Medidas técnicas boas, lacunas de implementação |
| Art. 48º | Comunicação de Incidente | ⚠️ Parcial | Plano de resposta documentado, não testado |

---

## 2. Análise dos Princípios (Art. 6º)

### Finalidade
✅ Os dados coletados têm finalidade específica e informada:
- Nome → identificação no agendamento
- Telefone → confirmação e lembretes
- E-mail → confirmação e marketing (com consentimento separado)

### Adequação
✅ Dados coletados são compatíveis com a finalidade informada.

### Necessidade
✅ Mínimo de dados coletados:
- Agendamento: apenas nome e WhatsApp (3 campos de texto)
- E-mail e observações são opcionais

### Livre Acesso
⚠️ Cliente pode ver seus dados? — Planejado (perfil), não implementado.

### Qualidade dos Dados
✅ Cliente pode atualizar seus dados (correção).

### Transparência
✅ Política de privacidade documentada como requisito. Checkbox LGPD no fluxo.

### Segurança
⚠️ Medidas técnicas boas, mas com lacunas de implementação (ver SECURITY_AUDIT.md).

### Prevenção
✅ Sistema projetado para evitar danos (zero dados de cartão, mínimo de dados).

### Não Discriminação
✅ Dados não usados para fins discriminatórios.

### Responsabilização
⚠️ Documentação existe, mas agente de tratamento não formalizado.

---

## 3. Bases Legais por Tipo de Dado

| Dado | Base Legal | Consentimento Necessário? |
|------|-----------|:-------------------------:|
| Nome | Execução de Contrato | Não (essencial para agendamento) |
| Telefone | Execução de Contrato + Legítimo Interesse | Não (confirmação é parte do serviço) |
| E-mail | Consentimento | Sim (marketing) / Não (confirmação transacional) |
| Histórico de Agendamentos | Legítimo Interesse | Não (operação do negócio) |
| Fotos (galeria) | Consentimento | Sim (do profissional fotografado) |
| IP / Logs de Acesso | Legítimo Interesse | Não (segurança) |
| Cookies de Analytics | Consentimento | Sim (opt-in) |

---

## 4. Direitos do Titular — Status de Implementação

| Direito | Como Implementar | Status |
|---------|-----------------|:------:|
| **Confirmação** | GET /api/v1/customers/me → confirma se dados existem | ❌ Não implementado |
| **Acesso** | GET /api/v1/customers/me/export → JSON completo | ❌ Não implementado |
| **Correção** | PUT /api/v1/customers/me → atualiza dados | ❌ Não implementado |
| **Exclusão** | DELETE /api/v1/customers/me → soft delete → hard delete 30d | ❌ Não implementado |
| **Portabilidade** | GET /api/v1/customers/me/export?format=csv | ❌ Não implementado |
| **Revogação de Consentimento** | DELETE /api/v1/customers/me/consent/{type} | ❌ Não implementado |
| **Oposição** | Canal de contato (DPO) para contestar tratamento | ❌ Não implementado |
| **Revisão Automatizada** | N/A — sem decisões automatizadas | ✅ N/A |

### Recomendação

Criar módulo `src/presentation/api/gdpr.py` com endpoints dedicados:
- `GET /api/v1/gdpr/me` — Dados do titular
- `GET /api/v1/gdpr/me/export` — Portabilidade
- `DELETE /api/v1/gdpr/me` — Direito ao esquecimento

---

## 5. Consentimento — Fluxo Técnico

### Registro de Consentimento (Tabela `consents`)

```json
{
  "customer_id": "c_123",
  "consent_type": "marketing_email",
  "is_granted": true,
  "consent_version": "2.1",
  "ip_address": "189.54.32.10",
  "user_agent": "Mozilla/5.0...",
  "granted_at": "2026-07-20T14:30:00Z"
}
```

### Granularidade

Cada tipo de consentimento é independente:
- `privacy_policy` — Aceite da política de privacidade (obrigatório)
- `terms_of_service` — Aceite dos termos de uso (obrigatório)
- `marketing_email` — Receber promoções por e-mail (opcional)
- `marketing_whatsapp` — Receber promoções por WhatsApp (opcional)
- `analytics_cookies` — Cookies de analytics (opcional)

### Revogação

Revogar consentimento NÃO apaga dados já coletados legalmente. Apenas interrompe novo tratamento com aquela finalidade.

---

## 6. Retenção e Exclusão de Dados

| Dado | Retenção | Justificativa | Destino Final |
|------|:--------:|---------------|---------------|
| Dados de cliente ativo | Indefinido (enquanto ativo) | Operação do negócio | — |
| Dados de cliente inativo | 5 anos após última interação | Legítimo interesse | Anonimização |
| Logs de auditoria | 5 anos | Obrigação legal (LGPD) | Deleção |
| Logs de acesso | 1 ano | Segurança | Deleção |
| Backups | 30 dias (diários) + 12 meses (mensais) | Recuperação | Deleção |
| Dados de tenant cancelado | 90 dias (grace period) + 5 anos (backup final) | Compliance | Deleção total |

### Fluxo de Exclusão (Direito ao Esquecimento)

```
1. Cliente solicita exclusão (via perfil ou DPO)
2. Soft delete: customer.deleted_at = NOW()
   → Dados não aparecem mais no sistema
3. Período de 30 dias para possível arrependimento/reversão
4. Após 30 dias:
   a. Anonimizar: nome → "Usuário Excluído", telefone → NULL, email → NULL
   b. Manter: bookings para integridade financeira (já anonimizados)
   c. Deletar: consents, preferences, reviews associadas
5. Backup: versão com dados reais expira conforme política de retenção
```

---

## 7. Relatório de Impacto (DPIA — Data Protection Impact Assessment)

### Necessidade

Recomendado para:
- Tratamento de dados em larga escala (milhares de clientes)
- Uso de novas tecnologias (SaaS multi-tenant)
- Dados de clientes de múltiplos estabelecimentos

### Template DPIA (Resumido)

```
1. DESCRIÇÃO DO TRATAMENTO
   Plataforma SaaS de agendamento para barbearias.
   Coleta: nome, telefone, e-mail, histórico de serviços.

2. NECESSIDADE E PROPORCIONALIDADE
   Dados são mínimos e necessários para operação.
   Sem coleta de dados sensíveis ou excessivos.

3. AVALIAÇÃO DE RISCOS
   - Cross-tenant data leak: ALTO (mitigado por RLS)
   - PII em logs: MÉDIO (mitigado por sanitização)
   - Acesso não autorizado: MÉDIO (mitigado por RBAC)

4. MEDIDAS DE MITIGAÇÃO
   - RLS no PostgreSQL
   - Criptografia em trânsito (TLS) e repouso
   - Logs sem PII (sanitização)
   - Soft delete + anonimização

5. CONCLUSÃO
   Riscos residuais aceitáveis com mitigações implementadas.
   Revisão anual recomendada.
```

---

## 8. Checklist LGPD para Produção

- [ ] Política de Privacidade publicada no site
- [ ] Termos de Uso publicados
- [ ] Banner de consentimento de cookies implementado
- [ ] Checkbox LGPD no fluxo de agendamento
- [ ] Registro de consentimento (tabela consents)
- [ ] Endpoint de exportação de dados (portabilidade)
- [ ] Endpoint de exclusão de dados (direito ao esquecimento)
- [ ] Canal do DPO publicado (privacidade@barbersaas.com.br)
- [ ] DPIA elaborado e documentado
- [ ] Plano de resposta a incidentes testado
- [ ] Treinamento básico de LGPD para o desenvolvedor
- [ ] Contrato de tratamento de dados com gateways de pagamento (se aplicável)

---

## 9. Papel do Desenvolvedor como Operador

Como SaaS multi-tenant, o Barbershop SaaS atua como **Operador** dos dados (processa em nome do Controlador — a barbearia).

### Responsabilidades como Operador:
- Processar dados apenas conforme instruções do controlador
- Implementar medidas de segurança adequadas
- Notificar o controlador em caso de incidente
- Auxiliar o controlador no exercício dos direitos dos titulares
- Manter registro das operações de tratamento

### Recomendações:
- Elaborar **Contrato de Tratamento de Dados** (DPA) entre a plataforma e cada barbearia (tenant)
- Incluir DPA nos Termos de Uso (aceite no cadastro)

---

> **Resumo:** A arquitetura do Barbershop SaaS está alinhada com os princípios da LGPD. As principais lacunas são de implementação (registro de consentimento granular, endpoints de portabilidade/exclusão, DPIA formal). Com as recomendações deste documento implementadas, o sistema atenderá aos requisitos da lei para a fase de MVP e estará preparado para escalar em conformidade.
