# Installation

FastAPI Smith requires Python 3.10 or later.

## Installing FastAPI Smith

### Using uvx (Recommended)

The easiest way to run FastAPI Smith is with `uvx`, which runs it without installing:

```bash
uvx fastapi-smith
```

This is perfect for one-time use or trying it out.

### Using uv (Global Install)

For repeated use, install it globally with `uv`:

```bash
uv tool install fastapi-smith
```

Then run:

```bash
fastapi-smith
```

### Using pipx

`pipx` is another great option for installing CLI tools:

```bash
pipx install fastapi-smith
```

Then run:

```bash
fastapi-smith
```

### Using pip

You can also use regular pip:

```bash
pip install fastapi-smith
```

!!! warning "PATH Configuration"
    When using pip, ensure your Python scripts directory is in your PATH. On Linux/macOS this is usually `~/.local/bin`, on Windows it's `%APPDATA%\Python\Scripts`.

### From Source

To install from source for development:

```bash
git clone https://github.com/dhruvbhavsar0612/fastsql-project-setup.git
cd fastsql-project-setup
uv sync
uv run fastapi-smith
```

## Verifying Installation

Check that FastAPI Smith is installed correctly:

```bash
fastapi-smith --version
```

You should see output like:

```
fastapi-smith version 0.1.5
```

## Updating

### With uv
```bash
uv tool upgrade fastapi-smith
```

### With pipx
```bash
pipx upgrade fastapi-smith
```

### With pip
```bash
pip install --upgrade fastapi-smith
```

## Troubleshooting

### Command not found

If you get "command not found" after installation:

1. **Check if the script directory is in PATH**:
   ```bash
   # Find where pip installed it
   pip show fastapi-smith
   
   # On Linux/macOS, add to PATH in ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Use Python module syntax**:
   ```bash
   python -m fastapi_smith.cli
   ```

3. **Try pipx instead** (recommended for CLI tools):
   ```bash
   pip uninstall fastapi-smith
   pipx install fastapi-smith
   ```

### Permission errors

On Linux/macOS, avoid using `sudo pip install`. Instead:

```bash
pip install --user fastapi-smith
# or use pipx
pipx install fastapi-smith
```

## Next Steps

Now that you have FastAPI Smith installed, let's create your first project:

[Quick Start →](quickstart.md){ .md-button .md-button--primary }
