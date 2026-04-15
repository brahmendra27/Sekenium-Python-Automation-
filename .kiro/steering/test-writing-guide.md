---
title: Test Writing Guide
description: Guide for writing Selenium and Playwright tests in the Test Automation Framework
inclusion: auto
keywords: [test, selenium, playwright, write test, create test, test automation, browser test, ui test]
---

# Test Writing Guide

## Overview

This guide describes conventions and best practices for writing automated browser tests in the Test Automation Framework. The framework supports both Selenium WebDriver and Playwright for browser automation, unified under pytest as the test runner.

Use this guide when creating new tests, reviewing test code, or helping team members follow framework conventions.

---

## Test Structure

### Selenium Tests

**Location**: `tests/selenium/`

**Naming Convention**: `test_<feature>_<scenario>.py`
- Example: `test_login_success.py`, `test_checkout_invalid_card.py`

**Required Fixture**: `selenium_driver`
- Provides initialized WebDriver instance
- Automatically handles browser setup and teardown
- Captures screenshots on test failure
- Configured via `config.yaml` (browser, headless mode, timeouts)

**Required Marker**: `@pytest.mark.selenium`
- Enables filtering: `pytest -m selenium`
- Identifies tests as Selenium-based in reports

**Example Selenium Test**:

```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.selenium
def test_login_success(selenium_driver):
    """Test successful user login with valid credentials.
    
    Verifies that a user can log in with valid username and password,
    and is redirected to the dashboard page.
    """
    driver = selenium_driver
    
    # Navigate to login page
    driver.get("https://example.com/login")
    
    # Fill in login form
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    
    # Submit form
    driver.find_element(By.ID, "submit").click()
    
    # Wait for navigation to dashboard
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_contains("Dashboard"))
    
    # Verify successful login
    assert "Dashboard" in driver.title
    assert "/dashboard" in driver.current_url
```

**Selenium Best Practices**:

1. **Use Explicit Waits**: Prefer `WebDriverWait` with `expected_conditions` over `time.sleep()`
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
   ```

2. **Locator Strategy Priority**:
   - ID (most reliable): `By.ID`
   - CSS Selector: `By.CSS_SELECTOR`
   - XPath (last resort): `By.XPATH`

3. **Element Interaction**:
   - Always verify element is displayed before interaction
   - Use `is_displayed()`, `is_enabled()` for state checks
   - Clear input fields before entering text: `element.clear()`

4. **Navigation**:
   - Use `driver.get()` for initial navigation
   - Use `driver.back()`, `driver.forward()` for browser controls
   - Verify URL after navigation: `assert "expected" in driver.current_url`

---

### Playwright Tests

**Location**: `tests/playwright/`

**Naming Convention**: `test_<feature>_<scenario>.py`
- Example: `test_login_success.py`, `test_checkout_invalid_card.py`

**Required Fixture**: `playwright_page`
- Provides initialized Playwright Page instance
- Automatically handles browser context setup and teardown
- Captures screenshots and traces on test failure
- Configured via `config.yaml` (browser, headless mode, tracing)

**Required Marker**: `@pytest.mark.playwright`
- Enables filtering: `pytest -m playwright`
- Identifies tests as Playwright-based in reports

**Example Playwright Test**:

```python
import pytest
from playwright.sync_api import expect


@pytest.mark.playwright
def test_login_success(playwright_page):
    """Test successful user login with valid credentials.
    
    Verifies that a user can log in with valid username and password,
    and is redirected to the dashboard page.
    """
    page = playwright_page
    
    # Navigate to login page
    page.goto("https://example.com/login")
    
    # Fill in login form
    page.fill("#username", "testuser")
    page.fill("#password", "password123")
    
    # Submit form
    page.click("#submit")
    
    # Verify successful login
    expect(page).to_have_title("Dashboard")
    expect(page).to_have_url("**/dashboard")
```

**Playwright Best Practices**:

1. **Use Auto-Waiting**: Playwright automatically waits for elements to be actionable
   ```python
   # No explicit wait needed - Playwright waits automatically
   page.click("#submit")
   ```

2. **Use Playwright's Expect API**: Prefer `expect()` over standard assertions
   ```python
   from playwright.sync_api import expect
   
   # Good: Auto-retrying assertion
   expect(page.locator("h1")).to_have_text("Welcome")
   
   # Avoid: No auto-retry
   assert page.locator("h1").text_content() == "Welcome"
   ```

3. **Locator Strategy**:
   - CSS Selector: `page.locator("button.submit")`
   - Text content: `page.locator("text=Submit")`
   - Role-based: `page.get_by_role("button", name="Submit")`
   - Test ID: `page.get_by_test_id("submit-btn")`

4. **Element Interaction**:
   - Fill inputs: `page.fill("#input", "value")`
   - Click elements: `page.click("button")`
   - Select options: `page.select_option("#dropdown", "value")`
   - Check/uncheck: `page.check("#checkbox")`, `page.uncheck("#checkbox")`

5. **Navigation**:
   - Navigate: `page.goto("https://example.com")`
   - Wait for navigation: `page.wait_for_url("**/expected-path")`
   - Wait for load state: `page.wait_for_load_state("networkidle")`

---

## Test Conventions

### 1. Test Naming

**Function Names**: `test_<action>_<expected_result>`

Examples:
- `test_login_success` - Tests successful login
- `test_login_invalid_credentials` - Tests login with invalid credentials
- `test_checkout_empty_cart` - Tests checkout with empty cart
- `test_search_no_results` - Tests search with no matching results

**File Names**: `test_<feature>_<scenario>.py`

Examples:
- `test_login.py` - Contains all login-related tests
- `test_checkout.py` - Contains all checkout-related tests
- `test_search.py` - Contains all search-related tests

### 2. Docstrings

**Required**: Every test function must have a docstring explaining:
- What the test does
- What it verifies
- Any important preconditions or setup

**Format**:
```python
def test_example(selenium_driver):
    """Brief one-line summary of what the test does.
    
    Optional longer description explaining:
    - Test scenario steps
    - Expected behavior
    - Any special conditions or data requirements
    """
    # Test implementation
