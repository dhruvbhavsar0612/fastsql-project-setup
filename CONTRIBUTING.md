# Contributing to setup-fastsql

First off, thank you for considering contributing to setup-fastsql! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

- Make sure you have a [GitHub account](https://github.com/signup)
- Fork the repository on GitHub
- Clone your fork locally

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (command line inputs, configuration options selected)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Adding New Features

Some ideas for contributions:

- **New project templates** - Add support for new frameworks or tools
- **New database support** - Add drivers for other databases
- **New cloud providers** - Extend beyond AWS (GCP, Azure, etc.)
- **New authentication methods** - Add more auth options
- **Internationalization** - Add support for other languages
- **Documentation** - Improve docs, add examples, fix typos

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the style guidelines
5. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fastsql-project-setup.git
cd fastsql-project-setup

# Install dependencies with uv
uv sync --dev

# Or with pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=setup_fastsql

# Run specific test file
uv run pytest tests/test_generator.py
```

### Running Linters

```bash
# Run ruff linter
uv run ruff check .

# Run ruff formatter
uv run ruff format .

# Run type checker
uv run mypy src/setup_fastsql
```

### Testing Locally

```bash
# Run the CLI locally
uv run setup-fastsql

# Or install in development mode
pip install -e .
setup-fastsql
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   We use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation only
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Fill in the PR template
   - Link any related issues
   - Request review from maintainers

6. **Address review feedback**
   - Make requested changes
   - Push additional commits
   - Re-request review when ready

## Style Guidelines

### Python Code Style

- We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Line length: 100 characters
- Use type hints for all function signatures
- Write docstrings for public functions and classes

```python
def generate_project(config: ProjectConfig, output_dir: Path) -> None:
    """
    Generate a new FastAPI project.

    Args:
        config: Project configuration from user prompts
        output_dir: Directory to create the project in

    Raises:
        FileExistsError: If output directory already exists
    """
    ...
```

### Template Style

- Use Jinja2 templates with `.j2` extension
- Keep templates readable with proper indentation
- Use conditional blocks for optional features
- Comment complex logic

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs in the body

### Documentation

- Keep README.md up to date
- Document new features in the appropriate section
- Include code examples where helpful

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

Thank you for contributing!
