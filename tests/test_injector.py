# tests/test_injector.py

from pathlib import Path

from path_comment.injector import Result, ensure_header


def test_fix_plain_python(tmp_path: Path) -> None:
    project = tmp_path
    target = tmp_path / "scripts" / "foo.py"
    target.parent.mkdir()
    # Use binary write to ensure exact line endings across platforms
    target.write_bytes(b"print('hi')\n")

    assert ensure_header(target, project, mode="fix") is Result.CHANGED
    content = target.read_text(encoding="utf-8")
    # Use splitlines to be robust against line ending differences
    lines = content.splitlines()
    assert lines[0] == "# scripts/foo.py"
    assert "print('hi')" in content
    assert ensure_header(target, project, mode="check") is Result.OK


def test_skip_binary(tmp_path: Path) -> None:
    binary = tmp_path / "img.png"
    binary.write_bytes(b"\x89PNG\r\n\x1a\n")
    assert ensure_header(binary, tmp_path, mode="check") is Result.SKIPPED


def test_skip_markdown(tmp_path: Path) -> None:
    md = tmp_path / "README.md"
    md.write_bytes(b"# Hello\n")
    assert ensure_header(md, tmp_path, mode="check") is Result.SKIPPED


def test_fix_shebang(tmp_path: Path) -> None:
    sh = tmp_path / "bin" / "foo"
    sh.parent.mkdir()
    sh.write_bytes(b"#!/usr/bin/env python\nprint('hi')\n")

    assert ensure_header(sh, tmp_path, mode="fix") is Result.CHANGED
    lines = sh.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("#!")  # shebang preserved
    assert lines[1] == "# bin/foo"  # header inserted right after
    assert "print('hi')" in sh.read_text(encoding="utf-8")


def test_fix_c_file(tmp_path: Path) -> None:
    c_file = tmp_path / "src" / "main.c"
    c_file.parent.mkdir(parents=True)
    c_file.write_bytes(b"#include <stdio.h>\nint main(){return 0;}\n")

    assert ensure_header(c_file, tmp_path, mode="fix") is Result.CHANGED
    content = c_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert lines[0] == "// src/main.c"
    assert "#include <stdio.h>" in content
