## Path-Comment-Hook – Lean & Focused Project Plan

> **Goal:** Deliver a simple, reliable Python package + pre-commit hook
> that adds relative-path headers to source files. Validate its utility with real users.

---

### **Project Vision & Principles (Simplified):**

*   **Utility First:** Solve one small problem well.
*   **Reliability:** Make it work correctly and consistently.
*   **Ease of Use:** Simple to install, configure, and run.
*   **Performance:** Fast enough not to be annoying.

---

## 0 ▸ Executive Summary

`path-comment-hook` is a Python tool designed to automatically add or update a comment at the top of source files, indicating the file's relative path within the project. This can aid in navigation and context, especially in large codebases or when viewing files outside an IDE.

The tool has evolved significantly with comprehensive functionality including file processing, deletion of headers, intelligent ignore patterns, and user-friendly command-line interface. The immediate goal is to create a stable, well-tested `v0.1.0` release that is easily installable via PyPI.

Future development beyond `v0.1.0` will be strictly driven by user feedback and validated needs. If this core tool proves useful to a tangible number of users/projects, we will then consider adding more advanced configuration or features based on direct requests.

---

## 0.1 ▸ Current Reality

*   **Active Users:** 0 (outside of developer)
*   **GitHub Stars:** 0 (or current number if any)
*   **Test Coverage:** ~69% (monitored via Codecov integration)
*   **Test Suite:** 152 passing tests across all functionality
*   **CI/CD Status:** Fully operational with cross-platform testing
*   **Market Validation:** None to date
*   **Competition:** Editor snippets, manual commenting, potentially other small scripts.
*   **Primary Value Proposition Focus (for v0.1.0):** **Reliability & Ease of Use** – a comprehensive tool that *just works* for both adding and managing path comments across projects.

---

## 0.2 ▸ Hard Questions

1.  **Why would someone use this over editor snippets or existing IDE features?**
    *   *Hypothesis:* For automated, consistent enforcement across a whole project/team, especially via pre-commit hooks, which snippets don't offer. The delete functionality also provides cleanup capabilities that snippets lack.
2.  **What's the actual, specific pain point this solves?**
    *   *Hypothesis:* Quickly understanding a file's location and context when viewed in isolation (e.g., in code reviews, terminal output, or simple editors) without relying on IDE-specific navigation. Reduces cognitive load for frequently context-switching developers. Also provides project hygiene by cleaning up headers when needed.
3.  **Have we talked to at least 10 developers (outside the project) who genuinely express a need for this specific solution?**
    *   *Action:* This needs to be done post-v0.1.0 release.
4.  **What, if anything, would make someone pay for an advanced version of this?**
    *   *Hypothesis (Highly speculative, for far future):* Enterprise compliance, deep VCS integration for context, advanced analytics. Not a concern for v0.1.0.
5.  **Is this a vitamin (nice-to-have) or a painkiller (solves a real, acute problem)?**
    *   *Hypothesis:* Currently a vitamin. The goal of v0.1.0 and subsequent user feedback is to determine if it can become a painkiller for specific workflows or teams.

---

## 1 ▸ Work Completed (Status @ v0.3.x internally, pre-first-release)

*(This section details the existing foundation, which is solid technical work and should be acknowledged. Recent advancements have significantly enhanced functionality.)*

