# Skechers Staging Tests

This directory contains tests specifically for the Skechers staging environment.

## Test Files

### 1. `test_homepage.py`
Tests for Skechers homepage functionality.

**Test Classes:**
- `TestSkechersHomepage` - Homepage element and functionality tests
- `TestSkechersResponsiveness` - Responsive design tests

**Tests:**
- ✅ Homepage loads successfully
- ✅ Logo is present
- ✅ Navigation menu is present
- ✅ Search functionality is present
- ✅ Footer is present
- ✅ Category links are present
- ✅ Responsive design at different viewports

### 2. `test_product_search.py`
Tests for product search functionality.

**Test Classes:**
- `TestSkechersProductSearch` - Search functionality tests
- `TestSkechersSearchResults` - Search results page tests

**Tests:**
- ✅ Search with valid keyword
- ✅ Search with empty query
- ✅ Search various product types
- ✅ Search results display
- ✅ Search filters present
- ✅ Search sorting options

### 3. `test_api_products.py`
Tests for Skechers product API endpoints.

**Test Classes:**
- `TestSkechersProductAPI` - Product API tests
- `TestSkechersProductFilters` - Product filtering tests
- `TestSkechersProductReviews` - Product reviews tests

**Tests:**
- ✅ Get products list
- ✅ Get product by ID
- ✅ Search products via API
- ✅ Get products by category
- ✅ Check product availability
- ✅ Filter by price range
- ✅ Filter by size
- ✅ Filter by color
- ✅ Get product reviews
- ✅ Get product rating

## Configuration

### Using Skechers Staging Config

```bash
# Run tests with Skechers staging configuration
pytest tests/skechers/ --config=config.skechers-staging.yaml -v
```

### Environment Variables

Set these environment variables for sensitive data:

```bash
export SKECHERS_TEST_EMAIL="test.user@skechers.com"
export SKECHERS_TEST_PASSWORD="your-password"
export SKECHERS_API_KEY="your-api-key"
```

## Running Tests

### Run All Skechers Tests

```bash
pytest tests/skechers/ -v
```

### Run Specific Test File

```bash
# Homepage tests
pytest tests/skechers/test_homepage.py -v

# Search tests
pytest tests/skechers/test_product_search.py -v

# API tests
pytest tests/skechers/test_api_products.py -v
```

### Run Smoke Tests Only

```bash
pytest tests/skechers/ -m smoke -v
```

### Run API Tests Only

```bash
pytest tests/skechers/ -m api -v
```

### Run with Specific Browser

```bash
# Chrome
pytest tests/skechers/ --browser=chrome -v

# Firefox
pytest tests/skechers/ --browser=firefox -v
```

### Run in Headless Mode

```bash
pytest tests/skechers/ --headless -v
```

### Run with Allure Report

```bash
pytest tests/skechers/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```

## Test Markers

Tests are marked with pytest markers for easy filtering:

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.api` - API tests

## Notes

### Selector Updates Required

⚠️ **Important:** The tests use generic selectors that may need to be updated based on the actual Skechers staging site structure.

**To update selectors:**
1. Inspect the Skechers staging site
2. Identify actual element selectors (IDs, classes, XPath)
3. Update selectors in test files

**Example:**
```python
# Generic selector (may need update)
logo = page.find_element("css", ".logo")

# Update to actual Skechers selector
logo = page.find_element("css", ".skechers-logo")
```

### API Endpoints

The API tests assume certain endpoint patterns. Update these based on actual Skechers API documentation:

```python
# Example endpoints (update as needed)
/api/products
/api/products/{id}
/api/products/search
/api/products/category/{category}
```

### Test Data

Update test data in `config.skechers-staging.yaml`:
- Test user credentials
- Product IDs
- Categories
- Regions

## CI/CD Integration

These tests are integrated with GitHub Actions workflows:

### Pull Request Tests
```yaml
# Runs automatically on PR
- API tests
- UI tests
- Generates reports
```

### Scheduled Tests
```bash
# Run Skechers tests daily
pytest tests/skechers/ -v
```

## Troubleshooting

### Tests Failing Due to Selectors

If tests fail with "Element not found" errors:

1. **Inspect the page** - Use browser DevTools
2. **Update selectors** - Modify test files with correct selectors
3. **Add waits** - Increase timeout if elements load slowly
4. **Check for iframes** - Elements may be in iframes

### API Tests Returning 404

If API tests return 404:

1. **Verify API endpoints** - Check Skechers API documentation
2. **Update base URL** - Ensure correct API base URL in config
3. **Check authentication** - API may require authentication

### Slow Test Execution

If tests run slowly:

1. **Use headless mode** - `--headless` flag
2. **Reduce waits** - Optimize explicit waits
3. **Run in parallel** - Use `-n auto` with pytest-xdist

## Contributing

When adding new Skechers tests:

1. Follow existing test structure
2. Use descriptive test names
3. Add appropriate markers (`@pytest.mark.smoke`, etc.)
4. Update this README
5. Ensure tests pass locally before PR

## Contact

For questions about Skechers tests:
- Check test documentation
- Review test code comments
- Consult Skechers staging documentation
