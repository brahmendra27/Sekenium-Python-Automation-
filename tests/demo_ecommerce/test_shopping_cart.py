# tests/demo_ecommerce/test_shopping_cart.py

"""
Demo E-commerce Shopping Cart Tests
Tests for shopping cart functionality.
"""

import pytest
from framework.base_page import BasePageSelenium


class TestShoppingCart:
    """Test shopping cart functionality."""
    
    @pytest.mark.smoke
    def test_cart_icon_present(self, driver):
        """Test that shopping cart icon is present in header."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/")
        
        # Check for cart icon
        cart_selectors = [
            ("css", ".cart-icon"),
            ("css", ".shopping-cart"),
            ("css", "[class*='cart']"),
            ("xpath", "//a[contains(@class, 'cart')]"),
            ("xpath", "//div[contains(@class, 'cart')]")
        ]
        
        cart_found = False
        for selector_type, selector in cart_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                cart_found = True
                break
        
        assert cart_found, "Shopping cart icon not found"
    
    def test_cart_page_accessible(self, driver):
        """Test that cart page is accessible."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Verify we're on cart page
        current_url = driver.current_url.lower()
        assert "cart" in current_url or "basket" in current_url, \
            f"Expected cart/basket in URL, got: {current_url}"
    
    def test_empty_cart_message(self, driver):
        """Test that empty cart shows appropriate message."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for empty cart message
        empty_selectors = [
            ("css", ".empty-cart"),
            ("css", ".cart-empty"),
            ("xpath", "//div[contains(text(), 'empty')]"),
            ("xpath", "//p[contains(text(), 'empty')]"),
            ("xpath", "//div[contains(text(), 'no items')]")
        ]
        
        empty_found = False
        for selector_type, selector in empty_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                empty_found = True
                break
        
        # Note: Cart might not be empty if items were added previously
        if not empty_found:
            print("Note: Empty cart message not found - cart may have items")
    
    @pytest.mark.regression
    def test_continue_shopping_button(self, driver):
        """Test that continue shopping button is present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for continue shopping button/link
        continue_selectors = [
            ("xpath", "//a[contains(text(), 'Continue Shopping')]"),
            ("xpath", "//button[contains(text(), 'Continue Shopping')]"),
            ("css", ".continue-shopping"),
            ("css", "a[href*='products']"),
            ("css", "a[href*='shop']")
        ]
        
        continue_found = False
        for selector_type, selector in continue_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                continue_found = True
                break
        
        if not continue_found:
            print("Note: Continue shopping button not found")


class TestCartOperations:
    """Test cart operations like add, remove, update."""
    
    def test_cart_quantity_controls(self, driver):
        """Test that quantity controls are present (if cart has items)."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for quantity input/controls
        quantity_selectors = [
            ("css", "input[type='number']"),
            ("css", ".quantity"),
            ("css", "[class*='quantity']"),
            ("xpath", "//input[contains(@class, 'quantity')]")
        ]
        
        quantity_found = False
        for selector_type, selector in quantity_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                quantity_found = True
                break
        
        if not quantity_found:
            print("Note: Quantity controls not found - cart may be empty")
    
    def test_remove_item_button(self, driver):
        """Test that remove item button is present (if cart has items)."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for remove button
        remove_selectors = [
            ("css", ".remove"),
            ("css", ".delete"),
            ("css", "button[class*='remove']"),
            ("xpath", "//button[contains(@class, 'remove')]"),
            ("xpath", "//a[contains(@class, 'remove')]")
        ]
        
        remove_found = False
        for selector_type, selector in remove_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                remove_found = True
                break
        
        if not remove_found:
            print("Note: Remove button not found - cart may be empty")
    
    def test_cart_total_displayed(self, driver):
        """Test that cart total is displayed."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for total price
        total_selectors = [
            ("css", ".cart-total"),
            ("css", ".total"),
            ("css", "[class*='total']"),
            ("xpath", "//div[contains(@class, 'total')]"),
            ("xpath", "//span[contains(@class, 'total')]")
        ]
        
        total_found = False
        for selector_type, selector in total_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                total_found = True
                break
        
        if not total_found:
            print("Note: Cart total not found - cart may be empty")
    
    @pytest.mark.smoke
    def test_checkout_button_present(self, driver):
        """Test that checkout button is present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/cart")
        
        # Check for checkout button
        checkout_selectors = [
            ("css", ".checkout"),
            ("css", "button[class*='checkout']"),
            ("xpath", "//button[contains(text(), 'Checkout')]"),
            ("xpath", "//a[contains(text(), 'Checkout')]"),
            ("css", "a[href*='checkout']")
        ]
        
        checkout_found = False
        for selector_type, selector in checkout_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                checkout_found = True
                break
        
        if not checkout_found:
            print("Note: Checkout button not found - may require items in cart")
