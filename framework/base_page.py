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
    """Base class for Playwright Page Objects with common functionality.
    
    All page objects should inherit from this class.
    Provides 80+ reusable Playwright actions matching AQE-KIRO standards.
    """
    
    def __init__(self, page: Page, timeout=30000):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page instance
            timeout: Default timeout for waits in milliseconds
        """
        self.page = page
        self.timeout = timeout

    # ==================== NAVIGATION ====================

    @allure.step("Navigate to {url}")
    def navigate_to(self, url, wait_until='domcontentloaded'):
        """Navigate to URL."""
        self.page.goto(url, wait_until=wait_until)

    def reload_page(self):
        """Reload current page."""
        self.page.reload()

    def go_back(self):
        """Navigate back."""
        self.page.go_back()

    def go_forward(self):
        """Navigate forward."""
        self.page.go_forward()

    def refresh(self):
        """Refresh page (alias for reload_page)."""
        self.page.reload()

    def close_page(self):
        """Close current page."""
        self.page.close()

    # ==================== ELEMENT LOCATION ====================

    def find_element(self, selector):
        """Find single element."""
        return self.page.locator(selector).first

    def find_elements(self, selector):
        """Find all matching elements."""
        return self.page.locator(selector).all()

    def element_exists(self, selector, timeout=5000):
        """Check if element exists."""
        try:
            return self.page.locator(selector).first.is_visible(timeout=timeout)
        except:
            return False

    def count_elements(self, selector):
        """Count matching elements."""
        return self.page.locator(selector).count()

    # ==================== CLICK ACTIONS ====================

    @allure.step("Click element: {selector}")
    def click(self, selector, timeout=None, force=False):
        """Click element."""
        self.page.locator(selector).first.click(
            timeout=timeout or self.timeout, force=force
        )

    def click_with_retry(self, selector, max_attempts=3):
        """Click with retry logic."""
        for attempt in range(max_attempts):
            try:
                self.click(selector)
                return True
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                self.wait(1000)
        return False

    def double_click(self, selector):
        """Double click element."""
        self.page.locator(selector).first.dblclick()

    def right_click(self, selector):
        """Right click element."""
        self.page.locator(selector).first.click(button='right')

    def click_at_position(self, selector, x, y):
        """Click at specific position within element."""
        self.page.locator(selector).first.click(position={'x': x, 'y': y})

    # ==================== INPUT ACTIONS ====================

    @allure.step("Fill '{text}' into {selector}")
    def fill(self, selector, text, clear_first=True):
        """Fill input field."""
        element = self.page.locator(selector).first
        if clear_first:
            element.clear()
        element.fill(text)

    @allure.step("Type '{text}' into {selector}")
    def type(self, selector, text):
        """Type text into element (clears first). Alias for fill."""
        self.fill(selector, text)

    def type_text(self, selector, text, delay=0):
        """Type text character by character."""
        self.page.locator(selector).first.type(text, delay=delay)

    @allure.step("Press key: {key}")
    def press_key(self, selector, key):
        """Press key on element."""
        self.page.locator(selector).first.press(key)

    def clear_input(self, selector):
        """Clear input field."""
        self.page.locator(selector).first.clear()

    def upload_file(self, selector, file_path):
        """Upload file(s)."""
        self.page.locator(selector).first.set_input_files(file_path)

    # ==================== CHECKBOX/RADIO ====================

    @allure.step("Check: {selector}")
    def check(self, selector):
        """Check checkbox or radio button."""
        self.page.locator(selector).first.check()

    @allure.step("Uncheck: {selector}")
    def uncheck(self, selector):
        """Uncheck checkbox."""
        self.page.locator(selector).first.uncheck()

    def is_checked(self, selector):
        """Check if checkbox/radio is checked."""
        return self.page.locator(selector).first.is_checked()

    # Keep old aliases
    def check_checkbox(self, selector):
        """Check a checkbox (alias for check)."""
        self.check(selector)

    def uncheck_checkbox(self, selector):
        """Uncheck a checkbox (alias for uncheck)."""
        self.uncheck(selector)

    # ==================== DROPDOWN ====================

    @allure.step("Select option: {selector}")
    def select_option(self, selector, value=None, label=None, index=None):
        """Select dropdown option by value, label, or index."""
        element = self.page.locator(selector).first
        if value:
            element.select_option(value=value)
        elif label:
            element.select_option(label=label)
        elif index is not None:
            element.select_option(index=index)

    # ==================== HOVER & FOCUS ====================

    @allure.step("Hover: {selector}")
    def hover(self, selector):
        """Hover over element."""
        self.page.locator(selector).first.hover()

    @allure.step("Focus: {selector}")
    def focus(self, selector):
        """Focus element."""
        self.page.locator(selector).first.focus()

    # ==================== GET INFORMATION ====================

    @allure.step("Get text from {selector}")
    def get_text(self, selector):
        """Get element text."""
        return self.page.locator(selector).first.text_content() or ""

    def get_inner_text(self, selector):
        """Get inner text."""
        return self.page.locator(selector).first.inner_text()

    @allure.step("Get attribute '{attribute}' from {selector}")
    def get_attribute(self, selector, attribute):
        """Get element attribute."""
        return self.page.locator(selector).first.get_attribute(attribute)

    def get_value(self, selector):
        """Get input value."""
        return self.page.locator(selector).first.input_value()

    def get_all_text(self, selector):
        """Get text from all matching elements."""
        elements = self.find_elements(selector)
        return [el.text_content() or "" for el in elements]

    # ==================== VISIBILITY & STATE ====================

    @allure.step("Check if visible: {selector}")
    def is_visible(self, selector, timeout=None):
        """Check if element is visible."""
        try:
            return self.page.locator(selector).first.is_visible(
                timeout=timeout or 5000
            )
        except:
            return False

    def is_hidden(self, selector):
        """Check if element is hidden."""
        return self.page.locator(selector).first.is_hidden()

    def is_enabled(self, selector):
        """Check if element is enabled."""
        return self.page.locator(selector).first.is_enabled()

    def is_disabled(self, selector):
        """Check if element is disabled."""
        return self.page.locator(selector).first.is_disabled()

    def is_editable(self, selector):
        """Check if element is editable."""
        return self.page.locator(selector).first.is_editable()

    # ==================== WAIT ACTIONS ====================

    def wait_for_element(self, selector, state='visible', timeout=None):
        """Wait for element state (visible, hidden, attached, detached)."""
        self.page.locator(selector).first.wait_for(
            state=state, timeout=timeout or self.timeout
        )

    def wait_for_url(self, url_pattern, timeout=None):
        """Wait for URL to match pattern."""
        self.page.wait_for_url(url_pattern, timeout=timeout or self.timeout)

    def wait_for_load_state(self, state='load'):
        """Wait for page load state (load, domcontentloaded, networkidle)."""
        self.page.wait_for_load_state(state)

    def wait(self, milliseconds):
        """Wait for specified time."""
        self.page.wait_for_timeout(milliseconds)

    def wait_for_selector(self, selector, state="visible", timeout=None):
        """Wait for selector to appear."""
        self.page.wait_for_selector(
            selector, state=state, timeout=timeout or self.timeout
        )

    def wait_for_element_to_disappear(self, selector, timeout=None):
        """Wait for element to become hidden or detached."""
        self.page.locator(selector).wait_for(
            state="hidden", timeout=timeout or self.timeout
        )

    # ==================== SCROLL ACTIONS ====================

    @allure.step("Scroll to element: {selector}")
    def scroll_to_element(self, selector):
        """Scroll element into view."""
        self.page.locator(selector).first.scroll_into_view_if_needed()

    def scroll_to_top(self):
        """Scroll to top of page."""
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_by(self, x, y):
        """Scroll by pixels."""
        self.page.mouse.wheel(x, y)

    # ==================== SCREENSHOT ====================

    @allure.step("Take screenshot")
    def take_screenshot(self, path=None, full_page=False, name="screenshot"):
        """Take screenshot. Saves to path and/or attaches to Allure."""
        if path:
            self.page.screenshot(path=path, full_page=full_page)
        else:
            screenshot = self.page.screenshot(full_page=full_page)
            allure.attach(
                screenshot, name=name,
                attachment_type=allure.attachment_type.PNG
            )

    def take_element_screenshot(self, selector, path):
        """Take screenshot of specific element."""
        self.page.locator(selector).first.screenshot(path=path)

    # ==================== JAVASCRIPT ====================

    def execute_script(self, script, *args):
        """Execute JavaScript."""
        return self.page.evaluate(script, *args)

    def execute_script_on_element(self, selector, script):
        """Execute JavaScript on element."""
        return self.page.locator(selector).first.evaluate(script)

    # ==================== ALERTS & DIALOGS ====================

    def accept_alert(self):
        """Accept alert/confirm dialog."""
        self.page.on("dialog", lambda dialog: dialog.accept())

    def dismiss_alert(self):
        """Dismiss alert/confirm dialog."""
        self.page.on("dialog", lambda dialog: dialog.dismiss())

    # ==================== FRAMES ====================

    def switch_to_frame(self, frame_selector):
        """Switch to iframe."""
        return self.page.frame_locator(frame_selector)

    # ==================== DRAG AND DROP ====================

    def drag_and_drop(self, source_selector, target_selector):
        """Drag and drop element."""
        self.page.drag_and_drop(source_selector, target_selector)

    # ==================== UTILITY ====================

    @allure.step("Get current URL")
    def get_current_url(self):
        """Get current URL."""
        return self.page.url

    @allure.step("Get page title")
    def get_page_title(self):
        """Get page title."""
        return self.page.title()

    # ==================== ADVANCED SELECTORS ====================

    def find_by_text(self, text, exact=False):
        """Find element by text."""
        if exact:
            return self.page.get_by_text(text, exact=True).first
        return self.page.get_by_text(text).first

    def find_by_role(self, role, name=None):
        """Find element by ARIA role."""
        if name:
            return self.page.get_by_role(role, name=name).first
        return self.page.get_by_role(role).first

    def find_by_label(self, label):
        """Find input by label."""
        return self.page.get_by_label(label).first

    def find_by_placeholder(self, placeholder):
        """Find input by placeholder."""
        return self.page.get_by_placeholder(placeholder).first

    def find_by_test_id(self, test_id):
        """Find element by test ID."""
        return self.page.get_by_test_id(test_id).first
