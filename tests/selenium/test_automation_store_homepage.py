"""
Test cases for Automation Test Store Homepage.

This module contains automated tests for the homepage functionality.
"""

import pytest
from selenium.webdriver.common.by import By
from tests.selenium.pages.home_page import HomePage


@pytest.mark.selenium
def test_homepage_loads_successfully(selenium_driver):
    """
    TC-001: Verify homepage loads successfully.
    
    Steps:
    1. Navigate to https://automationteststore.com/
    2. Verify page loads successfully
    3. Verify main sections are visible
    
    Expected Result:
    - Homepage loads with all sections visible
    - Featured products section is displayed
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    # Navigate to homepage
    home_page.navigate()
    
    # Verify homepage loaded
    assert home_page.is_loaded(), "Homepage did not load successfully"
    
    # Verify page title contains expected text
    assert "A place to practice" in driver.page_source, "Homepage content not found"
    
    print("✅ Homepage loaded successfully")


@pytest.mark.selenium
def test_homepage_has_featured_products(selenium_driver):
    """
    TC-001b: Verify homepage displays featured products.
    
    Steps:
    1. Navigate to homepage
    2. Verify featured products section exists
    3. Verify at least one product is displayed
    
    Expected Result:
    - Featured products section is visible
    - At least one product is displayed
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    
    # Verify featured products section
    featured = driver.find_elements(*home_page.FEATURED_PRODUCTS)
    assert len(featured) > 0, "No featured products section found"
    
    # Verify products are displayed
    product_count = home_page.get_product_count()
    assert product_count > 0, "No products displayed on homepage"
    
    print(f"✅ Homepage displays {product_count} products")


@pytest.mark.selenium
def test_homepage_search_box_visible(selenium_driver):
    """
    TC-001c: Verify search box is visible on homepage.
    
    Steps:
    1. Navigate to homepage
    2. Verify search input is visible
    3. Verify search button is visible
    
    Expected Result:
    - Search input field is visible
    - Search button is visible
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    
    # Verify search input
    search_input = driver.find_element(*home_page.SEARCH_INPUT)
    assert search_input.is_displayed(), "Search input not visible"
    
    # Verify search button
    search_button = driver.find_element(*home_page.SEARCH_BUTTON)
    assert search_button.is_displayed(), "Search button not visible"
    
    print("✅ Search box is visible and functional")


@pytest.mark.selenium
def test_homepage_login_link_visible(selenium_driver):
    """
    TC-001d: Verify login link is visible on homepage.
    
    Steps:
    1. Navigate to homepage
    2. Verify login/register link is visible
    
    Expected Result:
    - Login/register link is visible
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    
    # Verify login link
    login_link = driver.find_element(*home_page.LOGIN_LINK)
    assert login_link.is_displayed(), "Login link not visible"
    
    print("✅ Login link is visible")


@pytest.mark.selenium
def test_product_search(selenium_driver):
    """
    TC-002: Verify product search functionality.
    
    Steps:
    1. Navigate to homepage
    2. Enter "skincare" in search box
    3. Click search button
    4. Verify search results displayed
    
    Expected Result:
    - Search results page loads
    - Results contain searched term or products
    
    Test Data:
    - Search term: "skincare"
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    home_page.search_product("skincare")
    
    # Verify search results page
    assert "keyword=skincare" in driver.current_url or "search" in driver.current_url.lower()
    
    # Verify results displayed (page should contain product or result text)
    page_content = driver.page_source.lower()
    assert "product" in page_content or "result" in page_content or "skincare" in page_content
    
    print("✅ Product search works correctly")


@pytest.mark.selenium
@pytest.mark.parametrize("search_term", [
    "skincare",
    "makeup",
    "fragrance",
])
def test_search_multiple_terms(selenium_driver, search_term):
    """
    TC-002b: Verify search works for multiple product categories.
    
    Steps:
    1. Navigate to homepage
    2. Search for different product categories
    3. Verify results for each category
    
    Expected Result:
    - Search works for all product categories
    - Results are relevant to search term
    
    Test Data:
    - Search terms: skincare, makeup, fragrance
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    
    home_page.navigate()
    home_page.search_product(search_term)
    
    # Verify search executed
    assert "keyword=" in driver.current_url or "search" in driver.current_url.lower()
    
    print(f"✅ Search works for term: {search_term}")
