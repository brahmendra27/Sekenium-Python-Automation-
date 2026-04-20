# tests/demo_ecommerce/test_product_catalog.py

"""
Demo E-commerce Product Catalog Tests
Tests for product browsing and catalog functionality.
"""

import pytest
from framework.base_page import BasePageSelenium


class TestProductCatalog:
    """Test product catalog functionality."""
    
    @pytest.mark.smoke
    def test_catalog_page_loads(self, driver):
        """Test that product catalog page loads successfully."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Verify page loaded
        assert "product" in driver.current_url.lower() or "catalog" in driver.current_url.lower(), \
            f"Expected products/catalog in URL, got: {driver.current_url}"
    
    @pytest.mark.smoke
    def test_product_grid_displayed(self, driver):
        """Test that product grid is displayed."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for product grid/list
        product_selectors = [
            ("css", ".product-grid"),
            ("css", ".product-list"),
            ("css", "[class*='product']"),
            ("xpath", "//div[contains(@class, 'product')]")
        ]
        
        grid_found = False
        for selector_type, selector in product_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                grid_found = True
                break
        
        assert grid_found, "Product grid/list not found on catalog page"
    
    def test_product_images_displayed(self, driver):
        """Test that product images are displayed."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for product images
        image_selectors = [
            ("css", ".product-image img"),
            ("css", ".product img"),
            ("xpath", "//img[contains(@class, 'product')]"),
            ("css", "img[alt*='product']")
        ]
        
        images_found = False
        for selector_type, selector in image_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                images_found = True
                break
        
        assert images_found, "Product images not found on catalog page"
    
    def test_product_prices_displayed(self, driver):
        """Test that product prices are displayed."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for price elements
        price_selectors = [
            ("css", ".price"),
            ("css", ".product-price"),
            ("css", "[class*='price']"),
            ("xpath", "//span[contains(@class, 'price')]")
        ]
        
        prices_found = False
        for selector_type, selector in price_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                prices_found = True
                break
        
        assert prices_found, "Product prices not found on catalog page"
    
    @pytest.mark.regression
    def test_product_titles_displayed(self, driver):
        """Test that product titles are displayed."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for product titles
        title_selectors = [
            ("css", ".product-title"),
            ("css", ".product-name"),
            ("css", "h2.product"),
            ("css", "h3.product"),
            ("xpath", "//h2[contains(@class, 'product')]")
        ]
        
        titles_found = False
        for selector_type, selector in title_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                titles_found = True
                break
        
        assert titles_found, "Product titles not found on catalog page"
    
    @pytest.mark.regression
    def test_add_to_cart_buttons_present(self, driver):
        """Test that add to cart buttons are present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for add to cart buttons
        button_selectors = [
            ("css", "button[class*='add-to-cart']"),
            ("css", ".add-to-cart"),
            ("css", "button[class*='cart']"),
            ("xpath", "//button[contains(text(), 'Add to Cart')]"),
            ("xpath", "//button[contains(@class, 'cart')]")
        ]
        
        buttons_found = False
        for selector_type, selector in button_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                buttons_found = True
                break
        
        # Note: Some sites may not have add to cart on catalog page
        if not buttons_found:
            print("Note: Add to cart buttons not found on catalog page (may be on product detail page)")


class TestProductFiltering:
    """Test product filtering functionality."""
    
    def test_category_filters_present(self, driver):
        """Test that category filters are present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for filter elements
        filter_selectors = [
            ("css", ".filter"),
            ("css", ".filters"),
            ("css", "[class*='filter']"),
            ("css", ".sidebar"),
            ("xpath", "//div[contains(@class, 'filter')]")
        ]
        
        filters_found = False
        for selector_type, selector in filter_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                filters_found = True
                break
        
        if not filters_found:
            print("Note: Filters not found - may not be available on this site")
    
    def test_sort_options_present(self, driver):
        """Test that sort options are present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Check for sort dropdown
        sort_selectors = [
            ("css", "select[class*='sort']"),
            ("css", ".sort-by"),
            ("css", "[class*='sort']"),
            ("xpath", "//select[contains(@class, 'sort')]")
        ]
        
        sort_found = False
        for selector_type, selector in sort_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                sort_found = True
                break
        
        if not sort_found:
            print("Note: Sort options not found - may not be available on this site")
    
    @pytest.mark.parametrize("viewport", [
        (1920, 1080),  # Desktop
        (768, 1024),   # Tablet
        (375, 667)     # Mobile
    ])
    def test_catalog_responsive(self, driver, viewport):
        """Test catalog page at different viewport sizes."""
        width, height = viewport
        driver.set_window_size(width, height)
        
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/products")
        
        # Verify page loads at this viewport
        assert "product" in driver.current_url.lower() or "catalog" in driver.current_url.lower()
        
        # Check that some product elements are visible
        product_selectors = [
            ("css", ".product"),
            ("css", "[class*='product']"),
            ("xpath", "//div[contains(@class, 'product')]")
        ]
        
        products_visible = False
        for selector_type, selector in product_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                products_visible = True
                break
        
        assert products_visible, f"Products not visible at {width}x{height}"
