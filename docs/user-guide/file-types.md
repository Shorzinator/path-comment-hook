---
description: Supported file types and comment styles in path-comment-hook
keywords: file types, languages, comment styles, support
---

# Supported File Types

path-comment-hook supports multiple programming languages and file types. Each file type uses the appropriate comment syntax for that language.

## Supported Languages

### Python
- **Extensions**: `.py`, `.pyx`
- **Comment style**: `# path/to/file.py`
- **Shebang support**: ✅

```python
# src/utils/helpers.py

def helper_function():
    return "Hello, World!"
```

### JavaScript
- **Extensions**: `.js`
- **Comment style**: `// path/to/file.js`
- **Shebang support**: ✅

```javascript
// src/frontend/utils.js

function formatDate(date) {
    return date.toISOString();
}
```

### C/C++
- **Extensions**: `.c`, `.h`
- **Comment style**: `// path/to/file.c`
- **Shebang support**: ❌

```c
// src/core/memory.c

#include <stdlib.h>

void* allocate_memory(size_t size) {
    return malloc(size);
}
```

### Shell Scripts
- **Extensions**: `.sh`, `.bash`
- **Comment style**: `# path/to/file.sh`
- **Shebang support**: ✅

```bash
# scripts/deploy.sh

#!/bin/bash
set -e

echo "Starting deployment..."
```

### Configuration Files

#### YAML
- **Extensions**: `.yml`, `.yaml`
- **Comment style**: `# path/to/file.yml`

```yaml
# config/database.yml

development:
  adapter: postgresql
  database: myapp_dev
```

#### TOML
- **Extensions**: `.toml`
- **Comment style**: `# path/to/file.toml`

```toml
# pyproject.toml

[tool.path-comment]
exclude_globs = ["*.md"]
```

### Build Files

#### Makefile
- **Extensions**: `Makefile`, `makefile`
- **Comment style**: `# path/to/Makefile`

```makefile
# Makefile

.PHONY: build test

build:
	poetry build
```

## File Detection

path-comment-hook uses the [`identify`](https://github.com/pre-commit/identify) library to detect file types. This provides robust detection based on:

1. **File extensions**
2. **File names** (e.g., `Makefile`)
3. **Shebang lines** (e.g., `#!/usr/bin/python3`)

## Shebang Handling

Files with shebangs have special handling:

### Python Script with Shebang

```python
#!/usr/bin/env python3
# scripts/process_data.py

import sys

if __name__ == "__main__":
    print("Processing data...")
```

The path header is placed **after** the shebang line.

### Shell Script with Shebang

```bash
#!/bin/bash
# scripts/backup.sh

set -euo pipefail

echo "Starting backup..."
```

## Unsupported File Types

Some file types are automatically excluded:

### Binary Files
- Images (`.png`, `.jpg`, `.gif`)
- Executables (`.exe`, `.bin`)
- Archives (`.zip`, `.tar.gz`)

### Documentation
- Markdown (`.md`)
- RestructuredText (`.rst`)
- Plain text (`.txt`)

### Data Files
- JSON (`.json`)
- CSV (`.csv`)
- XML (`.xml`)

## Adding New File Types

To add support for a new file type:

1. **Check if identify supports it**:
   ```python
   from identify.identify import tags_from_path
   print(tags_from_path("example.rs"))  # ['rust']
   ```

2. **Add to COMMENT_PREFIXES**:
   ```python
   # In src/path_comment/detectors.py
   COMMENT_PREFIXES["rust"] = "//"
   ```

3. **Test the change**:
   ```bash
   path-comment-hook test.rs
   ```

### Contributing New File Types

We welcome contributions for new file types! Please:

1. Open an issue first to discuss
2. Include example files
3. Add tests for the new file type
4. Update documentation

Popular requested file types:
- Rust (`.rs`) - `//` comments
- Go (`.go`) - `//` comments
- TypeScript (`.ts`) - `//` comments
- Swift (`.swift`) - `//` comments

## File Type Examples

### Complete Examples

Here are complete examples showing how different file types look with path headers:

=== "Python"

    ```python
    # src/models/user.py

    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class User:
        name: str
        email: str
        age: Optional[int] = None
    ```

=== "JavaScript"

    ```javascript
    // src/components/Button.js

    import React from 'react';

    export function Button({ children, onClick }) {
        return (
            <button onClick={onClick}>
                {children}
            </button>
        );
    }
    ```

=== "C"

    ```c
    // src/utils/string_utils.c

    #include <string.h>
    #include <stdlib.h>

    char* string_duplicate(const char* source) {
        size_t len = strlen(source) + 1;
        char* dest = malloc(len);
        if (dest) {
            strcpy(dest, source);
        }
        return dest;
    }
    ```

=== "YAML"

    ```yaml
    # .github/workflows/ci.yml

    name: CI
    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
    ```

## Customization

### Excluding File Types

If you don't want certain supported file types to be processed:

```toml
[tool.path-comment]
exclude_globs = [
    "*.yml",      # Skip YAML files
    "*.yaml",     # Skip YAML files
    "Makefile*",  # Skip Makefiles
]
```

### Per-Directory Rules

You can have different rules for different directories:

```toml
[tool.path-comment]
exclude_globs = [
    "tests/**/*.py",     # Skip test files
    "scripts/**/*.sh",   # Skip script files
    "config/**/*.yml",   # Skip config files
]
```

## Future Support

File types being considered for future support:

- **Go** (`.go`) - `//` style comments
- **Rust** (`.rs`) - `//` style comments
- **TypeScript** (`.ts`, `.tsx`) - `//` style comments
- **Swift** (`.swift`) - `//` style comments
- **Kotlin** (`.kt`) - `//` style comments
- **PHP** (`.php`) - `//` or `#` style comments

## Troubleshooting

### File Not Processed

If a file isn't being processed:

1. **Check if it's supported**:
   ```bash
   path-comment-hook --verbose your-file.ext
   ```

2. **Check exclusion patterns**:
   ```bash
   path-comment-hook show-config
   ```

3. **Verify file type detection**:
   ```python
   from identify.identify import tags_from_path
   print(tags_from_path("your-file.ext"))
   ```

### Wrong Comment Style

If the comment style looks wrong:
- File might be detected as a different type
- Check the `identify` output
- File might have ambiguous extension

## See Also

- [Configuration](configuration.md) - Exclude file types
- [CLI Usage](cli-usage.md) - Process specific file types
