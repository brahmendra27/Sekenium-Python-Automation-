# conftest.py

import pytest
from framework.config import Config
from framework.api_client import APIClient, APIResponse
from framework.mongodb_client import MongoDBClient, MongoDBTestHelper
from framework.selenium_driver import SeleniumDriver
from framework.playwright_driver import PlaywrightDriver


@pytest.fixture(scope="session")
def config():
    """Provide configuration object for tests.
    
    Returns:
        Config instance
    """
    return Config()


@pytest.fixture(scope="function")
def driver(config):
    """Provide Selenium WebDriver for tests.
    
    Args:
        config: Configuration fixture
        
    Returns:
        WebDriver instance
        
    Yields:
        WebDriver instance (quits after test)
    """
    browser = config.browser
    headless = config.headless
    
    selenium_driver = SeleniumDriver(browser=browser, headless=headless)
    driver = selenium_driver.initialize()
    
    # Store config on driver for access in tests
    driver.config = config
    driver.base_url = config.base_url
    
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_url(config):
    """Provide base URL from configuration.
    
    Args:
        config: Configuration fixture
        
    Returns:
        Base URL string
    """
    return config.base_url


@pytest.fixture(scope="function")
def playwright_driver(config):
    """Provide Playwright driver for tests.
    
    Args:
        config: Configuration fixture
        
    Returns:
        Playwright page instance
        
    Yields:
        Playwright page instance (closes after test)
    """
    # Map browser names
    browser_map = {
        'chrome': 'chromium',
        'chromium': 'chromium',
        'firefox': 'firefox',
        'webkit': 'webkit'
    }
    
    browser_type = browser_map.get(config.browser.lower(), 'chromium')
    headless = config.headless
    
    pw_driver = PlaywrightDriver(
        browser_type=browser_type,
        headless=headless,
        slow_mo=0,
        tracing=True
    )
    context = pw_driver.initialize()
    page = context.new_page()
    
    yield page
    
    pw_driver.close()


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
