# tests/test_processor.py
"""Tests for the processor module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from path_comment.injector import Result
from path_comment.processor import (
    FileProcessor,
    ProcessingError,
    ProcessingResult,
    collect_processing_statistics,
    print_processing_summary,
    process_files_parallel,
)


class TestProcessingResult:
    """Test the ProcessingResult dataclass."""

    def test_processing_result_creation(self) -> None:
        """Test creating a ProcessingResult instance."""
        file_path = Path("test.py")
        result = ProcessingResult(file_path=file_path, result=Result.CHANGED, error=None)

        assert result.file_path == file_path
        assert result.result == Result.CHANGED
        assert result.error is None

    def test_processing_result_with_error(self) -> None:
        """Test ProcessingResult with error."""
        file_path = Path("test.py")
        error = ValueError("Test error")
        result = ProcessingResult(file_path=file_path, result=Result.SKIPPED, error=error)

        assert result.file_path == file_path
        assert result.result == Result.SKIPPED
        assert result.error == error

    def test_processing_result_default_error(self) -> None:
        """Test ProcessingResult default error value."""
        result = ProcessingResult(file_path=Path("test.py"), result=Result.OK)

        assert result.error is None


class TestFileProcessor:
    """Test the FileProcessor class."""

    def test_file_processor_initialization(self, tmp_path: Path) -> None:
        """Test FileProcessor initialization."""
        processor = FileProcessor(tmp_path)
        assert processor.project_root == tmp_path.resolve()

    def test_file_processor_resolves_project_root(self, tmp_path: Path) -> None:
        """Test that FileProcessor resolves project root."""
        # Create a relative path
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        os.chdir(subdir)

        # Use relative path for project root
        processor = FileProcessor(Path(".."))
        assert processor.project_root == tmp_path.resolve()

    @patch("path_comment.processor.ensure_header")
    def test_process_file_ensure_success(self, mock_ensure_header, tmp_path: Path) -> None:
        """Test successful file processing with ensure operation."""
        mock_ensure_header.return_value = Result.CHANGED

        processor = FileProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        result = processor.process_file(test_file, mode="fix", operation="ensure")

        assert result.file_path == test_file
        assert result.result == Result.CHANGED
        assert result.error is None
        mock_ensure_header.assert_called_once_with(test_file, tmp_path.resolve(), mode="fix")

    @patch("path_comment.processor.delete_header")
    def test_process_file_delete_success(self, mock_delete_header, tmp_path: Path) -> None:
        """Test successful file processing with delete operation."""
        mock_delete_header.return_value = Result.REMOVED

        processor = FileProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("# test.py\nprint('hello')")

        result = processor.process_file(test_file, mode="fix", operation="delete")

        assert result.file_path == test_file
        assert result.result == Result.REMOVED
        assert result.error is None
        mock_delete_header.assert_called_once_with(test_file, tmp_path.resolve(), mode="fix")

    @patch("path_comment.processor.ensure_header")
    def test_process_file_check_mode(self, mock_ensure_header, tmp_path: Path) -> None:
        """Test file processing in check mode."""
        mock_ensure_header.return_value = Result.OK

        processor = FileProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        result = processor.process_file(test_file, mode="check", operation="ensure")

        assert result.result == Result.OK
        mock_ensure_header.assert_called_once_with(test_file, tmp_path.resolve(), mode="check")

    @patch("path_comment.processor.ensure_header")
    def test_process_file_exception_handling(self, mock_ensure_header, tmp_path: Path) -> None:
        """Test that exceptions are caught and returned as errors."""
        test_error = ValueError("Test error")
        mock_ensure_header.side_effect = test_error

        processor = FileProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        result = processor.process_file(test_file, mode="fix", operation="ensure")

        assert result.file_path == test_file
        assert result.result == Result.SKIPPED
        assert result.error == test_error

    @patch("path_comment.processor.delete_header")
    def test_process_file_delete_exception(self, mock_delete_header, tmp_path: Path) -> None:
        """Test exception handling in delete operation."""
        test_error = PermissionError("Permission denied")
        mock_delete_header.side_effect = test_error

        processor = FileProcessor(tmp_path)
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        result = processor.process_file(test_file, mode="fix", operation="delete")

        assert result.file_path == test_file
        assert result.result == Result.SKIPPED
        assert result.error == test_error


class TestProcessFilesParallel:
    """Test the process_files_parallel function."""

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_empty_list(self, mock_processor_class, tmp_path: Path) -> None:
        """Test processing empty file list."""
        result = process_files_parallel([], tmp_path)
        assert result == []
        mock_processor_class.assert_not_called()

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_single_file(self, mock_processor_class, tmp_path: Path) -> None:
        """Test processing single file."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        expected_result = ProcessingResult(test_file, Result.CHANGED)
        mock_processor.process_file.return_value = expected_result

        result = process_files_parallel([test_file], tmp_path, mode="fix", workers=1)

        assert len(result) == 1
        assert result[0] == expected_result
        mock_processor.process_file.assert_called_once_with(test_file, "fix", "ensure")

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_multiple_files(
        self, mock_processor_class, tmp_path: Path
    ) -> None:
        """Test processing multiple files."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        files = []
        expected_results = []

        for i in range(3):
            test_file = tmp_path / f"test{i}.py"
            test_file.write_text(f"print('hello {i}')")
            files.append(test_file)
            expected_results.append(ProcessingResult(test_file, Result.CHANGED))

        mock_processor.process_file.side_effect = expected_results

        result = process_files_parallel(files, tmp_path, mode="fix", workers=2)

        assert len(result) == 3
        # Results should be in the same order as input files
        for i, res in enumerate(result):
            assert res.file_path == files[i]
            assert res.result == Result.CHANGED

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_with_progress(
        self, mock_processor_class, tmp_path: Path
    ) -> None:
        """Test processing with progress bar."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        expected_result = ProcessingResult(test_file, Result.OK)
        mock_processor.process_file.return_value = expected_result

        result = process_files_parallel([test_file], tmp_path, show_progress=True)

        assert len(result) == 1
        assert result[0] == expected_result

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_delete_operation(
        self, mock_processor_class, tmp_path: Path
    ) -> None:
        """Test processing with delete operation."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        expected_result = ProcessingResult(test_file, Result.REMOVED)
        mock_processor.process_file.return_value = expected_result

        result = process_files_parallel([test_file], tmp_path, operation="delete")

        assert len(result) == 1
        assert result[0] == expected_result

    @patch("path_comment.processor.FileProcessor")
    def test_process_files_parallel_worker_limit(
        self, mock_processor_class, tmp_path: Path
    ) -> None:
        """Test that worker count is limited by number of files."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        expected_result = ProcessingResult(test_file, Result.OK)
        mock_processor.process_file.return_value = expected_result

        # Request more workers than files
        result = process_files_parallel([test_file], tmp_path, workers=10)

        assert len(result) == 1
        assert result[0] == expected_result

    def test_process_files_parallel_default_workers(self, tmp_path: Path) -> None:
        """Test that default worker count is used when None."""
        with patch("path_comment.processor.FileProcessor") as mock_processor_class:
            mock_processor = Mock()
            mock_processor_class.return_value = mock_processor

            test_file = tmp_path / "test.py"
            test_file.write_text("print('hello')")

            expected_result = ProcessingResult(test_file, Result.OK)
            mock_processor.process_file.return_value = expected_result

            with patch.object(os, "cpu_count", return_value=4):
                result = process_files_parallel([test_file], tmp_path, workers=None)

                assert len(result) == 1
                assert result[0] == expected_result

    def test_process_files_parallel_no_cpu_count(self, tmp_path: Path) -> None:
        """Test handling when os.cpu_count() returns None."""
        with patch("path_comment.processor.FileProcessor") as mock_processor_class:
            mock_processor = Mock()
            mock_processor_class.return_value = mock_processor

            test_file = tmp_path / "test.py"
            test_file.write_text("print('hello')")

            expected_result = ProcessingResult(test_file, Result.OK)
            mock_processor.process_file.return_value = expected_result

            with patch.object(os, "cpu_count", return_value=None):
                result = process_files_parallel([test_file], tmp_path, workers=None)

                assert len(result) == 1
                assert result[0] == expected_result

    @patch("path_comment.processor.ThreadPoolExecutor")
    def test_process_files_parallel_executor_exception(
        self, mock_executor_class, tmp_path: Path
    ) -> None:
        """Test handling of executor exceptions."""
        mock_executor_class.side_effect = RuntimeError("Executor failed")

        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        with pytest.raises(ProcessingError, match="Failed to process files in parallel"):
            process_files_parallel([test_file], tmp_path)


