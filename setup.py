"""Setup script with post-install welcome message."""

import subprocess
import sys
from pathlib import Path
from typing import Any

from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Custom install command that shows welcome message after installation."""

    def run(self) -> None:
        """Run the standard installation and then show welcome message."""
        install.run(self)
        try:
            # Try to show the welcome message
            subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from path_comment.welcome import show_welcome; show_welcome()",
                ],
                check=False,
                capture_output=True,
            )
        except Exception:
            # Fallback to simple text message if rich is not available yet
            print("\n" + "=" * 60)
            print("    /·\\")
            print("   /│·│\\    ┌─┐┌─┐┬ ┬")
            print("  / │·│ \\   ├─┘│  ├─┤")
            print(" /  │·│  >   ┴  └─┘┴ ┴")
            print("/___│·│___\\ path-comment-hook")
            print("\n🎉 Welcome to path-comment-hook! 🎉")
            print("\nThank you for installing path-comment-hook!")
            print("Add file path headers to your source code for better navigation.")
            print("\nQuick Start:")
            url = "https://shouryamaheshwari.github.io/path-comment-hook"
            print(f"• Documentation: {url}")
            print("• Run 'path-comment-welcome' for this message anytime")
            print("\nHappy coding! 🚀")
            print("=" * 60 + "\n")


# Read the pyproject.toml to get package info
def read_pyproject() -> dict[str, Any]:
    """Read basic info from pyproject.toml for fallback setup."""
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            # Fallback if no TOML library available
            return {
                "name": "path-comment-hook",
                "version": "0.1.0",
                "description": "Pre-commit hook that adds file path headers",
            }

    pyproject_path = Path(__file__).parent / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            tool_data = data.get("tool", {})
            poetry_data = tool_data.get("poetry", {})
            return dict(poetry_data)  # Ensure it's a dict
    return {}


if __name__ == "__main__":
    pyproject_data = read_pyproject()

    setup(
        name=pyproject_data.get("name", "path-comment-hook"),
        version=pyproject_data.get("version", "0.1.0"),
        description=pyproject_data.get(
            "description", "Pre-commit hook that adds file path headers"
        ),
        cmdclass={
            "install": PostInstallCommand,
        },
    )
