# Security Policy

## Supported Versions

We actively support the following versions of path-comment-hook with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in path-comment-hook, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

1. **Email**: Send details to shorz2905@gmail.com
2. **Subject Line**: `[SECURITY] path-comment-hook vulnerability`
3. **GitHub Security Advisory**: Use GitHub's private security reporting feature

### What to Include

Please include the following information in your report:

- **Description**: A clear description of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Impact**: What an attacker could achieve by exploiting this vulnerability
- **Affected Versions**: Which versions of path-comment-hook are affected
- **Environment**: Operating system, Python version, installation method
- **Proof of Concept**: If possible, include a minimal proof-of-concept

### Response Timeline

We aim to respond to security reports according to the following timeline:

- **Initial Response**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix & Release**: Within 30 days (for confirmed vulnerabilities)
- **Public Disclosure**: After fix is released and users have time to update

## Security Considerations

### File System Access

path-comment-hook operates on your file system with the permissions of the user running it. Be aware that:

- The tool reads and writes files in your project directory
- It preserves file permissions and line endings
- It uses atomic writes (temporary file + rename) for safety
- It respects ignore patterns to avoid modifying sensitive files

### Input Validation

- File paths are validated and normalized
- Binary files are automatically detected and skipped
- Configuration values are validated before use
- Encoding detection includes fallback mechanisms

### Dependencies

We maintain minimal dependencies and regularly update them:

- `typer` - CLI framework
- `rich` - Terminal formatting
- `chardet` - Encoding detection
- `identify` - File type detection

### Known Limitations

- The tool processes files based on file extensions and content detection
- It relies on the `identify` library for file type detection
- Configuration is loaded from `pyproject.toml` files in the project tree

## Best Practices for Users

1. **Review Configuration**: Always review your `pyproject.toml` configuration
2. **Use Version Control**: Use git or similar VCS when running the tool
3. **Test First**: Use `--check` mode before making changes
4. **Backup Important Files**: Ensure you have backups of critical files
5. **Update Regularly**: Keep path-comment-hook updated to the latest version

## Security Updates

Security updates will be:

1. Released as soon as possible after confirmation
2. Documented in the [CHANGELOG.md](CHANGELOG.md)
3. Announced through:
   - GitHub Security Advisories
   - Release notes
   - Documentation updates

## Contact

For security-related questions or concerns that don't require private reporting:

- **GitHub Issues**: [Open an issue](https://github.com/Shorzinator/path-comment-hook/issues)
- **GitHub Discussions**: [Start a discussion](https://github.com/Shorzinator/path-comment-hook/discussions)
- **Documentation**: [Security section](https://shorzinator.github.io/path-comment-hook/troubleshooting/#security-considerations)

---

Thank you for helping keep path-comment-hook secure!
