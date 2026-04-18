"""
Base Page Object class with common functionality for all page objects.

This module provides base classes for both Selenium and Playwright page objects,
implementing common patterns and utilities to reduce code duplication.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from playwright.sync_api import Page, expect
import allure


class BasePageSelenium:
    """Base class for Selenium Page Objects with common functionality."""
    
    def __init__(self, driver, timeout=30, base_url=None):
        """
        Initialize base page.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits in seconds
            base_url: Base URL for the application (optional, for relative URLs)
        """
        self.driver = driver
        self.timeout = timeout
        self.base_url = base_url or ""
        self.wait = WebDriverWait(driver, timeout)
    
    @allure.step("Navigate to {url}")
    def navigate_to(self, url):
        """
        Navigate to a URL (supports both absolute and relative URLs).
        
        Args:
            url: URL to navigate to (absolute or relative)
        """
        # If URL starts with http:// or https://, use it as-is
        if url.startswith(('http://', 'https://')):
            full_url = url
        # If URL is relative and base_url is set, combine them
        elif self.base_url:
            # Remove trailing slash from base_url and leading slash from url if both exist
            base = self.base_url.rstrip('/')
            path = url.lstrip('/') if url.startswith('/') else url
            full_url = f"{base}/{path}"
        else:
            # No base_url set, use URL as-is (might fail if relative)
            full_url = url
        
        self.driver.get(full_url)
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator_type, locator_value=None):
        """
        Find element with explicit wait.
        
        Args:
            locator_type: Either a tuple of (By.TYPE, "selector") or a string like "css", "xpath", etc.
            locator_value: Selector value (required if locator_type is a string)
            
        Returns:
            WebElement
        """
        from selenium.webdriver.common.by import By
        
        # If locator_type is a tuple, use it directly
        if isinstance(locator_type, tuple):
            locator = locator_type
        # If locator_type is a string, convert to tuple
        elif isinstance(locator_type, str) and locator_value is not None:
            selector_map = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME,
                "link_text": By.LINK_TEXT,
                "partial_link_text": By.PARTIAL_LINK_TEXT
            }
            by_type = selector_map.get(locator_type.lower(), By.CSS_SELECTOR)
            locator = (by_type, locator_value)
        else:
            raise ValueError("Invalid locator format. Use tuple (By.TYPE, 'selector') or strings ('css', 'selector')")
        
        return self.wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Find elements: {locator}")
    def find_elements(self, locator):
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            
        Returns:
            List of WebElements
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Click element: {locator}")
    def click(self, locator):
        """
        Click element with wait for clickability.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Type '{text}' into {locator}")
    def type(self, locator, text):
        """
        Type text into element after clearing it.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            text: Text to type
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Get text from {locator}")
    def get_text(self, locator):
        """
        Get text content from element.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            
        Returns:
            str: Element text
        """
        return self.find_element(locator).text
    
    @allure.step("Get attribute '{attribute}' from {locator}")
    def get_attribute(self, locator, attribute):
        """
        Get attribute value from element.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            attribute: Attribute name
            
        Returns:
            str: Attribute value
        """
        return self.find_element(locator).get_attribute(attribute)
    
    @allure.step("Check if element is visible: {locator}")
    def is_visible(self, locator, timeout=None):
        """
        Check if element is visible within timeout.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            timeout: Optional custom timeout
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("Check if element exists: {locator}")
    def element_exists(self, locator, timeout=None):
        """
        Check if element exists in DOM (may not be visible).
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            timeout: Optional custom timeout
            
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("Check if element is present: {selector_type}={selector}")
    def is_element_present(self, selector_type, selector, timeout=5):
        """
        Check if element is present in DOM using string selector type and value.
        
        Args:
            selector_type: Type of selector ("css", "xpath", "id", "name", "class", "tag")
            selector: Selector value
            timeout: Optional custom timeout (default 5 seconds for quick checks)
            
        Returns:
            bool: True if present, False otherwise
        """
        from selenium.webdriver.common.by import By
        
        # Map string selector types to By constants
        selector_map = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        
        by_type = selector_map.get(selector_type.lower(), By.CSS_SELECTOR)
        locator = (by_type, selector)
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for page to be fully loaded (document.readyState == 'complete')."""
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @allure.step("Wait for element to disappear: {locator}")
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        Wait for element to become invisible or removed from DOM.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
            timeout: Optional custom timeout
        """
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.invisibility_of_element_located(locator)
        )
    
    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator):
        """
        Scroll element into view.
        
        Args:
            locator: Tuple of (By.TYPE, "selector")
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @allure.step("Get current URL")
    def get_current_url(self):
        """
        Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    @allure.step("Get page title")
    def get_page_title(self):
        """
        Get current page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title


