# AGENTS.md — Multi-Agent AI Integration

## Visão Geral

O **AGENDA OS** integra 5 agentes de IA especializados que trabalham em conjunto para otimizar a operação de barbearias:

| Agente | Porta | Função | Caso de Uso |
|--------|-------|--------|-------------|
| **AND** | 8001 | Raciocínio avançado | Aprende padrões de agendamento |
| **Hermes** | 8002 | Planejamento autônomo | Otimiza horários |
| **Evolver** | 8003 | Evolução de estratégias | Sugere preços dinâmicos |
| **Generic** | 8004 | Orquestração de tarefas | Chatbot de atendimento |
| **Claude-Mem** | 8005 | Memória de longo prazo | Preferências de clientes |

## Interface Padrão

Cada agente expõe:

```
POST /api/v1/process  — Processa uma tarefa
POST /api/v1/learn    — Aprende com dados
GET  /api/v1/status   — Status detalhado
GET  /api/v1/health   — Health check
```

## Docker

```bash
# Subir apenas os agentes
docker compose -f docker-compose.dev.yml --profile agents up -d

# Subir tudo (backend + frontend + agentes)
docker compose -f docker-compose.dev.yml --profile full up -d
```

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/agents/health` | Health de todos agentes |
| `GET` | `/api/v1/agents/{id}/status` | Status de um agente |
| `POST` | `/api/v1/agents/and/execute` | Executar análise AND |
| `POST` | `/api/v1/agents/hermes/plan` | Planejar com Hermes |
| `POST` | `/api/v1/agents/evolver/optimize` | Otimizar com Evolver |
| `POST` | `/api/v1/agents/generic/orchestrate` | Orquestrar tarefas |
| `POST` | `/api/v1/agents/claude-mem/retrieve` | Recuperar memórias |
| `POST` | `/api/v1/agents/claude-mem/store` | Armazenar memória |
| `POST` | `/api/v1/agents/workflow` | Workflow multi-agente |

## Workflow de Exemplo

```json
POST /api/v1/agents/workflow
{
  "name": "booking_optimization",
  "steps": [
    {"agent": "and", "action": "analyze_patterns"},
    {"agent": "hermes", "action": "optimize_schedule"},
    {"agent": "evolver", "action": "suggest_pricing"}
  ]
}
```

## Testes

```bash
cd backend
pytest tests/test_agents.py -v
```
