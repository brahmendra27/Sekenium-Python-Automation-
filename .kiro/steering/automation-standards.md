---
inclusion: always
---

# Automation Framework Standards

**Purpose**: This document steers all Kiro agent actions for UI, API, and Database test automation. Every generated test, page object, helper, or script must follow these rules.

**Scope**: Applies to the entire framework. Primary UI tool is **Playwright with Python**. Selenium is allowed for legacy maintenance.

## 1. Core Testing Principles

- **AAA Pattern**: Arrange, Act, Assert. One clear behavior per test.
- **Test Independence**: Every test runs with fresh setup/teardown. No shared state between tests.
- **Data-Driven Testing**: Use `@pytest.mark.parametrize` or external data sources via fixtures.
- **Flakiness Zero Tolerance**: Rely on Playwright's auto-waiting. Avoid `time.sleep()`. Use explicit waits only for custom conditions.
- **Error Handling**: Clear, actionable failure messages. Attach screenshots on failure.
- **Cleanup**: Always teardown test data (use `pytest` fixtures with `yield`).

## 2. Coding Style & Naming

- Follow PEP 8 for formatting.
- **Test Naming**: `snake_case`. Pattern: `test_[action]_[condition]_[expected_result]`
- **Page Objects**: Upper camel case (`LoginPage`, `ProductCatalogPage`).
- **Variables**: `snake_case`. Constants: `UPPER_SNAKE_CASE`.
- **Locators**: Prefer semantic Playwright locators (get_by_role, get_by_test_id, get_by_label).

### Anti-Patterns to Avoid
- Hard-coded credentials or test data. Use environment variables, fixtures, or data files.
- Duplicated code. Extract to reusable page methods or fixtures.
- Fixed sleeps or implicit waits.
- Locators inside test files. All selectors must live in page objects.

## 3. UI Automation Standards (Playwright Primary)

### Page Object Model (POM)
- Each page/component is a separate class inheriting from `BasePagePlaywright`.
- Constructor accepts the `page: Page` object.
- Keep classes focused and under ~200 lines.
- Separate actions from assertions (assertions stay in test functions).

### Locator Strategy (priority order)
1. `page.get_by_role()` (best for accessibility and resilience)
2. `page.get_by_test_id()` (add `data-testid` attributes where possible)
3. `page.get_by_label()`, `page.get_by_placeholder()`, `page.get_by_text()`
4. `page.locator()` only as fallback (with clear comment explaining why)
- Avoid brittle XPath or complex CSS as primary locators.

### Waiting Strategy
- Trust Playwright's built-in auto-waiting for actions and assertions.
- Use `wait_for_element()` or `expect()` sparingly with meaningful timeouts.

### Fixtures
- Use `pytest` fixtures extensively (defined in `conftest.py`).
- Browser/context/page fixtures for lifecycle management.
- Authenticated user fixtures for login flows.

### Best Practices
- Enable parallel execution where tests are independent.
- Enforce screenshot on test failure via conftest hook.
- Run headless in CI, headed only during debugging.

## 4. API Testing Standards

### Service Object Pattern
- API service objects inherit from `APIClient`.
- Each service encapsulates endpoints for a specific domain.
- Use `APIResponse` wrapper for assertions with method chaining.

### Schema Validation
- Use `framework/schema_validator.py` for JSON schema validation.
- Store schemas in `tests/test_data/schemas/` directory.

## 5. Test Data Management

- No hardcoded test data in tests.
- Use project-level test data files under `tests/test_data/`.
- Use `.env` files for environment-specific configuration.
- Use `python-dotenv` for loading environment variables.

## 6. Environment Handling

- Environment-specific data must be configurable via `.env` or `config.yaml`.
- Never commit real credentials.
- Use `.env.example` as a template.

## 7. Reporting

- Use Allure for test reporting.
- Include: Steps, Screenshots, Failure reasons.
- Generate reports with: `pytest --alluredir=reports/allure-results`
- View reports with: `allure serve reports/allure-results`

## 8. Project Structure

```
project/
├── framework/                  # Core framework code
│   ├── base_page.py           # BasePageSelenium + BasePagePlaywright
│   ├── api_client.py          # REST API client
│   ├── config.py              # Configuration loader
│   ├── schema_validator.py    # JSON schema validation
│   ├── selenium_driver.py     # Selenium WebDriver wrapper
│   ├── playwright_driver.py   # Playwright driver wrapper
│   └── mongodb_client.py      # MongoDB client
├── tests/                     # Test suites
│   ├── skechers/             # Skechers staging tests
│   ├── demo_ecommerce/       # Demo e-commerce tests
│   ├── api/                  # API tests
│   └── database/             # Database tests
├── conftest.py               # Root fixtures
├── config.yaml               # Default configuration
├── pytest.ini                # Test runner config
├── requirements.txt          # Dependencies
└── docker/                   # Docker configuration
    └── Dockerfile
```
