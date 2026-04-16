# Multi-Project Test Automation Framework Structure

## Overview

This guide shows how to organize the framework to support **multiple projects** with a clean **Page Object Model** structure that teams can easily adopt and extend.

---

## 🏗️ Recommended Folder Structure

```
test-automation-framework/
│
├── framework/                          # Core framework (shared across all projects)
│   ├── __init__.py
│   ├── config.py                       # Configuration loader
│   ├── selenium_driver.py              # Selenium WebDriver wrapper
│   ├── playwright_driver.py            # Playwright browser wrapper
│   ├── report_utils.py                 # Report generation utilities
│   ├── csv_logger.py                   # CSV logging utility
│   ├── self_healing.py                 # AI self-healing utility
│   └── base_page.py                    # Base Page Object class (NEW)
│
├── projects/                           # All test projects organized here
│   │
│   ├── automation_test_store/          # Project 1: Automation Test Store
│   │   ├── __init__.py
│   │   ├── config.yaml                 # Project-specific config
│   │   ├── pages/                      # Page Objects for this project
│   │   │   ├── __init__.py
│   │   │   ├── base_page.py            # Project base page (optional)
│   │   │   ├── home_page.py
│   │   │   ├── product_page.py
│   │   │   ├── cart_page.py
│   │   │   ├── checkout_page.py
│   │   │   └── account_page.py
│   │   ├── tests/                      # Tests for this project
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py             # Project-specific fixtures
│   │   │   ├── selenium/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_homepage.py
│   │   │   │   ├── test_cart.py
│   │   │   │   └── test_checkout.py
│   │   │   └── playwright/
│   │   │       ├── __init__.py
│   │   │       ├── test_homepage.py
│   │   │       ├── test_cart.py
│   │   │       └── test_checkout.py
│   │   ├── test_data/                  # Test data for this project
│   │   │   ├── users.json
│   │   │   ├── products.json
│   │   │   └── test_accounts.csv
│   │   └── reports/                    # Project-specific reports
│   │       ├── allure-results/
│   │       ├── csv/
│   │       └── screenshots/
│   │
│   ├── skechers_staging/               # Project 2: Skechers Staging
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── home_page.py
│   │   │   ├── product_listing_page.py
│   │   │   ├── product_detail_page.py
│   │   │   └── search_page.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── selenium/
│   │   │   └── playwright/
│   │   ├── test_data/
│   │   └── reports/
│   │
│   ├── internal_portal/                # Project 3: Internal Portal (Example)
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── login_page.py
│   │   │   ├── dashboard_page.py
│   │   │   └── admin_page.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── selenium/
│   │   │   └── playwright/
│   │   ├── test_data/
│   │   └── reports/
│   │
│   └── _template/                      # Template for new projects
│       ├── __init__.py
│       ├── config.yaml.template
│       ├── pages/
│       │   ├── __init__.py
│       │   └── README.md
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py.template
│       │   ├── selenium/
│       │   │   └── __init__.py
│       │   └── playwright/
│       │       └── __init__.py
│       ├── test_data/
│       │   └── README.md
│       └── README.md
│
├── .kiro/                              # Kiro IDE integration
│   ├── hooks/
│   │   ├── test-file-review.kiro.hook
│   │   ├── scaffold-test.kiro.hook
│   │   ├── report-summary.kiro.hook
│   │   └── ai-element-healer.kiro.hook
│   └── steering/
│       ├── test-writing-guide.md
│       ├── framework-overview.md
│       ├── page-object-model-guide.md  # NEW
│       └── multi-project-guide.md      # NEW
│
├── docker/                             # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github/                            # CI/CD
│   └── workflows/
│       ├── test-automation-store.yml   # Project-specific workflow
│       ├── test-skechers.yml           # Project-specific workflow
│       └── test-all-projects.yml       # Run all projects
│
├── scripts/                            # Utility scripts
│   ├── create_new_project.py           # Script to create new project
│   ├── run_project_tests.py            # Run tests for specific project
│   └── generate_reports.py             # Generate consolidated reports
│
├── config.yaml                         # Global framework config
├── pytest.ini                          # Global pytest config
├── requirements.txt                    # Python dependencies
├── README.md                           # Main documentation
├── MULTI_PROJECT_STRUCTURE_GUIDE.md    # This guide
└── .gitignore
```

---

## 🎯 Key Design Principles

### 1. **Separation of Concerns**
- **Framework**: Core utilities shared across all projects
- **Projects**: Each project is self-contained
- **Tests**: Organized by project and driver type

