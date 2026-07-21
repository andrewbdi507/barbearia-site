# 👥 Módulo de Equipe (Staff) — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.staff`

---

## 1. Visão Geral

O módulo de equipe gerencia **quem trabalha dentro da empresa** (barbeiros, recepcionistas, gerentes, administradores). NÃO gerencia clientes finais. Inspirado em plataformas como **Slack** (member management), **Calendly** (availability), **Shopify** (staff permissions).

### 1.1 Arquitetura

```
app/modules/staff/
├── domain/
│   ├── entities.py       # StaffProfile, Team, Position, Specialty, Schedule, TimeOff, Invitation
│   ├── value_objects.py  # CommissionRule
│   ├── enums.py          # StaffStatus, TimeOffType, InvitationStatus, etc.
│   └── interfaces.py     # 8 ports (IStaffRepository, ITeamRepository, etc.)
├── application/
│   ├── staff_service.py  # StaffService — orquestração completa
│   └── dto.py            # 20+ DTOs
├── infrastructure/
│   ├── models/staff_models.py  # 8 modelos SQLAlchemy
│   └── repository.py     # 8 implementações
└── presentation/
    └── routes.py         # 30+ endpoints REST
```

---

## 2. Modelo de Dados

```
┌────────────────────────────────────────────────────────────────┐
│                        STAFF MODULE                            │
│                                                                │
│  User (auth) ──1:1── StaffProfile ──N:N── Specialty            │
│                    │                                           │
│                    ├── N:1 ── Position (cargo)                 │
│                    ├── 1:N ── StaffSchedule (jornada)          │
│                    ├── 1:N ── TimeOff (ausências)              │
│                    └── N:N ── Team (equipes)                   │
│                                                                │
│  Invitation ──→ convida email ──→ StaffProfile + User         │
│  StaffAuditLog ──→ registra toda alteração                    │
└────────────────────────────────────────────────────────────────┘
```

### 2.1 Relação com User (auth module)

`StaffProfile` é 1:1 com `User`. O `User` gerencia autenticação (login, senha, sessões). O `StaffProfile` gerencia o perfil profissional (cargo, especialidades, horários, comissão).

```
User (auth module)          StaffProfile (staff module)
┌──────────────┐           ┌──────────────────────┐
│ id           │◄──────────│ user_id (FK unique)   │
│ email        │           │ professional_name     │
│ password_hash│           │ position_id (FK)      │
│ name         │           │ specialties (JSONB)   │
│ phone        │           │ commission_type       │
│ is_active    │           │ status                │
│ tenant_id    │           │ schedules             │
└──────────────┘           └──────────────────────┘
```

---

## 3. Cargos (Positions)

**NUNCA hardcoded.** Cada tenant cria seus próprios cargos:

```sql
-- Exemplos:
INSERT INTO staff_positions (id, tenant_id, name) VALUES
  ('p1', 't_001', 'Administrador'),
  ('p2', 't_001', 'Gerente'),
  ('p3', 't_001', 'Recepcionista'),
  ('p4', 't_001', 'Barbeiro'),
  ('p5', 't_001', 'Auxiliar'),
  ('p6', 't_001', 'Estagiário');
```

**Para adicionar um novo cargo:** `POST /api/v1/staff/positions` — sem alterar código.

---

## 4. Equipes (Teams)

Agrupamento flexível de profissionais:

- **Equipe Manhã** — turno da manhã
- **Equipe Tarde** — turno da tarde
- **Equipe Premium** — profissionais premium
- **Unidade Centro** — filial centro
- **Unidade Norte** — filial norte

Cada equipe tem um líder (`leader_id`), membros (N:N) e cor identificadora.

---

## 5. Jornada de Trabalho

Cada profissional tem sua própria jornada por dia da semana, independente do horário da empresa:

```
StaffSchedule:
  Seg-Sex: 08:00-17:00 (almoço 12:00-13:00)
  Sáb:     08:00-12:00
  Dom:     Fechado
```

**Prioridade na geração de slots:**
1. StaffSchedule (se definido) — jornada do profissional
2. BusinessHours do tenant — horário da empresa

---

## 6. Ausências (TimeOff)

| Tipo | Descrição |
|------|-----------|
| `vacation` | Férias |
| `day_off` | Folga |
| `sick_leave` | Licença médica |
| `maternity_leave` | Licença maternidade |
| `paternity_leave` | Licença paternidade |
| `bereavement` | Luto |
| `training` | Treinamento |

**Fluxo:** Solicitação → Pendente → Aprovado/Rejeitado.

---

## 7. Convites

Fluxo de onboarding:

1. Admin envia convite: `POST /staff/invitations {email, position_id}`
2. Sistema gera token único (expira em 7 dias)
3. Convidado recebe email com link (MVP: token logado)
4. Convidado cria conta ou faz login
5. Ao aceitar: `StaffProfile` é criado automaticamente vinculado ao `User`

---

## 8. Comissões

Estrutura preparada para cálculo financeiro futuro:

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `none` | Sem comissão | Funcionário CLT |
| `percentage` | % sobre serviço | 30% de cada corte |
| `fixed` | Valor fixo | R$ 15 por serviço |

---

## 9. Auditoria

Toda ação é registrada em `staff_audit_logs`:

- Criação/edição/desativação de funcionário
- Mudança de cargo/permissão
- Criação/edição de equipe
- Adição/remoção de membros
- Solicitação/aprovação de ausências
- Envio/cancelamento de convites

---

## 10. Como Escalar

| Estratégia | Descrição |
|------------|-----------|
| **Índices** | `tenant_id`, `user_id`, `status`, `email` |
| **Cache Redis** | Staff profiles (5 min TTL), schedules, specialties |
| **Batch operations** | Upsert de horários em lote |
| **Paginação** | Todas as listagens com offset/limit |
| **Plan limits** | `max_professionals` validado no create |
