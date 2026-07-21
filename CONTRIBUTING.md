# Guia de Contribuição

## 🚀 Primeiros Passos

1. Leia o [`README.md`](./README.md)
2. Leia a [documentação de arquitetura](./docs/06-arquitetura-geral.md)
3. Configure o ambiente com `make setup`

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação estrita de responsabilidades:

```
Domain (regras de negócio) → Application (casos de uso) → Infrastructure (adaptadores) → Presentation (API)
```

**Regra de ouro:** O domínio NUNCA importa código de camadas externas.

## 📝 Convenções de Código

### Python (Backend)
- Type hints em TODAS as funções públicas
- Docstrings no estilo Google
- Arquivos ≤ 300 linhas
- Funções ≤ 30 linhas
- Black (100 chars) + Ruff + MyPy strict

### TypeScript (Frontend)
- Strict mode, zero `any`
- Componentes funcionais com hooks
- Arquivos ≤ 200 linhas
- Prettier + ESLint

### Geral
- Commits em português, seguindo [Conventional Commits](https://conventionalcommits.org)
- Branches: `feature/*`, `fix/*`, `docs/*`
- PR obrigatório para merge na `main`

## 🔍 Code Review

Todo PR deve:
- Passar lint (Ruff/ESLint)
- Passar type check (MyPy/tsc)
- Passar testes (pytest/vitest)
- Ter cobertura ≥ 80%
- Ser revisado por pelo menos 1 pessoa

## 🧪 Testes

```bash
# Backend
cd backend && uv run pytest -v --cov

# Frontend
cd frontend && pnpm test
```

## 📚 Documentação

- Documente toda função pública
- Atualize o CHANGELOG.md a cada release
- Decisões de arquitetura em `docs/adr/`

---

*Obrigado por contribuir! 🎉*
