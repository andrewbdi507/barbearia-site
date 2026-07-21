# 04 — Data Dictionary (Dicionário de Dados)

> Dicionário completo de atributos para as entidades principais.  
> Tipo: PostgreSQL. PK = PRIMARY KEY, FK = FOREIGN KEY, UQ = UNIQUE, NN = NOT NULL.

---

## Platform Context

### tenants

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK, DEFAULT uuid7() | Identificador único |
| `subdomain` | VARCHAR(63) | UQ, NN | Subdomínio no barbersaas.com.br |
| `name` | VARCHAR(255) | NN | Nome da empresa |
| `slug` | VARCHAR(255) | UQ, NN | Slug URL-friendly |
| `status` | tenant_status | NN, DEFAULT 'trial' | trial, active, past_due, suspended, cancelled, deleted |
| `plan_id` | UUID | FK → plans.id, NN | Plano contratado |
| `trial_ends_at` | TIMESTAMPTZ | NN | Data fim do trial (created_at + 14d) |
| `metadata` | JSONB | | Dados extensíveis |
| `created_at` | TIMESTAMPTZ | NN, DEFAULT NOW() | Data de criação |
| `updated_at` | TIMESTAMPTZ | NN, DEFAULT NOW() | Última atualização |
| `deleted_at` | TIMESTAMPTZ | | Soft delete |

### plans

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | Identificador |
| `name` | VARCHAR(100) | NN | Starter, Pro, Business, Enterprise |
| `slug` | VARCHAR(100) | UQ, NN | starter, pro, business, enterprise |
| `description` | TEXT | | Descrição do plano |
| `price_monthly` | INTEGER | NN, CHECK(≥0) | Preço mensal em centavos |
| `price_yearly` | INTEGER | CHECK(≥0) | Preço anual em centavos |
| `max_professionals` | INTEGER | CHECK(≥1) | Limite de profissionais |
| `features` | JSONB | NN | Lista de funcionalidades do plano |
| `is_active` | BOOLEAN | NN, DEFAULT true | Plano disponível para venda |
| `sort_order` | INTEGER | NN, DEFAULT 0 | Ordem de exibição |
| `created_at` | TIMESTAMPTZ | NN, DEFAULT NOW() | |

### subscriptions

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | Identificador |
| `tenant_id` | UUID | FK → tenants.id, NN | Tenant assinante |
| `plan_id` | UUID | FK → plans.id, NN | Plano assinado |
| `status` | VARCHAR(30) | NN | active, past_due, cancelled, expired |
| `current_period_start` | DATE | NN | Início do período atual |
| `current_period_end` | DATE | NN | Fim do período atual |
| `cancel_at_period_end` | BOOLEAN | NN, DEFAULT false | Cancela ao fim do período |
| `cancelled_at` | TIMESTAMPTZ | | Data do cancelamento |
| `gateway_subscription_id` | VARCHAR(255) | | ID da assinatura no gateway |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |

---

## Tenant Context

### tenant_settings

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, UQ, NN | |
| `timezone` | VARCHAR(50) | NN, DEFAULT 'America/Sao_Paulo' | Fuso horário |
| `language` | VARCHAR(10) | NN, DEFAULT 'pt-BR' | Idioma |
| `currency` | VARCHAR(3) | NN, DEFAULT 'BRL' | Moeda |
| `date_format` | VARCHAR(20) | NN, DEFAULT 'DD/MM/YYYY' | Formato de data |
| `time_format` | VARCHAR(5) | NN, DEFAULT '24h' | 12h ou 24h |
| `booking_interval_minutes` | INTEGER | NN, DEFAULT 5 | Intervalo entre agendamentos |
| `booking_advance_hours` | INTEGER | NN, DEFAULT 1 | Antecedência mínima para agendar |
| `cancellation_policy_hours` | INTEGER | NN, DEFAULT 2 | Horas limite para cancelar |
| `max_future_bookings_per_customer` | INTEGER | DEFAULT 5 | Limite de agendamentos futuros |
| `require_payment` | BOOLEAN | NN, DEFAULT false | Exigir pagamento para confirmar |
| `deposit_type` | VARCHAR(20) | DEFAULT 'fixed' | fixed, percentage |
| `deposit_value` | INTEGER | DEFAULT 0 | Valor do sinal em centavos |
| `notification_preferences` | JSONB | NN | Canais e preferências |
| `metadata` | JSONB | | Extensível |

