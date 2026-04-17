# conftest.py

import pytest
from framework.config import Config
from framework.api_client import APIClient, APIResponse
from framework.mongodb_client import MongoDBClient, MongoDBTestHelper


@pytest.fixture(scope="session")
def config():
    """Provide configuration object for tests.
    
    Returns:
        Config instance
    """
    return Config()


@pytest.fixture(scope="session")
def api_client(config):
    """Provide API client for tests.
    
    Args:
        config: Configuration fixture
        
    Returns:
        APIClient instance
        
    Yields:
        APIClient instance (closes session after tests)
    """
    client = APIClient(config)
    yield client
    client.close()


@pytest.fixture(scope="function")
def api_response_wrapper():
    """Provide APIResponse wrapper factory.
    
    Returns:
        Function that wraps requests.Response in APIResponse
    """
    def wrapper(response):
        return APIResponse(response)
    return wrapper


@pytest.fixture(scope="session")
def mongodb_client(config):
    """Provide MongoDB client for tests.
    
    Args:
        config: Configuration fixture
        
    Returns:
        MongoDBClient instance
        
    Yields:
        MongoDBClient instance (disconnects after tests)
    """
    client = MongoDBClient(config)
    try:
        client.connect()
        yield client
    finally:
        client.disconnect()


@pytest.fixture(scope="function")
def mongodb_test_helper(mongodb_client):
    """Provide MongoDB test helper with automatic cleanup.
    
    Args:
        mongodb_client: MongoDB client fixture
        
    Returns:
        MongoDBTestHelper instance
        
    Yields:
        MongoDBTestHelper instance (cleans up after test)
    """
    helper = MongoDBTestHelper(mongodb_client)
    yield helper
    helper.teardown_test_collections()


@pytest.fixture(scope="function")
def clean_mongodb_collection(mongodb_client):
    """Provide function to clean a MongoDB collection after test.
    
    Args:
        mongodb_client: MongoDB client fixture
        
    Returns:
        Function that marks collection for cleanup
    """
    collections_to_clean = []
    
    def mark_for_cleanup(collection_name: str):
        if collection_name not in collections_to_clean:
            collections_to_clean.append(collection_name)
    
    yield mark_for_cleanup
    
    # Cleanup after test
    for collection_name in collections_to_clean:
        try:
            mongodb_client.delete_many(collection_name, {})
        except Exception as e:
            print(f"Failed to clean collection {collection_name}: {str(e)}")
