# MongoDB Testing Guide

This guide explains how to use the MongoDB testing capabilities in the Test Automation Framework.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [MongoDB Client Features](#mongodb-client-features)
5. [Writing Database Tests](#writing-database-tests)
6. [Test Helper Utilities](#test-helper-utilities)
7. [Advanced Usage](#advanced-usage)
8. [Best Practices](#best-practices)

## Overview

The framework provides comprehensive MongoDB testing capabilities with:

- **Connection management** with automatic pooling
- **CRUD operations** (Create, Read, Update, Delete)
- **Query operations** with filtering, sorting, and limiting
- **Aggregation pipeline** support
- **Index management**
- **Test helpers** for setup/teardown
- **Assertion utilities** for validation

## Setup

### Install MongoDB

#### Windows
```bash
# Download from MongoDB website or use Chocolatey
choco install mongodb

# Start MongoDB service
net start MongoDB
```

#### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# Start service
sudo systemctl start mongod
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pymongo` - MongoDB driver
- `motor` - Async MongoDB driver (for async operations)

## Configuration

### config.yaml

Add MongoDB configuration to your `config.yaml`:

```yaml
mongodb:
  connection_string: "mongodb://localhost:27017"
  database: "test_db"
  timeout: 5000          # Connection timeout in milliseconds
  max_pool_size: 10      # Maximum connection pool size
```

### Connection String Formats

```yaml
# Local MongoDB
connection_string: "mongodb://localhost:27017"

# MongoDB with authentication
connection_string: "mongodb://username:password@localhost:27017"

# MongoDB Atlas (cloud)
connection_string: "mongodb+srv://username:password@cluster.mongodb.net"

# Replica set
connection_string: "mongodb://host1:27017,host2:27017,host3:27017/?replicaSet=myReplicaSet"
```

### Environment-Specific Configuration

```yaml
# config.yaml (development)
mongodb:
  connection_string: "mongodb://localhost:27017"
  database: "test_db"

# config.prod.yaml (production)
mongodb:
  connection_string: "mongodb://prod-server:27017"
  database: "production_db"
```

## MongoDB Client Features

### Connection Management

```python
from framework.mongodb_client import MongoDBClient

# Create client
client = MongoDBClient()

# Connect to database
client.connect()

# Use the client...

# Disconnect when done
client.disconnect()
```

### CRUD Operations

#### Create (Insert)

```python
# Insert single document
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
}
doc_id = mongodb_client.insert_one('users', user_data)

# Insert multiple documents
users = [
    {'name': 'User 1', 'email': 'user1@example.com'},
    {'name': 'User 2', 'email': 'user2@example.com'}
]
doc_ids = mongodb_client.insert_many('users', users)
```

#### Read (Find)

```python
# Find single document
user = mongodb_client.find_one('users', {'name': 'John Doe'})

# Find multiple documents
users = mongodb_client.find_many('users', {'age': {'$gt': 25}})

# Find with sorting
users = mongodb_client.find_many(
    'users',
    {},
    sort=[('age', -1)]  # -1 for descending, 1 for ascending
)

# Find with limit
users = mongodb_client.find_many('users', {}, limit=10)

# Count documents
count = mongodb_client.count_documents('users', {'age': {'$gt': 25}})
```

#### Update

```python
# Update single document
mongodb_client.update_one(
    'users',
    {'name': 'John Doe'},
    {'$set': {'age': 31}}
)

# Update multiple documents
mongodb_client.update_many(
    'users',
    {'status': 'inactive'},
    {'$set': {'archived': True}}
)

# Upsert (update or insert)
mongodb_client.update_one(
    'settings',
    {'key': 'theme'},
    {'$set': {'value': 'dark'}},
    upsert=True
)
```

#### Delete

```python
# Delete single document
mongodb_client.delete_one('users', {'name': 'John Doe'})

# Delete multiple documents
mongodb_client.delete_many('users', {'status': 'deleted'})

# Drop entire collection
mongodb_client.drop_collection('temp_collection')
```

### Query Operators

```python
# Comparison operators
users = mongodb_client.find_many('users', {'age': {'$gt': 25}})  # Greater than
users = mongodb_client.find_many('users', {'age': {'$gte': 25}})  # Greater than or equal
users = mongodb_client.find_many('users', {'age': {'$lt': 50}})  # Less than
users = mongodb_client.find_many('users', {'age': {'$lte': 50}})  # Less than or equal
users = mongodb_client.find_many('users', {'age': {'$ne': 30}})  # Not equal

# Logical operators
users = mongodb_client.find_many('users', {
    '$and': [
        {'age': {'$gt': 25}},
        {'status': 'active'}
    ]
})

users = mongodb_client.find_many('users', {
    '$or': [
        {'role': 'admin'},
        {'role': 'moderator'}
    ]
})

# Array operators
users = mongodb_client.find_many('users', {
    'tags': {'$in': ['python', 'javascript']}
})

# Text search
users = mongodb_client.find_many('users', {
    'name': {'$regex': 'John', '$options': 'i'}  # Case-insensitive
})
```

### Aggregation Pipeline

```python
# Group and sum
pipeline = [
    {
        '$group': {
            '_id': '$category',
            'total': {'$sum': '$amount'},
            'count': {'$sum': 1}
        }
    },
    {'$sort': {'total': -1}}
]

results = mongodb_client.aggregate('sales', pipeline)

# Match, group, and project
pipeline = [
    {'$match': {'status': 'completed'}},
    {
        '$group': {
            '_id': '$user_id',
            'total_spent': {'$sum': '$amount'},
            'order_count': {'$sum': 1}
        }
    },
    {
        '$project': {
            'user_id': '$_id',
            'total_spent': 1,
            'order_count': 1,
            'average_order': {'$divide': ['$total_spent', '$order_count']}
        }
    }
]

results = mongodb_client.aggregate('orders', pipeline)
```

### Index Management

```python
# Create single field index
mongodb_client.create_index('users', 'email', unique=True)

# Create compound index
mongodb_client.create_index('users', [('last_name', 1), ('first_name', 1)])

# List collections
collections = mongodb_client.list_collections()
```

## Writing Database Tests

### Basic Test Structure

```python
import pytest

class TestUserDatabase:
    """Test user database operations."""
    
    def test_insert_user(self, mongodb_client, clean_mongodb_collection):
        """Test inserting a user."""
        collection_name = 'users'
        clean_mongodb_collection(collection_name)
        
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30
        }
        
        doc_id = mongodb_client.insert_one(collection_name, user_data)
        assert doc_id is not None
        
        # Verify insertion
        user = mongodb_client.find_one(collection_name, {'name': 'John Doe'})
        assert user is not None
        assert user['email'] == 'john@example.com'
```

### Using Test Helper

```python
def test_with_test_helper(mongodb_test_helper):
    """Test using MongoDB test helper."""
    collection_name = 'products'
    
    # Setup collection with initial data
    initial_data = [
        {'name': 'Product 1', 'price': 10.99},
        {'name': 'Product 2', 'price': 20.99}
    ]
    
    mongodb_test_helper.setup_test_collection(collection_name, initial_data)
    
    # Run tests
    count = mongodb_test_helper.client.count_documents(collection_name, {})
    assert count == 2
    
    # Cleanup happens automatically
```

### Assertion Helpers

```python
def test_with_assertions(mongodb_test_helper):
    """Test using assertion helpers."""
    collection_name = 'orders'
    
    # Setup
    mongodb_test_helper.setup_test_collection(collection_name, [
        {'order_id': '001', 'status': 'pending', 'amount': 100},
        {'order_id': '002', 'status': 'completed', 'amount': 200}
    ])
    
    # Assert document exists
    mongodb_test_helper.assert_document_exists(
        collection_name,
        {'order_id': '001'}
    )
    
    # Assert document count
    mongodb_test_helper.assert_document_count(collection_name, 2)
    mongodb_test_helper.assert_document_count(
        collection_name,
        1,
        {'status': 'pending'}
    )
    
    # Assert field value
    mongodb_test_helper.assert_field_value(
        collection_name,
        {'order_id': '001'},
        'status',
        'pending'
    )
```

## Test Helper Utilities

### Setup Test Collection

```python
def test_setup_collection(mongodb_test_helper):
    """Setup a test collection with data."""
    mongodb_test_helper.setup_test_collection('users', [
        {'name': 'User 1', 'email': 'user1@example.com'},
        {'name': 'User 2', 'email': 'user2@example.com'}
    ])
    
    # Collection is ready for testing
```

### Create Test Document

```python
def test_create_document(mongodb_test_helper):
    """Create a test document with metadata."""
    doc = mongodb_test_helper.create_test_document(
        name='Test Item',
        value=123,
        status='active'
    )
    
    # Document includes:
    # - created_at: timestamp
    # - test_marker: True
    # - Your custom fields
    
    assert doc['name'] == 'Test Item'
    assert 'created_at' in doc
    assert doc['test_marker'] is True
```

### Automatic Cleanup

```python
def test_automatic_cleanup(mongodb_test_helper):
    """Test collections are cleaned up automatically."""
    # Setup multiple collections
    mongodb_test_helper.setup_test_collection('collection1', [{'data': 1}])
    mongodb_test_helper.setup_test_collection('collection2', [{'data': 2}])
    
    # Test your logic...
    
    # All collections tracked by test_helper are cleaned up automatically
    # after the test completes
```

## Advanced Usage

### Testing Data Relationships

```python
def test_user_orders_relationship(mongodb_client, clean_mongodb_collection):
    """Test relationship between users and orders."""
    clean_mongodb_collection('users')
    clean_mongodb_collection('orders')
    
    # Create user
    user_id = mongodb_client.insert_one('users', {
        'name': 'John Doe',
        'email': 'john@example.com'
    })
    
    # Create orders for user
    orders = [
        {'user_id': user_id, 'product': 'Product 1', 'amount': 100},
        {'user_id': user_id, 'product': 'Product 2', 'amount': 200}
    ]
    mongodb_client.insert_many('orders', orders)
    
    # Query orders for user
    user_orders = mongodb_client.find_many('orders', {'user_id': user_id})
    assert len(user_orders) == 2
    
    # Calculate total
    total = sum(order['amount'] for order in user_orders)
    assert total == 300
```

### Testing Aggregations

```python
def test_sales_aggregation(mongodb_client, clean_mongodb_collection):
    """Test sales aggregation pipeline."""
    collection_name = 'sales'
    clean_mongodb_collection(collection_name)
    
    # Insert test data
    sales = [
        {'product': 'A', 'category': 'Electronics', 'amount': 1000},
        {'product': 'B', 'category': 'Electronics', 'amount': 500},
        {'product': 'C', 'category': 'Furniture', 'amount': 300}
    ]
    mongodb_client.insert_many(collection_name, sales)
    
    # Aggregate by category
    pipeline = [
        {
            '$group': {
                '_id': '$category',
                'total': {'$sum': '$amount'},
                'count': {'$sum': 1}
            }
        }
    ]
    
    results = mongodb_client.aggregate(collection_name, pipeline)
    
    # Verify results
    electronics = next(r for r in results if r['_id'] == 'Electronics')
    assert electronics['total'] == 1500
    assert electronics['count'] == 2
```

### Testing Indexes

```python
def test_unique_index(mongodb_client, clean_mongodb_collection):
    """Test unique index enforcement."""
    collection_name = 'users'
    clean_mongodb_collection(collection_name)
    
    # Create unique index on email
    mongodb_client.create_index(collection_name, 'email', unique=True)
    
    # Insert first user
    mongodb_client.insert_one(collection_name, {
        'name': 'User 1',
        'email': 'user@example.com'
    })
    
    # Try to insert duplicate email
    with pytest.raises(Exception):
        mongodb_client.insert_one(collection_name, {
            'name': 'User 2',
            'email': 'user@example.com'
        })
```

### Testing Updates

```python
def test_complex_update(mongodb_client, clean_mongodb_collection):
    """Test complex update operations."""
    collection_name = 'products'
    clean_mongodb_collection(collection_name)
    
    # Insert product
    mongodb_client.insert_one(collection_name, {
        'name': 'Product 1',
        'price': 100,
        'stock': 50,
        'tags': ['electronics']
    })
    
    # Update with multiple operations
    mongodb_client.update_one(
        collection_name,
        {'name': 'Product 1'},
        {
            '$set': {'price': 90},
            '$inc': {'stock': -5},
            '$push': {'tags': 'sale'}
        }
    )
    
    # Verify update
    product = mongodb_client.find_one(collection_name, {'name': 'Product 1'})
    assert product['price'] == 90
    assert product['stock'] == 45
    assert 'sale' in product['tags']
```

## Best Practices

### 1. Use Fixtures for Database Setup

```python
@pytest.fixture
def sample_users(mongodb_client, clean_mongodb_collection):
    """Provide sample users for testing."""
    collection_name = 'users'
    clean_mongodb_collection(collection_name)
    
    users = [
        {'name': 'User 1', 'role': 'admin'},
        {'name': 'User 2', 'role': 'user'},
        {'name': 'User 3', 'role': 'user'}
    ]
    
    mongodb_client.insert_many(collection_name, users)
    return collection_name

def test_with_sample_users(mongodb_client, sample_users):
    """Test using sample users fixture."""
    admin_count = mongodb_client.count_documents(
        sample_users,
        {'role': 'admin'}
    )
    assert admin_count == 1
```

### 2. Clean Up Test Data

```python
# Use clean_mongodb_collection fixture
def test_with_cleanup(mongodb_client, clean_mongodb_collection):
    collection_name = 'test_collection'
    clean_mongodb_collection(collection_name)
    
    # Your test code...
    # Collection is automatically cleaned after test

# Or use mongodb_test_helper
def test_with_helper(mongodb_test_helper):
    mongodb_test_helper.setup_test_collection('test_collection', [])
    # Automatic cleanup after test
```

### 3. Test Data Isolation

```python
# Use unique collection names per test
def test_isolated_data(mongodb_client):
    collection_name = f'test_{uuid.uuid4()}'
    
    # Test with isolated collection
    mongodb_client.insert_one(collection_name, {'data': 'test'})
    
    # Cleanup
    mongodb_client.drop_collection(collection_name)
```

### 4. Validate Data Integrity

```python
def test_data_integrity(mongodb_client, clean_mongodb_collection):
    """Test data integrity constraints."""
    collection_name = 'orders'
    clean_mongodb_collection(collection_name)
    
    # Insert order
    order = {
        'order_id': '001',
        'user_id': 'user123',
        'items': [
            {'product_id': 'p1', 'quantity': 2, 'price': 10.00}
        ],
        'total': 20.00
    }
    
    mongodb_client.insert_one(collection_name, order)
    
    # Verify all required fields exist
    saved_order = mongodb_client.find_one(collection_name, {'order_id': '001'})
    
    required_fields = ['order_id', 'user_id', 'items', 'total']
    for field in required_fields:
        assert field in saved_order, f"Missing required field: {field}"
    
    # Verify calculated total matches
    calculated_total = sum(
        item['quantity'] * item['price']
        for item in saved_order['items']
    )
    assert saved_order['total'] == calculated_total
```

### 5. Use Descriptive Test Names

```python
def test_user_creation_with_valid_data_succeeds():
    """Good: Clear and descriptive."""
    pass

def test_user():
    """Bad: Unclear what is being tested."""
    pass
```

### 6. Test Edge Cases

```python
def test_empty_collection_query(mongodb_client, clean_mongodb_collection):
    """Test querying empty collection."""
    collection_name = 'empty_collection'
    clean_mongodb_collection(collection_name)
    
    results = mongodb_client.find_many(collection_name, {})
    assert results == []
    
    count = mongodb_client.count_documents(collection_name, {})
    assert count == 0

def test_large_document_insertion(mongodb_client, clean_mongodb_collection):
    """Test inserting large document."""
    collection_name = 'large_docs'
    clean_mongodb_collection(collection_name)
    
    # Create large document (MongoDB limit is 16MB)
    large_doc = {
        'data': 'x' * 1000000  # 1MB of data
    }
    
    doc_id = mongodb_client.insert_one(collection_name, large_doc)
    assert doc_id is not None
```

## Running MongoDB Tests

```bash
# Run all database tests
pytest tests/database/

# Run specific test file
pytest tests/database/test_mongodb_example.py

# Run with verbose output
pytest tests/database/ -v

# Run tests matching pattern
pytest tests/database/ -k "aggregation"
```

## Troubleshooting

### Connection Issues

```python
# Check if MongoDB is running
# Windows: net start MongoDB
# macOS/Linux: sudo systemctl status mongod

# Test connection
from framework.mongodb_client import MongoDBClient

client = MongoDBClient()
try:
    client.connect()
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    client.disconnect()
```

### Authentication Errors

```yaml
# Update connection string with credentials
mongodb:
  connection_string: "mongodb://username:password@localhost:27017/test_db?authSource=admin"
```

### Timeout Issues

```yaml
# Increase timeout
mongodb:
  timeout: 10000  # 10 seconds
```

## Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Query Operators](https://docs.mongodb.com/manual/reference/operator/query/)
- [Aggregation Pipeline](https://docs.mongodb.com/manual/core/aggregation-pipeline/)
