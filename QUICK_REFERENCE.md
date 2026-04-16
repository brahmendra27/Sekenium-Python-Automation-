# Test Automation Framework - Quick Reference Card

## 🚀 Creating a New Project

```bash
# Create new project
python scripts/create_new_project.py my_project

# What it creates:
# projects/my_project/
# ├── config.yaml
# ├── pages/
# ├── tests/
# ├── test_data/
# └── reports/
```

---

## 📝 Writing Page Objects

### Selenium Page Object

```python
from selenium.webdriver.common.by import By
from framework.base_page import BasePageSelenium
import allure

class HomePage(BasePageSelenium):
    # Locators
    LOGO = (By.CSS_SELECTOR, ".logo")
    SEARCH_BOX = (By.ID, "search")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com"
    
    @allure.step("Open homepage")
    def open(self):
        self.navigate_to(self.url)
        return self
    
    @allure.step("Search for: {query}")
    def search(self, query):
        self.type(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)
        return self
```

### Playwright Page Object

```python
from framework.base_page import BasePagePlaywright
import allure

class HomePage(BasePagePlaywright):
    # Selectors
    LOGO = ".logo"
    SEARCH_BOX = "#search"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://example.com"
    
    @allure.step("Open homepage")
    def open(self):
        self.navigate_to(self.url)
        return self
    
    @allure.step("Search for: {query}")
    def search(self, query):
        self.type(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)
        return self
```

---

## 🧪 Writing Tests

### Selenium Test

```python
import pytest
import allure
from projects.my_project.pages.home_page import HomePage

@allure.epic("My App")
@allure.feature("Homepage")
@pytest.mark.selenium
@pytest.mark.my_project
def test_homepage_loads(selenium_driver):
    """Test homepage loads successfully."""
    home_page = HomePage(selenium_driver)
    home_page.open()
    
    assert home_page.is_visible(home_page.LOGO)
```

### Playwright Test

```python
import pytest
import allure
from projects.my_project.pages.home_page import HomePage

@allure.epic("My App")
@allure.feature("Homepage")
@pytest.mark.playwright
@pytest.mark.my_project
def test_homepage_loads(playwright_page):
    """Test homepage loads successfully."""
    home_page = HomePage(playwright_page)
    home_page.open()
    
    assert home_page.is_visible(home_page.LOGO)
```

---

## 🏃 Running Tests

```bash
# Run all tests for a project
pytest projects/my_project/tests/

# Run Selenium tests only
pytest projects/my_project/tests/selenium/

# Run Playwright tests only
pytest projects/my_project/tests/playwright/

# Run with marker
pytest -m my_project

# Run specific test
pytest projects/my_project/tests/selenium/test_homepage.py

# Run with Allure
pytest projects/my_project/tests/ --alluredir=projects/my_project/reports/allure-results
allure serve projects/my_project/reports/allure-results

# Run in headless mode
pytest projects/my_project/tests/ --headless

# Run with different browser
pytest projects/my_project/tests/ --browser=firefox

# Run in parallel
pytest projects/my_project/tests/ -n 4
```

---

## 🛠️ Base Page Methods

### Common Methods (Both Selenium & Playwright)

```python
# Navigation
page.navigate_to(url)
page.get_current_url()
page.get_page_title()

# Element Interaction
page.click(locator)
page.type(locator, text)
page.get_text(locator)
page.get_attribute(locator, attribute)

# Visibility Checks
page.is_visible(locator)
page.element_exists(locator)

# Waiting
page.wait_for_selector(selector)
page.wait_for_element_to_disappear(locator)
page.wait_for_page_load()

# Scrolling
page.scroll_to_element(locator)

# Screenshots (Playwright only)
page.take_screenshot(name="screenshot")
```

---

## 📊 Allure Decorators

```python
import allure

# Epic (highest level)
@allure.epic("E-Commerce")

# Feature (mid level)
@allure.feature("Shopping Cart")

# Story (specific functionality)
@allure.story("Add to Cart")

# Severity
@allure.severity(allure.severity_level.CRITICAL)
# Options: BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL

# Tags
@allure.tag("smoke", "regression", "cart")

# Steps
@allure.step("Navigate to product page")
def navigate_to_product():
    pass

# Attachments
allure.attach(data, name="Screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach(text, name="Log", attachment_type=allure.attachment_type.TEXT)
```

---

## 🎯 Pytest Markers

```python
# Driver type
@pytest.mark.selenium
@pytest.mark.playwright

# Test type
@pytest.mark.smoke
@pytest.mark.regression

# Project
@pytest.mark.my_project
@pytest.mark.automation_test_store

# Custom markers (add to pytest.ini)
@pytest.mark.slow
@pytest.mark.api
@pytest.mark.integration
```

---

