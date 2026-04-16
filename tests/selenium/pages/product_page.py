"""
Product Page Object for Automation Test Store.

This module contains the Page Object Model for product details pages.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    """Page Object for Product Details Page."""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".productname")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productprice")
    PRODUCT_PRICE_NEW = (By.CSS_SELECTOR, ".productpricenew")
    PRODUCT_PRICE_OLD = (By.CSS_SELECTOR, ".productpriceold")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".cart")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product-image img")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".productdesc")
    
    def __init__(self, driver):
        """
        Initialize ProductPage.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def get_product_name(self):
        """
        Get product name.
        
        Returns:
            str: Product name
        """
        product_name = self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_NAME)
        )
        return product_name.text
    
    def get_product_price(self):
        """
        Get product price.
        
        Returns:
            str: Product price
        """
        try:
            # Try new price first (for sale items)
            product_price = self.driver.find_element(*self.PRODUCT_PRICE_NEW)
            return product_price.text
        except:
            # Fall back to regular price
            product_price = self.driver.find_element(*self.PRODUCT_PRICE)
            return product_price.text
    
    def add_to_cart(self):
        """Add product to cart."""
        add_button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )
        add_button.click()
    
    def set_quantity(self, quantity):
        """
        Set product quantity.
        
        Args:
            quantity: Quantity to set
        """
        quantity_input = self.driver.find_element(*self.QUANTITY_INPUT)
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
    
    def is_product_image_displayed(self):
        """
        Check if product image is displayed.
        
        Returns:
            bool: True if image is displayed
        """
        try:
            image = self.driver.find_element(*self.PRODUCT_IMAGE)
            return image.is_displayed()
        except:
            return False
    
    def get_product_description(self):
        """
        Get product description.
        
        Returns:
            str: Product description
        """
        try:
            description = self.driver.find_element(*self.PRODUCT_DESCRIPTION)
            return description.text
        except:
            return ""
