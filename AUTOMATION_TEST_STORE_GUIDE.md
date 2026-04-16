# Automation Test Store - Testing Guide

**Application URL:** https://automationteststore.com/  
**Purpose:** Practice automation skills  
**Framework:** Test Automation Framework v0.2.0  
**Last Updated:** 2024-01-15

---

## 🎯 Overview

This guide shows you how to create test cases and automate them for the Automation Test Store using our framework.

**Important Notes:**
- ✅ This is a practice site (no real orders/payments)
- ✅ Use test data only
- ✅ Educational purposes only
- ✅ Site is designed for automation practice

---

## 📋 Step 1: Explore the Application

### Manual Exploration Checklist

Before writing automated tests, manually explore the application:

- [ ] **Homepage**: Featured products, latest products, bestsellers, specials
- [ ] **Navigation**: Categories, search, cart, account
- [ ] **Product Pages**: Product details, add to cart, images
- [ ] **Shopping Cart**: Add/remove items, update quantities, checkout
- [ ] **Checkout**: Guest checkout, registered user checkout, payment
- [ ] **Account**: Register, login, logout, profile, orders
- [ ] **Search**: Search functionality, filters, results

### Key Features Identified

1. **Product Browsing**
   - Categories (Apparel & Accessories, Makeup, Skincare, Fragrance, Men, Hair Care, Books)
   - Featured products
   - Latest products
   - Bestsellers
   - Specials/Sales

2. **Shopping Cart**
   - Add to cart
   - Update quantities
   - Remove items
   - View cart total

3. **Checkout Process**
   - Guest checkout
   - Registered user checkout
   - Shipping information
   - Payment information

4. **User Account**
   - Registration
   - Login/Logout
   - Profile management
   - Order history

5. **Search**
   - Product search
   - Search results
   - Filters

---

## 📝 Step 2: Define Test Cases

### Test Case Template

```
Test Case ID: TC-XXX
Test Case Name: [Descriptive name]
Priority: High/Medium/Low
Preconditions: [What must be true before test]
Test Steps:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
Expected Result: [What should happen]
Test Data: [Data needed for test]
```

### High-Priority Test Cases

#### TC-001: Homepage Load
- **Priority**: High
- **Preconditions**: None
- **Steps**:
  1. Navigate to https://automationteststore.com/
  2. Verify page loads successfully
  3. Verify main sections are visible (Featured, Latest, Bestsellers, Specials)
- **Expected**: Homepage loads with all sections visible
- **Test Data**: None

#### TC-002: Product Search
- **Priority**: High
- **Preconditions**: Homepage loaded
- **Steps**:
  1. Navigate to homepage
  2. Enter "skincare" in search box
  3. Click search button
  4. Verify search results displayed
- **Expected**: Search results show skincare products
- **Test Data**: Search term: "skincare"

#### TC-003: Add Product to Cart
- **Priority**: High
- **Preconditions**: Homepage loaded
- **Steps**:
  1. Navigate to homepage
  2. Click on a product
  3. Click "Add to Cart" button
  4. Verify cart count increases
  5. Navigate to cart
  6. Verify product is in cart
- **Expected**: Product added to cart successfully
- **Test Data**: Any product

#### TC-004: User Registration
- **Priority**: High
- **Preconditions**: None
- **Steps**:
  1. Navigate to homepage
  2. Click "Login or register"
  3. Click "Continue" under "I am a new customer"
  4. Fill registration form
  5. Click "Continue"
  6. Verify registration success
- **Expected**: User registered successfully
- **Test Data**: 
  - First Name: Test
  - Last Name: User
  - Email: test{timestamp}@example.com
  - Password: Test123!

#### TC-005: User Login
- **Priority**: High
- **Preconditions**: User registered
- **Steps**:
  1. Navigate to homepage
  2. Click "Login or register"
  3. Enter login credentials
  4. Click "Login"
  5. Verify user logged in
- **Expected**: User logged in successfully
- **Test Data**: Registered user credentials

#### TC-006: Guest Checkout
- **Priority**: High
- **Preconditions**: Product in cart
- **Steps**:
  1. Add product to cart
  2. Navigate to cart
  3. Click "Checkout"
  4. Select "Guest Checkout"
  5. Fill shipping information
  6. Confirm order
- **Expected**: Order placed successfully
- **Test Data**: Guest shipping information

#### TC-007: Remove Item from Cart
- **Priority**: Medium
- **Preconditions**: Product in cart
- **Steps**:
  1. Add product to cart
  2. Navigate to cart
  3. Click remove button
  4. Verify product removed
  5. Verify cart empty