### tenant_branding

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, UQ, NN | |
| `logo_url` | VARCHAR(500) | | URL no S3/R2 |
| `logo_dark_url` | VARCHAR(500) | | Logo para dark mode |
| `favicon_url` | VARCHAR(500) | | |
| `banner_url` | VARCHAR(500) | | Banner principal |
| `banner_title` | VARCHAR(255) | | Título sobre banner |
| `banner_subtitle` | VARCHAR(255) | | Subtítulo |
| `banner_cta_text` | VARCHAR(50) | DEFAULT 'Agendar Agora' | Texto do CTA |
| `primary_color` | CHAR(7) | NN, DEFAULT '#1a1a2e' | Hex (#RRGGBB) |
| `secondary_color` | CHAR(7) | NN, DEFAULT '#e94560' | |
| `background_color` | CHAR(7) | NN, DEFAULT '#fafafa' | |
| `surface_color` | CHAR(7) | NN, DEFAULT '#ffffff' | |
| `text_color` | CHAR(7) | NN, DEFAULT '#1a1a2e' | |
| `text_light_color` | CHAR(7) | NN, DEFAULT '#666680' | |
| `heading_font` | VARCHAR(100) | DEFAULT 'Inter' | Google Fonts |
| `body_font` | VARCHAR(100) | DEFAULT 'Inter' | |
| `base_font_size` | INTEGER | DEFAULT 16 | px |
| `border_radius` | INTEGER | DEFAULT 8 | px |
| `layout_template` | VARCHAR(50) | DEFAULT 'classic' | classic, modern, minimal |
| `custom_css` | TEXT | | CSS customizado (Enterprise) |
| `metadata` | JSONB | | |

### business_hours

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `day_of_week` | SMALLINT | NN, CHECK(0-6) | 0=Dom, 6=Sáb |
| `is_closed` | BOOLEAN | NN, DEFAULT false | Fechado neste dia |
| `open_time` | TIME | | Horário abertura |
| `close_time` | TIME | | Horário fechamento |
| `lunch_start` | TIME | | Início almoço |
| `lunch_end` | TIME | | Fim almoço |
| `slot_duration_minutes` | INTEGER | NN, DEFAULT 30 | Duração do slot |

---

## Auth Context

### users

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id | NULL para platform users |
| `email` | VARCHAR(255) | NN | |
| `password_hash` | VARCHAR(255) | NN | bcrypt cost≥12 |
| `name` | VARCHAR(255) | NN | Nome completo |
| `phone` | VARCHAR(20) | | |
| `avatar_url` | VARCHAR(500) | | |
| `role` | user_role | NN | super_admin, admin, manager, receptionist, professional, customer |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| `is_verified` | BOOLEAN | NN, DEFAULT false | Email verificado |
| `email_verified_at` | TIMESTAMPTZ | | |
| `phone_verified_at` | TIMESTAMPTZ | | |
| `last_login_at` | TIMESTAMPTZ | | |
| `last_login_ip` | INET | | |
| `failed_login_attempts` | INTEGER | DEFAULT 0 | Reseta após sucesso |
| `locked_until` | TIMESTAMPTZ | | Bloqueio temporário |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |
| `deleted_at` | TIMESTAMPTZ | | Soft delete |

- UQ parcial: `(tenant_id, email) WHERE deleted_at IS NULL`

### roles

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `name` | VARCHAR(100) | NN | |
| `description` | TEXT | | |
| `permissions` | JSONB | NN | Array de strings de permissão |
| `is_system` | BOOLEAN | NN, DEFAULT false | Não pode ser deletado |
| `created_at` | TIMESTAMPTZ | NN | |

### user_roles

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `user_id` | UUID | FK → users.id, NN | |
| `role_id` | UUID | FK → roles.id, NN | |
| `assigned_at` | TIMESTAMPTZ | NN, DEFAULT NOW() | |
| `assigned_by` | UUID | FK → users.id | Quem atribuiu |
| | | PK: (user_id, role_id) | |

### sessions

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `user_id` | UUID | FK → users.id, NN | |
| `token_hash` | VARCHAR(255) | UQ, NN | SHA-256 do access token |
| `expires_at` | TIMESTAMPTZ | NN | |
| `ip_address` | INET | NN | |
| `user_agent` | TEXT | | |
| `device_info` | JSONB | | |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| `last_activity_at` | TIMESTAMPTZ | NN | |
| `created_at` | TIMESTAMPTZ | NN | |

### refresh_tokens

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `user_id` | UUID | FK → users.id, NN | |
| `token_hash` | VARCHAR(255) | UQ, NN | SHA-256 |
| `family_id` | UUID | NN | Tokens da mesma família |
| `expires_at` | TIMESTAMPTZ | NN | 7 dias |
| `is_revoked` | BOOLEAN | NN, DEFAULT false | |
| `revoked_at` | TIMESTAMPTZ | | |
| `created_at` | TIMESTAMPTZ | NN | |

---

## Scheduling Context

### service_categories

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `name` | VARCHAR(100) | NN | Cabelo, Barba, Tratamentos |
| `description` | TEXT | | |
| `sort_order` | INTEGER | DEFAULT 0 | |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| `color_tag` | CHAR(7) | | Cor para identificação |
| `created_at` | TIMESTAMPTZ | NN | |
| `deleted_at` | TIMESTAMPTZ | | |

### services

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `category_id` | UUID | FK → service_categories.id | |
| `name` | VARCHAR(255) | NN | |
| `description` | TEXT | | |
| `price` | INTEGER | NN, CHECK(≥0) | Centavos |
| `duration_minutes` | INTEGER | NN, CHECK(>0) | |
| `color_tag` | CHAR(7) | | |
| `image_url` | VARCHAR(500) | | |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| `sort_order` | INTEGER | DEFAULT 0 | |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |
| `deleted_at` | TIMESTAMPTZ | | |

- UQ: `(tenant_id, name) WHERE deleted_at IS NULL`

### professionals

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `user_id` | UUID | FK → users.id, UQ | Link opcional ao User |
| `name` | VARCHAR(255) | NN | |
| `bio` | TEXT | | Biografia pública |
| `photo_url` | VARCHAR(500) | | |
| `specialties` | TEXT[] | | Array de tags |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| `is_visible_on_site` | BOOLEAN | NN, DEFAULT true | Exibir no site |
| `commission_percentage` | DECIMAL(5,2) | CHECK(0-100) | % de comissão |
| `commission_type` | VARCHAR(20) | DEFAULT 'none' | none, percentage, fixed |
| `sort_order` | INTEGER | DEFAULT 0 | |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |
| `deleted_at` | TIMESTAMPTZ | | |

### professional_services

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `professional_id` | UUID | FK → professionals.id, NN | |
| `service_id` | UUID | FK → services.id, NN | |
| `custom_price` | INTEGER | | Preço específico (centavos) |
| `custom_duration` | INTEGER | | Duração específica (min) |
| `is_active` | BOOLEAN | NN, DEFAULT true | |
| | | PK: (professional_id, service_id) | |

### schedules

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `professional_id` | UUID | FK → professionals.id, NN | |
| `day_of_week` | SMALLINT | NN, CHECK(0-6) | |
| `is_working` | BOOLEAN | NN, DEFAULT true | |
| `open_time` | TIME | | |
| `close_time` | TIME | | |
| `lunch_start` | TIME | | |
| `lunch_end` | TIME | | |
| `slot_duration_minutes` | INTEGER | | Sobrescreve business_hours |

- UQ: `(professional_id, day_of_week)`

### blocked_dates

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `professional_id` | UUID | FK → professionals.id | NULL = todos |
| `date` | DATE | NN | |
| `reason` | VARCHAR(255) | | Férias, feriado, etc. |
| `block_type` | VARCHAR(20) | NN, DEFAULT 'full_day' | full_day, partial |
| `start_time` | TIME | | Se partial |
| `end_time` | TIME | | Se partial |
| `created_by` | UUID | FK → users.id | |
| `created_at` | TIMESTAMPTZ | NN | |

### bookings

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `customer_id` | UUID | FK → customers.id | NULL = guest |
| `professional_id` | UUID | FK → professionals.id, NN | |
| `date` | DATE | NN | Data do agendamento |
| `start_time` | TIME | NN | Horário início |
| `end_time` | TIME | NN | Horário fim (calculado) |
| `status` | booking_status | NN, DEFAULT 'pending' | |
| `guest_name` | VARCHAR(255) | | Se customer_id NULL |
| `guest_phone` | VARCHAR(20) | | |
| `guest_email` | VARCHAR(255) | | |
| `notes` | TEXT | | Observações do cliente |
| `total_amount` | INTEGER | | Centavos |
| `total_duration_minutes` | INTEGER | | |
| `source` | VARCHAR(30) | DEFAULT 'website' | website, admin, receptionist, instagram, whatsapp |
| `created_by` | UUID | FK → users.id | |
| `cancelled_at` | TIMESTAMPTZ | | |
| `cancelled_by` | UUID | FK → users.id | |
| `cancellation_reason` | TEXT | | |
| `checked_in_at` | TIMESTAMPTZ | | |
| `completed_at` | TIMESTAMPTZ | | |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |

- UQ: `(tenant_id, professional_id, date, start_time)`

---

## Payment Context

### payments

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `booking_id` | UUID | FK → bookings.id, UQ, NN | |
| `gateway_payment_id` | VARCHAR(255) | | ID no gateway |
| `gateway` | VARCHAR(30) | NN | stripe, pagseguro, mercadopago |
| `amount` | INTEGER | NN, CHECK(>0) | Centavos |
| `currency` | VARCHAR(3) | NN, DEFAULT 'BRL' | |
| `status` | payment_status | NN, DEFAULT 'pending' | |
| `payment_method` | VARCHAR(30) | | pix, credit_card, debit_card |
| `paid_at` | TIMESTAMPTZ | | |
| `refunded_at` | TIMESTAMPTZ | | |
| `metadata` | JSONB | | Dados complementares |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |

---

## Customer Context

### customers

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `user_id` | UUID | FK → users.id, UQ | Se tiver conta |
| `name` | VARCHAR(255) | NN | |
| `phone` | VARCHAR(20) | NN | |
| `email` | VARCHAR(255) | | |
| `birth_date` | DATE | | Aniversário |
| `gender` | VARCHAR(20) | | |
| `notes` | TEXT | | Anotações internas |
| `total_visits` | INTEGER | DEFAULT 0 | Counter |
| `total_spent` | INTEGER | DEFAULT 0 | Centavos, counter |
| `last_visit_at` | TIMESTAMPTZ | | |
| `tags` | TEXT[] | | Tags do CRM |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |
| `deleted_at` | TIMESTAMPTZ | | Soft delete (LGPD) |

- UQ: `(tenant_id, phone) WHERE deleted_at IS NULL`

### reviews

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `booking_id` | UUID | FK → bookings.id, UQ, NN | |
| `customer_id` | UUID | FK → customers.id, NN | |
| `professional_id` | UUID | FK → professionals.id, NN | |
| `rating` | SMALLINT | NN, CHECK(1-5) | 1-5 estrelas |
| `comment` | TEXT | | |
| `tags` | TEXT[] | | Tags: "Pontual", "Preço bom", etc. |
| `is_visible` | BOOLEAN | NN, DEFAULT true | |
| `is_anonymous` | BOOLEAN | NN, DEFAULT false | |
| `created_at` | TIMESTAMPTZ | NN | |
| `updated_at` | TIMESTAMPTZ | NN | |

---

## Audit Context

### audit_logs

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| `id` | UUID | PK | |
| `tenant_id` | UUID | FK → tenants.id, NN | |
| `user_id` | UUID | FK → users.id | |
| `event_type` | VARCHAR(100) | NN | booking.created, service.updated, etc. |
| `resource_type` | VARCHAR(100) | NN | booking, service, customer |
| `resource_id` | UUID | | |
| `action` | VARCHAR(20) | NN | create, update, delete, login, logout |
| `changes` | JSONB | | Diff dos dados alterados |
| `ip_address` | INET | | |
| `user_agent` | TEXT | | |
| `request_id` | UUID | | Propagado entre serviços |
| `metadata` | JSONB | | |
| `created_at` | TIMESTAMPTZ | NN | |

- Append-only (sem UPDATE/DELETE). Particionado por `created_at` (mensal).

---

## Resumo de Tipos de Dados

| Tipo PostgreSQL | Uso Principal |
|----------------|---------------|
| UUID | Todas as PKs e FKs |
| VARCHAR(n) | Textos com limite (nomes, emails, URLs) |
| TEXT | Textos longos (descrições, observações) |
| INTEGER | Valores monetários (centavos), contadores, durações |
| DECIMAL(5,2) | Percentuais (comissão) |
| SMALLINT | Enums numéricos (dias, ratings) |
| BOOLEAN | Flags (is_active, is_verified) |
| DATE | Datas (agendamento, nascimento) |
| TIME | Horários (abertura, agendamento) |
| TIMESTAMPTZ | Timestamps com timezone (always UTC) |
| JSONB | Dados semiestruturados, arrays, metadados |
| INET | Endereços IP |
| TEXT[] | Arrays PostgreSQL (tags, specialties) |
| CHAR(7) | Cores hex (#RRGGBB) |
| ENUM (custom type) | Estados (booking_status, payment_status, etc.) |

---

> **Resumo:** O dicionário de dados cobre todas as colunas das entidades principais com seus tipos, constraints e descrições. Valores monetários são sempre em centavos (INTEGER). Timestamps são sempre TIMESTAMPTZ (UTC). JSONB é usado para dados extensíveis sem necessidade de migration. Arrays nativos do PostgreSQL são usados onde faz sentido (tags, specialties).
