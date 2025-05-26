# src/path_comment/cli.py
"""
cli.py
======

Root CLI for the *path-comment* pre-commit hook.
Calling pattern expected by pre-commit:
    path-comment  [--check/-c]  <file1> <file2> ...
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer

from .injector import Result, ensure_header

# Typer application object (console-script points here)
app = typer.Typer(
    add_completion=False,
    help="Insert or verify a relative-path comment at the top of each file.",
)


# Root callback: runs even when no sub-command is given
@app.callback(invoke_without_command=True)
def main(  # noqa: D401 (imperative mood fine for CLI)
    files: list[Path] = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Files passed by pre-commit (or manually).",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        "-c",
        help="Dry-run: only verify; exit 1 if any file would change.",
    ),
    project_root: Path = typer.Option(
        Path.cwd(),
        "--project-root",
        help="Root directory used to compute the relative header path.",
    ),
) -> None:
    """Process each *file* and ensure it has the correct header."""
    mode = "check" if check else "fix"
    had_changes = False

    for raw in files:
        result = ensure_header(raw, project_root, mode=mode)
        if result is Result.CHANGED:
            had_changes = True
            typer.echo(f"{'Would update' if check else 'Updated'} {raw}")

    if had_changes and check:
        sys.exit(1)


# Convenience: python -m path_comment.cli
if __name__ == "__main__":
    app()
