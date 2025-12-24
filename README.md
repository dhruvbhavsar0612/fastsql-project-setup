# fastapi-smith

[![PyPI version](https://badge.fury.io/py/fastapi-smith.svg)](https://badge.fury.io/py/fastapi-smith)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/dhruvbhavsar0612/fastsql-project-setup/actions/workflows/ci.yml/badge.svg)](https://github.com/dhruvbhavsar0612/fastsql-project-setup/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-github.io-blue)](https://dhruvbhavsar0612.github.io/fastsql-project-setup/)

Interactive CLI to scaffold production-ready FastAPI projects with database, authentication, admin panel, and more.

📚 **[Full Documentation](https://dhruvbhavsar0612.github.io/fastsql-project-setup/)**

## Features

- **Interactive prompts** - Answer questions to customize your project
- **Production-ready** - Best practices baked in from the start
- **Highly configurable** - Choose your database, ORM, auth, and more
- **Modern tooling** - Ruff, mypy, pre-commit, GitHub Actions
- **Docker support** - Multi-stage Dockerfile and docker-compose included

## Installation

```bash
# Using uvx (recommended - no install needed)
uvx fastapi-smith

# Or install globally with uv
uv tool install fastapi-smith

# Or with pip
pip install fastapi-smith
```

## Quick Start

Simply run:

```bash
fastapi-smith
```

Follow the interactive prompts to configure your project. A new directory will be created with your complete FastAPI application.

```bash
cd my-project
uv sync
uv run uvicorn app.main:app --reload
```

## Configuration Options

### Project Basics
- Project name, description, author
- Python version (3.10, 3.11, 3.12, 3.13)

### Database & ORM
| Database   | Drivers                    | ORMs                              |
|------------|----------------------------|-----------------------------------|
| PostgreSQL | psycopg3 (async)           | SQLAlchemy 2.0, SQLModel          |
| MySQL      | asyncmy                    | SQLAlchemy 2.0, SQLModel          |
| SQLite     | aiosqlite                  | SQLAlchemy 2.0, SQLModel          |
| -          | -                          | Tortoise-ORM (any DB)             |

Migrations: **Alembic** (SQLAlchemy/SQLModel) or **Aerich** (Tortoise-ORM)

### Authentication
- **JWT** - JSON Web Tokens with refresh tokens
- **OAuth2** - Password flow with bearer tokens
- **Session** - Server-side sessions with cookies
- **None** - No authentication

### Admin Panel
- **SQLAdmin** - Beautiful admin interface for SQLAlchemy/SQLModel

### Caching
- **Redis** - Distributed caching
- **Memcached** - High-performance caching
- **In-memory** - Simple local caching

### Message Queue & Background Tasks
| Broker   | Task Queues                          |
|----------|--------------------------------------|
| RabbitMQ | Celery, Taskiq                       |
| Redis    | Celery, ARQ, Taskiq                  |
| -        | Built-in BackgroundTasks             |

### Logging & Monitoring
- **Loguru** - Modern logging with rich formatting
- **structlog** - Structured logging for production
- **Standard** - Python's built-in logging
- **Sentry** - Error tracking integration
- **Health checks** - Kubernetes-ready endpoints

### Development Tools
| Category        | Options                        |
|-----------------|--------------------------------|
| Package Manager | uv, pip                        |
| Linting         | Ruff, Black + isort            |
| Type Checking   | mypy (strict/standard), Pyrefly|
| Testing         | Pytest with async support      |
| Pre-commit      | Automated code quality hooks   |

### Deployment
- **Docker** - Multi-stage build with non-root user
- **docker-compose** - Full stack with DB, Redis, etc.
- **GitHub Actions** - CI/CD workflows

### AWS Integration
- **S3** - Object storage with boto3
- **SES** - Email service
- **ECR** - Container registry
- **ECS** - Container orchestration deployment

### Project Structure
```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings with pydantic-settings
│   ├── database.py          # Database connection & session
│   ├── models/              # SQLAlchemy/SQLModel models
│   ├── schemas/             # Pydantic schemas
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic
│   ├── core/                # Security, logging, caching
│   └── admin/               # SQLAdmin views
├── migrations/              # Alembic migrations
├── tests/                   # Pytest tests
├── .github/workflows/       # CI/CD pipelines
├── .env.example             # Environment template
├── pyproject.toml           # Dependencies & tool config
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Local development stack
└── README.md                # Project documentation
```

## Development

```bash
# Clone the repo
git clone https://github.com/dhruvbhavsar0612/fastsql-project-setup.git
cd fastsql-project-setup

# Install dependencies
uv sync

# Run locally
uv run fastapi-smith

# Run tests
uv run pytest

# Type checking
uv run mypy src

# Linting
uv run ruff check src
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Documentation](https://dhruvbhavsar0612.github.io/fastsql-project-setup/)
- [GitHub Repository](https://github.com/dhruvbhavsar0612/fastsql-project-setup)
- [PyPI Package](https://pypi.org/project/fastapi-smith/)
- [Issue Tracker](https://github.com/dhruvbhavsar0612/fastsql-project-setup/issues)
- [Changelog](CHANGELOG.md)
