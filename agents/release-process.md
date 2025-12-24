# Release Process

## Release Checklist

Before creating any release, complete ALL steps in this checklist.

## Pre-Release Checks

### 1. Code Quality ✅

Run all quality checks:

```bash
# All tests must pass
uv run pytest

# Coverage check (aim for 80%+)
uv run pytest --cov=fastapi_smith --cov-report=term-missing

# Type checking must pass
uv run mypy src

# Linting must pass
uv run ruff check src tests

# Format check
uv run ruff format --check src tests
```

**All must pass with no errors.**

### 2. Dependencies ✅

Check dependencies are up to date:

```bash
# Check for outdated packages
uv pip list --outdated

# Update uv.lock if needed
uv sync

# Verify no security vulnerabilities
pip-audit || echo "Consider running: pip install pip-audit && pip-audit"
```

### 3. Documentation ✅

Ensure docs are current:

- [ ] README.md is up to date
- [ ] CHANGELOG.md has all changes for this release
- [ ] Online docs at https://dhruvbhavsar0612.github.io/fastsql-project-setup/ are current
- [ ] All code examples work
- [ ] Installation instructions tested
- [ ] No broken links in docs

```bash
# Build docs locally to verify
mkdocs build --strict
```

### 4. Changelog ✅

Update `CHANGELOG.md` with:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
```

Follow [Keep a Changelog](https://keepachangelog.com/) format.

### 5. Version Bump ✅

Update version in `pyproject.toml`:

```toml
[project]
name = "fastapi-smith"
version = "X.Y.Z"  # Update this
```

**Versioning rules (Semantic Versioning):**
- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, backwards compatible

### 6. Generated Project Testing ✅

Test the actual project generation:

```bash
# Generate a test project
uv run fastapi-smith

# Use these test settings:
# - Project: test-release
# - Database: PostgreSQL + SQLAlchemy
# - Auth: JWT
# - Admin: Yes
# - Docker: Yes

cd test-release

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the app
uv run uvicorn app.main:app &
sleep 3

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Stop the app
pkill -f uvicorn

# Test Docker build
docker build -t test-release .

# Clean up
cd ..
rm -rf test-release
```

**All must work without errors.**

### 7. Cross-Platform Testing ✅

If possible, test on:
- [ ] Linux (Ubuntu/Debian)
- [ ] macOS
- [ ] Windows (WSL)

### 8. Clean Git State ✅

Ensure clean git state:

```bash
git status
# Should show: "nothing to commit, working tree clean"

git log --oneline -10
# Review recent commits

git diff origin/main
# Should be up to date
```

## Creating a Release

### Step 1: Create Release Branch

```bash
git checkout main
git pull origin main
git checkout -b release/vX.Y.Z
```

### Step 2: Commit Version Updates

```bash
# After updating pyproject.toml and CHANGELOG.md
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git push origin release/vX.Y.Z
```

### Step 3: Create Release PR

Create PR with title: `Release vX.Y.Z`

**PR Description Template:**
```markdown
## Release vX.Y.Z

### Summary
Brief description of this release

### Changes
See CHANGELOG.md for full details:
- New feature 1
- Bug fix 1
- etc.

### Pre-Release Checklist
- [x] All tests passing
- [x] Coverage adequate
- [x] Documentation updated
- [x] CHANGELOG.md updated
- [x] Version bumped in pyproject.toml
- [x] Generated project tested
- [x] No broken links

### Breaking Changes
None / List breaking changes

### Migration Guide
N/A / Link to migration guide if breaking changes
```

### Step 4: Review and Merge

- Get approval
- Ensure all CI checks pass
- **Merge using "Merge commit"** (not squash) to preserve history
- Delete release branch after merge

### Step 5: Create Git Tag

```bash
git checkout main
git pull origin main

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push tag
git push origin vX.Y.Z
```

### Step 6: Create GitHub Release

On GitHub:
1. Go to **Releases** → **Draft a new release**
2. Choose the tag: `vX.Y.Z`
3. Release title: `vX.Y.Z`
4. Description: Copy from CHANGELOG.md for this version
5. Click **Publish release**

**Release notes template:**
```markdown
## What's New

Brief highlight of major changes

## Changes

### Added
- Feature 1
- Feature 2

### Fixed
- Bug fix 1
- Bug fix 2

