# setup-fastsql

Interactive CLI to scaffold FastAPI projects with database, authentication, admin panel, and more.

## Installation

```bash
# Using uvx (recommended)
uvx setup-fastsql

# Or install globally
uv tool install setup-fastsql

# Or with pip
pip install setup-fastsql
```

## Usage

Simply run:

```bash
setup-fastsql
```

The CLI will guide you through configuring:

### Project Basics
- Project name and description
- Author information
- Python version (3.10, 3.11, 3.12, 3.13)

### Database Configuration
- Database: PostgreSQL, MySQL, SQLite, or None
- ORM: SQLAlchemy 2.0, SQLModel, Tortoise-ORM
- Migrations: Alembic, Aerich
- Drivers: psycopg3 (PostgreSQL), asyncmy (MySQL), aiosqlite (SQLite)

### Authentication & Security
- JWT, OAuth2, Session-based, or None
- SQLAdmin panel integration
- CORS configuration

### API Features
- API versioning
- Rate limiting (slowapi)

### Message Queue & Background Tasks
- Message broker: RabbitMQ, Redis
- Task queue: Celery, ARQ, Taskiq, Built-in BackgroundTasks

### Caching
- Redis, Memcached, In-memory

### Logging & Monitoring
- Loguru, structlog, or standard library
- Sentry error tracking
- Health check endpoints

### Development Tools
- Package manager: uv, pip
- Linter: Ruff, Black + isort
- Type checking: mypy (strict/standard), Pyrefly
- Testing: Pytest
- Pre-commit hooks

### Deployment
- Dockerfile with multi-stage build
- docker-compose.yml
- GitHub Actions workflows (CI, Deploy)

### AWS Integration
- S3 (Object storage)
- SES (Email service)
- ECR (Container registry)
- ECS (Container orchestration)

### Project Structure
- Layered (routes/services/repositories)
- Domain-Driven (by feature)
- Flat (simple)

## Generated Project Structure

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── api/v1/routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   └── admin/
├── migrations/
├── tests/
├── .github/workflows/
├── .env.example
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Development

```bash
# Clone the repo
git clone https://github.com/yourusername/setup-fastsql
cd setup-fastsql

# Install dependencies
uv sync

# Run locally
uv run setup-fastsql
```

## License

MIT
