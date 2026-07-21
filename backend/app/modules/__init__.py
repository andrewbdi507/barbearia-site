"""Modules — Domain Modules.

Cada módulo segue Clean Architecture internamente:
domain/ → application/ → infrastructure/ → presentation/

domain/:       Entidades, Value Objects, Interfaces (ports)
application/:  Casos de uso, DTOs
infrastructure/: Adaptadores concretos (repositórios, serviços externos)
presentation/:  Rotas API, schemas, dependências FastAPI
"""
