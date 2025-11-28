"""Tests for CLI."""

import re

from typer.testing import CliRunner

from fastapi_smith import __version__
from fastapi_smith.cli import app

runner = CliRunner()


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_pattern.sub("", text)


def test_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Interactively scaffold" in output
    assert "--output" in output
    assert "--version" in output