```

### 3. Assertions

**Best Practices**:
- Use descriptive assertion messages
- One primary assertion per test (when possible)
- Verify expected state, not just absence of errors

**Examples**:

```python
# Good: Descriptive message
assert "Dashboard" in driver.title, f"Expected 'Dashboard' in title, got: {driver.title}"

# Good: Playwright expect with auto-retry
expect(page.locator("h1")).to_have_text("Welcome")

# Avoid: No context on failure
assert "Dashboard" in driver.title
```

### 4. Page Object Model (POM)

For complex pages with many elements and interactions, use the Page Object Model pattern:

**Page Object Example**:

```python
# pages/login_page.py
from selenium.webdriver.common.by import By


class LoginPage:
    """Page Object for login page."""
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example.com/login"
        
        # Locators
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.submit_button = (By.ID, "submit")
        self.error_message = (By.CLASS_NAME, "error")
    
    def navigate(self):
        """Navigate to login page."""
        self.driver.get(self.url)
    
    def login(self, username, password):
        """Perform login with given credentials."""
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.submit_button).click()
    
    def get_error_message(self):
        """Get error message text if displayed."""
        return self.driver.find_element(*self.error_message).text
```

**Using Page Object in Test**:

```python
@pytest.mark.selenium
def test_login_invalid_credentials(selenium_driver):
    """Test login fails with invalid credentials."""
    login_page = LoginPage(selenium_driver)
    
    login_page.navigate()
    login_page.login("invalid_user", "wrong_password")
    
    error = login_page.get_error_message()
    assert "Invalid credentials" in error
```

### 5. Test Markers

Use pytest markers to categorize and filter tests:

**Built-in Markers**:
- `@pytest.mark.selenium` - Selenium WebDriver tests
- `@pytest.mark.playwright` - Playwright tests
- `@pytest.mark.smoke` - Quick smoke tests for critical functionality
- `@pytest.mark.regression` - Full regression suite tests

**Usage**:
```python
@pytest.mark.selenium
@pytest.mark.smoke
def test_login_success(selenium_driver):
    """Critical smoke test for login functionality."""
    # Test implementation
```

**Running Tests by Marker**:
```bash
# Run only smoke tests
pytest -m smoke

# Run Selenium smoke tests
pytest -m "selenium and smoke"

# Run all tests except regression
pytest -m "not regression"
```

### 6. Test Data

**Best Practices**:
- Use fixtures for reusable test data
- Avoid hardcoding sensitive data (use environment variables or config)
- Use descriptive variable names for test data

**Example**:
```python
@pytest.fixture
def valid_user_credentials():
    """Provide valid user credentials for testing."""
    return {
        "username": "testuser",
        "password": "Test123!",
        "email": "testuser@example.com"
    }


@pytest.mark.selenium
def test_login_success(selenium_driver, valid_user_credentials):
    """Test login with valid credentials."""
    driver = selenium_driver
    driver.get("https://example.com/login")
    
    driver.find_element(By.ID, "username").send_keys(valid_user_credentials["username"])
    driver.find_element(By.ID, "password").send_keys(valid_user_credentials["password"])
    driver.find_element(By.ID, "submit").click()
    
    assert "Dashboard" in driver.title
```

---

## Common Patterns

### Handling Dynamic Content

**Selenium**:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for element to be visible
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID, "dynamic-content")))

# Wait for element to be clickable
button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
```

**Playwright**:
```python
# Playwright auto-waits, but you can be explicit
page.locator("#dynamic-content").wait_for(state="visible")

# Or use expect with timeout
expect(page.locator("#dynamic-content")).to_be_visible(timeout=10000)
```

### Handling Multiple Elements

**Selenium**:
```python
# Find all matching elements
elements = driver.find_elements(By.CLASS_NAME, "item")

# Iterate and verify
for element in elements:
    assert element.is_displayed()
```

