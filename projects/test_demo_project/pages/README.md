# Page Objects Directory

Place your Page Object classes here.

## Example Page Object (Selenium)

```python
"""
Home Page Object for My Project.
"""

import allure
from selenium.webdriver.common.by import By
from framework.base_page import BasePageSelenium


class HomePage(BasePageSelenium):
    """Page Object for homepage."""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, ".logo")
    SEARCH_BOX = (By.ID, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-btn")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com"
    
    @allure.step("Open homepage")
    def open(self):
        """Navigate to homepage."""
        self.navigate_to(self.url)
        return self
    
    @allure.step("Search for: {query}")
    def search(self, query):
        """Perform search."""
        self.type(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)
        return self
```

## Example Page Object (Playwright)

```python
"""
Home Page Object for My Project (Playwright).
"""

import allure
from framework.base_page import BasePagePlaywright


class HomePage(BasePagePlaywright):
    """Page Object for homepage."""
    
    # Selectors
    LOGO = ".logo"
    SEARCH_BOX = "#search"
    SEARCH_BUTTON = ".search-btn"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://example.com"
    
    @allure.step("Open homepage")
    def open(self):
        """Navigate to homepage."""
        self.navigate_to(self.url)
        return self
    
    @allure.step("Search for: {query}")
    def search(self, query):
        """Perform search."""
        self.type(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)
        return self
```

## Best Practices

1. **One page object per page** - Each page gets its own class
2. **Define locators at the top** - All locators as class constants
3. **Use descriptive names** - Clear method and locator names
4. **Return page objects** - Methods return self or next page object
5. **Add Allure steps** - Use @allure.step decorator for reporting
6. **Inherit from base** - Use BasePageSelenium or BasePagePlaywright
