# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [0.1.2] - 2024-11-28

### Fixed
- Fix questionary default value error by using `Choice` objects instead of plain dicts
  - The `make_choices()` function now returns `list[Choice]` for proper default value handling
  - This fixes the "Invalid default value" error when selecting Python version

## [0.1.1] - 2024-11-27

### Fixed
- Fix CI workflow: use `uv sync --extra dev` for optional dependencies
- Fix ruff formatting issues in generator.py, prompts.py, test_config.py
- Fix test_help to handle ANSI escape codes in CLI output
- Fix generator to use correct package name (fastapi_smith)
- Fix mypy type errors in prompts.py

### Added
- Add uv.lock file for dependency caching
- Add comprehensive test_generator.py with 7 new tests

## [0.1.0] - 2024-11-27

### Added
- Initial release of fastapi-smith
- Interactive CLI for scaffolding FastAPI projects
- Database support:
  - PostgreSQL with psycopg3 driver
  - MySQL with asyncmy driver
  - SQLite with aiosqlite driver
- ORM support:
  - SQLAlchemy 2.0
  - SQLModel
  - Tortoise-ORM
- Authentication methods:
  - JWT (JSON Web Tokens)
  - OAuth2
  - Session-based
- Admin panel integration with SQLAdmin
- Caching backends:
  - Redis
  - Memcached
  - In-memory
- Message brokers:
  - RabbitMQ
  - Redis
- Task queues:
  - Celery
  - ARQ
  - Taskiq
  - Built-in BackgroundTasks
- Logging libraries:
  - Loguru
  - structlog
  - Standard library logging
- Type checking:
  - mypy (strict and standard modes)
  - Pyrefly
- Linting/Formatting:
  - Ruff
  - Black + isort
- Docker support:
  - Multi-stage Dockerfile
  - docker-compose.yml with services
- GitHub Actions workflows:
  - CI (lint, test, build)
  - Deploy workflow
- AWS integration:
  - S3 (object storage)
  - SES (email service)
  - ECR (container registry)
  - ECS (container orchestration)
- Multiple project structures:
  - Layered (routes/services/repositories)
  - Domain-Driven (by feature)
  - Flat (simple)
- Database migrations with Alembic/Aerich
- Pre-commit hooks configuration
- Pytest testing setup
- Health check endpoints
- Rate limiting with slowapi
- CORS configuration

[Unreleased]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/releases/tag/v0.1.0
