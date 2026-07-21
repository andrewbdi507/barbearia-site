# 02 — Entity Catalog (Catálogo de Entidades)

> Catálogo completo de todas as entidades do sistema.  
> Para cada entidade: objetivo, responsabilidade, atributos, relacionamentos, regras, ciclo de vida.

---

## Plataforma (Platform Context)

### 1. Tenant

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Representa uma empresa/cliente da plataforma SaaS |
| **Responsabilidade** | Raiz do isolamento multi-tenant; todo dado de negócio pertence a um tenant |
| **Atributos** | `id` (UUID), `subdomain` (único), `name`, `slug`, `status` (enum tenant_status), `plan_id` (FK), `trial_ends_at`, `created_at`, `updated_at`, `deleted_at` |
| **Relacionamentos** | Plan (N:1), Subscription (1:N), TenantSettings (1:1), TenantBranding (1:1), BusinessHours (1:N), Domain (1:N), SocialMedia (1:N), Media (1:N) |
| **Regras** | Subdomínio único global; trial de 14 dias; status segue máquina de estados |
| **Soft Delete** | ✅ (`deleted_at`) |
| **Ciclo de Vida** | trial → active → (past_due → suspended | cancelled → deleted) |

### 2. Plan

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Define os planos de assinatura disponíveis (Starter, Pro, Business, Enterprise) |
| **Atributos** | `id`, `name`, `slug`, `description`, `price_monthly`, `price_yearly`, `max_professionals`, `features` (JSONB), `is_active`, `sort_order`, `created_at` |
| **Relacionamentos** | Tenant (1:N), Subscription (1:N) |
| **Regras** | Features como JSONB para flexibilidade (cada feature pode ser adicionada sem migration) |
| **Soft Delete** | ❌ (planos são versionados via `is_active`) |

### 3. Subscription

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registra a assinatura de um tenant a um plano |
| **Atributos** | `id`, `tenant_id` (FK), `plan_id` (FK), `status`, `current_period_start`, `current_period_end`, `cancel_at_period_end`, `cancelled_at`, `payment_method`, `gateway_subscription_id`, `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (N:1), Plan (N:1) |
| **Regras** | Cobrança recorrente gerenciada pelo gateway; cancel_at_period_end = true → não renova |
| **Soft Delete** | ❌ (histórico financeiro) |

### 4. PlatformUser

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Super administradores da plataforma (você / CTO) |
| **Atributos** | `id`, `email`, `password_hash`, `name`, `role`, `is_active`, `last_login_at`, `created_at` |
| **Relacionamentos** | Nenhum (acesso cross-tenant por definição) |
| **Regras** | Sem `tenant_id`; acessa qualquer tenant via bypass RLS |
| **Soft Delete** | ✅ |

### 5. FeatureFlag

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Controla liberação gradual de funcionalidades |
| **Atributos** | `id`, `name`, `description`, `enabled_for_all`, `enabled_tenant_ids` (UUID[]), `enabled_percentage`, `created_at` |
| **Relacionamentos** | Nenhum direto (referencia tenants por array de IDs) |
| **Regras** | Permite rollout gradual (10% → 50% → 100%) |

---

## Tenant (Configuração)

### 6. TenantSettings

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Configurações operacionais do tenant |
| **Atributos** | `id`, `tenant_id` (FK, único), `timezone`, `language`, `currency`, `date_format`, `time_format`, `booking_interval_minutes`, `booking_advance_hours`, `cancellation_policy_hours`, `max_future_bookings_per_customer`, `require_payment`, `deposit_type` (fixed/percentage), `deposit_value`, `notification_preferences` (JSONB), `metadata` (JSONB) |
| **Relacionamentos** | Tenant (1:1) |
| **Regras** | Configurações padrão no create; alterações registradas em audit_log |
| **Soft Delete** | ❌ (vinculado ao tenant) |

### 7. TenantBranding

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Identidade visual e tema do site do tenant |
| **Atributos** | `id`, `tenant_id` (FK, único), `logo_url`, `logo_dark_url`, `favicon_url`, `banner_url`, `banner_title`, `banner_subtitle`, `banner_cta_text`, `primary_color`, `secondary_color`, `background_color`, `surface_color`, `text_color`, `text_light_color`, `heading_font`, `body_font`, `base_font_size`, `border_radius`, `layout_template`, `custom_css` (text), `metadata` (JSONB) |
| **Relacionamentos** | Tenant (1:1) |
| **Regras** | Design tokens armazenados diretamente (flat) para performance; alterações invalidam cache CDN |
| **Soft Delete** | ❌ (vinculado ao tenant) |

### 8. BusinessHours

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Horários de funcionamento do tenant por dia da semana |
| **Atributos** | `id`, `tenant_id` (FK), `day_of_week` (0-6), `is_closed`, `open_time`, `close_time`, `lunch_start`, `lunch_end`, `slot_duration_minutes` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Um registro por dia da semana; slot_duration padrão = 30 min; usado para gerar grid de horários |
| **Soft Delete** | ❌ |

### 9. Domain

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Domínios associados ao tenant (subdomínio padrão + domínio próprio) |
| **Atributos** | `id`, `tenant_id` (FK), `domain_name`, `is_primary`, `is_verified`, `verified_at`, `ssl_status`, `dns_instructions` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Subdomínio padrão é sempre primary até domínio próprio ser verificado |
| **Soft Delete** | ✅ |

### 10. SocialMedia

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Links de redes sociais do tenant |
| **Atributos** | `id`, `tenant_id` (FK), `platform` (instagram, facebook, tiktok, youtube, twitter), `url`, `is_visible`, `sort_order` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Exibidos no footer do site público |
| **Soft Delete** | ❌ |

### 11. Media

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Arquivos de mídia do tenant (galeria, fotos, uploads) |
| **Atributos** | `id`, `tenant_id` (FK), `uploaded_by` (FK User), `type` (enum: logo, banner, gallery, professional_photo, service_photo), `filename`, `original_name`, `mime_type`, `size_bytes`, `url`, `thumbnail_url`, `width`, `height`, `alt_text`, `title`, `sort_order`, `is_visible`, `metadata` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1), User (N:1 — quem fez upload) |
| **Regras** | Armazenado no S3/R2 com prefixo `/{tenant_id}/`; processamento assíncrono (WebP); soft delete para permitir recuperação |
| **Soft Delete** | ✅ |

### 12. SEOSettings

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Configurações de SEO do site público |
| **Atributos** | `id`, `tenant_id` (FK, único), `meta_title`, `meta_description`, `og_image_url`, `google_analytics_id`, `facebook_pixel_id`, `custom_header_code`, `custom_footer_code`, `robots_txt`, `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (1:1) |
| **Regras** | custom_header_code e custom_footer_code sanitizados (sem <script> malicioso no MVP) |
| **Soft Delete** | ❌ |

