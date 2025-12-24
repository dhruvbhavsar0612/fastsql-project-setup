# Code Review Guidelines

## Purpose

Code reviews ensure:
- Code quality and maintainability
- Knowledge sharing across team
- Bug prevention before production
- Consistent code style
- Security best practices

## When to Request Review

Request code review when:
- ✅ PR is ready for merge
- ✅ All CI checks passing
- ✅ Self-review completed
- ✅ Description is clear and complete
- ✅ Tests added/updated

## Self-Review Checklist

Before requesting review, check:

### Code Quality
- [ ] Code follows project style (Ruff passes)
- [ ] Type hints added (mypy passes)
- [ ] No commented-out code
- [ ] No debug statements (print, breakpoint)
- [ ] Meaningful variable/function names
- [ ] Complex logic has comments
- [ ] No code duplication
- [ ] Error handling implemented

### Tests
- [ ] New functionality has tests
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases covered
- [ ] All tests pass locally
- [ ] Coverage maintained/improved

### Documentation
- [ ] Docstrings for public functions/classes
- [ ] README updated (if needed)
- [ ] Docs updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] Code comments for complex logic

### Security
- [ ] No secrets in code
- [ ] Input validation added
- [ ] SQL injection prevented
- [ ] XSS prevention (if applicable)
- [ ] Dependencies secure

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Caching considered (if appropriate)

## For Reviewers

### Review Process

1. **Understand the Context**
   - Read PR description
   - Check related issues
   - Understand the "why" not just the "what"

2. **Review the Code**
   - Check out branch locally if needed
   - Read through all changes
   - Test functionality manually
   - Run tests locally

3. **Provide Feedback**
   - Be constructive and respectful
   - Explain the "why" behind suggestions
   - Ask questions if unclear
   - Suggest alternatives

4. **Approve or Request Changes**
   - Approve if ready to merge
   - Request changes if issues found
   - Comment for minor suggestions

### What to Look For

#### Critical (Block Merge)
- ❌ Tests failing
- ❌ Security vulnerabilities
- ❌ Breaking changes without documentation
- ❌ Data loss potential
- ❌ Performance regressions
- ❌ Incorrect functionality

#### Important (Should Fix)
- ⚠️ Missing tests
- ⚠️ Poor error handling
- ⚠️ Code duplication
- ⚠️ Missing documentation
- ⚠️ Unclear variable names
- ⚠️ Type hint issues

#### Nice to Have (Suggestions)
- 💡 Code style improvements
- 💡 Better abstractions
- 💡 Performance optimizations
- 💡 Additional test cases
- 💡 Documentation enhancements

### Review Comments

Use GitHub's review features:

**Request Changes:**
```markdown
This needs to be fixed before merge:
- SQL injection vulnerability on line 45
- Missing error handling on line 78
```

**Approve:**
```markdown
LGTM! Nice implementation of the caching layer.
```

**Comment:**
```markdown
Suggestion: Consider using a constant for this magic number.
```

### Comment Conventions

Use prefixes for clarity:

- `[blocking]` - Must fix before merge
- `[suggestion]` - Optional improvement
- `[question]` - Asking for clarification
- `[nit]` - Minor style/formatting issue
- `[praise]` - Positive feedback

**Examples:**

```markdown
[blocking] This SQL query is vulnerable to injection. Use parameterized queries.

[suggestion] Consider extracting this to a separate function for reusability.

[question] Why did we choose Redis over Memcached here?

[nit] Missing space after comma on line 42.

[praise] Great test coverage on the edge cases!
```

## Response Time

- **Initial acknowledgment**: Within 1 business day
- **Full review**: Within 2 business days
- **Urgent/hotfix**: Same day

## Handling Feedback

### For PR Authors

**Receiving feedback:**
- ✅ Thank reviewers for their time
- ✅ Ask questions if unclear
- ✅ Push back respectfully if disagree
- ✅ Fix issues promptly
- ✅ Mark conversations resolved

**DON'T:**
- ❌ Take criticism personally
- ❌ Ignore feedback
- ❌ Be defensive
- ❌ Rush changes

**Responding to comments:**

