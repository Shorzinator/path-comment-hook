---
description: Development guide for contributing to path-comment-hook
keywords: development, contributing, setup, guidelines
---

# Development Guide

Guide for setting up a development environment and contributing to path-comment-hook.

## Development Setup

### Prerequisites
- Python 3.8+
- Poetry
- Git

### Installation
```bash
git clone https://github.com/shouryamaheshwari/path-comment-hook.git
cd path-comment-hook
poetry install
```

### Running Tests
```bash
make test
make test-cov  # With coverage
```

### Code Quality
```bash
make lint      # Run linting
make format    # Format code
```

## Project Structure
```
path-comment-hook/
├── src/path_comment/    # Main package
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Usage examples
└── scripts/            # Development scripts
```

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run quality checks
5. Submit pull request

## Code Standards
- Type hints required
- 90%+ test coverage
- Google-style docstrings
- Ruff formatting

## Release Process
1. Update version
2. Update changelog
3. Create release PR
4. Tag and publish
