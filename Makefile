# ============================================================
# Barbershop SaaS — Makefile
# Comandos de produtividade para desenvolvimento.
# ============================================================

.PHONY: help up down setup backend frontend test lint clean

# Cores para output
GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
NC     := \033[0m

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================
# Docker
# ============================================================

up: ## Inicia serviços de desenvolvimento
	@echo "$(YELLOW)🐳 Iniciando desenvolvimento...$(NC)"
	docker compose -f docker-compose.dev.yml up -d
	@echo "$(GREEN)✅ Dev stack iniciada!$(NC)"
	@echo "  API:    http://localhost:8000"
	@echo "  Docs:   http://localhost:8000/docs"

up-full: ## Inicia stack completa (com frontend + workers)
	@echo "$(YELLOW)🐳 Iniciando stack completa...$(NC)"
	docker compose -f docker-compose.dev.yml --profile full up -d
	@echo "$(GREEN)✅ Stack completa iniciada!$(NC)"
	@echo "  API:    http://localhost:8000"
	@echo "  Admin:  http://localhost:5173"
	@echo "  Nginx:  http://localhost"

down: ## Para todos os serviços Docker
	@echo "$(YELLOW)🛑 Parando serviços...$(NC)"
	docker compose -f docker-compose.dev.yml down
	@echo "$(GREEN)✅ Serviços parados.$(NC)"

restart: down up ## Reinicia todos os serviços

logs: ## Segue logs de todos os serviços
	docker compose logs -f

logs-backend: ## Segue logs do backend
	docker compose logs -f backend

# ============================================================
# Setup
# ============================================================

setup: ## Configura o ambiente de desenvolvimento completo
	@echo "$(YELLOW)🔧 Configurando ambiente...$(NC)"
	@echo "  → Backend..."
	cd backend && uv sync --dev && uv run pre-commit install
	@echo "  → Frontend..."
	cd frontend && pnpm install
	@echo "  → Docker..."
	docker compose up -d
	@echo "  → Migrations..."
	cd backend && uv run alembic upgrade head
	@echo "$(GREEN)✅ Ambiente configurado!$(NC)"

# ============================================================
# Backend
# ============================================================

backend: ## Inicia o servidor backend (dev)
	cd backend && uv run uvicorn app.presentation.api.app:create_app --factory --reload

backend-test: ## Roda testes do backend
	cd backend && uv run pytest -v --cov

backend-lint: ## Roda lint do backend
	cd backend && uv run ruff check app/ tests/ && uv run mypy app/

# ============================================================
# Frontend
# ============================================================

frontend-admin: ## Inicia painel admin (dev)
	cd frontend && pnpm dev:admin

frontend-site: ## Inicia site público (dev)
	cd frontend && pnpm dev:site

frontend-build: ## Build de produção do frontend
	cd frontend && pnpm build:admin && pnpm build:site

# ============================================================
# Qualidade
# ============================================================

lint: ## Roda lint em todo o projeto
	@echo "$(YELLOW)🔍 Linting...$(NC)"
	cd backend && uv run ruff check app/ tests/
	cd frontend && pnpm lint
	@echo "$(GREEN)✅ Lint concluído.$(NC)"

typecheck: ## Roda verificação de tipos
	@echo "$(YELLOW)🔍 Type checking...$(NC)"
	cd backend && uv run mypy app/
	cd frontend && pnpm typecheck
	@echo "$(GREEN)✅ Type check concluído.$(NC)"

test: ## Roda todos os testes
	@echo "$(YELLOW)🧪 Testando...$(NC)"
	cd backend && uv run pytest -v
	cd frontend && pnpm test
	@echo "$(GREEN)✅ Testes concluídos.$(NC)"

# ============================================================
# Utilidades
# ============================================================

migrate: ## Gera e aplica migrations
	cd backend && uv run alembic revision --autogenerate -m "auto"
	cd backend && uv run alembic upgrade head

clean: ## Limpa arquivos temporários
	@echo "$(YELLOW)🧹 Limpando...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -not -path "*/node_modules/*" -prune

# ============================================================
# DevOps / Infra
# ============================================================

staging-up: ## Inicia ambiente de staging
	@echo "$(YELLOW)🚀 Iniciando staging...$(NC)"
	docker compose -f docker-compose.staging.yml up -d
	@echo "$(GREEN)✅ Staging: http://localhost$(NC)"

staging-down: ## Para ambiente de staging
	docker compose -f docker-compose.staging.yml down

prod-up: ## Inicia ambiente de produção
	@echo "$(RED)⚠️  Iniciando PRODUÇÃO...$(NC)"
	docker compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✅ Produção iniciada.$(NC)"

prod-ps: ## Status dos serviços em produção
	docker compose -f docker-compose.prod.yml ps

test-ci: ## Roda testes em ambiente CI (containers efêmeros)
	@echo "$(YELLOW)🧪 CI Test Suite...$(NC)"
	docker compose -f docker-compose.test.yml up -d postgres-test redis-test
	sleep 5
	docker compose -f docker-compose.test.yml run --rm backend-test
	docker compose -f docker-compose.test.yml down

backup-db: ## Backup manual do banco de dados
	@echo "$(YELLOW)💾 Backup do banco...$(NC)"
	bash scripts/backup-db.sh manual

backup-uploads: ## Backup dos uploads
	@echo "$(YELLOW)📁 Backup dos uploads...$(NC)"
	bash scripts/backup-uploads.sh

restore-db: ## Restaura banco (usage: make restore-db FILE=path/to/dump.gz)
	@echo "$(RED)⚠️  RESTAURAR BANCO: $(FILE)$(NC)"
	bash scripts/restore-db.sh $(FILE)

build-images: ## Build de todas as imagens Docker
	@echo "$(YELLOW)🐳 Buildando imagens...$(NC)"
	docker compose -f docker-compose.prod.yml build

shell-backend: ## Shell no container backend
	docker compose -f docker-compose.dev.yml exec backend bash

shell-db: ## Shell psql no banco
	docker compose -f docker-compose.dev.yml exec postgres psql -U barbershop -d barbershop_dev

grafana: ## Abre Grafana (localhost:3000)
	@echo "$(GREEN)Grafana: http://localhost:3000 (admin / ver .env)$(NC)"

prometheus: ## Abre Prometheus (localhost:9090)
	@echo "$(GREEN)Prometheus: http://localhost:9090$(NC)"
	rm -rf backend/.mypy_cache frontend/.turbo
	@echo "$(GREEN)✅ Limpo.$(NC)"
