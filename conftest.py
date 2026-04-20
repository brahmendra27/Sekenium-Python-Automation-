# conftest.py

"""
Root conftest — provides all shared fixtures and hooks.

Features:
  - Screenshot-on-failure (auto-captured, attached to Allure)
  - Playwright trace capture on failure
  - Environment health check before test run
  - Config validation
  - Worker ID for parallel isolation
  - Selenium and Playwright driver fixtures
  - API and MongoDB client fixtures
"""

import os
import logging
import pytest
import allure
from pathlib import Path
from framework.config import Config
from framework.api_client import APIClient, APIResponse
from framework.mongodb_client import MongoDBClient, MongoDBTestHelper
from framework.selenium_driver import SeleniumDriver
from framework.playwright_driver import PlaywrightDriver

logger = logging.getLogger(__name__)

# ==================== DIRECTORIES ====================

SCREENSHOTS_DIR = Path("screenshots/failures")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ==================== HOOKS ====================

def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to Allure.

    This hook runs after each test phase (setup, call, teardown).
    On failure during the 'call' phase, it captures a screenshot
    from the active driver and attaches it to the Allure report.
    """
    if call.when == "call" and call.excinfo is not None:
        # Test failed — try to capture screenshot
        test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
        screenshot_path = str(SCREENSHOTS_DIR / f"{test_name}.png")

        # Try Selenium driver first
        driver = item.funcargs.get("driver")
        if driver:
            try:
                driver.save_screenshot(screenshot_path)
                allure.attach.file(
                    screenshot_path,
                    name=f"failure_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture Selenium screenshot: {e}")

        # Try Playwright page
        page = item.funcargs.get("playwright_driver")
        if page:
            try:
                page.screenshot(path=screenshot_path)
                allure.attach.file(
                    screenshot_path,
                    name=f"failure_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture Playwright screenshot: {e}")


# ==================== SESSION FIXTURES ====================

@pytest.fixture(scope="session")
def config():
    """Provide validated configuration object.

    Loads config from .env + config.yaml, validates settings,
    and logs any configuration issues.
    """
    cfg = Config()
    issues = cfg.validate()
    if issues:
        logger.warning(f"Configuration issues found: {issues}")
    return cfg


@pytest.fixture(scope="session")
def base_url(config):
    """Provide base URL from configuration."""
    return config.base_url


@pytest.fixture(scope="session", autouse=True)
def validate_environment(config):
    """Validate that the target environment is accessible.

    Runs once before all tests. Logs a warning if the base URL
    is not reachable, but does not fail the session (some tests
    like API tests may not need the UI base URL).
    """
    import requests as req

    base = config.base_url
    if not base or base == "http://localhost:8080":
        logger.info("Using default base_url — skipping environment check")
        return

    try:
        # Strip credentials from URL for the health check
        clean_url = base.split("@")[-1] if "@" in base else base
        if not clean_url.startswith("http"):
            clean_url = "https://" + clean_url

        resp = req.head(clean_url, timeout=10, allow_redirects=True, verify=False)
        logger.info(f"Environment check: {clean_url} returned {resp.status_code}")
    except Exception as e:
        logger.warning(
            f"Environment check failed for {base}: {e}. "
            f"UI tests may fail if the site is unreachable."
        )


# ==================== DRIVER FIXTURES ====================

@pytest.fixture(scope="function")
def driver(config, request):
    """Provide Selenium WebDriver with auto-screenshot on failure.

    Yields:
        WebDriver instance (quits after test)
    """
    browser = config.browser
    headless = config.headless

    selenium_driver = SeleniumDriver(browser=browser, headless=headless)
    drv = selenium_driver.initialize()

    # Attach config and base_url for easy access in tests
    drv.config = config
    drv.base_url = config.base_url

    yield drv

    drv.quit()


@pytest.fixture(scope="function")
def playwright_driver(config, request):
    """Provide Playwright page with trace capture on failure.

    Yields:
        Playwright Page instance (closes after test, saves trace on failure)
    """
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

    # Save trace on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.nodeid.replace("::", "_").replace("/", "_")
        trace_path = f"reports/traces/{test_name}.zip"
        try:
            os.makedirs("reports/traces", exist_ok=True)
            pw_driver.close(trace_path=trace_path)
            allure.attach.file(
                trace_path,
                name=f"trace_{test_name}",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.info(f"Trace saved: {trace_path}")
            return
        except Exception as e:
            logger.warning(f"Failed to save trace: {e}")

    pw_driver.close()


# ==================== API FIXTURES ====================

@pytest.fixture(scope="session")
def api_client(config):
    """Provide API client for tests.

    Yields:
        APIClient instance (closes session after all tests)
    """
    client = APIClient(config)
    yield client
    client.close()


@pytest.fixture(scope="function")
def api_response_wrapper():
    """Provide APIResponse wrapper factory."""
    def wrapper(response):
        return APIResponse(response)
    return wrapper


# ==================== DATABASE FIXTURES ====================

@pytest.fixture(scope="session")
def mongodb_client(config):
    """Provide MongoDB client for tests.

    Yields:
        MongoDBClient instance (disconnects after all tests)
    """
    client = MongoDBClient(config)
    try:
        client.connect()
        yield client
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}. Database tests will be skipped.")
        yield None
    finally:
        try:
            client.disconnect()
        except Exception:
            pass


@pytest.fixture(scope="function")
def mongodb_test_helper(mongodb_client):
    """Provide MongoDB test helper with automatic cleanup.

    Yields:
        MongoDBTestHelper instance (cleans up after test)
    """
    if mongodb_client is None:
        pytest.skip("MongoDB not available")
    helper = MongoDBTestHelper(mongodb_client)
    yield helper
    helper.teardown_test_collections()


@pytest.fixture(scope="function")
def clean_mongodb_collection(mongodb_client):
    """Provide function to mark MongoDB collections for cleanup after test."""
    if mongodb_client is None:
        pytest.skip("MongoDB not available")

    collections_to_clean = []

    def mark_for_cleanup(collection_name: str):
        if collection_name not in collections_to_clean:
            collections_to_clean.append(collection_name)

    yield mark_for_cleanup

    for collection_name in collections_to_clean:
        try:
            mongodb_client.delete_many(collection_name, {})
        except Exception as e:
            logger.warning(f"Failed to clean collection {collection_name}: {e}")


# ==================== PARALLEL EXECUTION ====================

@pytest.fixture(scope="session")
def worker_id(request):
    """Provide unique worker ID for parallel test isolation.

    Returns 'master' when running without xdist, or 'gw0', 'gw1', etc.
    Use this to namespace test data in parallel runs.
    """
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"


# ==================== TEST DATA ====================

@pytest.fixture(scope="function")
def unique_id(worker_id):
    """Provide a unique identifier for test data isolation.

    Combines worker ID with a counter to ensure uniqueness
    across parallel workers and sequential tests.
    """
    import uuid
    short_id = str(uuid.uuid4())[:8]
    return f"{worker_id}_{short_id}"


# ==================== SALESFORCE FIXTURES ====================

@pytest.fixture(scope="session")
def sf_client(config):
    """Provide authenticated Salesforce client.

    Authenticates once per session. Skips if SF credentials not configured.

    Yields:
        SalesforceClient instance (closes after all tests)
    """
    from framework.salesforce_client import SalesforceClient
    import os

    if not os.environ.get('SF_CLIENT_ID'):
        pytest.skip("Salesforce not configured (SF_CLIENT_ID missing from .env)")

    client = SalesforceClient()
    if not client.authenticate():
        pytest.skip("Salesforce authentication failed")

    yield client
    client.close()


@pytest.fixture(scope="function")
def sf_cleanup(sf_client):
    """Provide automatic Salesforce record cleanup after test.

    Usage:
        def test_create_account(sf_client, sf_cleanup):
            result = sf_client.create("Account", {"Name": "Test"})
            sf_cleanup("Account", result["id"])
            # Record will be deleted after test
    """
    records_to_delete = []

    def mark_for_cleanup(sobject: str, record_id: str):
        records_to_delete.append((sobject, record_id))

    yield mark_for_cleanup

    for sobject, record_id in reversed(records_to_delete):
        try:
            sf_client.delete(sobject, record_id)
        except Exception as e:
            logger.warning(f"Failed to cleanup {sobject}/{record_id}: {e}")


# ==================== BOOMI FIXTURES ====================

@pytest.fixture(scope="session")
def boomi_client():
    """Provide Boomi middleware client.

    Skips if Boomi credentials not configured.

    Yields:
        BoomiClient instance (closes after all tests)
    """
    from framework.boomi_client import BoomiClient
    import os

    if not os.environ.get('BOOMI_ACCOUNT_ID'):
        pytest.skip("Boomi not configured (BOOMI_ACCOUNT_ID missing from .env)")

    client = BoomiClient()
    yield client
    client.close()