| Area | Deliverables | Status | Notes |
|------|--------------|--------|-------|
| **Repository & Infrastructure** |  | ✅ | |
| ├─ Poetry migration | `pyproject.toml` (Poetry), dependency groups, scripts | ✅ | Migrated for dependency management |
| ├─ Development automation | `Makefile`, `setup-dev.sh`, VS Code config | ✅ | Streamlined developer experience |
| ├─ Git workflow | `develop`/`main` branches, conventional commits | ✅ | Professional git workflow established |
| └─ Pre-commit integration | Comprehensive hook suite (ruff, mypy, bandit, etc.) | ✅ | Code quality gates |
| **Core Functionality** |  | ✅ | |
| ├─ File detection | `detectors.py` with binary/shebang handling | ✅ | Robust file type detection |
| ├─ Header injection | `injector.py` with preservation logic | ✅ | Smart header insertion |
| ├─ Header deletion | **NEW**: `delete_header()` with intelligent detection | ✅ | **Complete removal of path comments** |
| ├─ CLI interface | Typer-based CLI with comprehensive commands | ✅ | **Enhanced with delete, version, help support** |
| ├─ Auto-discovery | Recursive file discovery with advanced exclusions | ✅ | `--all` flag for project-wide processing |
| └─ Command shortcuts | **NEW**: Auto-insert run command (`pch --all` = `pch run --all`) | ✅ | **Improved user experience** |
| **Configuration System** |  | ✅ | |
| ├─ TOML configuration | `[tool.path-comment-hook]` in `pyproject.toml` | ✅ | User-configurable behavior |
| ├─ Advanced exclusions | **ENHANCED**: 52 default ignore patterns + custom globs | ✅ | **Comprehensive file filtering** |
| ├─ Ignore system | Version control, build artifacts, caches, IDEs | ✅ | **Smart defaults for common exclusions** |
| ├─ Configuration display | `show-config` command with detailed output | ✅ | **Enhanced config introspection** |
| └─ Custom comment maps | File extension to comment style mapping | ✅ | Extensible comment formats |
| **File Handling & Safety** |  | ✅ | |
| ├─ Encoding detection | UTF-8 + chardet fallback | ✅ | Robust encoding handling |
| ├─ Line ending preservation | CRLF/LF detection and preservation | ✅ | Cross-platform compatibility |
| ├─ Atomic writes | Temporary file + rename for safety | ✅ | Data integrity protection |
| └─ Error handling | Comprehensive exception handling | ✅ | Graceful failure modes |
| **Performance & Concurrency** |  | ✅ | |
| ├─ Multiprocessing | ThreadPoolExecutor for parallel processing | ✅ | Performance improvement |
| ├─ Progress reporting | Rich-based progress bars | ✅ | User feedback |
| ├─ Concise output | **NEW**: Summary messages for bulk operations | ✅ | **Clean, professional output** |
| └─ Worker configuration | Configurable thread count | ✅ | Tunable performance |
| **CLI & User Experience** |  | ✅ | |
| ├─ Version support | **NEW**: `--version` flag with proper version display | ✅ | **Professional CLI behavior** |
| ├─ Help system | **ENHANCED**: `-h` flag support for all commands | ✅ | **Improved accessibility** |
| ├─ Multiple commands | `run`, `delete`, `show-config` with full option parity | ✅ | **Comprehensive functionality** |
| ├─ Bulk operations | Smart output for `--all` operations (summary vs. detailed) | ✅ | **Enhanced user experience** |
| └─ Pre-commit integration | Seamless integration with pre-commit hooks | ✅ | **Ready for team adoption** |
| **Testing & Quality** |  | ✅ | |
| ├─ Test suite | **IMPROVED**: 78 tests across all modules (vs. 54 previously) | ✅ | **Comprehensive test coverage** |
| ├─ Test categories | Unit, integration, file handling, config, CLI, deletion | ✅ | **Multiple test dimensions including new features** |
| ├─ All tests passing | **FIXED**: All 78 tests now pass consistently | ✅ | **Stable, reliable codebase** |
| ├─ CI/CD pipeline | GitHub Actions with matrix testing | ✅ | Automated quality assurance |
| ├─ Code quality | Ruff, mypy, bandit, docformatter | ✅ | Production-ready code standards |
| └─ Coverage improvement | **IMPROVED**: ~78% (from 56%) | ✅ | **Significant progress toward 90% target** |
| **Documentation** |  | 🚧 | |
| ├─ README | Comprehensive installation and usage guide | ✅ | Detailed user documentation |
| ├─ Code documentation | Docstrings, type hints throughout | ✅ | Self-documenting codebase |
| ├─ Feature documentation | **NEW**: All new features documented inline | ✅ | **Complete feature coverage** |
| └─ API documentation | **NEEDS WORK**: Auto-generated API docs via MkDocs | 📋 | **Priority for v0.1.0** |