- **Expected**: Product removed from cart
- **Test Data**: Any product

#### TC-008: Update Cart Quantity
- **Priority**: Medium
- **Preconditions**: Product in cart
- **Steps**:
  1. Add product to cart
  2. Navigate to cart
  3. Update quantity to 2
  4. Click update
  5. Verify quantity updated
  6. Verify total price updated
- **Expected**: Quantity and price updated
- **Test Data**: Quantity: 2

#### TC-009: Category Navigation
- **Priority**: Medium
- **Preconditions**: Homepage loaded
- **Steps**:
  1. Navigate to homepage
  2. Click on a category (e.g., "Makeup")
  3. Verify category page loads
  4. Verify products displayed
- **Expected**: Category page shows relevant products
- **Test Data**: Category: Makeup

#### TC-010: Product Details View
- **Priority**: Medium
- **Preconditions**: Homepage loaded
- **Steps**:
  1. Navigate to homepage
  2. Click on a product
  3. Verify product details displayed
  4. Verify product image, price, description visible
- **Expected**: Product details page shows all information
- **Test Data**: Any product

---

## 🚀 Step 3: Set Up Framework Configuration

### Update config.yaml

```yaml
# Base URL for Automation Test Store
base_url: "https://automationteststore.com/"

# Browser selection
browser: "chrome"

# Headless mode (false for debugging, true for CI)
headless: false

# Timeouts
timeout: 30
implicit_wait: 10
page_load_timeout: 60

# Parallel execution
parallel_workers: 2

# Report directory
report_dir: "reports"

# Selenium settings
selenium:
  implicit_wait: 10
  page_load_timeout: 60

# Playwright settings
playwright:
  slow_mo: 0
  tracing: true
```

---

## 📁 Step 4: Create Page Object Model

### Why Page Object Model?

- ✅ Maintainability: Locators in one place
- ✅ Reusability: Methods can be reused across tests
- ✅ Readability: Tests are more readable
- ✅ Scalability: Easy to add new pages

### Create Page Objects Directory

```bash
mkdir -p tests/selenium/pages
mkdir -p tests/playwright/pages
```

### Example: Homepage Page Object (Selenium)

Create `tests/selenium/pages/home_page.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    """Page Object for Automation Test Store Homepage."""
    
    # Locators
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    CART_ICON = (By.CSS_SELECTOR, ".cart")
    CART_COUNT = (By.CSS_SELECTOR, ".cart .label-orange")
    LOGIN_LINK = (By.LINK_TEXT, "Login or register")
    
    # Product sections
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".thumbnails.grid.row")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".thumbnails.grid.row .thumbnail:first-child")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate(self):
        """Navigate to homepage."""
        self.driver.get("https://automationteststore.com/")
    
    def search_product(self, search_term):
        """Search for a product."""
        search_input = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(search_term)
        
        search_button = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button.click()
    
    def click_first_product(self):
        """Click on the first product."""
        first_product = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_PRODUCT)
        )
        first_product.click()
    
    def click_login_link(self):
        """Click on login/register link."""
        login_link = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_link.click()
    
    def get_cart_count(self):
        """Get the number of items in cart."""
        try:
            cart_count = self.driver.find_element(*self.CART_COUNT)
            return int(cart_count.text)
        except:
            return 0
    
    def is_loaded(self):
        """Check if homepage is loaded."""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.FEATURED_PRODUCTS)
            )
            return True
        except:
            return False
```

### Example: Product Page Object (Selenium)

Create `tests/selenium/pages/product_page.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    """Page Object for Product Details Page."""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".productname")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productprice")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".cart")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def get_product_name(self):
        """Get product name."""
        product_name = self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_NAME)
        )
        return product_name.text
    
    def get_product_price(self):
        """Get product price."""
        product_price = self.driver.find_element(*self.PRODUCT_PRICE)
        return product_price.text
    
    def add_to_cart(self):
        """Add product to cart."""
        add_button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )
        add_button.click()
    
    def set_quantity(self, quantity):
        """Set product quantity."""
        quantity_input = self.driver.find_element(*self.QUANTITY_INPUT)
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
```

### Example: Cart Page Object (Selenium)

