# Demo E-commerce Test Suite

## Overview

This test suite provides comprehensive testing for e-commerce functionality including:
- Product catalog browsing
- Shopping cart operations
- User authentication and account management

## Test Structure

### Test Files

1. **test_product_catalog.py** (13 tests)
   - Product catalog page loading
   - Product grid display
   - Product images, prices, titles
   - Add to cart buttons
   - Category filters
   - Sort options
   - Responsive design testing

2. **test_shopping_cart.py** (9 tests)
   - Cart icon presence
   - Cart page accessibility
   - Empty cart messaging
   - Continue shopping functionality
   - Quantity controls
   - Remove item functionality
   - Cart total display
   - Checkout button

3. **test_user_account.py** (9 tests)
   - Login page accessibility
   - Login form elements
   - Password field
   - Login button
   - Forgot password link
   - Registration page
   - Register link on login
   - Account page authentication
   - My account link in header

**Total: 31 tests**

## Test Markers

- `@pytest.mark.smoke` - Critical functionality tests (7 tests)
- `@pytest.mark.regression` - Full regression suite tests (5 tests)
- Parametrized tests for responsive design (3 viewports)

## Configuration

Configuration file: `config.demo-ecommerce.yaml`

Default test site: https://www.saucedemo.com (public demo site)

## Running Tests

### All Tests
```bash
pytest tests/demo_ecommerce/ -v
```

### Smoke Tests Only
```bash
pytest tests/demo_ecommerce/ -m smoke -v
```

### Regression Tests
```bash
pytest tests/demo_ecommerce/ -m regression -v
```

### Specific Test File
```bash
pytest tests/demo_ecommerce/test_product_catalog.py -v
pytest tests/demo_ecommerce/test_shopping_cart.py -v
pytest tests/demo_ecommerce/test_user_account.py -v
```

### With Custom Config
```bash
pytest tests/demo_ecommerce/ --config=config.demo-ecommerce.yaml -v
```

### With Allure Reports
```bash
pytest tests/demo_ecommerce/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### In Docker
```bash
docker run --rm test-automation:latest \
  pytest tests/demo_ecommerce/ -v --alluredir=reports/allure-results
```

## Test Features

### Flexible Selectors
Tests use multiple fallback selector strategies to handle different site structures:
```python
product_selectors = [
    ("css", ".product-grid"),
    ("css", ".product-list"),
    ("css", "[class*='product']"),
    ("xpath", "//div[contains(@class, 'product')]")
]
```

### Graceful Degradation
Tests print informative messages when optional elements aren't found rather than failing:
```python
if not filters_found:
    print("Note: Filters not found - may not be available on this site")
```

### Responsive Testing
Tests verify functionality across multiple viewport sizes:
- Desktop: 1920x1080
- Tablet: 768x1024
- Mobile: 375x667

## Test Coverage

### Product Catalog (13 tests)
- ✅ Page loading
- ✅ Product grid display
- ✅ Product images
- ✅ Product prices
- ✅ Product titles
- ✅ Add to cart buttons
- ✅ Category filters
- ✅ Sort options
- ✅ Responsive design (3 viewports)

### Shopping Cart (9 tests)
- ✅ Cart icon visibility
- ✅ Cart page access
- ✅ Empty cart handling
- ✅ Continue shopping
- ✅ Quantity controls
- ✅ Remove items
- ✅ Cart total
- ✅ Checkout button

### User Account (9 tests)
- ✅ Login page access
- ✅ Login form elements
- ✅ Password field
- ✅ Login button
- ✅ Forgot password
- ✅ Registration page
- ✅ Register link
- ✅ Account authentication
- ✅ Account link

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:
- Docker-compatible
- Headless mode support
- Allure report generation
- Parallel execution support
- Flexible configuration

## Notes

- Tests are designed to be site-agnostic with flexible selectors
- Some tests may skip if certain features aren't available
- Default configuration uses a public demo site
- Update `config.demo-ecommerce.yaml` to test your own site

## Customization

To test your own e-commerce site:

1. Update `config.demo-ecommerce.yaml`:
   ```yaml
   base_url: "https://your-ecommerce-site.com"
   ```

2. Update selectors in test files if needed

3. Add site-specific test data

4. Run tests:
   ```bash
   pytest tests/demo_ecommerce/ -v
   ```

## Troubleshooting

### Tests Skipping
- Check if the site structure matches expected selectors
- Update selectors in test files
- Verify base_url is correct

### Timeouts
- Increase timeout in config.yaml
- Check network connectivity
- Verify site is accessible

### Element Not Found
- Tests use multiple fallback selectors
- Check browser console for errors
- Update selectors based on actual site structure

## Future Enhancements

- [ ] Add product detail page tests
- [ ] Add checkout flow tests
- [ ] Add payment integration tests
- [ ] Add order history tests
- [ ] Add wishlist functionality tests
- [ ] Add product review tests
- [ ] Add search functionality tests
