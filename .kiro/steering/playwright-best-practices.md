---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Playwright Best Practices (TestDino Golden Rules - Python Adapted)

Based on TestDino's Playwright Skill patterns, adapted for our Python framework.

## 10 Golden Rules

### 1. Use Semantic Locators Over CSS/XPath
```python
# ✅ GOOD — resilient, accessible
page.get_by_role("button", name="Add to Cart")
page.get_by_label("Email")
page.get_by_placeholder("Search products")
page.get_by_test_id("checkout-button")

# ❌ BAD — brittle, breaks on layout changes
page.locator("div.container > ul > li:nth-child(3)")
page.locator("#app > div:nth-child(2) > button")
```

Priority order: `get_by_role` → `get_by_test_id` → `get_by_label` → `get_by_placeholder` → `get_by_text` → `locator()` (last resort with comment)

### 2. Never Use page.wait_for_timeout()
```python
# ✅ GOOD — auto-waits for condition
page.get_by_role("button", name="Submit").click()
expect(page.get_by_text("Success")).to_be_visible()

# ❌ BAD — arbitrary sleep, flaky
page.wait_for_timeout(3000)
time.sleep(2)
```

Use Playwright's built-in auto-waiting. If you must wait, wait for a specific condition.

### 3. Web-First Assertions That Auto-Retry
```python
from playwright.sync_api import expect

# ✅ GOOD — auto-retries until timeout
expect(page.get_by_role("heading")).to_have_text("Welcome")
expect(page.get_by_role("button")).to_be_enabled()
expect(page).to_have_url("/dashboard")

# ❌ BAD — no retry, snapshot assertion
assert page.title() == "Dashboard"  # Fails if page still loading
```

### 4. Isolate Every Test — No Shared State
```python
# ✅ GOOD — each test gets fresh state via fixture
def test_add_to_cart(playwright_driver):
    page = playwright_driver  # Fresh browser context
    # ... test logic

# ❌ BAD — tests depend on each other
class TestCheckout:
    cart_items = []  # Shared mutable state
```

### 5. Use base_url in Config — Zero Hardcoded URLs
```python
# ✅ GOOD — URL from config
page.goto("/products")  # Uses baseURL from config

# ❌ BAD — hardcoded URL
page.goto("https://staging.skechers.com/products")
```

### 6. Retries: 2 in CI, 0 Locally
```python
# playwright.config or pytest.ini
# CI: --retries=2
# Local: --retries=0 (fail fast for debugging)
```

### 7. Traces: On First Retry
Enable tracing to capture what happened before a failure:
```python
# In conftest.py — traces auto-saved on failure
pw_driver = PlaywrightDriver(tracing=True)
```

### 8. Fixtures Over Globals
```python
# ✅ GOOD — fixture provides isolated resource
@pytest.fixture
def authenticated_page(playwright_driver):
    page = playwright_driver
    # Login logic
    yield page
    # Cleanup

# ❌ BAD — global state
GLOBAL_PAGE = None  # Shared across tests
```

### 9. One Behavior Per Test
```python
# ✅ GOOD — tests one thing
def test_add_product_to_cart(page):
    """Verify adding a product increases cart count."""
    # Arrange → Act → Assert

# ❌ BAD — tests multiple things
def test_shopping_flow(page):
    """Tests search, add to cart, checkout, and payment."""
    # Too many behaviors in one test
```

### 10. Mock External Services Only — Never Mock Your Own App
```python
# ✅ GOOD — mock third-party payment API
page.route("**/api.stripe.com/**", lambda route: route.fulfill(
    json={"status": "succeeded"}
))

# ❌ BAD — mocking your own API defeats the purpose of E2E
page.route("**/your-app.com/api/**", ...)
```

## AI Test Insights Pattern

When analyzing test failures, classify by root cause:

| Category | Symptoms | AI Suggestion |
|----------|----------|---------------|
| **Timing** | Timeout, not visible | Add explicit wait for specific condition |
| **Locator** | Element not found | Switch to semantic locator (getByRole) |
| **Data** | Assertion mismatch | Use unique test data, check data isolation |
| **Environment** | Connection refused | Verify environment health, check VPN |
| **Visual** | Screenshot diff | Update baseline or fix CSS regression |

## Fixture Scope Guidelines

| Scope | Use For | Example |
|-------|---------|---------|
| **function** (default) | Browser page, test data | `playwright_driver`, `unique_id` |
| **session** | Auth tokens, API clients, config | `sf_client`, `config` |
| **module** | Shared data within one file | Rare, avoid if possible |

## Network Mocking Pattern
```python
# Mock slow/unreliable external APIs
def test_checkout_with_mocked_payment(playwright_driver):
    page = playwright_driver
    page.route("**/api.stripe.com/**", lambda route: route.fulfill(
        status=200,
        json={"id": "pi_test", "status": "succeeded"}
    ))
    # Test checkout flow without hitting real Stripe
```

## Visual Regression Pattern
```python
# Compare screenshots with baseline
def test_homepage_visual(playwright_driver):
    page = playwright_driver
    page.goto("/")
    expect(page).to_have_screenshot("homepage.png", max_diff_pixel_ratio=0.01)
```
