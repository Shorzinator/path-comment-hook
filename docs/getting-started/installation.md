---
description: Learn how to install path-comment-hook via pip, pipx, or poetry
keywords: installation, setup, pip, poetry, pre-commit
---

# Installation

path-comment-hook can be installed in several ways depending on your preferred Python package manager and use case.

## Requirements

- Python 3.8 or higher
- Works on Linux, macOS, and Windows

## Installation Methods

### pip (Recommended)

The simplest way to install path-comment-hook:

```bash
pip install path-comment-hook
```

This installs the tool globally and makes the `path-comment-hook` command available in your terminal.

### pipx (Isolated Installation)

For an isolated installation that won't interfere with other Python packages:

```bash
# Install pipx if you don't have it
pip install pipx

# Install path-comment-hook with pipx
pipx install path-comment-hook
```

!!! tip "Why pipx?"
    pipx installs Python applications in isolated environments, preventing dependency conflicts while keeping the command globally available.

### Poetry (Development Projects)

For projects using Poetry, add as a development dependency:

```bash
# Add to dev dependencies
poetry add --group dev path-comment-hook

# Or if using older Poetry versions
poetry add --dev path-comment-hook
```

Then run with:

```bash
poetry run path-comment-hook --help
```

### From Source (Development)

To install the latest development version:

```bash
# Clone the repository
git clone https://github.com/shouryamaheshwari/path-comment-hook.git
cd path-comment-hook

# Install with pip
pip install -e .

# Or with Poetry
poetry install
```

## Verify Installation

After installation, verify it's working:

```bash
path-comment-hook --version
```

You should see output like:

```text
path-comment-hook 0.3.0
```

## Pre-commit Installation

Most users will want to use path-comment-hook as a pre-commit hook. This doesn't require installing the package directly:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0  # Use the latest version
    hooks:
      - id: path-comment
```

Then install the hook:

```bash
pre-commit install
```

!!! note "Pre-commit vs Direct Installation"
    When using pre-commit, the tool is automatically installed in an isolated environment. You don't need to install it separately unless you want to use it directly from the command line.

## Platform-Specific Notes

### macOS

If you're using Homebrew's Python:

```bash
# Use pip3 if pip points to Python 2
pip3 install path-comment-hook
```

### Windows

On Windows, you might need to use:

```cmd
# Command Prompt
python -m pip install path-comment-hook

# PowerShell
py -m pip install path-comment-hook
```

### Linux

Most Linux distributions work with the standard pip installation. For Ubuntu/Debian:

```bash
# Install pip if not available
sudo apt update
sudo apt install python3-pip

# Install path-comment-hook
pip3 install path-comment-hook
```

## Docker

You can also use path-comment-hook in a Docker container:

```dockerfile
FROM python:3.11-slim

RUN pip install path-comment-hook

# Your application code here
COPY . /app
WORKDIR /app

# Run path-comment-hook
RUN path-comment-hook --all
```

## Troubleshooting

### Command Not Found

If you get "command not found" after installation:

1. **Check PATH**: Make sure Python's scripts directory is in your PATH
2. **Use full path**: Try `python -m path_comment` instead
3. **Virtual environment**: Activate your virtual environment if you installed there

### Permission Errors

On Unix systems, if you get permission errors:

```bash
# Install for current user only
pip install --user path-comment-hook

# Or use sudo (not recommended)
sudo pip install path-comment-hook
```

### Version Conflicts

If you have dependency conflicts:

```bash
# Use pipx for isolated installation
pipx install path-comment-hook

# Or create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install path-comment-hook
```

## What's Next?

Now that you have path-comment-hook installed:

- [🚀 Quick Start](quick-start.md) - Run your first path comment operation
- [🔧 Pre-commit Setup](../user-guide/pre-commit-setup.md) - Integrate with your workflow
- [⚙️ Configuration](../user-guide/configuration.md) - Customize for your project