### 2. **Page Object Model**
- Each project has its own `pages/` directory
- Page objects encapsulate page interactions
- Tests use page objects, not direct element interactions

### 3. **Scalability**
- Easy to add new projects
- No conflicts between projects
- Independent test execution per project

### 4. **Reusability**
- Framework utilities shared
- Template for quick project setup
- Common patterns documented

---

## 📦 Core Framework Components

### Base Page Object Class

Create `framework/base_page.py`:

```python
"""
Base Page Object class with common functionality for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from playwright.sync_api import Page, expect
import allure


class BasePageSelenium:
    """Base class for Selenium Page Objects."""
    
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    @allure.step("Navigate to {url}")
    def navigate_to(self, url):
        """Navigate to a URL."""
        self.driver.get(url)
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator):
        """Find element with wait."""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Find elements: {locator}")
    def find_elements(self, locator):
        """Find multiple elements."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Click element: {locator}")
    def click(self, locator):
        """Click element with wait."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Type '{text}' into {locator}")
    def type(self, locator, text):
        """Type text into element."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Get text from {locator}")
    def get_text(self, locator):
        """Get text from element."""
        return self.find_element(locator).text
    
    @allure.step("Check if element is visible: {locator}")
    def is_visible(self, locator, timeout=None):
        """Check if element is visible."""
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for page to be fully loaded."""
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )


class BasePagePlaywright:
    """Base class for Playwright Page Objects."""
    
    def __init__(self, page: Page, timeout=30000):
        self.page = page
        self.timeout = timeout
    
    @allure.step("Navigate to {url}")
    def navigate_to(self, url):
        """Navigate to a URL."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Click element: {selector}")
    def click(self, selector):
        """Click element."""
        self.page.click(selector, timeout=self.timeout)
    
    @allure.step("Type '{text}' into {selector}")
    def type(self, selector, text):
        """Type text into element."""
        self.page.fill(selector, text, timeout=self.timeout)
    
    @allure.step("Get text from {selector}")
    def get_text(self, selector):
        """Get text from element."""
        return self.page.locator(selector).text_content(timeout=self.timeout)
    
    @allure.step("Check if element is visible: {selector}")
    def is_visible(self, selector, timeout=None):
        """Check if element is visible."""
        try:
            wait_time = timeout or self.timeout
            self.page.locator(selector).wait_for(state="visible", timeout=wait_time)
            return True
        except:
            return False
    
    @allure.step("Wait for selector: {selector}")
    def wait_for_selector(self, selector, state="visible"):
        """Wait for selector to be in specified state."""
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)
    
    @allure.step("Take screenshot")
    def take_screenshot(self, name="screenshot"):
        """Take screenshot and attach to Allure."""
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
```

---

## 🏗️ Project Structure Example

### Project: Automation Test Store

#### 1. Project Config (`projects/automation_test_store/config.yaml`)

```yaml
# Project-specific configuration
project_name: "Automation Test Store"
base_url: "https://automationteststore.com"

# Browser settings
browser: "chrome"
headless: false
timeout: 30

# Test data
test_users:
  - email: "test1@example.com"
    password: "Test123!"
  - email: "test2@example.com"
    password: "Test456!"

# Reporting
report_dir: "projects/automation_test_store/reports"
allure_results_dir: "projects/automation_test_store/reports/allure-results"
csv_dir: "projects/automation_test_store/reports/csv"
```

#### 2. Page Object (`projects/automation_test_store/pages/home_page.py`)

```python
"""
Home Page Object for Automation Test Store.
"""

import allure
from selenium.webdriver.common.by import By
from framework.base_page import BasePageSelenium


class HomePage(BasePageSelenium):
    """Page Object for Automation Test Store homepage."""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, ".logo")
    SEARCH_BOX = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".thumbnail")
    CART_ICON = (By.CSS_SELECTOR, ".cart")
    LOGIN_LINK = (By.LINK_TEXT, "Login or register")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://automationteststore.com"
    
    @allure.step("Open homepage")
    def open(self):
        """Navigate to homepage."""
        self.navigate_to(self.url)
        return self
    
    @allure.step("Search for product: {product_name}")
    def search_product(self, product_name):
        """Search for a product."""
        self.type(self.SEARCH_BOX, product_name)
        self.click(self.SEARCH_BUTTON)
        from .product_page import ProductPage
        return ProductPage(self.driver)
    
    @allure.step("Get featured products count")
    def get_featured_products_count(self):
        """Get number of featured products."""
        products = self.find_elements(self.FEATURED_PRODUCTS)
        return len(products)
    
    @allure.step("Click on featured product at index {index}")
    def click_featured_product(self, index=0):
        """Click on a featured product."""
        products = self.find_elements(self.FEATURED_PRODUCTS)
        products[index].click()
        from .product_page import ProductPage
        return ProductPage(self.driver)
    
    @allure.step("Go to login page")
    def go_to_login(self):
        """Navigate to login page."""
        self.click(self.LOGIN_LINK)
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    @allure.step("Verify homepage is loaded")
    def is_loaded(self):
        """Verify homepage is loaded."""
        return self.is_visible(self.LOGO) and self.is_visible(self.SEARCH_BOX)
```