**Playwright**:
```python
# Get all matching elements
items = page.locator(".item").all()

# Iterate and verify
for item in items:
    expect(item).to_be_visible()

# Or verify count
expect(page.locator(".item")).to_have_count(5)
```

### Handling Alerts and Dialogs

**Selenium**:
```python
from selenium.webdriver.common.alert import Alert

# Switch to alert and accept
alert = Alert(driver)
alert.accept()

# Get alert text before accepting
alert_text = alert.text
alert.accept()
```

**Playwright**:
```python
# Handle dialog with event listener
page.on("dialog", lambda dialog: dialog.accept())

# Or handle inline
page.click("#trigger-alert")
# Dialog is automatically handled by listener
```

### Taking Screenshots

**Selenium** (automatic on failure via fixture):
```python
# Manual screenshot if needed
driver.save_screenshot("screenshot.png")
```

**Playwright** (automatic on failure via fixture):
```python
# Manual screenshot if needed
page.screenshot(path="screenshot.png")
```

---

## Configuration

Tests are configured via `config.yaml` in the project root:

```yaml
# Base URL for application under test
base_url: "https://example.com"

# Browser selection: chrome, firefox (Selenium); chromium, firefox, webkit (Playwright)
browser: "chrome"

# Headless mode: true for CI, false for local debugging
headless: true

# Default timeout for element waits (seconds)
timeout: 30

# Selenium-specific settings
selenium:
  implicit_wait: 10
  page_load_timeout: 60

# Playwright-specific settings
playwright:
  slow_mo: 0  # Slow down operations by N milliseconds
  tracing: true  # Enable tracing on failure
```

**Override via CLI**:
```bash
# Run with specific browser
pytest --browser=firefox

# Run in headless mode
pytest --headless

# Run with custom base URL
pytest --base-url=https://staging.example.com
```

---

## Running Tests

**Run all tests**:
```bash
pytest
```

**Run specific test file**:
```bash
pytest tests/selenium/test_login.py
```

**Run specific test function**:
```bash
pytest tests/selenium/test_login.py::test_login_success
```

**Run by marker**:
```bash
# Run only Selenium tests
pytest -m selenium

# Run only Playwright tests
pytest -m playwright

# Run smoke tests
pytest -m smoke
```

**Run in parallel**:
```bash
# Run with 4 workers
pytest -n 4
```

**Run with custom configuration**:
```bash
# Run Firefox in headless mode
pytest --browser=firefox --headless
```

---

## Troubleshooting

### Common Issues

**Issue**: WebDriver not found or version mismatch
- **Solution**: The framework uses `webdriver-manager` to automatically download drivers. Ensure you have internet connectivity on first run.

**Issue**: Element not found
- **Solution**: Add explicit waits (Selenium) or verify locator (Playwright auto-waits)

**Issue**: Test passes locally but fails in CI
- **Solution**: Ensure headless mode is enabled in CI, check for timing issues, verify base URL configuration

**Issue**: Screenshot not captured on failure
- **Solution**: Verify `reports/screenshots/` directory exists and is writable, check fixture is properly configured

**Issue**: Playwright trace not generated
- **Solution**: Verify `tracing: true` in `config.yaml` under `playwright` section

---

## Additional Resources

- **Framework Documentation**: See `.kiro/steering/framework-overview.md` for project structure and fixtures
- **Docker Execution**: See `.kiro/steering/docker-execution.md` for containerized test execution
- **Selenium Documentation**: https://www.selenium.dev/documentation/
- **Playwright Documentation**: https://playwright.dev/python/
- **pytest Documentation**: https://docs.pytest.org/

---

## Quick Reference

### Selenium Cheat Sheet

```python
# Navigation
driver.get("https://example.com")
driver.back()
driver.forward()
driver.refresh()

# Finding elements
driver.find_element(By.ID, "element-id")
driver.find_element(By.CSS_SELECTOR, ".class-name")
driver.find_elements(By.TAG_NAME, "a")

# Interaction
element.click()
element.send_keys("text")
element.clear()
element.submit()

# Verification
element.is_displayed()
element.is_enabled()
element.is_selected()
element.text
element.get_attribute("href")

# Waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "element-id")))
```

### Playwright Cheat Sheet

```python
# Navigation
page.goto("https://example.com")
page.go_back()
page.go_forward()
page.reload()

# Finding elements
page.locator("#element-id")
page.locator(".class-name")
page.get_by_role("button", name="Submit")
page.get_by_text("Click me")

# Interaction
page.click("#button")
page.fill("#input", "text")
page.select_option("#dropdown", "value")
page.check("#checkbox")

# Verification
from playwright.sync_api import expect

expect(page).to_have_title("Title")
expect(page).to_have_url("**/path")
expect(page.locator("h1")).to_be_visible()
expect(page.locator("h1")).to_have_text("Text")
expect(page.locator(".item")).to_have_count(5)

# Waits (usually not needed - auto-waiting)
page.wait_for_url("**/path")
page.wait_for_load_state("networkidle")
page.locator("#element").wait_for(state="visible")
```

---

**Last Updated**: 2024
**Framework Version**: 0.1.0
