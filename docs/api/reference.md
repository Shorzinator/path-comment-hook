---
description: Complete API reference for path-comment-hook
keywords: API, reference, functions, classes, modules
---

# API Reference

This page provides comprehensive API documentation for path-comment-hook. The documentation is automatically generated from the source code docstrings.

## Modules Overview

The path-comment-hook package consists of several modules:

### CLI Module (`path_comment.cli`)
The command-line interface implementation using Typer.

### Configuration Module (`path_comment.config`)
Configuration loading and validation from `pyproject.toml`.

### Detectors Module (`path_comment.detectors`)
File type detection and comment prefix mapping.

### File Handler Module (`path_comment.file_handler`)
Safe file operations with encoding detection and atomic writes.

### Injector Module (`path_comment.injector`)
Core logic for adding and removing path headers.

### Processor Module (`path_comment.processor`)
Parallel processing and statistics collection.

!!! note "API Documentation"
    Detailed API documentation will be available when mkdocstrings is properly configured. For now, please refer to the source code docstrings.

## Usage Examples

### Programmatic Usage

You can use path-comment-hook programmatically in your Python code:

```python
from path_comment.config import load_config
from path_comment.processor import process_files_parallel
from pathlib import Path

# Load configuration
config = load_config()

# Process files
files = [Path("src/main.py"), Path("src/utils.py")]
project_root = Path(".")

results = process_files_parallel(
    files=files,
    project_root=project_root,
    mode="fix",
    workers=4
)

# Check results
for result in results:
    print(f"{result.file_path}: {result.result.name}")
```

### Custom File Processing

```python
from path_comment.injector import ensure_header, delete_header
from path_comment.detectors import comment_prefix
from pathlib import Path

file_path = Path("src/example.py")
project_root = Path(".")

# Check if file supports headers
prefix = comment_prefix(file_path)
if prefix:
    # Add header
    result = ensure_header(file_path, project_root, mode="fix")
    print(f"Result: {result.name}")
```

### Configuration Management

```python
from path_comment.config import Config, load_config

# Load default configuration
config = load_config()

# Create custom configuration
custom_config = Config(
    exclude_globs=[
        "*.md",
        "tests/**",
        "docs/**"
    ]
)

# Check if file should be excluded
file_path = Path("README.md")
should_exclude = custom_config.should_exclude_file(file_path)
print(f"Exclude {file_path}: {should_exclude}")
```

### Error Handling

```python
from path_comment.processor import ProcessingError
from path_comment.file_handler import FileHandlingError

try:
    results = process_files_parallel(files, project_root)
except ProcessingError as e:
    print(f"Processing failed: {e}")
except FileHandlingError as e:
    print(f"File handling error: {e}")
```

## Type Definitions

### Result Enum

Processing results from the injector module:

- `Result.OK`: File already has correct header
- `Result.CHANGED`: Header was added or modified
- `Result.SKIPPED`: File was skipped (binary, unsupported, etc.)
- `Result.REMOVED`: Header was removed (delete operation)

### ProcessingResult

Data class containing processing outcome:

```python
@dataclass
class ProcessingResult:
    file_path: Path
    result: Result
    error: Exception | None = None
```

### LineEnding

Enum for line ending types:

- `LineEnding.LF`: Unix-style line endings (`\n`)
- `LineEnding.CRLF`: Windows-style line endings (`\r\n`)

### FileInfo

Information about a file's content and metadata:

```python
@dataclass
class FileInfo:
    content: str
    encoding: str
    line_ending: LineEnding
```

## Extension Points

### Custom Comment Prefixes

You can extend the supported file types by modifying the `COMMENT_PREFIXES` mapping in the detectors module:

```python
from path_comment.detectors import COMMENT_PREFIXES

# Add support for a new file type
COMMENT_PREFIXES["rust"] = "//"
COMMENT_PREFIXES["go"] = "//"
```

### Custom File Handlers

Implement custom file processing logic:

```python
from path_comment.file_handler import FileHandler
from path_comment.injector import Result

class CustomFileHandler(FileHandler):
    def custom_process(self, content: str) -> tuple[str, Result]:
        # Your custom processing logic
        return modified_content, Result.CHANGED
```

## Performance Considerations

### Parallel Processing

The processor module uses `ThreadPoolExecutor` for parallel file processing:

- Default worker count: `os.cpu_count()`
- Can be customized via `workers` parameter
- Progress reporting available via `show_progress` parameter

### Memory Usage

For large files:

- File content is loaded entirely into memory
- Consider processing in batches for very large projects
- Use exclusion patterns to skip unnecessary files

### File System Operations

- Atomic writes prevent data loss
- Original file permissions are preserved
- Temporary files are cleaned up automatically

## Contributing to the API

When contributing new functionality:

1. **Add docstrings**: All public functions and classes need docstrings
2. **Include type hints**: Use proper type annotations
3. **Handle errors**: Raise appropriate exceptions with clear messages
4. **Add tests**: Include unit tests for new functionality
5. **Update docs**: Regenerate API docs after changes

## See Also

- [CLI Usage](../user-guide/cli-usage.md) - Command-line interface
- [Configuration](../user-guide/configuration.md) - Configuration options
- [Contributing](../contributing/development.md) - Development guide
