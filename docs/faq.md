---
description: Frequently asked questions about path-comment-hook
keywords: FAQ, questions, troubleshooting, help
---

# Frequently Asked Questions

## General Questions

### What is path-comment-hook?

path-comment-hook is a pre-commit hook that automatically adds file path comments to the top of your source files. This helps with code navigation, especially in large codebases where you might lose track of which file you're looking at.

### Why would I want path headers in my files?

Path headers solve several common problems:

- **Lost context**: When viewing code snippets in reviews, documentation, or search results
- **Navigation**: Quickly understanding where you are in large codebases
- **Team collaboration**: New team members can orient themselves faster
- **Documentation**: Code examples are clearer with context

See [Why Path Headers?](getting-started/why-path-headers.md) for detailed benefits.

### How is this different from IDE breadcrumbs?

IDE breadcrumbs only show when you're in the IDE. Path headers are embedded in the file itself, so they're visible in:
- Code reviews (GitHub, GitLab, etc.)
- Documentation
- Search results
- Terminal editors
- Code sharing/examples

## Installation & Setup

### How do I install path-comment-hook?

Choose your preferred method:

```bash
# pip
pip install path-comment-hook

# pipx (recommended)
pipx install path-comment-hook

# Poetry
poetry add --group dev path-comment-hook
```

See [Installation](getting-started/installation.md) for detailed instructions.

### Do I need to install it if I only use pre-commit?

No! When using pre-commit, the tool is automatically installed in an isolated environment. You only need to install it directly if you want to use it from the command line.

### How do I set it up with pre-commit?

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0  # Use the latest version
    hooks:
      - id: path-comment
```

Then run `pre-commit install`.

## Usage Questions

### What file types are supported?

Currently supported:
- Python (`.py`)
- JavaScript (`.js`)
- C/C++ (`.c`, `.h`)
- Shell scripts (`.sh`, `.bash`)
- YAML (`.yml`, `.yaml`)
- TOML (`.toml`)
- Makefile
- Cython (`.pyx`)

See [File Types](user-guide/file-types.md) for the complete list.

### Can I add support for new file types?

Yes! File type support is determined by the `COMMENT_PREFIXES` mapping in the `detectors.py` module. You can:

1. Fork the repository and add the mapping
2. Submit a pull request
3. Or modify it locally for your needs

### How do I exclude certain files?

Configure exclusions in your `pyproject.toml`:

```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "tests/fixtures/**",
    "generated/**"
]
```

See [Configuration](user-guide/configuration.md) for details.

### Can I customize the header format?

Currently, headers use the standard format: `# path/to/file.py`. Custom formats aren't supported yet, but this is planned for a future release.

## Common Issues

### "Command not found" after installation

This usually means Python's scripts directory isn't in your PATH. Try:

```bash
# Use Python module syntax
python -m path_comment --help

# Or find where it was installed
pip show -f path-comment-hook
```

### Files aren't being processed

Check these common causes:

1. **File type not supported**: Use `--verbose` to see why files are skipped
2. **File excluded**: Check your `exclude_globs` configuration
3. **Binary file**: Binary files are automatically skipped
4. **Permission issues**: Ensure files are readable/writable

### Headers look wrong or missing

1. **Check configuration**: Run `path-comment-hook show-config`
2. **Verify file type**: Ensure the file type is supported
3. **Check for existing headers**: Tool detects and replaces existing headers
4. **Use verbose mode**: Run with `--verbose` for detailed output

### Performance is slow

For large projects:

1. **Reduce workers**: Use `--workers 1` or `--workers 2`
2. **Add exclusions**: Skip directories you don't need processed
3. **Process in batches**: Process specific directories instead of `--all`

```bash
# Process specific directories
path-comment-hook --all src/
path-comment-hook --all tests/
```

### Pre-commit hook fails

Common pre-commit issues:

