---
inclusion: manual
---

# REST API Testing Support

## Overview
The workspace has a shared REST API helper (`ApiHelper`) that supports GET, POST, PUT, DELETE operations.
Tests use a request builder pattern where all API knowledge (method, URL, endpoint, auth, payload structure) lives in `api_endpoints.py`, and tests only pass field values.

## Key Files

### Shared Helper (single source of truth — edit here only)
- `framework/api_helper.py` — `ApiHelper` class with `get`, `post`, `put`, `delete`, `send` methods

### Project-Level API Tests
Each domain has its own api_endpoints.py:
- `tests/skechers/api_endpoints.py` — E-commerce endpoints and builders
- `tests/salesforce_crm/api_endpoints.py` — Salesforce CRM endpoints and builders
- `tests/boomi/api_endpoints.py` — Boomi middleware endpoints and builders

### Auth Tokens
- Stored in `.env` file (never committed)
- Loaded by `api_endpoints.py` via `dotenv`, included in builder bundles

## ApiHelper API

```python
class ApiHelper:
    def get(endpoint, params=None) -> Response
    def post(endpoint, payload=None) -> Response
    def put(endpoint, payload=None) -> Response
    def patch(endpoint, payload=None) -> Response
    def delete(endpoint) -> Response
    def send(request_bundle: dict) -> Response  # Preferred — uses builder bundles
```

## Request Builder Pattern

Builders in `api_endpoints.py` return a bundle dict with everything `send()` needs:

```python
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

Bundle keys: `method`, `base_url`, `endpoint`, `auth_token`, `payload` (optional), `params` (optional)

## How to Write a Test

Tests only pass field values — no URLs, methods, or payload structure:

```python
from api_endpoints import build_create_order

def test_create_order_returns_201(api_client):
    response = api_client.send(build_create_order())
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

def test_create_order_with_custom_qty(api_client):
    response = api_client.send(build_create_order(qty=5, size="12"))
    assert response.status_code == 201
```

## Dynamic Path Variables

Use `.format()` in the builder for path params:

```python
GET_ORDER_BY_ID = "/orders/{order_id}"

def build_get_order(order_id):
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_ORDER_BY_ID.format(order_id=order_id),
        "auth_token": API_AUTH_TOKEN,
    }
```

## Additional API Clients

### GraphQL (framework/graphql_client.py)
```python
client = GraphQLClient(endpoint)
result = client.query("query { Account { Name } }")
GraphQLClient.assert_no_errors(result)
```

### SOAP/XML (framework/soap_client.py)
```python
client = SOAPClient(endpoint, namespace="http://example.com")
response = client.call("GetOrder", {"OrderId": "123"})
value = client.extract(response, "//OrderStatus")
```

### Request Chaining (framework/api_helpers.py)
```python
chain = RequestChain(api_client)
chain.post("/orders", json_data={"item": "shoes"})
chain.extract("order_id", "id")
chain.get("/orders/{order_id}")
chain.assert_status(200)
```

## Where Things Live
- Config (base URLs, timeouts): `api_endpoints.py`
- Endpoints (paths): `api_endpoints.py`
- Auth tokens (values): `.env` → loaded by `api_endpoints.py`
- Payload structure: builder functions in `api_endpoints.py`
- Payload field values: passed by tests
- HTTP client logic: `framework/api_helper.py`
