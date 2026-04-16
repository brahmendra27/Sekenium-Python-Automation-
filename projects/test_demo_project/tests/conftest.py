"""
Project-specific fixtures and configuration.

This file contains fixtures specific to this project.
Copy this file to conftest.py and customize as needed.
"""

import pytest
import yaml
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import framework components
from framework.config import Config
from framework.selenium_driver import SeleniumDriver
from framework.playwright_driver import PlaywrightDriver


@pytest.fixture(scope="session")
def project_config():
    """Load project-specific configuration."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def base_url(project_config):
    """Provide base URL for the project."""
    return project_config['base_url']


@pytest.fixture(scope="session")
def test_user(project_config):
    """Provide test user credentials."""
    users = project_config.get('test_users', [])
    if users:
        return users[0]
    return None


# Selenium fixture
@pytest.fixture(scope="function")
def selenium_driver(request):
    """Pytest fixture providing Selenium WebDriver instance."""
    config = Config()
    
    driver_wrapper = SeleniumDriver(
        browser=config.browser,
        headless=config.headless
    )
    
    driver = driver_wrapper.initialize()
    
    selenium_config = config.get('selenium', {})
    driver.implicitly_wait(selenium_config.get('implicit_wait', 10))
    driver.set_page_load_timeout(selenium_config.get('page_load_timeout', 60))
    
    yield driver
    
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_path = f"{config.report_dir}/screenshots/{request.node.name}.png"
        driver_wrapper.capture_screenshot(screenshot_path)
    
    driver_wrapper.quit()


# Playwright fixtures
@pytest.fixture(scope="function")
def playwright_context(request):
    """Pytest fixture providing Playwright browser context."""
    config = Config()
    playwright_config = config.get('playwright', {})
    
    driver_wrapper = PlaywrightDriver(
        browser_type=config.browser if config.browser in ["chromium", "firefox", "webkit"] else "chromium",
        headless=config.headless,
        slow_mo=playwright_config.get('slow_mo', 0),
        tracing=playwright_config.get('tracing', True)
    )
    context = driver_wrapper.initialize()
    
    yield context
    
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        page = context.pages[0] if context.pages else None
        if page:
            screenshot_path = f"{config.report_dir}/screenshots/{request.node.name}.png"
            driver_wrapper.capture_screenshot(page, screenshot_path)
        
        trace_path = f"{config.report_dir}/traces/{request.node.name}.zip"
        driver_wrapper.quit(trace_path=trace_path)
    else:
        driver_wrapper.quit()


@pytest.fixture(scope="function")
def playwright_page(playwright_context):
    """Pytest fixture providing Playwright page."""
    page = playwright_context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
