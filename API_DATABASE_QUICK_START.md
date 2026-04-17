# API and Database Testing - Quick Start Guide

Get started with REST API and MongoDB testing in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- MongoDB installed and running (for database tests)
- Internet connection (for API tests with external APIs)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP client for API testing
- `pymongo` - MongoDB driver
- `jsonschema` - JSON validation
- All existing framework dependencies

### 2. Install Playwright (if not already installed)

```bash
playwright install
```

### 3. Start MongoDB (for database tests)

**Windows:**
```bash
net start MongoDB
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

## Configuration

### Update config.yaml

Add API and MongoDB settings to your `config.yaml`:

```yaml
# Existing configuration...
base_url: "https://automationteststore.com/"
browser: "chrome"
headless: false

# API Testing Configuration
api:
  base_url: "https://jsonplaceholder.typicode.com"  # Example API
  timeout: 30
  verify_ssl: true
  default_headers:
    Content-Type: "application/json"
    Accept: "application/json"

# MongoDB Configuration
mongodb:
  connection_string: "mongodb://localhost:27017"
  database: "test_db"
  timeout: 5000
  max_pool_size: 10
```

## Your First API Test

Create `tests/api/test_my_first_api.py`:

```python
import pytest

def test_get_posts(api_client):
    """Test retrieving posts from API."""
    response = api_client.get('/posts')
    
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    print(f"✓ Retrieved {len(posts)} posts")

def test_create_post(api_client):
    """Test creating a new post."""
    new_post = {
        'title': 'My First Test Post',
        'body': 'This is a test post created by automation',
        'userId': 1
    }
    
    response = api_client.post('/posts', json_data=new_post)
    
    assert response.status_code == 201
    created_post = response.json()
    assert created_post['title'] == new_post['title']
    print(f"✓ Created post with ID: {created_post['id']}")
```

### Run Your API Test

```bash
pytest tests/api/test_my_first_api.py -v
```

Expected output:
```
tests/api/test_my_first_api.py::test_get_posts PASSED
tests/api/test_my_first_api.py::test_create_post PASSED
```

## Your First MongoDB Test

Create `tests/database/test_my_first_db.py`:

```python
import pytest

def test_insert_and_find(mongodb_client, clean_mongodb_collection):
    """Test inserting and finding a document."""
    collection_name = 'test_users'
    clean_mongodb_collection(collection_name)
    
    # Insert a user
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    
    doc_id = mongodb_client.insert_one(collection_name, user_data)
    print(f"✓ Inserted document with ID: {doc_id}")
    
    # Find the user
    found_user = mongodb_client.find_one(collection_name, {'name': 'John Doe'})
    
    assert found_user is not None
    assert found_user['email'] == 'john@example.com'
    assert found_user['age'] == 30
    print(f"✓ Found user: {found_user['name']}")

def test_update_document(mongodb_client, clean_mongodb_collection):
    """Test updating a document."""
    collection_name = 'test_products'
    clean_mongodb_collection(collection_name)
    
    # Insert product
    product = {'name': 'Laptop', 'price': 999.99, 'stock': 10}
    mongodb_client.insert_one(collection_name, product)
    
    # Update price
    mongodb_client.update_one(
        collection_name,
        {'name': 'Laptop'},
        {'$set': {'price': 899.99}}
    )
    
    # Verify update
    updated_product = mongodb_client.find_one(collection_name, {'name': 'Laptop'})
    assert updated_product['price'] == 899.99
    print(f"✓ Updated product price to ${updated_product['price']}")
```

### Run Your MongoDB Test

```bash
pytest tests/database/test_my_first_db.py -v
```

Expected output:
```
tests/database/test_my_first_db.py::test_insert_and_find PASSED
tests/database/test_my_first_db.py::test_update_document PASSED
```

## Your First Integration Test

Create `tests/integration/test_my_first_integration.py`:

```python
import pytest

def test_api_to_database_flow(api_client, mongodb_client, clean_mongodb_collection):
    """Test that API operations persist to database."""
    collection_name = 'api_users'
    clean_mongodb_collection(collection_name)
    
    # Step 1: Create user via API
    new_user = {
        'name': 'Integration Test User',
        'email': 'integration@example.com',
        'username': 'integrationuser'
    }
    
    api_response = api_client.post('/users', json_data=new_user)
    assert api_response.status_code == 201
    
    user_id = api_response.json()['id']
    print(f"✓ Created user via API with ID: {user_id}")
    
    # Step 2: Verify in database
    # Note: This assumes your API writes to the same MongoDB
    # For the example API, we'll just verify the API response
    api_user = api_response.json()
    assert api_user['name'] == new_user['name']
    print(f"✓ Verified user data: {api_user['name']}")
    
    # Step 3: Retrieve via API
    get_response = api_client.get(f'/users/{user_id}')
    assert get_response.status_code == 200
    
    retrieved_user = get_response.json()
    assert retrieved_user['name'] == new_user['name']
    print(f"✓ Retrieved user via API: {retrieved_user['name']}")
