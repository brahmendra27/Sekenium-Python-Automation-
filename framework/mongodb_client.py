# framework/mongodb_client.py

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional, Dict, List, Any, Union
import logging
from datetime import datetime
from framework.config import Config


class MongoDBClient:
    """MongoDB client with connection management and common operations."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize MongoDB client with configuration.
        
        Args:
            config: Configuration object (creates new if not provided)
        """
        self.config = config or Config()
        self.connection_string = self.config.mongodb_connection_string
        self.database_name = self.config.mongodb_database
        self.timeout = self.config.mongodb_timeout
        self.max_pool_size = self.config.mongodb_max_pool_size
        
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=self.timeout,
                maxPoolSize=self.max_pool_size
            )
            # Test connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self.logger.info(f"Connected to MongoDB database: {self.database_name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.logger.info("Disconnected from MongoDB")
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection object
            
        Raises:
            RuntimeError: If not connected to database
        """
        if not self.db:
            raise RuntimeError("Not connected to database. Call connect() first.")
        return self.db[collection_name]
    
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a single document into collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            Inserted document ID as string
        """
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        self.logger.info(f"Inserted document into {collection_name}: {result.inserted_id}")
        return str(result.inserted_id)
    
    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents into collection.
        
        Args:
            collection_name: Name of the collection
            documents: List of documents to insert
            
        Returns:
            List of inserted document IDs as strings
        """
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        self.logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
        return [str(id) for id in result.inserted_ids]
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document matching query.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Document if found, None otherwise
        """
        collection = self.get_collection(collection_name)
        document = collection.find_one(query)
        self.logger.debug(f"Find one in {collection_name} with query: {query}")
        return document
    
    def find_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        limit: int = 0,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """Find multiple documents matching query.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            limit: Maximum number of documents to return (0 = no limit)
            sort: List of (field, direction) tuples for sorting
            
        Returns:
            List of matching documents
        """
        collection = self.get_collection(collection_name)
        cursor = collection.find(query)
        
        if sort:
            cursor = cursor.sort(sort)
        
        if limit > 0:
            cursor = cursor.limit(limit)
        
        documents = list(cursor)
        self.logger.debug(f"Found {len(documents)} documents in {collection_name}")
        return documents
    
    def update_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> int:
        """Update a single document.
        
        Args:
            collection_name: Name of the collection
            query: Query filter to find document
            update: Update operations
            upsert: Create document if not found
            
        Returns:
            Number of documents modified
        """
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, update, upsert=upsert)
        self.logger.info(f"Updated {result.modified_count} document(s) in {collection_name}")
        return result.modified_count
    
    def update_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> int:
        """Update multiple documents.
        
        Args:
            collection_name: Name of the collection
            query: Query filter to find documents
            update: Update operations
            upsert: Create documents if not found
            
        Returns:
            Number of documents modified
        """
        collection = self.get_collection(collection_name)
        result = collection.update_many(query, update, upsert=upsert)
        self.logger.info(f"Updated {result.modified_count} document(s) in {collection_name}")
        return result.modified_count
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a single document.
        
        Args:
            collection_name: Name of the collection
            query: Query filter to find document
            
        Returns:
            Number of documents deleted
        """
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        self.logger.info(f"Deleted {result.deleted_count} document(s) from {collection_name}")
        return result.deleted_count
    
    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete multiple documents.
        
        Args:
            collection_name: Name of the collection
            query: Query filter to find documents
            
        Returns:
            Number of documents deleted
        """
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        self.logger.info(f"Deleted {result.deleted_count} document(s) from {collection_name}")
        return result.deleted_count
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents matching query.
        
        Args:
            collection_name: Name of the collection
            query: Query filter (empty dict counts all)
            
        Returns:
            Number of matching documents
        """
        collection = self.get_collection(collection_name)
        query = query or {}
        count = collection.count_documents(query)
        self.logger.debug(f"Count in {collection_name}: {count}")
        return count
    
    def drop_collection(self, collection_name: str):
        """Drop (delete) an entire collection.
        
        Args:
            collection_name: Name of the collection to drop
        """
        collection = self.get_collection(collection_name)
        collection.drop()
        self.logger.warning(f"Dropped collection: {collection_name}")
    
    def create_index(
        self,
        collection_name: str,
        keys: Union[str, List[tuple]],
        unique: bool = False
    ) -> str:
        """Create an index on collection.
        
        Args:
            collection_name: Name of the collection
            keys: Field name or list of (field, direction) tuples
            unique: Whether index should enforce uniqueness
            
        Returns:
            Name of created index
        """
        collection = self.get_collection(collection_name)
        index_name = collection.create_index(keys, unique=unique)
        self.logger.info(f"Created index on {collection_name}: {index_name}")
        return index_name
    
    def aggregate(self, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute aggregation pipeline.
        
        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline stages
            
        Returns:
            List of aggregation results
        """
        collection = self.get_collection(collection_name)
        results = list(collection.aggregate(pipeline))
        self.logger.debug(f"Aggregation on {collection_name} returned {len(results)} results")
        return results
    
    def list_collections(self) -> List[str]:
        """List all collections in the database.
        
        Returns:
            List of collection names
        """
        if not self.db:
            raise RuntimeError("Not connected to database. Call connect() first.")
        return self.db.list_collection_names()


