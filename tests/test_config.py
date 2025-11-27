"""Tests for configuration models."""

import pytest

from setup_fastsql.config import (
    Database,
    ORM,
    ProjectConfig,
    PythonVersion,
)


class TestProjectConfig:
    """Tests for ProjectConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ProjectConfig()
        
        assert config.project_name == "my-fastapi-app"
        assert config.python_version == PythonVersion.PY312
        assert config.database == Database.POSTGRESQL
        assert config.orm == ORM.SQLALCHEMY

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ProjectConfig(
            project_name="my-app",
            python_version=PythonVersion.PY311,
            database=Database.MYSQL,
        )
        
        assert config.project_name == "my-app"
        assert config.python_version == PythonVersion.PY311
        assert config.database == Database.MYSQL

    def test_get_db_driver_postgresql(self):
        """Test PostgreSQL driver."""
        config = ProjectConfig(database=Database.POSTGRESQL)
        assert config.get_db_driver() == "psycopg[binary]"

    def test_get_db_driver_mysql(self):
        """Test MySQL driver."""
        config = ProjectConfig(database=Database.MYSQL)
        assert config.get_db_driver() == "asyncmy"

    def test_get_db_driver_sqlite(self):
        """Test SQLite driver."""
        config = ProjectConfig(database=Database.SQLITE)
        assert config.get_db_driver() == "aiosqlite"

    def test_get_db_driver_none(self):
        """Test no database driver."""
        config = ProjectConfig(database=Database.NONE)
        assert config.get_db_driver() == ""

    def test_get_db_url_template_postgresql(self):
        """Test PostgreSQL URL template."""
        config = ProjectConfig(database=Database.POSTGRESQL)
        url = config.get_db_url_template()
        assert "postgresql+psycopg" in url

    def test_get_db_url_template_mysql(self):
        """Test MySQL URL template."""
        config = ProjectConfig(database=Database.MYSQL)
        url = config.get_db_url_template()
        assert "mysql+asyncmy" in url


class TestEnums:
    """Tests for enum values."""

    def test_python_versions(self):
        """Test Python version enum values."""
        assert PythonVersion.PY310.value == "3.10"
        assert PythonVersion.PY311.value == "3.11"
        assert PythonVersion.PY312.value == "3.12"
        assert PythonVersion.PY313.value == "3.13"

    def test_database_values(self):
        """Test Database enum values."""
        assert Database.POSTGRESQL.value == "postgresql"
        assert Database.MYSQL.value == "mysql"
        assert Database.SQLITE.value == "sqlite"
        assert Database.NONE.value == "none"

    def test_orm_values(self):
        """Test ORM enum values."""
        assert ORM.SQLALCHEMY.value == "sqlalchemy"
        assert ORM.SQLMODEL.value == "sqlmodel"
        assert ORM.TORTOISE.value == "tortoise"
        assert ORM.NONE.value == "none"
