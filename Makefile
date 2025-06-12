.PHONY: install test lint format clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies with Poetry"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting checks"
	@echo "  format     - Format code"
	@echo "  clean      - Clean up temporary files"
	@echo "  pre-commit - Run pre-commit hooks"
	@echo "  build      - Build the package"
	@echo "  publish    - Publish to PyPI (dry-run)"

install:
	poetry install

test:
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ --cov=path_comment --cov-report=html --cov-report=term-missing

lint:
	poetry run ruff check .
	poetry run mypy src/path_comment tests

format:
	poetry run ruff format .
	poetry run ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +

pre-commit:
	poetry run pre-commit run --all-files

build:
	poetry build

publish:
	poetry publish --dry-run

# Development shortcuts
dev: install
	@echo "Development environment ready!"

check: lint test
	@echo "All checks passed!"

# Run the CLI tool
run:
	poetry run path-comment-hook --help

show-config:
	poetry run path-comment-hook show-config