#### 3. Test File (`projects/automation_test_store/tests/selenium/test_homepage.py`)

```python
"""
Homepage tests for Automation Test Store using Selenium.
"""

import pytest
import allure
from projects.automation_test_store.pages.home_page import HomePage


@allure.epic("E-Commerce")
@allure.feature("Homepage")
@allure.story("Homepage Load")
@pytest.mark.selenium
@pytest.mark.automation_test_store
def test_homepage_loads_successfully(selenium_driver):
    """
    Test that homepage loads successfully.
    
    Steps:
    1. Navigate to homepage
    2. Verify page elements are visible
    3. Verify featured products are displayed
    """
    with allure.step("Initialize homepage"):
        home_page = HomePage(selenium_driver)
    
    with allure.step("Open homepage"):
        home_page.open()
    
    with allure.step("Verify homepage is loaded"):
        assert home_page.is_loaded(), "Homepage did not load correctly"
    
    with allure.step("Verify featured products are displayed"):
        product_count = home_page.get_featured_products_count()
        assert product_count > 0, f"Expected featured products, found {product_count}"
        
        allure.attach(
            f"Featured products count: {product_count}",
            name="Product Count",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("E-Commerce")
@allure.feature("Product Search")
@allure.story("Search Functionality")
@pytest.mark.selenium
@pytest.mark.automation_test_store
def test_product_search(selenium_driver):
    """
    Test product search functionality.
    
    Steps:
    1. Navigate to homepage
    2. Search for a product
    3. Verify search results are displayed
    """
    with allure.step("Initialize homepage"):
        home_page = HomePage(selenium_driver)
    
    with allure.step("Open homepage"):
        home_page.open()
    
    with allure.step("Search for 'skincare'"):
        product_page = home_page.search_product("skincare")
    
    with allure.step("Verify search results"):
        # Product page verification would go here
        assert "skincare" in selenium_driver.current_url.lower() or \
               "search" in selenium_driver.current_url.lower(), \
               "Search did not navigate to results page"
```

#### 4. Project Fixtures (`projects/automation_test_store/tests/conftest.py`)

```python
"""
Project-specific fixtures for Automation Test Store.
"""

import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def project_config():
    """Load project-specific configuration."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def test_user(project_config):
    """Provide test user credentials."""
    return project_config['test_users'][0]


@pytest.fixture(scope="function")
def base_url(project_config):
    """Provide base URL for the project."""
    return project_config['base_url']
```

---

## 🚀 Creating a New Project

### Option 1: Use the Template (Recommended)

```bash
# Copy template to new project
cp -r projects/_template projects/my_new_project

# Rename template files
mv projects/my_new_project/config.yaml.template projects/my_new_project/config.yaml
mv projects/my_new_project/tests/conftest.py.template projects/my_new_project/tests/conftest.py

# Update config.yaml with project details
# Start creating page objects and tests!
```

### Option 2: Use the Creation Script

```python
# scripts/create_new_project.py
import os
import shutil
from pathlib import Path


def create_new_project(project_name):
    """Create a new project from template."""
    
    template_dir = Path("projects/_template")
    project_dir = Path(f"projects/{project_name}")
    
    if project_dir.exists():
        print(f"❌ Project '{project_name}' already exists!")
        return
    
    # Copy template
    shutil.copytree(template_dir, project_dir)
    
    # Rename template files
    (project_dir / "config.yaml.template").rename(project_dir / "config.yaml")
    (project_dir / "tests/conftest.py.template").rename(project_dir / "tests/conftest.py")
    
    # Update config with project name
    config_file = project_dir / "config.yaml"
    content = config_file.read_text()
    content = content.replace("PROJECT_NAME", project_name)
    config_file.write_text(content)
    
    print(f"✅ Project '{project_name}' created successfully!")
    print(f"📁 Location: {project_dir}")
    print(f"\nNext steps:")
    print(f"1. Update {project_dir}/config.yaml with your project details")
    print(f"2. Create page objects in {project_dir}/pages/")
    print(f"3. Write tests in {project_dir}/tests/")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_new_project.py <project_name>")
        sys.exit(1)
    
    create_new_project(sys.argv[1])
```

