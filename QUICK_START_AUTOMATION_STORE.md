# Quick Start: Testing Automation Test Store

**Application:** https://automationteststore.com/  
**Framework:** Test Automation Framework v0.2.0  
**Time to First Test:** 5 minutes

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Verify Setup (1 minute)

```bash
# Check Python
python --version  # Should be 3.10+

# Check virtual environment
# If not activated:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verify dependencies
pip list | grep pytest
pip list | grep selenium
```

### Step 2: Run Your First Test (2 minutes)

```bash
# Run homepage test
pytest tests/selenium/test_automation_store_homepage.py::test_homepage_loads_successfully -v

# Expected output:
# test_automation_store_homepage.py::test_homepage_loads_successfully PASSED
# ✅ Homepage loaded successfully
```

### Step 3: Run All Tests (2 minutes)

```bash
# Run all Automation Test Store tests
pytest tests/selenium/test_automation_store_*.py -v

# Or use the PowerShell script:
.\run_automation_store_tests.ps1
```

### Step 4: View Reports

```bash
# Open HTML report
start reports/report.html  # Windows
open reports/report.html  # Mac
xdg-open reports/report.html  # Linux
```

---

## 📋 What's Included

### Test Files Created

1. **`tests/selenium/test_automation_store_homepage.py`**
   - ✅ TC-001: Homepage loads successfully
   - ✅ TC-001b: Featured products displayed
   - ✅ TC-001c: Search box visible
   - ✅ TC-001d: Login link visible
   - ✅ TC-002: Product search functionality
   - ✅ TC-002b: Search multiple terms (parametrized)

2. **`tests/selenium/test_automation_store_cart.py`**
   - ✅ TC-003: Add product to cart
   - ✅ TC-007: Remove item from cart
   - ✅ TC-003b: View cart page
   - ✅ TC-003c: Add multiple products
   - ✅ TC-003d: Cart displays total price
   - ✅ TC-003e: Continue shopping button

### Page Objects Created

1. **`tests/selenium/pages/home_page.py`**
   - HomePage class with methods for homepage interactions
   - Locators for search, cart, login, products

2. **`tests/selenium/pages/product_page.py`**
   - ProductPage class for product details
   - Methods for viewing product info, adding to cart

3. **`tests/selenium/pages/cart_page.py`**
   - CartPage class for shopping cart
   - Methods for cart operations (add, remove, update)

### Configuration Updated

- **`config.yaml`**: Base URL set to https://automationteststore.com/

### Documentation Created

- **`AUTOMATION_TEST_STORE_GUIDE.md`**: Complete testing guide
- **`QUICK_START_AUTOMATION_STORE.md`**: This file

---

## 🎯 Test Execution Options

### Option 1: Run Specific Test Suite

```bash
# Homepage tests only
pytest tests/selenium/test_automation_store_homepage.py -v

# Cart tests only
pytest tests/selenium/test_automation_store_cart.py -v

# Specific test
pytest tests/selenium/test_automation_store_homepage.py::test_homepage_loads_successfully -v
```

### Option 2: Run All Tests

```bash
# All Automation Test Store tests
pytest tests/selenium/test_automation_store_*.py -v

# With detailed output
pytest tests/selenium/test_automation_store_*.py -v -s
```

### Option 3: Run with Different Modes

```bash
# Headless mode (no browser window)
pytest tests/selenium/test_automation_store_*.py --headless -v

# Parallel execution (2 workers)
pytest tests/selenium/test_automation_store_*.py -n 2 -v

# With self-healing enabled
pytest tests/selenium/test_automation_store_*.py -v -s
```

### Option 4: Use PowerShell Script

```powershell
# Interactive menu
.\run_automation_store_tests.ps1

# Menu options:
# 1. Homepage Tests
# 2. Shopping Cart Tests
# 3. All Tests
# 4. All Tests (Headless)
# 5. All Tests (Parallel)
```

---

## 📊 Test Results

After running tests, you'll see:

```
tests/selenium/test_automation_store_homepage.py::test_homepage_loads_successfully PASSED
tests/selenium/test_automation_store_homepage.py::test_homepage_has_featured_products PASSED
tests/selenium/test_automation_store_homepage.py::test_product_search PASSED
tests/selenium/test_automation_store_cart.py::test_add_product_to_cart PASSED
tests/selenium/test_automation_store_cart.py::test_remove_item_from_cart PASSED

====== 5 passed in 45.23s ======
```

### Reports Generated

- **HTML Report**: `reports/report.html` (visual report with screenshots)
- **JSON Report**: `reports/report.json` (machine-readable)
- **Screenshots**: `reports/screenshots/` (on failures)
- **Traces**: `reports/traces/` (Playwright traces)

