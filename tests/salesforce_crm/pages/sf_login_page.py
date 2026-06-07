# tests/salesforce_crm/pages/sf_login_page.py

"""
Salesforce Login Page Object.

Handles standard Salesforce login and Lightning redirect.
"""

from framework.base_page import BasePagePlaywright


class SalesforceLoginPage(BasePagePlaywright):
    """Page object for Salesforce login screen."""

    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#Login"
    LOGIN_ERROR = "#error"
    LIGHTNING_REDIRECT = ".oneHeader"

    def login(self, username: str, password: str):
        """Login to Salesforce with username and password.

        Args:
            username: Salesforce username
            password: Salesforce password
        """
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_load_state("networkidle")

    def is_login_successful(self) -> bool:
        """Check if login was successful by looking for Lightning header."""
        return self.is_visible(self.LIGHTNING_REDIRECT, timeout=15000)

    def get_login_error(self) -> str:
        """Get login error message if present."""
        if self.is_visible(self.LOGIN_ERROR, timeout=3000):
            return self.get_text(self.LOGIN_ERROR)
        return ""

    def is_on_login_page(self) -> bool:
        """Check if currently on the login page."""
        return self.is_visible(self.USERNAME_INPUT, timeout=5000)