```markdown
Good ✅:
"Great catch! I've updated the error handling. Fixed in abc123."

Good ✅:
"I considered that approach, but went with this because X. What do you think?"

Bad ❌:
"I'll fix it." (then don't)

Bad ❌:
"This is fine as is." (dismissive)
```

## Review Best Practices

### For Reviewers

**DO:**
- ✅ Review promptly
- ✅ Test the code
- ✅ Give specific feedback
- ✅ Praise good work
- ✅ Be respectful and constructive
- ✅ Explain reasoning
- ✅ Offer solutions, not just problems

**DON'T:**
- ❌ Nitpick excessively
- ❌ Rubber-stamp without reading
- ❌ Be vague ("this is bad")
- ❌ Rewrite the entire PR
- ❌ Ignore the context
- ❌ Be condescending

### For Authors

**DO:**
- ✅ Keep PRs small and focused
- ✅ Provide context in description
- ✅ Respond to feedback
- ✅ Be open to suggestions
- ✅ Update based on feedback
- ✅ Thank reviewers

**DON'T:**
- ❌ Create massive PRs
- ❌ Leave cryptic descriptions
- ❌ Ignore comments
- ❌ Argue unnecessarily
- ❌ Rush to merge
- ❌ Be defensive

## PR Size Guidelines

**Ideal PR size:**
- 📝 < 200 lines changed
- 📝 Single feature/fix
- 📝 Reviewable in < 30 minutes

**Too large?**
- 🚫 > 500 lines changed
- 🚫 Multiple features
- 🚫 Takes > 1 hour to review

Split large PRs into smaller ones:
1. Refactoring + tests
2. Feature implementation
3. Documentation

## Common Review Scenarios

### New Feature Review

Check:
- Tests comprehensive?
- Documentation complete?
- Error handling robust?
- Performance acceptable?
- Backwards compatible?

### Bug Fix Review

Check:
- Root cause identified?
- Fix correct and complete?
- Test added to prevent regression?
- Side effects considered?

### Refactoring Review

Check:
- Behavior unchanged?
- Tests still pass?
- Improvement clear?
- No scope creep?

### Documentation Review

Check:
- Accurate?
- Clear and concise?
- Examples work?
- Links valid?
- Grammar/spelling correct?

## Disagreements

If author and reviewer disagree:

1. **Discuss**: Have a conversation
2. **Explain**: Both sides explain reasoning
3. **Evidence**: Provide benchmarks, examples
4. **Compromise**: Find middle ground
5. **Escalate**: Involve maintainer if needed

**Remember**: Goal is best code, not "winning"

## Automated Checks

Before human review, CI must pass:
- ✅ Tests
- ✅ Linting
- ✅ Type checking
- ✅ Build

Reviewers should focus on:
- Logic correctness
- Architecture decisions
- Test quality
- User experience
- Security

## Examples

### Good Review Comment

```markdown
[suggestion] Line 45: Consider extracting this database query into the repository layer. 

This would make it easier to test and follows our repository pattern. Something like:

```python
# In repositories/user.py
async def get_user_by_email(db: AsyncSession, email: str):
    return await db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
```

What do you think?
```

### Good PR Response

```markdown
Great suggestion! I've extracted it to the repository layer as you suggested. 
Also added tests for the new repository method.

Updated in commit abc123.
```

## Review Checklist

Use this for every review:

```markdown
## Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling appropriate

### Code Quality
- [ ] Readable and maintainable
- [ ] Follows project patterns
- [ ] No code duplication
- [ ] Type hints present

### Tests
- [ ] Tests added/updated
- [ ] Tests are meaningful
- [ ] Coverage adequate
- [ ] All tests pass

### Documentation
- [ ] Code comments where needed
- [ ] Docstrings for public APIs
- [ ] Docs updated if needed
- [ ] CHANGELOG updated

### Security
- [ ] No security vulnerabilities
- [ ] Input validation present
- [ ] No hardcoded secrets

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
```

## Continuous Improvement

After each release:
- Review what issues slipped through
- Update review guidelines
- Share lessons learned
- Improve automated checks

## Questions?

If unsure about review process:
1. Refer to this guide
2. Ask in PR comments
3. Discuss with team

**Remember: Reviews are about improving code and sharing knowledge, not finding fault.**
