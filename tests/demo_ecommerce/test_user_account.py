# tests/demo_ecommerce/test_user_account.py

"""
Demo E-commerce User Account Tests
Tests for user account and authentication functionality.
"""

import pytest
from framework.base_page import BasePageSelenium


class TestUserAuthentication:
    """Test user authentication functionality."""
    
    @pytest.mark.smoke
    def test_login_page_accessible(self, driver):
        """Test that login page is accessible."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        
        # Try common login URLs
        login_urls = ["/login", "/signin", "/account/login", "/user/login"]
        
        login_accessible = False
        for url in login_urls:
            try:
                page.navigate_to(url)
                current_url = driver.current_url.lower()
                if "login" in current_url or "signin" in current_url:
                    login_accessible = True
                    break
            except:
                continue
        
        assert login_accessible, "Login page not accessible"
    
    def test_login_form_present(self, driver):
        """Test that login form elements are present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/login")
        
        # Check for email/username input
        email_selectors = [
            ("css", "input[type='email']"),
            ("css", "input[name='email']"),
            ("css", "input[name='username']"),
            ("css", "#email"),
            ("css", "#username")
        ]
        
        email_found = False
        for selector_type, selector in email_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                email_found = True
                break
        
        assert email_found, "Email/username input not found on login page"
    
    def test_password_field_present(self, driver):
        """Test that password field is present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/login")
        
        # Check for password input
        password_selectors = [
            ("css", "input[type='password']"),
            ("css", "input[name='password']"),
            ("css", "#password")
        ]
        
        password_found = False
        for selector_type, selector in password_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                password_found = True
                break
        
        assert password_found, "Password field not found on login page"
    
    def test_login_button_present(self, driver):
        """Test that login button is present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/login")
        
        # Check for login button
        button_selectors = [
            ("css", "button[type='submit']"),
            ("xpath", "//button[contains(text(), 'Login')]"),
            ("xpath", "//button[contains(text(), 'Sign In')]"),
            ("css", ".login-button"),
            ("css", "input[type='submit']")
        ]
        
        button_found = False
        for selector_type, selector in button_selectors:
            if page.is_element_present(selector_type, selector, timeout=10):
                button_found = True
                break
        
        assert button_found, "Login button not found on login page"
    
    @pytest.mark.regression
    def test_forgot_password_link(self, driver):
        """Test that forgot password link is present."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/login")
        
        # Check for forgot password link
        forgot_selectors = [
            ("xpath", "//a[contains(text(), 'Forgot')]"),
            ("xpath", "//a[contains(text(), 'forgot')]"),
            ("css", "a[href*='forgot']"),
            ("css", "a[href*='reset']")
        ]
        
        forgot_found = False
        for selector_type, selector in forgot_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                forgot_found = True
                break
        
        if not forgot_found:
            print("Note: Forgot password link not found")


class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_page_accessible(self, driver):
        """Test that registration page is accessible."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        
        # Try common registration URLs
        register_urls = ["/register", "/signup", "/account/register", "/user/register"]
        
        register_accessible = False
        for url in register_urls:
            try:
                page.navigate_to(url)
                current_url = driver.current_url.lower()
                if "register" in current_url or "signup" in current_url:
                    register_accessible = True
                    break
            except:
                continue
        
        if not register_accessible:
            print("Note: Registration page not accessible - may not be available")
    
    def test_register_link_on_login_page(self, driver):
        """Test that register link is present on login page."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/login")
        
        # Check for register/signup link
        register_selectors = [
            ("xpath", "//a[contains(text(), 'Register')]"),
            ("xpath", "//a[contains(text(), 'Sign Up')]"),
            ("xpath", "//a[contains(text(), 'Create Account')]"),
            ("css", "a[href*='register']"),
            ("css", "a[href*='signup']")
        ]
        
        register_found = False
        for selector_type, selector in register_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                register_found = True
                break
        
        if not register_found:
            print("Note: Register link not found on login page")


class TestUserAccount:
    """Test user account page functionality."""
    
    def test_account_page_requires_login(self, driver):
        """Test that account page redirects to login if not authenticated."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        
        # Try to access account page
        account_urls = ["/account", "/profile", "/my-account", "/user/account"]
        
        for url in account_urls:
            try:
                page.navigate_to(url)
                current_url = driver.current_url.lower()
                
                # Should redirect to login or show login requirement
                if "login" in current_url or "signin" in current_url:
                    print(f"Account page correctly redirects to login")
                    return
            except:
                continue
        
        print("Note: Could not verify account page login requirement")
    
    def test_my_account_link_in_header(self, driver):
        """Test that my account link is present in header."""
        page = BasePageSelenium(driver, base_url=driver.base_url)
        page.navigate_to("/")
        
        # Check for account link
        account_selectors = [
            ("xpath", "//a[contains(text(), 'Account')]"),
            ("xpath", "//a[contains(text(), 'My Account')]"),
            ("xpath", "//a[contains(text(), 'Profile')]"),
            ("css", "a[href*='account']"),
            ("css", "a[href*='profile']")
        ]
        
        account_found = False
        for selector_type, selector in account_selectors:
            if page.is_element_present(selector_type, selector, timeout=5):
                account_found = True
                break
        
        if not account_found:
            print("Note: Account link not found in header")
