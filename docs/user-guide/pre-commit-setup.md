---
description: Set up path-comment-hook with pre-commit for automated file processing
keywords: pre-commit, automation, git hooks, workflow
---

# Pre-commit Setup

Integrate path-comment-hook with pre-commit for automatic path header management. This ensures path headers are consistently applied across your team's workflow.

## Installation

First, install pre-commit:

```bash
# Using pip
pip install pre-commit

# Using pipx
pipx install pre-commit

# Using conda
conda install -c conda-forge pre-commit
```

## Configuration

Create or update `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0  # Use the latest version
    hooks:
      - id: path-comment
```

Install the pre-commit hooks:

```bash
pre-commit install
```

## Basic Usage

Once configured, the hook runs automatically on git commits:

```bash
git add .
git commit -m "Your commit message"
# path-comment-hook runs automatically
```

## Advanced Configuration

### Custom Arguments

Pass additional arguments to the hook:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
        args: [--workers=2, --progress]
```

### File Filtering

Limit which files the hook processes:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
        files: ^src/.*\.py$  # Only Python files in src/
```

### Integration with Other Hooks

Recommended order with other formatting tools:

```yaml
repos:
  # First: Add path headers
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment

  # Then: Format code
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

## Troubleshooting

### Hook Fails on Large Projects

For large codebases, increase timeout or reduce workers:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
        args: [--workers=1]
```

### Skip the Hook Temporarily

Skip path-comment-hook for a specific commit:

```bash
git commit -m "Message" --no-verify
```

Or skip just this hook:

```bash
SKIP=path-comment git commit -m "Message"
```

### Update Hook Version

Update to the latest version:

```bash
pre-commit autoupdate
```

## Best Practices

1. **Pin versions**: Always specify a version in `rev:`
2. **Test first**: Run `pre-commit run --all-files` before committing
3. **Team coordination**: Ensure all team members use the same configuration
4. **CI integration**: Run pre-commit in CI to catch issues

## See Also

- [CLI Usage](cli-usage.md) - Command-line options
- [Configuration](configuration.md) - Customize behavior
