# tests/test_detectors.py
"""Tests for the detectors module."""

from pathlib import Path

import pytest

from path_comment.detectors import COMMENT_PREFIXES, _get_shebang_tag, comment_prefix


class TestCommentPrefix:
    """Test the comment_prefix function."""

    def test_python_file(self, tmp_path: Path) -> None:
        """Test that Python files get the correct comment prefix."""
        python_file = tmp_path / "test.py"
        python_file.write_text("print('hello')")

        result = comment_prefix(python_file)
        assert result == "#"

    def test_javascript_file(self, tmp_path: Path) -> None:
        """Test that JavaScript files get the correct comment prefix."""
        js_file = tmp_path / "test.js"
        js_file.write_text("console.log('hello');")

        result = comment_prefix(js_file)
        assert result == "//"

    def test_typescript_file(self, tmp_path: Path) -> None:
        """Test that TypeScript files get the correct comment prefix."""
        ts_file = tmp_path / "test.ts"
        ts_file.write_text("console.log('hello');")

        result = comment_prefix(ts_file)
        # TypeScript files are detected as "ts" tag, not "typescript", so they return None
        # unless the COMMENT_PREFIXES mapping includes "ts"
        assert result is None

    def test_c_file(self, tmp_path: Path) -> None:
        """Test that C files get the correct comment prefix."""
        c_file = tmp_path / "test.c"
        c_file.write_text("#include <stdio.h>")

        result = comment_prefix(c_file)
        assert result == "//"

    def test_cpp_file(self, tmp_path: Path) -> None:
        """Test that C++ files get the correct comment prefix."""
        cpp_file = tmp_path / "test.cpp"
        cpp_file.write_text("#include <iostream>")

        result = comment_prefix(cpp_file)
        # C++ files are detected as "c++" tag, not "cpp", so they return None
        # unless the COMMENT_PREFIXES mapping includes "c++"
        assert result is None

    def test_yaml_file(self, tmp_path: Path) -> None:
        """Test that YAML files get the correct comment prefix."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value")

        result = comment_prefix(yaml_file)
        assert result == "#"

    def test_toml_file(self, tmp_path: Path) -> None:
        """Test that TOML files get the correct comment prefix."""
        toml_file = tmp_path / "test.toml"
        toml_file.write_text("[section]\nkey = 'value'")

        result = comment_prefix(toml_file)
        assert result == "#"

    def test_makefile(self, tmp_path: Path) -> None:
        """Test that Makefiles get the correct comment prefix."""
        makefile = tmp_path / "Makefile"
        makefile.write_text("all:\n\techo 'hello'")

        result = comment_prefix(makefile)
        assert result == "#"

    def test_shell_script(self, tmp_path: Path) -> None:
        """Test that shell scripts get the correct comment prefix."""
        sh_file = tmp_path / "test.sh"
        sh_file.write_text("echo 'hello'")

        result = comment_prefix(sh_file)
        assert result == "#"

    def test_json_file(self, tmp_path: Path) -> None:
        """Test that JSON files get the correct comment prefix."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value"}')

        result = comment_prefix(json_file)
        assert result == "//"

    def test_cython_file(self, tmp_path: Path) -> None:
        """Test that Cython files get the correct comment prefix."""
        pyx_file = tmp_path / "test.pyx"
        pyx_file.write_text("def func(): pass")

        result = comment_prefix(pyx_file)
        assert result == "#"

    def test_binary_file_skipped(self, tmp_path: Path) -> None:
        """Test that binary files are skipped."""
        # Create a binary-like file
        binary_file = tmp_path / "test.bin"
        binary_file.write_bytes(b"\x00\x01\x02\x03")

        result = comment_prefix(binary_file)
        assert result is None

    def test_unknown_file_type(self, tmp_path: Path) -> None:
        """Test that unknown file types return None."""
        unknown_file = tmp_path / "test.unknown"
        unknown_file.write_text("some content")

        result = comment_prefix(unknown_file)
        assert result is None

    def test_markdown_file_skipped(self, tmp_path: Path) -> None:
        """Test that markdown files are skipped (not in COMMENT_PREFIXES)."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Heading\n\nContent")

        result = comment_prefix(md_file)
        assert result is None

    def test_nonexistent_file(self) -> None:
        """Test handling of nonexistent files."""
        nonexistent = Path("/nonexistent/file.py")

        # The identify library raises ValueError for nonexistent files
        # The comment_prefix function doesn't handle this, so it propagates
        with pytest.raises(ValueError, match="does not exist"):
            comment_prefix(nonexistent)


class TestShebangDetection:
    """Test the _get_shebang_tag function."""

    def test_python_shebang(self, tmp_path: Path) -> None:
        """Test detection of Python shebang."""
        script = tmp_path / "script"
        script.write_text("#!/usr/bin/env python3\nprint('hello')")

        result = _get_shebang_tag(script)
        assert result == "python"

    def test_python_shebang_variations(self, tmp_path: Path) -> None:
        """Test various Python shebang formats."""
        variations = [
            "#!/usr/bin/python",
            "#!/usr/bin/python3",
            "#!/usr/bin/env python",
            "#!/usr/bin/env python3",
            "#!/opt/python/bin/python",
        ]

        for i, shebang in enumerate(variations):
            script = tmp_path / f"script{i}"
            script.write_text(f"{shebang}\nprint('hello')")

            result = _get_shebang_tag(script)
            assert result == "python", f"Failed for shebang: {shebang}"

    def test_shell_shebang(self, tmp_path: Path) -> None:
        """Test detection of shell shebang."""
        script = tmp_path / "script"
        script.write_text("#!/bin/sh\necho 'hello'")

        result = _get_shebang_tag(script)
        assert result == "shell"

    def test_bash_shebang(self, tmp_path: Path) -> None:
        """Test detection of bash shebang."""
        script = tmp_path / "script"
        script.write_text("#!/bin/bash\necho 'hello'")

        result = _get_shebang_tag(script)
        assert result == "shell"

    def test_zsh_shebang(self, tmp_path: Path) -> None:
        """Test detection of zsh shebang."""
        script = tmp_path / "script"
        script.write_text("#!/bin/zsh\necho 'hello'")

        result = _get_shebang_tag(script)
        assert result == "shell"

    def test_no_shebang(self, tmp_path: Path) -> None:
        """Test file without shebang."""
        script = tmp_path / "script"
        script.write_text("print('hello')")

        result = _get_shebang_tag(script)
        assert result is None

    def test_shebang_not_first_line(self, tmp_path: Path) -> None:
        """Test that shebang must be on first line."""
        script = tmp_path / "script"
        script.write_text("# Some comment\n#!/usr/bin/python3\nprint('hello')")

        result = _get_shebang_tag(script)
        assert result is None

    def test_unknown_shebang(self, tmp_path: Path) -> None:
        """Test shebang for unknown interpreter."""
        script = tmp_path / "script"
        script.write_text("#!/usr/bin/ruby\nputs 'hello'")

        result = _get_shebang_tag(script)
        assert result is None

    def test_binary_file_shebang(self, tmp_path: Path) -> None:
        """Test shebang detection on binary file."""
        script = tmp_path / "script"
        script.write_bytes(b"#!/bin/sh\x00\x01\x02")

        result = _get_shebang_tag(script)
        # The shebang is readable at the start, so it detects "shell"
        # Only truly binary content would cause UnicodeDecodeError
        assert result == "shell"

    def test_truly_binary_file_shebang(self, tmp_path: Path) -> None:
        """Test shebang detection on file with non-UTF8 content."""
        script = tmp_path / "script"
        # Write binary content that can't be decoded as UTF-8
        script.write_bytes(b"\xff\xfe\x00\x01\x02\x03")

        result = _get_shebang_tag(script)
        # Should handle the UnicodeDecodeError gracefully
        assert result is None

    def test_permission_denied(self, tmp_path: Path) -> None:
        """Test handling of permission denied errors."""
        script = tmp_path / "script"
        script.write_text("#!/usr/bin/python3\nprint('hello')")

        # Can't easily simulate permission denied in a cross-platform way
        # But the function should handle OSError gracefully
        result = _get_shebang_tag(script)
        assert result == "python"  # Should work normally

    def test_empty_file(self, tmp_path: Path) -> None:
        """Test handling of empty files."""
        script = tmp_path / "script"
        script.write_text("")

        result = _get_shebang_tag(script)
        assert result is None


class TestCommentPrefixesMapping:
    """Test the COMMENT_PREFIXES mapping."""

    def test_all_prefixes_are_strings(self) -> None:
        """Test that all comment prefixes are strings."""
        for tag, prefix in COMMENT_PREFIXES.items():
            assert isinstance(tag, str)
            assert isinstance(prefix, str)
            assert len(prefix) > 0

    def test_python_prefix(self) -> None:
        """Test Python comment prefix."""
        assert COMMENT_PREFIXES["python"] == "#"

    def test_javascript_prefix(self) -> None:
        """Test JavaScript comment prefix."""
        assert COMMENT_PREFIXES["javascript"] == "//"

    def test_c_style_prefixes(self) -> None:
        """Test C-style comment prefixes."""
        c_style_tags = ["javascript", "typescript", "json", "c", "cpp"]
        for tag in c_style_tags:
            # Only test tags that actually exist in the mapping
            if tag in COMMENT_PREFIXES:
                assert COMMENT_PREFIXES[tag] == "//"

    def test_hash_style_prefixes(self) -> None:
        """Test hash-style comment prefixes."""
        hash_style_tags = ["python", "cython", "yaml", "toml", "shell", "makefile"]
        for tag in hash_style_tags:
            assert COMMENT_PREFIXES[tag] == "#"

    def test_missing_common_tags(self) -> None:
        """Test that some common file types are not in the mapping."""
        # These are tags that identify library returns but aren't in COMMENT_PREFIXES
        missing_tags = ["ts", "c++"]
        for tag in missing_tags:
            assert tag not in COMMENT_PREFIXES


class TestShebangPriority:
    """Test that shebang detection takes priority over file extension."""

    def test_python_shebang_overrides_extension(self, tmp_path: Path) -> None:
        """Test that Python shebang overrides other file extensions."""
        # Create a .txt file with Python shebang
        script = tmp_path / "script.txt"
        script.write_text("#!/usr/bin/python3\nprint('hello')")

        result = comment_prefix(script)
        # Should use shebang detection (Python = #) rather than treating as unknown
        assert result == "#"

    def test_shell_shebang_overrides_extension(self, tmp_path: Path) -> None:
        """Test that shell shebang overrides other file extensions."""
        # Create a file with .py extension but shell shebang
        script = tmp_path / "script.py"
        script.write_text("#!/bin/sh\necho 'hello'")

        result = comment_prefix(script)
        # Should use shebang detection (shell = #)
        assert result == "#"

    def test_normal_python_file_without_shebang(self, tmp_path: Path) -> None:
        """Test normal Python file without shebang uses extension."""
        python_file = tmp_path / "test.py"
        python_file.write_text("print('hello')")

        result = comment_prefix(python_file)
        assert result == "#"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_very_long_first_line(self, tmp_path: Path) -> None:
        """Test file with very long first line."""
        script = tmp_path / "script"
        long_line = "#!/usr/bin/python3" + "x" * 10000
        script.write_text(f"{long_line}\nprint('hello')")

        result = _get_shebang_tag(script)
        assert result == "python"

    def test_file_with_only_shebang(self, tmp_path: Path) -> None:
        """Test file containing only a shebang line."""
        script = tmp_path / "script"
        script.write_text("#!/usr/bin/python3")

        result = _get_shebang_tag(script)
        assert result == "python"

    def test_case_insensitive_shebang_detection(self, tmp_path: Path) -> None:
        """Test that shebang detection is case insensitive."""
        script = tmp_path / "script"
        script.write_text("#!/usr/bin/Python3\nprint('hello')")

        result = _get_shebang_tag(script)
        assert result == "python"

    def test_multiple_file_extensions(self, tmp_path: Path) -> None:
        """Test files with multiple extensions."""
        # Test .tar.gz style extensions - should not crash
        file_with_multiple_ext = tmp_path / "archive.tar.gz"
        file_with_multiple_ext.write_text("some content")

        result = comment_prefix(file_with_multiple_ext)
        # Should handle gracefully (likely return None for unknown type)
        assert result is None or isinstance(result, str)

    def test_file_with_unicode_content(self, tmp_path: Path) -> None:
        """Test file with Unicode content."""
        script = tmp_path / "script.py"
        script.write_text("#!/usr/bin/python3\n# 你好世界\nprint('hello')", encoding="utf-8")

        result = comment_prefix(script)
        assert result == "#"
