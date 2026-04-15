# tests/selenium/conftest.py

import pytest
from framework.config import Config
from framework.selenium_driver import SeleniumDriver


@pytest.fixture(scope="function")
def selenium_driver(request):
    """Pytest fixture providing Selenium WebDriver instance.
    
    This fixture initializes a Selenium WebDriver based on configuration,
    sets timeouts, and handles screenshot capture on test failure.
    
    Args:
        request: Pytest request object for accessing test context
        
    Yields:
        WebDriver instance configured with implicit wait and page load timeout
    """
    # Load configuration
    config = Config()
    
    # Initialize Selenium driver wrapper
    driver_wrapper = SeleniumDriver(
        browser=config.browser,
        headless=config.headless
    )
    
    # Initialize WebDriver
    driver = driver_wrapper.initialize()
    
    # Set timeouts from config
    selenium_config = config.get('selenium', {})
    implicit_wait = selenium_config.get('implicit_wait', 10)
    page_load_timeout = selenium_config.get('page_load_timeout', 60)
    
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    # Yield driver to test
    yield driver
    
    # Capture screenshot on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_path = f"{config.report_dir}/screenshots/{request.node.name}.png"
        if driver_wrapper.capture_screenshot(screenshot_path):
            # Attach screenshot to pytest-html report
            extra = getattr(request.node, 'extra', [])
            extra.append(pytest.html.extra.image(screenshot_path))
            request.node.extra = extra
    
    # Tear down driver
    driver_wrapper.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure.
    
    This hook runs after each test phase (setup, call, teardown) and stores
    the test result on the item object so the fixture can access it.
    
    Args:
        item: Pytest test item
        call: Pytest call info
    """
    # Execute the test and get the result
    outcome = yield
    rep = outcome.get_result()
    
    # Store the result on the item for each phase (setup, call, teardown)
    setattr(item, f"rep_{rep.when}", rep)
