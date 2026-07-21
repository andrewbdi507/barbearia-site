-- Barbershop SaaS — Database Initialization
-- This script runs once when the PostgreSQL container starts.

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "citext";

-- Create custom enum types (will be managed by Alembic in production)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tenant_status') THEN
        CREATE TYPE tenant_status AS ENUM (
            'trial', 'active', 'past_due', 'suspended', 'cancelled', 'deleted'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'booking_status') THEN
        CREATE TYPE booking_status AS ENUM (
            'pending', 'confirmed', 'checked_in', 'in_progress',
            'completed', 'cancelled', 'no_show', 'expired'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_status') THEN
        CREATE TYPE payment_status AS ENUM (
            'pending', 'processing', 'paid', 'failed',
            'refunded', 'partially_refunded', 'expired'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM (
            'super_admin', 'admin', 'manager', 'receptionist', 'professional', 'customer'
        );
    END IF;
END
$$;

-- ============================================================
-- Note: Full schema is managed via Alembic migrations.
-- This file only sets up extensions and base types.
-- ============================================================
