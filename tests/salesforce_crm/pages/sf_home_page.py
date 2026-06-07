# tests/salesforce_crm/pages/sf_home_page.py

"""
Salesforce Lightning Home Page Object.

Handles navigation, app launcher, global search, and common Lightning actions.
"""

from framework.base_page import BasePagePlaywright


class SalesforceHomePage(BasePagePlaywright):
    """Page object for Salesforce Lightning home page."""

    # Navigation
    APP_LAUNCHER_BUTTON = ".slds-icon-waffle"
    APP_LAUNCHER_SEARCH = "input[placeholder='Search apps and items...']"
    GLOBAL_SEARCH_INPUT = "button[aria-label='Search']"
    GLOBAL_SEARCH_BOX = "input[placeholder='Search...']"
    NAV_BAR = "one-app-nav-bar"

    # Tabs
    HOME_TAB = "a[title='Home']"
    ACCOUNTS_TAB = "a[title='Accounts']"
    CONTACTS_TAB = "a[title='Contacts']"
    OPPORTUNITIES_TAB = "a[title='Opportunities']"
    LEADS_TAB = "a[title='Leads']"
    CASES_TAB = "a[title='Cases']"

    # Common elements
    NEW_BUTTON = "a[title='New'], button[name='New']"
    LIST_VIEW = ".slds-table"
    TOAST_MESSAGE = ".toastMessage"

    def navigate_to_app(self, app_name: str):
        """Open an app via the App Launcher.

        Args:
            app_name: Name of the app to open
        """
        self.click(self.APP_LAUNCHER_BUTTON)
        self.wait_for_element(self.APP_LAUNCHER_SEARCH)
        self.fill(self.APP_LAUNCHER_SEARCH, app_name)
        self.wait(1000)
        # Click the matching app result
        self.find_by_text(app_name, exact=False).click()
        self.wait_for_load_state("networkidle")

    def global_search(self, search_term: str):
        """Perform a global search.

        Args:
            search_term: Text to search for
        """
        self.click(self.GLOBAL_SEARCH_INPUT)
        self.wait_for_element(self.GLOBAL_SEARCH_BOX)
        self.fill(self.GLOBAL_SEARCH_BOX, search_term)
        self.press_key(self.GLOBAL_SEARCH_BOX, "Enter")
        self.wait_for_load_state("networkidle")

    def navigate_to_tab(self, tab_name: str):
        """Navigate to a Lightning tab by name.

        Args:
            tab_name: Tab name (Accounts, Contacts, Opportunities, etc.)
        """
        tab_selector = f"a[title='{tab_name}']"
        if self.is_visible(tab_selector, timeout=3000):
            self.click(tab_selector)
        else:
            # Tab might be in the overflow menu
            self.navigate_to_app(tab_name)
        self.wait_for_load_state("networkidle")

    def click_new_button(self):
        """Click the New button on a list view."""
        self.click(self.NEW_BUTTON)
        self.wait(1000)

    def get_toast_message(self) -> str:
        """Get the toast notification message."""
        if self.is_visible(self.TOAST_MESSAGE, timeout=5000):
            return self.get_text(self.TOAST_MESSAGE)
        return ""

    def is_on_home_page(self) -> bool:
        """Check if currently on the Lightning home page."""
        return self.is_visible(self.NAV_BAR, timeout=10000)

    def get_current_app_name(self) -> str:
        """Get the name of the currently active app."""
        app_name_selector = ".appName .slds-truncate"
        if self.is_visible(app_name_selector, timeout=3000):
            return self.get_text(app_name_selector)
        return ""