Create `tests/selenium/pages/cart_page.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Page Object for Shopping Cart Page."""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".table.table-striped tbody tr")
    CHECKOUT_BUTTON = (By.ID, "cart_checkout1")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, ".btn.btn-default")
    CART_TOTAL = (By.CSS_SELECTOR, ".total-price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".btn.btn-sm.btn-default")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate(self):
        """Navigate to cart page."""
        self.driver.get("https://automationteststore.com/index.php?rt=checkout/cart")
    
    def get_cart_items_count(self):
        """Get number of items in cart."""
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def click_checkout(self):
        """Click checkout button."""
        checkout_button = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        checkout_button.click()
    
    def remove_first_item(self):
        """Remove first item from cart."""
        remove_button = self.wait.until(
            EC.element_to_be_clickable(self.REMOVE_BUTTON)
        )
        remove_button.click()
    
    def get_cart_total(self):
        """Get cart total price."""
        total = self.driver.find_element(*self.CART_TOTAL)
        return total.text
    
    def is_cart_empty(self):
        """Check if cart is empty."""
        return self.get_cart_items_count() == 0
```

---

## ✍️ Step 5: Write Automated Tests

### Test 1: Homepage Load (TC-001)

Create `tests/selenium/test_automation_store_homepage.py`:

```python
import pytest
from selenium.webdriver.common.by import By
from tests.selenium.pages.home_page import HomePage


@pytest.mark.selenium
def test_homepage_loads_successfully(selenium_driver):
    """
    TC-001: Verify homepage loads successfully.
    
    Steps:
    1. Navigate to homepage
    2. Verify page loads
    3. Verify main sections visible
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    # Navigate to homepage
    home_page.navigate()
    
    # Verify homepage loaded
    assert home_page.is_loaded(), "Homepage did not load successfully"
    
    # Verify page title
    assert "A place to practice" in driver.page_source, "Homepage content not found"


@pytest.mark.selenium
def test_homepage_has_featured_products(selenium_driver):
    """
    TC-001b: Verify homepage displays featured products.
    
    Steps:
    1. Navigate to homepage
    2. Verify featured products section exists
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    
    # Verify featured products section
    featured = driver.find_elements(*home_page.FEATURED_PRODUCTS)
    assert len(featured) > 0, "No featured products found"
```

### Test 2: Product Search (TC-002)

```python
@pytest.mark.selenium
def test_product_search(selenium_driver):
    """
    TC-002: Verify product search functionality.
    
    Steps:
    1. Navigate to homepage
    2. Search for "skincare"
    3. Verify search results displayed
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    home_page.search_product("skincare")
    
    # Verify search results page
    assert "skincare" in driver.current_url.lower() or "search" in driver.current_url.lower()
    
    # Verify results displayed
    assert "result" in driver.page_source.lower() or "product" in driver.page_source.lower()
```

### Test 3: Add Product to Cart (TC-003)

Create `tests/selenium/test_automation_store_cart.py`:

```python
import pytest
from tests.selenium.pages.home_page import HomePage
from tests.selenium.pages.product_page import ProductPage
from tests.selenium.pages.cart_page import CartPage


@pytest.mark.selenium
def test_add_product_to_cart(selenium_driver):
    """
    TC-003: Verify adding product to cart.
    
    Steps:
    1. Navigate to homepage
    2. Click on first product
    3. Add product to cart
    4. Verify cart count increases
    5. Navigate to cart
    6. Verify product in cart
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Navigate and select product
    home_page.navigate()
    initial_cart_count = home_page.get_cart_count()
    
    home_page.click_first_product()
    
    # Add to cart
    product_name = product_page.get_product_name()
    product_page.add_to_cart()
    
    # Wait a moment for cart to update
    driver.implicitly_wait(2)
    
    # Verify cart count increased
    home_page.navigate()
    new_cart_count = home_page.get_cart_count()
    assert new_cart_count > initial_cart_count, "Cart count did not increase"
    
    # Verify product in cart
    cart_page.navigate()
    assert cart_page.get_cart_items_count() > 0, "No items in cart"
```

### Test 4: Remove Item from Cart (TC-007)

```python
@pytest.mark.selenium
def test_remove_item_from_cart(selenium_driver):
    """
    TC-007: Verify removing item from cart.
    
    Steps:
    1. Add product to cart
    2. Navigate to cart
    3. Remove product
    4. Verify cart empty
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Add product to cart
    home_page.navigate()
    home_page.click_first_product()
    product_page.add_to_cart()
    
    # Navigate to cart
    cart_page.navigate()
    initial_count = cart_page.get_cart_items_count()
    assert initial_count > 0, "Cart should have items"
    
    # Remove item
    cart_page.remove_first_item()
    
    # Wait for removal
    driver.implicitly_wait(2)
    
    # Verify item removed
    new_count = cart_page.get_cart_items_count()
    assert new_count < initial_count, "Item was not removed from cart"
```

