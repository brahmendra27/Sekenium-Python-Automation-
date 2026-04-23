---
inclusion: auto
---

# Quality Engineering Standards

## Test Reliability

### Flaky Test Management
- Use `framework/reliability_helper.py` for flaky test handling
- Classify failures: timing, data, environment, locator, unknown
- Use `@retry_on_flake(max_retries=2)` for known flaky tests
- Quarantine persistently flaky tests with `@pytest.mark.skip(reason="Quarantined: JIRA-XXX")`
- Track flaky test rate — target < 2% of total tests

### Root Cause Categories
| Category | Symptoms | Fix |
|----------|----------|-----|
| Timing | Timeout, not visible | Use Playwright auto-wait, add explicit waits |
| Locator | Element not found, stale | Use data-testid, getByRole |
| Data | Assertion mismatch | Use unique_id fixture, isolate test data |
| Environment | Connection refused | Add health check, verify VPN |

## Accessibility Testing

### When to Run
- On every PR that changes UI components
- Weekly full WCAG audit on e-commerce pages
- Before every release

### How to Use
```python
from framework.accessibility_helper import AccessibilityHelper

def test_homepage_accessibility(playwright_driver):
    page = playwright_driver
    page.goto("https://staging.skechers.com")
    a11y = AccessibilityHelper(page)
    a11y.assert_wcag_aa()  # WCAG 2.1 Level AA
```

### Standards
- Target: WCAG 2.1 Level AA compliance
- Critical/serious violations must be fixed before release
- Minor violations tracked in backlog

## Performance Testing

### Page Performance Budgets
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| Page Load | < 3000ms | < 5000ms | > 5000ms |
| TTFB | < 800ms | < 1800ms | > 1800ms |
| LCP | < 2500ms | < 4000ms | > 4000ms |
| CLS | < 0.1 | < 0.25 | > 0.25 |

### API Performance Budgets
| Endpoint Type | Target | Max |
|--------------|--------|-----|
| Read (GET) | < 200ms | < 500ms |
| Write (POST/PUT) | < 500ms | < 1000ms |
| Search/Query | < 1000ms | < 3000ms |
| Batch/Bulk | < 5000ms | < 10000ms |

### How to Use
```python
from framework.performance_helper import PerformanceHelper, APIPerformanceHelper

def test_homepage_performance(playwright_driver):
    page = playwright_driver
    page.goto("https://staging.skechers.com")
    perf = PerformanceHelper(page)
    perf.assert_page_load_under(3000)
    perf.assert_lcp_under(2500)

def test_api_response_time(api_client):
    response = api_client.get("/products")
    APIPerformanceHelper.assert_response_time(response, max_ms=500)
```

## Contract Testing

### When to Use
- Boomi middleware integration points
- Salesforce API responses
- E-commerce API endpoints
- Any cross-system data exchange

### How to Use
```python
from framework.contract_helper import ContractHelper

def test_order_api_contract(api_client):
    response = api_client.get("/orders/123")
    contract = ContractHelper()
    contract.assert_contract(response.json(), "order_response.json")
    contract.assert_fields_present(response.json(), ["id", "status", "total"])
    contract.assert_field_types(response.json(), {
        "id": str, "status": str, "total": (int, float)
    })
```

### Schema Files
Store JSON schemas in `tests/test_data/schemas/`:
```
tests/test_data/schemas/
├── order_response.json
├── product_response.json
├── loyalty_member.json
├── boomi_execution.json
└── snapshots/           # Auto-generated structure snapshots
```

## Quality Metrics to Track

### Test Suite Health
- **Pass Rate**: Target > 95%
- **Flaky Rate**: Target < 2%
- **Execution Time**: Track trends, flag regressions
- **Coverage**: Critical paths >= 80%

### Per Domain
- **E-commerce**: Page load < 3s, WCAG AA, cart flow 100% covered
- **Salesforce CRM**: CRUD operations, search, bulk operations
- **Loyalty**: Enrollment, points, transactions, tier changes
- **Boomi**: Process execution success rate, document validation
