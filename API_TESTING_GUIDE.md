# REST API Testing Guide

This guide explains how to use the REST API testing capabilities in the Test Automation Framework.

## Table of Contents

1. [Overview](#overview)
2. [Configuration](#configuration)
3. [API Client Features](#api-client-features)
4. [Writing API Tests](#writing-api-tests)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

## Overview

The framework provides a robust API testing client with the following features:

- **Automatic retry logic** for failed requests
- **Built-in logging** for requests and responses
- **Session management** with connection pooling
- **Authentication support** (Bearer tokens, custom headers)
- **Response validation helpers**
- **SSL verification control**
- **Timeout configuration**

## Configuration

### config.yaml

Add API configuration to your `config.yaml`:

```yaml
api:
  base_url: "https://api.example.com"  # Your API base URL
  timeout: 30                           # Request timeout in seconds
  verify_ssl: true                      # SSL certificate verification
  default_headers:
    Content-Type: "application/json"
    Accept: "application/json"
    # Add any default headers here
```

### Environment-Specific Configuration

You can override configuration for different environments:

```yaml
# config.yaml
api:
  base_url: "https://api.staging.example.com"

# config.prod.yaml
api:
  base_url: "https://api.production.example.com"
```

## API Client Features

### Basic HTTP Methods

The API client supports all standard HTTP methods:

```python
# GET request
response = api_client.get('/users')

# POST request
response = api_client.post('/users', json_data={'name': 'John'})

# PUT request
response = api_client.put('/users/1', json_data={'name': 'Jane'})

# PATCH request
response = api_client.patch('/users/1', json_data={'email': 'new@example.com'})

# DELETE request
response = api_client.delete('/users/1')
```

### Query Parameters

```python
# Single parameter
response = api_client.get('/users', params={'role': 'admin'})

# Multiple parameters
response = api_client.get('/users', params={
    'role': 'admin',
    'status': 'active',
    'page': 1
})
```

### Custom Headers

```python
# Per-request headers
response = api_client.get('/users', headers={
    'X-Custom-Header': 'value',
    'X-Request-ID': '12345'
})

# Set default header for all requests
api_client.set_header('X-API-Version', 'v2')

# Remove a default header
api_client.remove_header('X-API-Version')
```

### Authentication

```python
# Bearer token authentication
api_client.set_auth_token('your-token-here')

# Custom token type
api_client.set_auth_token('your-token', token_type='Token')

# Remove authentication
api_client.remove_header('Authorization')
```

### Retry Strategy

The client automatically retries failed requests with exponential backoff:

- Retries on status codes: 429, 500, 502, 503, 504
- Default: 3 retries with 0.3s backoff factor
- Supports all HTTP methods

## Writing API Tests

### Basic Test Structure

```python
import pytest

class TestUserAPI:
    """Test user API endpoints."""
    
    def test_get_users(self, api_client):
        """Test retrieving users list."""
        response = api_client.get('/users')
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
    
    def test_create_user(self, api_client):
        """Test creating a new user."""
        new_user = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'user'
        }
        
        response = api_client.post('/users', json_data=new_user)
        
        assert response.status_code == 201
        created_user = response.json()
        assert created_user['name'] == new_user['name']
        assert 'id' in created_user
```

### Using APIResponse Wrapper

The `APIResponse` wrapper provides convenient assertion methods:

```python
def test_with_response_wrapper(api_client, api_response_wrapper):
    """Test using APIResponse wrapper."""
    response = api_client.get('/users/1')
    api_response = api_response_wrapper(response)
    
    # Status code assertions
    api_response.assert_status_code(200)
    api_response.assert_status_in([200, 201])
    
    # JSON content assertions
    api_response.assert_json_contains('id')
    api_response.assert_json_value('name', 'John Doe')
    
    # Header assertions
    api_response.assert_header_exists('Content-Type')
    
    # Get values safely
    user_id = api_response.get_json_value('id')
    email = api_response.get_json_value('email', default='no-email')
```

### Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "John Doe"),
    (2, "Jane Smith"),
    (3, "Bob Johnson")
])
def test_get_user_by_id(api_client, user_id, expected_name):
    """Test retrieving specific users."""
    response = api_client.get(f'/users/{user_id}')
    
    assert response.status_code == 200
    user = response.json()
    assert user['name'] == expected_name
```

### Error Handling Tests

```python
def test_not_found_error(api_client):
    """Test 404 error handling."""
    response = api_client.get('/users/99999')
    assert response.status_code == 404

def test_validation_error(api_client):
    """Test 400 validation error."""
    invalid_user = {'name': ''}  # Missing required fields
    
    response = api_client.post('/users', json_data=invalid_user)
    assert response.status_code == 400
    
    error = response.json()
    assert 'error' in error or 'message' in error

def test_unauthorized_access(api_client):
    """Test 401 unauthorized error."""
    # Remove authentication
    api_client.remove_header('Authorization')
    
    response = api_client.get('/admin/users')
    assert response.status_code == 401
```

## Advanced Usage

### Custom Request Configuration

```python
def test_custom_timeout(api_client):
    """Test with custom timeout."""
    response = api_client.get('/slow-endpoint', timeout=60)
    assert response.status_code == 200

def test_disable_ssl_verification(api_client):
    """Test with SSL verification disabled."""
    response = api_client.get('/endpoint', verify=False)
    assert response.status_code == 200
```

### Response Validation

```python
def test_validate_response_schema(api_client):
    """Test response matches expected schema."""
    response = api_client.get('/users/1')
    user = response.json()
    
    # Validate required fields
    required_fields = ['id', 'name', 'email', 'created_at']
    for field in required_fields:
        assert field in user, f"Missing field: {field}"
    
    # Validate data types
    assert isinstance(user['id'], int)
    assert isinstance(user['name'], str)
    assert isinstance(user['email'], str)
    
    # Validate email format
    assert '@' in user['email']
```

### Chaining Requests

```python
def test_create_and_update_user(api_client):
    """Test creating and then updating a user."""
    # Create user
    new_user = {'name': 'John Doe', 'email': 'john@example.com'}
    create_response = api_client.post('/users', json_data=new_user)
    assert create_response.status_code == 201
    
    user_id = create_response.json()['id']
    
    # Update user
    update_data = {'name': 'John Updated'}
    update_response = api_client.patch(f'/users/{user_id}', json_data=update_data)
    assert update_response.status_code == 200
    
    # Verify update
    get_response = api_client.get(f'/users/{user_id}')
    updated_user = get_response.json()
    assert updated_user['name'] == 'John Updated'
```

### File Upload

```python
def test_file_upload(api_client):
    """Test uploading a file."""
    files = {'file': open('test_file.txt', 'rb')}
    
    response = api_client.post('/upload', files=files)
    assert response.status_code == 200
```

### Working with Different Content Types

```python
def test_form_data(api_client):
    """Test sending form data."""
    form_data = {
        'username': 'john',
        'password': 'secret'
    }
    
    response = api_client.post('/login', data=form_data)
    assert response.status_code == 200

def test_xml_response(api_client):
    """Test handling XML response."""
    response = api_client.get('/data.xml')
    
    assert response.status_code == 200
    assert 'xml' in response.headers['Content-Type'].lower()
    
    # Parse XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(response.text)
    # Process XML...
```

## Best Practices

### 1. Use Fixtures for Setup/Teardown

```python
@pytest.fixture
def test_user(api_client):
    """Create a test user and clean up after test."""
    # Setup
    user_data = {'name': 'Test User', 'email': 'test@example.com'}
    response = api_client.post('/users', json_data=user_data)
    user = response.json()
    
    yield user
    
    # Teardown
    api_client.delete(f'/users/{user["id"]}')

def test_with_test_user(api_client, test_user):
    """Test using the test user fixture."""
    response = api_client.get(f'/users/{test_user["id"]}')
    assert response.status_code == 200
```

### 2. Organize Tests by Resource

```python
# tests/api/test_users.py
class TestUserAPI:
    """Tests for user endpoints."""
    pass

# tests/api/test_products.py
class TestProductAPI:
    """Tests for product endpoints."""
    pass
```

### 3. Use Descriptive Test Names

```python
def test_get_user_returns_200_with_valid_id():
    """Good: Clear what is being tested and expected outcome."""
    pass

def test_user():
    """Bad: Unclear what is being tested."""
    pass
```

### 4. Test Both Success and Failure Cases

```python
class TestUserCreation:
    def test_create_user_with_valid_data_succeeds(self, api_client):
        """Test successful user creation."""
        pass
    
    def test_create_user_with_missing_email_fails(self, api_client):
        """Test validation error for missing email."""
        pass
    
    def test_create_user_with_duplicate_email_fails(self, api_client):
        """Test duplicate email rejection."""
        pass
```

### 5. Use Environment Variables for Sensitive Data

```python
import os

def test_with_api_key(api_client):
    """Test using API key from environment."""
    api_key = os.getenv('API_KEY')
    api_client.set_header('X-API-Key', api_key)
    
    response = api_client.get('/protected-endpoint')
    assert response.status_code == 200
```

### 6. Log Important Information

```python
import logging

def test_with_logging(api_client):
    """Test with detailed logging."""
    logger = logging.getLogger(__name__)
    
    response = api_client.get('/users')
    logger.info(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.text}")
    
    assert response.status_code == 200
```

### 7. Use Markers for Test Organization

```python
@pytest.mark.smoke
def test_api_health_check(api_client):
    """Smoke test for API availability."""
    response = api_client.get('/health')
    assert response.status_code == 200

@pytest.mark.regression
def test_complex_user_workflow(api_client):
    """Regression test for user workflow."""
    pass
```

## Running API Tests

```bash
# Run all API tests
pytest tests/api/

# Run specific test file
pytest tests/api/test_users.py

# Run with verbose output
pytest tests/api/ -v

# Run tests matching pattern
pytest tests/api/ -k "create_user"

# Run with markers
pytest tests/api/ -m smoke
```

## Troubleshooting

### Connection Errors

```python
# Increase timeout for slow endpoints
response = api_client.get('/slow-endpoint', timeout=120)

# Disable SSL verification for self-signed certificates
response = api_client.get('/endpoint', verify=False)
```

### Authentication Issues

```python
# Verify token is set correctly
api_client.set_auth_token('your-token')
print(api_client.default_headers)  # Check Authorization header

# Test without authentication first
api_client.remove_header('Authorization')
response = api_client.get('/public-endpoint')
```

### Response Parsing Errors

```python
# Check if response is actually JSON
try:
    data = response.json()
except ValueError:
    print(f"Response is not JSON: {response.text}")
```

## Additional Resources

- [Requests Documentation](https://requests.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [REST API Best Practices](https://restfulapi.net/)