1. **Wrong version**: Update to latest in `.pre-commit-config.yaml`
2. **Configuration error**: Check `pyproject.toml` syntax
3. **Permission issues**: Ensure files are accessible
4. **Update hooks**: Run `pre-commit autoupdate`

## Advanced Usage

### Can I use this in CI/CD?

Yes! Use check mode to verify files have headers:

```yaml
# GitHub Actions example
- name: Check path headers
  run: path-comment-hook --check --all
```

This fails (exit code 2) if files need headers.

### How do I remove all headers?

Use the delete mode:

```bash
# Check what would be removed
path-comment-hook --delete --check --all

# Remove headers
path-comment-hook --delete --all
```

### Can I run this on specific files only?

Yes! You can specify individual files or patterns:

```bash
# Specific files
path-comment-hook src/main.py src/utils.py

# Pattern matching
path-comment-hook src/**/*.py
```

### How do I handle files with shebangs?

The tool automatically handles shebangs correctly. For files starting with `#!/usr/bin/python`, the path header is added after the shebang:

```python
#!/usr/bin/env python3
# src/scripts/deploy.py

import sys
```

## Integration Questions

### Does this work with Black/isort/other formatters?

Yes! path-comment-hook is designed to work with other code formatters. Run it before other formatters in your pre-commit configuration:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
```

### Can I use this with monorepos?

Absolutely! Configure exclusions to handle multiple projects:

```toml
[tool.path-comment]
exclude_globs = [
    "*/node_modules/**",
    "*/target/**",
    "shared/docs/**"
]
```

### Does this work with Docker?

Yes! Add to your Dockerfile:

```dockerfile
FROM python:3.11-slim
RUN pip install path-comment-hook
COPY . /app
WORKDIR /app
RUN path-comment-hook --all
```

## Troubleshooting

### How do I debug issues?

Use verbose mode for detailed output:

```bash
path-comment-hook --verbose --all
```

This shows:
- Which files are being processed
- Why files are skipped
- Configuration being used
- Processing results

### Where can I get help?

1. **Documentation**: Start with this documentation
2. **GitHub Issues**: Report bugs or request features
3. **GitHub Discussions**: Ask questions and share ideas
4. **Troubleshooting Guide**: See [Troubleshooting](troubleshooting.md)

### How do I report a bug?

1. Check if it's already reported in [GitHub Issues](https://github.com/shouryamaheshwari/path-comment-hook/issues)
2. If not, create a new issue with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Output of `path-comment-hook --version`
   - Sample files (if applicable)

### Can I contribute?

Yes! We welcome contributions:

- **Bug fixes**: Submit pull requests
- **Features**: Discuss in issues first
- **Documentation**: Always appreciated
- **Testing**: Help test beta releases

See [Contributing Guide](contributing/development.md) for details.

## Migration & Compatibility

### Can I migrate from manual path comments?

Yes! The tool will detect and replace existing path comments. To clean up first:

```bash
# Remove existing headers
path-comment-hook --delete --all

# Add standardized headers
path-comment-hook --all
```

### Is this compatible with Python 2?

No, path-comment-hook requires Python 3.8 or higher. However, it can process Python 2 source files.

### Will this break my existing workflow?

The tool is designed to be minimally invasive:
- Only adds one line per file
- Preserves existing formatting
- Works with existing tools
- Can be easily removed if needed

## Future Plans

### What features are planned?

See our [roadmap](https://github.com/shouryamaheshwari/path-comment-hook/discussions) for upcoming features:

- Custom header formats
- More file type support
- IDE integrations
- Configuration presets

### How can I request a feature?

1. Check [existing discussions](https://github.com/shouryamaheshwari/path-comment-hook/discussions)
2. Create a new discussion or issue
3. Describe your use case and proposed solution

---

**Still have questions?** Check our [GitHub Discussions](https://github.com/shouryamaheshwari/path-comment-hook/discussions) or [open an issue](https://github.com/shouryamaheshwari/path-comment-hook/issues).
