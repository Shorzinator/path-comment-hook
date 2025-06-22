# tests/test_config.py

from pathlib import Path

import pytest
from path_comment.config import Config, ConfigError, load_config


class TestConfigLoading:
    """Test configuration loading from pyproject.toml."""

    def test_load_default_config_when_no_file(self, tmp_path: Path) -> None:
        """Test that default config is loaded when no pyproject.toml exists."""
        config = load_config(tmp_path)

        assert config.exclude_globs == []  # Now defaults to empty list
        assert config.custom_comment_map == {}
        assert config.default_mode == "file"
        assert config.use_default_ignores is True  # New field

    def test_load_config_from_pyproject_toml(self, tmp_path: Path) -> None:
        """Test loading configuration from pyproject.toml."""
        pyproject_content = """
[tool.path-comment-hook]
exclude_globs = ["*.generated.js", "build/*"]
custom_comment_map = {".py" = "# {_path_}", ".js" = "// {_path_}"}
default_mode = "folder"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content, encoding="utf-8")

        config = load_config(tmp_path)

        assert config.exclude_globs == ["*.generated.js", "build/*"]
        assert config.custom_comment_map == {".py": "# {_path_}", ".js": "// {_path_}"}
        assert config.default_mode == "folder"

    def test_load_partial_config_uses_defaults(self, tmp_path: Path) -> None:
        """Test that missing config options use defaults."""
        pyproject_content = """
[tool.path-comment-hook]
exclude_globs = ["custom/*"]
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content, encoding="utf-8")

        config = load_config(tmp_path)

        assert config.exclude_globs == ["custom/*"]
        assert config.custom_comment_map == {}  # default
        assert config.default_mode == "file"  # default

    def test_load_config_with_invalid_toml(self, tmp_path: Path) -> None:
        """Test error handling for invalid TOML."""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text("invalid toml [", encoding="utf-8")

        with pytest.raises(ConfigError, match="Failed to parse pyproject.toml"):
            load_config(tmp_path)

    def test_load_config_validates_mode(self, tmp_path: Path) -> None:
        """Test validation of default_mode values."""
        pyproject_content = """
[tool.path-comment-hook]
default_mode = "invalid"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content, encoding="utf-8")

        with pytest.raises(ConfigError, match="Invalid default_mode"):
            load_config(tmp_path)

    def test_load_config_validates_exclude_globs_type(self, tmp_path: Path) -> None:
        """Test validation that exclude_globs is a list."""
        pyproject_content = """
[tool.path-comment-hook]
exclude_globs = "not a list"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content, encoding="utf-8")

        with pytest.raises(ConfigError, match="exclude_globs must be a list"):
            load_config(tmp_path)

    def test_load_config_validates_custom_comment_map_type(self, tmp_path: Path) -> None:
        """Test validation that custom_comment_map is a dict."""
        pyproject_content = """
[tool.path-comment-hook]
custom_comment_map = ["not", "a", "dict"]
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content, encoding="utf-8")

        with pytest.raises(ConfigError, match="custom_comment_map must be a dict"):
            load_config(tmp_path)


class TestConfigClass:
    """Test the Config dataclass functionality."""

    def test_config_creation_with_defaults(self) -> None:
        """Test creating Config with default values."""
        config = Config()

        assert config.exclude_globs == []  # Now defaults to empty list
        assert config.custom_comment_map == {}
        assert config.default_mode == "file"
        assert config.use_default_ignores is True  # New field

    def test_config_creation_with_custom_values(self) -> None:
        """Test creating Config with custom values."""
        config = Config(
            exclude_globs=["*.test.js"],
            custom_comment_map={".py": "# Custom {_path_}"},
            default_mode="folder",
        )

        assert config.exclude_globs == ["*.test.js"]
        assert config.custom_comment_map == {".py": "# Custom {_path_}"}
        assert config.default_mode == "folder"

    def test_config_should_exclude_file(self) -> None:
        """Test the should_exclude method."""
        config = Config(exclude_globs=["*.min.js", "dist/*"])

        assert config.should_exclude(Path("app.min.js")) is True
        assert config.should_exclude(Path("dist/bundle.js")) is True
        assert config.should_exclude(Path("src/app.js")) is False

    def test_config_should_exclude_with_default_ignores(self, tmp_path: Path) -> None:
        """Test should_exclude with default ignore patterns."""
        config = Config(use_default_ignores=True)

        # Create test paths
        cache_file = tmp_path / "__pycache__" / "test.py"
        regular_file = tmp_path / "regular.py"

        # Test with project_root for relative path matching
        assert config.should_exclude(cache_file, tmp_path) is True  # Should be ignored
        assert config.should_exclude(regular_file, tmp_path) is False  # Should not be ignored

    def test_config_get_comment_prefix(self) -> None:
        """Test getting comment prefix from custom map."""
        config = Config(custom_comment_map={".py": "# {_path_}", ".js": "// {_path_}"})

        assert config.get_comment_prefix(".py") == "# {_path_}"
        assert config.get_comment_prefix(".js") == "// {_path_}"
        assert config.get_comment_prefix(".cpp") is None

    @pytest.mark.parametrize("mode", ["file", "folder", "smart"])
    def test_config_valid_modes(self, mode: str) -> None:
        """Test all valid mode values."""
        config = Config(default_mode=mode)
        assert config.default_mode == mode

    def test_config_to_dict(self) -> None:
        """Test converting config to dictionary."""
        config = Config(
            exclude_globs=["*.test"],
            custom_comment_map={".py": "# {_path_}"},
            default_mode="folder",
        )

        result = config.to_dict()

        # Check the basic fields
        assert result["exclude_globs"] == ["*.test"]
        assert result["custom_comment_map"] == {".py": "# {_path_}"}
        assert result["default_mode"] == "folder"
        assert result["use_default_ignores"] is True

        # Check that default_ignore_patterns is present and contains patterns
        assert "default_ignore_patterns" in result
        assert isinstance(result["default_ignore_patterns"], list)
        assert len(result["default_ignore_patterns"]) > 0  # Should have patterns
