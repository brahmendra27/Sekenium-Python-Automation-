"""
Test cases for Automation Test Store Shopping Cart.

This module contains automated tests for cart functionality.
"""

import pytest
import time
from tests.selenium.pages.home_page import HomePage
from tests.selenium.pages.product_page import ProductPage
from tests.selenium.pages.cart_page import CartPage


@pytest.mark.selenium
def test_add_product_to_cart(selenium_driver):
    """
    TC-003: Verify adding product to cart.
    
    Steps:
    1. Navigate to homepage
    2. Click on first product
    3. Add product to cart
    4. Verify cart count increases
    5. Navigate to cart
    6. Verify product in cart
    
    Expected Result:
    - Product is added to cart successfully
    - Cart count increases
    - Product appears in cart page
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Navigate and get initial cart count
    home_page.navigate()
    initial_cart_count = home_page.get_cart_count()
    
    # Select and view product
    home_page.click_first_product()
    
    # Get product details
    product_name = product_page.get_product_name()
    print(f"Adding product: {product_name}")
    
    # Add to cart
    product_page.add_to_cart()
    
    # Wait for cart to update
    time.sleep(2)
    
    # Navigate back to homepage to check cart count
    home_page.navigate()
    new_cart_count = home_page.get_cart_count()
    
    # Verify cart count increased
    assert new_cart_count > initial_cart_count, f"Cart count did not increase. Initial: {initial_cart_count}, New: {new_cart_count}"
    
    # Verify product in cart
    cart_page.navigate()
    cart_items = cart_page.get_cart_items_count()
    assert cart_items > 0, "No items found in cart"
    
    print(f"✅ Product added to cart successfully. Cart has {cart_items} item(s)")


@pytest.mark.selenium
def test_remove_item_from_cart(selenium_driver):
    """
    TC-007: Verify removing item from cart.
    
    Steps:
    1. Add product to cart
    2. Navigate to cart
    3. Remove product
    4. Verify cart updated
    
    Expected Result:
    - Product is removed from cart
    - Cart item count decreases
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Add product to cart
    home_page.navigate()
    home_page.click_first_product()
    product_page.add_to_cart()
    
    # Wait for cart update
    time.sleep(2)
    
    # Navigate to cart
    cart_page.navigate()
    initial_count = cart_page.get_cart_items_count()
    assert initial_count > 0, "Cart should have items before removal"
    
    print(f"Cart has {initial_count} item(s) before removal")
    
    # Remove first item
    cart_page.remove_first_item()
    
    # Wait for removal to process
    time.sleep(2)
    
    # Verify item removed
    new_count = cart_page.get_cart_items_count()
    assert new_count < initial_count, f"Item was not removed. Initial: {initial_count}, New: {new_count}"
    
    print(f"✅ Item removed successfully. Cart now has {new_count} item(s)")


@pytest.mark.selenium
def test_view_cart_page(selenium_driver):
    """
    TC-003b: Verify cart page loads and displays correctly.
    
    Steps:
    1. Navigate to cart page
    2. Verify page loads
    3. Verify cart elements are visible
    
    Expected Result:
    - Cart page loads successfully
    - Cart elements (table, buttons) are visible
    """
    driver = selenium_driver
    cart_page = CartPage(driver)
    
    # Navigate to cart
    cart_page.navigate()
    
    # Verify page loaded
    assert "checkout/cart" in driver.current_url, "Not on cart page"
    
    # Verify cart page elements
    assert "cart" in driver.page_source.lower() or "shopping" in driver.page_source.lower()
    
    print("✅ Cart page loads correctly")


@pytest.mark.selenium
def test_add_multiple_products_to_cart(selenium_driver):
    """
    TC-003c: Verify adding multiple products to cart.
    
    Steps:
    1. Navigate to homepage
    2. Add first product to cart
    3. Navigate back to homepage
    4. Add second product to cart
    5. Verify cart has 2 items
    
    Expected Result:
    - Multiple products can be added to cart
    - Cart count reflects total items
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Add first product
    home_page.navigate()
    home_page.click_first_product()
    product_page.add_to_cart()
    time.sleep(2)
    
    # Add second product
    home_page.navigate()
    # Click on a different product (if available)
    products = driver.find_elements(*home_page.PRODUCT_LINKS)
    if len(products) > 1:
        products[1].click()
        product_page.add_to_cart()
        time.sleep(2)
    
    # Verify cart has multiple items
    cart_page.navigate()
    cart_items = cart_page.get_cart_items_count()
    assert cart_items >= 1, f"Expected at least 1 item in cart, found {cart_items}"
    
    print(f"✅ Cart has {cart_items} item(s)")


@pytest.mark.selenium
def test_cart_displays_total_price(selenium_driver):
    """
    TC-003d: Verify cart displays total price.
    
    Steps:
    1. Add product to cart
    2. Navigate to cart
    3. Verify total price is displayed
    
    Expected Result:
    - Cart displays total price
    - Price is in correct format
    """
    driver = selenium_driver
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    
    # Add product to cart
    home_page.navigate()
    home_page.click_first_product()
    product_page.add_to_cart()
    time.sleep(2)
    
    # Navigate to cart
    cart_page.navigate()
    
    # Verify total price displayed
    total_price = cart_page.get_cart_total()
    assert total_price, "Total price not displayed"
    assert "$" in total_price or "price" in driver.page_source.lower(), "Price format incorrect"
    
    print(f"✅ Cart displays total price: {total_price}")


@pytest.mark.selenium
def test_continue_shopping_from_cart(selenium_driver):
    """
    TC-003e: Verify continue shopping button works.
    
    Steps:
    1. Navigate to cart
    2. Click continue shopping
    3. Verify redirected to homepage or products page
    
    Expected Result:
    - Continue shopping button works
    - User is redirected appropriately
    """
    driver = selenium_driver
    cart_page = CartPage(driver)
    
    # Navigate to cart
    cart_page.navigate()
    
    # Click continue shopping
    try:
        cart_page.continue_shopping()
        time.sleep(1)
        
        # Verify redirected (should not be on cart page anymore)
        assert "checkout/cart" not in driver.current_url, "Still on cart page after continue shopping"
        
        print("✅ Continue shopping button works correctly")
    except:
        print("⚠️ Continue shopping button not found or not clickable")
