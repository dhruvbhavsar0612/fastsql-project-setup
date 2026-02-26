"""Tests for project generator."""

import re
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from fastapi_smith.config import (
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
from fastapi_smith.generator import ProjectGenerator

# Box-drawing characters used in readme.md.j2 project structure diagrams.
# These are the exact characters that caused the charmap encoding error on
# Windows (cp1252 cannot encode them).
BOX_DRAWING_CHARS = {"├", "│", "└", "─"}


def _generate(config: ProjectConfig, tmpdir: str) -> Path:
    """Helper: generate a project and return its directory."""
    project_dir = Path(tmpdir) / config.project_name
    generator = ProjectGenerator(config, project_dir)
    generator.generate()
    return project_dir


class TestProjectGenerator:
    """Tests for ProjectGenerator class."""

    def test_generate_basic_project(self):
        """Test generating a basic project with default settings."""
        config = ProjectConfig(
            project_name="test-project",
            project_description="A test project",
            author_name="Test Author",
            author_email="test@example.com",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Check essential files exist
            assert (project_dir / "app/__init__.py").exists()
            assert (project_dir / "app/main.py").exists()
            assert (project_dir / "app/config.py").exists()
            assert (project_dir / "app/database.py").exists()
            assert (project_dir / "pyproject.toml").exists()
            assert (project_dir / ".gitignore").exists()
            assert (project_dir / "README.md").exists()

    def test_generate_project_with_docker(self):
        """Test generating a project with Docker enabled."""
        config = ProjectConfig(
            project_name="docker-project",
            docker=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "Dockerfile").exists()
            assert (project_dir / "docker-compose.yml").exists()

    def test_generate_project_without_database(self):
        """Test generating a project without database."""
        config = ProjectConfig(
            project_name="no-db-project",
            database=Database.NONE,
            orm=ORM.NONE,
            migration_tool=MigrationTool.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/main.py").exists()
            # When no database, database.py should not be created
            assert not (project_dir / "app/database.py").exists()

    def test_generate_project_with_auth(self):
        """Test generating a project with JWT authentication."""
        config = ProjectConfig(
            project_name="auth-project",
            auth_method=AuthMethod.JWT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/core/security.py").exists()
            # Check security file has JWT related content
            security_content = (project_dir / "app/core/security.py").read_text(encoding="utf-8")
            assert "jwt" in security_content.lower() or "token" in security_content.lower()

    def test_pyproject_has_correct_name(self):
        """Test that pyproject.toml has the correct project name."""
        config = ProjectConfig(
            project_name="my-custom-project",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            pyproject_content = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
            assert 'name = "my-custom-project"' in pyproject_content

    def test_main_py_has_fastapi_app(self):
        """Test that main.py has a FastAPI app."""
        config = ProjectConfig(project_name="fastapi-test")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            main_content = (project_dir / "app/main.py").read_text(encoding="utf-8")
            assert "FastAPI" in main_content
            assert "app" in main_content

    def test_layered_structure(self):
        """Test generating a project with layered structure."""
        config = ProjectConfig(
            project_name="layered-project",
            project_structure=ProjectStructure.LAYERED,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Layered structure should have api/v1/routes
            assert (project_dir / "app/api/v1/routes/__init__.py").exists()
            assert (project_dir / "app/services/__init__.py").exists()
            assert (project_dir / "app/repositories/__init__.py").exists()

    def test_pyproject_has_required_dependencies(self):
        """Test that generated pyproject.toml includes python-dotenv and pydantic[email]."""
        config = ProjectConfig(
            project_name="deps-test-project",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            pyproject_content = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
            assert "python-dotenv" in pyproject_content
            assert "pydantic[email]" in pyproject_content

    def test_generated_code_uses_absolute_imports_layered(self):
        """Test that generated Python files use absolute imports for LAYERED structure."""
        config = ProjectConfig(
            project_name="imports-test-layered",
            project_structure=ProjectStructure.LAYERED,
            auth_method=AuthMethod.JWT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text(encoding="utf-8")
                matches = relative_import_pattern.findall(content)
                assert not matches, f"Found relative imports in {py_file}: {matches}"

    def test_generated_code_uses_absolute_imports_domain_driven(self):
        """Test that generated Python files use absolute imports for DOMAIN_DRIVEN structure."""
        config = ProjectConfig(
            project_name="imports-test-ddd",
            project_structure=ProjectStructure.DOMAIN_DRIVEN,
            auth_method=AuthMethod.JWT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text(encoding="utf-8")
                matches = relative_import_pattern.findall(content)
                assert not matches, f"Found relative imports in {py_file}: {matches}"

    def test_generated_code_uses_absolute_imports_flat(self):
        """Test that generated Python files use absolute imports for FLAT structure."""
        config = ProjectConfig(
            project_name="imports-test-flat",
            project_structure=ProjectStructure.FLAT,
            auth_method=AuthMethod.JWT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text(encoding="utf-8")
                matches = relative_import_pattern.findall(content)
                assert not matches, f"Found relative imports in {py_file}: {matches}"

    def test_generated_imports_start_with_app(self):
        """Test that internal imports in generated code start with 'from app.'."""
        config = ProjectConfig(
            project_name="app-imports-test",
            project_structure=ProjectStructure.LAYERED,
            auth_method=AuthMethod.JWT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Check auth.py has correct absolute imports
            auth_file = project_dir / "app/api/v1/routes/auth.py"
            if auth_file.exists():
                content = auth_file.read_text(encoding="utf-8")
                # Should have imports from app.* not relative
                assert "from app.database" in content
                assert "from app.models" in content
                assert "from app.schemas" in content
                assert "from app.core" in content

    def test_pyproject_has_hatch_wheel_config(self):
        """Test that generated pyproject.toml has hatch wheel config for app package."""
        config = ProjectConfig(
            project_name="hatch-test-project",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            pyproject_content = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
            assert "[tool.hatch.build.targets.wheel]" in pyproject_content
            assert 'packages = ["app"]' in pyproject_content


class TestUTF8Encoding:
    """Tests for UTF-8 encoding fix.

    The generator must write all files with encoding='utf-8' so that
    templates containing non-ASCII characters (e.g. box-drawing chars
    in readme.md.j2) do not fail on systems where the default locale
    encoding cannot handle them (e.g. cp1252 on Windows).
    """

    def test_readme_contains_box_drawing_chars_layered(self):
        """README for LAYERED structure must contain box-drawing characters."""
        config = ProjectConfig(
            project_name="utf8-layered",
            project_structure=ProjectStructure.LAYERED,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)
            content = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in content, f"Box-drawing char {char!r} missing in LAYERED README"

    def test_readme_contains_box_drawing_chars_domain_driven(self):
        """README for DOMAIN_DRIVEN structure must contain box-drawing characters."""
        config = ProjectConfig(
            project_name="utf8-ddd",
            project_structure=ProjectStructure.DOMAIN_DRIVEN,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)
            content = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in content, f"Box-drawing char {char!r} missing in DOMAIN_DRIVEN README"

    def test_readme_contains_box_drawing_chars_flat(self):
        """README for FLAT structure must contain box-drawing characters."""
        config = ProjectConfig(
            project_name="utf8-flat",
            project_structure=ProjectStructure.FLAT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)
            content = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in content, f"Box-drawing char {char!r} missing in FLAT README"

    def test_write_text_uses_utf8_encoding(self):
        """Verify _render_template writes with encoding='utf-8'."""
        config = ProjectConfig(project_name="encoding-check")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "encoding-check"
            generator = ProjectGenerator(config, project_dir)

            # Patch Path.write_text to capture the encoding argument
            original_write_text = Path.write_text
            calls = []

            def tracking_write_text(self_path, content, *args, **kwargs):
                calls.append({"path": str(self_path), "encoding": kwargs.get("encoding")})
                return original_write_text(self_path, content, *args, **kwargs)

            with patch.object(Path, "write_text", tracking_write_text):
                generator.generate()

            # Every write_text call must have used encoding="utf-8"
            for call in calls:
                assert call["encoding"] == "utf-8", (
                    f"write_text for {call['path']} used encoding={call['encoding']!r} "
                    f"instead of 'utf-8'"
                )

    def test_write_file_uses_utf8_encoding(self):
        """Verify _write_file writes with encoding='utf-8'."""
        config = ProjectConfig(project_name="wf-encoding")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "wf-encoding"
            generator = ProjectGenerator(config, project_dir)

            # Call _write_file directly and verify the file is valid UTF-8
            test_file = project_dir / "test_utf8.txt"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            unicode_content = "Hello ├── World │ └── End ─"
            generator._write_file(test_file, unicode_content)

            # Read back with UTF-8 and verify round-trip
            assert test_file.read_text(encoding="utf-8") == unicode_content

    def test_render_template_uses_utf8_encoding(self):
        """Verify _render_template writes files that can be read back as UTF-8."""
        config = ProjectConfig(
            project_name="rt-encoding",
            project_structure=ProjectStructure.LAYERED,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "rt-encoding"
            generator = ProjectGenerator(config, project_dir)

            # Render the readme template (contains box-drawing chars)
            readme_path = project_dir / "README.md"
            generator._render_template("readme.md.j2", readme_path)

            # Must be readable as UTF-8
            content = readme_path.read_text(encoding="utf-8")
            assert "├" in content

    def test_all_generated_files_are_valid_utf8(self):
        """Every file produced by the generator must be valid UTF-8."""
        config = ProjectConfig(
            project_name="all-utf8",
            project_structure=ProjectStructure.LAYERED,
            auth_method=AuthMethod.JWT,
            docker=True,
            docker_compose=True,
            testing=True,
            pre_commit=True,
            health_checks=True,
            cache_backend=CacheBackend.REDIS,
            rate_limiting=True,
            github_workflow=GitHubWorkflow.CI_DEPLOY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            for file_path in project_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        file_path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        pytest.fail(f"File {file_path.relative_to(project_dir)} is not valid UTF-8")

    def test_exact_user_config_from_error_report(self):
        """Reproduce the exact configuration from the original bug report.

        This was the config that triggered:
        'charmap' codec can't encode characters in position 1465-1467
        """
        config = ProjectConfig(
            project_name="chatbot",
            project_description="A FastAPI application powered by user authentication and sse apis",
            author_name="Priyansi Ranawat",
            author_email="priyanshiranawat15@gmail.com",
            python_version=PythonVersion.PY313,
            database=Database.POSTGRESQL,
            orm=ORM.SQLALCHEMY,
            migration_tool=MigrationTool.ALEMBIC,
            auth_method=AuthMethod.OAUTH2,
            include_admin=True,
            cors_enabled=True,
            api_versioning=True,
            rate_limiting=False,
            message_broker=MessageBroker.RABBITMQ,
            task_queue=TaskQueue.CELERY,
            cache_backend=CacheBackend.REDIS,
            logging_lib=LoggingLib.LOGURU,
            sentry_enabled=True,
            health_checks=True,
            package_manager=PackageManager.UV,
            linter=Linter.RUFF,
            type_checker=TypeChecker.PYREFLY,
            testing=True,
            pre_commit=True,
            docker=True,
            docker_compose=True,
            github_workflow=GitHubWorkflow.CI_DEPLOY,
            project_structure=ProjectStructure.LAYERED,
            include_examples=False,
            aws_enabled=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Verify the README rendered correctly with box-drawing chars
            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in readme
            assert "chatbot" in readme
            assert "## Project Structure" in readme


class TestOutputVariations:
    """Tests for all meaningful output variations across config combinations.

    Covers the cross-product of ProjectStructure x AuthMethod x Database
    and secondary config toggles that produce different template branches.
    """

    # -- ProjectStructure variations ------------------------------------------

    def test_domain_driven_structure_directories(self):
        """DOMAIN_DRIVEN creates domains/ and shared/ directories."""
        config = ProjectConfig(
            project_name="ddd-dirs",
            project_structure=ProjectStructure.DOMAIN_DRIVEN,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/domains/users/routes/__init__.py").exists()
            assert (project_dir / "app/domains/users/models/__init__.py").exists()
            assert (project_dir / "app/domains/users/schemas/__init__.py").exists()
            assert (project_dir / "app/domains/users/services/__init__.py").exists()
            assert (project_dir / "app/shared/core/__init__.py").exists()

    def test_flat_structure_directories(self):
        """FLAT creates minimal routes/ and models/ directories."""
        config = ProjectConfig(
            project_name="flat-dirs",
            project_structure=ProjectStructure.FLAT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/routes/__init__.py").exists()
            assert (project_dir / "app/models/__init__.py").exists()
            # Should NOT have layered-specific dirs
            assert not (project_dir / "app/api").exists()
            assert not (project_dir / "app/services").exists()
            assert not (project_dir / "app/repositories").exists()

    # -- AuthMethod variations ------------------------------------------------

    def test_oauth2_auth(self):
        """OAUTH2 auth generates security.py with oauth content."""
        config = ProjectConfig(
            project_name="oauth2-test",
            auth_method=AuthMethod.OAUTH2,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/core/security.py").exists()
            content = (project_dir / "app/core/security.py").read_text(encoding="utf-8")
            assert "oauth" in content.lower()

    def test_session_auth(self):
        """SESSION auth generates security.py with session content."""
        config = ProjectConfig(
            project_name="session-test",
            auth_method=AuthMethod.SESSION,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/core/security.py").exists()
            content = (project_dir / "app/core/security.py").read_text(encoding="utf-8")
            assert "session" in content.lower() or "token" in content.lower()

    def test_no_auth(self):
        """NONE auth skips security.py entirely."""
        config = ProjectConfig(
            project_name="no-auth-test",
            auth_method=AuthMethod.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/core/security.py").exists()

    # -- Database variations --------------------------------------------------

    def test_mysql_database(self):
        """MySQL config produces correct connection strings."""
        config = ProjectConfig(
            project_name="mysql-test",
            database=Database.MYSQL,
            orm=ORM.SQLALCHEMY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/database.py").exists()
            env_content = (project_dir / ".env.example").read_text(encoding="utf-8")
            assert "mysql" in env_content.lower()

    def test_sqlite_database(self):
        """SQLite config produces correct connection strings."""
        config = ProjectConfig(
            project_name="sqlite-test",
            database=Database.SQLITE,
            orm=ORM.SQLALCHEMY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/database.py").exists()
            env_content = (project_dir / ".env.example").read_text(encoding="utf-8")
            assert "sqlite" in env_content.lower()

    # -- Minimal config (no DB, no auth) --------------------------------------

    def test_minimal_project(self):
        """Absolute minimal config: no DB, no auth, flat."""
        config = ProjectConfig(
            project_name="minimal",
            database=Database.NONE,
            orm=ORM.NONE,
            migration_tool=MigrationTool.NONE,
            auth_method=AuthMethod.NONE,
            include_admin=False,
            docker=False,
            docker_compose=False,
            testing=False,
            pre_commit=False,
            rate_limiting=False,
            cache_backend=CacheBackend.NONE,
            health_checks=False,
            github_workflow=GitHubWorkflow.NONE,
            project_structure=ProjectStructure.FLAT,
            include_examples=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Core files always generated
            assert (project_dir / "app/main.py").exists()
            assert (project_dir / "app/config.py").exists()
            assert (project_dir / "pyproject.toml").exists()
            assert (project_dir / "README.md").exists()
            assert (project_dir / ".gitignore").exists()
            assert (project_dir / ".env.example").exists()

            # Nothing extra
            assert not (project_dir / "app/database.py").exists()
            assert not (project_dir / "app/core/security.py").exists()
            assert not (project_dir / "Dockerfile").exists()
            assert not (project_dir / "docker-compose.yml").exists()
            assert not (project_dir / ".pre-commit-config.yaml").exists()
            assert not (project_dir / "tests/conftest.py").exists()

            # README still has box-drawing chars (flat structure diagram)
            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in readme

    # -- ORM variations -------------------------------------------------------

    def test_sqlmodel_orm(self):
        """SQLModel ORM generates database.py (uses SQLAlchemy under the hood)."""
        config = ProjectConfig(
            project_name="sqlmodel-test",
            database=Database.POSTGRESQL,
            orm=ORM.SQLMODEL,
            migration_tool=MigrationTool.ALEMBIC,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            db_content = (project_dir / "app/database.py").read_text(encoding="utf-8")
            # SQLModel template currently uses SQLAlchemy async engine underneath
            assert "sqlalchemy" in db_content.lower()

    def test_tortoise_orm(self):
        """Tortoise ORM generates different database.py and model files."""
        config = ProjectConfig(
            project_name="tortoise-test",
            database=Database.POSTGRESQL,
            orm=ORM.TORTOISE,
            migration_tool=MigrationTool.AERICH,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            db_content = (project_dir / "app/database.py").read_text(encoding="utf-8")
            assert "tortoise" in db_content.lower()

    # -- Cache backend variations ---------------------------------------------

    def test_redis_cache(self):
        """Redis cache backend generates cache.py with redis content."""
        config = ProjectConfig(
            project_name="redis-cache",
            cache_backend=CacheBackend.REDIS,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            cache_file = project_dir / "app/core/cache.py"
            assert cache_file.exists()
            content = cache_file.read_text(encoding="utf-8")
            assert "redis" in content.lower()

    def test_memcached_cache(self):
        """Memcached cache backend generates cache.py with memcached content."""
        config = ProjectConfig(
            project_name="memcached-cache",
            cache_backend=CacheBackend.MEMCACHED,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            cache_file = project_dir / "app/core/cache.py"
            assert cache_file.exists()
            content = cache_file.read_text(encoding="utf-8")
            assert "memcach" in content.lower()

    def test_inmemory_cache(self):
        """InMemory cache backend generates cache.py with in-memory content."""
        config = ProjectConfig(
            project_name="inmemory-cache",
            cache_backend=CacheBackend.INMEMORY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            cache_file = project_dir / "app/core/cache.py"
            assert cache_file.exists()

    def test_no_cache(self):
        """No cache backend skips cache.py."""
        config = ProjectConfig(
            project_name="no-cache",
            cache_backend=CacheBackend.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/core/cache.py").exists()

    # -- Logging variations ---------------------------------------------------

    def test_loguru_logging(self):
        """Loguru logging generates appropriate logging config."""
        config = ProjectConfig(
            project_name="loguru-log",
            logging_lib=LoggingLib.LOGURU,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            log_file = project_dir / "app/core/logging.py"
            assert log_file.exists()
            content = log_file.read_text(encoding="utf-8")
            assert "loguru" in content.lower()

    def test_structlog_logging(self):
        """Structlog logging generates appropriate logging config."""
        config = ProjectConfig(
            project_name="structlog-log",
            logging_lib=LoggingLib.STRUCTLOG,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            log_file = project_dir / "app/core/logging.py"
            assert log_file.exists()
            content = log_file.read_text(encoding="utf-8")
            assert "structlog" in content.lower()

    def test_standard_logging(self):
        """Standard logging generates basic logging config."""
        config = ProjectConfig(
            project_name="std-log",
            logging_lib=LoggingLib.STANDARD,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            log_file = project_dir / "app/core/logging.py"
            assert log_file.exists()
            content = log_file.read_text(encoding="utf-8")
            assert "logging" in content.lower()

    # -- Package manager variations -------------------------------------------

    def test_uv_package_manager(self):
        """UV package manager appears in README and CI."""
        config = ProjectConfig(
            project_name="uv-pkg",
            package_manager=PackageManager.UV,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            assert "uv" in readme

    def test_pip_package_manager(self):
        """PIP package manager appears in README and CI."""
        config = ProjectConfig(
            project_name="pip-pkg",
            package_manager=PackageManager.PIP,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            assert "pip install" in readme

    # -- Linter / type checker variations -------------------------------------

    def test_ruff_linter(self):
        """Ruff linter generates ruff.toml."""
        config = ProjectConfig(
            project_name="ruff-lint",
            linter=Linter.RUFF,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "ruff.toml").exists()

    def test_black_isort_linter(self):
        """Black+isort linter does NOT generate ruff.toml."""
        config = ProjectConfig(
            project_name="black-lint",
            linter=Linter.BLACK_ISORT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "ruff.toml").exists()

    def test_mypy_strict_type_checker(self):
        """Mypy strict generates mypy.ini."""
        config = ProjectConfig(
            project_name="mypy-strict",
            type_checker=TypeChecker.MYPY_STRICT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "mypy.ini").exists()
            assert not (project_dir / "pyrefly.toml").exists()

    def test_mypy_standard_type_checker(self):
        """Mypy standard generates mypy.ini."""
        config = ProjectConfig(
            project_name="mypy-std",
            type_checker=TypeChecker.MYPY_STANDARD,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "mypy.ini").exists()

    def test_pyrefly_type_checker(self):
        """Pyrefly generates pyrefly.toml instead of mypy.ini."""
        config = ProjectConfig(
            project_name="pyrefly-tc",
            type_checker=TypeChecker.PYREFLY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "pyrefly.toml").exists()
            assert not (project_dir / "mypy.ini").exists()

    def test_no_type_checker(self):
        """No type checker generates neither mypy.ini nor pyrefly.toml."""
        config = ProjectConfig(
            project_name="no-tc",
            type_checker=TypeChecker.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "mypy.ini").exists()
            assert not (project_dir / "pyrefly.toml").exists()

    # -- GitHub workflow variations -------------------------------------------

    def test_ci_only_workflow(self):
        """CI_ONLY generates ci.yml but not deploy.yml."""
        config = ProjectConfig(
            project_name="ci-only",
            github_workflow=GitHubWorkflow.CI_ONLY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / ".github/workflows/ci.yml").exists()
            assert not (project_dir / ".github/workflows/deploy.yml").exists()

    def test_ci_deploy_workflow(self):
        """CI_DEPLOY generates both ci.yml and deploy.yml."""
        config = ProjectConfig(
            project_name="ci-deploy",
            github_workflow=GitHubWorkflow.CI_DEPLOY,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / ".github/workflows/ci.yml").exists()
            assert (project_dir / ".github/workflows/deploy.yml").exists()

    def test_no_workflow(self):
        """No GitHub workflow skips workflow files."""
        config = ProjectConfig(
            project_name="no-workflow",
            github_workflow=GitHubWorkflow.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # The directory might still exist (created in _create_directories)
            # but no workflow files should be present
            assert not (project_dir / ".github/workflows/ci.yml").exists()
            assert not (project_dir / ".github/workflows/deploy.yml").exists()

    # -- Migration tool variations --------------------------------------------

    def test_alembic_migration(self):
        """Alembic generates alembic.ini and migrations/ directory."""
        config = ProjectConfig(
            project_name="alembic-mig",
            database=Database.POSTGRESQL,
            migration_tool=MigrationTool.ALEMBIC,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "alembic.ini").exists()
            assert (project_dir / "migrations/env.py").exists()
            assert (project_dir / "migrations/script.py.mako").exists()
            assert (project_dir / "migrations/versions").is_dir()

    def test_aerich_migration(self):
        """Aerich creates migrations/ directory but no alembic files."""
        config = ProjectConfig(
            project_name="aerich-mig",
            database=Database.POSTGRESQL,
            orm=ORM.TORTOISE,
            migration_tool=MigrationTool.AERICH,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "alembic.ini").exists()
            assert (project_dir / "migrations").is_dir()

    def test_no_migration(self):
        """No migration tool skips migration files."""
        config = ProjectConfig(
            project_name="no-mig",
            database=Database.POSTGRESQL,
            migration_tool=MigrationTool.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "alembic.ini").exists()
            assert not (project_dir / "migrations/env.py").exists()

    # -- Misc toggles ---------------------------------------------------------

    def test_rate_limiting_enabled(self):
        """Rate limiting generates rate_limit.py."""
        config = ProjectConfig(
            project_name="rate-limit",
            rate_limiting=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/core/rate_limit.py").exists()

    def test_rate_limiting_disabled(self):
        """No rate limiting skips rate_limit.py."""
        config = ProjectConfig(
            project_name="no-rate-limit",
            rate_limiting=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/core/rate_limit.py").exists()

    def test_health_checks_enabled(self):
        """Health checks enabled generates health.py."""
        config = ProjectConfig(
            project_name="health-on",
            health_checks=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/core/health.py").exists()

    def test_health_checks_disabled(self):
        """Health checks disabled skips health.py."""
        config = ProjectConfig(
            project_name="health-off",
            health_checks=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/core/health.py").exists()

    def test_admin_panel_with_database(self):
        """Admin panel with database generates admin files."""
        config = ProjectConfig(
            project_name="admin-test",
            include_admin=True,
            database=Database.POSTGRESQL,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/admin/views.py").exists()
            assert (project_dir / "app/admin/__init__.py").exists()

    def test_admin_panel_without_database(self):
        """Admin panel without database skips admin files."""
        config = ProjectConfig(
            project_name="admin-no-db",
            include_admin=True,
            database=Database.NONE,
            orm=ORM.NONE,
            migration_tool=MigrationTool.NONE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/admin/views.py").exists()

    def test_pre_commit_enabled(self):
        """Pre-commit generates .pre-commit-config.yaml."""
        config = ProjectConfig(
            project_name="precommit-on",
            pre_commit=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / ".pre-commit-config.yaml").exists()

    def test_pre_commit_disabled(self):
        """Pre-commit disabled skips .pre-commit-config.yaml."""
        config = ProjectConfig(
            project_name="precommit-off",
            pre_commit=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / ".pre-commit-config.yaml").exists()

    def test_testing_enabled(self):
        """Testing enabled generates tests/conftest.py."""
        config = ProjectConfig(
            project_name="tests-on",
            testing=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "tests/conftest.py").exists()

    def test_testing_disabled(self):
        """Testing disabled skips test files."""
        config = ProjectConfig(
            project_name="tests-off",
            testing=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "tests/conftest.py").exists()

    def test_include_examples_with_auth(self):
        """include_examples=True with auth generates example routes and tests."""
        config = ProjectConfig(
            project_name="examples-on",
            include_examples=True,
            auth_method=AuthMethod.JWT,
            testing=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/api/v1/routes/auth.py").exists()
            assert (project_dir / "app/api/v1/routes/users.py").exists()
            assert (project_dir / "tests/test_health.py").exists()
            assert (project_dir / "tests/test_auth.py").exists()

    def test_exclude_examples(self):
        """include_examples=False skips example routes and tests."""
        config = ProjectConfig(
            project_name="examples-off",
            include_examples=False,
            auth_method=AuthMethod.JWT,
            testing=True,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/api/v1/routes/auth.py").exists()
            assert not (project_dir / "app/api/v1/routes/users.py").exists()
            assert not (project_dir / "tests/test_health.py").exists()
            assert not (project_dir / "tests/test_auth.py").exists()

    def test_aws_services(self):
        """AWS enabled with S3 and SES generates service files."""
        config = ProjectConfig(
            project_name="aws-test",
            aws_enabled=True,
            aws_services=[AWSService.S3, AWSService.SES],
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/services/s3.py").exists()
            assert (project_dir / "app/services/ses.py").exists()

    def test_no_aws(self):
        """AWS disabled skips service files."""
        config = ProjectConfig(
            project_name="no-aws",
            aws_enabled=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert not (project_dir / "app/services/s3.py").exists()
            assert not (project_dir / "app/services/ses.py").exists()

    # -- Cross-product: structure x auth x database ---------------------------

    @pytest.mark.parametrize(
        "structure",
        [ProjectStructure.LAYERED, ProjectStructure.DOMAIN_DRIVEN, ProjectStructure.FLAT],
    )
    def test_all_structures_generate_valid_utf8_readme(self, structure):
        """Each project structure produces a README with valid UTF-8 box-drawing chars."""
        config = ProjectConfig(
            project_name=f"struct-{structure.value}",
            project_structure=structure,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in readme, (
                    f"Box-drawing char {char!r} missing in {structure.value} README"
                )

    @pytest.mark.parametrize(
        "auth",
        [AuthMethod.JWT, AuthMethod.OAUTH2, AuthMethod.SESSION, AuthMethod.NONE],
    )
    def test_all_auth_methods_generate_successfully(self, auth):
        """Every auth method generates a project without errors."""
        config = ProjectConfig(
            project_name=f"auth-{auth.value}",
            auth_method=auth,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/main.py").exists()
            assert (project_dir / "README.md").exists()
            # Verify all files are valid UTF-8
            for f in project_dir.rglob("*"):
                if f.is_file():
                    f.read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        "db,orm,migration",
        [
            (Database.POSTGRESQL, ORM.SQLALCHEMY, MigrationTool.ALEMBIC),
            (Database.MYSQL, ORM.SQLALCHEMY, MigrationTool.ALEMBIC),
            (Database.SQLITE, ORM.SQLALCHEMY, MigrationTool.ALEMBIC),
            (Database.POSTGRESQL, ORM.SQLMODEL, MigrationTool.ALEMBIC),
            (Database.POSTGRESQL, ORM.TORTOISE, MigrationTool.AERICH),
            (Database.NONE, ORM.NONE, MigrationTool.NONE),
        ],
    )
    def test_all_database_combos_generate_successfully(self, db, orm, migration):
        """Every database + ORM + migration combination generates without errors."""
        config = ProjectConfig(
            project_name=f"db-{db.value}-{orm.value}",
            database=db,
            orm=orm,
            migration_tool=migration,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            assert (project_dir / "app/main.py").exists()
            assert (project_dir / "README.md").exists()
            # Verify all files are valid UTF-8
            for f in project_dir.rglob("*"):
                if f.is_file():
                    f.read_text(encoding="utf-8")

    def test_full_featured_project(self):
        """Generate with every feature enabled -- the maximal config."""
        config = ProjectConfig(
            project_name="full-featured",
            project_description="All features enabled",
            author_name="Test Author",
            author_email="test@example.com",
            python_version=PythonVersion.PY313,
            database=Database.POSTGRESQL,
            orm=ORM.SQLALCHEMY,
            migration_tool=MigrationTool.ALEMBIC,
            auth_method=AuthMethod.JWT,
            include_admin=True,
            cors_enabled=True,
            api_versioning=True,
            rate_limiting=True,
            message_broker=MessageBroker.RABBITMQ,
            task_queue=TaskQueue.CELERY,
            cache_backend=CacheBackend.REDIS,
            logging_lib=LoggingLib.LOGURU,
            sentry_enabled=True,
            health_checks=True,
            package_manager=PackageManager.UV,
            linter=Linter.RUFF,
            type_checker=TypeChecker.MYPY_STRICT,
            testing=True,
            pre_commit=True,
            docker=True,
            docker_compose=True,
            github_workflow=GitHubWorkflow.CI_DEPLOY,
            project_structure=ProjectStructure.LAYERED,
            include_examples=True,
            aws_enabled=True,
            aws_services=[AWSService.S3, AWSService.SES],
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = _generate(config, tmpdir)

            # Verify core files
            assert (project_dir / "app/main.py").exists()
            assert (project_dir / "app/config.py").exists()
            assert (project_dir / "app/database.py").exists()
            assert (project_dir / "app/core/security.py").exists()
            assert (project_dir / "app/core/cache.py").exists()
            assert (project_dir / "app/core/health.py").exists()
            assert (project_dir / "app/core/rate_limit.py").exists()
            assert (project_dir / "app/core/logging.py").exists()
            assert (project_dir / "app/admin/views.py").exists()
            assert (project_dir / "app/services/s3.py").exists()
            assert (project_dir / "app/services/ses.py").exists()
            assert (project_dir / "Dockerfile").exists()
            assert (project_dir / "docker-compose.yml").exists()
            assert (project_dir / "alembic.ini").exists()
            assert (project_dir / "ruff.toml").exists()
            assert (project_dir / "mypy.ini").exists()
            assert (project_dir / ".pre-commit-config.yaml").exists()
            assert (project_dir / ".github/workflows/ci.yml").exists()
            assert (project_dir / ".github/workflows/deploy.yml").exists()
            assert (project_dir / "tests/conftest.py").exists()
            assert (project_dir / "tests/test_health.py").exists()
            assert (project_dir / "tests/test_auth.py").exists()

            # Verify all files are valid UTF-8
            for f in project_dir.rglob("*"):
                if f.is_file():
                    f.read_text(encoding="utf-8")

            # README has box-drawing chars
            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            for char in BOX_DRAWING_CHARS:
                assert char in readme
