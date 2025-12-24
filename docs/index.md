# FastAPI Smith

[![PyPI version](https://badge.fury.io/py/fastapi-smith.svg)](https://badge.fury.io/py/fastapi-smith)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Interactive CLI to scaffold production-ready FastAPI projects with database, authentication, admin panel, and more.**

## Why FastAPI Smith?

Building a production-ready FastAPI application involves making dozens of decisions and setting up boilerplate code. FastAPI Smith eliminates this overhead by:

- **Asking the right questions** - Interactive prompts guide you through project setup
- **Making best-practice choices** - Pre-configured with industry standards
- **Saving hours of setup time** - Go from idea to running API in minutes
- **Staying flexible** - Choose only what you need, nothing more

## Features

### Core Features
- **Interactive CLI** - Answer questions to customize your project
- **Production-Ready** - Best practices baked in from the start
- **Type-Safe** - Full type hints with mypy validation
- **Async by Default** - Built for high performance
- **Modern Tooling** - Ruff, pre-commit, GitHub Actions

### Database Support
- PostgreSQL, MySQL, SQLite
- SQLAlchemy 2.0, SQLModel, or Tortoise-ORM
- Automatic migrations with Alembic/Aerich
- Connection pooling and async support

### Authentication
- JWT with refresh tokens
- OAuth2 password flow
- Session-based auth
- Or skip auth entirely

### Additional Features
- Admin panel with SQLAdmin
- Redis/Memcached caching
- Task queues (Celery, ARQ, Taskiq)
- Structured logging (Loguru, structlog)
- Health check endpoints
- Docker & docker-compose
- CI/CD with GitHub Actions
- AWS integration (S3, SES, ECS)

## Quick Example

```bash
# Install
pip install fastapi-smith

# Run
fastapi-smith

# Answer a few questions...
# Project created!

cd my-project
uv sync
uv run uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to see your API documentation.

## What Gets Generated?

A complete, production-ready FastAPI application:

```
my-project/
├── app/
│   ├── main.py              # FastAPI app with routes
│   ├── config.py            # Settings with pydantic-settings
│   ├── database.py          # DB connection & session
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── core/                # Security, logging, caching
│   └── admin/               # Admin panel
├── migrations/              # Database migrations
├── tests/                   # Pytest tests
├── .github/workflows/       # CI/CD
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
└── pyproject.toml           # Dependencies
```

## Next Steps

Ready to get started?

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Getting Started__

    ---

    Install FastAPI Smith and create your first project

    [:octicons-arrow-right-24: Installation](getting-started/installation.md)

-   :material-book-open-variant:{ .lg .middle } __Configuration__

    ---

    Learn about all the configuration options available

    [:octicons-arrow-right-24: Configuration](configuration/overview.md)

-   :material-rocket-launch:{ .lg .middle } __Guides__

    ---

    In-depth guides on deployment, testing, and more

    [:octicons-arrow-right-24: Guides](guides/project-structure.md)

-   :material-github:{ .lg .middle } __Contributing__

    ---

    Help make FastAPI Smith even better

    [:octicons-arrow-right-24: Contributing](contributing.md)

</div>

## Community & Support

- **Issues & Bug Reports**: [GitHub Issues](https://github.com/dhruvbhavsar0612/fastsql-project-setup/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/dhruvbhavsar0612/fastsql-project-setup/discussions)
- **Source Code**: [GitHub Repository](https://github.com/dhruvbhavsar0612/fastsql-project-setup)

## License

FastAPI Smith is licensed under the [MIT License](https://github.com/dhruvbhavsar0612/fastsql-project-setup/blob/main/LICENSE).
