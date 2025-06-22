---
description: Configure path-comment-hook for your project needs
keywords: configuration, pyproject.toml, customization, settings
---

# Configuration

path-comment-hook can be customized through configuration files to match your project's specific needs. This guide covers all available configuration options.

## Configuration File

Configuration is stored in your project's `pyproject.toml` file under the `[tool.path-comment]` section:

```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "tests/fixtures/*",
    "docs/*"
]
```

## Configuration Options

### exclude_globs

**Type:** `list[str]`
**Default:** `["*.md", "*.txt", "*.json", "*.lock", ".git/**", "__pycache__/**"]`

Glob patterns for files and directories to exclude from processing.

```toml
[tool.path-comment]
exclude_globs = [
    # Documentation files
    "*.md",
    "*.rst",
    "*.txt",

    # Configuration files
    "*.json",
    "*.yml",
    "*.yaml",
    "*.toml",
    "*.ini",

    # Build artifacts
    "*.lock",
    "build/**",
    "dist/**",

    # Version control
    ".git/**",
    ".svn/**",

    # Python artifacts
    "__pycache__/**",
    "*.egg-info/**",
    ".pytest_cache/**",

    # Test fixtures
    "tests/fixtures/**",
    "tests/data/**",

    # Documentation
    "docs/**",
    "site/**"
]
```

### Supported Patterns

The exclude patterns support standard glob syntax:

| Pattern | Matches |
|---------|---------|
| `*.md` | All Markdown files |
| `tests/**` | Everything in tests directory |
| `**/temp/*` | Files in any temp directory |
| `file?.txt` | file1.txt, file2.txt, etc. |
| `[abc].py` | a.py, b.py, c.py |

## Examples by Project Type

### Python Library

```toml
[tool.path-comment]
exclude_globs = [
    # Standard exclusions
    "*.md",
    "*.txt",
    "*.json",
    "*.lock",
    ".git/**",
    "__pycache__/**",

    # Python specific
    "*.egg-info/**",
    ".pytest_cache/**",
    ".mypy_cache/**",
    ".ruff_cache/**",
    "build/**",
    "dist/**",

    # Documentation
    "docs/**",

    # Test fixtures
    "tests/fixtures/**"
]
```

### Web Application

```toml
[tool.path-comment]
exclude_globs = [
    # Standard exclusions
    "*.md",
    "*.txt",
    "*.json",
    "*.lock",
    ".git/**",
    "__pycache__/**",

    # Web specific
    "static/**",
    "media/**",
    "uploads/**",
    "node_modules/**",
    "*.min.js",
    "*.min.css",

    # Translations
    "locale/**",

    # Database
    "migrations/**",
    "*.db",
    "*.sqlite3"
]
```

### Data Science Project

```toml
[tool.path-comment]
exclude_globs = [
    # Standard exclusions
    "*.md",
    "*.txt",
    "*.json",
    "*.lock",
    ".git/**",
    "__pycache__/**",

    # Data files
    "data/**",
    "datasets/**",
    "*.csv",
    "*.parquet",
    "*.h5",
    "*.hdf5",

    # Notebooks (optional)
    "notebooks/**",
    "*.ipynb",

    # Models
    "models/**",
    "*.pkl",
    "*.joblib",

    # Outputs
    "outputs/**",
    "plots/**",
    "figures/**"
]
```

### Monorepo

```toml
[tool.path-comment]
exclude_globs = [
    # Standard exclusions
    "*.md",
    "*.txt",
    "*.json",
    "*.lock",
    ".git/**",
    "__pycache__/**",

    # Package specific exclusions
    "*/node_modules/**",
    "*/build/**",
    "*/dist/**",
    "*/target/**",

    # Documentation for all packages
    "*/docs/**",

    # Test fixtures for all packages
    "*/tests/fixtures/**",

    # Specific directories
    "infra/**",
    "scripts/**",
    "tools/**"
]
```

## Advanced Configuration

### Per-Directory Config

You can have different configurations for different parts of your project by using multiple `pyproject.toml` files:

```
project/
├── pyproject.toml          # Main config
├── src/
│   └── pyproject.toml      # Source-specific config
└── tests/
    └── pyproject.toml      # Test-specific config
```

### Environment-Specific Config

Use different configurations based on environment:

