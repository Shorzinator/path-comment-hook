"""Parallel file processing for path-comment-hook.

This module provides multiprocessing capabilities using ThreadPoolExecutor
to process multiple files concurrently, improving performance for large
codebases.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, TaskID

from .injector import Result, ensure_header

console = Console()


class ProcessingError(Exception):
    """Raised when there's an error during file processing."""

    pass


@dataclass
class ProcessingResult:
    """Result of processing a single file.

    Attributes:
        file_path: Path to the processed file.
        result: The processing result (OK, CHANGED, SKIPPED).
        error: Any exception that occurred during processing, or None.
    """

    file_path: Path
    result: Result
    error: Exception | None = None


class FileProcessor:
    """Handles processing of individual files with error handling."""

    def __init__(self, project_root: Path) -> None:
        """Initialize the file processor.

        Args:
            project_root: Root directory for relative path computation.
        """
        self.project_root = project_root.resolve()

    def process_file(self, file_path: Path, mode: str = "fix") -> ProcessingResult:
        """Process a single file and return the result.

        Args:
            file_path: Path to the file to process.
            mode: Processing mode ("fix" or "check").

        Returns:
            ProcessingResult with the outcome and any errors.
        """
        try:
            result = ensure_header(file_path, self.project_root, mode=mode)
            return ProcessingResult(file_path=file_path, result=result, error=None)
        except Exception as e:
            # Log the error but don't let it break the entire processing
            return ProcessingResult(file_path=file_path, result=Result.SKIPPED, error=e)


def process_files_parallel(
    files: list[Path],
    project_root: Path,
    mode: str = "fix",
    workers: int | None = None,
    show_progress: bool = False,
) -> list[ProcessingResult]:
    """Process multiple files in parallel using ThreadPoolExecutor.

    Args:
        files: List of file paths to process.
        project_root: Root directory for relative path computation.
        mode: Processing mode ("fix" or "check").
        workers: Number of worker threads. Defaults to os.cpu_count().
        show_progress: Whether to show a progress bar.

    Returns:
        List of ProcessingResult objects in the same order as input files.

    Raises:
        ProcessingError: If there's a critical error in parallel processing setup.
    """
    if not files:
        return []

    if workers is None:
        workers = os.cpu_count() or 1

    # Ensure we don't use more workers than files
    workers = min(workers, len(files))

    processor = FileProcessor(project_root)
    results: list[ProcessingResult | None] = [None] * len(files)

    try:
        if show_progress:
            with Progress() as progress:
                task = progress.add_task("Processing files...", total=len(files))
                _process_with_progress(
                    files, processor, mode, workers, results, progress, task
                )
        else:
            _process_without_progress(files, processor, mode, workers, results)

    except Exception as e:
        raise ProcessingError(f"Failed to process files in parallel: {e}") from e

    # Filter out None results (shouldn't happen, but type safety)
    return [r for r in results if r is not None]


def _process_with_progress(
    files: list[Path],
    processor: FileProcessor,
    mode: str,
    workers: int,
    results: list[ProcessingResult | None],
    progress: Progress,
    task: TaskID,
) -> None:
    """Process files with progress bar display."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks and keep track of their index
        future_to_index = {
            executor.submit(processor.process_file, file_path, mode): i
            for i, file_path in enumerate(files)
        }

        # Collect results as they complete
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                results[index] = result
            except Exception as e:
                # This should not happen since process_file handles exceptions
                # But we include it for extra safety
                results[index] = ProcessingResult(
                    file_path=files[index], result=Result.SKIPPED, error=e
                )

            progress.advance(task)


def _process_without_progress(
    files: list[Path],
    processor: FileProcessor,
    mode: str,
    workers: int,
    results: list[ProcessingResult | None],
) -> None:
    """Process files without progress bar display."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks and keep track of their index
        future_to_index = {
            executor.submit(processor.process_file, file_path, mode): i
            for i, file_path in enumerate(files)
        }

        # Collect results as they complete
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                results[index] = result
            except Exception as e:
                # This should not happen since process_file handles exceptions
                # But we include it for extra safety
                results[index] = ProcessingResult(
                    file_path=files[index], result=Result.SKIPPED, error=e
                )


def collect_processing_statistics(results: list[ProcessingResult]) -> dict:
    """Collect statistics from processing results.

    Args:
        results: List of processing results.

    Returns:
        Dictionary with processing statistics.
    """
    stats = {"total": len(results), "ok": 0, "changed": 0, "skipped": 0, "errors": 0}

    for result in results:
        if result.result == Result.OK:
            stats["ok"] += 1
        elif result.result == Result.CHANGED:
            stats["changed"] += 1
        elif result.result == Result.SKIPPED:
            stats["skipped"] += 1

        if result.error is not None:
            stats["errors"] += 1

    return stats


def print_processing_summary(
    results: list[ProcessingResult], mode: str, show_details: bool = False
) -> None:
    """Print a summary of processing results.

    Args:
        results: List of processing results.
        mode: Processing mode that was used.
        show_details: Whether to show detailed file-by-file results.
    """
    stats = collect_processing_statistics(results)

    console.print(f"\n[bold]Processing Summary ({mode} mode)[/bold]")
    console.print(f"Total files: {stats['total']}")
    console.print(f"[green]OK (no changes needed): {stats['ok']}[/green]")
    console.print(f"[yellow]Changed: {stats['changed']}[/yellow]")
    console.print(f"[blue]Skipped: {stats['skipped']}[/blue]")

    if stats["errors"] > 0:
        console.print(f"[red]Errors: {stats['errors']}[/red]")

    if show_details:
        console.print("\n[bold]Details:[/bold]")
        for result in results:
            status_color = {
                Result.OK: "green",
                Result.CHANGED: "yellow",
                Result.SKIPPED: "blue",
            }.get(result.result, "white")

            status_text = result.result.name
            if result.error:
                status_text += f" (Error: {result.error})"

            console.print(
                f"  [{status_color}]{status_text}[/{status_color}]: {result.file_path}"
            )

    console.print()
