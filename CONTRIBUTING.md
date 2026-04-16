# Contributing to Test Automation Framework

Thank you for your interest in contributing to the Test Automation Framework! This guide will help you add tests, update configuration, and submit changes following our team conventions.

## Table of Contents

- [Getting Started](#getting-started)
- [Adding New Tests](#adding-new-tests)
- [Updating Configuration](#updating-configuration)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Kiro IDE Integration](#kiro-ide-integration)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. Cloned the repository and set up your development environment (see [README.md](README.md))
2. Created a virtual environment and installed dependencies
3. Verified that example tests pass on your machine

### Development Workflow

1. Create a feature branch from `main`
2. Make your changes (add tests, update config, etc.)
3. Run tests locally to verify changes
4. Commit changes with descriptive messages
5. Push branch and open a pull request
6. Address review feedback
7. Merge after approval

---

## Adding New Tests

### Test Location

- **Selenium tests**: Place in `tests/selenium/`
- **Playwright tests**: Place in `tests/playwright/`

### Test Naming Convention

Use descriptive names that follow the pattern:

```
test_<feature>_<scenario>_<expected_result>.py
```

**Examples**:
- `test_login_valid_credentials_success.py`
- `test_checkout_empty_cart_shows_error.py`
- `test_search_no_results_displays_message.py`

### Selenium Test Template

```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.selenium
def test_feature_scenario_result(selenium_driver):
    """
    Test description: What this test validates.
    
    Steps:
    1. Navigate to page
    2. Perform action
    3. Verify result
    """
    driver = selenium_driver
    
    # Navigate
    driver.get("https://example.com/page")
    
    # Interact
    element = driver.find_element(By.ID, "element-id")
    element.click()
    
    # Assert
    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.presence_of_element_located((By.ID, "result-id")))
    assert "Expected Text" in result.text
```

### Playwright Test Template

```python
import pytest
from playwright.sync_api import expect

@pytest.mark.playwright
def test_feature_scenario_result(playwright_page):
    """
    Test description: What this test validates.
    
    Steps:
    1. Navigate to page
    2. Perform action
    3. Verify result
    """
    page = playwright_page
    
    # Navigate
    page.goto("https://example.com/page")
    
    # Interact
    page.click("#element-id")
    
    # Assert
    expect(page.locator("#result-id")).to_contain_text("Expected Text")
```

### Test Conventions

1. **One assertion per test**: Keep tests focused on a single behavior
2. **Use descriptive docstrings**: Explain what the test validates and key steps
3. **Use appropriate markers**: Add `@pytest.mark.selenium` or `@pytest.mark.playwright`
4. **Add custom markers**: Use `@pytest.mark.smoke` or `@pytest.mark.regression` for filtering
5. **Use Page Object Model**: For complex pages, create page objects in `tests/<driver>/pages/`
6. **Avoid hardcoded waits**: Use explicit waits (Selenium) or auto-waiting (Playwright)
7. **Clean up test data**: Ensure tests don't leave side effects

### Adding Custom Markers

To add a new marker, update `pytest.ini`:

```ini
markers =
    selenium: Selenium WebDriver tests
    playwright: Playwright tests
    smoke: Smoke tests for quick validation
    regression: Full regression suite
    your_marker: Description of your marker
```

### Page Object Model Example

```python
# tests/selenium/pages/login_page.py
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.submit_button = (By.ID, "submit")
    
    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.submit_button).click()

# tests/selenium/test_login.py
import pytest
from tests.selenium.pages.login_page import LoginPage

@pytest.mark.selenium
def test_login_valid_credentials_success(selenium_driver):
    """Test successful login with valid credentials."""
    driver = selenium_driver
    driver.get("https://example.com/login")
    
    login_page = LoginPage(driver)
    login_page.login("testuser", "password123")
    
    assert "Dashboard" in driver.title
```

---

## Updating Configuration

### config.yaml

The `config.yaml` file contains default values for test execution. Update this file to change:

- Base URL for the application under test
- Default browser (chrome, firefox, chromium, webkit)
- Headless mode (true/false)
- Timeouts and wait durations
- Parallel worker count
- Report output directory

**Example**:

```yaml
base_url: "https://staging.example.com"
browser: "firefox"
headless: true
timeout: 45
parallel_workers: 4
```

### pytest.ini

The `pytest.ini` file configures pytest behavior. Update this file to:

- Add new test markers
- Change report output paths
- Modify test discovery patterns
- Adjust logging levels
- Set default command-line options

**Example - Adding a new marker**:

```ini
markers =
    selenium: Selenium WebDriver tests
    playwright: Playwright tests
    smoke: Smoke tests for quick validation
    regression: Full regression suite
    api: API integration tests
```

### Framework Components

To modify framework behavior, update files in the `framework/` directory:

- `config.py`: Configuration loading logic
- `selenium_driver.py`: Selenium WebDriver initialization
- `playwright_driver.py`: Playwright browser initialization
- `report_utils.py`: Report generation utilities

**Important**: When modifying framework components, add unit tests in `tests/test_<component>.py`.

---

## Submitting Pull Requests

### Branch Naming

Use descriptive branch names that indicate the type of change:

- `feature/<description>` - New features or tests
- `fix/<description>` - Bug fixes
- `docs/<description>` - Documentation updates
- `refactor/<description>` - Code refactoring

**Examples**:
- `feature/add-checkout-tests`
- `fix/selenium-timeout-issue`
- `docs/update-readme-setup`

### Commit Messages

Write clear, concise commit messages:

```
<type>: <short description>

<optional detailed description>

<optional footer>
```

**Types**:
- `feat`: New feature or test
- `fix`: Bug fix
- `docs`: Documentation change
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: add login tests for Selenium

- Add test for valid credentials
- Add test for invalid credentials
- Add test for empty fields

Closes #123
```

```
fix: resolve Playwright timeout in checkout test

The checkout test was timing out due to slow page load.
Increased timeout from 30s to 60s and added explicit wait.
```

### Pull Request Description

Use this template for pull request descriptions:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New tests
- [ ] Bug fix
- [ ] Configuration update
- [ ] Documentation update
- [ ] Framework enhancement

## Changes Made
- List key changes
- Include file paths if relevant

## Testing
- [ ] All existing tests pass
- [ ] New tests added and passing
- [ ] Tested locally with Selenium
- [ ] Tested locally with Playwright
- [ ] Tested in Docker (if applicable)

## Screenshots (if applicable)
Add screenshots of test reports or UI changes.

## Related Issues
Closes #<issue-number>
```

### Pull Request Checklist

Before submitting a pull request:

- [ ] Code follows style guidelines (see [Code Style Guidelines](#code-style-guidelines))
- [ ] All tests pass locally (`pytest`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (README, CONTRIBUTING, etc.)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with `main`
- [ ] No merge conflicts

### Review Process

1. Submit pull request with descriptive title and description
2. Automated CI checks run (GitHub Actions)
3. Team member reviews code
4. Address feedback and push updates
5. Approval and merge by maintainer

---

## Code Style Guidelines

### Python Style (PEP 8)

Follow [PEP 8](https://pep8.org/) style guidelines:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use snake_case for functions and variables
- Use PascalCase for classes
- Add blank lines between functions and classes

### Docstrings

Use docstrings for all test functions, classes, and modules:

```python
def test_login_success(selenium_driver):
    """
    Test successful login with valid credentials.
    
    Steps:
    1. Navigate to login page
    2. Enter valid username and password
    3. Click submit button
    4. Verify redirect to dashboard
    """
    # Test implementation
```

### Type Hints

Use type hints for function parameters and return values:

```python
from typing import Optional
from selenium import webdriver

def initialize_driver(browser: str, headless: bool = False) -> webdriver.Remote:
    """Initialize WebDriver with specified browser."""
    # Implementation
```

### Imports

Organize imports in this order:

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import os
from typing import Optional

import pytest
from selenium import webdriver

from framework.config import Config
```

### Naming Conventions

- **Test files**: `test_<feature>.py`
- **Test functions**: `test_<action>_<result>`
- **Fixtures**: `<driver>_driver`, `<driver>_page`
- **Page objects**: `<PageName>Page` (e.g., `LoginPage`)
- **Utility functions**: `<verb>_<noun>` (e.g., `parse_json_report`)

---

## Testing Guidelines

### Unit Tests for Framework Code

When modifying framework components, add unit tests:

```python
# tests/test_config.py
import pytest
from framework.config import Config

def test_config_loads_yaml_file():
    """Test that Config loads values from config.yaml."""
    config = Config()
    assert config.base_url is not None
    assert config.browser in ["chrome", "firefox", "chromium", "webkit"]

def test_config_get_with_default():
    """Test that Config.get returns default when key missing."""
    config = Config()
    assert config.get("nonexistent_key", "default_value") == "default_value"
```

### Integration Tests

Integration tests validate end-to-end workflows:

```python
# tests/test_runner_integration.py
import pytest
import subprocess

def test_pytest_runs_selenium_tests():
    """Test that pytest can discover and run Selenium tests."""
    result = subprocess.run(
        ["pytest", "-m", "selenium", "--collect-only"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "test_example_selenium.py" in result.stdout
```

### Test Coverage

Aim for high test coverage on framework components:

- Configuration loading: 100%
- Driver initialization: 100%
- Report generation: 100%
- Fixtures: 100%

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/test_*.py

# Run with coverage
pytest --cov=framework --cov-report=html
```

---

## Kiro IDE Integration

### Steering Files

Steering files provide contextual guidance to the Kiro AI agent. When adding new features, consider updating:

- `.kiro/steering/test-writing-guide.md` - Test authoring conventions
- `.kiro/steering/framework-overview.md` - Framework structure and usage
- `.kiro/steering/docker-execution.md` - Docker build and execution

### Hooks

Hooks automate repetitive tasks. Current hooks:

- `test-file-review.json` - Reviews test files for convention violations
- `report-summary.json` - Summarizes test execution reports
- `scaffold-test.json` - Scaffolds new test files with correct structure

To add a new hook, create a JSON file in `.kiro/hooks/`:

```json
{
  "id": "my-hook",
  "name": "My Hook",
  "description": "Description of what the hook does",
  "eventType": "fileEdited",
  "filePatterns": "tests/**/*.py",
  "hookAction": "askAgent",
  "outputPrompt": "Prompt for the AI agent"
}
```

---

## Questions or Issues?

If you have questions or encounter issues:

1. Check the [README.md](README.md) for setup and usage instructions
2. Review this contributing guide
3. Check existing issues in the GitHub repository
4. Open a new issue using the pilot feedback template

Thank you for contributing to the Test Automation Framework! 🚀