## Installation

```bash
pip install fastapi-smith==X.Y.Z
# or
uvx fastapi-smith@X.Y.Z
```

## Full Changelog

[vX.Y.Z...vX.Y.Z-1](link-to-compare)
```

### Step 7: Publish to PyPI

The GitHub Actions workflow should automatically publish to PyPI when a release is created.

**If manual publishing needed:**

```bash
# Build the package
uv build

# Check the distribution
ls -lh dist/

# Upload to TestPyPI first
uv publish --repository testpypi

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ fastapi-smith==X.Y.Z

# If all good, upload to PyPI
uv publish

# Verify on PyPI
pip install fastapi-smith==X.Y.Z
fastapi-smith --version
```

### Step 8: Verify Deployment

After release:

1. **Check PyPI**: https://pypi.org/project/fastapi-smith/
   - Correct version shown
   - README renders correctly
   - Links work

2. **Test Installation**:
   ```bash
   # Fresh environment
   python -m venv test-env
   source test-env/bin/activate
   pip install fastapi-smith
   fastapi-smith --version
   fastapi-smith  # Test it works
   deactivate
   rm -rf test-env
   ```

3. **Check Documentation**: https://dhruvbhavsar0612.github.io/fastsql-project-setup/
   - Version updated
   - Changelog visible

### Step 9: Announce Release

- Post on GitHub Discussions
- Update any external references
- Social media (if applicable)

## Post-Release

### Update Development Version

Create a new commit on main:

```bash
git checkout main
git pull origin main

# Update to next dev version (e.g., 0.2.0-dev)
# Edit pyproject.toml

git add pyproject.toml
git commit -m "chore: bump version to X.Y.Z-dev"
git push origin main
```

### Monitor for Issues

After release:
- Watch for new issues on GitHub
- Monitor PyPI download stats
- Check for broken installations

## Hotfix Process

For critical bugs in production:

### 1. Create Hotfix Branch

```bash
git checkout vX.Y.Z  # Latest release tag
git checkout -b hotfix/vX.Y.Z+1
```

### 2. Fix the Bug

```bash
# Make minimal changes to fix critical bug
git add .
git commit -m "fix: critical bug description"
```

### 3. Update Version and Changelog

```bash
# Bump patch version: X.Y.Z → X.Y.Z+1
# Update CHANGELOG.md

git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z+1"
```

### 4. Create Hotfix PR

PR to main with title: `Hotfix vX.Y.Z+1`

### 5. Release Hotfix

Follow normal release process from Step 5 onwards.

## Release Frequency

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Every 2-4 weeks with new features
- **Major releases**: When breaking changes necessary

## Version Support

- **Current version**: Full support
- **Previous minor**: Security fixes only
- **Older versions**: No support

## Emergency Rollback

If a release has critical issues:

### 1. Yank from PyPI

```bash
# This prevents new installations but doesn't break existing ones
pip install twine
twine upload --skip-existing  # Mark as yanked on PyPI
```

Or use PyPI web interface: Project → Releases → Options → Yank

### 2. Delete GitHub Release

Mark as pre-release or delete entirely.

### 3. Fix and Re-release

Fix issues and release new patch version.

## Release Artifacts

Each release should have:
- ✅ Git tag
- ✅ GitHub Release with notes
- ✅ PyPI package
- ✅ Updated documentation
- ✅ Updated CHANGELOG.md

## Common Release Issues

### Tests fail on CI but pass locally
- Environment differences
- Check Python version compatibility
- Check dependency versions

### PyPI upload fails
- Version already exists (can't overwrite)
- Authentication issues
- Check .pypirc or use tokens

### Documentation not deploying
- Check GitHub Actions logs
- Verify mkdocs.yml is valid
- Check for broken links

## Release Roles

**Release Manager Responsibilities:**
- Run all pre-release checks
- Coordinate release timing
- Monitor post-release issues
- Update documentation
- Communicate with users

## Automation

Currently automated via GitHub Actions (`.github/workflows/release.yml`):
- ✅ Build package
- ✅ Run tests
- ✅ Publish to PyPI on release creation

## Questions?

If unsure about any step:
1. Consult this document
2. Check previous releases for examples
3. Ask in team discussion before proceeding

**When in doubt, don't release. Better safe than sorry.**