**Major Recent Advancements (Completed):**
*   ✅ **Delete Command**: Full-featured `pch delete` command with `--all`, `--check`, `--verbose` support
*   ✅ **Version Support**: Professional `--version` flag displaying current version
*   ✅ **Auto-insert Run**: `pch --all` automatically becomes `pch run --all` for better UX
*   ✅ **Help Flag Support**: `-h` flag works alongside `--help` for all commands
*   ✅ **Concise Output**: Bulk operations show "Successfully updated X files" instead of listing each file
*   ✅ **Comprehensive Ignores**: 52 default ignore patterns covering version control, build artifacts, caches, IDEs
*   ✅ **Enhanced Config Display**: `custom_comment_map` and all config options properly explained
*   ✅ **Test Suite Stability**: All 152 tests passing consistently, enhanced coverage
*   ✅ **Smart Path Detection**: Intelligent path comment detection for deletion operations
*   ✅ **CI/CD Pipeline**: Comprehensive GitHub Actions with cross-platform testing, security scanning, and automated releases
*   ✅ **Codecov Integration**: Real-time coverage reporting and monitoring
*   ✅ **Documentation Infrastructure**: Complete MkDocs site with Material theme and GitHub Pages deployment
*   ✅ **ASCII Art Integration**: Professional welcome message and post-install display
*   ✅ **Cross-Platform Compatibility**: Resolved Windows line ending issues and Poetry installation problems

**Current Technical Debt & Remaining Priorities for `v0.1.0`:**
*   **Test Coverage**: Increase from ~69% to >90% (MEDIUM PRIORITY - monitoring via Codecov)
*   **PyPI Packaging**: Final packaging and metadata preparation for PyPI release (HIGH PRIORITY)
*   **Version Bump**: Update version from 0.0.0 to 0.1.0 in preparation for release (HIGH PRIORITY)
*   **Release Notes**: Prepare comprehensive changelog and release documentation (MEDIUM PRIORITY)

**Deferred Items (Previously Problematic, Now Resolved):**
*   ~~Permission Error Handling~~ → ✅ **RESOLVED**: Proper error handling implemented
*   ~~Pre-commit Shorthand Syntax~~ → ✅ **RESOLVED**: Auto-insert functionality implemented
*   ~~-h Flag Support~~ → ✅ **RESOLVED**: Full `-h` flag support added
*   ~~Documentation Site~~ → ✅ **RESOLVED**: Complete MkDocs site with Material theme deployed
*   ~~Windows CI Testing~~ → ✅ **RESOLVED**: Windows added to CI matrix, all tests pass
*   ~~Cross-Platform Line Endings~~ → ✅ **RESOLVED**: Binary file handling fixes Windows compatibility
*   ~~CI/CD Pipeline Failures~~ → ✅ **RESOLVED**: Docformatter conflicts eliminated, Poetry issues fixed
*   ~~Badge Accuracy~~ → ✅ **RESOLVED**: All README badges now display real-time, accurate information

---

## 2 ▸ Lean Roadmap (Focus: `v0.1.0` Release & Validation)

### **Phase 1: Finalize & Ship `v0.1.0` (IMMEDIATE FOCUS)**
**Goal:** Release a stable, feature-complete, and well-documented first version to PyPI.
**Key Outcomes:**
    *   Comprehensive functionality is robust and tested.
    *   Users can easily install and use the full feature set.
    *   Professional documentation exists.

