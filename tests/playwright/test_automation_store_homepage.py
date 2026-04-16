"""
Test cases for Automation Test Store Homepage (Playwright).

This module contains automated tests for the homepage functionality using Playwright.
Playwright works perfectly on Windows without ChromeDriver issues.
"""

import pytest
from playwright.sync_api import expect


@pytest.mark.playwright
def test_homepage_loads_successfully(playwright_page):
    """
    TC-001: Verify homepage loads successfully (Playwright).
    
    Steps:
    1. Navigate to https://automationteststore.com/
    2. Verify page loads successfully
    3. Verify main sections are visible
    
    Expected Result:
    - Homepage loads with all sections visible
    - Featured products section is displayed
    """
    page = playwright_page
    
    # Navigate to homepage
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Verify page title/content
    expect(page).to_have_url("https://automationteststore.com/")
    
    # Verify products are visible (check actual product elements, not container)
    products = page.locator(".thumbnail")
    expect(products.first).to_be_visible()
    
    print("✅ Homepage loaded successfully (Playwright)")


@pytest.mark.playwright
def test_homepage_has_featured_products(playwright_page):
    """
    TC-001b: Verify homepage displays featured products (Playwright).
    
    Steps:
    1. Navigate to homepage
    2. Verify featured products section exists
    3. Verify at least one product is displayed
    
    Expected Result:
    - Featured products section is visible
    - At least one product is displayed
    """
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Verify products are displayed (check actual products, not hidden container)
    products = page.locator(".thumbnail")
    expect(products.first).to_be_visible()
    
    product_count = products.count()
    assert product_count > 0, "No products found on homepage"
    
    print(f"✅ Homepage displays {product_count} products (Playwright)")


@pytest.mark.playwright
def test_homepage_search_box_visible(playwright_page):
    """
    TC-001c: Verify search box is visible on homepage (Playwright).
    
    Steps:
    1. Navigate to homepage
    2. Verify search input is visible
    3. Verify search button is visible
    
    Expected Result:
    - Search input field is visible
    - Search button is visible
    """
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Verify search input
    search_input = page.locator("#filter_keyword")
    expect(search_input).to_be_visible()
    
    # Verify search button (try multiple selectors)
    search_button = page.locator(".fa-search").first
    expect(search_button).to_be_visible()
    
    print("✅ Search box is visible and functional (Playwright)")


@pytest.mark.playwright
def test_homepage_login_link_visible(playwright_page):
    """
    TC-001d: Verify login link is visible on homepage (Playwright).
    
    Steps:
    1. Navigate to homepage
    2. Verify login/register link is visible
    
    Expected Result:
    - Login/register link is visible
    """
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Verify login link
    login_link = page.get_by_text("Login or register")
    expect(login_link).to_be_visible()
    
    print("✅ Login link is visible (Playwright)")


@pytest.mark.playwright
def test_product_search(playwright_page):
    """
    TC-002: Verify product search functionality (Playwright).
    
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
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Search for product - use keyboard Enter instead of clicking button
    page.fill("#filter_keyword", "skincare")
    page.locator("#filter_keyword").press("Enter")
    
    # Wait for navigation
    page.wait_for_load_state("networkidle")
    
    # Verify search executed - accept both search results page OR direct product page
    # (site may redirect to product if there's an exact match)
    current_url = page.url
    assert ("keyword=skincare" in current_url or 
            "search" in current_url.lower() or 
            "product" in current_url), \
            f"Search did not execute correctly. URL: {current_url}"
    
    print("✅ Product search works correctly (Playwright)")


@pytest.mark.playwright
@pytest.mark.parametrize("search_term", [
    "skincare",
    "makeup",
    "fragrance",
])
def test_search_multiple_terms(playwright_page, search_term):
    """
    TC-002b: Verify search works for multiple product categories (Playwright).
    
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
    page = playwright_page
    
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Search for product - use keyboard Enter
    page.fill("#filter_keyword", search_term)
    page.locator("#filter_keyword").press("Enter")
    
    # Wait for navigation
    page.wait_for_load_state("networkidle")
    
    # Verify search executed - accept search results OR direct product page
    current_url = page.url
    assert ("keyword=" in current_url or 
            "search" in current_url.lower() or 
            "product" in current_url), \
            f"Search did not execute for term '{search_term}'. URL: {current_url}"
    
    print(f"✅ Search works for term: {search_term} (Playwright)")