class BasePagePlaywright:
    """Base class for Playwright Page Objects with common functionality."""
    
    def __init__(self, page: Page, timeout=30000):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page instance
            timeout: Default timeout for waits in milliseconds
        """
        self.page = page
        self.timeout = timeout
    
    @allure.step("Navigate to {url}")
    def navigate_to(self, url):
        """Navigate to a URL and wait for network idle."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Click element: {selector}")
    def click(self, selector):
        """
        Click element.
        
        Args:
            selector: CSS selector or other supported selector
        """
        self.page.click(selector, timeout=self.timeout)
    
    @allure.step("Type '{text}' into {selector}")
    def type(self, selector, text):
        """
        Type text into element (clears first).
        
        Args:
            selector: CSS selector or other supported selector
            text: Text to type
        """
        self.page.fill(selector, text, timeout=self.timeout)
    
    @allure.step("Get text from {selector}")
    def get_text(self, selector):
        """
        Get text content from element.
        
        Args:
            selector: CSS selector or other supported selector
            
        Returns:
            str: Element text
        """
        return self.page.locator(selector).text_content(timeout=self.timeout)
    
    @allure.step("Get attribute '{attribute}' from {selector}")
    def get_attribute(self, selector, attribute):
        """
        Get attribute value from element.
        
        Args:
            selector: CSS selector or other supported selector
            attribute: Attribute name
            
        Returns:
            str: Attribute value
        """
        return self.page.locator(selector).get_attribute(attribute, timeout=self.timeout)
    
    @allure.step("Check if element is visible: {selector}")
    def is_visible(self, selector, timeout=None):
        """
        Check if element is visible within timeout.
        
        Args:
            selector: CSS selector or other supported selector
            timeout: Optional custom timeout in milliseconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            self.page.locator(selector).wait_for(state="visible", timeout=wait_time)
            return True
        except:
            return False
    
    @allure.step("Check if element exists: {selector}")
    def element_exists(self, selector, timeout=None):
        """
        Check if element exists in DOM (may not be visible).
        
        Args:
            selector: CSS selector or other supported selector
            timeout: Optional custom timeout in milliseconds
            
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            self.page.locator(selector).wait_for(state="attached", timeout=wait_time)
            return True
        except:
            return False
    
    @allure.step("Wait for selector: {selector}")
    def wait_for_selector(self, selector, state="visible"):
        """
        Wait for selector to be in specified state.
        
        Args:
            selector: CSS selector or other supported selector
            state: State to wait for (visible, attached, detached, hidden)
        """
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)
    
    @allure.step("Wait for element to disappear: {selector}")
    def wait_for_element_to_disappear(self, selector, timeout=None):
        """
        Wait for element to become hidden or detached.
        
        Args:
            selector: CSS selector or other supported selector
            timeout: Optional custom timeout in milliseconds
        """
        wait_time = timeout or self.timeout
        self.page.locator(selector).wait_for(state="hidden", timeout=wait_time)
    
    @allure.step("Scroll to element: {selector}")
    def scroll_to_element(self, selector):
        """
        Scroll element into view.
        
        Args:
            selector: CSS selector or other supported selector
        """
        self.page.locator(selector).scroll_into_view_if_needed(timeout=self.timeout)
    
    @allure.step("Take screenshot")
    def take_screenshot(self, name="screenshot"):
        """
        Take screenshot and attach to Allure report.
        
        Args:
            name: Screenshot name for Allure report
        """
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Get current URL")
    def get_current_url(self):
        """
        Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.page.url
    
    @allure.step("Get page title")
    def get_page_title(self):
        """
        Get current page title.
        
        Returns:
            str: Page title
        """
        return self.page.title()
    
    @allure.step("Press key: {key}")
    def press_key(self, selector, key):
        """
        Press a key on an element.
        
        Args:
            selector: CSS selector or other supported selector
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
        """
        self.page.locator(selector).press(key, timeout=self.timeout)
    
    @allure.step("Select option: {value}")
    def select_option(self, selector, value):
        """
        Select option from dropdown.
        
        Args:
            selector: CSS selector for select element
            value: Option value to select
        """
        self.page.select_option(selector, value, timeout=self.timeout)
    
    @allure.step("Check checkbox: {selector}")
    def check_checkbox(self, selector):
        """
        Check a checkbox.
        
        Args:
            selector: CSS selector for checkbox
        """
        self.page.check(selector, timeout=self.timeout)
    
    @allure.step("Uncheck checkbox: {selector}")
    def uncheck_checkbox(self, selector):
        """
        Uncheck a checkbox.
        
        Args:
            selector: CSS selector for checkbox
        """
        self.page.uncheck(selector, timeout=self.timeout)