| ID    | Task                                  | Sub-Tasks & Details                                                                                                                                                                                             | Acceptance Criteria (AC)                                                                                                                               | Priority   |
| :---- | :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| **P1-01** | **Test Coverage >90%**                | 1. Analyze current ~69% coverage; identify gaps in CLI, edge cases. <br> 2. Write targeted tests for remaining uncovered paths. <br> 3. Maintain >90% coverage target via Codecov. | • Test coverage consistently ≥ 90%. <br> • All major features fully tested. <br> • Codecov integration monitors coverage.                                            | **MEDIUM** |
| ~~**P1-02**~~ | ~~**Windows CI & Compatibility**~~        | ✅ **COMPLETED**: Windows added to CI matrix, all line ending issues resolved via binary file handling.                               | ✅ All tests pass on Windows CI. Cross-platform compatibility verified.                                                                | ~~**COMPLETE**~~     |
| ~~**P1-03**~~ | ~~**Basic Documentation Site (MkDocs)**~~ | ✅ **COMPLETED**: MkDocs with Material theme deployed, comprehensive documentation structure created with all essential pages. | ✅ Complete docs site covers all features, API reference, usage examples. | ~~**COMPLETE**~~     |
| **P1-04** | **PyPI Release `v0.1.0`**             | 1. Polish `README.md` for PyPI with new features. <br> 2. Finalize `pyproject.toml` metadata (version `0.1.0`, feature descriptions). <br> 3. Build package (`poetry build`). <br> 4. Test publishing to TestPyPI. <br> 5. Publish to PyPI. <br> 6. Create `v0.1.0` git tag and GitHub Release. | • Package successfully installs via `pip install path-comment-hook`. <br> • All CLI commands work after fresh install. <br> • PyPI page reflects full feature set. | **HIGH**     |
| **P1-05** | **Performance Validation**    | 1. Test tool on medium-sized directory (100-500 files). <br> 2. Validate both `run --all` and `delete --all` performance. <br> 3. Ensure concise output works correctly at scale. | • Tool processes 500 files in reasonable time (<10 seconds). <br> • Bulk operations show proper summary messages. | **LOW**   |

**Definition of Done for Phase 1 (`v0.1.0`):**
*   All P1 tasks completed.
*   `path-comment-hook==0.1.0` is published on PyPI with full feature set.
*   Documentation site covers all functionality.
*   Project is ready for initial user feedback with comprehensive capabilities.

---

### **Phase 2: Validate & Enhance (Post-`v0.1.0` Release)**
**Goal:** Gather user feedback on comprehensive feature set, fix bugs, and add quality-of-life improvements.
**Key Outcomes:**
    *   Early user pain points addressed.
    *   Tool's comprehensive functionality validated in real-world use.
    *   Clear understanding of most valuable features.

*(This phase is intentionally less detailed now; its content will be defined by user feedback from v0.1.0)*

| ID    | Task                                  | Details                                                                                                                                                               | AC                                                                     |
| :---- | :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| **P2-01** | **Gather User Feedback**              | 1. Announce `v0.1.0` with full feature set. <br> 2. Actively solicit feedback on delete functionality, ignore patterns, CLI UX. <br> 3. Get 5-10 projects to try comprehensive workflow. | • Feedback on delete, ignore patterns, CLI shortcuts received.                 |
| **P2-02** | **Bug Fixing & Stability**            | 1. Prioritize and fix bugs in new features (delete, ignore patterns, etc.). <br> 2. Release patch versions as needed.                                                        | • Critical bugs in all features resolved.                          |
| **P2-03** | **Usage Analytics & Optimization**    | 1. Understand which features are most/least used. <br> 2. Optimize based on real usage patterns. <br> 3. Enhance documentation for popular workflows. | • Clear understanding of feature adoption and user preferences. |
| **P2-04** | **Quality-of-Life Improvements**      | Based on feedback, implement small UX improvements. Examples: <br> • Enhanced ignore pattern syntax. <br> • More flexible comment templates. <br> • Additional CLI shortcuts. | • User-requested improvements enhance daily workflow. |

**Definition of Done for Phase 2:**
*   `v0.1.0` comprehensive feature set has been validated by external users.
*   Critical feedback has been addressed.
*   Clear data on feature usage and user preferences exists.

---

### **Phase 3: Strategic Decision (Post-Phase 2)**
**Goal:** Decide the project's future based on validated usage of comprehensive feature set.
**Key Outcomes:**
    *   Data-driven decision on project direction: maintain, expand, pivot, or sunset.

