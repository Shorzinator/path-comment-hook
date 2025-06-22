#!/bin/bash
# setup-dev.sh
    echo "Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
poetry run pre-commit install

# Show environment info
echo "Environment information:"
poetry env info

echo ""
echo " Setup complete!"
echo ""
echo "To use the development environment:"
echo "   • Use 'poetry run <command>' to run commands"
echo "   • Use 'make <target>' for common tasks (see 'make help')"
echo "   • Configure your IDE to use: ./.venv/bin/python"
echo ""
echo " Common commands:"
echo "   make test      - Run tests"
echo "   make lint      - Run linting"
echo "   make format    - Format code"
echo "   make check     - Run all checks"
