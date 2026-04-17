# tests/database/test_mongodb_example.py

"""
Example MongoDB tests demonstrating database testing capabilities.
"""

import pytest
from datetime import datetime
from bson import ObjectId


class TestMongoDBBasicOperations:
    """Test basic MongoDB CRUD operations."""
    
    def test_insert_and_find_document(self, mongodb_client, clean_mongodb_collection):
        """Test inserting and finding a document."""
        collection_name = 'test_users'
        clean_mongodb_collection(collection_name)
        
        # Insert document
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30,
            'created_at': datetime.utcnow()
        }
        
        doc_id = mongodb_client.insert_one(collection_name, user_data)
        assert doc_id is not None
        
        # Find document
        found_user = mongodb_client.find_one(collection_name, {'name': 'John Doe'})
        assert found_user is not None
        assert found_user['email'] == 'john@example.com'
        assert found_user['age'] == 30
    
    def test_insert_multiple_documents(self, mongodb_client, clean_mongodb_collection):
        """Test inserting multiple documents."""
        collection_name = 'test_products'
        clean_mongodb_collection(collection_name)
        
        products = [
            {'name': 'Product 1', 'price': 10.99, 'stock': 100},
            {'name': 'Product 2', 'price': 20.99, 'stock': 50},
            {'name': 'Product 3', 'price': 15.99, 'stock': 75}
        ]
        
        doc_ids = mongodb_client.insert_many(collection_name, products)
        assert len(doc_ids) == 3
        
        # Verify all documents were inserted
        count = mongodb_client.count_documents(collection_name, {})
        assert count == 3
    
    def test_update_document(self, mongodb_client, clean_mongodb_collection):
        """Test updating a document."""
        collection_name = 'test_users'
        clean_mongodb_collection(collection_name)
        
        # Insert initial document
        user_data = {'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 25}
        mongodb_client.insert_one(collection_name, user_data)
        
        # Update document
        update_result = mongodb_client.update_one(
            collection_name,
            {'name': 'Jane Doe'},
            {'$set': {'age': 26, 'updated_at': datetime.utcnow()}}
        )
        
        assert update_result == 1
        
        # Verify update
        updated_user = mongodb_client.find_one(collection_name, {'name': 'Jane Doe'})
        assert updated_user['age'] == 26
        assert 'updated_at' in updated_user
    
    def test_delete_document(self, mongodb_client, clean_mongodb_collection):
        """Test deleting a document."""
        collection_name = 'test_users'
        clean_mongodb_collection(collection_name)
        
        # Insert document
        user_data = {'name': 'Delete Me', 'email': 'delete@example.com'}
        mongodb_client.insert_one(collection_name, user_data)
        
        # Verify document exists
        assert mongodb_client.count_documents(collection_name, {'name': 'Delete Me'}) == 1
        
        # Delete document
        delete_result = mongodb_client.delete_one(collection_name, {'name': 'Delete Me'})
        assert delete_result == 1
        
        # Verify document is gone
        assert mongodb_client.count_documents(collection_name, {'name': 'Delete Me'}) == 0


class TestMongoDBQueries:
    """Test MongoDB query operations."""
    
    def test_find_with_filter(self, mongodb_client, clean_mongodb_collection):
        """Test finding documents with filters."""
        collection_name = 'test_products'
        clean_mongodb_collection(collection_name)
        
        # Insert test data
        products = [
            {'name': 'Laptop', 'category': 'Electronics', 'price': 999.99},
            {'name': 'Mouse', 'category': 'Electronics', 'price': 29.99},
            {'name': 'Desk', 'category': 'Furniture', 'price': 299.99},
            {'name': 'Chair', 'category': 'Furniture', 'price': 199.99}
        ]
        mongodb_client.insert_many(collection_name, products)
        
        # Find electronics
        electronics = mongodb_client.find_many(collection_name, {'category': 'Electronics'})
        assert len(electronics) == 2
        
        # Find expensive items
        expensive = mongodb_client.find_many(collection_name, {'price': {'$gt': 200}})
        assert len(expensive) == 2
    
    def test_find_with_sorting(self, mongodb_client, clean_mongodb_collection):
        """Test finding documents with sorting."""
        collection_name = 'test_products'
        clean_mongodb_collection(collection_name)
        
        # Insert test data
        products = [
            {'name': 'Product C', 'price': 30},
            {'name': 'Product A', 'price': 10},
            {'name': 'Product B', 'price': 20}
        ]
        mongodb_client.insert_many(collection_name, products)
        
        # Find and sort by price ascending
        sorted_products = mongodb_client.find_many(
            collection_name,
            {},
            sort=[('price', 1)]
        )
        
        assert sorted_products[0]['price'] == 10
        assert sorted_products[1]['price'] == 20
        assert sorted_products[2]['price'] == 30
    
    def test_find_with_limit(self, mongodb_client, clean_mongodb_collection):
        """Test finding documents with limit."""
        collection_name = 'test_items'
        clean_mongodb_collection(collection_name)
        
        # Insert 10 documents
        items = [{'name': f'Item {i}', 'value': i} for i in range(10)]
        mongodb_client.insert_many(collection_name, items)
        
        # Find with limit
        limited_items = mongodb_client.find_many(collection_name, {}, limit=5)
        assert len(limited_items) == 5
    
    def test_count_documents(self, mongodb_client, clean_mongodb_collection):
        """Test counting documents."""
        collection_name = 'test_orders'
        clean_mongodb_collection(collection_name)
        
        # Insert test data
        orders = [
            {'status': 'pending', 'amount': 100},
            {'status': 'pending', 'amount': 200},
            {'status': 'completed', 'amount': 150},
            {'status': 'cancelled', 'amount': 50}
        ]
        mongodb_client.insert_many(collection_name, orders)
        
        # Count all orders
        total_count = mongodb_client.count_documents(collection_name, {})
        assert total_count == 4
        
        # Count pending orders
        pending_count = mongodb_client.count_documents(collection_name, {'status': 'pending'})
        assert pending_count == 2


class TestMongoDBAdvancedOperations:
    """Test advanced MongoDB operations."""
    
    def test_update_multiple_documents(self, mongodb_client, clean_mongodb_collection):
        """Test updating multiple documents."""
        collection_name = 'test_products'
        clean_mongodb_collection(collection_name)
        
        # Insert test data
        products = [
            {'name': 'Product 1', 'category': 'Electronics', 'discount': False},
            {'name': 'Product 2', 'category': 'Electronics', 'discount': False},
            {'name': 'Product 3', 'category': 'Furniture', 'discount': False}
        ]
        mongodb_client.insert_many(collection_name, products)
        
        # Apply discount to all electronics
        update_count = mongodb_client.update_many(
            collection_name,
            {'category': 'Electronics'},
            {'$set': {'discount': True, 'discount_percent': 10}}
        )
        
        assert update_count == 2
        
        # Verify updates
        discounted = mongodb_client.find_many(collection_name, {'discount': True})
        assert len(discounted) == 2
    
    def test_upsert_operation(self, mongodb_client, clean_mongodb_collection):
        """Test upsert (update or insert) operation."""
        collection_name = 'test_settings'
        clean_mongodb_collection(collection_name)
        
        # Upsert - should insert since document doesn't exist
        mongodb_client.update_one(
            collection_name,
            {'key': 'theme'},
            {'$set': {'value': 'dark'}},
            upsert=True
        )
        
        # Verify document was created
        setting = mongodb_client.find_one(collection_name, {'key': 'theme'})
        assert setting is not None
        assert setting['value'] == 'dark'
        
        # Upsert again - should update existing document
        mongodb_client.update_one(
            collection_name,
            {'key': 'theme'},
            {'$set': {'value': 'light'}},
            upsert=True
        )
        
        # Verify document was updated, not duplicated
        count = mongodb_client.count_documents(collection_name, {'key': 'theme'})
        assert count == 1
        
        updated_setting = mongodb_client.find_one(collection_name, {'key': 'theme'})
        assert updated_setting['value'] == 'light'
    
    def test_aggregation_pipeline(self, mongodb_client, clean_mongodb_collection):
        """Test aggregation pipeline."""
        collection_name = 'test_sales'
        clean_mongodb_collection(collection_name)
        
        # Insert test data
        sales = [
            {'product': 'Laptop', 'category': 'Electronics', 'amount': 1000, 'quantity': 2},
            {'product': 'Mouse', 'category': 'Electronics', 'amount': 50, 'quantity': 5},
            {'product': 'Desk', 'category': 'Furniture', 'amount': 300, 'quantity': 1},
            {'product': 'Chair', 'category': 'Furniture', 'amount': 200, 'quantity': 2}
        ]
        mongodb_client.insert_many(collection_name, sales)
        
        # Aggregate sales by category
        pipeline = [
            {
                '$group': {
                    '_id': '$category',
                    'total_amount': {'$sum': '$amount'},
                    'total_quantity': {'$sum': '$quantity'}
                }
            },
            {'$sort': {'total_amount': -1}}
        ]
        
        results = mongodb_client.aggregate(collection_name, pipeline)
        
        assert len(results) == 2
        assert results[0]['_id'] == 'Electronics'
        assert results[0]['total_amount'] == 1050
    
    def test_create_index(self, mongodb_client, clean_mongodb_collection):
        """Test creating an index."""
        collection_name = 'test_users'
        clean_mongodb_collection(collection_name)
        
        # Create unique index on email
        index_name = mongodb_client.create_index(collection_name, 'email', unique=True)
        assert index_name is not None
        
        # Insert document
        mongodb_client.insert_one(collection_name, {'name': 'User 1', 'email': 'user1@example.com'})
        
        # Try to insert duplicate email - should fail
        with pytest.raises(Exception):
            mongodb_client.insert_one(collection_name, {'name': 'User 2', 'email': 'user1@example.com'})


class TestMongoDBTestHelper:
    """Test MongoDB test helper utilities."""
    
    def test_setup_test_collection(self, mongodb_test_helper):
        """Test setting up a test collection with initial data."""
        collection_name = 'test_helper_collection'
        
        initial_data = [
            {'name': 'Item 1', 'value': 100},
            {'name': 'Item 2', 'value': 200}
        ]
        
        mongodb_test_helper.setup_test_collection(collection_name, initial_data)
        
        # Verify data was inserted
        count = mongodb_test_helper.client.count_documents(collection_name, {})
        assert count == 2
    
    def test_create_test_document(self, mongodb_test_helper):
        """Test creating a test document with timestamp."""
        doc = mongodb_test_helper.create_test_document(
            name='Test Item',
            value=123
        )
        
        assert doc['name'] == 'Test Item'
        assert doc['value'] == 123
        assert 'created_at' in doc
        assert doc['test_marker'] is True
    
    def test_assert_document_exists(self, mongodb_test_helper):
        """Test asserting document existence."""
        collection_name = 'test_assertions'
        
        # Setup collection
        mongodb_test_helper.setup_test_collection(
            collection_name,
            [{'name': 'Test User', 'email': 'test@example.com'}]
        )
        
        # Should pass
        mongodb_test_helper.assert_document_exists(
            collection_name,
            {'name': 'Test User'}
        )
        
        # Should fail
        with pytest.raises(AssertionError):
            mongodb_test_helper.assert_document_exists(
                collection_name,
                {'name': 'Non-existent User'}
            )
    
    def test_assert_document_count(self, mongodb_test_helper):
        """Test asserting document count."""
        collection_name = 'test_count'
        
        # Setup collection with 3 documents
        mongodb_test_helper.setup_test_collection(
            collection_name,
            [
                {'status': 'active'},
                {'status': 'active'},
                {'status': 'inactive'}
            ]
        )
        
        # Assert total count
        mongodb_test_helper.assert_document_count(collection_name, 3)
        
        # Assert count with filter
        mongodb_test_helper.assert_document_count(
            collection_name,
            2,
            {'status': 'active'}
        )
    
    def test_assert_field_value(self, mongodb_test_helper):
        """Test asserting field value."""
        collection_name = 'test_fields'
        
        # Setup collection
        mongodb_test_helper.setup_test_collection(
            collection_name,
            [{'name': 'Test Item', 'status': 'active', 'value': 100}]
        )
        
        # Should pass
        mongodb_test_helper.assert_field_value(
            collection_name,
            {'name': 'Test Item'},
            'status',
            'active'
        )
        
        # Should fail
        with pytest.raises(AssertionError):
            mongodb_test_helper.assert_field_value(
                collection_name,
                {'name': 'Test Item'},
                'status',
                'inactive'
            )
    
    def test_automatic_cleanup(self, mongodb_test_helper):
        """Test that collections are automatically cleaned up."""
        collection_name = 'test_cleanup'
        
        # Setup collection
        mongodb_test_helper.setup_test_collection(
            collection_name,
            [{'name': 'Item 1'}, {'name': 'Item 2'}]
        )
        
        # Verify data exists
        count = mongodb_test_helper.client.count_documents(collection_name, {})
        assert count == 2
        
        # Cleanup will happen automatically after test via fixture
