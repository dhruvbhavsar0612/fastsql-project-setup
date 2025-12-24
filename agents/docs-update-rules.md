# Documentation Update Rules

## When to Update Documentation

Documentation must be updated when:

### 1. New Features Added
- Add to appropriate guide in `docs/guides/`
- Update configuration docs in `docs/configuration/`
- Add examples to getting started if user-facing
- Update CLI reference if new commands/options

### 2. Breaking Changes
- Document in `CHANGELOG.md` with ⚠️ warning
- Update affected guide pages
- Add migration guide if needed
- Update examples

### 3. Configuration Changes
- Update `docs/configuration/` pages
- Update `.env.example` references
- Update `docs/reference/options.md`

### 4. Bug Fixes (User-Impacting)
- Add to `CHANGELOG.md`
- Update troubleshooting sections if applicable

### 5. API Changes
- Update code examples in docs
- Update schema documentation
- Update CLI reference

## Documentation Branch Strategy

### Always Use docs/ Prefix

All documentation changes must be in branches prefixed with `docs/`:

```bash
git checkout -b docs/update-installation-guide
git checkout -b docs/add-caching-examples
git checkout -b docs/fix-typos
```

### Pure Documentation PRs

For documentation-only changes:
- Use `docs/` prefix
- Can be reviewed and merged faster
- Still require CI to pass (builds docs)

### Feature + Docs Together

When a feature includes documentation:
```bash
# Use feat/ prefix, but update docs in same PR
git checkout -b feat/add-redis-support

# Make feature changes
# ... code changes ...

# Update docs in same branch
vim docs/configuration/caching.md
vim docs/getting-started/quickstart.md
vim CHANGELOG.md

git commit -m "feat: add Redis caching support with documentation"
```

## Documentation Structure

```
docs/
├── index.md                    # Homepage
├── getting-started/            # Onboarding users
│   ├── installation.md
│   ├── quickstart.md
│   └── first-project.md
├── configuration/              # Configuration options
│   ├── overview.md
│   ├── database.md
│   ├── authentication.md
│   └── ...
├── guides/                     # In-depth how-tos
│   ├── project-structure.md
│   ├── testing.md
│   ├── docker.md
│   └── ...
├── reference/                  # API/CLI reference
│   ├── cli.md
│   └── options.md
├── contributing.md             # Contribution guide
└── changelog.md                # Links to CHANGELOG.md
```

## Where to Document What

### Installation Changes
→ `docs/getting-started/installation.md`

### New Configuration Option
→ `docs/configuration/<category>.md`
→ `docs/reference/options.md`

### New CLI Command/Flag
→ `docs/reference/cli.md`

### Project Structure Changes
→ `docs/guides/project-structure.md`

### Deployment Changes
→ `docs/guides/docker.md` or `docs/guides/cicd.md`

### Bug Fixes
→ `CHANGELOG.md` (user-facing)
→ Troubleshooting section if needed

### Breaking Changes
→ `CHANGELOG.md` with migration guide
→ Update all affected doc pages

## Documentation Checklist

When updating docs, ensure:

- [ ] Accurate and up-to-date
- [ ] Code examples tested and working
- [ ] Screenshots updated (if applicable)
- [ ] Links work (no 404s)
- [ ] Proper markdown formatting
- [ ] Grammar and spelling checked
- [ ] Navigation updated in `mkdocs.yml` (if new pages)
- [ ] CHANGELOG.md updated
- [ ] Cross-references updated

## Writing Style Guidelines

### 1. Be Clear and Concise
❌ "You might want to consider perhaps using PostgreSQL"
✅ "Use PostgreSQL for production applications"

### 2. Use Active Voice
❌ "The database connection is established by the application"
✅ "The application establishes the database connection"

### 3. Provide Examples
Always include code examples:
```python
# Good example
from fastapi_smith.cli import app

# Run the CLI
app()
```

### 4. Use Admonitions for Important Info

```markdown
!!! note
    This is a note

!!! warning
    This is a warning

!!! tip
    This is a helpful tip

!!! danger
    This is critical information
```

### 5. Structure with Headings
Use proper heading hierarchy (H1 → H2 → H3)

### 6. Link to Related Pages
```markdown
See [Database Configuration](../configuration/database.md) for details.
```

## Testing Documentation

### 1. Build Locally

```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocs-material-extensions

# Build and serve
mkdocs serve

# Visit http://127.0.0.1:8000
```

### 2. Check for Errors

```bash
# Strict build (fails on warnings)
mkdocs build --strict
```

### 3. Verify Links

Check all internal and external links work.

### 4. Test Code Examples

Copy-paste code examples and verify they work.

### 5. Check Mobile View

Documentation should be readable on mobile devices.

## Documentation Review Process

### For docs/ Branches

1. **Create PR** with `docs:` prefix
   ```
   docs: update Redis caching configuration guide
   ```

2. **PR Description** should include:
   - What docs were updated and why
   - Link to related feature PR (if applicable)
   - Screenshots of rendered docs (if significant changes)

3. **Review Checklist**:
   - [ ] Docs build successfully
   - [ ] No broken links
   - [ ] Code examples work
   - [ ] Grammar and spelling correct
   - [ ] Navigation makes sense

4. **Merge**: Fast-track approval for typo fixes and clarifications

## Automatic Deployment

Documentation automatically deploys when:
- PR merged to `main` branch
- GitHub Actions builds with MkDocs
- Deploys to GitHub Pages

**Live site**: https://dhruvbhavsar0612.github.io/fastsql-project-setup/

## Documentation Versioning

Currently: Single version (latest)

Future: Version docs per release
- `latest/` - main branch
- `v0.1.x/` - stable releases
- `v0.2.x/` - next version

## Common Documentation Tasks

### Adding a New Page

1. Create markdown file in appropriate directory:
   ```bash
   vim docs/guides/new-guide.md
   ```

2. Update navigation in `mkdocs.yml`:
   ```yaml
   nav:
     - Guides:
         - New Guide: guides/new-guide.md
   ```

3. Test locally:
   ```bash
   mkdocs serve
   ```

### Updating Code Examples

1. Update the code
2. Test the code works
3. Update the docs with new code
4. Rebuild docs and verify

### Fixing Broken Links

1. Find broken links:
   ```bash
   mkdocs build --strict
   ```

2. Fix in source markdown files

3. Rebuild to verify

## Documentation Maintenance

### Regular Reviews

- **Monthly**: Review docs for accuracy
- **Per Release**: Update all version-specific info
- **On Bug Reports**: Add to troubleshooting

### Keep Updated

- Update screenshots when UI changes
- Update code examples when APIs change
- Update installation steps when requirements change
- Archive outdated information

## Examples

### Good Documentation PR

```
Title: docs: add Redis caching configuration guide

Description:
Adds comprehensive guide for configuring Redis caching including:
- Installation and setup
- Connection pooling
- Cache strategies
- Code examples

Tested all code examples locally.
Related to #45
```

### Documentation Update with Feature

```
Title: feat: add Celery task queue support

Description:
Adds Celery integration for background tasks.

Changes:
- Add Celery configuration in config.py
- Add task queue prompts to CLI
- Generate celery.py template
- Update docs/configuration/tasks.md
- Add examples to docs/guides/background-jobs.md
- Update CHANGELOG.md

All code examples tested.
```

## Questions?

If unsure where to document something:
1. Check existing structure
2. Ask in PR discussion
3. Refer to this guide

When in doubt: More documentation is better than less!
