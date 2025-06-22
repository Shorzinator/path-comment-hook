# Contributing to path-comment-hook

Thank you for your interest in contributing to path-comment-hook! This document provides guidelines and information for contributors.

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/path-comment-hook.git
   cd path-comment-hook
   ```
3. **Set up development environment**:
   ```bash
   poetry install
   poetry shell
   pre-commit install
   ```
4. **Run tests** to ensure everything works:
   ```bash
   make test
   ```

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Shorzinator/path-comment-hook.git
cd path-comment-hook

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install

# Verify installation
make test
make lint
```

### Development Commands

We use a Makefile for common development tasks:

```bash
# Run tests
make test
make test-cov          # With coverage report

# Code quality
make lint              # Run all linters
make format           # Format code
make type-check       # Type checking

# Documentation
make docs-serve       # Serve docs locally
make docs-build       # Build docs

# Full quality check
make check            # Run all quality checks
```

## Making Changes

### Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write tests** for new functionality

4. **Run quality checks**:
   ```bash
   make check
   ```

5. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add new functionality"
   ```

6. **Push and create a pull request**

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat: add delete command functionality
fix: resolve Windows line ending issues
docs: update installation instructions
test: add comprehensive CLI tests
```

## Code Style

### Python Style Guidelines

- **Line length**: 100 characters max
- **Formatting**: Use Ruff for formatting
- **Type hints**: Required for all functions and methods
- **Docstrings**: Use Google-style docstrings
- **Imports**: Use absolute imports, sort with Ruff

### Example Function

```python
def process_file(file_path: Path, project_root: Path, mode: str = "fix") -> Result:
    """Process a single file to add or check path headers.

    Args:
        file_path: Path to the file to process.
        project_root: Root directory of the project.
        mode: Processing mode, either "fix" or "check".

    Returns:
        Result enum indicating the outcome.

    Raises:
        FileHandlingError: If file cannot be processed.
    """
    # Implementation here
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Trailing whitespace**: Remove trailing whitespace
- **End of file**: Ensure files end with newline

## Reporting Issues

Before creating a new issue:

1. **Search existing issues** for duplicates
2. **Check the documentation** for solutions
3. **Test with the latest version**

When reporting bugs, include:
- Operating system and Python version
- path-comment-hook version
- Complete error messages
- Steps to reproduce
- Expected vs actual behavior

## Release Process

Releases are automated but follow this process:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create release PR** with version bump
4. **Merge to main** triggers automated release
5. **GitHub Actions** handles PyPI publishing

## Recognition

Contributors are recognized in:
- Release notes
- GitHub contributors page
- Special mentions for significant contributions

Thank you for contributing to path-comment-hook!

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

Thank you for contributing to path-comment-hook! 🎉
