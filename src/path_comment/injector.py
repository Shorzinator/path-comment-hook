# src/path_comment/injector.py
"""
injector.py
===========

Ensure every source file starts with a comment that contains its path
relative to the project root.  Operates in two modes:
 • check → just verify, no edits
 • fix   → rewrite the file in-place if needed
"""

from __future__ import annotations

import shutil
import tempfile
from enum import Enum, auto
from pathlib import Path, PurePosixPath
from identify.identify import tags_from_path

from .detectors import comment_prefix


class Result(Enum):
    OK = auto()        # header already present
    CHANGED = auto()   # header inserted / fixed
    SKIPPED = auto()   # binary or unsupported


def _has_shebang(first_line: str) -> bool:
    return first_line.startswith("#!")  # e.g. "#!/usr/bin/env bash"


def ensure_header(
    file_path: Path,
    project_root: Path,
    mode: str = "fix",  # "check" | "fix"
) -> Result:
    """
    Ensure *file_path* contains the correct header.

    Returns a Result enum; in "check" mode we never modify files.
    """

    # ------------------------------------------------------------------ #
    # Normalize paths:                                                    #
    #  • pre-commit passes *relative* paths; tests pass absolute paths.   #
    #  • We resolve both file_path and project_root so                   #
    #    `file_path.relative_to(project_root)` is always valid.          #
    # ------------------------------------------------------------------ #
    project_root = project_root.resolve()
    if not file_path.is_absolute():
        file_path = (project_root / file_path).resolve()

    # Binary?  bail early
    if "binary" in tags_from_path(str(file_path)):
        return Result.SKIPPED

    prefix = comment_prefix(file_path)
    if prefix is None:
        return Result.SKIPPED

    rel = PurePosixPath(file_path.relative_to(project_root))
    expected_line = f"{prefix} {rel}\n"

    with file_path.open("r", encoding="utf-8") as fh:
        first_line = fh.readline()
        rest = fh.read()

    # Handle files that start with a shebang; header must go *after* it
    if _has_shebang(first_line):
        header_pos = 1
        present_header = rest.splitlines()[0] + "\n" if rest else ""
        needs_change = present_header != expected_line
    else:
        header_pos = 0
        present_header = first_line
        needs_change = present_header != expected_line

    if not needs_change:
        return Result.OK
    if mode == "check":
        return Result.CHANGED

    # --- rewrite in-place (atomic temp file swap) --------------------------
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        if header_pos == 1:               # keep shebang first
            tmp.write(first_line)
        tmp.write(expected_line)

        # write the remaining original content (skip old header if it exists)
        if header_pos == 1:
            tmp.write("\n".join(rest.splitlines()[1:]) + ("\n" if rest else ""))
        else:
            tmp.write(first_line + rest if present_header != "" else rest)

    shutil.move(tmp.name, file_path)
    return Result.CHANGED
