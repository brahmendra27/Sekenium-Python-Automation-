# Tests Directory

This directory contains all test files for the Test Automation Framework.

## Directory Structure

```
tests/
├── api/                    # REST API tests
│   └── test_api_example.py
├── database/               # MongoDB database tests
│   └── test_mongodb_example.py
└── README.md              # This file
```

## Test Types

### API Tests (`tests/api/`)

REST API tests using the `api_client` fixture. These tests verify:
- HTTP endpoints (GET, POST, PUT, PATCH, DELETE)
- Request/response validation
- Authentication and authorization
- Error handling
- API data contracts

**Example:**
```python
def test_get_user(api_client):
    response = api_client.get('/users/1')
    assert response.status_code == 200
```

**Run API tests:**
```bash
pytest tests/api/ -v
```

### Database Tests (`tests/database/`)

MongoDB database tests using the `mongodb_client` fixture. These tests verify:
- CRUD operations
- Query operations
- Data integrity
- Indexes and constraints
- Aggregation pipelines

**Example:**
```python
def test_insert_user(mongodb_client, clean_mongodb_collection):
    clean_mongodb_collection('users')
    doc_id = mongodb_client.insert_one('users', {'name': 'John'})
    assert doc_id is not None
```

**Run database tests:**
```bash
pytest tests/database/ -v
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/api/test_api_example.py -v
```

### Run Specific Test
```bash
pytest tests/api/test_api_example.py::test_get_request -v
```

### Run with Markers
```bash
pytest tests/ -m smoke -v
```

### Run with Coverage
```bash
pytest tests/ --cov=framework --cov-report=html
```

## Writing New Tests

### 1. Choose the Right Directory

- **API tests** → `tests/api/`
- **Database tests** → `tests/database/`
- **Integration tests** → Create `tests/integration/`

### 2. Use Appropriate Fixtures

**For API tests:**
```python
def test_my_api(api_client):
    response = api_client.get('/endpoint')
    assert response.status_code == 200
```

**For database tests:**
```python
def test_my_database(mongodb_client, clean_mongodb_collection):
    clean_mongodb_collection('my_collection')
    # Your test code
```

**For integration tests:**
```python
def test_integration(api_client, mongodb_client, clean_mongodb_collection):
    # Test API and database together
    pass
```

### 3. Follow Naming Conventions

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### 4. Use Descriptive Names

```python
# Good
def test_user_creation_with_valid_data_succeeds():
    pass

# Bad
def test_user():
    pass
```

## Available Fixtures

### API Testing Fixtures

- `api_client` - HTTP client for making API requests
- `api_response_wrapper` - Wrapper for response assertions
- `config` - Configuration object

### Database Testing Fixtures

- `mongodb_client` - MongoDB client for database operations
- `mongodb_test_helper` - Test helper with automatic cleanup
- `clean_mongodb_collection` - Collection cleanup utility

### Shared Fixtures

- `config` - Framework configuration

## Example Test Templates

### API Test Template

```python
import pytest

class TestMyAPI:
    """Test my API endpoints."""
    
    def test_get_resource(self, api_client):
        """Test retrieving a resource."""
        response = api_client.get('/resource/1')
        
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
    
    def test_create_resource(self, api_client):
        """Test creating a resource."""
        new_resource = {'name': 'Test', 'value': 123}
        
        response = api_client.post('/resource', json_data=new_resource)
        
        assert response.status_code == 201
        created = response.json()
        assert created['name'] == new_resource['name']
```

### Database Test Template

```python
import pytest

class TestMyDatabase:
    """Test my database operations."""
    
    def test_insert_document(self, mongodb_client, clean_mongodb_collection):
        """Test inserting a document."""
        collection_name = 'my_collection'
        clean_mongodb_collection(collection_name)
        
        doc_data = {'name': 'Test', 'value': 123}
        doc_id = mongodb_client.insert_one(collection_name, doc_data)
        
        assert doc_id is not None
        
        # Verify insertion
        doc = mongodb_client.find_one(collection_name, {'name': 'Test'})
        assert doc['value'] == 123
    
    def test_query_documents(self, mongodb_test_helper):
        """Test querying documents."""
        collection_name = 'my_collection'
        
        # Setup test data
        test_data = [
            {'name': 'Item 1', 'status': 'active'},
            {'name': 'Item 2', 'status': 'inactive'}
        ]
        
        mongodb_test_helper.setup_test_collection(collection_name, test_data)
        
        # Query active items
        active_items = mongodb_test_helper.client.find_many(
            collection_name,
            {'status': 'active'}
        )
        
        assert len(active_items) == 1
```

### Integration Test Template

```python
import pytest

class TestIntegration:
    """Test API and database integration."""
    
    def test_api_database_flow(self, api_client, mongodb_client, clean_mongodb_collection):
        """Test complete flow from API to database."""
        collection_name = 'resources'
        clean_mongodb_collection(collection_name)
        
        # Step 1: Create via API
        new_resource = {'name': 'Test Resource'}
        api_response = api_client.post('/resources', json_data=new_resource)
        
        assert api_response.status_code == 201
        resource_id = api_response.json()['id']
        
        # Step 2: Verify in database
        db_resource = mongodb_client.find_one(collection_name, {'_id': resource_id})
        assert db_resource is not None
        assert db_resource['name'] == new_resource['name']
        
        # Step 3: Update via API
        update_data = {'name': 'Updated Resource'}
        update_response = api_client.patch(
            f'/resources/{resource_id}',
            json_data=update_data
        )
        
        assert update_response.status_code == 200
        
        # Step 4: Verify update in database
        updated_resource = mongodb_client.find_one(collection_name, {'_id': resource_id})
        assert updated_resource['name'] == 'Updated Resource'
```

## Test Organization Best Practices

1. **Group related tests in classes**
   ```python
   class TestUserAPI:
       def test_create_user(self): pass
       def test_get_user(self): pass
       def test_update_user(self): pass
   ```

2. **Use descriptive docstrings**
   ```python
   def test_user_creation():
       """Test that users can be created with valid data."""
       pass
   ```

3. **One assertion concept per test**
   - Test one thing at a time
   - Makes failures easier to diagnose

4. **Use fixtures for setup/teardown**
   - Avoid code duplication
   - Ensure proper cleanup

5. **Use markers for test categorization**
   ```python
   @pytest.mark.smoke
   def test_critical_feature():
       pass
   ```

## Debugging Tests

### Run with verbose output
```bash
pytest tests/ -v -s
```

### Run specific test with print statements
```bash
pytest tests/api/test_api_example.py::test_get_request -v -s
```

### Run with pdb debugger
```bash
pytest tests/ --pdb
```

### View test coverage
```bash
pytest tests/ --cov=framework --cov-report=term-missing
```

## Documentation

For detailed information, see:
- [API Testing Guide](../API_TESTING_GUIDE.md)
- [MongoDB Testing Guide](../MONGODB_TESTING_GUIDE.md)
- [Integration Testing Guide](../API_AND_DATABASE_INTEGRATION_GUIDE.md)
- [Quick Start Guide](../API_DATABASE_QUICK_START.md)

## Need Help?

1. Check the example tests in this directory
2. Review the documentation guides
3. Look at the framework source code in `framework/`
4. Check `conftest.py` for available fixtures
