"""Tests for CLI."""

from typer.testing import CliRunner

from setup_fastsql.cli import app

runner = CliRunner()


def test_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Interactively scaffold" in result.stdout
    assert "--output" in result.stdout
    assert "--version" in result.stdout
