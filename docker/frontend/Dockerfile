# ============================================================
# Barbershop SaaS — Frontend Dockerfile (Multi-stage)
# ============================================================
# Builds admin panel and public site.

# ---- Stage 0: Base ----
FROM node:22-alpine AS base

RUN corepack enable && corepack prepare pnpm@9 --activate

WORKDIR /app

# ---- Stage 1: Dependencies ----
FROM base AS deps

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/admin/package.json apps/admin/
COPY apps/site/package.json apps/site/
COPY packages/ packages/

RUN pnpm install --frozen-lockfile

# ---- Stage 2: Builder ----
FROM deps AS builder

COPY . .

ARG VITE_API_URL=https://api.barbershop.local
ARG VITE_APP_ENV=production

RUN pnpm build:admin && pnpm build:site

# ---- Stage 3: Production (Nginx) ----
FROM nginx:1.27-alpine AS production

RUN rm -rf /usr/share/nginx/html/*

# Copy built assets
COPY --from=builder /app/apps/admin/dist /usr/share/nginx/html/admin
COPY --from=builder /app/apps/site/dist /usr/share/nginx/html/

# Copy custom nginx config
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost:80/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