---

## 🎓 Next Steps

### 1. Add More Test Cases

Implement remaining test cases from the guide:

- [ ] TC-004: User Registration
- [ ] TC-005: User Login
- [ ] TC-006: Guest Checkout
- [ ] TC-008: Update Cart Quantity
- [ ] TC-009: Category Navigation
- [ ] TC-010: Product Details View

### 2. Create Playwright Tests

Convert Selenium tests to Playwright:

```bash
# Create Playwright page objects
mkdir -p tests/playwright/pages

# Create Playwright tests
# tests/playwright/test_automation_store_homepage.py
```

### 3. Add Data-Driven Tests

Use pytest parametrize for multiple test data:

```python
@pytest.mark.parametrize("product_name,expected_category", [
    ("Skincare", "Skincare"),
    ("Makeup", "Makeup"),
    ("Fragrance", "Fragrance"),
])
def test_product_categories(selenium_driver, product_name, expected_category):
    # Test implementation
    pass
```

### 4. Integrate with CI/CD

Add to `.github/workflows/test.yml`:

```yaml
- name: Run Automation Test Store Tests
  run: |
    pytest tests/selenium/test_automation_store_*.py --headless -v
```

### 5. Use Self-Healing

Enable self-healing for flaky locators:

```python
from framework.self_healing import SelfHealingLocator

def test_with_healing(selenium_driver):
    healer = SelfHealingLocator(selenium_driver)
    element = healer.find_element_with_healing(By.ID, "submit")
```

---

## 🔍 Troubleshooting

### Issue: Tests fail with "element not found"

**Solution:**
1. Check if site is accessible: https://automationteststore.com/
2. Increase timeout in `config.yaml`
3. Enable self-healing (see `AI_SELF_HEALING_GUIDE.md`)
4. Run with `-s` flag to see detailed output

### Issue: ChromeDriver error on Windows

**Solution:**
Use Docker execution:
```bash
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

### Issue: Tests are slow

**Solution:**
1. Run in headless mode: `--headless`
2. Run in parallel: `-n 2`
3. Reduce implicit wait in `config.yaml`

### Issue: Can't see browser window

**Solution:**
Set `headless: false` in `config.yaml`

---

## 📚 Documentation

- **Complete Guide**: `AUTOMATION_TEST_STORE_GUIDE.md`
- **Framework Overview**: `README.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Kiro Integration**: `KIRO_INTEGRATION_FAQ.md`
- **Self-Healing**: `AI_SELF_HEALING_GUIDE.md`

---

## 🎯 Test Coverage

### Current Coverage

| Feature | Test Cases | Status |
|---------|------------|--------|
| Homepage Load | 4 tests | ✅ Complete |
| Product Search | 2 tests | ✅ Complete |
| Shopping Cart | 6 tests | ✅ Complete |
| User Registration | 0 tests | ⏳ Pending |
| User Login | 0 tests | ⏳ Pending |
| Checkout | 0 tests | ⏳ Pending |

**Total Tests**: 12 automated  
**Total Test Cases**: 10 documented  
**Coverage**: 60% (6/10 test cases)

---

## 💡 Tips

### Tip 1: Use Page Objects

Always use page objects for maintainability:

```python
# ✅ Good
home_page = HomePage(driver)
home_page.search_product("skincare")

# ❌ Bad
driver.find_element(By.ID, "search").send_keys("skincare")
```

### Tip 2: Add Waits

Use explicit waits for dynamic content:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "submit")))
```

### Tip 3: Use Descriptive Test Names

```python
# ✅ Good
def test_add_product_to_cart_increases_cart_count():

# ❌ Bad
def test_cart():
```

### Tip 4: Add Docstrings

Document your tests:

```python
def test_example(selenium_driver):
    """
    TC-001: Test description.
    
    Steps:
    1. Step 1
    2. Step 2
    
    Expected: Expected result
    """
```

### Tip 5: Run Tests Frequently

```bash
# Quick smoke test
pytest tests/selenium/test_automation_store_homepage.py::test_homepage_loads_successfully -v

# Full regression
pytest tests/selenium/test_automation_store_*.py -v
```

---

## 🎉 You're Ready!

You now have:

- ✅ 12 automated tests
- ✅ Page Object Model structure
- ✅ Test execution scripts
- ✅ Comprehensive documentation
- ✅ Self-healing capabilities
- ✅ CI/CD integration ready

**Start testing:**

```bash
pytest tests/selenium/test_automation_store_*.py -v
```

**View results:**

```bash
start reports/report.html
```

Happy testing! 🚀