---

## Auth (Usuários e Permissões)

### 13. User

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Usuários do tenant (admin, barbeiro, recepcionista, cliente) |
| **Atributos** | `id`, `tenant_id` (FK), `email`, `password_hash`, `name`, `phone`, `avatar_url`, `role` (enum user_role), `is_active`, `is_verified`, `email_verified_at`, `phone_verified_at`, `last_login_at`, `last_login_ip`, `failed_login_attempts`, `locked_until`, `metadata` (JSONB), `created_at`, `updated_at`, `deleted_at` |
| **Relacionamentos** | Tenant (N:1), Role (N:N via user_roles), Session (1:N), RefreshToken (1:N), Professional (1:1 — se role=professional) |
| **Regras** | Email único por tenant; senha bcrypt cost≥12; lockout 5 tentativas/15min |
| **Soft Delete** | ✅ |

### 14. Role

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Papéis de usuário com conjunto de permissões |
| **Atributos** | `id`, `tenant_id` (FK), `name`, `description`, `permissions` (JSONB — array de strings), `is_system` (não pode ser deletado), `created_at` |
| **Relacionamentos** | User (N:N via user_roles), Tenant (N:1) |
| **Regras** | Roles de sistema: admin, manager, receptionist, professional, customer; tenants podem criar roles customizados |
| **Soft Delete** | ❌ (roles são referenciados por users) |

### 15. UserRole

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Tabela associativa User ↔ Role |
| **Atributos** | `user_id` (FK), `role_id` (FK), `assigned_at`, `assigned_by` (FK User) |
| **Relacionamentos** | User (N:1), Role (N:1) |
| **Regras** | Um user pode ter múltiplas roles; permissão efetiva = união das permissões |

