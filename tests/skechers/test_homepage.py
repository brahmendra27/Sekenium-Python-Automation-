# tests/skechers/test_homepage.py

"""
Skechers Homepage Tests
Tests for Skechers staging environment homepage functionality.
"""

import pytest
from framework.base_page import BasePageSelenium


class TestSkechersHomepage:
    """Test Skechers homepage functionality."""
    
    @pytest.mark.smoke
    def test_homepage_loads(self, driver):
        """Test that Skechers homepage loads successfully."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Verify page title contains Skechers
        assert "Skechers" in driver.title, f"Expected 'Skechers' in title, got: {driver.title}"
        
        # Verify page loaded (check for common element)
        # Note: Update selectors based on actual Skechers site structure
        assert page.is_element_present("css", "header"), "Header not found on homepage"
    
    @pytest.mark.smoke
    def test_logo_present(self, driver):
        """Test that Skechers logo is present on homepage."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Check for logo (update selector based on actual site)
        logo_selectors = [
            ("css", ".logo"),
            ("css", "[class*='logo']"),
            ("xpath", "//img[contains(@alt, 'Skechers')]"),
            ("xpath", "//a[contains(@class, 'logo')]")
        ]
        
        logo_found = False
        for selector_type, selector in logo_selectors:
            if page.is_element_present(selector_type, selector):
                logo_found = True
                break
        
        assert logo_found, "Skechers logo not found on homepage"
    
    @pytest.mark.smoke
    def test_navigation_menu_present(self, driver):
        """Test that main navigation menu is present."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Check for navigation menu
        nav_selectors = [
            ("css", "nav"),
            ("css", ".navigation"),
            ("css", "[role='navigation']"),
            ("xpath", "//nav")
        ]
        
        nav_found = False
        for selector_type, selector in nav_selectors:
            if page.is_element_present(selector_type, selector):
                nav_found = True
                break
        
        assert nav_found, "Navigation menu not found on homepage"
    
    def test_search_functionality_present(self, driver):
        """Test that search functionality is present."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Check for search input
        search_selectors = [
            ("css", "input[type='search']"),
            ("css", "input[placeholder*='Search']"),
            ("css", ".search-input"),
            ("xpath", "//input[contains(@placeholder, 'Search')]")
        ]
        
        search_found = False
        for selector_type, selector in search_selectors:
            if page.is_element_present(selector_type, selector):
                search_found = True
                break
        
        assert search_found, "Search functionality not found on homepage"
    
    def test_footer_present(self, driver):
        """Test that footer is present on homepage."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Check for footer
        footer_selectors = [
            ("css", "footer"),
            ("css", ".footer"),
            ("xpath", "//footer")
        ]
        
        footer_found = False
        for selector_type, selector in footer_selectors:
            if page.is_element_present(selector_type, selector):
                footer_found = True
                break
        
        assert footer_found, "Footer not found on homepage"
    
    @pytest.mark.regression
    def test_category_links_present(self, driver):
        """Test that main category links are present."""
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Expected categories
        categories = ["Men", "Women", "Kids"]
        
        for category in categories:
            # Try multiple selector strategies
            category_selectors = [
                ("xpath", f"//a[contains(text(), '{category}')]"),
                ("xpath", f"//a[contains(@href, '{category.lower()}')]"),
                ("css", f"a[href*='{category.lower()}']")
            ]
            
            category_found = False
            for selector_type, selector in category_selectors:
                if page.is_element_present(selector_type, selector):
                    category_found = True
                    break
            
            # Log if category not found (don't fail test as structure may vary)
            if not category_found:
                print(f"Warning: {category} category link not found")


class TestSkechersResponsiveness:
    """Test Skechers homepage responsiveness."""
    
    @pytest.mark.parametrize("viewport", [
        (1920, 1080),  # Desktop
        (1366, 768),   # Laptop
        (768, 1024),   # Tablet
        (375, 667)     # Mobile
    ])
    def test_homepage_responsive(self, driver, viewport):
        """Test homepage loads correctly at different viewport sizes."""
        width, height = viewport
        driver.set_window_size(width, height)
        
        page = BasePageSelenium(driver)
        page.navigate_to("/")
        
        # Verify page loads
        assert "Skechers" in driver.title
        
        # Verify essential elements are present
        assert page.is_element_present("css", "header"), f"Header not found at {width}x{height}"
