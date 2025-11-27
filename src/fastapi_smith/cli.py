"""CLI entry point for fastapi-smith."""

import asyncio
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from . import __version__
from .generator import ProjectGenerator
from .prompts import confirm_config, gather_all_config

app = typer.Typer(
    name="fastapi-smith",
    help="Interactive CLI to scaffold FastAPI projects with database, auth, admin, and more.",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"fastapi-smith version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    output_dir: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output directory (defaults to project name in current directory)",
        ),
    ] = None,
    version: Annotated[  # noqa: ARG001
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = False,
) -> None:
    """
    Interactively scaffold a new FastAPI project.

    This tool will guide you through selecting options for your project including:
    - Database and ORM configuration
    - Authentication method
    - Admin panel setup
    - Caching and message queue
    - Logging and monitoring
    - Development tools
    - Docker and CI/CD
    - AWS integration
    """
    try:
        asyncio.run(_async_main(output_dir))
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        sys.exit(1)


async def _async_main(output_dir: Path | None) -> None:
    """Async main function to handle interactive prompts."""
    # Gather configuration from user
    config = await gather_all_config()

    # Confirm configuration
    confirmed = await confirm_config(config)

    if not confirmed:
        console.print("[yellow]Setup cancelled.[/yellow]")
        return

    # Determine output directory
    project_dir = output_dir or Path.cwd() / config.project_name

    # Check if directory exists
    if project_dir.exists() and any(project_dir.iterdir()):
        overwrite = typer.confirm(
            f"Directory {project_dir} already exists and is not empty. Overwrite?"
        )
        if not overwrite:
            console.print("[yellow]Setup cancelled.[/yellow]")
            return

    # Generate project
    generator = ProjectGenerator(config, project_dir)
    generator.generate()

    # Print next steps
    _print_next_steps(config, project_dir)


def _print_next_steps(config, project_dir: Path) -> None:
    """Print next steps for the user."""
    console.print("\n[bold green]Next steps:[/bold green]\n")
    console.print(f"  cd {project_dir.name}")

    if config.package_manager.value == "uv":
        console.print("  uv sync")
        console.print("  uv run uvicorn app.main:app --reload")
    else:
        console.print("  pip install -e .")
        console.print("  uvicorn app.main:app --reload")

    if config.pre_commit:
        console.print("\n  # Setup pre-commit hooks")
        console.print("  pre-commit install")

    if config.migration_tool.value == "alembic":
        console.print("\n  # Run database migrations")
        if config.package_manager.value == "uv":
            console.print("  uv run alembic upgrade head")
        else:
            console.print("  alembic upgrade head")

    if config.docker:
        console.print("\n  # Or run with Docker")
        console.print("  docker-compose up --build")

    console.print("\n[dim]Documentation: http://localhost:8000/docs[/dim]")
    if config.include_admin:
        console.print("[dim]Admin panel: http://localhost:8000/admin[/dim]")


if __name__ == "__main__":
    app()