### 16. Session

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Sessões ativas de usuários |
| **Atributos** | `id`, `user_id` (FK), `token_hash`, `expires_at`, `ip_address`, `user_agent`, `device_info` (JSONB), `is_active`, `last_activity_at`, `created_at` |
| **Relacionamentos** | User (N:1) |
| **Regras** | Expiração: 15 minutos (access token); renovável via refresh token |

### 17. RefreshToken

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Refresh tokens para renovação de sessão |
| **Atributos** | `id`, `user_id` (FK), `token_hash`, `family_id` (UUID — tokens da mesma família), `expires_at`, `is_revoked`, `revoked_at`, `created_at` |
| **Relacionamentos** | User (N:1) |
| **Regras** | Rotação a cada uso; família inteira revogada se detectado reuso (proteção contra roubo) |

### 18. PasswordReset

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Tokens de recuperação de senha |
| **Atributos** | `id`, `user_id` (FK), `token_hash`, `expires_at`, `used_at`, `created_at` |
| **Relacionamentos** | User (N:1) |
| **Regras** | Expira em 1 hora; uso único; invalidado ao usar ou expirar |

---

## Scheduling (Agendamento)

### 19. ServiceCategory

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Categorias de serviços (ex: Cabelo, Barba, Tratamentos) |
| **Atributos** | `id`, `tenant_id` (FK), `name`, `description`, `sort_order`, `is_active`, `color_tag`, `created_at` |
| **Relacionamentos** | Service (1:N), Tenant (N:1) |
| **Soft Delete** | ✅ |

### 20. Service

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Serviços oferecidos pelo tenant |
| **Atributos** | `id`, `tenant_id` (FK), `category_id` (FK, opcional), `name`, `description`, `price` (integer, centavos), `duration_minutes`, `color_tag`, `image_url`, `is_active`, `sort_order`, `metadata` (JSONB), `created_at`, `updated_at`, `deleted_at` |
| **Relacionamentos** | ServiceCategory (N:1), Tenant (N:1), Professional (N:N via professional_services), Booking (N:N via booking_services) |
| **Regras** | Preço em centavos (ex: R$ 45,00 = 4500); duração usada para calcular slot |
| **Soft Delete** | ✅ (histórico de bookings referencia serviço) |

### 21. Professional

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Profissionais que realizam serviços (barbeiros, cabeleireiros, etc.) |
| **Atributos** | `id`, `tenant_id` (FK), `user_id` (FK, opcional — link ao User se tiver login), `name`, `bio`, `photo_url`, `specialties` (TEXT[]), `is_active`, `is_visible_on_site`, `commission_percentage`, `commission_type` (none, percentage, fixed), `sort_order`, `metadata` (JSONB), `created_at`, `updated_at`, `deleted_at` |
| **Relacionamentos** | Tenant (N:1), User (1:1 opcional), Service (N:N via professional_services), Schedule (1:N), Booking (1:N) |
| **Regras** | Um profissional pode realizar múltiplos serviços; comissão opcional |
| **Soft Delete** | ✅ |

### 22. ProfessionalService

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Tabela associativa: quais serviços cada profissional realiza |
| **Atributos** | `professional_id` (FK), `service_id` (FK), `custom_price` (opcional — preço diferente do padrão), `custom_duration` (opcional), `is_active` |
| **Relacionamentos** | Professional (N:1), Service (N:1) |
| **Regras** | Preço e duração customizados por profissional; se nulo, usa do Service |

### 23. Schedule

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Horários de trabalho específicos de cada profissional |
| **Atributos** | `id`, `tenant_id` (FK), `professional_id` (FK), `day_of_week` (0-6), `is_working`, `open_time`, `close_time`, `lunch_start`, `lunch_end`, `slot_duration_minutes` |
| **Relacionamentos** | Tenant (N:1), Professional (N:1) |
| **Regras** | Sobrescreve BusinessHours do tenant se definido; um registro por dia por profissional |
| **Soft Delete** | ❌ |

### 24. BlockedDate

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Datas bloqueadas (férias, folgas, feriados) |
| **Atributos** | `id`, `tenant_id` (FK), `professional_id` (FK — NULL = todos), `date`, `reason`, `block_type` (full_day, partial), `start_time`, `end_time`, `created_by` (FK User) |
| **Relacionamentos** | Tenant (N:1), Professional (N:1 opcional) |
| **Regras** | Se professional_id é NULL, bloqueia todos os profissionais (feriado da barbearia) |
| **Soft Delete** | ❌ |

