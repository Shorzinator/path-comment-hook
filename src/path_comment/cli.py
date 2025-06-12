# src/path_comment/cli.py
"""CLI interface for path-comment-hook.

Root CLI for the *path-comment* pre-commit hook.
Calling pattern expected by pre-commit:
    path-comment-hook  [--check/-c]  <file1> <file2> ...
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console
from rich.table import Table

from .config import ConfigError, load_config
from .processor import print_processing_summary, process_files_parallel

if TYPE_CHECKING:
    from .config import Config

# Rich console for better output
console = Console()

# Main typer app
app = typer.Typer(
    help="Insert or verify a relative-path comment at the top of each file."
)

# Constants for Typer parameter defaults to avoid function calls in default

# Argument/Option factory calls are evaluated at import time here, avoiding
# ruff B008 (function calls in default argument values) inside the actual
# function signatures.

# -- Files argument
FILES_ARGUMENT = typer.Argument(
    None,
    help="Files to process. If omitted, use --all to process entire project.",
)

# -- Common options
CHECK_OPTION = typer.Option(
    False,
    "--check",
    "-c",
    help="Dry-run: only verify; exit 1 if any file would change.",
)

PROJECT_ROOT_OPTION = typer.Option(
    Path.cwd(),
    "--project-root",
    help="Root directory used to compute the relative header path.",
)

WORKERS_OPTION = typer.Option(
    None,
    "--workers",
    help="Number of worker threads for parallel processing. Defaults to CPU count.",
)

VERBOSE_OPTION = typer.Option(
    False,
    "--verbose",
    "-v",
    help="Show detailed processing information.",
)

PROGRESS_OPTION = typer.Option(
    False,
    "--progress",
    help="Show progress bar during processing.",
)

ALL_FILES_OPTION = typer.Option(
    False,
    "--all",
    help="Process all supported files under --project-root (recursively)",
)


@app.command()
def run(
    files: list[Path] = FILES_ARGUMENT,
    check: bool = CHECK_OPTION,
    project_root: Path = PROJECT_ROOT_OPTION,
    workers: int = WORKERS_OPTION,
    verbose: bool = VERBOSE_OPTION,
    show_progress: bool = PROGRESS_OPTION,
    all_files: bool = ALL_FILES_OPTION,
) -> None:
    """Process files and ensure they have the correct header."""
    # If --all specified or no files provided, discover files automatically
    if all_files or not files:
        try:
            cfg = load_config(project_root)
        except ConfigError as e:
            console.print(f"[bold red]Configuration Error:[/bold red] {e}")
            raise typer.Exit(code=1) from e

        files = _discover_files(project_root, cfg)

        if not files:
            console.print("[yellow]No eligible files found to process.[/yellow]")
            raise typer.Exit(code=0)

    # Validate provided/discovered files
    for file_path in files:
        if not file_path.exists():
            console.print(
                f"[bold red]Error:[/bold red] File '{file_path}' does not exist."
            )
            raise typer.Exit(code=1)
        if not file_path.is_file():
            console.print(f"[bold red]Error:[/bold red] '{file_path}' is not a file.")
            raise typer.Exit(code=1)

    mode = "check" if check else "fix"

    # Process files in parallel
    results = process_files_parallel(
        files=files,
        project_root=project_root,
        mode=mode,
        workers=workers,
        show_progress=show_progress,
    )

    # Print summary if verbose or if there were changes/errors
    has_changes = any(r.result.name == "CHANGED" for r in results)
    has_errors = any(r.error is not None for r in results)

    if verbose or has_errors:
        print_processing_summary(results, mode, show_details=verbose)
    elif has_changes and not check:
        # Just show simple output for changed files in fix mode
        for result in results:
            if result.result.name == "CHANGED":
                console.print(f"Updated {result.file_path}")
    elif has_changes and check:
        # Show what would be updated in check mode
        for result in results:
            if result.result.name == "CHANGED":
                console.print(f"Would update {result.file_path}")

    # Exit with error code if in check mode and there were changes or errors
    if check and (has_changes or has_errors):
        raise typer.Exit(code=1)
    elif has_errors:
        raise typer.Exit(code=1)


@app.command("show-config")
def show_config(
    project_root: Path = PROJECT_ROOT_OPTION,
) -> None:
    """Display the current path-comment-hook configuration."""
    try:
        config = load_config(project_root)
        config_dict = config.to_dict()

        console.print("\n[bold green]Path-Comment-Hook Configuration[/bold green]")
        console.print(f"[dim]Loaded from: {project_root / 'pyproject.toml'}[/dim]\n")

        # Create a nice table for display
        table = Table(
            title="Configuration Settings",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        # Add configuration rows
        table.add_row("exclude_globs", str(config_dict["exclude_globs"]))
        table.add_row(
            "custom_comment_map",
            str(config_dict["custom_comment_map"])
            if config_dict["custom_comment_map"]
            else "[dim]None[/dim]",
        )
        table.add_row("default_mode", config_dict["default_mode"])

        console.print(table)
        console.print()

    except ConfigError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=1) from e
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        raise typer.Exit(code=1) from e


def _discover_files(project_root: Path, config: Config) -> list[Path]:
    """Recursively discover files to process under *project_root*.

    The discovery respects *exclude_globs* from the configuration and also
    consults :func:`path_comment.detectors.comment_prefix` to skip binaries or
    unsupported types.
    """
    from .detectors import comment_prefix  # local import to avoid CLI startup cost

    files: list[Path] = []
    for path in project_root.rglob("*"):
        if path.is_file() and not config.should_exclude(path):
            if comment_prefix(path) is not None:  # only supported types
                files.append(path)
    return files


def main() -> None:
    """Main entry point that handles pre-commit hook behavior."""
    # If called with file arguments but no subcommand, assume 'run' command
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        # If first arg is not a known command and not a flag, assume it's a file
        # for 'run'
        if (
            not first_arg.startswith("-")
            and first_arg not in ["show-config", "run"]
            and first_arg not in ["--help", "-h", "--version"]
        ):
            # Insert 'run' command for pre-commit hook compatibility
            sys.argv.insert(1, "run")

    app()


# Convenience: python -m path_comment.cli
if __name__ == "__main__":
    main()