| Decision Point                                       | Criteria                                                                                                     | Potential Action                                                                                                |
| :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| **Low Adoption** (<10 active users, minimal feedback on comprehensive features) | Comprehensive feature set is not solving significant problems for others. | • **Sunset:** Archive the project. <br> • **Personal Tool:** Maintain for personal use only. |
| **Selective Adoption** (Users primarily use only some features, clear preferences emerge) | Some features are highly valued, others ignored. Tool serves specific needs well. | • **Focused Maintenance:** Emphasize popular features, consider deprecating unused ones. <br> • **Targeted Documentation:** Focus on validated use cases. |
| **Broad Adoption** (>50 users, active use of multiple features, community engagement) | Comprehensive feature set is solving real problems across different workflows. | • **Community Building:** Foster contributions and feature requests. <br> • **Cautious Expansion:** Consider advanced features for proven high-value use cases. |

---

## 3 ▸ Realistic Success Metrics (Updated for Enhanced Functionality)

*   **Test Coverage:** Achieved and maintained >90%.
*   **Feature Adoption:** Clear data on which features (run, delete, ignore patterns) are most valuable to users.
*   **Installations & Use:** At least 10 distinct projects/users have installed and actively used `v0.1.0` within 1-2 months.
*   **GitHub Stars:** 25-50 stars (as indicator of interest in comprehensive functionality).
*   **Quality Feedback:** At least 3 developers provide feedback specifically on delete functionality, ignore patterns, or CLI UX.
*   **Documentation Effectiveness:** Users successfully adopt multiple features based on documentation.
*   **Real-world Validation:** Evidence that both add and delete workflows are valuable in practice.

---

## 4 ▸ Resources

*   **Lead Developer (You):** Focused effort on Phase 1 completion. Subsequent investment based on Phase 3 decision.
*   **Contributors:** 1-2 external individuals interested in comprehensive toolset for feedback and contributions.
*   **Budget:** $0 (all tools and platforms are free tier).
*   **Timeline:** Aim to ship feature-complete `v0.1.0` within 2-3 weeks focused effort on remaining priorities.

---

## 5 ▸ When to Kill This Project

*   If comprehensive `v0.1.0` fails to attract <5 users providing feedback within 2-3 months of promotion.
*   If user feedback indicates the comprehensive feature set is overwhelming or unnecessary for the core problem.
*   If >90% test coverage proves unachievable or maintenance burden exceeds value.
*   If no external interest in the full feature set emerges within 3-4 months post-release.
*   If personal motivation wanes due to lack of validation of the comprehensive approach.

---

## 6 ▸ Governance & Quality Gates

| Aspect | Policy |
|--------|--------|
| **Semantic Versioning** | MAJOR ⇒ breaking, MINOR ⇒ new features, PATCH ⇒ bug-fix. |
| **Branch Model** | `develop` default, `main` protected for releases, `feature/*`, `fix/*`. |
| **CI Gates** | Ruff, mypy (strict), pytest + >90% coverage target, Bandit. |
| **Review Rules** | Self-review for solo dev, external review preferred if contributors emerge. |

---

## 7 ▸ Lessons Learned & What's Working Well

### **Recent Successful Strategies**
- **Comprehensive Feature Development**: Building delete, version, help, and ignore functionality created a complete tool
- **User Experience Focus**: Auto-insert commands and concise output significantly improve daily usage
- **Intelligent Defaults**: 52 default ignore patterns solve real-world file filtering needs without configuration
- **Test-Driven Improvements**: Fixing all 78 tests created a stable foundation for new features
- **Incremental Enhancement**: Each feature built naturally on existing architecture

### **Validated Technical Decisions**
- **Modular Architecture**: Easy addition of delete functionality proves design flexibility
- **Rich CLI Framework**: Typer enabled sophisticated command structure with minimal complexity
- **Comprehensive Configuration**: TOML-based config system handles growing feature set elegantly
- **Parallel Processing**: Performance remains good even with expanded functionality

### **Key Success Factors for v0.1.0**
- **Feature Completeness**: Comprehensive add/delete/configure workflow addresses full user journey
- **Professional Polish**: Version support, help systems, concise output create professional tool experience
- **Smart Defaults**: Intelligent ignore patterns and auto-insert commands reduce configuration burden
- **Stable Foundation**: All tests passing provides confidence in comprehensive feature set
