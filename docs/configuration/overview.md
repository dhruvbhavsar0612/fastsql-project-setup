# Configuration Overview

FastAPI Smith offers extensive configuration options to tailor your project exactly to your needs. This page provides an overview of all available options.

## Configuration Categories

### Project Basics
- Project name and description
- Author information
- Python version (3.10, 3.11, 3.12, 3.13)

### Database & ORM
Choose from multiple database and ORM combinations:

| Category | Options |
|----------|---------|
| **Databases** | PostgreSQL, MySQL, SQLite |
| **ORMs** | SQLAlchemy 2.0, SQLModel, Tortoise-ORM |
| **Migrations** | Alembic (SQLAlchemy/SQLModel), Aerich (Tortoise) |

[Learn more →](database.md)

### Authentication
Secure your API with built-in authentication:

| Type | Features |
|------|----------|
| **JWT** | Access & refresh tokens, automatic expiry |
| **OAuth2** | Password flow with bearer tokens |
| **Session** | Server-side sessions with cookies |
| **None** | Skip authentication entirely |

[Learn more →](authentication.md)

### Admin Panel
- **SQLAdmin** - Beautiful admin interface for SQLAlchemy/SQLModel models
- Automatic CRUD operations
- Customizable views and forms

[Learn more →](admin.md)

### Caching
Speed up your API with caching:

- **Redis** - Distributed caching, pub/sub support
- **Memcached** - High-performance in-memory caching
- **In-memory** - Simple local caching for development

[Learn more →](caching.md)

### Task Queues & Background Jobs
Handle long-running tasks asynchronously:

| Broker | Task Libraries |
|--------|---------------|
| **RabbitMQ** | Celery, Taskiq |
| **Redis** | Celery, ARQ, Taskiq |
| **None** | FastAPI BackgroundTasks |

[Learn more →](tasks.md)

### Logging & Monitoring
Production-grade logging and error tracking:

| Feature | Options |
|---------|---------|
| **Logging** | Loguru, structlog, standard library |
| **Error Tracking** | Sentry integration |
| **Health Checks** | Kubernetes-ready endpoints |
| **Metrics** | Request timing, database monitoring |

[Learn more →](logging.md)

### Development Tools

#### Package Management
- **uv** - Fast, modern Python package manager (recommended)
- **pip** - Traditional package management

#### Code Quality
- **Linting**: Ruff (recommended) or Black + isort
- **Type Checking**: mypy (strict/standard) or Pyrefly
- **Pre-commit**: Automated code quality checks

#### Testing
- pytest with async support
- Coverage reporting
- Fixtures for database and authentication

### Deployment

#### Docker
- Multi-stage Dockerfile with optimized builds
- Non-root user for security
- Health checks included
- docker-compose for local development with all services

#### CI/CD
- GitHub Actions workflows
- Automated testing on push
- Optional deployment pipelines
- Code quality checks

### AWS Integration
Deploy and integrate with AWS services:

| Service | Purpose |
|---------|---------|
| **S3** | Object storage (file uploads, backups) |
| **SES** | Email service (transactional emails) |
| **ECR** | Container registry (Docker images) |
| **ECS** | Container orchestration (deployment) |

[Learn more →](aws.md)

## Interactive Configuration

FastAPI Smith uses an interactive CLI to guide you through configuration. You can:

- Use arrow keys to navigate options
- Press Enter to select
- Use Space to toggle multi-select options
- Press Ctrl+C to cancel at any time

## Example Configuration Session

```
? Project name: my-api
? Database type: PostgreSQL
? ORM: SQLAlchemy 2.0
? Authentication: JWT
? Include admin panel? Yes
? Caching: Redis
? Task queue: Celery
? Logging: Loguru
? Include Sentry? No
? Package manager: uv
? Linting: Ruff
? Type checker: mypy (strict)
? Pre-commit hooks? Yes
? Docker files? Yes
? GitHub Actions? Yes
```

## Configuration Files Generated

Based on your choices, FastAPI Smith generates appropriate configuration files:

- `pyproject.toml` - Dependencies and tool configuration
- `.env.example` - Environment variable template
- `app/config.py` - Application settings (using pydantic-settings)
- `alembic.ini` - Database migration config (if using Alembic)
- `docker-compose.yml` - Multi-service setup (if using Docker)
- `.pre-commit-config.yaml` - Pre-commit hooks (if enabled)
- `ruff.toml` or `pyproject.toml` - Linting configuration
- `mypy.ini` - Type checking configuration

## Default Values

FastAPI Smith uses sensible defaults:

- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Auth**: JWT
- **Package manager**: uv
- **Linting**: Ruff
- **Type checking**: mypy (standard mode)
- **Docker**: Included
- **CI/CD**: GitHub Actions

## Modifying Configuration

After generation, you can modify the configuration by:

1. **Editing config files directly** - All settings are in standard formats
2. **Environment variables** - Override settings via `.env` file
3. **Code changes** - Modify `app/config.py` for application settings

## Next Steps

Dive deeper into specific configuration areas:

<div class="grid cards" markdown>

-   [Database & ORM →](database.md)
-   [Authentication →](authentication.md)
-   [Caching →](caching.md)
-   [Task Queues →](tasks.md)

</div>
