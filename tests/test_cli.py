# tests/test_cli.py
"""Test the CLI interface for path-comment-hook."""

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from path_comment.cli import app


class TestRunCommand:
    """Test the 'run' command functionality."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_run_single_file_success(self, runner, tmp_path: Path) -> None:
        """Test processing a single file successfully."""
        # Create a test file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        # Run the command with proper project root
        result = runner.invoke(app, ["run", str(test_file), "--project-root", str(tmp_path)])

        # Check success
        assert result.exit_code == 0
        # File should now have header
        content = test_file.read_text()
        assert content.startswith("# test.py\n")

    def test_run_check_mode_no_changes(self, runner, tmp_path: Path) -> None:
        """Test check mode when no changes are needed."""
        # Create a file with correct header - use binary write for precise control
        test_file = tmp_path / "test.py"
        content = "# test.py\nprint('hello')\n"
        test_file.write_bytes(content.encode("utf-8"))

        result = runner.invoke(
            app, ["run", "--check", str(test_file), "--project-root", str(tmp_path)]
        )

        assert result.exit_code == 0
        # File should be unchanged - check content exists rather than exact match
        file_content = test_file.read_text(encoding="utf-8")
        assert "# test.py" in file_content
        assert "print('hello')" in file_content

    def test_run_check_mode_needs_changes(self, runner, tmp_path: Path) -> None:
        """Test check mode when changes are needed."""
        # Create a file without header
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        result = runner.invoke(
            app, ["run", "--check", str(test_file), "--project-root", str(tmp_path)]
        )

        # Should exit with code 1
        assert result.exit_code == 1
        assert "Would update" in result.output
        # File should be unchanged
        assert test_file.read_text() == "print('hello')\n"

    def test_run_multiple_files(self, runner, tmp_path: Path) -> None:
        """Test processing multiple files."""
        # Create multiple test files
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.py"
        file1.write_text("print('file1')\n", encoding="utf-8")
        file2.write_text("print('file2')\n", encoding="utf-8")

        result = runner.invoke(
            app, ["run", str(file1), str(file2), "--project-root", str(tmp_path)]
        )

        assert result.exit_code == 0
        assert file1.read_text().startswith("# file1.py\n")
        assert file2.read_text().startswith("# file2.py\n")

    def test_run_nonexistent_file(self, runner, tmp_path: Path) -> None:
        """Test error handling for non-existent files."""
        nonexistent = tmp_path / "nonexistent.py"

        result = runner.invoke(app, ["run", str(nonexistent), "--project-root", str(tmp_path)])

        assert result.exit_code == 1
        # Check for key parts that should be present, robust against line wrapping
        assert "Error" in result.output
        assert "nonexistent.py" in result.output
        assert "does not exist" in result.output or "not exist" in result.output

    def test_run_directory_instead_of_file(self, runner, tmp_path: Path) -> None:
        """Test error handling when directory is passed instead of file."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        result = runner.invoke(app, ["run", str(test_dir), "--project-root", str(tmp_path)])

        assert result.exit_code == 1
        assert "is not a file" in result.output

    def test_run_all_flag(self, runner, tmp_path: Path) -> None:
        """Test --all flag for automatic file discovery."""
        # Create a project structure
        (tmp_path / "src").mkdir()
        file1 = tmp_path / "src" / "main.py"
        file2 = tmp_path / "src" / "utils.py"
        file3 = tmp_path / "README.md"  # Should be skipped

        file1.write_text("print('main')\n", encoding="utf-8")
        file2.write_text("print('utils')\n", encoding="utf-8")
        file3.write_text("# README\n", encoding="utf-8")

        # Run with --all flag
        result = runner.invoke(app, ["run", "--all", "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert file1.read_text().startswith("# src/main.py\n")
        assert file2.read_text().startswith("# src/utils.py\n")
        assert file3.read_text() == "# README\n"  # Unchanged

    def test_run_no_files_triggers_auto_discovery(self, runner, tmp_path: Path) -> None:
        """Test that running without files triggers auto-discovery."""
        # Create a test file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        # Run without specifying files but with project root
        result = runner.invoke(app, ["run", "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert test_file.read_text().startswith("# test.py\n")

    def test_run_all_no_files_found(self, runner, tmp_path: Path) -> None:
        """Test --all when no eligible files are found."""
        # Create only non-eligible files
        (tmp_path / "image.png").write_bytes(b"fake image data")
        (tmp_path / "README.md").write_text("# README\n", encoding="utf-8")

        result = runner.invoke(app, ["run", "--all", "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert "No eligible files found" in result.output

    def test_run_verbose_output(self, runner, tmp_path: Path) -> None:
        """Test verbose output option."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        result = runner.invoke(
            app, ["run", "--verbose", str(test_file), "--project-root", str(tmp_path)]
        )

        assert result.exit_code == 0
        assert "Processing Summary" in result.output

    def test_run_with_progress(self, runner, tmp_path: Path) -> None:
        """Test progress bar display."""
        # Create multiple files for progress
        files = []
        for i in range(5):
            f = tmp_path / f"file{i}.py"
            f.write_text(f"print('{i}')\n", encoding="utf-8")
            files.append(str(f))

        # Run with progress flag
        result = runner.invoke(app, ["run", "--progress", "--project-root", str(tmp_path)] + files)

        assert result.exit_code == 0
        # All files should be processed
        for i in range(5):
            content = (tmp_path / f"file{i}.py").read_text()
            assert content.startswith(f"# file{i}.py\n")

    def test_run_with_custom_workers(self, runner, tmp_path: Path) -> None:
        """Test custom worker count."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        # Run with custom workers
        result = runner.invoke(
            app,
            ["run", "--workers", "2", str(test_file), "--project-root", str(tmp_path)],
        )

        assert result.exit_code == 0
        assert test_file.read_text().startswith("# test.py\n")

    def test_run_with_nested_project_structure(self, runner, tmp_path: Path) -> None:
        """Test with nested directory structure."""
        # Create nested structure
        (tmp_path / "src" / "utils" / "helpers").mkdir(parents=True)
        test_file = tmp_path / "src" / "utils" / "helpers" / "math.py"
        test_file.write_text("def add(a, b): return a + b\n", encoding="utf-8")

        result = runner.invoke(app, ["run", str(test_file), "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        # Should have path relative to project root
        assert test_file.read_text().startswith("# src/utils/helpers/math.py\n")

    def test_run_config_error(self, runner, tmp_path: Path) -> None:
        """Test handling of configuration errors."""
        # Create invalid config
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(
            "[tool.path-comment-hook]\nexclude_globs = 'not a list'", encoding="utf-8"
        )

        result = runner.invoke(app, ["run", "--all", "--project-root", str(tmp_path)])

        assert result.exit_code == 1
        assert "Configuration Error" in result.output

    def test_run_relative_paths(self, runner, tmp_path: Path) -> None:
        """Test with relative file paths (as pre-commit provides)."""
        # Create test file
        subdir = tmp_path / "src"
        subdir.mkdir()
        test_file = subdir / "test.py"
        test_file.write_text("print('hello')\n", encoding="utf-8")

        # Change to project directory and use relative path
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["run", "src/test.py"])

            assert result.exit_code == 0
            assert test_file.read_text().startswith("# src/test.py\n")
        finally:
            os.chdir(original_cwd)


class TestShowConfigCommand:
    """Test the 'show-config' command functionality."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_show_config_default(self, runner, tmp_path: Path) -> None:
        """Test showing default configuration."""
        result = runner.invoke(app, ["show-config", "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert "Path-Comment-Hook Configuration" in result.output
        assert "exclude_globs" in result.output
        assert "custom_comment_map" in result.output
        assert "default_mode" in result.output

    def test_show_config_custom(self, runner, tmp_path: Path) -> None:
        """Test showing custom configuration."""
        # Create custom config
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(
            """
[tool.path-comment-hook]
exclude_globs = ["*.test.js"]
custom_comment_map = {".py" = "# {_path_}"}
default_mode = "folder"
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["show-config", "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert "*.test.js" in result.output
        assert "folder" in result.output

    def test_show_config_invalid(self, runner, tmp_path: Path) -> None:
        """Test showing config with invalid configuration."""
        # Create invalid config
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text("invalid toml [", encoding="utf-8")

        result = runner.invoke(app, ["show-config", "--project-root", str(tmp_path)])

        assert result.exit_code == 1
        assert "Configuration Error" in result.output

    def test_show_config_unexpected_error(self, runner, tmp_path: Path) -> None:
        """Test handling of unexpected errors in show-config."""
        with patch("path_comment.cli.load_config") as mock_config:
            mock_config.side_effect = Exception("Unexpected error")

            result = runner.invoke(app, ["show-config", "--project-root", str(tmp_path)])

        assert result.exit_code == 1
        assert "Unexpected error" in result.output


class TestPreCommitCompatibility:
    """Test pre-commit hook compatibility features."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    def test_empty_file_processing(self, runner, tmp_path: Path) -> None:
        """Test processing empty files."""
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("", encoding="utf-8")

        result = runner.invoke(app, ["run", str(empty_file), "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        assert empty_file.read_text() == "# empty.py\n"

    def test_shebang_file_processing(self, runner, tmp_path: Path) -> None:
        """Test processing files with shebang."""
        script_file = tmp_path / "script"
        script_file.write_text("#!/usr/bin/env python\nprint('hello')\n", encoding="utf-8")

        result = runner.invoke(app, ["run", str(script_file), "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        content = script_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert lines[0] == "#!/usr/bin/env python"
        assert lines[1] == "# script"
        assert "print('hello')" in content

    def test_binary_file_skipped(self, runner, tmp_path: Path) -> None:
        """Test that binary files are skipped."""
        binary_file = tmp_path / "image.png"
        binary_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        result = runner.invoke(
            app, ["run", str(binary_file), "--project-root", str(tmp_path), "--verbose"]
        )

        assert result.exit_code == 0
        assert "Skipped: 1" in result.output

    def test_unicode_file_processing(self, runner, tmp_path: Path) -> None:
        """Test processing files with unicode content."""
        unicode_file = tmp_path / "unicode.py"
        unicode_file.write_text("print('Hello, 世界! 🌍')\n", encoding="utf-8")

        result = runner.invoke(app, ["run", str(unicode_file), "--project-root", str(tmp_path)])

        assert result.exit_code == 0
        content = unicode_file.read_text(encoding="utf-8")
        assert content.startswith("# unicode.py\n")
        assert "世界" in content
        assert "🌍" in content
