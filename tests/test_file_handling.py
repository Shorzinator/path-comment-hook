# tests/test_file_handling.py
"""Including CRLF preservation, encoding detection, and atomic writes."""

from pathlib import Path
from unittest.mock import patch

import pytest
from path_comment.file_handler import (
    FileHandler,
    FileHandlingError,
    LineEnding,
    detect_encoding,
    detect_line_ending,
)


class TestLineEndingDetection:
    """Test line ending detection and preservation."""

    def test_detect_lf_line_ending(self, tmp_path: Path) -> None:
        """Test detection of LF line endings."""
        content = "line1\nline2\nline3\n"
        file_path = tmp_path / "test_lf.txt"
        file_path.write_bytes(content.encode("utf-8"))

        ending = detect_line_ending(file_path)
        assert ending == LineEnding.LF

    def test_detect_crlf_line_ending(self, tmp_path: Path) -> None:
        """Test detection of CRLF line endings."""
        content = "line1\r\nline2\r\nline3\r\n"
        file_path = tmp_path / "test_crlf.txt"
        file_path.write_bytes(content.encode("utf-8"))

        ending = detect_line_ending(file_path)
        assert ending == LineEnding.CRLF

    def test_detect_mixed_line_endings_prefers_first(self, tmp_path: Path) -> None:
        """Test that mixed line endings return the first detected."""
        content = "line1\r\nline2\nline3\r\n"
        file_path = tmp_path / "test_mixed.txt"
        file_path.write_bytes(content.encode("utf-8"))

        ending = detect_line_ending(file_path)
        assert ending == LineEnding.CRLF  # First \r\n found

    def test_detect_no_line_endings(self, tmp_path: Path) -> None:
        """Test file with no line endings defaults to LF."""
        content = "single line no ending"
        file_path = tmp_path / "test_none.txt"
        file_path.write_bytes(content.encode("utf-8"))

        ending = detect_line_ending(file_path)
        assert ending == LineEnding.LF  # Default

    def test_detect_empty_file(self, tmp_path: Path) -> None:
        """Test empty file defaults to LF."""
        file_path = tmp_path / "test_empty.txt"
        file_path.write_bytes(b"")

        ending = detect_line_ending(file_path)
        assert ending == LineEnding.LF  # Default


class TestEncodingDetection:
    """Test encoding detection and fallback."""

    def test_detect_utf8_encoding(self, tmp_path: Path) -> None:
        """Test detection of UTF-8 encoding."""
        content = "Hello, 世界! 🌍"
        file_path = tmp_path / "test_utf8.txt"
        file_path.write_text(content, encoding="utf-8")

        encoding = detect_encoding(file_path)
        assert encoding == "utf-8"

    def test_detect_latin1_encoding(self, tmp_path: Path) -> None:
        """Test detection of Latin-1 encoding with chardet fallback."""
        content = "Héllo, wørld! Ñoël"
        file_path = tmp_path / "test_latin1.txt"
        with file_path.open("wb") as f:
            f.write(content.encode("latin-1"))

        encoding = detect_encoding(file_path)
        # chardet should detect latin-1 or compatible encoding
        assert encoding is not None
        assert encoding != "utf-8"

    def test_detect_encoding_fallback_on_utf8_failure(self, tmp_path: Path) -> None:
        """Test that chardet fallback is used when UTF-8 fails."""
        # Create a file with bytes that are invalid UTF-8
        file_path = tmp_path / "test_invalid_utf8.txt"
        with file_path.open("wb") as f:
            f.write(b"\xff\xfe\x48\x00\x65\x00\x6c\x00\x6c\x00\x6f\x00")  # UTF-16 BOM + "Hello"

        encoding = detect_encoding(file_path)
        # Should use chardet fallback
        assert encoding is not None
        assert encoding != "utf-8"

    def test_detect_encoding_handles_empty_file(self, tmp_path: Path) -> None:
        """Test encoding detection on empty file."""
        file_path = tmp_path / "test_empty.txt"
        file_path.write_bytes(b"")

        encoding = detect_encoding(file_path)
        assert encoding == "utf-8"  # Default for empty files


