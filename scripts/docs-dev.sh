#!/bin/bash
# scripts/docs-dev.sh
# Development script for path-comment-hook documentation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    print_error "Poetry is not installed. Please install Poetry first."
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "docs" ]]; then
    print_error "This script must be run from the project root directory."
    exit 1
fi

# Help function
show_help() {
    echo "Documentation Development Script for path-comment-hook"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  serve         Start local development server"
    echo "  build         Build documentation site"
    echo "  clean         Clean build artifacts"
    echo "  install       Install documentation dependencies"
    echo "  check-links   Check for broken links"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 serve       # Start docs server at http://localhost:8000"
    echo "  $0 build       # Build docs to site/ directory"
    echo "  $0 clean       # Remove site/ directory"
}

# Install documentation dependencies
install_deps() {
    print_info "Installing documentation dependencies..."
    poetry install --only=docs
    print_info "Documentation dependencies installed."
}

# Start development server
serve_docs() {
    print_info "Starting documentation development server..."
    print_info "Documentation will be available at: http://localhost:8000"
    print_info "Press Ctrl+C to stop the server"
    poetry run mkdocs serve
}

# Build documentation
build_docs() {
    print_info "Building documentation..."

    # Clean previous build
    if [[ -d "site" ]]; then
        print_info "Cleaning previous build..."
        rm -rf site/
    fi

    # Build docs
    poetry run mkdocs build --clean --strict

    if [[ $? -eq 0 ]]; then
        print_info "Documentation built successfully in site/ directory"
        print_info "To preview: python -m http.server -d site 8000"
    else
        print_error "Documentation build failed!"
        exit 1
    fi
}

# Clean build artifacts
clean_docs() {
    print_info "Cleaning documentation build artifacts..."

    if [[ -d "site" ]]; then
        rm -rf site/
        print_info "Removed site/ directory"
    else
        print_info "No build artifacts to clean"
    fi
}

# Check for broken links (basic implementation)
check_links() {
    print_info "Checking documentation links..."

    if [[ ! -d "site" ]]; then
        print_warning "Documentation not built. Building first..."
        build_docs
    fi

    # Basic link checking using grep
    print_info "Scanning for potential broken links..."

    # Check for relative links that might be broken
    find site/ -name "*.html" -exec grep -l "href=\"[^http]" {} \; | while read file; do
        print_info "Found relative links in: $file"
    done

    print_info "Link check completed. Manual verification recommended."
}

# Validate mkdocs configuration
validate_config() {
    print_info "Validating MkDocs configuration..."

    if poetry run mkdocs build --quiet --strict 2>/dev/null; then
        print_info "MkDocs configuration is valid"
    else
        print_error "MkDocs configuration has errors"
        return 1
    fi
}

# Main command handling
case "${1:-serve}" in
    "serve")
        validate_config && serve_docs
        ;;
    "build")
        validate_config && build_docs
        ;;
    "clean")
        clean_docs
        ;;
    "install")
        install_deps
        ;;
    "check-links")
        check_links
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