```

### Run Your Integration Test

```bash
pytest tests/integration/test_my_first_integration.py -v
```

## Common Use Cases

### Use Case 1: Test with Authentication

```python
def test_with_auth(api_client):
    """Test API with authentication."""
    # Set authentication token
    api_client.set_auth_token('your-api-token-here')
    
    # Make authenticated request
    response = api_client.get('/protected-endpoint')
    assert response.status_code == 200
```

### Use Case 2: Test with Query Parameters

```python
def test_with_query_params(api_client):
    """Test API with query parameters."""
    response = api_client.get('/posts', params={
        'userId': 1,
        'limit': 10
    })
    
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) <= 10
```

### Use Case 3: Test MongoDB Aggregation

```python
def test_aggregation(mongodb_client, clean_mongodb_collection):
    """Test MongoDB aggregation."""
    collection_name = 'sales'
    clean_mongodb_collection(collection_name)
    
    # Insert sales data
    sales = [
        {'product': 'A', 'amount': 100, 'category': 'Electronics'},
        {'product': 'B', 'amount': 200, 'category': 'Electronics'},
        {'product': 'C', 'amount': 150, 'category': 'Furniture'}
    ]
    mongodb_client.insert_many(collection_name, sales)
    
    # Aggregate by category
    pipeline = [
        {
            '$group': {
                '_id': '$category',
                'total': {'$sum': '$amount'}
            }
        }
    ]
    
    results = mongodb_client.aggregate(collection_name, pipeline)
    
    electronics_total = next(r for r in results if r['_id'] == 'Electronics')
    assert electronics_total['total'] == 300
```

## Running Tests

### Run All Tests

```bash
# Run everything
pytest tests/ -v

# Run with detailed output
pytest tests/ -v -s
```

### Run Specific Test Types

```bash
# API tests only
pytest tests/api/ -v

# Database tests only
pytest tests/database/ -v

# Integration tests only
pytest tests/integration/ -v
```

### Run with Markers

```bash
# Run smoke tests
pytest tests/ -m smoke -v

# Run regression tests
pytest tests/ -m regression -v
```

### Generate Reports

```bash
# HTML report
pytest tests/ --html=reports/report.html

# Allure report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Troubleshooting

### API Tests Failing

**Problem:** Connection errors or timeouts

**Solution:**
```yaml
# Increase timeout in config.yaml
api:
  timeout: 60  # Increase to 60 seconds
```

**Problem:** SSL certificate errors

**Solution:**
```yaml
# Disable SSL verification (not recommended for production)
api:
  verify_ssl: false
```

### MongoDB Tests Failing

**Problem:** Connection refused

**Solution:**
```bash
# Check if MongoDB is running
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

**Problem:** Authentication failed

**Solution:**
```yaml
# Add credentials to connection string
mongodb:
  connection_string: "mongodb://username:password@localhost:27017"
```

## Next Steps

1. **Read the detailed guides:**
   - [API Testing Guide](API_TESTING_GUIDE.md)
   - [MongoDB Testing Guide](MONGODB_TESTING_GUIDE.md)
   - [Integration Testing Guide](API_AND_DATABASE_INTEGRATION_GUIDE.md)

2. **Explore example tests:**
   - `tests/api/test_api_example.py`
   - `tests/database/test_mongodb_example.py`

3. **Customize configuration:**
   - Update `config.yaml` with your API endpoints
   - Configure MongoDB connection for your environment

4. **Write your own tests:**
   - Start with simple CRUD operations
   - Add authentication and authorization tests
   - Build complex integration test scenarios

## Quick Reference

### API Client Methods

```python
# HTTP Methods
api_client.get('/endpoint')
api_client.post('/endpoint', json_data={...})
api_client.put('/endpoint', json_data={...})
api_client.patch('/endpoint', json_data={...})
api_client.delete('/endpoint')

# Authentication
api_client.set_auth_token('token')
api_client.set_header('X-Custom', 'value')
api_client.remove_header('X-Custom')
```

### MongoDB Client Methods

```python
# CRUD Operations
mongodb_client.insert_one('collection', {...})
mongodb_client.insert_many('collection', [{...}, {...}])
mongodb_client.find_one('collection', {'key': 'value'})
mongodb_client.find_many('collection', {'key': 'value'})
mongodb_client.update_one('collection', query, {'$set': {...}})
mongodb_client.update_many('collection', query, {'$set': {...}})
mongodb_client.delete_one('collection', query)
mongodb_client.delete_many('collection', query)

# Utilities
mongodb_client.count_documents('collection', query)
mongodb_client.aggregate('collection', pipeline)
mongodb_client.create_index('collection', 'field', unique=True)
```

## Support

For issues or questions:
1. Check the detailed guides in the documentation
2. Review example tests in `tests/api/` and `tests/database/`
3. Refer to the framework documentation

Happy Testing! 🚀
