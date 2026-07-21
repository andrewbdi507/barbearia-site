# 06 — Arquitetura Geral

---

## 6.1 Visão Macro

O sistema segue uma **arquitetura em camadas** com princípios de **Clean Architecture**, organizada em **módulos independentes** que se comunicam via APIs bem definidas.

```
┌─────────────────────────────────────────────────────────┐
│                     CDN / WAF (Cloudflare)                │
│            DDoS Protection · Cache · SSL · DNS            │
└────────────┬──────────────┬──────────────┬───────────────┘
             │              │              │
     ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
     │ Site Público │ │ Painel     │ │ PWA        │
     │ (Next.js)    │ │ Admin      │ │ (Mobile)   │
     │ SSR/SSG      │ │ (React)    │ │            │
     └───────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                   ┌────────▼────────┐
                   │   API Gateway    │
                   │  Auth · Rate     │
                   │  Limit · Route   │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
    ┌─────────▼────┐ ┌─────▼──────┐ ┌────▼──────┐
    │  BFF Public  │ │  BFF Admin │ │ BFF Super │
    │  (FastAPI)   │ │  (FastAPI) │ │  Admin    │
    └──────┬───────┘ └─────┬──────┘ └─────┬─────┘
           │               │              │
           └───────────────┼──────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌──────▼──────┐   ┌─────▼─────┐
    │  Auth     │   │  Scheduler  │   │  Tenant   │
    │  Service  │   │  Service    │   │  Service  │
    └───────────┘   └─────────────┘   └───────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌──────▼──────┐   ┌─────▼─────┐
    │ Payment   │   │Notification │   │  Media    │
    │ Service   │   │  Service    │   │  Service  │
    └───────────┘   └─────────────┘   └───────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌──────▼──────┐   ┌─────▼─────┐
    │PostgreSQL │   │   Redis     │   │  S3 (R2)  │
    │ (Primary) │   │Cache/Queue  │   │  Storage  │
    └───────────┘   └─────────────┘   └───────────┘
```

---

## 6.2 Camadas da Clean Architecture (por serviço)

Cada serviço de backend segue a mesma estrutura interna:

```
servico/
├── domain/           # Entidades, Value Objects, Interfaces (núcleo)
│   ├── entities/
│   ├── value_objects/
│   ├── enums/
│   └── interfaces/   # Ports (repositórios, serviços externos)
│
├── application/      # Casos de Uso (orquestração)
│   ├── use_cases/
│   ├── dtos/
│   └── interfaces/   # Ports de entrada
│
├── infrastructure/   # Adaptadores (implementações concretas)
│   ├── database/
│   ├── cache/
│   ├── queue/
│   ├── storage/
│   ├── payment/
│   └── notification/
│
├── presentation/     # API REST, Schemas, Middlewares
│   ├── routes/
│   ├── schemas/
│   ├── middlewares/
│   └── dependencies/
│
└── config/           # Configurações, Settings
```

### Regra de Dependência

```
presentation → application → domain ← infrastructure
```

- **Domain** não depende de nada externo (zero dependências)
- **Application** depende apenas de domain
- **Infrastructure** implementa interfaces de domain
- **Presentation** depende de application e infrastructure (via DI)

---

## 6.3 Módulos do Sistema

### Frontend (3 aplicações)

| Aplicação | Framework | Renderização | Responsabilidade |
|-----------|-----------|--------------|------------------|
| **Site Público** | Next.js 14+ (App Router) | SSR + ISR | Vitrine do tenant, agendamento público, SEO |
| **Painel Admin** | React 18 + Vite | SPA (CSR) | Gestão do tenant (serviços, agenda, relatórios) |
| **Super Admin** | React 18 + Vite | SPA (CSR) | Gestão da plataforma (tenants, planos, métricas) |

### Backend (BFF Pattern + Services)

| Serviço | Responsabilidade |
|---------|-----------------|
| **BFF — Site Público** | Endpoints para o site do tenant (read-heavy, cache agressivo) |
| **BFF — Painel Admin** | Endpoints para gestão do tenant (read/write) |
| **BFF — Super Admin** | Endpoints para gestão da plataforma |
| **Auth Service** | Autenticação, autorização, RBAC, sessões, refresh tokens |
| **Scheduler Service** | Agendamentos, disponibilidade, conflitos, slots |
| **Tenant Service** | Configurações do tenant, personalização, temas, branding |
| **Payment Service** | Integração com gateways, webhooks, conciliação |
| **Notification Service** | WhatsApp, e-mail, SMS, push (assíncrono via fila) |
| **Media Service** | Upload, processamento de imagens, storage |