```toml
# Development configuration
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt"
]

# CI/CD can override with more restrictive patterns
```

## Configuration Validation

path-comment-hook validates your configuration and will show helpful error messages:

```bash
$ path-comment-hook --all
Error: Invalid configuration in pyproject.toml
- exclude_globs must be a list of strings
- Found: exclude_globs = "*.md" (string, not list)
```

## Viewing Current Configuration

Check your current configuration:

```bash
# Show configuration from default location
path-comment-hook show-config

# Show configuration from specific file
path-comment-hook show-config --config custom.toml
```

Output:
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt",
    "*.json",
    "*.lock",
    ".git/**",
    "__pycache__/**"
]
```

## Common Patterns

### Exclude by File Extension

```toml
exclude_globs = [
    "*.log",       # Log files
    "*.tmp",       # Temporary files
    "*.bak",       # Backup files
    "*.swp",       # Vim swap files
    "*.DS_Store"   # macOS metadata
]
```

### Exclude by Directory

```toml
exclude_globs = [
    "vendor/**",     # Third-party code
    "extern/**",     # External dependencies
    "legacy/**",     # Legacy code
    "archive/**"     # Archived code
]
```

### Exclude Test Files

```toml
exclude_globs = [
    "test_*.py",           # Test files
    "*_test.py",           # Alternative test pattern
    "tests/**",            # Test directory
    "spec/**",             # Spec directory
    "**/*_spec.py"         # Spec files anywhere
]
```

### Exclude Generated Files

```toml
exclude_globs = [
    "generated/**",        # Generated code
    "*_pb2.py",           # Protocol buffer files
    "*_pb2_grpc.py",      # gRPC generated files
    "schema.py",          # Generated schema
    "migrations/**"       # Database migrations
]
```

## Override Configuration

### Command Line Override

You can specify a different config file:

```bash
path-comment-hook --config custom.toml --all
```

### Environment Variables

Set configuration through environment:

```bash
export PATH_COMMENT_CONFIG=/path/to/config.toml
path-comment-hook --all
```

## Configuration Best Practices

### Start Simple

Begin with minimal configuration:

```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "tests/fixtures/**"
]
```

### Add as Needed

Expand configuration based on your project's needs:

1. Run path-comment-hook
2. Identify unwanted files being processed
3. Add appropriate exclusion patterns
4. Test with `--check` mode

### Team Coordination

Ensure all team members use the same configuration:

1. **Commit configuration**: Include `pyproject.toml` in version control
2. **Document changes**: Note configuration changes in pull requests
3. **Validate in CI**: Run `path-comment-hook --check --all` in CI

### Review Regularly

Periodically review and update configuration:

- Remove patterns for deleted directories
- Add patterns for new file types
- Optimize patterns for performance

## Troubleshooting

### Files Not Excluded

If files aren't being excluded as expected:

```bash
# Test specific patterns
path-comment-hook --verbose src/unwanted_file.py

# Show current config
path-comment-hook show-config

# Test with different config
path-comment-hook --config test.toml --check --all
```

### Performance Issues

For large projects with many exclusions:

1. **Use specific patterns**: `src/tests/**` instead of `**/tests/**`
2. **Order matters**: Put most common patterns first
3. **Test performance**: Use `--progress` to monitor speed

### Pattern Syntax

Common pattern mistakes:

| Wrong | Right | Reason |
|-------|-------|--------|
| `tests/` | `tests/**` | Need `**` for directories |
| `*.py.bak` | `*.bak` | Extension should be at end |
| `/root/file` | `root/file` | No leading slash needed |

## Migration Guide

### From Previous Versions

If upgrading from an older version:

1. **Check new defaults**: Review default exclusions
2. **Update patterns**: Some patterns may have changed
3. **Test thoroughly**: Run in check mode first

### From Manual Configuration

If migrating from manual file exclusions:

1. **List current exclusions**: Document what you currently skip
2. **Convert to patterns**: Transform to glob patterns
3. **Test coverage**: Ensure all files are handled correctly

## Next Steps

- [File Types](file-types.md) - See what file types are supported
- [CLI Usage](cli-usage.md) - Learn command-line options
- [Examples](examples.md) - See real-world configuration examples
- [Pre-commit Setup](pre-commit-setup.md) - Automate with pre-commit