class TestCollectProcessingStatistics:
    """Test the collect_processing_statistics function."""

    def test_collect_statistics_empty_results(self) -> None:
        """Test statistics collection with empty results."""
        stats = collect_processing_statistics([])

        expected = {
            "total": 0,
            "ok": 0,
            "changed": 0,
            "skipped": 0,
            "removed": 0,
            "errors": 0,
        }
        assert stats == expected

    def test_collect_statistics_all_result_types(self) -> None:
        """Test statistics collection with all result types."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.CHANGED),
            ProcessingResult(Path("file3.py"), Result.SKIPPED),
            ProcessingResult(Path("file4.py"), Result.REMOVED),
            ProcessingResult(Path("file5.py"), Result.OK, ValueError("error")),
        ]

        stats = collect_processing_statistics(results)

        expected = {
            "total": 5,
            "ok": 2,
            "changed": 1,
            "skipped": 1,
            "removed": 1,
            "errors": 1,  # One result had an error
        }
        assert stats == expected

    def test_collect_statistics_multiple_errors(self) -> None:
        """Test statistics collection with multiple errors."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK, ValueError("error1")),
            ProcessingResult(Path("file2.py"), Result.CHANGED, RuntimeError("error2")),
            ProcessingResult(Path("file3.py"), Result.SKIPPED, None),
        ]

        stats = collect_processing_statistics(results)

        expected = {
            "total": 3,
            "ok": 1,
            "changed": 1,
            "skipped": 1,
            "removed": 0,
            "errors": 2,  # Two results had errors
        }
        assert stats == expected

    def test_collect_statistics_only_successful(self) -> None:
        """Test statistics collection with only successful results."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.CHANGED),
            ProcessingResult(Path("file3.py"), Result.OK),
        ]

        stats = collect_processing_statistics(results)

        expected = {
            "total": 3,
            "ok": 2,
            "changed": 1,
            "skipped": 0,
            "removed": 0,
            "errors": 0,
        }
        assert stats == expected


class TestPrintProcessingSummary:
    """Test the print_processing_summary function."""

    @patch("path_comment.processor.console")
    def test_print_summary_basic(self, mock_console) -> None:
        """Test basic summary printing."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.CHANGED),
        ]

        print_processing_summary(results, "fix")

        # Verify console.print was called multiple times
        assert mock_console.print.call_count >= 5  # At least title + stats

    @patch("path_comment.processor.console")
    def test_print_summary_with_errors(self, mock_console) -> None:
        """Test summary printing with errors."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.SKIPPED, ValueError("test error")),
        ]

        print_processing_summary(results, "check")

        # Should print error count
        assert mock_console.print.call_count >= 6

    @patch("path_comment.processor.console")
    def test_print_summary_with_details(self, mock_console) -> None:
        """Test summary printing with detailed output."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.CHANGED),
            ProcessingResult(Path("file3.py"), Result.SKIPPED, ValueError("error")),
        ]

        print_processing_summary(results, "fix", show_details=True)

        # Should print more lines for details
        assert mock_console.print.call_count >= 8  # Summary + details header + file details

    @patch("path_comment.processor.console")
    def test_print_summary_all_result_types(self, mock_console) -> None:
        """Test summary with all result types."""
        results = [
            ProcessingResult(Path("file1.py"), Result.OK),
            ProcessingResult(Path("file2.py"), Result.CHANGED),
            ProcessingResult(Path("file3.py"), Result.SKIPPED),
            ProcessingResult(Path("file4.py"), Result.REMOVED),
        ]

        print_processing_summary(results, "fix", show_details=True)

        # Verify all result types are handled
        assert mock_console.print.call_count >= 9

    @patch("path_comment.processor.console")
    def test_print_summary_empty_results(self, mock_console) -> None:
        """Test summary printing with empty results."""
        print_processing_summary([], "fix")

        # Should still print basic summary
        assert mock_console.print.call_count >= 5


