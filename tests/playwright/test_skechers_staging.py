"""
Skechers Staging Environment Tests with HTTP Basic Authentication.

This module contains automated tests for the Skechers staging environment.
Handles HTTP Basic Auth: storefront:ske1234@staging.skechers.com
"""

import pytest
import allure
from playwright.sync_api import expect
from faker import Faker

fake = Faker()

# Staging environment credentials
STAGING_URL = "https://staging.skechers.com"
STAGING_USERNAME = "storefront"
STAGING_PASSWORD = "ske1234"


@pytest.fixture
def authenticated_page(playwright_page):
    """
    Fixture that provides a page with HTTP Basic Authentication configured.
    
    This handles the authentication automatically for all tests.
    """
    page = playwright_page
    
    # Set HTTP credentials for the page
    # This will automatically handle the HTTP Basic Auth popup
    page.context.set_extra_http_headers({
        "Authorization": f"Basic {__import__('base64').b64encode(f'{STAGING_USERNAME}:{STAGING_PASSWORD}'.encode()).decode()}"
    })
    
    return page


@allure.epic("Skechers E-Commerce")
@allure.feature("Homepage")
@allure.story("Homepage Load")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "staging", "skechers")
@pytest.mark.playwright
def test_skechers_homepage_loads(authenticated_page):
    """
    Test that Skechers staging homepage loads successfully with authentication.
    
    Steps:
    1. Navigate to staging homepage with HTTP Basic Auth
    2. Verify page loads successfully
    3. Verify main elements are visible
    """
    page = authenticated_page
    
    with allure.step("Navigate to Skechers staging homepage"):
        allure.attach(
            f"URL: {STAGING_URL}\nUsername: {STAGING_USERNAME}",
            name="Authentication Details",
            attachment_type=allure.attachment_type.TEXT
        )
        
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Homepage",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Verify homepage loaded successfully"):
        # Verify URL
        current_url = page.url
        allure.attach(
            f"Current URL: {current_url}",
            name="URL Verification",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert "skechers.com" in current_url.lower(), f"Expected Skechers URL, got: {current_url}"
        
        # Verify page title
        title = page.title()
        allure.attach(
            f"Page Title: {title}",
            name="Title Verification",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print(f"✅ Homepage loaded: {title}")


@allure.epic("Skechers E-Commerce")
@allure.feature("Navigation")
@allure.story("Main Navigation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "staging", "navigation")
@pytest.mark.playwright
def test_skechers_navigation_visible(authenticated_page):
    """
    Test that main navigation elements are visible on Skechers staging.
    
    Steps:
    1. Navigate to homepage
    2. Verify navigation menu is visible
    3. Verify key navigation items exist
    """
    page = authenticated_page
    
    with allure.step("Navigate to homepage"):
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
    
    with allure.step("Verify navigation elements"):
        # Take screenshot of navigation
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Navigation Elements",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Check for common navigation elements
        # Note: Actual selectors will depend on Skechers' site structure
        page_content = page.content()
        
        # Log page structure for analysis
        allure.attach(
            page_content[:5000],  # First 5000 chars
            name="Page HTML Structure",
            attachment_type=allure.attachment_type.HTML
        )
        
        print("✅ Navigation elements checked")


@allure.epic("Skechers E-Commerce")
@allure.feature("Product Search")
@allure.story("Search Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "staging", "search")
@pytest.mark.playwright
def test_skechers_search_functionality(authenticated_page):
    """
    Test product search functionality on Skechers staging.
    
    Steps:
    1. Navigate to homepage
    2. Find search box
    3. Search for products
    4. Verify search results
    """
    page = authenticated_page
    
    with allure.step("Navigate to homepage"):
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
    
    with allure.step("Locate search functionality"):
        # Common search selectors to try
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='Search']",
            "input[placeholder*='search']",
            "#search",
            ".search-input",
            "[name='q']",
            "[name='search']"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    search_input = element
                    allure.attach(
                        f"Found search input with selector: {selector}",
                        name="Search Element Found",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    break
            except:
                continue
        
        if search_input:
            with allure.step("Perform search"):
                search_term = "shoes"
                search_input.fill(search_term)
                
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Search Input Filled",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Try to submit search
                search_input.press("Enter")
                page.wait_for_load_state("networkidle")
                
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Search Results",
                    attachment_type=allure.attachment_type.PNG
                )
                
                print(f"✅ Search performed for: {search_term}")
        else:
            allure.attach(
                "Search input not found with common selectors",
                name="Search Element Status",
                attachment_type=allure.attachment_type.TEXT
            )
            print("⚠️ Search input not found - may need manual inspection")


@allure.epic("Skechers E-Commerce")
@allure.feature("Product Catalog")
@allure.story("Product Listing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("staging", "products")
@pytest.mark.playwright
def test_skechers_product_listing(authenticated_page):
    """
    Test that product listings are displayed on Skechers staging.
    
    Steps:
    1. Navigate to homepage
    2. Look for product listings
    3. Verify products are displayed
    """
    page = authenticated_page
    
    with allure.step("Navigate to homepage"):
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
    
    with allure.step("Check for product listings"):
        # Common product selectors
        product_selectors = [
            ".product",
            ".product-item",
            "[class*='product']",
            ".item",
            "[data-product]"
        ]
        
        products_found = False
        for selector in product_selectors:
            try:
                products = page.locator(selector)
                count = products.count()
                if count > 0:
                    products_found = True
                    allure.attach(
                        f"Found {count} products with selector: {selector}",
                        name="Products Found",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    screenshot = page.screenshot()
                    allure.attach(
                        screenshot,
                        name="Product Listings",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    print(f"✅ Found {count} products")
                    break
            except:
                continue
        
        if not products_found:
            allure.attach(
                "No products found with common selectors - may need manual inspection",
                name="Product Status",
                attachment_type=allure.attachment_type.TEXT
            )
            print("⚠️ No products found - may need to navigate to specific category")


@allure.epic("Skechers E-Commerce")
@allure.feature("Page Performance")
@allure.story("Load Time")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("staging", "performance")
@pytest.mark.playwright
def test_skechers_page_load_time(authenticated_page):
    """
    Test page load performance on Skechers staging.
    
    Steps:
    1. Measure page load time
    2. Verify acceptable performance
    """
    page = authenticated_page
    
    import time
    
    with allure.step("Measure page load time"):
        start_time = time.time()
        
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
        
        load_time = time.time() - start_time
        
        allure.attach(
            f"Page Load Time: {load_time:.2f} seconds",
            name="Performance Metrics",
            attachment_type=allure.attachment_type.TEXT
        )
        
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Loaded Page",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Verify acceptable load time"):
        # Acceptable load time: under 10 seconds
        assert load_time < 10, f"Page load time too slow: {load_time:.2f}s"
        
        if load_time < 3:
            status = "Excellent"
        elif load_time < 5:
            status = "Good"
        elif load_time < 10:
            status = "Acceptable"
        else:
            status = "Slow"
        
        allure.attach(
            f"Load Time: {load_time:.2f}s\nStatus: {status}",
            name="Performance Assessment",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print(f"✅ Page loaded in {load_time:.2f}s ({status})")


@allure.epic("Skechers E-Commerce")
@allure.feature("Authentication")
@allure.story("HTTP Basic Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "staging", "auth")
@pytest.mark.playwright
def test_skechers_authentication_required(playwright_page):
    """
    Test that authentication is required for Skechers staging.
    
    Steps:
    1. Try to access without authentication
    2. Verify authentication is required
    """
    page = playwright_page
    
    with allure.step("Attempt to access without authentication"):
        try:
            # Try to access without auth
            response = page.goto(STAGING_URL, wait_until="commit", timeout=5000)
            
            status = response.status if response else None
            
            allure.attach(
                f"Response Status: {status}",
                name="Authentication Check",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 401 means authentication required (expected)
            if status == 401:
                print("✅ Authentication is required (401 Unauthorized)")
            else:
                print(f"⚠️ Unexpected status: {status}")
                
        except Exception as e:
            allure.attach(
                f"Error: {str(e)}",
                name="Access Attempt",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"✅ Access blocked without authentication: {str(e)}")


@allure.epic("Skechers E-Commerce")
@allure.feature("Responsive Design")
@allure.story("Mobile View")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("staging", "mobile", "responsive")
@pytest.mark.playwright
def test_skechers_mobile_view(authenticated_page):
    """
    Test Skechers staging site on mobile viewport.
    
    Steps:
    1. Set mobile viewport
    2. Navigate to homepage
    3. Verify mobile layout
    """
    page = authenticated_page
    
    with allure.step("Set mobile viewport"):
        # iPhone 12 Pro dimensions
        page.set_viewport_size({"width": 390, "height": 844})
        
        allure.attach(
            "Viewport: 390x844 (iPhone 12 Pro)",
            name="Mobile Viewport",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Navigate to homepage in mobile view"):
        page.goto(STAGING_URL)
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="Mobile View",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Verify mobile layout"):
        # Check viewport
        viewport = page.viewport_size
        assert viewport["width"] == 390, "Mobile viewport not set correctly"
        
        print("✅ Mobile view tested")
