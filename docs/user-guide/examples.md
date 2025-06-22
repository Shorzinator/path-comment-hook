---
description: Real-world examples and usage patterns for path-comment-hook
keywords: examples, patterns, use cases, workflows
---

# Examples

Real-world examples and usage patterns for path-comment-hook in different project types and workflows.

## Django Web Application

### Project Structure
```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   └── blog/
│       ├── models.py
│       ├── views.py
│       └── urls.py
└── requirements.txt
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt",
    "*.json",
    "staticfiles/**",
    "media/**",
    "locale/**",
    "migrations/**",
    "venv/**",
    "node_modules/**"
]
```

### Result
```python
# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

## FastAPI Microservice

### Project Structure
```
api/
├── main.py
├── routers/
│   ├── auth.py
│   ├── users.py
│   └── posts.py
├── models/
│   ├── user.py
│   └── post.py
├── services/
│   ├── auth_service.py
│   └── user_service.py
└── tests/
    ├── test_auth.py
    └── test_users.py
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "tests/**",
    "alembic/**",
    "__pycache__/**",
    ".pytest_cache/**"
]
```

### Result
```python
# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Login logic here
    pass
```

## React Frontend

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Footer.js
│   │   └── Button.js
│   ├── pages/
│   │   ├── Home.js
│   │   └── About.js
│   ├── utils/
│   │   ├── api.js
│   │   └── helpers.js
│   └── App.js
├── public/
└── package.json
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.json",
    "*.lock",
    "node_modules/**",
    "build/**",
    "public/**",
    "*.test.js",
    "*.spec.js"
]
```

### Result
```javascript
// src/components/Header.js

import React from 'react';
import './Header.css';

export function Header({ title, user }) {
    return (
        <header className="app-header">
            <h1>{title}</h1>
            {user && <span>Welcome, {user.name}</span>}
        </header>
    );
}
```

## Data Science Project

### Project Structure
```
ml-project/
├── notebooks/
│   ├── exploration.ipynb
│   └── modeling.ipynb
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   └── preprocessor.py
│   ├── models/
│   │   ├── classifier.py
│   │   └── regressor.py
│   └── utils/
│       ├── metrics.py
│       └── visualization.py
├── scripts/
│   ├── train.py
│   └── evaluate.py
└── requirements.txt
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt",
    "*.json",
    "*.csv",
    "*.parquet",
    "*.pkl",
    "*.joblib",
    "notebooks/**",
    "data/**",
    "models/**",
    "outputs/**",
    ".ipynb_checkpoints/**"
]
```

### Result
```python
# src/models/classifier.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class CustomClassifier:
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state
        )
```

## Monorepo with Multiple Services

### Project Structure
```
monorepo/
├── services/
│   ├── auth-service/
│   │   ├── src/
│   │   │   ├── auth.py
│   │   │   └── models.py
│   │   └── tests/
│   ├── user-service/
│   │   ├── src/
│   │   │   ├── users.py
│   │   │   └── schemas.py
│   │   └── tests/
│   └── notification-service/
│       ├── src/
│       └── tests/
├── shared/
│   ├── utils/
│   │   ├── database.py
│   │   └── logging.py
│   └── models/
│       └── base.py
└── infra/
    ├── docker/
    └── k8s/
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.yml",
    "*.yaml",
    "*.json",
    "*/tests/**",
    "infra/**",
    "*.lock",
    "node_modules/**",
    "__pycache__/**"
]
```

### Result
```python
# shared/utils/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DatabaseConnection:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
```

## C/C++ Project

### Project Structure
```
c-project/
├── src/
│   ├── main.c
│   ├── utils/
│   │   ├── string_utils.c
│   │   └── memory_utils.c
│   └── include/
│       ├── utils.h
│       └── constants.h
├── tests/
│   ├── test_utils.c
│   └── test_main.c
├── Makefile
└── CMakeLists.txt
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt",
    "build/**",
    "cmake-build-*/**",
    "*.o",
    "*.so",
    "*.a"
]
```

### Result
```c
// src/utils/string_utils.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

char* string_concat(const char* str1, const char* str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    char* result = malloc(len1 + len2 + 1);

    if (result) {
        strcpy(result, str1);
        strcat(result, str2);
    }

    return result;
}
```

