"""
Home Page Object for Automation Test Store.

This module contains the Page Object Model for the homepage.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    """Page Object for Automation Test Store Homepage."""
    
    # Locators
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    CART_ICON = (By.CSS_SELECTOR, ".cart")
    CART_COUNT = (By.CSS_SELECTOR, ".cart .label-orange")
    LOGIN_LINK = (By.LINK_TEXT, "Login or register")
    
    # Product sections
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".thumbnails.grid.row")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".thumbnails.grid.row .thumbnail:first-child a")
    PRODUCT_LINKS = (By.CSS_SELECTOR, ".thumbnails.grid.row .thumbnail a.prdocutname")
    
    # Categories
    CATEGORIES_MENU = (By.CSS_SELECTOR, ".categorymenu")
    
    def __init__(self, driver):
        """
        Initialize HomePage.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = "https://automationteststore.com/"
    
    def navigate(self):
        """Navigate to homepage."""
        self.driver.get(self.base_url)
    
    def search_product(self, search_term):
        """
        Search for a product.
        
        Args:
            search_term: Product name or keyword to search
        """
        search_input = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(search_term)
        
        search_button = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button.click()
    
    def click_first_product(self):
        """Click on the first product in featured products."""
        first_product = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_PRODUCT)
        )
        first_product.click()
    
    def click_login_link(self):
        """Click on login/register link."""
        login_link = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_link.click()
    
    def get_cart_count(self):
        """
        Get the number of items in cart.
        
        Returns:
            int: Number of items in cart, 0 if cart is empty
        """
        try:
            cart_count = self.driver.find_element(*self.CART_COUNT)
            return int(cart_count.text)
        except:
            return 0
    
    def is_loaded(self):
        """
        Check if homepage is loaded.
        
        Returns:
            bool: True if homepage loaded successfully
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self.FEATURED_PRODUCTS)
            )
            return True
        except:
            return False
    
    def get_product_count(self):
        """
        Get number of products displayed on homepage.
        
        Returns:
            int: Number of products
        """
        try:
            products = self.driver.find_elements(*self.PRODUCT_LINKS)
            return len(products)
        except:
            return 0
