---
description: CI/CD integration patterns
---

# CI/CD Integration

Integrating path-comment-hook with CI/CD systems.

## GitHub Actions
```yaml
- name: Check headers
  run: path-comment-hook --check --all
```

## GitLab CI
```yaml
check-headers:
  script:
    - path-comment-hook --check --all
```

## Pre-commit in CI
```yaml
- name: Pre-commit
  uses: pre-commit/action@v3.0.0
```
