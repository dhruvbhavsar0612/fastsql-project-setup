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

## [0.2.0] - 2024-12-24

### Added
- **Comprehensive Documentation Site**: Added MkDocs Material documentation site with 22+ pages
  - Getting Started guides (Installation, Quick Start, First Project tutorial)
  - Configuration guides (Database, Authentication, Admin, Caching, etc.)
  - In-depth guides (Project Structure, Testing, Docker, Migrations, CI/CD)
  - Reference documentation (CLI, Configuration Options)
  - Contributing guidelines and changelog
  - Automatic deployment to GitHub Pages: https://dhruvbhavsar0612.github.io/fastsql-project-setup/
- **Agent Rules and Protocols**: Added comprehensive development guidelines in `agents/` directory
  - Git workflow rules (branch naming, commits, PRs)
  - Documentation update protocols (always use `docs/` prefix)
  - Release process checklist with pre-release tests
  - Code review standards and comment conventions
  - Testing requirements and best practices (80% coverage minimum)
- **GitHub Actions**: Added automated documentation deployment workflow
- **Documentation Badge**: Added docs badge and link to README

### Changed
- Updated project URLs to point to new documentation site
- Enhanced README with documentation link

### Fixed
- Fixed GitHub Pages deployment to use default github.io domain (removed custom domain redirects)

## [0.1.5] - 2024-11-28

### Fixed
- Add missing dependencies to generated `pyproject.toml`:
  - `python-dotenv>=1.0.0` - required by pydantic-settings to load `.env` files
  - `pydantic[email]>=2.7.0` - required for `EmailStr` validation in user schemas
- Convert all relative imports to absolute imports in generated code
  - Changed `from ...module` to `from app.module` pattern
  - Fixes import errors when running generated projects

### Added
- New test cases for dependency and import validation:
  - `test_pyproject_has_required_dependencies`
  - `test_generated_code_uses_absolute_imports_layered`
  - `test_generated_code_uses_absolute_imports_domain_driven`
  - `test_generated_code_uses_absolute_imports_flat`
  - `test_generated_imports_start_with_app`
  - `test_pyproject_has_hatch_wheel_config`

## [0.1.4] - 2024-11-28

### Fixed
- Fix generated projects failing `uv sync` with "Unable to determine which files to ship inside the wheel"
  - Add `[tool.hatch.build.targets.wheel]` section with `packages = ["app"]` to pyproject.toml template
  - This tells hatchling where to find the application package

## [0.1.3] - 2024-11-28

### Fixed
- Fix remaining questionary default value errors for migration tool and AWS services prompts
  - Convert inline dict choices to `Choice` objects in migration tool selection (Alembic/Aerich)
  - Convert inline dict choices to `Choice` objects in AWS services checkbox
  - This fixes "Invalid default value" error when selecting SQLModel + migration tool

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

[Unreleased]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dhruvbhavsar0612/fastsql-project-setup/releases/tag/v0.1.0
