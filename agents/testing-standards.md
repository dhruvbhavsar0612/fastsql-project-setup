# Testing Standards

## Testing Philosophy

- **Test behavior, not implementation**
- **Write tests first (TDD encouraged)**
- **Keep tests simple and focused**
- **Tests should be fast and reliable**
- **Tests are documentation**

## Test Coverage Requirements

### Minimum Coverage
- **Overall**: 80% coverage
- **New code**: 90% coverage
- **Critical paths**: 100% coverage

### What to Test

**Must Test:**
- ✅ All public APIs
- ✅ Business logic
- ✅ Error handling
- ✅ Edge cases
- ✅ Security features
- ✅ Database operations
- ✅ Authentication/authorization

**Optional:**
- 💡 Private helper functions (if complex)
- 💡 UI rendering (if applicable)

**Don't Test:**
- ❌ Third-party libraries
- ❌ Framework internals
- ❌ Simple getters/setters

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_cli.py              # CLI tests
├── test_generator.py        # Project generation tests
├── test_config.py           # Configuration tests
└── integration/             # Integration tests
    └── test_full_flow.py
```

### Test File Naming

- **File**: `test_<module>.py`
- **Class**: `Test<Feature>`
- **Function**: `test_<behavior>`

**Examples:**
```python
# test_auth.py
class TestJWTAuthentication:
    def test_create_token_with_valid_user(self):
        pass
    
    def test_create_token_with_invalid_user(self):
        pass
    
    def test_token_expiry(self):
        pass
```

## Test Types

### 1. Unit Tests

Test individual functions/methods in isolation.

```python
def test_hash_password():
    """Test password hashing produces different hash each time."""
    password = "mysecret"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
```

**Characteristics:**
- Fast (< 100ms each)
- No external dependencies
- Use mocks/stubs for dependencies
- Test one thing

### 2. Integration Tests

Test multiple components working together.

```python
@pytest.mark.asyncio
async def test_user_registration_flow(client: AsyncClient, db: AsyncSession):
    """Test complete user registration flow."""
    # Register user
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201
    
    # Verify user in database
    result = await db.execute(select(User).where(User.email == "test@example.com"))
    user = result.scalar_one()
    assert user.email == "test@example.com"
    
    # Verify can login
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

**Characteristics:**
- Slower (< 1s each)
- Use test database
- Test multiple components
- Test real workflows

### 3. End-to-End Tests

Test complete user scenarios.

```python
def test_full_project_generation():
    """Test generating a complete project and running it."""
    # Generate project
    result = subprocess.run(
        ["fastapi-smith", "--output", "test-project"],
        input="test\n...\n",
        capture_output=True
    )
    assert result.returncode == 0
    
    # Verify structure
    assert os.path.exists("test-project/app/main.py")
    assert os.path.exists("test-project/pyproject.toml")
    
    # Install dependencies
    subprocess.run(["uv", "sync"], cwd="test-project", check=True)
    
    # Run tests
    result = subprocess.run(
        ["uv", "run", "pytest"],
        cwd="test-project",
        capture_output=True
    )
    assert result.returncode == 0
```

**Characteristics:**
- Slowest (several seconds)
- Test from user perspective
- Run sparingly
- Use for critical paths

## Fixtures

### Common Fixtures

```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from httpx import AsyncClient

@pytest.fixture
async def db() -> AsyncSession:
    """Provide test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
    
    await engine.dispose()

@pytest.fixture
async def client(db: AsyncSession) -> AsyncClient:
    """Provide test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def sample_user(db: AsyncSession):
    """Provide sample user for tests."""
    user = User(email="test@example.com", hashed_password=hash_password("secret"))
    db.add(user)
    await db.commit()
    return user

@pytest.fixture
def auth_headers(sample_user):
    """Provide authentication headers."""
    token = create_access_token(sample_user.id)
    return {"Authorization": f"Bearer {token}"}
```

## Test Patterns

### AAA Pattern (Arrange-Act-Assert)

```python
def test_user_creation():
    # Arrange
    email = "test@example.com"
    password = "secret123"
    
    # Act
    user = create_user(email, password)
    
    # Assert
    assert user.email == email
    assert user.id is not None
    assert verify_password(password, user.hashed_password)
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid-email", False),
    ("missing@", False),
    ("@nodomain.com", False),
])
def test_email_validation(email: str, expected: bool):
    assert is_valid_email(email) == expected
```

### Testing Exceptions

```python
def test_user_not_found_raises_404():
    with pytest.raises(HTTPException) as exc_info:
        get_user_or_404(db, user_id=999)
    
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail.lower()
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_database_query(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    assert len(users) == 0
```

## Mocking

### When to Mock

Mock external dependencies:
- External APIs
- File system operations
- Time-dependent code
- Random number generation
- External services (email, SMS)

### Using pytest-mock

