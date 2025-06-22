---
description: Get started with path-comment-hook in 5 minutes
keywords: quick start, tutorial, first steps, getting started
---

# Quick Start

Get path-comment-hook up and running in 5 minutes. This guide will walk you through adding path headers to your first project.

## Prerequisites

- Python 3.8+ installed
- A Git repository with source code files

## Step 1: Install path-comment-hook

Choose your preferred installation method:

=== "pip"

    ```bash
    pip install path-comment-hook
    ```

=== "pipx"

    ```bash
    pipx install path-comment-hook
    ```

=== "Poetry"

    ```bash
    poetry add --group dev path-comment-hook
    ```

## Step 2: Test the Installation

Verify the installation worked:

```bash
path-comment-hook --version
```

You should see version information displayed.

## Step 3: Try It Out

Let's add path headers to a sample file:

1. **Create a test file**:
   ```bash
   mkdir -p src/utils
   cat > src/utils/helper.py << 'EOF'
   def greet(name):
       return f"Hello, {name}!"

   def add_numbers(a, b):
       return a + b
   EOF
   ```

2. **Run path-comment-hook**:
   ```bash
   path-comment-hook src/utils/helper.py
   ```

3. **Check the result**:
   ```bash
   cat src/utils/helper.py
   ```

   You should see:
   ```python
   # src/utils/helper.py

   def greet(name):
       return f"Hello, {name}!"

   def add_numbers(a, b):
       return a + b
   ```

🎉 **Success!** The path header has been added to your file.

## Step 4: Process Multiple Files

Process all Python files in your project:

```bash
# Process all files in src/ directory
path-comment-hook --all src/

# Or process your entire project
path-comment-hook --all
```

!!! tip "Dry Run First"
    Use `--check` mode to see what would be changed without modifying files:
    ```bash
    path-comment-hook --check --all
    ```

## Step 5: Set Up Pre-commit (Recommended)

For automatic path header management, set up pre-commit:

1. **Install pre-commit** (if not already installed):
   ```bash
   pip install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`** in your project root:
   ```yaml
   repos:
     - repo: https://github.com/Shorzinator/path-comment-hook
       rev: v0.3.0  # Use the latest version
       hooks:
         - id: path-comment
   ```

3. **Install the hook**:
   ```bash
   pre-commit install
   ```

4. **Test it**:
   ```bash
   # Run on all files
   pre-commit run path-comment --all-files

   # Or make a commit to trigger automatically
   git add .
   git commit -m "Add path-comment-hook"
   ```

## Common Use Cases

### Add Headers to Existing Project

```bash
# Check what would be changed
path-comment-hook --check --all

# Apply changes
path-comment-hook --all

# Commit the changes
git add .
git commit -m "Add file path headers"
```

### Remove Headers

```bash
# Remove all path headers
path-comment-hook --delete --all

# Or check what would be removed first
path-comment-hook --delete --check --all
```

### Process Specific File Types

```bash
# Only Python files
find . -name "*.py" -exec path-comment-hook {} +

# Multiple file types
path-comment-hook src/**/*.py src/**/*.js
```

## Understanding the Output

When you run path-comment-hook, you'll see output like:

```text
Processing files...
✓ src/utils/helper.py - CHANGED
✓ src/main.py - OK (already has header)
⚠ binary_file.so - SKIPPED
```

- **CHANGED**: Header was added or updated
- **OK**: File already has the correct header
- **SKIPPED**: File was skipped (binary, unsupported type, etc.)

## Configuration (Optional)

Create a `pyproject.toml` configuration for custom behavior:

```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "tests/fixtures/*",
    "docs/*"
]
```

See the [Configuration Guide](../user-guide/configuration.md) for all options.

## Troubleshooting

### Files Not Being Processed

- Check if the file type is supported: [Supported File Types](../user-guide/file-types.md)
- Verify the file isn't excluded by default patterns
- Use `--verbose` for detailed output

### Headers Look Wrong

- Check your configuration in `pyproject.toml`
- See [Configuration Guide](../user-guide/configuration.md) for customization

### Pre-commit Issues

- Make sure you have the latest version in `.pre-commit-config.yaml`
- Run `pre-commit autoupdate` to update hooks
- Use `pre-commit run --all-files` to test

## What's Next?

Now that you have the basics working:

- **[CLI Usage](../user-guide/cli-usage.md)** - Learn all command-line options
- **[Pre-commit Setup](../user-guide/pre-commit-setup.md)** - Advanced pre-commit configuration
- **[Configuration](../user-guide/configuration.md)** - Customize for your project
- **[File Types](../user-guide/file-types.md)** - See all supported languages

## Example Project

Here's what a typical project looks like after running path-comment-hook:

```
my-project/
├── src/
│   ├── main.py              # src/main.py
│   ├── utils/
│   │   ├── helpers.py       # src/utils/helpers.py
│   │   └── constants.py     # src/utils/constants.py
│   └── api/
│       ├── routes.py        # src/api/routes.py
│       └── models.py        # src/api/models.py
└── tests/
    ├── test_main.py         # tests/test_main.py
    └── test_utils.py        # tests/test_utils.py
```

Each file now has a clear path header making navigation effortless!

## Need Help?

- [Troubleshooting Guide](../troubleshooting.md)
- [FAQ](../faq.md)
- [GitHub Issues](https://github.com/Shorzinator/path-comment-hook/issues)
