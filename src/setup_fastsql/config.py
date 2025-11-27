"""Configuration models and enums for setup-fastsql."""

from dataclasses import dataclass, field
from enum import Enum


class PythonVersion(str, Enum):
    PY310 = "3.10"
    PY311 = "3.11"
    PY312 = "3.12"
    PY313 = "3.13"


class Database(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    NONE = "none"


class ORM(str, Enum):
    SQLALCHEMY = "sqlalchemy"
    SQLMODEL = "sqlmodel"
    TORTOISE = "tortoise"
    NONE = "none"


class MigrationTool(str, Enum):
    ALEMBIC = "alembic"
    AERICH = "aerich"
    NONE = "none"


class AuthMethod(str, Enum):
    JWT = "jwt"
    OAUTH2 = "oauth2"
    SESSION = "session"
    NONE = "none"


class MessageBroker(str, Enum):
    RABBITMQ = "rabbitmq"
    REDIS = "redis"
    NONE = "none"


class TaskQueue(str, Enum):
    CELERY = "celery"
    ARQ = "arq"
    TASKIQ = "taskiq"
    BUILTIN = "builtin"
    NONE = "none"


class CacheBackend(str, Enum):
    REDIS = "redis"
    MEMCACHED = "memcached"
    INMEMORY = "inmemory"
    NONE = "none"


class LoggingLib(str, Enum):
    LOGURU = "loguru"
    STRUCTLOG = "structlog"
    STANDARD = "standard"


class PackageManager(str, Enum):
    UV = "uv"
    PIP = "pip"


class Linter(str, Enum):
    RUFF = "ruff"
    BLACK_ISORT = "black_isort"
    NONE = "none"


class TypeChecker(str, Enum):
    MYPY_STRICT = "mypy_strict"
    MYPY_STANDARD = "mypy_standard"
    PYREFLY = "pyrefly"
    NONE = "none"


class GitHubWorkflow(str, Enum):
    CI_ONLY = "ci_only"
    CI_DEPLOY = "ci_deploy"
    NONE = "none"


class ProjectStructure(str, Enum):
    LAYERED = "layered"
    DOMAIN_DRIVEN = "domain_driven"
    FLAT = "flat"


class AWSService(str, Enum):
    S3 = "s3"
    SES = "ses"
    ECR = "ecr"
    ECS = "ecs"
    LAMBDA = "lambda"


@dataclass
class ProjectConfig:
    """Complete project configuration from user choices."""

    # Project basics
    project_name: str = "my-fastapi-app"
    project_description: str = "A FastAPI application"
    author_name: str = ""
    author_email: str = ""
    python_version: PythonVersion = PythonVersion.PY312

    # Database
    database: Database = Database.POSTGRESQL
    orm: ORM = ORM.SQLALCHEMY
    migration_tool: MigrationTool = MigrationTool.ALEMBIC

    # Auth & Security
    auth_method: AuthMethod = AuthMethod.JWT
    include_admin: bool = True
    cors_enabled: bool = True

    # API Features
    api_versioning: bool = True
    rate_limiting: bool = True

    # Message Queue
    message_broker: MessageBroker = MessageBroker.NONE
    task_queue: TaskQueue = TaskQueue.BUILTIN

    # Caching
    cache_backend: CacheBackend = CacheBackend.REDIS

    # Logging & Monitoring
    logging_lib: LoggingLib = LoggingLib.LOGURU
    sentry_enabled: bool = False
    health_checks: bool = True

    # Development Tools
    package_manager: PackageManager = PackageManager.UV
    linter: Linter = Linter.RUFF
    type_checker: TypeChecker = TypeChecker.MYPY_STANDARD
    testing: bool = True
    pre_commit: bool = True

    # Deployment
    docker: bool = True
    docker_compose: bool = True
    github_workflow: GitHubWorkflow = GitHubWorkflow.CI_ONLY

    # AWS
    aws_enabled: bool = False
    aws_services: list[AWSService] = field(default_factory=list)

    # Structure
    project_structure: ProjectStructure = ProjectStructure.LAYERED
    include_examples: bool = True

    def get_db_driver(self) -> str:
        """Get the appropriate database driver based on database choice."""
        drivers = {
            Database.POSTGRESQL: "psycopg[binary]",
            Database.MYSQL: "asyncmy",
            Database.SQLITE: "aiosqlite",
            Database.NONE: "",
        }
        return drivers.get(self.database, "")

    def get_db_url_template(self) -> str:
        """Get the database URL template."""
        templates = {
            Database.POSTGRESQL: "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}",
            Database.MYSQL: "mysql+asyncmy://{user}:{password}@{host}:{port}/{database}",
            Database.SQLITE: "sqlite+aiosqlite:///./{database}.db",
            Database.NONE: "",
        }
        return templates.get(self.database, "")
