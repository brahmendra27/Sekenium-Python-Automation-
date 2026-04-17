# API and Database Integration Testing Guide

This guide demonstrates how to combine REST API testing with MongoDB database testing for comprehensive integration tests.

## Table of Contents

1. [Overview](#overview)
2. [Integration Test Patterns](#integration-test-patterns)
3. [End-to-End Test Examples](#end-to-end-test-examples)
4. [Data Verification Strategies](#data-verification-strategies)
5. [Best Practices](#best-practices)

## Overview

Integration testing validates that your API and database work together correctly. This involves:

- Testing API endpoints that interact with the database
- Verifying data persistence after API operations
- Testing data consistency across API and database layers
- Validating business logic that spans multiple components

## Integration Test Patterns

### Pattern 1: API → Database Verification

Test that API operations correctly persist data to the database.

```python
def test_api_creates_database_record(api_client, mongodb_client, clean_mongodb_collection):
    """Test that API POST creates a record in the database."""
    collection_name = 'users'
    clean_mongodb_collection(collection_name)
    
    # Make API request
    new_user = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'user'
    }
    
    response = api_client.post('/users', json_data=new_user)
    assert response.status_code == 201
    
    user_id = response.json()['id']
    
    # Verify in database
    db_user = mongodb_client.find_one(collection_name, {'_id': user_id})
    assert db_user is not None
    assert db_user['name'] == new_user['name']
    assert db_user['email'] == new_user['email']
```

### Pattern 2: Database → API Verification

Test that API correctly retrieves data from the database.

```python
def test_api_retrieves_database_record(api_client, mongodb_test_helper):
    """Test that API GET retrieves data from database."""
    collection_name = 'products'
    
    # Setup database with test data
    test_products = [
        {'_id': 'prod1', 'name': 'Product 1', 'price': 10.99},
        {'_id': 'prod2', 'name': 'Product 2', 'price': 20.99}
    ]
    
    mongodb_test_helper.setup_test_collection(collection_name, test_products)
    
    # Retrieve via API
    response = api_client.get('/products/prod1')
    assert response.status_code == 200
    
    product = response.json()
    assert product['name'] == 'Product 1'
    assert product['price'] == 10.99
```

### Pattern 3: Full CRUD Cycle

Test complete Create, Read, Update, Delete cycle across API and database.

```python
def test_full_crud_cycle(api_client, mongodb_client, clean_mongodb_collection):
    """Test complete CRUD cycle through API with database verification."""
    collection_name = 'tasks'
    clean_mongodb_collection(collection_name)
    
    # CREATE
    new_task = {'title': 'Test Task', 'status': 'pending'}
    create_response = api_client.post('/tasks', json_data=new_task)
    assert create_response.status_code == 201
    
    task_id = create_response.json()['id']
    
    # Verify creation in database
    db_task = mongodb_client.find_one(collection_name, {'_id': task_id})
    assert db_task['title'] == 'Test Task'
    
    # READ
    read_response = api_client.get(f'/tasks/{task_id}')
    assert read_response.status_code == 200
    assert read_response.json()['title'] == 'Test Task'
    
    # UPDATE
    update_data = {'status': 'completed'}
    update_response = api_client.patch(f'/tasks/{task_id}', json_data=update_data)
    assert update_response.status_code == 200
    
    # Verify update in database
    updated_task = mongodb_client.find_one(collection_name, {'_id': task_id})
    assert updated_task['status'] == 'completed'
    
    # DELETE
    delete_response = api_client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 204
    
    # Verify deletion in database
    deleted_task = mongodb_client.find_one(collection_name, {'_id': task_id})
    assert deleted_task is None
```

## End-to-End Test Examples

### Example 1: User Registration Flow

```python
def test_user_registration_flow(api_client, mongodb_client, clean_mongodb_collection):
    """Test complete user registration flow."""
    users_collection = 'users'
    sessions_collection = 'sessions'
    
    clean_mongodb_collection(users_collection)
    clean_mongodb_collection(sessions_collection)
    
    # Step 1: Register user via API
    registration_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'SecurePass123!'
    }
    
    register_response = api_client.post('/auth/register', json_data=registration_data)
    assert register_response.status_code == 201
    
    user_data = register_response.json()
    user_id = user_data['id']
    
    # Step 2: Verify user in database
    db_user = mongodb_client.find_one(users_collection, {'_id': user_id})
    assert db_user is not None
    assert db_user['username'] == 'newuser'
    assert db_user['email'] == 'newuser@example.com'
    assert 'password' not in db_user  # Password should be hashed, not stored
    assert 'password_hash' in db_user
    
    # Step 3: Login via API
    login_data = {
        'username': 'newuser',
        'password': 'SecurePass123!'
    }
    
    login_response = api_client.post('/auth/login', json_data=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()['token']
    
    # Step 4: Verify session in database
    session = mongodb_client.find_one(sessions_collection, {'user_id': user_id})
    assert session is not None
    assert session['token'] == token
    
    # Step 5: Access protected endpoint with token
    api_client.set_auth_token(token)
    profile_response = api_client.get('/users/me')
    assert profile_response.status_code == 200
    assert profile_response.json()['username'] == 'newuser'
```

### Example 2: E-commerce Order Processing

```python
def test_order_processing_flow(api_client, mongodb_client, clean_mongodb_collection):
    """Test complete order processing flow."""
    products_collection = 'products'
    orders_collection = 'orders'
    inventory_collection = 'inventory'
    
    clean_mongodb_collection(products_collection)
    clean_mongodb_collection(orders_collection)
    clean_mongodb_collection(inventory_collection)
    
    # Setup: Create products and inventory
    product_id = mongodb_client.insert_one(products_collection, {
        'name': 'Test Product',
        'price': 29.99,
        'sku': 'TEST-001'
    })
    
    mongodb_client.insert_one(inventory_collection, {
        'product_id': product_id,
        'quantity': 100
    })
    
    # Step 1: Create order via API
    order_data = {
        'items': [
            {'product_id': product_id, 'quantity': 2}
        ],
        'shipping_address': {
            'street': '123 Main St',
            'city': 'Anytown',
            'zip': '12345'
        }
    }
    
    order_response = api_client.post('/orders', json_data=order_data)
    assert order_response.status_code == 201
    
    order_id = order_response.json()['id']
    
    # Step 2: Verify order in database
    db_order = mongodb_client.find_one(orders_collection, {'_id': order_id})
    assert db_order is not None
    assert db_order['status'] == 'pending'
    assert db_order['total'] == 59.98  # 2 * 29.99
    
    # Step 3: Verify inventory was decremented
    inventory = mongodb_client.find_one(inventory_collection, {'product_id': product_id})
    assert inventory['quantity'] == 98  # 100 - 2
    
    # Step 4: Process payment via API
    payment_data = {
        'order_id': order_id,
        'payment_method': 'credit_card',
        'amount': 59.98
    }
    
    payment_response = api_client.post('/payments', json_data=payment_data)
    assert payment_response.status_code == 200
    
    # Step 5: Verify order status updated
    updated_order = mongodb_client.find_one(orders_collection, {'_id': order_id})
    assert updated_order['status'] == 'paid'
    assert 'payment_id' in updated_order
    
    # Step 6: Ship order via API
    ship_response = api_client.post(f'/orders/{order_id}/ship')
    assert ship_response.status_code == 200
    
    # Step 7: Verify final order status
    final_order = mongodb_client.find_one(orders_collection, {'_id': order_id})
    assert final_order['status'] == 'shipped'
    assert 'tracking_number' in final_order
```

### Example 3: Social Media Post with Comments

```python
def test_social_post_with_comments(api_client, mongodb_client, clean_mongodb_collection):
    """Test creating a post and adding comments."""
    posts_collection = 'posts'
    comments_collection = 'comments'
    users_collection = 'users'
    
    clean_mongodb_collection(posts_collection)
    clean_mongodb_collection(comments_collection)
    clean_mongodb_collection(users_collection)
    
    # Setup: Create test user
    user_id = mongodb_client.insert_one(users_collection, {
        'username': 'testuser',
        'email': 'test@example.com'
    })
    
    # Authenticate
    api_client.set_header('X-User-ID', str(user_id))
    
    # Step 1: Create post via API
    post_data = {
        'title': 'Test Post',
        'content': 'This is a test post content',
        'tags': ['test', 'automation']
    }
    
    post_response = api_client.post('/posts', json_data=post_data)
    assert post_response.status_code == 201
    
    post_id = post_response.json()['id']
    
    # Step 2: Verify post in database
    db_post = mongodb_client.find_one(posts_collection, {'_id': post_id})
    assert db_post['title'] == 'Test Post'
    assert db_post['author_id'] == user_id
    assert db_post['comment_count'] == 0
    
    # Step 3: Add comments via API
    comments = [
        {'content': 'Great post!'},
        {'content': 'Very informative'},
        {'content': 'Thanks for sharing'}
    ]
    
    comment_ids = []
    for comment_data in comments:
        comment_response = api_client.post(
            f'/posts/{post_id}/comments',
            json_data=comment_data
        )
        assert comment_response.status_code == 201
        comment_ids.append(comment_response.json()['id'])
    
    # Step 4: Verify comments in database
    db_comments = mongodb_client.find_many(
        comments_collection,
        {'post_id': post_id}
    )
    assert len(db_comments) == 3
    
    # Step 5: Verify post comment count updated
    updated_post = mongodb_client.find_one(posts_collection, {'_id': post_id})
    assert updated_post['comment_count'] == 3
    
    # Step 6: Get post with comments via API
    post_with_comments = api_client.get(f'/posts/{post_id}?include=comments')
    assert post_with_comments.status_code == 200
    
    post_data = post_with_comments.json()
    assert len(post_data['comments']) == 3
```

## Data Verification Strategies

### Strategy 1: Timestamp Verification

```python
from datetime import datetime, timedelta

def test_timestamp_verification(api_client, mongodb_client, clean_mongodb_collection):
    """Verify timestamps are set correctly."""
    collection_name = 'events'
    clean_mongodb_collection(collection_name)
    
    before_time = datetime.utcnow()
    
    # Create via API
    event_data = {'name': 'Test Event', 'type': 'test'}
    response = api_client.post('/events', json_data=event_data)
    
    after_time = datetime.utcnow()
    
    event_id = response.json()['id']
    
    # Verify timestamp in database
    db_event = mongodb_client.find_one(collection_name, {'_id': event_id})
    created_at = db_event['created_at']
    
    assert before_time <= created_at <= after_time
```

### Strategy 2: Data Consistency Checks

```python
def test_data_consistency(api_client, mongodb_client, clean_mongodb_collection):
    """Verify data consistency between API and database."""
    collection_name = 'products'
    clean_mongodb_collection(collection_name)
    
    # Create product
    product_data = {
        'name': 'Test Product',
        'price': 99.99,
        'stock': 50
    }
    
    response = api_client.post('/products', json_data=product_data)
    product_id = response.json()['id']
    
    # Get from API
    api_product = api_client.get(f'/products/{product_id}').json()
    
    # Get from database
    db_product = mongodb_client.find_one(collection_name, {'_id': product_id})
    
    # Verify consistency
    assert api_product['name'] == db_product['name']
    assert api_product['price'] == db_product['price']
    assert api_product['stock'] == db_product['stock']
```

### Strategy 3: Aggregated Data Verification

```python
def test_aggregated_data(api_client, mongodb_client, clean_mongodb_collection):
    """Verify aggregated statistics match between API and database."""
    orders_collection = 'orders'
    clean_mongodb_collection(orders_collection)
    
    # Create multiple orders
    for i in range(5):
        mongodb_client.insert_one(orders_collection, {
            'user_id': 'user123',
            'amount': (i + 1) * 10,
            'status': 'completed'
        })
    
    # Get statistics from API
    stats_response = api_client.get('/users/user123/stats')
    api_stats = stats_response.json()
    
    # Calculate from database
    pipeline = [
        {'$match': {'user_id': 'user123', 'status': 'completed'}},
        {
            '$group': {
                '_id': None,
                'total_orders': {'$sum': 1},
                'total_spent': {'$sum': '$amount'}
            }
        }
    ]
    
    db_stats = mongodb_client.aggregate(orders_collection, pipeline)[0]
    
    # Verify consistency
    assert api_stats['total_orders'] == db_stats['total_orders']
    assert api_stats['total_spent'] == db_stats['total_spent']
```

## Best Practices

### 1. Use Transactions for Multi-Step Operations

```python
def test_with_transaction(api_client, mongodb_client):
    """Test operations that should be atomic."""
    # When testing operations that modify multiple collections,
    # verify they succeed or fail together
    
    response = api_client.post('/transfer', json_data={
        'from_account': 'acc1',
        'to_account': 'acc2',
        'amount': 100
    })
    
    if response.status_code == 200:
        # Both accounts should be updated
        from_account = mongodb_client.find_one('accounts', {'_id': 'acc1'})
        to_account = mongodb_client.find_one('accounts', {'_id': 'acc2'})
        
        # Verify balances changed correctly
        assert from_account['balance'] == original_from_balance - 100
        assert to_account['balance'] == original_to_balance + 100
```

### 2. Test Data Isolation

```python
@pytest.fixture
def isolated_test_data(mongodb_test_helper):
    """Create isolated test data for each test."""
    test_id = str(uuid.uuid4())
    
    mongodb_test_helper.setup_test_collection(f'users_{test_id}', [
        {'name': 'Test User', 'test_id': test_id}
    ])
    
    yield test_id
    
    # Cleanup happens automatically

def test_with_isolation(api_client, isolated_test_data):
    """Test with isolated data."""
    # Use isolated_test_data to ensure no interference
    pass
```

### 3. Verify Side Effects

```python
def test_side_effects(api_client, mongodb_client, clean_mongodb_collection):
    """Verify all side effects of an operation."""
    users_collection = 'users'
    notifications_collection = 'notifications'
    audit_log_collection = 'audit_log'
    
    clean_mongodb_collection(users_collection)
    clean_mongodb_collection(notifications_collection)
    clean_mongodb_collection(audit_log_collection)
    
    # Perform action
    response = api_client.post('/users', json_data={
        'name': 'New User',
        'email': 'new@example.com'
    })
    
    user_id = response.json()['id']
    
    # Verify primary effect
    user = mongodb_client.find_one(users_collection, {'_id': user_id})
    assert user is not None
    
    # Verify side effects
    # 1. Welcome notification created
    notification = mongodb_client.find_one(
        notifications_collection,
        {'user_id': user_id, 'type': 'welcome'}
    )
    assert notification is not None
    
    # 2. Audit log entry created
    audit_entry = mongodb_client.find_one(
        audit_log_collection,
        {'action': 'user_created', 'user_id': user_id}
    )
    assert audit_entry is not None
```

### 4. Test Error Scenarios

```python
def test_error_rollback(api_client, mongodb_client, clean_mongodb_collection):
    """Verify database is not modified on API errors."""
    collection_name = 'products'
    clean_mongodb_collection(collection_name)
    
    # Get initial count
    initial_count = mongodb_client.count_documents(collection_name, {})
    
    # Attempt invalid operation
    invalid_data = {'name': ''}  # Invalid: empty name
    response = api_client.post('/products', json_data=invalid_data)
    
    assert response.status_code == 400
    
    # Verify no data was created
    final_count = mongodb_client.count_documents(collection_name, {})
    assert final_count == initial_count
```

### 5. Performance Testing

```python
import time

def test_api_database_performance(api_client, mongodb_test_helper):
    """Test performance of API with database operations."""
    collection_name = 'products'
    
    # Setup large dataset
    products = [
        {'name': f'Product {i}', 'price': i * 10}
        for i in range(1000)
    ]
    mongodb_test_helper.setup_test_collection(collection_name, products)
    
    # Measure API response time
    start_time = time.time()
    response = api_client.get('/products?limit=100')
    end_time = time.time()
    
    assert response.status_code == 200
    
    response_time = end_time - start_time
    assert response_time < 1.0  # Should respond within 1 second
```

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/ -v

# Run only API tests
pytest tests/api/ -v

# Run only database tests
pytest tests/database/ -v

# Run with coverage
pytest tests/ --cov=framework --cov-report=html

# Run specific integration test
pytest tests/integration/test_user_flow.py -v
```

## Conclusion

Integration testing ensures your API and database work together correctly. Key takeaways:

1. **Verify both layers**: Always check both API responses and database state
2. **Test complete flows**: Test end-to-end user journeys
3. **Check side effects**: Verify all expected changes occur
4. **Test error cases**: Ensure errors don't leave inconsistent state
5. **Isolate test data**: Use fixtures and cleanup to prevent test interference

For more details, see:
- [API Testing Guide](API_TESTING_GUIDE.md)
- [MongoDB Testing Guide](MONGODB_TESTING_GUIDE.md)