### Infraestrutura

| Componente | Tecnologia | Função |
|------------|-----------|--------|
| **PostgreSQL** | PostgreSQL 16 | Banco primário (dados transacionais) |
| **Redis** | Redis 7 | Cache, sessões, fila de mensagens, rate limiting |
| **S3 Storage** | Cloudflare R2 / AWS S3 | Imagens, uploads, backups |
| **CDN** | Cloudflare | Cache de assets, DDoS, WAF, SSL |
| **Message Queue** | Redis Streams | Processamento assíncrono de notificações |

---

## 6.4 Comunicação Entre Serviços

### Síncrona (Request-Response)
- **REST sobre HTTP/2** entre frontend e BFFs
- **REST sobre HTTP/2** entre BFFs e serviços de domínio
- Autenticação via JWT propagado nos headers

### Assíncrona (Event-Driven)
- **Redis Streams** para notificações, webhooks, processamento de mídia
- Eventos imutáveis com schema versionado
- Consumidores idempotentes

### Exemplo de fluxo assíncrono:

```
Agendamento Criado
    ↓ (evento no Redis Streams)
    ├── Notification Service → Envia WhatsApp
    ├── Notification Service → Envia E-mail
    ├── Analytics Service → Atualiza métricas
    └── CRM Service → Atualiza histórico do cliente
```

---

## 6.5 Isolamento Multi-Tenant

O isolamento ocorre em 3 camadas:

### Camada 1 — Aplicação
- Todo request carrega `X-Tenant-ID` (extraído do subdomínio ou JWT)
- Middleware injeta tenant context em toda requisição

### Camada 2 — Banco de Dados
- **Schema compartilhado** com `tenant_id` em todas as tabelas
- **Row-Level Security (RLS)** no PostgreSQL como segunda camada de proteção
- Índices com `tenant_id` como primeira coluna

### Camada 3 — Storage
- Prefixo por tenant no bucket S3: `/{tenant_id}/logo.png`
- Políticas IAM com condição de prefixo

---

## 6.6 Estratégia de Cache (Multi-camada)

```
CDN (Cloudflare)
    ↓ cache miss
API Response Cache (Redis, 30s-5min dependendo do endpoint)
    ↓ cache miss
Application Cache (Redis, dados computados: slots disponíveis)
    ↓ cache miss
Database Query Cache (PostgreSQL shared_buffers)
    ↓ cache miss
Database Disk
```

### O que é cacheado e por quanto tempo:

| Dado | Camada | TTL | Invalidação |
|------|--------|-----|-------------|
| Página inicial do tenant | CDN | 5 min | Webhook no update do tenant |
| Lista de serviços | CDN + Redis | 5 min | On update |
| Grid de horários | Redis | 30s | On booking/cancellation |
| Dados do profissional | CDN + Redis | 5 min | On update |
| Sessão do usuário | Redis | 15 min (access token) | On logout |
| Rate limit counters | Redis | Janela deslizante | Automático |

---

## 6.7 Tratamento de Erros

### Circuit Breaker
- Serviços externos (gateway pagamento, envio de e-mail, WhatsApp API)
- 5 falhas consecutivas → circuito aberto por 30s
- Half-open para teste antes de fechar

### Retry Policy
- Máximo 3 tentativas
- Exponential backoff (1s, 2s, 4s) + jitter aleatório
- Apenas para operações idempotentes (GET, PUT, DELETE idempotente)
- Sem retry para POST de criação (risco de duplicação)

### Dead Letter Queue
- Eventos que falham após 3 retries
- Inspeção manual para correção e replay

---

## 6.8 Versionamento de API

- Versionamento via URL: `/api/v1/...`
- Depreciação com aviso de 6 meses (header `Sunset` + `Deprecation`)
- Documentação via OpenAPI 3.1 (Swagger)
- Sempre backward-compatible dentro da mesma versão major

---

> **Convenção:** Esta arquitetura é a espinha dorsal do sistema. Cada decisão foi tomada pensando em: 1 desenvolvedor, 10.000+ tenants, custo mínimo, segurança máxima.