## 📁 Project Structure

```
projects/my_project/
├── config.yaml              # Project configuration
├── pages/                   # Page Objects
│   ├── __init__.py
│   ├── home_page.py
│   ├── product_page.py
│   └── cart_page.py
├── tests/                   # Tests
│   ├── __init__.py
│   ├── conftest.py          # Project fixtures
│   ├── selenium/
│   │   ├── __init__.py
│   │   ├── test_homepage.py
│   │   └── test_cart.py
│   └── playwright/
│       ├── __init__.py
│       ├── test_homepage.py
│       └── test_cart.py
├── test_data/               # Test data
│   ├── users.json
│   └── products.csv
└── reports/                 # Generated reports
    ├── allure-results/
    ├── csv/
    └── screenshots/
```

---

## ⚙️ Configuration

### Project Config (projects/my_project/config.yaml)

```yaml
project_name: "My Project"
base_url: "https://example.com"
browser: "chrome"
headless: false
timeout: 30

test_users:
  - email: "test@example.com"
    password: "Test123!"

report_dir: "projects/my_project/reports"
```

### CLI Overrides

```bash
# Override browser
pytest --browser=firefox

# Override headless
pytest --headless

# Override base URL
pytest --base-url=https://staging.example.com
```

---

## 🔧 Fixtures

### Built-in Fixtures

```python
# Selenium
def test_example(selenium_driver):
    driver = selenium_driver
    # Use driver

# Playwright
def test_example(playwright_page):
    page = playwright_page
    # Use page

# Project config
def test_example(project_config):
    base_url = project_config['base_url']
    # Use config

# Test user
def test_example(test_user):
    email = test_user['email']
    # Use user data
```

### Custom Fixtures (in conftest.py)

```python
import pytest

@pytest.fixture
def logged_in_user(selenium_driver):
    """Fixture that logs in a user."""
    # Login logic
    yield selenium_driver
    # Logout logic
```

---

## 📊 CSV Logging

```python
from framework.csv_logger import CSVLogger

# Initialize logger
logger = CSVLogger("projects/my_project/reports/csv")

# Log registration
logger.log_registration(
    test_name="test_user_registration",
    email="test@example.com",
    first_name="John",
    last_name="Doe",
    status="success"
)

# Log validation
logger.log_validation(
    test_name="test_cart_total",
    validation_type="price_calculation",
    expected="49.99",
    actual="49.99",
    status="pass"
)
```

---

## 🐳 Docker

```bash
# Build image
docker build -t test-framework -f docker/Dockerfile .

# Run tests
docker-compose -f docker/docker-compose.yml up

# Run specific project
docker run test-framework pytest projects/my_project/tests/
```

---

## 🤖 AI-Assisted Test Creation

### Using Prompts

```
"Create a Playwright test for user login with valid credentials"

"Write a Selenium test to verify shopping cart total calculation"

"Generate tests for product search functionality"

"Create a test suite for user registration with validation"
```

### What AI Generates

✅ Correct imports
✅ Proper fixtures
✅ Appropriate markers
✅ Allure decorations
✅ Page Object usage
✅ Best practices

---

## 🔍 Common Locator Strategies

### Selenium

```python
from selenium.webdriver.common.by import By

# ID (best)
ELEMENT = (By.ID, "element-id")

# CSS Selector
ELEMENT = (By.CSS_SELECTOR, ".class-name")
ELEMENT = (By.CSS_SELECTOR, "#id-name")
ELEMENT = (By.CSS_SELECTOR, "[data-testid='value']")

# XPath (last resort)
ELEMENT = (By.XPATH, "//div[@class='example']")

# Link Text
ELEMENT = (By.LINK_TEXT, "Click Here")
```

### Playwright

```python
# ID
ELEMENT = "#element-id"

# CSS Selector
ELEMENT = ".class-name"
ELEMENT = "[data-testid='value']"

# Text content
ELEMENT = "text=Click Here"

# Role
ELEMENT = "role=button[name='Submit']"
```

---

## 📚 Documentation

- **MULTI_PROJECT_STRUCTURE_GUIDE.md** - Complete guide
- **FRAMEWORK_FEATURES_HIGHLIGHTS.md** - Feature showcase
- **MULTI_PROJECT_SETUP_COMPLETE.md** - Setup summary
- **projects/_template/README.md** - Template guide

---

## 💡 Tips

### Page Objects
- One page = one class
- Define locators at top
- Use base class methods
- Return self or next page
- Add Allure steps

### Tests
- Use page objects
- Follow AAA pattern
- One assertion per test
- Descriptive names
- Add markers

### Best Practices
- Keep projects independent
- Use project config
- Organize test data
- Generate reports per project
- Version control everything

---

*Quick Reference v1.0 - April 16, 2026*
