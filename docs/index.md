---
description: Automatically add file path headers to your source code with path-comment-hook
keywords: pre-commit, file headers, code organization, Python
---

# path-comment-hook

**Add file path headers to your source code automatically.**

Never lose track of where you are in large codebases. This pre-commit hook automatically adds file path comments to the top of your source files, making code navigation effortless.

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Set up in 5 minutes**

    ---

    Install with pip and integrate with pre-commit in minutes.

    [:octicons-arrow-right-24: Getting started](getting-started/installation.md)

-   :material-file-tree:{ .lg .middle } **Better Code Navigation**

    ---

    Know exactly where you are in large codebases.

    [:octicons-arrow-right-24: Why path headers?](getting-started/why-path-headers.md)

-   :material-cog:{ .lg .middle } **Highly Configurable**

    ---

    Customize comment styles, exclusions, and more.

    [:octicons-arrow-right-24: Configuration](user-guide/configuration.md)

-   :material-language-python:{ .lg .middle } **Multi-Language Support**

    ---

    Works with Python, JavaScript, TypeScript, C/C++, and more.

    [:octicons-arrow-right-24: Supported languages](user-guide/file-types.md)

</div>

## Quick Example

=== "Before"

    ```python
    def calculate_tax(amount, rate):
        """Calculate tax based on amount and rate."""
        return amount * rate

    def format_currency(amount):
        """Format amount as currency string."""
        return f"${amount:.2f}"
    ```

=== "After"

    ```python
    # src/utils/tax_calculator.py

    def calculate_tax(amount, rate):
        """Calculate tax based on amount and rate."""
        return amount * rate

    def format_currency(amount):
        """Format amount as currency string."""
        return f"${amount:.2f}"
    ```

## Installation

=== "pip"

    ```bash
    pip install path-comment-hook
    ```

=== "pipx"

    ```bash
    pipx install path-comment-hook
    ```

=== "poetry"

    ```bash
    poetry add --group dev path-comment-hook
    ```

## Pre-commit Integration

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0  # Use the latest version
    hooks:
      - id: path-comment
```

## Key Features

- **🚀 Fast**: Parallel processing for large codebases
- **🔧 Configurable**: Customize comment styles and exclusions
- **🌍 Multi-language**: Support for 10+ programming languages
- **📦 Zero dependencies**: Lightweight and reliable
- **🔄 Reversible**: Easy to add or remove headers
- **🎯 Smart detection**: Handles shebangs and encoding automatically

## Quick Start

1. **Install the hook**:
   ```bash
   pip install path-comment-hook
   ```

2. **Add to pre-commit config**:
   ```yaml
   - repo: https://github.com/shouryamaheshwari/path-comment-hook
     rev: v0.3.0
     hooks:
       - id: path-comment
   ```

3. **Run on your project**:
   ```bash
   pre-commit run path-comment --all-files
   ```

That's it! Your files now have path headers for better navigation.

## What's Next?

- [🚀 Quick Start Guide](getting-started/quick-start.md) - Get up and running in 5 minutes
- [📖 User Guide](user-guide/cli-usage.md) - Learn all the commands and options
- [⚙️ Configuration](user-guide/configuration.md) - Customize for your project
- [🔧 Pre-commit Setup](user-guide/pre-commit-setup.md) - Integrate with your workflow

## Community

- [GitHub Issues](https://github.com/shouryamaheshwari/path-comment-hook/issues) - Report bugs or request features
- [GitHub Discussions](https://github.com/shouryamaheshwari/path-comment-hook/discussions) - Ask questions and share ideas
- [Contributing Guide](contributing/development.md) - Help improve the project

---

*path-comment-hook is open source and available under the MIT license.*
