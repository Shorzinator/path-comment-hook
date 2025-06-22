## Pull Request Type
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring (no functional changes)
- [ ] Test improvements

## Description
Brief description of the changes and their purpose.

## Related Issue(s)
Fixes #(issue number)
Closes #(issue number)
Related to #(issue number)

## Changes Made
- [ ] Added/modified functionality
- [ ] Updated tests
- [ ] Updated documentation
- [ ] Updated changelog

## Testing
Describe the tests you ran to verify your changes:

- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Tested manually with various file types
- [ ] Tested on multiple platforms (specify which)

### Test Commands Run
```bash
# Commands used for testing
poetry run pytest tests/
poetry run ruff check src tests
poetry run mypy src/path_comment tests
```

## Breaking Changes
If this is a breaking change, describe what breaks and how users should adapt:

## Documentation
- [ ] Updated README.md (if needed)
- [ ] Updated docs/ (if needed)
- [ ] Updated docstrings (if needed)
- [ ] Updated CHANGELOG.md

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

---

**Additional Notes:**
Add any additional notes, concerns, or questions for reviewers here.
