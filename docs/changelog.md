---
description: Project changelog and version history
keywords: changelog, releases, version history, updates
---

# Changelog

All notable changes to path-comment-hook are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

--8<-- "CHANGELOG.md"

## Release Process

path-comment-hook follows semantic versioning:

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, backwards compatible

### What Constitutes a Breaking Change?

- Changes to CLI argument names or behavior
- Removal of configuration options
- Changes to default behavior that affect existing users
- API changes that break existing integrations

### Release Schedule

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Monthly or when significant features are ready
- **Major releases**: Rarely, only when necessary for architectural changes

## Getting Latest Releases

### PyPI
```bash
pip install --upgrade path-comment-hook
```

### GitHub Releases
Visit [GitHub Releases](https://github.com/Shorzinator/path-comment-hook/releases) for:
- Detailed release notes
- Binary downloads
- Source code archives

### Pre-commit
Update your `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/Shorzinator/path-comment-hook
    rev: v0.3.0  # Use latest version
    hooks:
      - id: path-comment
```

Then run:
```bash
pre-commit autoupdate
```

## Migration Guides

### Upgrading from 0.2.x to 0.3.x

Key changes in v0.3.0:
- Enhanced file handling with better encoding detection
- Improved parallel processing performance
- New configuration options

To upgrade:
1. Update your installation: `pip install --upgrade path-comment-hook`
2. Review configuration: Some default exclusions may have changed
3. Test on a branch: Run `path-comment-hook --check --all` to verify

### Upgrading from 0.1.x to 0.2.x

Key changes in v0.2.0:
- Complete rewrite with better architecture
- New CLI interface
- Configuration in `pyproject.toml`

To upgrade:
1. Update configuration from old format to `pyproject.toml`
2. Review new CLI options
3. Update pre-commit configuration if needed

## Beta Releases

Beta releases are available for testing new features:

```bash
# Install latest beta
pip install --pre path-comment-hook

# Or specific beta version
pip install path-comment-hook==0.4.0b1
```

!!! warning "Beta Releases"
    Beta releases are for testing only. Don't use in production.

## Deprecation Policy

When features are deprecated:

1. **Announcement**: Marked as deprecated in documentation
2. **Warning period**: Minimum of one minor version with warnings
3. **Removal**: Removed in next major version

Example timeline:
- v0.3.0: Feature deprecated with warnings
- v0.4.0: Feature still works but warns
- v1.0.0: Feature removed

## Contributing to Releases

To contribute to releases:

1. **Bug fixes**: Target the current release branch
2. **Features**: Target the development branch
3. **Documentation**: Can target either branch

See [Contributing Guide](contributing/development.md) for details.

## Security Updates

Security issues are addressed promptly:

- Critical: Emergency patch release
- High: Patch release within 1 week
- Medium: Include in next scheduled release

To report security issues, see our [Security Policy](https://github.com/Shorzinator/path-comment-hook/security/policy).

## Staying Updated

Stay informed about releases:

- ⭐ **Star the repository** on GitHub for updates
- 📧 **Watch releases** to get notifications
- 📰 **Follow the changelog** for detailed changes
- 🐦 **Follow updates** through GitHub Discussions

## Version Support

- **Current major version**: Full support with new features and bug fixes
- **Previous major version**: Security updates and critical bug fixes only
- **Older versions**: Community support only

Currently supported versions:
- 0.3.x: ✅ Full support
- 0.2.x: ⚠️ Security updates only
- 0.1.x: ❌ No longer supported