## Shell Scripts Collection

### Project Structure
```
scripts/
├── deployment/
│   ├── deploy.sh
│   └── rollback.sh
├── backup/
│   ├── database_backup.sh
│   └── files_backup.sh
├── monitoring/
│   ├── health_check.sh
│   └── log_analyzer.sh
└── utils/
    ├── setup_env.sh
    └── cleanup.sh
```

### Configuration
```toml
[tool.path-comment]
exclude_globs = [
    "*.md",
    "*.txt",
    "*.log",
    "temp/**",
    "backup_files/**"
]
```

### Result
```bash
# deployment/deploy.sh

#!/bin/bash
set -euo pipefail

# Deployment script for production environment
# Usage: ./deploy.sh <version>

VERSION=${1:-latest}
APP_NAME="myapp"
DEPLOY_DIR="/opt/${APP_NAME}"

echo "Deploying ${APP_NAME} version ${VERSION}..."
```

## Configuration Files

### Project Structure
```
configs/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── ci/
│   ├── .github/
│   │   └── workflows/
│   │       ├── ci.yml
│   │       └── deploy.yml
└── monitoring/
    ├── prometheus.yml
    └── grafana.yml
```

### Result
```yaml
# ci/.github/workflows/ci.yml

name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
```

## Pre-commit Integration Examples

### Basic Setup
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
```

### Advanced Setup with Multiple Tools
```yaml
# .pre-commit-config.yaml
repos:
  # Path headers first
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
        args: [--workers=4]

  # Then formatting
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  # Finally linting
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
```

### File-Specific Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/shouryamaheshwari/path-comment-hook
    rev: v0.3.0
    hooks:
      - id: path-comment
        files: ^src/.*\.py$  # Only process Python files in src/
        args: [--progress]
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/check-headers.yml
name: Check Path Headers

on: [push, pull_request]

jobs:
  check-headers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install path-comment-hook
        run: pip install path-comment-hook
      - name: Check path headers
        run: path-comment-hook --check --all
```

### GitLab CI
```yaml
# .gitlab-ci.yml
check-path-headers:
  stage: test
  image: python:3.11-slim
  script:
    - pip install path-comment-hook
    - path-comment-hook --check --all
  only:
    - merge_requests
    - main
```

## Makefile Integration

```makefile
# Makefile

.PHONY: format check-format

format:
	path-comment-hook --all
	black .
	isort .

check-format:
	path-comment-hook --check --all
	black --check .
	isort --check .

pre-commit: check-format
	pytest
	mypy .
```

## Docker Integration

### Adding Headers During Build
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install path-comment-hook
RUN pip install path-comment-hook

# Copy source code
COPY src/ /app/src/

# Add path headers
WORKDIR /app
RUN path-comment-hook --all

# Continue with application setup
CMD ["python", "src/main.py"]
```

### Development Workflow
```bash
# Development script
#!/bin/bash

# Add headers before building
path-comment-hook --all

# Build and run
docker build -t myapp .
docker run --rm myapp
```

## Migration Examples

### From Manual Headers
```bash
# Remove existing manual headers
path-comment-hook --delete --all

# Add standardized headers
path-comment-hook --all

# Review changes
git diff

# Commit if satisfied
git add .
git commit -m "Standardize path headers with path-comment-hook"
```

### Team Adoption
```bash
# Setup script for new team members
#!/bin/bash

echo "Setting up path-comment-hook..."

# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
path-comment-hook --all

echo "Setup complete! Path headers will be managed automatically."
```

## Troubleshooting Examples

### Debug File Processing
```bash
# Check why a file isn't processed
path-comment-hook --verbose problem_file.py

# Check configuration
path-comment-hook show-config

# Test with different config
path-comment-hook --config test.toml --check --all
```

### Performance Optimization
```bash
# For large projects, reduce workers
path-comment-hook --all --workers 2

# Process specific directories
path-comment-hook --all src/
path-comment-hook --all tests/

# Show progress for long operations
path-comment-hook --all --progress
```

These examples show how path-comment-hook adapts to different project types and development workflows, making code navigation easier across diverse environments.
