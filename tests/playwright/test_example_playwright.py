# tests/playwright/test_example_playwright.py

import pytest
from playwright.sync_api import expect


@pytest.mark.playwright
def test_example_navigation_and_interaction(playwright_page):
    """Example Playwright test demonstrating framework usage.
    
    This test serves as a template for QE engineers writing Playwright tests
    in the framework. It demonstrates:
    
    1. Navigation: Using page.goto() to navigate to a URL
    2. Element Interaction: Finding and interacting with page elements
    3. Auto-waiting: Playwright's built-in waiting for elements
    4. Assertions: Using Playwright's expect API for robust assertions
    
    The test uses the playwright_page fixture which:
    - Initializes Playwright browser context based on config.yaml settings
    - Creates a new page for the test
    - Enables tracing for debugging on failure
    - Captures screenshots on test failure
    - Automatically tears down the page and context after test completion
    
    Test Scenario:
    - Navigate to example.com
    - Verify page title
    - Locate and verify heading element
    - Interact with a link element
    - Assert expected page behavior
    
    Usage:
        Run this test with: pytest tests/playwright/test_example_playwright.py
        Run with specific browser: pytest --browser=firefox tests/playwright/test_example_playwright.py
        Run in headless mode: pytest --headless tests/playwright/test_example_playwright.py
    """
    page = playwright_page
    
    # 1. Navigation: Navigate to the application under test
    page.goto("https://example.com")
    
    # 2. Assertion: Verify page title using Playwright's expect API
    expect(page).to_have_title("Example Domain")
    
    # 3. Element Interaction: Find heading element using CSS selector
    heading = page.locator("h1")
    
    # Verify heading is visible (Playwright auto-waits for element)
    expect(heading).to_be_visible()
    
    # Verify heading text content
    expect(heading).to_have_text("Example Domain")
    
    # 4. Element Interaction: Find and verify paragraph text
    paragraph = page.locator("p").first
    expect(paragraph).to_be_visible()
    expect(paragraph).not_to_be_empty()
    
    # 5. Element Interaction: Find link element
    # Playwright auto-waits for element to be actionable
    link = page.locator("a")
    
    # 6. Element Interaction: Verify link properties
    expect(link).to_be_visible()
    expect(link).to_be_enabled()
    
    # Get and verify href attribute
    href = link.get_attribute("href")
    assert href is not None, "Link should have href attribute"
    assert "iana.org" in href, f"Expected 'iana.org' in href, got: {href}"
    
    # 7. Element Interaction: Verify link is actionable
    expect(link).to_be_enabled()
    
    # 8. Assertion: Verify page URL
    assert "example.com" in page.url, f"Expected example.com in URL, got: {page.url}"
    
    # 9. Element Interaction: Demonstrate getting element count
    all_links = page.locator("a")
    link_count = all_links.count()
    assert link_count > 0, f"Expected at least one link, found: {link_count}"


@pytest.mark.playwright
def test_example_multiple_elements(playwright_page):
    """Example test demonstrating interaction with multiple elements.
    
    This test shows how to:
    - Find multiple elements using locator.all()
    - Iterate over element collections
    - Verify element counts and properties
    - Use Playwright's count assertion
    
    Test Scenario:
    - Navigate to example.com
    - Find all paragraph elements
    - Verify count and properties of elements
    """
    page = playwright_page
    
    # Navigate to page
    page.goto("https://example.com")
    
    # Find all paragraph elements
    paragraphs = page.locator("p")
    
    # Verify we found at least one paragraph using Playwright's count assertion
    expect(paragraphs).not_to_have_count(0)
    
    # Get all paragraph elements
    paragraph_elements = paragraphs.all()
    
    # Verify all paragraphs are displayed and contain text
    for i, paragraph in enumerate(paragraph_elements):
        expect(paragraph).to_be_visible()
        expect(paragraph).not_to_be_empty()


@pytest.mark.playwright
def test_example_element_properties(playwright_page):
    """Example test demonstrating element property verification.
    
    This test shows how to:
    - Get element attributes
    - Verify element text content
    - Check element state (visible, enabled)
    - Use various Playwright locator strategies
    
    Test Scenario:
    - Navigate to example.com
    - Verify various element properties and attributes
    """
    page = playwright_page
    
    # Navigate to page
    page.goto("https://example.com")
    
    # Find heading element using tag name
    heading = page.locator("h1")
    
    # Verify element is visible
    expect(heading).to_be_visible()
    
    # Get and verify text content
    heading_text = heading.text_content()
    assert heading_text is not None, "Heading should have text content"
    assert "Example" in heading_text, f"Expected 'Example' in heading text, got: {heading_text}"
    
    # Verify using Playwright's text assertion
    expect(heading).to_contain_text("Example")
    
    # Find link using text selector
    link = page.locator("a")
    
    # Verify link attributes
    href = link.get_attribute("href")
    assert href is not None, "Link should have href attribute"
    assert href.startswith("http"), f"href should be a valid URL, got: {href}"
    
    # Verify link is visible and enabled
    expect(link).to_be_visible()
    expect(link).to_be_enabled()


@pytest.mark.playwright
def test_example_form_interaction(playwright_page):
    """Example test demonstrating form interaction patterns.
    
    This test shows how to:
    - Fill input fields using page.fill()
    - Click buttons
    - Handle form submissions
    - Verify form behavior
    
    Note: This test uses example.com which doesn't have forms,
    so it demonstrates the API patterns that would be used with actual forms.
    
    Test Scenario:
    - Navigate to example.com
    - Demonstrate form interaction patterns
    """
    page = playwright_page
    
    # Navigate to page
    page.goto("https://example.com")
    
    # Verify page loaded successfully
    expect(page).to_have_title("Example Domain")
    
    # Example patterns for form interaction (commented as example.com has no forms):
    # 
    # Fill text input:
    # page.fill("#username", "testuser")
    # 
    # Fill password input:
    # page.fill("#password", "password123")
    # 
    # Click submit button:
    # page.click("button[type='submit']")
    # 
    # Select dropdown option:
    # page.select_option("#country", "USA")
    # 
    # Check checkbox:
    # page.check("#terms")
    # 
    # Uncheck checkbox:
    # page.uncheck("#newsletter")
    # 
    # Upload file:
    # page.set_input_files("#file-upload", "path/to/file.txt")
    
    # Verify page content as placeholder for form verification
    expect(page.locator("h1")).to_have_text("Example Domain")


@pytest.mark.playwright
def test_example_waiting_strategies(playwright_page):
    """Example test demonstrating Playwright's waiting strategies.
    
    This test shows how to:
    - Use auto-waiting (Playwright's default behavior)
    - Wait for specific conditions
    - Handle dynamic content
    - Use timeout configurations
    
    Test Scenario:
    - Navigate to example.com
    - Demonstrate various waiting patterns
    """
    page = playwright_page
    
    # Navigate to page
    page.goto("https://example.com")
    
    # Playwright auto-waits for elements to be actionable
    # No explicit waits needed for most interactions
    heading = page.locator("h1")
    expect(heading).to_be_visible()
    
    # Wait for element to be visible (explicit wait)
    page.locator("p").first.wait_for(state="visible")
    
    # Wait for navigation (useful after clicks that trigger navigation)
    # page.wait_for_url("**/expected-path")
    
    # Wait for load state
    page.wait_for_load_state("networkidle")
    
    # Custom timeout for specific assertion (in milliseconds)
    expect(page.locator("h1")).to_be_visible(timeout=5000)
    
    # Verify content after waiting
    expect(page.locator("h1")).to_have_text("Example Domain")
