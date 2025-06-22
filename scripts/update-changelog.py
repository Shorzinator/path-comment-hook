#!/usr/bin/env python3
"""Changelog automation script for path-comment-hook.

Automatically updates CHANGELOG.md during the release process.
"""

import re
import sys
from datetime import datetime
from pathlib import Path


def update_changelog_for_release(version: str, changelog_path: Path = Path("CHANGELOG.md")) -> bool:
    """Update changelog for a new release.

    Args:
        version: The version being released (e.g., "0.1.0")
        changelog_path: Path to the CHANGELOG.md file

    Returns:
        True if changelog was updated successfully, False otherwise
    """
    if not changelog_path.exists():
        print(f"Changelog file not found: {changelog_path}")
        return False

    # Read current changelog
    try:
        content = changelog_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read changelog: {e}")
        return False

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Replace [Unreleased] section with version and date
    updated_content = content.replace(
        "## [Unreleased]",
        f"## [Unreleased]\n\n### Added\n- \n\n### Changed\n- \n\n"
        f"### Fixed\n- \n\n### Security\n- \n\n## [{version}] - {current_date}",
    )

    # Also update any existing upcoming version placeholder
    updated_content = re.sub(
        rf"\[{re.escape(version)}\] - \d{{4}}-\d{{2}}-XX \(Upcoming\)",
        f"[{version}] - {current_date}",
        updated_content,
    )

    # Write updated changelog
    try:
        changelog_path.write_text(updated_content, encoding="utf-8")
        print(f"Updated changelog for version {version}")
        return True
    except Exception as e:
        print(f"Failed to write changelog: {e}")
        return False


def extract_release_notes(version: str, changelog_path: Path = Path("CHANGELOG.md")) -> str:
    """Extract release notes for a specific version from changelog.

    Args:
        version: The version to extract notes for
        changelog_path: Path to the CHANGELOG.md file

    Returns:
        Release notes content for the version
    """
    if not changelog_path.exists():
        return "Release notes not available - changelog file not found"

    try:
        content = changelog_path.read_text(encoding="utf-8")
    except Exception:
        return "Release notes not available - failed to read changelog"

    # Find the version section
    version_pattern = rf"## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}"
    version_match = re.search(version_pattern, content)

    if not version_match:
        return f"Release notes not found for version {version}"

    # Extract content from this version to the next version or end
    start_pos = version_match.end()

    # Find the next version section
    next_version_pattern = r"## \[\d+\.\d+\.\d+\]"
    next_version_match = re.search(next_version_pattern, content[start_pos:])

    if next_version_match:
        end_pos = start_pos + next_version_match.start()
        notes = content[start_pos:end_pos].strip()
    else:
        # Look for Development History or other major sections
        end_patterns = [
            r"## Development History",
            r"## Release Process",
            r"## Migration Guide",
        ]

        end_pos = len(content)
        for pattern in end_patterns:
            match = re.search(pattern, content[start_pos:])
            if match:
                end_pos = start_pos + match.start()
                break

        notes = content[start_pos:end_pos].strip()

    return notes


def generate_github_release_notes(version: str) -> str:
    """Generate formatted release notes for GitHub release.

    Args:
        version: The version being released

    Returns:
        Formatted release notes
    """
    # Extract changelog content
    changelog_notes = extract_release_notes(version)

    # Create formatted release notes
    release_notes = f"""## path-comment-hook v{version}

```
    /·\\
   /│·│\\    ┌─┐┌─┐┬ ┬
  / │·│ \\   ├─┘│  ├─┤
 /  │·│  >  ┴  └─┘┴ ┴
/___│·│___\\ path-comment-hook
```

### Installation

```bash
pip install path-comment-hook=={version}
```

### Quick Start

```bash
# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Shorzinator/path-comment-hook
    rev: v{version}
    hooks:
      - id: path-comment
```

### What's Changed

{changelog_notes}

### Documentation

**Full Documentation:** https://shorzinator.github.io/path-comment-hook

### Support

- **Report Issues:** https://github.com/Shorzinator/path-comment-hook/issues
- **Discussions:** https://github.com/Shorzinator/path-comment-hook/discussions
- **Security Issues:** shorz2905@gmail.com

---

**Full Changelog:** https://github.com/Shorzinator/path-comment-hook/blob/main/CHANGELOG.md
"""

    return release_notes


def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python update-changelog.py <command> [version]")
        print("Commands:")
        print("  update <version>   - Update changelog for release")
        print("  extract <version>  - Extract release notes for version")
        print("  generate <version> - Generate GitHub release notes")
        sys.exit(1)

    command = sys.argv[1]

    if command == "update":
        if len(sys.argv) < 3:
            print("Version required for update command")
            sys.exit(1)

        version = sys.argv[2].lstrip("v")  # Remove 'v' prefix if present
        success = update_changelog_for_release(version)
        sys.exit(0 if success else 1)

    elif command == "extract":
        if len(sys.argv) < 3:
            print("Version required for extract command")
            sys.exit(1)

        version = sys.argv[2].lstrip("v")
        notes = extract_release_notes(version)
        print(notes)

    elif command == "generate":
        if len(sys.argv) < 3:
            print("Version required for generate command")
            sys.exit(1)

        version = sys.argv[2].lstrip("v")
        notes = generate_github_release_notes(version)
        print(notes)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