---

## 🎭 Step 6: Write Playwright Tests

### Playwright Version of Homepage Test

Create `tests/playwright/test_automation_store_homepage.py`:

```python
import pytest
from playwright.sync_api import expect


@pytest.mark.playwright
def test_homepage_loads_successfully(playwright_page):
    """
    TC-001: Verify homepage loads successfully (Playwright).
    
    Steps:
    1. Navigate to homepage
    2. Verify page loads
    3. Verify main sections visible
    """
    page = playwright_page
    
    # Navigate to homepage
    page.goto("https://automationteststore.com/")
    
    # Verify page title
    expect(page).to_have_title(/practice/)
    
    # Verify featured products section
    featured_section = page.locator(".thumbnails.grid.row")
    expect(featured_section).to_be_visible()


@pytest.mark.playwright
def test_product_search_playwright(playwright_page):
    """
    TC-002: Verify product search (Playwright).
    
    Steps:
    1. Navigate to homepage
    2. Search for product
    3. Verify results
    """
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    
    # Search for product
    page.fill("#filter_keyword", "skincare")
    page.click(".button-in-search")
    
    # Verify search results
    expect(page).to_have_url(/search|skincare/)
```

---

## 🏃 Step 7: Run Your Tests

### Run All Tests

```bash
# Run all Automation Test Store tests
pytest tests/selenium/test_automation_store_*.py -v

# Run with Playwright
pytest tests/playwright/test_automation_store_*.py -v

# Run specific test
pytest tests/selenium/test_automation_store_homepage.py::test_homepage_loads_successfully -v

# Run in parallel
pytest tests/selenium/test_automation_store_*.py -n 2 -v

# Run in headless mode
pytest tests/selenium/test_automation_store_*.py --headless -v
```

### Run with Self-Healing

```bash
# Run with self-healing enabled
pytest tests/selenium/test_automation_store_*.py -v -s
```

---

## 📊 Step 8: Review Reports

After running tests:

```bash
# Open HTML report
open reports/report.html  # Mac
start reports/report.html  # Windows
xdg-open reports/report.html  # Linux

# View JSON report
cat reports/report.json | python -m json.tool

# View screenshots (if any failures)
ls reports/screenshots/

# View Playwright traces (if any failures)
playwright show-trace reports/traces/<test-name>.zip
```

---

## 🎯 Next Steps

### 1. Expand Test Coverage

Add more test cases:
- User registration (TC-004)
- User login (TC-005)
- Guest checkout (TC-006)
- Update cart quantity (TC-008)
- Category navigation (TC-009)
- Product details view (TC-010)

### 2. Add Data-Driven Tests

Use pytest parametrize for multiple test data:

```python
@pytest.mark.parametrize("search_term,expected_results", [
    ("skincare", "skincare"),
    ("makeup", "makeup"),
    ("fragrance", "fragrance"),
])
def test_search_multiple_terms(selenium_driver, search_term, expected_results):
    # Test implementation
    pass
```

### 3. Add API Tests

Test the backend APIs if available:

```python
import requests

def test_api_get_products():
    response = requests.get("https://automationteststore.com/api/products")
    assert response.status_code == 200
```

### 4. Integrate with CI/CD

Add to GitHub Actions workflow:

```yaml
- name: Run Automation Test Store Tests
  run: pytest tests/selenium/test_automation_store_*.py -v --headless
```

### 5. Create Test Data Management

Create fixtures for test data:

```python
@pytest.fixture
def test_user():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test{int(time.time())}@example.com",
        "password": "Test123!"
    }
```

---

## 📝 Summary

You now have:

1. ✅ **Test Cases**: 10 high/medium priority test cases
2. ✅ **Page Objects**: Reusable page object classes
3. ✅ **Automated Tests**: Working Selenium and Playwright tests
4. ✅ **Framework Integration**: Tests use your framework
5. ✅ **Self-Healing**: AI-assisted element healing
6. ✅ **Reports**: HTML/JSON reports with screenshots
7. ✅ **CI/CD Ready**: Can run in Docker and GitHub Actions

---

**Ready to start testing!** 🚀

Run your first test:
```bash
pytest tests/selenium/test_automation_store_homepage.py -v
```