class TestProcessingError:
    """Test the ProcessingError exception."""

    def test_processing_error_creation(self) -> None:
        """Test creating a ProcessingError."""
        error = ProcessingError("Test message")
        assert str(error) == "Test message"

    def test_processing_error_inheritance(self) -> None:
        """Test that ProcessingError inherits from Exception."""
        error = ProcessingError("Test message")
        assert isinstance(error, Exception)


class TestIntegration:
    """Integration tests for the processor module."""

    def test_real_file_processing(self, tmp_path: Path) -> None:
        """Test actual file processing without mocks."""
        # Create test files
        python_file = tmp_path / "test.py"
        python_file.write_text("print('hello')")

        js_file = tmp_path / "test.js"
        js_file.write_text("console.log('hello');")

        files = [python_file, js_file]

        # Process files
        results = process_files_parallel(files, tmp_path, mode="check")

        assert len(results) == 2
        for result in results:
            assert isinstance(result, ProcessingResult)
            assert result.file_path in files
            assert isinstance(result.result, Result)

    def test_processor_with_different_modes(self, tmp_path: Path) -> None:
        """Test processor with different modes."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        processor = FileProcessor(tmp_path)

        # Test check mode
        result_check = processor.process_file(test_file, mode="check")
        assert isinstance(result_check, ProcessingResult)

        # Test fix mode
        result_fix = processor.process_file(test_file, mode="fix")
        assert isinstance(result_fix, ProcessingResult)

    def test_statistics_with_real_results(self, tmp_path: Path) -> None:
        """Test statistics collection with real processing results."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        results = process_files_parallel([test_file], tmp_path, mode="check")
        stats = collect_processing_statistics(results)

        assert stats["total"] == 1
        assert sum(stats[key] for key in ["ok", "changed", "skipped", "removed"]) == 1