**Usage**:
```bash
python scripts/create_new_project.py my_new_project
```

---

## 🧪 Running Tests

### Run Tests for Specific Project

```bash
# Run all tests for a project
pytest projects/automation_test_store/tests/

# Run only Selenium tests for a project
pytest projects/automation_test_store/tests/selenium/

# Run only Playwright tests for a project
pytest projects/automation_test_store/tests/playwright/

# Run with project marker
pytest -m automation_test_store

# Run specific test file
pytest projects/automation_test_store/tests/selenium/test_homepage.py
```

### Run Tests for All Projects

```bash
# Run all tests across all projects
pytest projects/

# Run with parallel execution
pytest projects/ -n 4

# Generate Allure report for all projects
pytest projects/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 📊 Project-Specific Reporting

### Allure Reports per Project

```bash
# Generate report for specific project
pytest projects/automation_test_store/tests/ \
  --alluredir=projects/automation_test_store/reports/allure-results

allure serve projects/automation_test_store/reports/allure-results
```

### Consolidated Reports

```bash
# Generate consolidated report for all projects
pytest projects/ --alluredir=reports/allure-results-all
allure serve reports/allure-results-all
```

---

## 🎯 Best Practices

### 1. **Page Object Naming**
- Use descriptive names: `HomePage`, `ProductDetailPage`, `CheckoutPage`
- Suffix with `Page`: `LoginPage`, not just `Login`
- Group related pages in subdirectories if needed

### 2. **Test Organization**
- One test file per page or feature
- Use descriptive test names: `test_user_can_add_product_to_cart`
- Group related tests in classes if needed

### 3. **Locator Strategy**
- Define all locators at the top of the page class
- Use constants: `SEARCH_BOX = (By.ID, "search")`
- Prefer IDs > CSS > XPath

### 4. **Test Data Management**
- Store test data in `test_data/` directory
- Use JSON or CSV for structured data
- Use fixtures to load test data

### 5. **Configuration**
- Keep project-specific config in project directory
- Use global config for framework settings
- Override with CLI arguments when needed

---

## 🔧 Migration Guide

### Migrating Existing Tests

**Current Structure**:
```
tests/
├── selenium/
│   ├── pages/
│   └── test_*.py
└── playwright/
    └── test_*.py
```

**New Structure**:
```
projects/
└── automation_test_store/
    ├── pages/
    └── tests/
        ├── selenium/
        └── playwright/
```

**Migration Steps**:

1. Create new project directory
2. Move page objects to `projects/<project>/pages/`
3. Move tests to `projects/<project>/tests/selenium/` or `playwright/`
4. Create project config
5. Update imports in tests
6. Update CI/CD workflows

---

## 📚 Additional Resources

- **Page Object Model Guide**: `.kiro/steering/page-object-model-guide.md`
- **Multi-Project Guide**: `.kiro/steering/multi-project-guide.md`
- **Framework Overview**: `.kiro/steering/framework-overview.md`
- **Test Writing Guide**: `.kiro/steering/test-writing-guide.md`

---

## 🎓 Example Projects Included

### 1. Automation Test Store
- **URL**: https://automationteststore.com
- **Features**: E-commerce, shopping cart, user registration
- **Status**: ✅ Complete with 45+ tests

### 2. Skechers Staging
- **URL**: https://staging.skechers.com
- **Features**: HTTP Basic Auth, product catalog
- **Status**: ✅ Complete with 8 tests

### 3. Template Project
- **Purpose**: Quick start for new projects
- **Status**: ✅ Ready to use

---

## 💡 Tips for Teams

### For QE Teams:
- Each team can own their project directory
- Share framework utilities
- Contribute improvements to core framework

### For Project Managers:
- Easy to track test coverage per project
- Independent test execution
- Clear project boundaries

### For DevOps:
- Project-specific CI/CD workflows
- Parallel execution across projects
- Consolidated reporting

---

## 🚀 Next Steps

1. **Review the structure** - Understand the organization
2. **Create your first project** - Use the template or script
3. **Write page objects** - Follow the base class pattern
4. **Write tests** - Use page objects in tests
5. **Run tests** - Execute and generate reports
6. **Share with team** - Onboard other teams

---

*Last Updated: April 16, 2026*
*Version: 1.0.0*
