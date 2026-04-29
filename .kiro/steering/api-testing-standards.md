---
inclusion: fileMatch
fileMatchPattern: "**/tests/**/test_api*.py,**/tests/**/api_endpoints.py,**/tests/api/**"
---

# API Testing Standards

## Architecture: Request Builder Pattern

All API tests MUST follow the Request Builder Pattern. Tests never construct URLs, methods, headers, or payload structures directly.

```
framework/
  api_helper.py              # Single source of truth — ApiHelper class (DO NOT DUPLICATE)

tests/<domain>/
  api_endpoints.py           # Config, endpoints, auth tokens, request builders
  test_*.py                  # Tests — only pass field values to builders
  conftest.py                # api_client fixture
```

## Request Builder Rules

### api_endpoints.py owns ALL API knowledge:
- Base URL constants
- Auth tokens (loaded from .env)
- Endpoint path constants
- Builder functions that return bundle dicts

### Builder function rules:
- Accept only field values as parameters with sensible defaults
- Accept `**overrides` for flexibility
- Return a complete bundle dict: `method`, `base_url`, `endpoint`, `auth_token`, `payload`

### Example:
```python
# tests/skechers/api_endpoints.py
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.skechers.com")
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "")
API_TIMEOUT = 30

# Endpoint constants
GET_PRODUCTS = "/products"
GET_PRODUCT_BY_ID = "/products/{product_id}"
CREATE_ORDER = "/orders"

def build_get_products(limit=20, offset=0, **overrides):
    params = {"limit": limit, "offset": offset}
    params.update(overrides)
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_PRODUCTS,
        "auth_token": API_AUTH_TOKEN,
        "params": params,
    }

def build_create_order(product_id="12345", qty=1, **overrides):
    payload = {"productId": product_id, "quantity": qty, "status": "pending"}
    payload.update(overrides)
    return {
        "method": "POST",
        "base_url": API_BASE_URL,
        "endpoint": CREATE_ORDER,
        "auth_token": API_AUTH_TOKEN,
        "payload": payload,
    }
```

## Test Conventions

### Naming
- File: `test_<domain>.py` (e.g., `test_orders.py`)
- Function: `test_<action>_<condition>_<expected>` in snake_case
  - `test_get_products_returns_200_with_defaults`
  - `test_post_order_returns_201_with_valid_payload`
  - `test_get_product_returns_404_when_invalid_id`

### Structure (AAA Pattern)
```python
from api_endpoints import build_create_order

def test_post_order_returns_201_with_defaults(api_client):
    # Arrange — builder handles everything
    # Act
    response = api_client.send(build_create_order())
    # Assert
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    created = response.json()
    assert created["productId"] == "12345"
```

### Rules
- Tests only pass field values to builders — NO URLs, methods, or payload structures in test files
- One behavior per test
- Use `api_client` fixture — never instantiate ApiHelper directly
- Assertions must include failure messages: `assert x == y, f"Expected {y}, got {x}"`
- No hardcoded credentials — auth tokens come from .env via builders
- No `time.sleep()`

## Fixture Pattern

```python
# tests/<domain>/conftest.py
import pytest
from framework.api_helper import ApiHelper

@pytest.fixture
def api_client():
    client = ApiHelper()
    yield client
    client.close()
```

## ApiHelper Methods

| Method | Use Case |
|--------|----------|
| `send(bundle)` | **Preferred** — uses builder bundles |
| `get(endpoint)` | Direct GET (fallback) |
| `post(endpoint, payload)` | Direct POST (fallback) |
| `put(endpoint, payload)` | Direct PUT (fallback) |
| `delete(endpoint)` | Direct DELETE (fallback) |

**Always prefer `send()` with builders over direct methods.**

## Anti-Patterns (DO NOT)

- ❌ Put URLs, HTTP methods, or payload structures in test files
- ❌ Instantiate ApiHelper directly in tests — use api_client fixture
- ❌ Hardcode auth tokens — use .env
- ❌ Edit framework/api_helper.py for project-specific logic — extend via builders
- ❌ Duplicate ApiHelper logic in project code
- ❌ Use time.sleep() — use timeout parameter

## Per-Domain Endpoints

Each domain should have its own api_endpoints.py:
- `tests/skechers/api_endpoints.py` — E-commerce endpoints
- `tests/salesforce_crm/api_endpoints.py` — Salesforce CRM endpoints
- `tests/salesforce_loyalty/api_endpoints.py` — Loyalty endpoints
- `tests/boomi/api_endpoints.py` — Boomi endpoints
