# Git Workflow Rules

## Branch Naming Convention

All work must be done in feature branches following this naming convention:

```
<prefix>/<descriptive-task-name>
```

### Prefixes

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks (dependencies, configs)
- `ci/` - CI/CD changes

### Examples

```bash
feat/add-postgres-support
fix/jwt-token-expiry
docs/update-installation-guide
refactor/database-connection
test/add-auth-tests
chore/update-dependencies
ci/add-docker-build
```

## Branch Creation Workflow

### 1. Always Start from Updated Main

```bash
git checkout main
git pull origin main
```

### 2. Create Feature Branch

```bash
git checkout -b <prefix>/<task-name>
```

### 3. Make Changes

- Write code
- Add tests
- Update documentation if needed

### 4. Commit Changes

Follow conventional commit format:

```bash
git add .
git commit -m "<type>: <description>"
```

**Commit types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

**Examples:**
```bash
git commit -m "feat: add SQLModel ORM support"
git commit -m "fix: resolve JWT token refresh issue"
git commit -m "docs: update database configuration guide"
```

## Pre-commit Checks

Before every commit, the following checks run automatically:

### 1. Code Formatting
- **Ruff** formats all Python files
- Auto-fixes simple issues

### 2. Linting
- **Ruff** checks for code quality issues
- Reports errors that need manual fixing

### 3. Type Checking
- **mypy** validates type hints
- Ensures type safety

### 4. Import Sorting
- **Ruff** organizes imports
- Removes unused imports

## Pre-push Checks

Before pushing to remote, ensure:

### 1. All Tests Pass

```bash
uv run pytest
```

### 2. Coverage is Adequate

```bash
uv run pytest --cov=fastapi_smith --cov-report=term-missing
```

Target: 80%+ coverage for new code

### 3. Type Checking Passes

```bash
uv run mypy src
```

### 4. Linting Passes

```bash
uv run ruff check src tests
```

### 5. No Debugging Code

Check for:
- `print()` statements
- `breakpoint()`
- `import pdb`
- `TODO` comments (document in issues instead)

## Push Workflow

### 1. Push Feature Branch

```bash
git push origin <prefix>/<task-name>
```

### 2. Create Pull Request

On GitHub, create a PR with:

**Title format:**
```
<type>: <description>
```

**Description must include:**
- Summary of changes (what and why)
- Related issue numbers (#123)
- Testing done
- Screenshots (if UI changes)
- Breaking changes (if any)

**PR Template:**
```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- List of specific changes
- Another change
- etc.

## Related Issues
Closes #123
Relates to #456

## Testing
- [ ] Unit tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Documentation
- [ ] README updated (if needed)
- [ ] Docs updated (if needed)
- [ ] CHANGELOG updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Pull Request Rules

### Required Checks

All PRs must pass:
- ✅ CI tests (pytest)
- ✅ Code coverage (80%+)
- ✅ Linting (ruff)
- ✅ Type checking (mypy)
- ✅ Build succeeds

### Review Requirements

- At least 1 approval required
- No unresolved comments
- All CI checks passing

### Merging

- **Squash and merge** for feature branches
- **Merge commit** for release branches
- Delete branch after merge

## Never Commit Directly to Main

**Exception:** Emergency hotfixes only, with immediate PR to document changes

## Common Mistakes to Avoid

❌ **DON'T:**
- Push directly to main
- Commit without running tests
- Skip pre-commit hooks (`--no-verify`)
- Use generic commit messages ("fix", "update")
- Commit sensitive data (.env files, secrets)
- Leave debugging code

✅ **DO:**
- Work in feature branches
- Write descriptive commit messages
- Run tests before pushing
- Update docs with code changes
- Keep commits focused and atomic
- Rebase on main before PR

## Example Complete Workflow

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feat/add-redis-caching

# 3. Make changes
# ... edit files ...

# 4. Run tests
uv run pytest

# 5. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: add Redis caching support with connection pooling"

# 6. Push to remote
git push origin feat/add-redis-caching

# 7. Create PR on GitHub

# 8. Address review comments
# ... make changes ...
git add .
git commit -m "fix: address PR review comments"
git push origin feat/add-redis-caching

# 9. After approval and merge
git checkout main
git pull origin main
git branch -d feat/add-redis-caching
```

## Documentation Updates

See [docs-update-rules.md](./docs-update-rules.md) for documentation-specific workflows.

## Release Process

See [release-process.md](./release-process.md) for creating and publishing releases.
