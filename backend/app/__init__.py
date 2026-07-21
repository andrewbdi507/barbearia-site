"""Barbershop SaaS — Backend Application.

Clean Architecture com separação estrita de camadas:

app/
├── core/            # Kernel: config, exceptions, logging, security
├── shared/          # Utilitários e tipos compartilhados
├── modules/         # Módulos de domínio (DDD)
│   ├── auth/        # Autenticação, autorização, RBAC
│   ├── tenant/      # Multi-tenancy, configurações, branding
│   ├── scheduling/  # Agendamentos, serviços, profissionais
│   ├── customer/    # Clientes, CRM, fidelidade
│   ├── payment/     # Pagamentos, gateways, webhooks
│   ├── notification/# Notificações multicanal
│   ├── media/       # Upload, storage, processamento
│   ├── analytics/   # Métricas e relatórios (futuro)
│   └── audit/       # Logs de auditoria (futuro)
├── infrastructure/  # Adaptadores (DB, Redis, HTTP, Events, Workers)
└── presentation/    # API REST (rotas, middleware, schemas)
"""
