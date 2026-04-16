"""
Cart Page Object for Automation Test Store.

This module contains the Page Object Model for the shopping cart page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Page Object for Shopping Cart Page."""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".table.table-striped tbody tr")
    CHECKOUT_BUTTON = (By.ID, "cart_checkout1")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, ".btn.btn-default")
    CART_TOTAL = (By.CSS_SELECTOR, ".total-price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".btn.btn-sm.btn-default")
    UPDATE_BUTTON = (By.ID, "cart_update")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity']")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".contentpanel")
    
    def __init__(self, driver):
        """
        Initialize CartPage.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = "https://automationteststore.com/index.php?rt=checkout/cart"
    
    def navigate(self):
        """Navigate to cart page."""
        self.driver.get(self.base_url)
    
    def get_cart_items_count(self):
        """
        Get number of items in cart.
        
        Returns:
            int: Number of items in cart
        """
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            # Filter out header and footer rows
            actual_items = [item for item in items if item.find_elements(By.CSS_SELECTOR, "td.align_left")]
            return len(actual_items)
        except:
            return 0
    
    def click_checkout(self):
        """Click checkout button."""
        checkout_button = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        checkout_button.click()
    
    def remove_first_item(self):
        """Remove first item from cart."""
        remove_button = self.wait.until(
            EC.element_to_be_clickable(self.REMOVE_BUTTON)
        )
        remove_button.click()
    
    def update_quantity(self, quantity):
        """
        Update quantity of first item.
        
        Args:
            quantity: New quantity
        """
        quantity_input = self.wait.until(
            EC.presence_of_element_located(self.QUANTITY_INPUT)
        )
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        
        update_button = self.driver.find_element(*self.UPDATE_BUTTON)
        update_button.click()
    
    def get_cart_total(self):
        """
        Get cart total price.
        
        Returns:
            str: Cart total price
        """
        try:
            total = self.driver.find_element(*self.CART_TOTAL)
            return total.text
        except:
            return "$0.00"
    
    def is_cart_empty(self):
        """
        Check if cart is empty.
        
        Returns:
            bool: True if cart is empty
        """
        try:
            empty_message = self.driver.find_element(*self.EMPTY_CART_MESSAGE)
            return "empty" in empty_message.text.lower() or self.get_cart_items_count() == 0
        except:
            return self.get_cart_items_count() == 0
    
    def continue_shopping(self):
        """Click continue shopping button."""
        continue_button = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING)
        )
        continue_button.click()
