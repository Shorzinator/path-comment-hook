---
description: Complete guide to path-comment-hook command-line interface
keywords: CLI, command line, options, flags, usage
---

# CLI Usage

path-comment-hook provides a powerful command-line interface for managing file path headers. This guide covers all available commands and options.

## Basic Syntax

```bash
path-comment-hook [OPTIONS] [FILES...]
```

## Core Commands

### Process Files

Add path headers to specific files:

```bash
# Single file
path-comment-hook src/main.py

# Multiple files
path-comment-hook src/main.py src/utils.py

# Using wildcards
path-comment-hook src/**/*.py
```

### Process All Files

Process all supported files in the project:

```bash
# Process entire project
path-comment-hook --all

# Process specific directory
path-comment-hook --all src/

# Process multiple directories
path-comment-hook --all src/ tests/
```

### Check Mode (Dry Run)

See what would be changed without modifying files:

```bash
# Check single file
path-comment-hook --check src/main.py

# Check all files
path-comment-hook --check --all

# Check with detailed output
path-comment-hook --check --all --verbose
```

### Delete Headers

Remove path headers from files:

```bash
# Remove from specific file
path-comment-hook --delete src/main.py

# Remove from all files
path-comment-hook --delete --all

# Check what would be removed
path-comment-hook --delete --check --all
```

## Command Options

### Core Options

| Option | Short | Description |
|--------|-------|-------------|
| `--all` | `-a` | Process all files in project/directory |
| `--check` | `-c` | Check mode - don't modify files |
| `--delete` | `-d` | Remove path headers instead of adding |
| `--verbose` | `-v` | Show detailed output |
| `--quiet` | `-q` | Suppress all output except errors |
| `--version` | | Show version information |
| `--help` | `-h` | Show help message |

### Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--workers N` | Number of parallel workers | CPU count |
| `--progress` | Show progress bar | False |
| `--config PATH` | Path to config file | `pyproject.toml` |

## Examples

### Basic Usage

```bash
# Add headers to Python files
path-comment-hook src/*.py

# Process entire src directory
path-comment-hook --all src/

# Check what would change
path-comment-hook --check --all
```

### Advanced Usage

```bash
# Process with progress bar and verbose output
path-comment-hook --all --progress --verbose

# Use specific number of workers
path-comment-hook --all --workers 4

# Remove headers with confirmation
path-comment-hook --delete --check --all
path-comment-hook --delete --all  # If previous looks good
```

### Configuration

```bash
# Use custom config file
path-comment-hook --all --config custom.toml

# Show current configuration
path-comment-hook show-config
```

## Output Format

### Standard Output

```text
Processing files...
✓ src/main.py - CHANGED
✓ src/utils.py - OK
⚠ binary_file.so - SKIPPED
✗ locked_file.py - ERROR: Permission denied
```

### Verbose Output

```text
path-comment-hook v0.3.0
Configuration loaded from: pyproject.toml
Project root: /home/user/my-project

Processing files with 4 workers...

src/main.py:
  Current header: None
  Expected header: # src/main.py
  Action: ADD
  Result: CHANGED

src/utils.py:
  Current header: # src/utils.py
  Expected header: # src/utils.py
  Action: NONE
  Result: OK
```

### Quiet Mode

In quiet mode (`--quiet`), only errors are shown:

```text
ERROR: Permission denied: locked_file.py
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - no changes needed |
| 1 | Files were modified (in fix mode) |
| 2 | Files need changes (in check mode) |
| 3 | Configuration error |
| 4 | Runtime error |

!!! tip "Pre-commit Compatibility"
    Exit code 1 indicates files were changed, which pre-commit uses to re-run hooks after modifications.

## Working with Different File Types

### Python Files

```bash
# Process all Python files
find . -name "*.py" -exec path-comment-hook {} +

# Or use built-in discovery
path-comment-hook --all
```

### JavaScript/TypeScript

```bash
# Process JS/TS files
path-comment-hook src/**/*.{js,ts,jsx,tsx}
```

### Multiple Languages

```bash
# Process common source files
path-comment-hook --all  # Automatically detects supported types
```

## Performance Optimization

### Parallel Processing

```bash
# Use all CPU cores (default)
path-comment-hook --all

# Limit workers for resource-constrained environments
path-comment-hook --all --workers 2

# Single-threaded processing
path-comment-hook --all --workers 1
```

### Large Projects

```bash
# Show progress for long-running operations
path-comment-hook --all --progress

# Process specific directories to reduce scope
path-comment-hook --all src/ --progress
```

## Integration Examples

### Git Hooks

```bash
#!/bin/bash
# pre-commit hook
path-comment-hook --all --check
if [ $? -eq 2 ]; then
    echo "Files need path headers. Run: path-comment-hook --all"
    exit 1
fi
```

### CI/CD Pipelines

```yaml
# GitHub Actions
- name: Check path headers
  run: path-comment-hook --check --all
```

### Makefile Integration

```makefile
.PHONY: format
format:
	path-comment-hook --all

.PHONY: check-format
check-format:
	path-comment-hook --check --all
```

## Configuration Commands

### Show Configuration

Display current configuration:

```bash
path-comment-hook show-config
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

## Troubleshooting

### Common Issues

**Files not being processed:**
```bash
# Check if files are supported
path-comment-hook --verbose src/unknown_file.xyz

# Check exclusion patterns
path-comment-hook show-config
```

**Performance issues:**
```bash
# Reduce worker count
path-comment-hook --all --workers 2

# Process smaller batches
path-comment-hook --all src/
path-comment-hook --all tests/
```

**Permission errors:**
```bash
# Check file permissions
ls -la problematic_file.py

# Use sudo if necessary (not recommended)
sudo path-comment-hook problematic_file.py
```

### Debug Mode

For detailed debugging information:

```bash
# Maximum verbosity
path-comment-hook --verbose --all

# Show configuration details
path-comment-hook show-config --verbose
```

## Best Practices

### Development Workflow

```bash
# 1. Check what would change
path-comment-hook --check --all

# 2. Apply changes
path-comment-hook --all

# 3. Review changes
git diff

# 4. Commit if satisfied
git add .
git commit -m "Add path headers"
```

### Team Usage

```bash
# Standardize on specific options
alias pch="path-comment-hook --all --progress"

# Include in project scripts
echo "pch" >> scripts/format.sh
```

### Pre-commit Integration

```bash
# Test before committing
pre-commit run path-comment --all-files

# Install for automatic runs
pre-commit install
```

## Migration Guide

### From Manual Headers

If you have existing manual path headers:

```bash
# Remove existing headers first
path-comment-hook --delete --all

# Add standardized headers
path-comment-hook --all
```

### Changing Format

To change header format, update configuration and reprocess:

```bash
# Update pyproject.toml configuration
# Then reprocess all files
path-comment-hook --all
```

## Next Steps

- [Pre-commit Setup](pre-commit-setup.md) - Automate with pre-commit
- [Configuration](configuration.md) - Customize behavior
- [File Types](file-types.md) - See supported languages
- [Examples](examples.md) - Real-world usage patterns