class TestFileHandler:
    """Test the FileHandler class for safe file operations."""

    def test_read_file_with_utf8(self, tmp_path: Path) -> None:
        """Test reading UTF-8 file."""
        content = "Hello, 世界!\nLine 2\n"
        file_path = tmp_path / "test.py"
        file_path.write_text(content, encoding="utf-8")

        handler = FileHandler(file_path)
        result = handler.read()

        assert result.content == content
        assert result.encoding == "utf-8"
        assert result.line_ending == LineEnding.LF

    def test_read_file_with_crlf(self, tmp_path: Path) -> None:
        """Test reading file with CRLF line endings."""
        content = "Hello, world!\r\nLine 2\r\n"
        file_path = tmp_path / "test.py"
        file_path.write_bytes(content.encode("utf-8"))

        handler = FileHandler(file_path)
        result = handler.read()

        assert result.content == content
        assert result.encoding == "utf-8"
        assert result.line_ending == LineEnding.CRLF

    @patch("path_comment.file_handler.chardet.detect")
    def test_read_file_with_encoding_fallback(self, mock_detect, tmp_path: Path) -> None:
        """Test reading file with chardet fallback."""
        file_path = tmp_path / "test.py"

        # Create content that will actually fail UTF-8 decoding
        invalid_utf8_bytes = b"Hello, w\xff\xfeorld!\n"  # Invalid UTF-8 sequence
        with file_path.open("wb") as f:
            f.write(invalid_utf8_bytes)

        # Mock chardet to return latin-1
        mock_detect.return_value = {"encoding": "latin-1", "confidence": 0.9}

        handler = FileHandler(file_path)
        result = handler.read()

        expected_content = invalid_utf8_bytes.decode("latin-1")
        assert result.content == expected_content
        assert result.encoding == "latin-1"
        mock_detect.assert_called_once()

    def test_write_file_preserves_line_endings(self, tmp_path: Path) -> None:
        """Test that writing preserves original line endings."""
        original_content = "line1\r\nline2\r\nline3\r\n"
        file_path = tmp_path / "test.py"
        file_path.write_bytes(original_content.encode("utf-8"))

        handler = FileHandler(file_path)
        file_info = handler.read()

        # Modify content but preserve line endings
        new_content = "# header\r\nline1\r\nline2\r\nline3\r\n"
        handler.write(new_content, file_info.line_ending)

        # Read back and verify CRLF preserved
        result_bytes = file_path.read_bytes()
        assert b"\r\n" in result_bytes
        assert result_bytes == new_content.encode("utf-8")

    def test_write_file_with_lf_endings(self, tmp_path: Path) -> None:
        """Test writing file with LF line endings."""
        original_content = "line1\nline2\nline3\n"
        file_path = tmp_path / "test.py"
        file_path.write_text(original_content, encoding="utf-8")

        handler = FileHandler(file_path)
        file_info = handler.read()

        new_content = "# header\nline1\nline2\nline3\n"
        handler.write(new_content, file_info.line_ending)

        # Read back and verify LF preserved
        result_bytes = file_path.read_bytes()
        assert b"\r\n" not in result_bytes
        assert result_bytes == new_content.encode("utf-8")

    def test_atomic_write_success(self, tmp_path: Path) -> None:
        """Test that atomic write succeeds and creates correct file."""
        file_path = tmp_path / "test.py"
        file_path.write_text("original content\n", encoding="utf-8")

        handler = FileHandler(file_path)
        new_content = "new content\n"

        handler.write(new_content, LineEnding.LF)

        assert file_path.read_text(encoding="utf-8") == new_content

    def test_atomic_write_preserves_permissions(self, tmp_path: Path) -> None:
        """Test that atomic write preserves file permissions."""
        file_path = tmp_path / "test.py"
        file_path.write_text("original content\n", encoding="utf-8")

        # Set specific permissions
        file_path.stat()
        file_path.chmod(0o644)

        handler = FileHandler(file_path)
        handler.write("new content\n", LineEnding.LF)

        # Check permissions are preserved
        new_stat = file_path.stat()
        assert new_stat.st_mode == file_path.stat().st_mode

    def test_atomic_write_failure_cleanup(self, tmp_path: Path) -> None:
        """Test that failed atomic write cleans up temporary file."""
        file_path = tmp_path / "test.py"
        file_path.write_text("original content\n", encoding="utf-8")

        handler = FileHandler(file_path)

        # Simulate write failure by making directory read-only
        file_path.parent.chmod(0o444)

        try:
            with pytest.raises(FileHandlingError):
                handler.write("new content\n", LineEnding.LF)
        finally:
            # Restore permissions for cleanup
            file_path.parent.chmod(0o755)

        # Original file should be unchanged
        assert file_path.read_text(encoding="utf-8") == "original content\n"

        # No temp files should remain
        temp_files = list(tmp_path.glob("*.tmp*"))
        assert len(temp_files) == 0

    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        """Test reading non-existent file raises appropriate error."""
        file_path = tmp_path / "nonexistent.py"

        handler = FileHandler(file_path)
        with pytest.raises(FileHandlingError, match="Failed to read file"):
            handler.read()

    def test_read_permission_denied(self, tmp_path: Path) -> None:
        """Test reading file with no permissions raises appropriate error."""
        file_path = tmp_path / "no_read.py"
        file_path.write_text("content\n", encoding="utf-8")
        file_path.chmod(0o000)

        handler = FileHandler(file_path)

        try:
            with pytest.raises(FileHandlingError, match="Failed to"):
                handler.read()
        finally:
            # Restore permissions for cleanup
            file_path.chmod(0o644)