class MongoDBTestHelper:
    """Helper class for MongoDB testing with setup/teardown utilities."""
    
    def __init__(self, client: MongoDBClient):
        """Initialize test helper with MongoDB client.
        
        Args:
            client: MongoDBClient instance
        """
        self.client = client
        self.test_collections: List[str] = []
        self.logger = logging.getLogger(__name__)
    
    def setup_test_collection(self, collection_name: str, initial_data: Optional[List[Dict[str, Any]]] = None):
        """Setup a test collection with optional initial data.
        
        Args:
            collection_name: Name of the collection
            initial_data: Optional list of documents to insert
        """
        # Track collection for cleanup
        if collection_name not in self.test_collections:
            self.test_collections.append(collection_name)
        
        # Clear existing data
        self.client.delete_many(collection_name, {})
        
        # Insert initial data if provided
        if initial_data:
            self.client.insert_many(collection_name, initial_data)
            self.logger.info(f"Setup test collection '{collection_name}' with {len(initial_data)} documents")
    
    def teardown_test_collections(self):
        """Clean up all test collections."""
        for collection_name in self.test_collections:
            try:
                self.client.delete_many(collection_name, {})
                self.logger.info(f"Cleaned up test collection: {collection_name}")
            except Exception as e:
                self.logger.error(f"Failed to clean up {collection_name}: {str(e)}")
        
        self.test_collections.clear()
    
    def create_test_document(self, **kwargs) -> Dict[str, Any]:
        """Create a test document with timestamp.
        
        Args:
            **kwargs: Document fields
            
        Returns:
            Document dictionary with timestamp
        """
        document = {
            'created_at': datetime.utcnow(),
            'test_marker': True,
            **kwargs
        }
        return document
    
    def assert_document_exists(self, collection_name: str, query: Dict[str, Any]):
        """Assert that a document exists in collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Raises:
            AssertionError: If document not found
        """
        document = self.client.find_one(collection_name, query)
        assert document is not None, f"Document not found in {collection_name} with query: {query}"
    
    def assert_document_count(self, collection_name: str, expected_count: int, query: Dict[str, Any] = None):
        """Assert document count in collection.
        
        Args:
            collection_name: Name of the collection
            expected_count: Expected number of documents
            query: Optional query filter
            
        Raises:
            AssertionError: If count doesn't match
        """
        actual_count = self.client.count_documents(collection_name, query or {})
        assert actual_count == expected_count, \
            f"Expected {expected_count} documents in {collection_name}, found {actual_count}"
    
    def assert_field_value(
        self,
        collection_name: str,
        query: Dict[str, Any],
        field: str,
        expected_value: Any
    ):
        """Assert field value in a document.
        
        Args:
            collection_name: Name of the collection
            query: Query filter to find document
            field: Field name to check
            expected_value: Expected field value
            
        Raises:
            AssertionError: If field value doesn't match
        """
        document = self.client.find_one(collection_name, query)
        assert document is not None, f"Document not found in {collection_name}"
        
        actual_value = document.get(field)
        assert actual_value == expected_value, \
            f"Expected {field}={expected_value}, got {actual_value}"