```python
def test_send_welcome_email(mocker):
    # Mock email sending
    mock_send = mocker.patch("app.services.email.send_email")
    
    # Call function
    register_user("test@example.com", "password")
    
    # Verify email sent
    mock_send.assert_called_once()
    args = mock_send.call_args[0]
    assert args[0] == "test@example.com"
    assert "Welcome" in args[1]
```

### Mocking Time

```python
def test_token_expiry(mocker):
    # Mock current time
    mock_time = mocker.patch("time.time", return_value=1000000)
    
    token = create_token(user_id=1, expires_in=3600)
    
    # Advance time
    mock_time.return_value = 1000000 + 3601
    
    # Token should be expired
    with pytest.raises(TokenExpiredError):
        verify_token(token)
```

## Database Testing

### Use Transactions

```python
@pytest.fixture
async def db():
    """Rollback after each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSession(bind=conn) as session:
            # Start transaction
            async with session.begin():
                yield session
                # Rollback happens automatically
```

### Test Data Factories

```python
# factories.py
class UserFactory:
    @staticmethod
    async def create(db: AsyncSession, **kwargs):
        defaults = {
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "hashed_password": hash_password("default_password"),
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

# In tests
async def test_user_list(db: AsyncSession):
    user1 = await UserFactory.create(db, email="user1@example.com")
    user2 = await UserFactory.create(db, email="user2@example.com")
    
    users = await get_all_users(db)
    assert len(users) == 2
```

## Testing Best Practices

### DO ✅

- Write descriptive test names
- Test one thing per test
- Use fixtures for common setup
- Clean up after tests
- Test edge cases
- Test error conditions
- Use meaningful assertions
- Keep tests independent
- Make tests fast
- Run tests frequently

### DON'T ❌

- Test implementation details
- Write brittle tests
- Use sleeps (use mocking instead)
- Share state between tests
- Ignore flaky tests
- Skip error cases
- Use print for debugging
- Commit failing tests
- Mix unit and integration tests
- Over-mock

## Running Tests

### All Tests

```bash
uv run pytest
```

### Specific Test File

```bash
uv run pytest tests/test_cli.py
```

### Specific Test

```bash
uv run pytest tests/test_cli.py::test_create_project
```

### With Coverage

```bash
uv run pytest --cov=fastapi_smith --cov-report=html
```

### Verbose Output

```bash
uv run pytest -v
```

### Stop on First Failure

```bash
uv run pytest -x
```

### Run Only Failed Tests

```bash
uv run pytest --lf
```

### Parallel Execution

```bash
uv run pytest -n auto
```

## Coverage Requirements

### Check Coverage

```bash
uv run pytest --cov=fastapi_smith --cov-report=term-missing
```

### Coverage Report

```bash
uv run pytest --cov=fastapi_smith --cov-report=html
# Open htmlcov/index.html
```

### Fail on Low Coverage

```bash
uv run pytest --cov=fastapi_smith --cov-fail-under=80
```

## CI Integration

Tests run automatically on:
- Every push
- Every PR
- Before merge

See `.github/workflows/ci.yml`

## Debugging Tests

### Using pytest debugger

```bash
# Drop into debugger on failure
uv run pytest --pdb

# Drop into debugger immediately
uv run pytest --trace
```

### Print debugging

```python
def test_something(capsys):
    print("Debug output")
    result = function_under_test()
    
    captured = capsys.readouterr()
    assert captured.out == "Debug output\n"
```

### Logging in tests

```python
import logging

def test_with_logging(caplog):
    caplog.set_level(logging.INFO)
    
    function_that_logs()
    
    assert "expected message" in caplog.text
```

## Test Documentation

### Docstrings

```python
def test_user_registration_with_invalid_email():
    """
    Test that user registration fails with invalid email.
    
    Given: An invalid email address
    When: User attempts to register
    Then: Registration fails with validation error
    """
    with pytest.raises(ValidationError):
        register_user("invalid-email", "password123")
```

### Comments for Complex Tests

```python
def test_complex_workflow():
    # Setup: Create user with specific permissions
    user = create_user_with_permissions(["read", "write"])
    
    # Test: User can read resource
    resource = get_resource(user, resource_id=1)
    assert resource is not None
    
    # Test: User can update resource
    update_resource(user, resource_id=1, data={"name": "updated"})
    
    # Verify: Resource was updated
    updated = get_resource(user, resource_id=1)
    assert updated.name == "updated"
```

## Common Testing Mistakes

❌ **Testing implementation details**
```python
# Bad
def test_internal_cache_structure():
    cache = Cache()
    assert isinstance(cache._storage, dict)
```

✅ **Test behavior**
```python
# Good
def test_cache_stores_and_retrieves_values():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

❌ **Fragile tests**
```python
# Bad - breaks if order changes
assert users == [user1, user2, user3]
```

✅ **Robust assertions**
```python
# Good
assert len(users) == 3
assert user1 in users
assert user2 in users
```

## Questions?

If unsure about testing approach:
1. Check this guide
2. Look at existing tests
3. Ask in PR discussion

**Remember: Good tests are an investment in code quality and confidence.**
