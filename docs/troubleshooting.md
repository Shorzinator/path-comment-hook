---
description: Troubleshooting common issues with path-comment-hook
keywords: troubleshooting, issues, problems, solutions
---

# Troubleshooting

Common issues and solutions when using path-comment-hook.

## Installation Issues

### Command Not Found

**Problem**: `path-comment-hook: command not found`

**Solutions**:
1. Check if it's installed: `pip show path-comment-hook`
2. Use module syntax: `python -m path_comment`
3. Add to PATH or use full path

### Permission Errors

**Problem**: Permission denied when processing files

**Solutions**:
1. Check file permissions: `ls -la file.py`
2. Use `sudo` (not recommended)
3. Change file ownership: `chown user:group file.py`

## Processing Issues

### Files Not Being Processed

**Common causes**:
- File type not supported
- File excluded by configuration
- Binary file (automatically skipped)

**Debugging**:
```bash
path-comment-hook --verbose file.py
path-comment-hook show-config
```

### Wrong Headers

**Problem**: Headers don't look right

**Solutions**:
1. Check file type detection
2. Verify configuration
3. Check for existing headers

## Performance Issues

### Slow Processing

**Solutions**:
- Reduce workers: `--workers 2`
- Process in batches
- Add exclusion patterns

### Memory Usage

**For large files**:
- Process specific directories
- Use exclusion patterns
- Monitor system resources

## Configuration Issues

### Invalid Configuration

**Problem**: Configuration syntax errors

**Solution**: Validate TOML syntax in `pyproject.toml`

### Exclusions Not Working

**Common issues**:
- Wrong glob pattern syntax
- Patterns too broad/narrow
- Path separator issues

**Testing patterns**:
```bash
python -c "import fnmatch; print(fnmatch.fnmatch('file.py', '*.py'))"
```

## Pre-commit Issues

### Hook Fails

**Common causes**:
1. Wrong version in config
2. Configuration errors
3. File permission issues

**Solutions**:
```bash
pre-commit autoupdate
pre-commit run --all-files --verbose
```

### Slow Hook Execution

**Solutions**:
- Reduce worker count
- Add file filters
- Use cached environments

## Getting Help

1. Check documentation
2. Search GitHub issues
3. Create new issue with details
4. Join discussions

Include in bug reports:
- OS and Python version
- Command used
- Error messages
- Sample files (if relevant)
