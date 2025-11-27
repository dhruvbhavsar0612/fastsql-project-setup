"""Project generator - creates files and directories based on configuration."""

from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import (
    AuthMethod,
    AWSService,
    CacheBackend,
    Database,
    GitHubWorkflow,
    Linter,
    MigrationTool,
    ProjectConfig,
    ProjectStructure,
    TypeChecker,
)

console = Console()


class ProjectGenerator:
    """Generates FastAPI project based on configuration."""

    def __init__(self, config: ProjectConfig, output_dir: Path | None = None):
        self.config = config
        self.output_dir = output_dir or Path.cwd() / config.project_name
        self.env = Environment(
            loader=PackageLoader("fastapi_smith", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self) -> None:
        """Generate the complete project."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating project structure...", total=None)

            # Create base directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Generate based on structure type
            progress.update(task, description="Creating directories...")
            self._create_directories()

            progress.update(task, description="Generating configuration files...")
            self._generate_config_files()

            progress.update(task, description="Generating application code...")
            self._generate_app_code()

            if self.config.database != Database.NONE:
                progress.update(task, description="Setting up database...")
                self._generate_database_files()

            if self.config.auth_method != AuthMethod.NONE:
                progress.update(task, description="Setting up authentication...")
                self._generate_auth_files()

            if self.config.include_admin and self.config.database != Database.NONE:
                progress.update(task, description="Setting up admin panel...")
                self._generate_admin_files()

            if self.config.docker:
                progress.update(task, description="Creating Docker files...")
                self._generate_docker_files()

            if self.config.github_workflow != GitHubWorkflow.NONE:
                progress.update(task, description="Creating GitHub workflows...")
                self._generate_github_workflows()

            if self.config.testing:
                progress.update(task, description="Setting up tests...")
                self._generate_test_files()

            if self.config.pre_commit:
                progress.update(task, description="Setting up pre-commit...")
                self._generate_precommit_config()

            if self.config.aws_enabled:
                progress.update(task, description="Setting up AWS integration...")
                self._generate_aws_files()

            progress.update(task, description="Done!")

        console.print(f"\n[green]Project created at:[/green] {self.output_dir}")

    def _create_directories(self) -> None:
        """Create project directory structure."""
        app_dir = self.output_dir / "app"

        if self.config.project_structure == ProjectStructure.LAYERED:
            dirs = [
                app_dir / "api" / "v1" / "routes",
                app_dir / "api" / "v1" / "deps",
                app_dir / "models",
                app_dir / "schemas",
                app_dir / "services",
                app_dir / "repositories",
                app_dir / "core",
                app_dir / "utils",
            ]
        elif self.config.project_structure == ProjectStructure.DOMAIN_DRIVEN:
            dirs = [
                app_dir / "domains" / "users" / "routes",
                app_dir / "domains" / "users" / "models",
                app_dir / "domains" / "users" / "schemas",
                app_dir / "domains" / "users" / "services",
                app_dir / "shared" / "core",
                app_dir / "shared" / "utils",
            ]
        else:  # FLAT
            dirs = [
                app_dir / "routes",
                app_dir / "models",
            ]

        # Common directories
        dirs.extend(
            [
                self.output_dir / "tests",
                self.output_dir / ".github" / "workflows",
            ]
        )

        if self.config.include_admin and self.config.database != Database.NONE:
            dirs.append(app_dir / "admin")

        if self.config.migration_tool == MigrationTool.ALEMBIC:
            dirs.append(self.output_dir / "migrations" / "versions")
        elif self.config.migration_tool == MigrationTool.AERICH:
            dirs.append(self.output_dir / "migrations")

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            # Create __init__.py for Python packages
            if "app" in str(d) or "tests" in str(d):
                init_file = d / "__init__.py"
                if not init_file.exists():
                    init_file.touch()

    def _render_template(self, template_name: str, output_path: Path, **context) -> None:
        """Render a Jinja2 template to a file."""
        template = self.env.get_template(template_name)
        content = template.render(config=self.config, **context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    def _write_file(self, path: Path, content: str) -> None:
        """Write content to a file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def _generate_config_files(self) -> None:
        """Generate project configuration files."""
        self._render_template("pyproject.toml.j2", self.output_dir / "pyproject.toml")
        self._render_template("gitignore.j2", self.output_dir / ".gitignore")
        self._render_template("env.example.j2", self.output_dir / ".env.example")
        self._render_template("readme.md.j2", self.output_dir / "README.md")

        if self.config.linter == Linter.RUFF:
            self._render_template("ruff.toml.j2", self.output_dir / "ruff.toml")

        if self.config.type_checker in (TypeChecker.MYPY_STRICT, TypeChecker.MYPY_STANDARD):
            self._render_template("mypy.ini.j2", self.output_dir / "mypy.ini")
        elif self.config.type_checker == TypeChecker.PYREFLY:
            self._render_template("pyrefly.toml.j2", self.output_dir / "pyrefly.toml")

    def _generate_app_code(self) -> None:
        """Generate main application code."""
        app_dir = self.output_dir / "app"

        # Main entry point
        self._render_template("app/main.py.j2", app_dir / "main.py")
        self._render_template("app/config.py.j2", app_dir / "config.py")
        self._write_file(app_dir / "__init__.py", '"""FastAPI Application."""\n')

        # Core files
        if self.config.project_structure == ProjectStructure.LAYERED:
            core_dir = app_dir / "core"
        elif self.config.project_structure == ProjectStructure.DOMAIN_DRIVEN:
            core_dir = app_dir / "shared" / "core"
        else:
            core_dir = app_dir

        self._render_template("app/core/logging.py.j2", core_dir / "logging.py")

        if self.config.rate_limiting:
            self._render_template("app/core/rate_limit.py.j2", core_dir / "rate_limit.py")

        if self.config.cache_backend != CacheBackend.NONE:
            self._render_template("app/core/cache.py.j2", core_dir / "cache.py")

        if self.config.health_checks:
            self._render_template("app/core/health.py.j2", core_dir / "health.py")

    def _generate_database_files(self) -> None:
        """Generate database-related files."""
        app_dir = self.output_dir / "app"

        self._render_template("app/database.py.j2", app_dir / "database.py")

        # Generate models
        if self.config.project_structure == ProjectStructure.LAYERED:
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "schemas"
        elif self.config.project_structure == ProjectStructure.DOMAIN_DRIVEN:
            models_dir = app_dir / "domains" / "users" / "models"
            schemas_dir = app_dir / "domains" / "users" / "schemas"
        else:
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "models"

        self._render_template("app/models/base.py.j2", models_dir / "base.py")

        if self.config.include_examples:
            self._render_template("app/models/user.py.j2", models_dir / "user.py")
            self._render_template("app/schemas/user.py.j2", schemas_dir / "user.py")

        # Migration setup
        if self.config.migration_tool == MigrationTool.ALEMBIC:
            self._render_template("alembic.ini.j2", self.output_dir / "alembic.ini")
            self._render_template("migrations/env.py.j2", self.output_dir / "migrations" / "env.py")
            self._render_template(
                "migrations/script.py.mako.j2",
                self.output_dir / "migrations" / "script.py.mako",
            )

    def _generate_auth_files(self) -> None:
        """Generate authentication files."""
        app_dir = self.output_dir / "app"

        if self.config.project_structure == ProjectStructure.LAYERED:
            core_dir = app_dir / "core"
            routes_dir = app_dir / "api" / "v1" / "routes"
        elif self.config.project_structure == ProjectStructure.DOMAIN_DRIVEN:
            core_dir = app_dir / "shared" / "core"
            routes_dir = app_dir / "domains" / "users" / "routes"
        else:
            core_dir = app_dir
            routes_dir = app_dir / "routes"

        self._render_template("app/core/security.py.j2", core_dir / "security.py")

        if self.config.include_examples:
            self._render_template("app/routes/auth.py.j2", routes_dir / "auth.py")
            self._render_template("app/routes/users.py.j2", routes_dir / "users.py")

    def _generate_admin_files(self) -> None:
        """Generate admin panel files."""
        app_dir = self.output_dir / "app"
        self._render_template("app/admin/views.py.j2", app_dir / "admin" / "views.py")
        self._write_file(app_dir / "admin" / "__init__.py", '"""Admin panel configuration."""\n')

    def _generate_docker_files(self) -> None:
        """Generate Docker-related files."""
        self._render_template("Dockerfile.j2", self.output_dir / "Dockerfile")

        if self.config.docker_compose:
            self._render_template("docker-compose.yml.j2", self.output_dir / "docker-compose.yml")

    def _generate_github_workflows(self) -> None:
        """Generate GitHub Actions workflows."""
        workflows_dir = self.output_dir / ".github" / "workflows"

        if self.config.github_workflow == GitHubWorkflow.CI_ONLY:
            self._render_template("github/ci.yml.j2", workflows_dir / "ci.yml")
        elif self.config.github_workflow == GitHubWorkflow.CI_DEPLOY:
            self._render_template("github/ci.yml.j2", workflows_dir / "ci.yml")
            self._render_template("github/deploy.yml.j2", workflows_dir / "deploy.yml")

    def _generate_test_files(self) -> None:
        """Generate test files."""
        tests_dir = self.output_dir / "tests"
        self._render_template("tests/conftest.py.j2", tests_dir / "conftest.py")

        if self.config.include_examples:
            self._render_template("tests/test_health.py.j2", tests_dir / "test_health.py")
            if self.config.auth_method != AuthMethod.NONE:
                self._render_template("tests/test_auth.py.j2", tests_dir / "test_auth.py")

    def _generate_precommit_config(self) -> None:
        """Generate pre-commit configuration."""
        self._render_template(
            "pre-commit-config.yaml.j2", self.output_dir / ".pre-commit-config.yaml"
        )

    def _generate_aws_files(self) -> None:
        """Generate AWS integration files."""
        app_dir = self.output_dir / "app"

        if self.config.project_structure == ProjectStructure.LAYERED:
            services_dir = app_dir / "services"
        elif self.config.project_structure == ProjectStructure.DOMAIN_DRIVEN:
            services_dir = app_dir / "shared" / "services"
            services_dir.mkdir(parents=True, exist_ok=True)
        else:
            services_dir = app_dir

        if AWSService.S3 in self.config.aws_services:
            self._render_template("app/services/s3.py.j2", services_dir / "s3.py")

        if AWSService.SES in self.config.aws_services:
            self._render_template("app/services/ses.py.j2", services_dir / "ses.py")
