# Contributing to FastAPI Smith

Thank you for your interest in contributing to FastAPI Smith! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](https://github.com/dhruvbhavsar0612/fastsql-project-setup/blob/main/CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Open an issue on [GitHub Issues](https://github.com/dhruvbhavsar0612/fastsql-project-setup/issues) with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Suggesting Features

Open a feature request on [GitHub Issues](https://github.com/dhruvbhavsar0612/fastsql-project-setup/issues) with:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach

### Contributing Code

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## Development Setup

```bash
git clone https://github.com/dhruvbhavsar0612/fastsql-project-setup.git
cd fastsql-project-setup
uv sync
uv run pre-commit install
```

## Running Tests

```bash
uv run pytest
uv run pytest --cov=fastapi_smith
```

## Code Style

We use:
- **Ruff** for linting and formatting
- **mypy** for type checking
- **pre-commit** for automated checks

```bash
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
