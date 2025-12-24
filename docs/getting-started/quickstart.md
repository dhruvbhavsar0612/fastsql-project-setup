# Quick Start

This guide will walk you through creating your first FastAPI project with FastAPI Smith.

## Running FastAPI Smith

Simply run the command:

```bash
fastapi-smith
```

You'll be greeted with an interactive prompt that will guide you through the setup process.

## Configuration Prompts

### 1. Project Basics

First, you'll be asked about your project details:

```
? Project name: my-awesome-api
? Project description: My awesome FastAPI project
? Author name: Your Name
? Author email: you@example.com
? Python version: 3.12
```

### 2. Database Setup

Choose your database and ORM:

```
? Database type: PostgreSQL
? ORM: SQLAlchemy 2.0
? Include Alembic migrations? Yes
```

### 3. Authentication

Select your authentication method:

```
? Authentication type: JWT
? Include user registration endpoints? Yes
```

### 4. Additional Features

Choose optional features:

```
? Include admin panel? Yes (SQLAdmin)
? Caching: Redis
? Task queue: Celery
? Logging library: Loguru
? Include Sentry error tracking? No
```

### 5. Development Tools

Configure your development environment:

```
? Package manager: uv
? Linting: Ruff
? Type checker: mypy (strict)
? Include pre-commit hooks? Yes
```

### 6. Deployment

Set up deployment options:

```
? Include Docker files? Yes
? Include docker-compose? Yes
? Set up GitHub Actions CI/CD? Yes
? Deploy to AWS ECS? No
```

### 7. Confirmation

Review your choices and confirm:

```
╭─────────────────── Configuration Summary ───────────────────╮
│ Project: my-awesome-api                                     │
│ Database: PostgreSQL with SQLAlchemy 2.0                    │
│ Auth: JWT                                                   │
│ Admin: SQLAdmin                                             │
│ Caching: Redis                                              │
│ Tasks: Celery                                               │
│ ...                                                         │
╰─────────────────────────────────────────────────────────────╯

? Proceed with project generation? Yes
```

## Project Generated!

Once confirmed, FastAPI Smith will generate your project:

```
✓ Creating project structure...
✓ Generating configuration files...
✓ Creating database models...
✓ Setting up authentication...
✓ Configuring admin panel...
✓ Creating Docker files...
✓ Setting up CI/CD...

Project created successfully! 🎉
```

## Running Your Project

### With uv (Recommended)

```bash
cd my-awesome-api
uv sync
uv run uvicorn app.main:app --reload
```

### With pip

```bash
cd my-awesome-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```

### With Docker

```bash
cd my-awesome-api
docker-compose up --build
```

## Viewing Your API

Once running, visit:

- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin) (if enabled)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## Next Steps

Congratulations! You now have a running FastAPI application. Here's what to do next:

1. **Set up the database**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your database credentials
   # Then run migrations
   uv run alembic upgrade head
   ```

2. **Create your first endpoint** - See the [Project Structure](../guides/project-structure.md) guide

3. **Add models and schemas** - Learn about [Database Configuration](../configuration/database.md)

4. **Set up authentication** - Check the [Authentication Guide](../configuration/authentication.md)

5. **Deploy to production** - Follow the [Docker Deployment](../guides/docker.md) guide

## Example Project

Want to see what a generated project looks like? Check out our [example repository](https://github.com/dhruvbhavsar0612/fastapi-smith-example).

## Getting Help

If you run into issues:

- Check the [Configuration Overview](../configuration/overview.md)
- Read the [Guides](../guides/project-structure.md)
- Open an [issue on GitHub](https://github.com/dhruvbhavsar0612/fastsql-project-setup/issues)
