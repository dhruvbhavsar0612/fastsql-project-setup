"""Tests for project generator."""

import re
import tempfile
from pathlib import Path

from fastapi_smith.config import (
    ORM,
    AuthMethod,
    Database,
    MigrationTool,
    ProjectConfig,
    ProjectStructure,
)
from fastapi_smith.generator import ProjectGenerator


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
            project_dir = Path(tmpdir) / "test-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

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
            project_dir = Path(tmpdir) / "docker-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

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
            project_dir = Path(tmpdir) / "no-db-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

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
            project_dir = Path(tmpdir) / "auth-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            assert (project_dir / "app/core/security.py").exists()
            # Check security file has JWT related content
            security_content = (project_dir / "app/core/security.py").read_text()
            assert "jwt" in security_content.lower() or "token" in security_content.lower()

    def test_pyproject_has_correct_name(self):
        """Test that pyproject.toml has the correct project name."""
        config = ProjectConfig(
            project_name="my-custom-project",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "my-custom-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            pyproject_content = (project_dir / "pyproject.toml").read_text()
            assert 'name = "my-custom-project"' in pyproject_content

    def test_main_py_has_fastapi_app(self):
        """Test that main.py has a FastAPI app."""
        config = ProjectConfig(project_name="fastapi-test")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "fastapi-test"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            main_content = (project_dir / "app/main.py").read_text()
            assert "FastAPI" in main_content
            assert "app" in main_content

    def test_layered_structure(self):
        """Test generating a project with layered structure."""
        config = ProjectConfig(
            project_name="layered-project",
            project_structure=ProjectStructure.LAYERED,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "layered-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

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
            project_dir = Path(tmpdir) / "deps-test-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            pyproject_content = (project_dir / "pyproject.toml").read_text()
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
            project_dir = Path(tmpdir) / "imports-test-layered"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text()
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
            project_dir = Path(tmpdir) / "imports-test-ddd"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text()
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
            project_dir = Path(tmpdir) / "imports-test-flat"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            # Check all .py files in app/ for relative imports
            app_dir = project_dir / "app"
            relative_import_pattern = re.compile(r"from \.\.+")

            for py_file in app_dir.rglob("*.py"):
                content = py_file.read_text()
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
            project_dir = Path(tmpdir) / "app-imports-test"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            # Check auth.py has correct absolute imports
            auth_file = project_dir / "app/api/v1/routes/auth.py"
            if auth_file.exists():
                content = auth_file.read_text()
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
            project_dir = Path(tmpdir) / "hatch-test-project"
            generator = ProjectGenerator(config, project_dir)
            generator.generate()

            pyproject_content = (project_dir / "pyproject.toml").read_text()
            assert "[tool.hatch.build.targets.wheel]" in pyproject_content
            assert 'packages = ["app"]' in pyproject_content
