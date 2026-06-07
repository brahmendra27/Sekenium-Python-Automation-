---
inclusion: always
---

# Enterprise Testing Guide

## Supported Domains

This framework supports testing across 4 domains:

### 1. E-commerce (Skechers)
- **UI Tests**: Playwright/Selenium against staging site
- **API Tests**: Product catalog, search, cart APIs
- **Config**: `config.skechers-staging.yaml`
- **Tests**: `tests/skechers/`

### 2. Salesforce CRM
- **API Tests**: SOQL queries, CRUD on Accounts/Contacts/Opportunities
- **Client**: `framework/salesforce_client.py` → `SalesforceClient`
- **Auth**: OAuth2 password flow or client credentials
- **Config**: `.env` file with SF_* variables
- **Tests**: `tests/salesforce_crm/`

### 3. Salesforce Loyalty Management
- **API Tests**: Member enrollment, points, transactions, tiers
- **Client**: `framework/salesforce_client.py` → Loyalty methods
- **Objects**: LoyaltyProgramMember, TransactionJournal, LoyaltyProgram
- **Tests**: `tests/salesforce_loyalty/`

### 4. Boomi Middleware
- **Integration Tests**: Process execution, document tracking
- **Client**: `framework/boomi_client.py` → `BoomiClient`
- **Auth**: HTTP Basic Auth with API token
- **Config**: `.env` file with BOOMI_* variables
- **Tests**: `tests/boomi/`

## Project Structure

```
project/
├── framework/                      # Core framework
│   ├── base_page.py               # UI page objects (Selenium + Playwright)
│   ├── api_client.py              # Generic REST API client
│   ├── salesforce_client.py       # Salesforce CRM + Loyalty client
│   ├── boomi_client.py            # Boomi middleware client
│   ├── config.py                  # Configuration loader (.env + YAML)
│   ├── schema_validator.py        # JSON schema validation
│   ├── selenium_driver.py         # Selenium WebDriver wrapper
│   ├── playwright_driver.py       # Playwright driver wrapper
│   └── mongodb_client.py          # MongoDB client
├── tests/
│   ├── skechers/                  # E-commerce tests
│   ├── salesforce_crm/            # Salesforce CRM tests
│   ├── salesforce_loyalty/        # Loyalty Management tests
│   ├── boomi/                     # Boomi integration tests
│   ├── api/                       # Generic API tests
│   └── test_data/                 # Shared test data files
├── conftest.py                    # Root fixtures
├── config.yaml                    # Default config (no credentials)
├── .env                           # Credentials (gitignored)
├── .env.example                   # Credential template
└── pytest.ini                     # Test runner config
```

## Environment Variables

### Salesforce
```
SF_INSTANCE_URL=https://your-org.my.salesforce.com
SF_CLIENT_ID=your_connected_app_client_id
SF_CLIENT_SECRET=your_connected_app_secret
SF_USERNAME=test.user@company.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_LOGIN_URL=https://login.salesforce.com
```

### Boomi
```
BOOMI_ACCOUNT_ID=BOOMI-XXXXX
BOOMI_USERNAME=your_username
BOOMI_PASSWORD=your_api_token
```

### E-commerce
```
BASE_URL=https://storefront:password@staging.skechers.com/
BROWSER=chrome
HEADLESS=false
```

## Test Markers

Use markers to run domain-specific tests:

```bash
# E-commerce only
pytest -m ecommerce -v

# Salesforce CRM only
pytest -m salesforce_crm -v

# Loyalty Management only
pytest -m loyalty -v

# Boomi integration only
pytest -m boomi -v

# Smoke tests across all domains
pytest -m smoke -v

# API tests only (no UI)
pytest -m api -v
```

## Writing Tests by Domain

### E-commerce Test Pattern
```python
import pytest
from framework.base_page import BasePageSelenium

class TestProductCatalog:
    @pytest.mark.ecommerce
    @pytest.mark.smoke
    def test_catalog_loads(self, driver):
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        assert "product" in driver.current_url.lower()
```

### Salesforce CRM Test Pattern
```python
import pytest

class TestAccountManagement:
    @pytest.mark.salesforce_crm
    @pytest.mark.api
    def test_create_account(self, sf_client):
        result = sf_client.create("Account", {"Name": "Test Corp"})
        assert result["success"] is True
        # Cleanup
        sf_client.delete("Account", result["id"])
```

### Loyalty Management Test Pattern
```python
import pytest

class TestLoyaltyEnrollment:
    @pytest.mark.loyalty
    @pytest.mark.api
    def test_enroll_member(self, sf_client):
        member = sf_client.enroll_loyalty_member({
            "ContactId": "003XXXXXXXXXXXX",
            "LoyaltyProgramId": "0lp XXXXXXXXXXXX"
        })
        assert member["success"] is True
```

### Boomi Integration Test Pattern
```python
import pytest

class TestOrderIntegration:
    @pytest.mark.boomi
    @pytest.mark.integration
    def test_order_sync_flow(self, boomi_client):
        result = boomi_client.validate_integration(
            process_id="abc-123",
            atom_id="atom-456",
            expected_status="COMPLETE",
            timeout=120
        )
        assert result["status"] == "COMPLETE"
```

## Cross-Domain Integration Tests

For end-to-end flows that span multiple systems:

```python
class TestOrderToLoyaltyFlow:
    """Test: E-commerce order → Boomi sync → Salesforce loyalty points."""

    @pytest.mark.integration
    @pytest.mark.e2e
    def test_order_triggers_loyalty_points(self, sf_client, boomi_client, api_client):
        # 1. Place order via e-commerce API
        order = api_client.post("/orders", json_data={...})

        # 2. Wait for Boomi to process the order
        boomi_client.wait_for_execution(execution_id, timeout=120)

        # 3. Verify loyalty points credited in Salesforce
        points = sf_client.get_member_points(member_id)
        assert points["TotalPointsBalance"] > 0
```

## Data Isolation Rules

- Each test creates its own data and cleans up after
- Use `unique_id` fixture for parallel-safe identifiers
- Never modify shared/production data
- Use Salesforce sandbox environments only
- Boomi test processes should use test Atoms

## CI/CD Integration

### Run by Domain
```yaml
jobs:
  ecommerce-tests:
    run: pytest -m ecommerce --alluredir=reports/allure-results
  salesforce-tests:
    run: pytest -m "salesforce_crm or loyalty" --alluredir=reports/allure-results
  boomi-tests:
    run: pytest -m boomi --alluredir=reports/allure-results
```

## Troubleshooting

### Salesforce Auth Fails
- Verify SF_CLIENT_ID and SF_CLIENT_SECRET in .env
- Check Connected App settings in Salesforce Setup
- Ensure IP restrictions allow your test runner
- For sandbox: use SF_LOGIN_URL=https://test.salesforce.com

### Boomi Execution Timeout
- Check Atom status: `boomi_client.list_atoms()`
- Verify process is deployed to the correct environment
- Check Boomi execution logs in AtomSphere UI
- Increase timeout for long-running processes

### E-commerce Site Unreachable
- Check VPN connection
- Verify BASE_URL in .env
- Check staging environment status
