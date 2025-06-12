# Path-Comment Hook

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A powerful pre-commit hook that automatically injects relative path comments into your source files, improving code navigation and project understanding.

## 🚀 What It Does

Path-Comment Hook automatically adds a comment at the top of your source files containing the file's relative path from your project root. This simple addition dramatically improves code readability and navigation, especially in large codebases.

### Before and After

**Before:**
```python
def calculate_tax(amount, rate):
    return amount * rate
```

**After:**
```python
# src/utils/tax_calculator.py
def calculate_tax(amount, rate):
    return amount * rate
```

**JavaScript Example:**
```javascript
// src/components/UserProfile.jsx
import React from 'react';

export function UserProfile({ user }) {
    return <div>{user.name}</div>;
}
```

## 🎯 Why Use Path-Comment Hook?

- **🧭 Enhanced Navigation**: Instantly know which file you're looking at
- **📝 Better Code Reviews**: Reviewers can quickly identify file locations
- **🔍 Improved Search**: Easier to find files when copy-pasting code
- **📚 Documentation**: Self-documenting code with built-in file references
- **🔧 IDE Integration**: Works seamlessly with any editor or IDE
- **⚡ Performance**: Parallel processing for fast execution on large codebases

## 📦 Installation

### As a Pre-commit Hook (Recommended)

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/Shorzinator/path-comment-hook
    rev: v1.0.0  # Use the latest version
    hooks:
      - id: path-comment
```

Then install the pre-commit hook:

```bash
pre-commit install
```

### Standalone Installation

```bash
pip install path-comment-hook
```

### Development Installation

```bash
git clone https://github.com/Shorzinator/path-comment-hook.git
cd path-comment-hook
pip install -e ".[dev]"
```

## 🛠️ Usage

### Pre-commit Hook (Automatic)

Once configured, the hook runs automatically on every commit:

```bash
git add .
git commit -m "Your commit message"
# Hook runs automatically and adds path comments
```

### Manual CLI Usage

#### Process specific files:
```bash
path-comment-hook src/main.py src/utils/helper.js
```

#### Check mode (dry run):
```bash
path-comment-hook --check src/
```

#### Process all files in a directory:
```bash
find src/ -name "*.py" -o -name "*.js" | xargs path-comment-hook
```

#### Show current configuration:
```bash
path-comment-hook show-config
```

### Advanced CLI Options

```bash
path-comment-hook [OPTIONS] FILES...

Options:
  -c, --check           Dry-run: only verify; exit 1 if any file would change
  --project-root PATH   Root directory for computing relative paths
  --workers INTEGER     Number of worker threads (defaults to CPU count)
  -v, --verbose         Show detailed processing information
  --progress            Show progress bar during processing
  --help               Show help message
```

## ⚙️ Configuration

Configure the hook in your `pyproject.toml`:

```toml
[tool.path-comment-hook]
# Files/directories to exclude (glob patterns)
exclude_globs = [
    "*.min.js",
    "dist/*",
    "node_modules/*",
    ".git/*",
    "*.generated.*"
]

# Custom comment templates for specific file extensions
custom_comment_map = {
    ".py" = "# {_path_}",
    ".js" = "// {_path_}",
    ".ts" = "// {_path_}",
    ".yaml" = "# {_path_}",
    ".sql" = "-- {_path_}"
}

# Default path resolution mode
default_mode = "file"  # Options: "file", "folder", "smart"
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `exclude_globs` | List of glob patterns for files to skip | `["*.min.js", "dist/*", "node_modules/*", ".git/*"]` |
| `custom_comment_map` | Custom comment templates by file extension | `{}` (uses auto-detection) |
| `default_mode` | Path resolution strategy | `"file"` |

### Path Resolution Modes

- **`file`**: Use the exact file path (default)
- **`folder`**: Use only the directory path
- **`smart`**: Automatically choose between file and folder based on context

## 🎨 Supported File Types

Path-Comment Hook automatically detects and supports:

