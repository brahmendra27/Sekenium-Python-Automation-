# tests/selenium/test_example_selenium.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.selenium
def test_example_navigation_and_interaction(selenium_driver):
    """Example Selenium test demonstrating framework usage.
    
    This test serves as a template for QE engineers writing Selenium tests
    in the framework. It demonstrates:
    
    1. Navigation: Using driver.get() to navigate to a URL
    2. Element Interaction: Finding and interacting with page elements
    3. Explicit Waits: Using WebDriverWait for dynamic content
    4. Assertions: Verifying expected page state and element properties
    
    The test uses the selenium_driver fixture which:
    - Initializes WebDriver based on config.yaml settings
    - Sets implicit wait and page load timeout
    - Captures screenshots on test failure
    - Automatically tears down the driver after test completion
    
    Test Scenario:
    - Navigate to example.com
    - Verify page title
    - Locate and verify heading element
    - Interact with a link element
    - Assert expected page behavior
    
    Usage:
        Run this test with: pytest tests/selenium/test_example_selenium.py
        Run with specific browser: pytest --browser=firefox tests/selenium/test_example_selenium.py
        Run in headless mode: pytest --headless tests/selenium/test_example_selenium.py
    """
    driver = selenium_driver
    
    # 1. Navigation: Navigate to the application under test
    driver.get("https://example.com")
    
    # 2. Assertion: Verify page title
    assert "Example Domain" in driver.title, f"Expected 'Example Domain' in title, got: {driver.title}"
    
    # 3. Element Interaction: Find heading element using different locator strategies
    # Using CSS Selector
    heading = driver.find_element(By.CSS_SELECTOR, "h1")
    assert heading.is_displayed(), "Heading should be visible on the page"
    assert "Example Domain" in heading.text, f"Expected 'Example Domain' in heading, got: {heading.text}"
    
    # 4. Element Interaction: Find and verify paragraph text
    paragraph = driver.find_element(By.TAG_NAME, "p")
    assert paragraph.is_displayed(), "Paragraph should be visible"
    assert len(paragraph.text) > 0, "Paragraph should contain text"
    
    # 5. Explicit Wait: Wait for link element to be clickable
    wait = WebDriverWait(driver, 10)
    link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "More information..."))
    )
    
    # 6. Element Interaction: Verify link properties
    assert link.is_displayed(), "Link should be visible"
    assert link.is_enabled(), "Link should be enabled"
    href = link.get_attribute("href")
    assert href is not None, "Link should have href attribute"
    assert "iana.org" in href, f"Expected 'iana.org' in href, got: {href}"
    
    # 7. Navigation: Click the link (demonstrates interaction)
    link.click()
    
    # 8. Assertion: Verify navigation occurred
    wait.until(EC.url_contains("iana.org"))
    assert "iana.org" in driver.current_url, f"Expected navigation to iana.org, current URL: {driver.current_url}"
    
    # 9. Navigation: Navigate back to demonstrate browser controls
    driver.back()
    wait.until(EC.title_contains("Example Domain"))
    assert "example.com" in driver.current_url, "Should navigate back to example.com"


@pytest.mark.selenium
def test_example_multiple_elements(selenium_driver):
    """Example test demonstrating interaction with multiple elements.
    
    This test shows how to:
    - Find multiple elements using find_elements()
    - Iterate over element collections
    - Verify element counts and properties
    
    Test Scenario:
    - Navigate to example.com
    - Find all paragraph elements
    - Verify count and properties of elements
    """
    driver = selenium_driver
    
    # Navigate to page
    driver.get("https://example.com")
    
    # Find all paragraph elements
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    
    # Verify we found at least one paragraph
    assert len(paragraphs) > 0, "Should find at least one paragraph element"
    
    # Verify all paragraphs are displayed
    for i, paragraph in enumerate(paragraphs):
        assert paragraph.is_displayed(), f"Paragraph {i} should be visible"
        assert len(paragraph.text) > 0, f"Paragraph {i} should contain text"


@pytest.mark.selenium
def test_example_element_properties(selenium_driver):
    """Example test demonstrating element property verification.
    
    This test shows how to:
    - Get element attributes
    - Verify CSS properties
    - Check element state (displayed, enabled)
    
    Test Scenario:
    - Navigate to example.com
    - Verify various element properties and attributes
    """
    driver = selenium_driver
    
    # Navigate to page
    driver.get("https://example.com")
    
    # Find heading element
    heading = driver.find_element(By.TAG_NAME, "h1")
    
    # Verify element is displayed
    assert heading.is_displayed(), "Heading should be visible"
    
    # Get and verify text content
    heading_text = heading.text
    assert len(heading_text) > 0, "Heading should have text content"
    assert "Example" in heading_text, f"Expected 'Example' in heading text, got: {heading_text}"
    
    # Get tag name
    tag_name = heading.tag_name
    assert tag_name == "h1", f"Expected tag name 'h1', got: {tag_name}"
    
    # Find link and verify attributes
    link = driver.find_element(By.TAG_NAME, "a")
    href = link.get_attribute("href")
    assert href is not None, "Link should have href attribute"
    assert href.startswith("http"), f"href should be a valid URL, got: {href}"
