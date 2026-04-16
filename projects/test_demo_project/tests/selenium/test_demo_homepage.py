"""
Demo homepage tests using Selenium and Page Object Model.

This test demonstrates:
1. Using the BasePageSelenium class
2. Page Object Model pattern
3. Allure reporting integration
4. Framework fixtures
"""

import pytest
import allure
from projects.test_demo_project.pages.demo_home_page import DemoHomePage


@allure.epic("Demo Project")
@allure.feature("Homepage")
@allure.story("Homepage Load")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "demo", "homepage")
@pytest.mark.selenium
@pytest.mark.test_demo_project
def test_demo_homepage_loads_successfully(selenium_driver):
    """
    Test that the demo homepage loads successfully.
    
    This test verifies:
    1. Homepage can be opened
    2. Logo is visible
    3. Search box is visible
    4. Featured products are displayed
    
    Steps:
    1. Initialize page object
    2. Open homepage
    3. Verify page is loaded
    4. Verify featured products exist
    """
    
    with allure.step("Initialize demo home page"):
        home_page = DemoHomePage(selenium_driver)
        allure.attach(
            "Using BasePageSelenium class",
            name="Page Object Info",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Open demo homepage"):
        home_page.open()
        
        current_url = home_page.get_current_url()
        allure.attach(
            f"Current URL: {current_url}",
            name="URL Verification",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Verify homepage is loaded"):
        assert home_page.is_loaded(), "Homepage did not load correctly"
        
        page_title = home_page.get_title()
        allure.attach(
            f"Page Title: {page_title}",
            name="Title Verification",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print(f"✅ Homepage loaded successfully: {page_title}")
    
    with allure.step("Verify featured products are displayed"):
        product_count = home_page.get_featured_products_count()
        
        assert product_count > 0, f"Expected featured products, found {product_count}"
        
        allure.attach(
            f"Found {product_count} featured products",
            name="Product Verification",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print(f"✅ Found {product_count} featured products")


@allure.epic("Demo Project")
@allure.feature("Product Search")
@allure.story("Search Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "demo", "search")
@pytest.mark.selenium
@pytest.mark.test_demo_project
def test_demo_product_search(selenium_driver):
    """
    Test product search functionality using Page Object Model.
    
    This test verifies:
    1. Search box is functional
    2. Search results are displayed
    
    Steps:
    1. Open homepage
    2. Search for a product
    3. Verify search was executed
    """
    
    with allure.step("Initialize and open homepage"):
        home_page = DemoHomePage(selenium_driver)
        home_page.open()
    
    with allure.step("Search for 'skincare'"):
        search_term = "skincare"
        home_page.search_product(search_term)
        
        allure.attach(
            f"Search term: {search_term}",
            name="Search Input",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Verify search was executed"):
        current_url = home_page.get_current_url()
        
        allure.attach(
            f"Result URL: {current_url}",
            name="Search Result URL",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Verify URL contains search term or search keyword
        assert "skincare" in current_url.lower() or "keyword=" in current_url.lower(), \
            f"Search did not execute correctly. URL: {current_url}"
        
        print(f"✅ Search executed successfully")


@allure.epic("Demo Project")
@allure.feature("Base Page Methods")
@allure.story("Method Testing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("demo", "base-class")
@pytest.mark.selenium
@pytest.mark.test_demo_project
def test_demo_base_page_methods(selenium_driver):
    """
    Test various base page methods to verify functionality.
    
    This test demonstrates:
    1. Element visibility checks
    2. Element existence checks
    3. Text retrieval
    4. URL and title retrieval
    
    This validates that the BasePageSelenium class works correctly.
    """
    
    with allure.step("Initialize page and navigate"):
        home_page = DemoHomePage(selenium_driver)
        home_page.open()
    
    with allure.step("Test is_visible() method"):
        logo_visible = home_page.is_visible(home_page.LOGO)
        assert logo_visible, "Logo should be visible"
        print("✅ is_visible() works correctly")
    
    with allure.step("Test element_exists() method"):
        search_exists = home_page.element_exists(home_page.SEARCH_BOX)
        assert search_exists, "Search box should exist"
        print("✅ element_exists() works correctly")
    
    with allure.step("Test get_current_url() method"):
        url = home_page.get_current_url()
        assert "automationteststore.com" in url, f"Unexpected URL: {url}"
        print(f"✅ get_current_url() works correctly: {url}")
    
    with allure.step("Test get_page_title() method"):
        title = home_page.get_page_title()
        assert len(title) > 0, "Title should not be empty"
        print(f"✅ get_page_title() works correctly: {title}")
    
    with allure.step("Summary"):
        allure.attach(
            "All base page methods tested successfully:\n"
            "- is_visible()\n"
            "- element_exists()\n"
            "- get_current_url()\n"
            "- get_page_title()\n"
            "- navigate_to()\n"
            "- wait_for_page_load()",
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print("✅ All base page methods work correctly!")
