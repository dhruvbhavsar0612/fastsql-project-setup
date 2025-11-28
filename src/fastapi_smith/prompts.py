"""Interactive prompts for gathering user configuration."""

import subprocess
from typing import Any

import questionary
from questionary import Choice, Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .config import (
    ORM,
    AuthMethod,
    AWSService,
    CacheBackend,
    Database,
    GitHubWorkflow,
    Linter,
    LoggingLib,
    MessageBroker,
    MigrationTool,
    PackageManager,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
    TaskQueue,
    TypeChecker,
)

console = Console()

# Custom style for questionary
custom_style = Style(
    [
        ("qmark", "fg:cyan bold"),
        ("question", "fg:white bold"),
        ("answer", "fg:green bold"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:green"),
        ("separator", "fg:gray"),
        ("instruction", "fg:gray italic"),
    ]
)


def get_git_config(key: str) -> str:
    """Get a value from git config."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def print_header() -> None:
    """Print the welcome header."""
    header = Text()
    header.append("Setup FastSQL", style="bold cyan")
    header.append("\n")
    header.append("Interactive FastAPI Project Scaffolder", style="italic")

    console.print(Panel(header, border_style="cyan", padding=(1, 2)))
    console.print()


def print_section(title: str) -> None:
    """Print a section header."""
    console.print(f"\n[bold cyan]━━━ {title} ━━━[/bold cyan]\n")


def make_choices(enum_class: Any, labels: dict[str, str] | None = None) -> list[Choice]:
    """Create choices from an enum class with optional custom labels."""
    choices = []
    for item in enum_class:
        label = (
            labels.get(item.value, item.value.replace("_", " ").title())
            if labels
            else item.value.replace("_", " ").title()
        )
        choices.append(Choice(title=label, value=item.value))
    return choices


async def gather_project_basics() -> dict:
    """Gather basic project information."""
    print_section("Project Basics")

    default_author = get_git_config("user.name")
    default_email = get_git_config("user.email")

    project_name = await questionary.text(
        "Project name:",
        default="my-fastapi-app",
        style=custom_style,
    ).ask_async()

    project_description = await questionary.text(
        "Project description:",
        default="A FastAPI application",
        style=custom_style,
    ).ask_async()

    author_name = await questionary.text(
        "Author name:",
        default=default_author,
        style=custom_style,
    ).ask_async()

    author_email = await questionary.text(
        "Author email:",
        default=default_email,
        style=custom_style,
    ).ask_async()

    python_version = await questionary.select(
        "Python version:",
        choices=make_choices(
            PythonVersion,
            {
                "3.10": "Python 3.10",
                "3.11": "Python 3.11",
                "3.12": "Python 3.12 (Recommended)",
                "3.13": "Python 3.13",
            },
        ),
        default="3.12",
        style=custom_style,
    ).ask_async()

    return {
        "project_name": project_name,
        "project_description": project_description,
        "author_name": author_name,
        "author_email": author_email,
        "python_version": PythonVersion(python_version),
    }


async def gather_database_config() -> dict[str, Any]:
    """Gather database configuration."""
    print_section("Database Configuration")

    database = await questionary.select(
        "Database:",
        choices=make_choices(
            Database,
            {
                "postgresql": "PostgreSQL (Recommended)",
                "mysql": "MySQL",
                "sqlite": "SQLite",
                "none": "None (No database)",
            },
        ),
        default="postgresql",
        style=custom_style,
    ).ask_async()

    result: dict[str, Any] = {"database": Database(database)}

    if database != "none":
        orm = await questionary.select(
            "ORM:",
            choices=make_choices(
                ORM,
                {
                    "sqlalchemy": "SQLAlchemy 2.0 (Recommended)",
                    "sqlmodel": "SQLModel (Pydantic + SQLAlchemy)",
                    "tortoise": "Tortoise-ORM",
                    "none": "None (Raw SQL)",
                },
            ),
            default="sqlalchemy",
            style=custom_style,
        ).ask_async()
        result["orm"] = ORM(orm)

        if orm in ("sqlalchemy", "sqlmodel"):
            migration_tool = await questionary.select(
                "Migration tool:",
                choices=[
                    Choice(title="Alembic (Recommended)", value="alembic"),
                    Choice(title="None", value="none"),
                ],
                default="alembic",
                style=custom_style,
            ).ask_async()
        elif orm == "tortoise":
            migration_tool = await questionary.select(
                "Migration tool:",
                choices=[
                    Choice(title="Aerich (Tortoise migrations)", value="aerich"),
                    Choice(title="None", value="none"),
                ],
                default="aerich",
                style=custom_style,
            ).ask_async()
        else:
            migration_tool = "none"

        result["migration_tool"] = MigrationTool(migration_tool)
    else:
        result["orm"] = ORM.NONE
        result["migration_tool"] = MigrationTool.NONE

    return result


async def gather_auth_config() -> dict:
    """Gather authentication configuration."""
    print_section("Authentication & Security")

    auth_method = await questionary.select(
        "Authentication method:",
        choices=make_choices(
            AuthMethod,
            {
                "jwt": "JWT (JSON Web Tokens) - Recommended",
                "oauth2": "OAuth2 (Social logins)",
                "session": "Session-based",
                "none": "None",
            },
        ),
        default="jwt",
        style=custom_style,
    ).ask_async()

    include_admin = await questionary.confirm(
        "Include admin panel (SQLAdmin)?",
        default=True,
        style=custom_style,
    ).ask_async()

    cors_enabled = await questionary.confirm(
        "Enable CORS?",
        default=True,
        style=custom_style,
    ).ask_async()

    return {
        "auth_method": AuthMethod(auth_method),
        "include_admin": include_admin,
        "cors_enabled": cors_enabled,
    }


async def gather_api_features() -> dict:
    """Gather API feature configuration."""
    print_section("API Features")

    api_versioning = await questionary.confirm(
        "Enable API versioning (e.g., /api/v1/)?",
        default=True,
        style=custom_style,
    ).ask_async()

    rate_limiting = await questionary.confirm(
        "Enable rate limiting (slowapi)?",
        default=True,
        style=custom_style,
    ).ask_async()

    return {
        "api_versioning": api_versioning,
        "rate_limiting": rate_limiting,
    }


async def gather_messaging_config() -> dict:
    """Gather message broker and task queue configuration."""
    print_section("Message Queue & Background Tasks")

    message_broker = await questionary.select(
        "Message broker:",
        choices=make_choices(
            MessageBroker,
            {
                "rabbitmq": "RabbitMQ",
                "redis": "Redis",
                "none": "None",
            },
        ),
        default="none",
        style=custom_style,
    ).ask_async()

    task_queue = await questionary.select(
        "Task queue:",
        choices=make_choices(
            TaskQueue,
            {
                "celery": "Celery (Full-featured)",
                "arq": "ARQ (Async, Redis-based)",
                "taskiq": "Taskiq (Modern async)",
                "builtin": "Built-in BackgroundTasks",
                "none": "None",
            },
        ),
        default="builtin",
        style=custom_style,
    ).ask_async()

    return {
        "message_broker": MessageBroker(message_broker),
        "task_queue": TaskQueue(task_queue),
    }


async def gather_cache_config() -> dict:
    """Gather caching configuration."""
    print_section("Caching")

    cache_backend = await questionary.select(
        "Cache backend:",
        choices=make_choices(
            CacheBackend,
            {
                "redis": "Redis (Recommended)",
                "memcached": "Memcached",
                "inmemory": "In-memory (Development only)",
                "none": "None",
            },
        ),
        default="redis",
        style=custom_style,
    ).ask_async()

    return {"cache_backend": CacheBackend(cache_backend)}


async def gather_logging_config() -> dict:
    """Gather logging and monitoring configuration."""
    print_section("Logging & Monitoring")

    logging_lib = await questionary.select(
        "Logging library:",
        choices=make_choices(
            LoggingLib,
            {
                "loguru": "Loguru (Simple & powerful)",
                "structlog": "structlog (Structured logging)",
                "standard": "Standard library logging",
            },
        ),
        default="loguru",
        style=custom_style,
    ).ask_async()

    sentry_enabled = await questionary.confirm(
        "Enable Sentry error tracking?",
        default=False,
        style=custom_style,
    ).ask_async()

    health_checks = await questionary.confirm(
        "Include health check endpoints?",
        default=True,
        style=custom_style,
    ).ask_async()

    return {
        "logging_lib": LoggingLib(logging_lib),
        "sentry_enabled": sentry_enabled,
        "health_checks": health_checks,
    }


async def gather_dev_tools() -> dict:
    """Gather development tools configuration."""
    print_section("Development Tools")

    package_manager = await questionary.select(
        "Package manager:",
        choices=make_choices(
            PackageManager,
            {
                "uv": "uv (Fast, recommended)",
                "pip": "pip",
            },
        ),
        default="uv",
        style=custom_style,
    ).ask_async()

    linter = await questionary.select(
        "Linter/Formatter:",
        choices=make_choices(
            Linter,
            {
                "ruff": "Ruff (Fast, all-in-one)",
                "black_isort": "Black + isort",
                "none": "None",
            },
        ),
        default="ruff",
        style=custom_style,
    ).ask_async()

    type_checker = await questionary.select(
        "Type checking:",
        choices=make_choices(
            TypeChecker,
            {
                "mypy_strict": "mypy (Strict mode)",
                "mypy_standard": "mypy (Standard)",
                "pyrefly": "Pyrefly (Meta's type checker)",
                "none": "None",
            },
        ),
        default="mypy_standard",
        style=custom_style,
    ).ask_async()

    testing = await questionary.confirm(
        "Include testing setup (pytest)?",
        default=True,
        style=custom_style,
    ).ask_async()

    pre_commit = await questionary.confirm(
        "Include pre-commit hooks?",
        default=True,
        style=custom_style,
    ).ask_async()

    return {
        "package_manager": PackageManager(package_manager),
        "linter": Linter(linter),
        "type_checker": TypeChecker(type_checker),
        "testing": testing,
        "pre_commit": pre_commit,
    }


async def gather_deployment_config() -> dict:
    """Gather deployment configuration."""
    print_section("Deployment & CI/CD")

    docker = await questionary.confirm(
        "Include Dockerfile?",
        default=True,
        style=custom_style,
    ).ask_async()

    docker_compose = await questionary.confirm(
        "Include docker-compose.yml?",
        default=True,
        style=custom_style,
    ).ask_async()

    github_workflow = await questionary.select(
        "GitHub Actions workflow:",
        choices=make_choices(
            GitHubWorkflow,
            {
                "ci_only": "CI only (lint, test)",
                "ci_deploy": "CI + Deploy",
                "none": "None",
            },
        ),
        default="ci_only",
        style=custom_style,
    ).ask_async()

    return {
        "docker": docker,
        "docker_compose": docker_compose,
        "github_workflow": GitHubWorkflow(github_workflow),
    }


async def gather_aws_config() -> dict:
    """Gather AWS configuration."""
    print_section("AWS Cloud Services")

    aws_enabled = await questionary.confirm(
        "Configure AWS services?",
        default=False,
        style=custom_style,
    ).ask_async()

    aws_services = []
    if aws_enabled:
        aws_choices = await questionary.checkbox(
            "Select AWS services to integrate:",
            choices=[
                Choice(title="S3 (Object storage)", value="s3"),
                Choice(title="SES (Email service)", value="ses"),
                Choice(title="ECR (Container registry)", value="ecr"),
                Choice(title="ECS (Container orchestration)", value="ecs"),
                Choice(title="Lambda (Serverless functions)", value="lambda"),
            ],
            style=custom_style,
        ).ask_async()
        aws_services = [AWSService(s) for s in (aws_choices or [])]

    return {
        "aws_enabled": aws_enabled,
        "aws_services": aws_services,
    }


async def gather_structure_config() -> dict:
    """Gather project structure configuration."""
    print_section("Project Structure")

    project_structure = await questionary.select(
        "Project structure:",
        choices=make_choices(
            ProjectStructure,
            {
                "layered": "Layered (routes/services/repositories)",
                "domain_driven": "Domain-Driven (by feature/domain)",
                "flat": "Flat (simple, minimal)",
            },
        ),
        default="layered",
        style=custom_style,
    ).ask_async()

    include_examples = await questionary.confirm(
        "Include example code (User model, routes)?",
        default=True,
        style=custom_style,
    ).ask_async()

    return {
        "project_structure": ProjectStructure(project_structure),
        "include_examples": include_examples,
    }


async def gather_all_config() -> ProjectConfig:
    """Run through all prompts and gather complete configuration."""
    print_header()

    config_dict: dict[str, Any] = {}

    # Gather all configurations
    config_dict.update(await gather_project_basics())
    config_dict.update(await gather_database_config())
    config_dict.update(await gather_auth_config())
    config_dict.update(await gather_api_features())
    config_dict.update(await gather_messaging_config())
    config_dict.update(await gather_cache_config())
    config_dict.update(await gather_logging_config())
    config_dict.update(await gather_dev_tools())
    config_dict.update(await gather_deployment_config())
    config_dict.update(await gather_aws_config())
    config_dict.update(await gather_structure_config())

    return ProjectConfig(**config_dict)


async def confirm_config(config: ProjectConfig) -> bool:
    """Display configuration summary and ask for confirmation."""
    console.print("\n")
    console.print(
        Panel(
            "[bold]Configuration Summary[/bold]",
            border_style="green",
        )
    )

    summary_lines = [
        f"[cyan]Project:[/cyan] {config.project_name}",
        f"[cyan]Python:[/cyan] {config.python_version.value}",
        f"[cyan]Database:[/cyan] {config.database.value} + {config.orm.value}",
        f"[cyan]Auth:[/cyan] {config.auth_method.value}",
        f"[cyan]Admin Panel:[/cyan] {'Yes' if config.include_admin else 'No'}",
        f"[cyan]Cache:[/cyan] {config.cache_backend.value}",
        f"[cyan]Task Queue:[/cyan] {config.task_queue.value}",
        f"[cyan]Logging:[/cyan] {config.logging_lib.value}",
        f"[cyan]Type Checker:[/cyan] {config.type_checker.value}",
        f"[cyan]Package Manager:[/cyan] {config.package_manager.value}",
        f"[cyan]Docker:[/cyan] {'Yes' if config.docker else 'No'}",
        f"[cyan]Structure:[/cyan] {config.project_structure.value}",
    ]

    if config.aws_enabled:
        services = ", ".join(s.value for s in config.aws_services)
        summary_lines.append(f"[cyan]AWS Services:[/cyan] {services}")

    for line in summary_lines:
        console.print(f"  {line}")

    console.print()

    confirmed = await questionary.confirm(
        "Proceed with this configuration?",
        default=True,
        style=custom_style,
    ).ask_async()
    return bool(confirmed)