### 25. Customer

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Clientes finais (quem agenda) |
| **Atributos** | `id`, `tenant_id` (FK), `user_id` (FK opcional — se tiver conta), `name`, `phone`, `email`, `birth_date`, `gender`, `notes` (anotações internas), `total_visits`, `total_spent`, `last_visit_at`, `tags` (TEXT[]), `metadata` (JSONB), `created_at`, `updated_at`, `deleted_at` |
| **Relacionamentos** | Tenant (N:1), User (1:1 opcional), Booking (1:N), Review (1:N), Consent (1:N) |
| **Regras** | Telefone único por tenant (identificador); pode existir sem user (guest); total_visits e total_spent são counters (atualizados via trigger ou batch) |
| **Soft Delete** | ✅ (LGPD — exclusão lógica 30d, depois anonimização) |

### 26. CustomerPreference

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Preferências do cliente (barbeiro favorito, serviços preferidos) |
| **Atributos** | `id`, `customer_id` (FK), `favorite_professional_id` (FK), `preferred_services` (UUID[]), `communication_preferences` (JSONB), `created_at`, `updated_at` |
| **Relacionamentos** | Customer (1:1) |
| **Regras** | Dados usados para "Repetir último agendamento" e sugestões |
| **Soft Delete** | ❌ (vinculado ao customer) |

### 27. Consent

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de consentimentos LGPD |
| **Atributos** | `id`, `tenant_id` (FK), `customer_id` (FK), `consent_type` (privacy_policy, terms_of_service, marketing_emails, marketing_whatsapp), `is_granted`, `consent_version`, `ip_address`, `user_agent`, `granted_at`, `revoked_at` |
| **Relacionamentos** | Tenant (N:1), Customer (N:1) |
| **Regras** | Registro imutável (append-only); versão do termo aceita |
| **Soft Delete** | ❌ (registro legal, nunca deletar) |

### 28. Booking

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Agendamento — entidade central do sistema |
| **Atributos** | `id`, `tenant_id` (FK), `customer_id` (FK, nullable — guest), `professional_id` (FK), `date`, `start_time`, `end_time`, `status` (enum booking_status), `guest_name`, `guest_phone`, `guest_email`, `notes`, `total_amount`, `total_duration_minutes`, `source` (website, admin, receptionist, instagram, whatsapp), `created_by` (FK User, nullable), `cancelled_at`, `cancelled_by` (FK User), `cancellation_reason`, `checked_in_at`, `completed_at`, `metadata` (JSONB), `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (N:1), Customer (N:1 opcional), Professional (N:1), Service (N:N via booking_services), Payment (1:1), BookingStatusLog (1:N), Review (1:1), Waitlist (1:N) |
| **Regras** | Sem double-booking (unique constraint); guest info se customer_id nulo; status segue máquina de estados |
| **Soft Delete** | ❌ (cancelamento é status, não deleção) |

### 29. BookingService

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Serviços incluídos em um agendamento (N:N) |
| **Atributos** | `booking_id` (FK), `service_id` (FK), `service_name` (snapshot), `price` (snapshot, centavos), `duration_minutes` (snapshot) |
| **Relacionamentos** | Booking (N:1), Service (N:1) |
| **Regras** | Snapshot do serviço no momento do booking (se serviço mudar depois, booking não é afetado) |
| **Soft Delete** | ❌ |

### 30. BookingStatusLog

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Histórico de mudanças de status do booking |
| **Atributos** | `id`, `booking_id` (FK), `from_status`, `to_status`, `changed_by` (FK User, nullable), `ip_address`, `notes`, `created_at` |
| **Relacionamentos** | Booking (N:1) |
| **Regras** | Registro imutável (append-only) para auditoria |
| **Soft Delete** | ❌ |

### 31. Waitlist

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Lista de espera para horários lotados |
| **Atributos** | `id`, `tenant_id` (FK), `customer_id` (FK), `professional_id` (FK, opcional), `desired_date`, `desired_period` (morning, afternoon, evening), `status` (waiting, notified, booked, expired, cancelled), `notified_at`, `expires_at`, `created_at` |
| **Relacionamentos** | Tenant (N:1), Customer (N:1), Professional (N:1) |
| **Regras** | Notificado quando slot libera; expira em 24h se não agendar |
| **Soft Delete** | ❌ (status managed) |

---

## Payment (Pagamentos)

### 32. Payment

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de pagamento (NUNCA contém dados de cartão) |
| **Atributos** | `id`, `tenant_id` (FK), `booking_id` (FK, único), `gateway_payment_id`, `gateway` (stripe, pagseguro, mercadopago), `amount` (centavos), `currency`, `status` (enum payment_status), `payment_method` (pix, credit_card, debit_card), `paid_at`, `refunded_at`, `metadata` (JSONB), `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (N:1), Booking (1:1), PaymentEvent (1:N), Refund (1:N) |
| **Regras** | NUNCA armazenar card_number, cvv, expiry; status via webhook |
| **Soft Delete** | ❌ (registro financeiro imutável) |

