# 🏛️ Barbershop SaaS

> Plataforma Multi-Tenant para gestão de barbearias e negócios baseados em agendamento.

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-✅-2496ED?logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-Proprietary-red)](./LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Estrutura](#estrutura)
- [Stack Tecnológica](#stack-tecnológica)
- [Quick Start](#quick-start)
- [Documentação](#documentação)
- [Contribuindo](#contribuindo)

---

## Sobre o Projeto

O **Barbershop SaaS** é uma plataforma completa de relacionamento entre empresas baseadas em agendamento e seus clientes finais. Não é apenas um sistema de agenda — é um ecossistema white-label que permite a qualquer negócio administrar sua presença digital sem depender de programadores.

**Foco inicial:** Barbearias  
**Expansão planejada:** Salões, clínicas, estúdios de tatuagem, psicólogos, fisioterapeutas, dentistas, podólogos

### Diferenciais

- 🎨 **White-label total** — cada empresa tem site próprio sem aparência de "sistema"
- ⚡ **Agendamento em < 2 minutos** — mobile-first, zero fricção
- 🏢 **Multi-Tenant nativo** — um banco, uma API, isolamento por Row-Level Security
- 🔒 **Segurança como fundamento** — zero dados de cartão, LGPD by design
- 💰 **Custo operacional baixo** — arquitetado para 1 dev manter 10.000+ tenants

---

## Arquitetura

O sistema segue **Clean Architecture** com princípios **SOLID**, **DDD** (quando aplicável) e **12-Factor App**.

```
┌─────────────────────────────────────────┐
│            CDN / WAF (Cloudflare)        │
└──────────┬──────────┬──────────┬────────┘
           │          │          │
    ┌──────▼──┐ ┌─────▼───┐ ┌───▼──────┐
    │  Site   │ │ Painel  │ │   API    │
    │ Público │ │  Admin  │ │  Pública │
    └────┬────┘ └────┬────┘ └────┬─────┘
         └───────────┼───────────┘
                     │
              ┌──────▼──────┐
              │  API (BFF)  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐ ┌──────▼──┐ ┌──────▼──┐
   │  Auth  │ │Scheduler│ │ Tenant  │
   └────────┘ └─────────┘ └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┼────────────┐
   ┌────▼───┐ ┌──────▼──┐ ┌──────▼──┐
   │Payment │ │  Notif  │ │  Media  │
   └────────┘ └─────────┘ └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┼────────────┐
   ┌────▼───┐ ┌──────▼──┐ ┌──────▼──┐
   │  PG    │ │  Redis  │ │   S3    │
   └────────┘ └─────────┘ └─────────┘
```

Documentação completa em [`docs/`](./docs/).

---

## Estrutura

```
barbearia-site/
├── backend/                    # API (FastAPI + Clean Architecture)
│   ├── app/                    # Código fonte da aplicação
│   │   ├── core/               # Kernel: config, exceptions, logging, security
│   │   ├── shared/             # Utilitários compartilhados
│   │   ├── modules/            # Módulos de domínio
│   │   │   ├── auth/           # Autenticação e autorização
│   │   │   ├── tenant/         # Empresas (multi-tenant)
│   │   │   ├── scheduling/     # Agendamentos
│   │   │   ├── payment/        # Pagamentos
│   │   │   ├── notification/   # Notificações
│   │   │   └── media/          # Uploads e storage
│   │   ├── infrastructure/     # Adaptadores (DB, Redis, HTTP)
│   │   └── presentation/       # API REST (rotas, middleware, schemas)
│   ├── tests/                  # Testes
│   ├── alembic/                # Migrations
│   ├── docker/                 # Dockerfiles
│   └── scripts/                # Scripts utilitários
│
├── frontend/                   # Aplicações frontend
│   ├── packages/               # Bibliotecas compartilhadas
│   │   └── design-system/      # Componentes e tokens de design
│   ├── apps/                   # Aplicações
│   │   ├── admin/              # Painel Administrativo (React SPA)
│   │   └── site/               # Site Público (React + Vite)
│   └── tooling/                # Configs compartilhadas
│
├── docs/                       # Documentação
│   ├── 01-21 (arquitetura)     # Documentos de arquitetura
│   ├── ux/                     # UX/UI Design
│   ├── database/               # Modelagem de dados
│   ├── integrations/           # Integrações
│   ├── security/               # Segurança
│   └── executive-review/       # Revisão executiva
│
├── .github/                    # CI/CD (GitHub Actions)
├── docker-compose.yml          # Ambiente de desenvolvimento
├── Makefile                    # Comandos de produtividade
└── README.md                   # Este arquivo
```

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.13+ · FastAPI · SQLAlchemy 2.x · Alembic · Pydantic v2 |
| **Frontend** | React 19 · TypeScript · Vite · TailwindCSS · Radix UI |
| **Banco** | PostgreSQL 16 (primary) · Redis 7 (cache/queue) |
| **Infra** | Docker · Docker Compose · GitHub Actions · Cloudflare |
| **Qualidade** | Ruff · Black · MyPy · Pre-commit · Pytest · Vitest |

---

## Quick Start

### Pré-requisitos
- **Python** 3.13+
- **Node.js** 20+
- **pnpm** 9+
- **Docker** & **Docker Compose**
- **uv** (Python package manager)

### 1. Clone o repositório

```bash
git clone <repo-url>
cd barbearia-site
```

### 2. Inicie os serviços

```bash
make up
# ou: docker compose up -d
```

### 3. Backend

```bash
cd backend
cp .env.example .env
uv sync --dev
uv run alembic upgrade head
uv run uvicorn app.presentation.api.app:create_app --factory --reload
```

### 4. Frontend

```bash
cd frontend
pnpm install
pnpm dev:admin   # Painel admin → http://localhost:5173
pnpm dev:site    # Site público → http://localhost:3000
```

### 5. Acesse

| Serviço | URL |
|---------|-----|
| **API** | http://localhost:8000 |
| **Swagger** | http://localhost:8000/docs |
| **Admin** | http://localhost:5173 |
| **Site** | http://localhost:3000 |

---

## Documentação

Toda a documentação do projeto está em [`docs/`](./docs/):

- [Visão Geral](./docs/01-visao-geral.md)
- [Arquitetura](./docs/06-arquitetura-geral.md)
- [Segurança](./docs/11-estrategia-seguranca.md)
- [Banco de Dados](./docs/database/DATABASE.md)
- [UX/UI](./docs/ux/README.md)
- [Integrações](./docs/integrations/INTEGRATIONS.md)
- [Auditoria de Segurança](./docs/security/SECURITY_AUDIT.md)
- [Revisão Executiva](./docs/executive-review/EXECUTIVE_REVIEW.md)

---

## Contribuindo

Veja [`CONTRIBUTING.md`](./CONTRIBUTING.md) para guia de contribuição.

---

## Licença

Este software é **proprietário**. Veja [`LICENSE`](./LICENSE) para detalhes.

---

*Desenvolvido com ❤️ no Brasil*
