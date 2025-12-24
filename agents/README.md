# Agent Rules - README

## Overview

This directory contains comprehensive rules and protocols for working on the fastapi-smith project. All contributors and AI agents must follow these guidelines.

## Documents

### 1. [Git Workflow Rules](./git-workflow-rules.md)
**Purpose**: Branch naming, commit messages, PR creation

**Key Points**:
- Always use feature branches with prefixes (`feat/`, `fix/`, `docs/`, etc.)
- Follow conventional commit format
- Pre-commit hooks enforce code quality
- Never commit directly to main

**When to use**: Before starting any work

---

### 2. [Documentation Update Rules](./docs-update-rules.md)
**Purpose**: When and how to update documentation

**Key Points**:
- Always use `docs/` prefix for documentation branches
- Update docs with every user-facing change
- Test documentation builds locally
- Documentation auto-deploys to GitHub Pages

**When to use**: When making any changes that affect users

---

### 3. [Release Process](./release-process.md)
**Purpose**: Creating and publishing releases

**Key Points**:
- Comprehensive pre-release checklist
- Test generated projects before release
- Follow semantic versioning
- Update CHANGELOG.md
- Publish to PyPI

**When to use**: When preparing a new release

---

### 4. [Code Review Guidelines](./code-review-guidelines.md)
**Purpose**: Reviewing and providing feedback on PRs

**Key Points**:
- Self-review before requesting review
- Constructive and specific feedback
- Use comment conventions ([blocking], [suggestion], etc.)
- Focus on behavior, not implementation
- Be respectful and helpful

**When to use**: When reviewing or submitting PRs

---

### 5. [Testing Standards](./testing-standards.md)
**Purpose**: Writing and maintaining tests

**Key Points**:
- 80% minimum coverage, 90% for new code
- Unit, integration, and E2E tests
- Use fixtures and factories
- Test behavior, not implementation
- Fast and reliable tests

**When to use**: When writing any code

---

## Quick Reference

### Starting New Work

1. ✅ Pull latest main: `git checkout main && git pull`
2. ✅ Create feature branch: `git checkout -b <prefix>/<task>`
3. ✅ Make changes and write tests
4. ✅ Run tests: `uv run pytest`
5. ✅ Commit: `git commit -m "<type>: <description>"`
6. ✅ Push and create PR

### Before Merging

- ✅ All tests pass
- ✅ Code reviewed and approved
- ✅ Documentation updated
- ✅ CHANGELOG.md updated
- ✅ No merge conflicts

### Before Releasing

- ✅ Complete [Release Checklist](./release-process.md#pre-release-checks)
- ✅ Test generated projects
- ✅ Update version and CHANGELOG
- ✅ Create release branch and PR
- ✅ Tag and publish

## For AI Agents

When working on this project:

1. **Read relevant docs** before starting work
2. **Follow branch naming** conventions strictly
3. **Run all checks** before committing
4. **Write tests** for all new code
5. **Update documentation** as needed
6. **Follow release process** for versions

## Common Workflows

### Adding a Feature

```bash
git checkout -b feat/my-feature
# Make changes
uv run pytest  # Ensure tests pass
git commit -m "feat: add my amazing feature"
git push origin feat/my-feature
# Create PR on GitHub
```

### Fixing a Bug

```bash
git checkout -b fix/bug-description
# Make fix
uv run pytest  # Add regression test
git commit -m "fix: resolve bug in X"
git push origin fix/bug-description
# Create PR with bug description
```

### Updating Documentation

```bash
git checkout -b docs/update-guides
# Update docs/
mkdocs serve  # Preview locally
git commit -m "docs: update installation guide"
git push origin docs/update-guides
# Create PR - docs will auto-deploy
```

### Creating a Release

```bash
git checkout -b release/v1.2.3
# Update pyproject.toml version
# Update CHANGELOG.md
git commit -m "chore: bump version to 1.2.3"
# Follow full release checklist
```

## File Structure

```
agents/
├── README.md                      # This file
├── git-workflow-rules.md          # Branch, commit, PR rules
├── docs-update-rules.md           # Documentation workflow
├── release-process.md             # Release checklist
├── code-review-guidelines.md      # Review standards
└── testing-standards.md           # Testing requirements
```

## Enforcement

These rules are enforced through:

- **Pre-commit hooks** - Code quality checks
- **GitHub Actions** - CI/CD pipeline
- **Branch protection** - Prevent direct commits to main
- **Required reviews** - PRs need approval
- **Automated tests** - Must pass before merge

## Getting Help

If you're unsure about:
- **Git workflow** → See [git-workflow-rules.md](./git-workflow-rules.md)
- **Documentation** → See [docs-update-rules.md](./docs-update-rules.md)
- **Releasing** → See [release-process.md](./release-process.md)
- **Code review** → See [code-review-guidelines.md](./code-review-guidelines.md)
- **Testing** → See [testing-standards.md](./testing-standards.md)

Still unclear? Open a GitHub issue for discussion.

## Updates

These rules evolve with the project. When updating:

1. Create PR with `docs/update-agent-rules` branch
2. Get team review and approval
3. Communicate changes to all contributors
4. Update this README with summary

## Compliance

All PRs must follow these rules. Non-compliant PRs will:
- Fail CI checks
- Be blocked from merging
- Require fixes before review

## Philosophy

These rules exist to:
- ✅ Maintain code quality
- ✅ Enable collaboration
- ✅ Prevent bugs
- ✅ Speed up development
- ✅ Ensure reliability

Follow them to make the project better for everyone.

---

**Last Updated**: 2025-12-24
**Version**: 1.0.0