### 33. PaymentEvent

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Event sourcing dos pagamentos (cada mudança de status) |
| **Atributos** | `id`, `payment_id` (FK), `event_type`, `gateway_raw_data` (JSONB), `ip_address`, `created_at` |
| **Relacionamentos** | Payment (N:1) |
| **Regras** | Append-only; gateway_raw_data contém o payload bruto do webhook |
| **Soft Delete** | ❌ |

### 34. Refund

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de reembolso |
| **Atributos** | `id`, `payment_id` (FK), `amount` (centavos), `reason`, `gateway_refund_id`, `status`, `requested_by` (FK User), `created_at` |
| **Relacionamentos** | Payment (N:1) |
| **Regras** | Soma dos refunds ≤ payment.amount; pode ser múltiplos (partial refunds) |
| **Soft Delete** | ❌ |

### 35. GatewayConfig

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Configuração dos gateways de pagamento |
| **Atributos** | `id`, `tenant_id` (FK), `gateway`, `is_active`, `api_key_encrypted`, `webhook_secret_encrypted`, `settings` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Chaves criptografadas (AES-256-GCM); cada tenant pode ter múltiplos gateways |
| **Soft Delete** | ✅ |

---

## Notification (Notificações)

### 36. NotificationTemplate

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Templates de mensagem por tipo de evento |
| **Atributos** | `id`, `tenant_id` (FK), `event_type`, `channel` (whatsapp, email, sms, push), `subject`, `body_template`, `is_default`, `is_active`, `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Templates padrão do sistema (is_default=true); tenant pode customizar |
| **Soft Delete** | ✅ |

### 37. Notification

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de envio de notificação |
| **Atributos** | `id`, `tenant_id` (FK), `user_id` (FK), `customer_id` (FK), `booking_id` (FK), `channel`, `status` (pending, sent, delivered, read, failed), `content`, `error_message`, `retry_count`, `sent_at`, `delivered_at`, `read_at`, `created_at` |
| **Relacionamentos** | Tenant, User, Customer, Booking (todas opcionais) |
| **Regras** | Retry: 5 tentativas com backoff; falha total → DLQ |
| **Soft Delete** | ❌ |

---

## Marketing (Promoções e Fidelidade)

### 38. Coupon

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Cupons de desconto |
| **Atributos** | `id`, `tenant_id` (FK), `code` (único por tenant), `discount_type` (percentage, fixed), `discount_value`, `min_purchase_amount`, `max_uses`, `current_uses`, `starts_at`, `expires_at`, `is_active`, `applies_to` (all, specific_services, specific_professionals), `applicable_ids` (UUID[]), `created_by` (FK User), `created_at` |
| **Relacionamentos** | Tenant (N:1), Booking (N:N via booking_coupons) |
| **Regras** | Código único por tenant; validade por data e/ou quantidade de usos |
| **Soft Delete** | ✅ |

### 39. Campaign

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Campanhas de marketing automatizadas |
| **Atributos** | `id`, `tenant_id` (FK), `name`, `type` (return_30days, birthday, reactivation, promotion), `target_segment` (JSONB), `template_id` (FK), `is_active`, `schedule` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1), NotificationTemplate (N:1) |
| **Regras** | Segmentação por: dias sem visitar, total gasto, aniversário, serviços |
| **Soft Delete** | ✅ |

### 40. LoyaltyPoints

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Programa de pontos de fidelidade |
| **Atributos** | `id`, `tenant_id` (FK), `customer_id` (FK), `points`, `total_earned`, `total_spent`, `updated_at` |
| **Relacionamentos** | Tenant (N:1), Customer (1:1) |
| **Regras** | 1 ponto por R$ 1 gasto; resgate via catálogo de recompensas |
| **Soft Delete** | ❌ (vinculado ao customer) |

### 41. LoyaltyTransaction

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Histórico de transações de pontos |
| **Atributos** | `id`, `loyalty_id` (FK), `type` (earn, redeem, expire, adjustment), `points`, `reference_type`, `reference_id`, `description`, `created_at` |
| **Relacionamentos** | LoyaltyPoints (N:1) |
| **Regras** | Append-only; referência ao booking que gerou pontos |
| **Soft Delete** | ❌ |

### 42. Referral

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Programa de indicação |
| **Atributos** | `id`, `tenant_id` (FK), `referrer_id` (FK Customer), `referral_code` (único), `referred_name`, `referred_phone`, `status` (pending, registered, booked, rewarded), `reward_granted_at`, `created_at` |
| **Relacionamentos** | Tenant (N:1), Customer (N:1 — referrer) |
| **Regras** | Recompensa quando referido agenda; código único por referrer |
| **Soft Delete** | ❌ |

### 43. Review

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Avaliações de clientes pós-atendimento |
| **Atributos** | `id`, `tenant_id` (FK), `booking_id` (FK, único), `customer_id` (FK), `professional_id` (FK), `rating` (1-5), `comment`, `tags` (TEXT[]), `is_visible`, `is_anonymous`, `created_at`, `updated_at` |
| **Relacionamentos** | Tenant (N:1), Booking (1:1), Customer (N:1), Professional (N:1) |
| **Regras** | Um review por booking; tags sugeridas: "Pontual", "Atendimento ótimo", etc. |
| **Soft Delete** | ✅ |

---

## Audit (Auditoria e Logs)

### 44. AuditLog

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de auditoria de todas as ações do sistema |
| **Atributos** | `id`, `tenant_id` (FK), `user_id` (FK, opcional), `event_type`, `resource_type`, `resource_id`, `action` (create, update, delete, login, logout, export), `changes` (JSONB — diff), `ip_address`, `user_agent`, `request_id`, `metadata` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Append-only (sem UPDATE/DELETE); retenção: 5 anos; particionamento por mês |
| **Soft Delete** | ❌ (append-only) |

### 45. LoginLog

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Registro de tentativas de login (sucesso e falha) |
| **Atributos** | `id`, `tenant_id` (FK, opcional), `email_attempted`, `user_id` (FK, opcional), `success`, `failure_reason`, `ip_address`, `user_agent`, `created_at` |
| **Relacionamentos** | Tenant (N:1), User (N:1) |
| **Regras** | Retenção: 1 ano; particionamento por mês; usado para detectar ataques brute-force |
| **Soft Delete** | ❌ |

### 46. SecurityEvent

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Eventos de segurança (cross-tenant, rate limit, bloqueios) |
| **Atributos** | `id`, `tenant_id` (FK, opcional), `event_type`, `severity` (low, medium, high, critical), `description`, `source_ip`, `metadata` (JSONB), `resolved_at`, `created_at` |
| **Relacionamentos** | Tenant (N:1) |
| **Regras** | Eventos críticos disparam alerta; investigação e resolução registradas |
| **Soft Delete** | ❌ |

---

## IA (Inteligência Artificial — V4)

### 47. AIPrompt

| Atributo | Descrição |
|----------|-----------|
| **Objetivo** | Histórico de prompts enviados para IA |
| **Atributos** | `id`, `tenant_id` (FK), `user_id` (FK), `prompt_type`, `prompt_text`, `response_text`, `model_used`, `tokens_used`, `metadata` (JSONB), `created_at` |
| **Relacionamentos** | Tenant (N:1), User (N:1) |
| **Regras** | Usado para: sugestões de resposta, análise de reviews, campanhas automáticas |
| **Soft Delete** | ✅ |

---

## 48. Contagem Total de Entidades

| Contexto | Entidades |
|----------|:---------:|
| Platform | 5 |
| Tenant | 7 |
| Auth | 6 |
| Scheduling | 13 |
| Payment | 4 |
| Notification | 2 |
| Marketing | 6 |
| Audit | 3 |
| IA (futuro) | 1 |
| **Total** | **47 entidades** |

---

> **Resumo:** O catálogo contém 47 entidades distribuídas em 9 contextos. Cada entidade tem propósito, responsabilidade e ciclo de vida claramente definidos. O design prioriza: segurança (RLS, criptografia), rastreabilidade (audit logs, event sourcing), e flexibilidade (JSONB para dados semiestruturados).
