---
inclusion: always
---

# Coding Standards & Rules

## Naming Conventions

### Files
- Test files: `test_[action]_[subject].py` (e.g., `test_create_account.py`)
- Page objects: `[page_name]_page.py` (e.g., `login_page.py`)
- Utilities: `[purpose]_helper.py` or `[purpose]_utils.py`
- All filenames: `snake_case` only. No hyphens, spaces, or uppercase.

### Classes
- Page objects: `UpperCamelCase` ending with `Page` (e.g., `LoginPage`)
- Test classes: `UpperCamelCase` starting with `Test` (e.g., `TestAccountCRUD`)
- Clients: `UpperCamelCase` ending with `Client` (e.g., `SalesforceClient`)

### Functions
- Test functions: `test_[action]_[condition]_[expected]` (e.g., `test_create_account_with_valid_data`)
- Helper functions: `snake_case` descriptive verbs (e.g., `navigate_to_dashboard`)
- Fixtures: `snake_case` nouns (e.g., `sf_client`, `boomi_client`)

### Variables
- Local variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes: `_leading_underscore`

## Test Structure Rules

### AAA Pattern (Arrange-Act-Assert)
Every test must follow this structure:
```python
def test_create_account(self, sf_client, sf_cleanup, unique_id):
    # Arrange
    account_name = f"Test Account {unique_id}"

    # Act
    result = sf_client.create("Account", {"Name": account_name})
    sf_cleanup("Account", result["id"])

    # Assert
    assert result["success"] is True
```

### One Behavior Per Test
- Each test validates ONE thing
- Multiple assertions are OK if they validate the same behavior
- Split complex flows into multiple tests

### Test Independence
- Tests must not depend on other tests
- Each test creates its own data
- Each test cleans up after itself
- Use fixtures with `yield` for automatic cleanup

### No Hardcoded Data
- Use `unique_id` fixture for unique identifiers
- Use `.env` for credentials and URLs
- Use `test_data/` files for static test data
- Use `Faker` for dynamic test data

## Code Quality Rules

### Imports
- Standard library first, then third-party, then local
- One import per line for clarity
- No wildcard imports (`from module import *`)

### Error Handling
- Never use bare `except:` — always catch specific exceptions
- Log errors with context before re-raising
- Use `pytest.skip()` when prerequisites are missing

### Logging
- Use `logging` module, not `print()`
- Log at appropriate levels: INFO for actions, WARNING for issues, ERROR for failures
- Include context in log messages (IDs, names, values)

### Documentation
- Every test function must have a docstring
- Every page object class must have a docstring
- Every fixture must have a docstring explaining what it provides

## Domain-Specific Rules

### E-commerce Tests
- Use `BasePageSelenium` or `BasePagePlaywright` for UI tests
- Pass `base_url=driver.base_url` when creating page objects
- Use flexible selector strategies with fallbacks
- Mark with `@pytest.mark.ecommerce`

### Salesforce Tests
- Always use `sf_cleanup` fixture for created records
- Use `unique_id` in record names to avoid conflicts
- Query with LIMIT to avoid governor limits
- Mark with `@pytest.mark.salesforce_crm` or `@pytest.mark.loyalty`

### Boomi Tests
- Set reasonable timeouts for process execution (default 300s)
- Check Atom status before running process tests
- Mark with `@pytest.mark.boomi`

### Integration Tests
- Mark with `@pytest.mark.integration` and `@pytest.mark.e2e`
- Document the full flow in the test docstring
- Use longer timeouts for cross-system flows
- Clean up in reverse order of creation

## Fixture Rules

### Scope Guidelines
- `session`: Clients, config, authentication (expensive setup)
- `function`: Drivers, test data, cleanup helpers (test isolation)
- `module`: Shared data within a test file (rare)

### Cleanup Pattern
```python
@pytest.fixture(scope="function")
def my_fixture():
    # Setup
    resource = create_resource()
    yield resource
    # Teardown (always runs)
    resource.cleanup()
```

### Skip Pattern
```python
@pytest.fixture(scope="session")
def sf_client():
    if not os.environ.get('SF_CLIENT_ID'):
        pytest.skip("Salesforce not configured")
    # ... setup
```

## Marker Usage

### Required Markers
Every test must have at least ONE domain marker:
- `@pytest.mark.ecommerce`
- `@pytest.mark.salesforce_crm`
- `@pytest.mark.loyalty`
- `@pytest.mark.boomi`
- `@pytest.mark.api`

### Optional Markers
- `@pytest.mark.smoke` — Critical path tests (run on every PR)
- `@pytest.mark.regression` — Full regression suite
- `@pytest.mark.integration` — Cross-domain tests
- `@pytest.mark.e2e` — End-to-end flows

## Pull Request Checklist

Before submitting a PR, verify:
- [ ] All tests pass locally
- [ ] No credentials in code (use .env)
- [ ] Tests have docstrings
- [ ] Tests have domain markers
- [ ] Tests clean up after themselves
- [ ] No `time.sleep()` in tests
- [ ] No `print()` — use `logging`
- [ ] No hardcoded test data
- [ ] Allure report generates correctly
