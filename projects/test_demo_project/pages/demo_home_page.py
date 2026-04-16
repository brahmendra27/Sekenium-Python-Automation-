"""
Demo Home Page Object for testing the framework.

This page object demonstrates using the BasePageSelenium class.
"""

import allure
from selenium.webdriver.common.by import By
from framework.base_page import BasePageSelenium


class DemoHomePage(BasePageSelenium):
    """Page Object for Automation Test Store homepage (demo)."""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, ".logo")
    SEARCH_BOX = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".thumbnail")
    CART_ICON = (By.CSS_SELECTOR, ".cart")
    
    def __init__(self, driver):
        """
        Initialize the demo home page.
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.url = "https://automationteststore.com"
    
    @allure.step("Open demo homepage")
    def open(self):
        """Navigate to the demo homepage."""
        self.navigate_to(self.url)
        self.wait_for_page_load()
        return self
    
    @allure.step("Search for product: {product_name}")
    def search_product(self, product_name):
        """
        Search for a product.
        
        Args:
            product_name: Name of product to search for
            
        Returns:
            self for method chaining
        """
        self.type(self.SEARCH_BOX, product_name)
        self.click(self.SEARCH_BUTTON)
        return self
    
    @allure.step("Get featured products count")
    def get_featured_products_count(self):
        """
        Get the number of featured products displayed.
        
        Returns:
            int: Number of featured products
        """
        products = self.find_elements(self.FEATURED_PRODUCTS)
        count = len(products)
        
        allure.attach(
            f"Featured products count: {count}",
            name="Product Count",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return count
    
    @allure.step("Verify homepage is loaded")
    def is_loaded(self):
        """
        Verify that the homepage has loaded correctly.
        
        Returns:
            bool: True if homepage is loaded, False otherwise
        """
        logo_visible = self.is_visible(self.LOGO, timeout=10)
        search_visible = self.is_visible(self.SEARCH_BOX, timeout=10)
        
        return logo_visible and search_visible
    
    @allure.step("Get page title")
    def get_title(self):
        """
        Get the page title.
        
        Returns:
            str: Page title
        """
        return self.get_page_title()
