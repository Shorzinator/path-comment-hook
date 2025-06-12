# src/path_comment/config.py

"""
This module handles loading and validating configuration from
pyproject.toml files, providing a centralized way to manage tool
settings.
"""

from __future__ import annotations

import fnmatch
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised when there's an error in configuration loading or validation."""

    pass


@dataclass
class Config:
    """Configuration settings for path-comment-hook.

    Attributes:
        exclude_globs: List of glob patterns for files to exclude from processing.
        custom_comment_map: Mapping of file extensions to custom comment templates.
        default_mode: Default path resolution mode ('file', 'folder', or 'smart').
    """

    exclude_globs: list[str] = field(
        default_factory=lambda: ["*.min.js", "dist/*", "node_modules/*", ".git/*"]
    )
    custom_comment_map: dict[str, str] = field(default_factory=dict)
    default_mode: str = "file"

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.default_mode not in {"file", "folder", "smart"}:
            raise ConfigError(
                f"Invalid default_mode '{self.default_mode}'. "
                "Must be one of: file, folder, smart"
            )

    def should_exclude(self, file_path: Path) -> bool:
        """Check if a file should be excluded based on exclude_globs.

        Args:
            file_path: Path to check against exclusion patterns.

        Returns:
            True if the file should be excluded, False otherwise.
        """
        path_str = str(file_path)
        return any(fnmatch.fnmatch(path_str, pattern) for pattern in self.exclude_globs)

    def get_comment_prefix(self, extension: str) -> str | None:
        """Get custom comment prefix for a file extension.

        Args:
            extension: File extension (including the dot, e.g., '.py').

        Returns:
            Custom comment template if configured, None otherwise.
        """
        return self.custom_comment_map.get(extension)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary representation.

        Returns:
            Dictionary containing all configuration values.
        """
        return {
            "exclude_globs": self.exclude_globs,
            "custom_comment_map": self.custom_comment_map,
            "default_mode": self.default_mode,
        }


def load_config(project_root: Path) -> Config:
    """Load configuration from pyproject.toml in the project root.

    Args:
        project_root: Path to the project root directory.

    Returns:
        Config object with loaded or default settings.

    Raises:
        ConfigError: If there's an error parsing the configuration file.
    """
    pyproject_path = project_root / "pyproject.toml"

    if not pyproject_path.exists():
        return Config()

    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Failed to parse pyproject.toml: {e}") from e
    except OSError as e:
        raise ConfigError(f"Failed to read pyproject.toml: {e}") from e

    tool_config = data.get("tool", {}).get("path-comment-hook", {})

    # Extract and validate configuration values
    exclude_globs = tool_config.get(
        "exclude_globs", ["*.min.js", "dist/*", "node_modules/*", ".git/*"]
    )
    custom_comment_map = tool_config.get("custom_comment_map", {})
    default_mode = tool_config.get("default_mode", "file")

    # Type validation
    if not isinstance(exclude_globs, list):
        raise ConfigError("exclude_globs must be a list of strings")

    if not isinstance(custom_comment_map, dict):
        raise ConfigError(
            "custom_comment_map must be a dict mapping extensions to comment templates"
        )

    if not isinstance(default_mode, str):
        raise ConfigError("default_mode must be a string")

    try:
        return Config(
            exclude_globs=exclude_globs,
            custom_comment_map=custom_comment_map,
            default_mode=default_mode,
        )
    except ConfigError:
        # Re-raise validation errors from Config.__post_init__
        raise


def show_config(project_root: Path) -> dict[str, Any]:
    """Load and return configuration for display purposes.

    Args:
        project_root: Path to the project root directory.

    Returns:
        Dictionary representation of the current configuration.
    """
    config = load_config(project_root)
    return config.to_dict()