- **Python** (`.py`) → `# comment`
- **JavaScript/TypeScript** (`.js`, `.ts`, `.jsx`, `.tsx`) → `// comment`
- **Shell Scripts** (`.sh`, `.bash`) → `# comment`
- **YAML/TOML** (`.yaml`, `.yml`, `.toml`) → `# comment`
- **C/C++** (`.c`, `.cpp`, `.h`, `.hpp`) → `// comment`
- **JSON** (`.json`) → `// comment`
- **Makefile** → `# comment`
- **Shebang Scripts** (auto-detected from `#!` line)

The tool uses the [`identify`](https://github.com/pre-commit/identify) library for robust file type detection.

## 🔧 Features

### Smart File Detection
- Automatic file type recognition using multiple heuristics
- Shebang script detection (`#!/usr/bin/env python`)
- Binary file exclusion
- Custom extension mapping

### Performance Optimized
- **Parallel Processing**: Utilizes multiple CPU cores
- **Smart Caching**: Avoids unnecessary file modifications
- **Memory Efficient**: Streams large files without loading entirely into memory

### Encoding & Safety
- **Encoding Preservation**: Maintains original file encoding (UTF-8, Latin-1, etc.)
- **Line Ending Preservation**: Keeps original line endings (LF, CRLF)
- **Atomic Operations**: Safe file modifications with rollback on errors
- **Backup Support**: Optional backup creation before modifications

### Rich CLI Experience
- **Progress Bars**: Visual feedback for large operations
- **Colored Output**: Easy-to-read status messages
- **Detailed Reporting**: Comprehensive operation summaries
- **Error Handling**: Clear error messages with context

## 📝 Examples

### Basic Python Project

```python
# src/main.py
from utils.database import connect
from utils.helpers import format_data

def main():
    conn = connect()
    data = format_data(conn.fetch_all())
    print(data)
```

### React Component

```javascript
// src/components/LoginForm.jsx
import React, { useState } from 'react';
import { validateEmail } from '../utils/validation';

export function LoginForm({ onSubmit }) {
    const [email, setEmail] = useState('');
    // ... component logic
}
```

### Configuration File

```yaml
# config/database.yaml
host: localhost
port: 5432
database: myapp
credentials:
  username: user
  password: secret
```

## 🏗️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/Shorzinator/path-comment-hook.git
cd path-comment-hook

# Install dependencies with Poetry
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run type checking
poetry run mypy src/path_comment tests

# Run linting
poetry run ruff check .
poetry run ruff format .
```

### Using Make Commands (Optional)

For convenience, you can use the provided Makefile:

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run all checks
make check

# Clean up temporary files
make clean
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=path_comment --cov-report=html

# Run specific test file
poetry run pytest tests/test_config.py

# Run with verbose output
poetry run pytest -v
```

### Project Structure

```
path-comment-hook/
├── src/path_comment/          # Main package
│   ├── __init__.py
│   ├── cli.py                 # CLI interface
│   ├── config.py              # Configuration management
│   ├── detectors.py           # File type detection
│   ├── file_handler.py        # File I/O operations
│   ├── injector.py            # Core comment injection logic
│   └── processor.py           # Parallel processing
├── tests/                     # Test suite
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass

## 📋 Requirements

- **Python**: 3.9 or higher
- **Dependencies**:
  - `typer>=0.9.0` - CLI framework
  - `rich>=13.0.0` - Rich text and beautiful formatting
  - `identify>=2.5.0` - File type identification
  - `chardet>=5.0.0` - Character encoding detection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI interface
- Uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- File detection powered by [identify](https://github.com/pre-commit/identify)
- Inspired by the pre-commit ecosystem

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Shorzinator/path-comment-hook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Shorzinator/path-comment-hook/discussions)
- **Documentation**: [Project Wiki](https://github.com/Shorzinator/path-comment-hook/wiki)

---

**Happy coding!** 🎉 Make your codebase more navigable with Path-Comment Hook.
