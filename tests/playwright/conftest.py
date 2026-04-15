# tests/playwright/conftest.py

import pytest
import os
from framework.config import Config
from framework.playwright_driver import PlaywrightDriver


@pytest.fixture(scope="function")
def playwright_context(request):
    """Pytest fixture providing Playwright browser context.
    
    This fixture initializes a Playwright browser context based on configuration,
    starts tracing if enabled, and handles screenshot and trace capture on test failure.
    
    Args:
        request: Pytest request object for accessing test context
        
    Yields:
        BrowserContext instance configured with tracing support
    """
    # Load configuration
    config = Config()
    playwright_config = config.get('playwright', {})
    
    # Determine browser type - map Selenium browser names to Playwright equivalents
    browser = config.browser
    if browser in ["chromium", "firefox", "webkit"]:
        browser_type = browser
    else:
        # Default to chromium for non-Playwright browser names (e.g., "chrome")
        browser_type = "chromium"
    
    # Initialize Playwright driver wrapper
    driver_wrapper = PlaywrightDriver(
        browser_type=browser_type,
        headless=config.headless,
        slow_mo=playwright_config.get('slow_mo', 0),
        tracing=playwright_config.get('tracing', True)
    )
    
    # Initialize browser context
    context = driver_wrapper.initialize()
    
    # Yield context to test
    yield context
    
    # Save trace file on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        # Save trace file if tracing is enabled
        trace_path = f"{config.report_dir}/traces/{request.node.name}.zip"
        driver_wrapper.quit(trace_path=trace_path)
    else:
        # Normal teardown without trace
        driver_wrapper.quit()


@pytest.fixture(scope="function")
def playwright_page(playwright_context, request):
    """Pytest fixture providing Playwright page.
    
    This fixture creates a new page from the browser context and ensures
    it is closed after the test completes. On test failure, captures screenshot
    before closing the page.
    
    Args:
        playwright_context: Browser context from playwright_context fixture
        request: Pytest request object for accessing test context
        
    Yields:
        Page instance for test execution
    """
    # Create new page from context
    page = playwright_context.new_page()
    
    # Yield page to test
    yield page
    
    # Capture screenshot on test failure before closing page
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        config = Config()
        screenshot_path = f"{config.report_dir}/screenshots/{request.node.name}.png"
        
        # Import PlaywrightDriver to use its capture_screenshot method
        driver_wrapper = PlaywrightDriver()
        
        if driver_wrapper.capture_screenshot(page, screenshot_path):
            # Attach screenshot to pytest-html report
            # Check if pytest-html plugin is available
            if hasattr(request.config, '_html'):
                extra = getattr(request.node, 'extra', [])
                # Import pytest_html to access the extras
                try:
                    from pytest_html import extras
                    extra.append(extras.image(screenshot_path))
                    request.node.extra = extra
                except ImportError:
                    pass
    
    # Close page after test
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot and trace on failure.
    
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
