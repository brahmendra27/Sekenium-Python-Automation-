"""
Example test demonstrating self-healing element locators.

This test shows how to use the self-healing capabilities to automatically
recover from element locator failures.
"""

import pytest
from selenium.webdriver.common.by import By
from framework.self_healing import SelfHealingLocator


@pytest.mark.selenium
@pytest.mark.self_healing
def test_login_with_self_healing(selenium_driver):
    """
    Test login with self-healing element locators.
    
    If the original locators fail (e.g., due to UI changes), the self-healing
    mechanism will try alternative strategies to find the elements.
    """
    driver = selenium_driver
    healer = SelfHealingLocator(driver, enable_logging=True)
    
    # Navigate to login page
    driver.get("https://example.com/login")
    
    # Find username field with self-healing
    # If ID "username" doesn't exist, it will try:
    # - name="username"
    # - [data-testid="username"]
    # - [aria-label*="username"]
    # - etc.
    username_field = healer.find_element_with_healing(By.ID, "username")
    if username_field:
        username_field.send_keys("testuser")
    else:
        pytest.fail("Could not find username field even with self-healing")
    
    # Find password field with self-healing
    password_field = healer.find_element_with_healing(By.ID, "password")
    if password_field:
        password_field.send_keys("password123")
    else:
        pytest.fail("Could not find password field even with self-healing")
    
    # Find submit button with self-healing
    submit_button = healer.find_element_with_healing(By.ID, "submit")
    if submit_button:
        submit_button.click()
    else:
        pytest.fail("Could not find submit button even with self-healing")
    
    # Verify login success
    assert "Dashboard" in driver.title or "Home" in driver.title
    
    # Print healing report
    print("\n" + healer.get_healing_report())
    
    # Print suggestions for permanent fixes
    suggestions = healer.suggest_locator_improvements()
    if suggestions:
        print("\n🔧 Suggested Locator Improvements:")
        for suggestion in suggestions:
            print(suggestion)


@pytest.mark.selenium
@pytest.mark.self_healing
def test_search_with_self_healing(selenium_driver):
    """
    Test search functionality with self-healing.
    
    Demonstrates self-healing for multiple element types.
    """
    driver = selenium_driver
    healer = SelfHealingLocator(driver, enable_logging=True)
    
    # Navigate to homepage
    driver.get("https://example.com")
    
    # Find search input with self-healing
    search_input = healer.find_element_with_healing(By.NAME, "q")
    if search_input:
        search_input.send_keys("test automation")
    else:
        pytest.fail("Could not find search input even with self-healing")
    
    # Find search button with self-healing
    # Try multiple strategies: ID, class, CSS selector, XPath
    search_button = healer.find_element_with_healing(By.CLASS_NAME, "search-button")
    if search_button:
        search_button.click()
    else:
        pytest.fail("Could not find search button even with self-healing")
    
    # Verify search results
    results = healer.find_element_with_healing(By.CLASS_NAME, "search-results")
    assert results is not None, "Search results not found"
    
    # Print healing report
    print("\n" + healer.get_healing_report())
