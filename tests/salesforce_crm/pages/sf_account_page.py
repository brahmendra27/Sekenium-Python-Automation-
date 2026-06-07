# tests/salesforce_crm/pages/sf_account_page.py

"""
Salesforce Account Page Object.

Handles Account list view, detail view, and record creation/editing.
"""

from framework.base_page import BasePagePlaywright


class SalesforceAccountPage(BasePagePlaywright):
    """Page object for Salesforce Account pages."""

    # List View
    ACCOUNT_LIST_TABLE = ".slds-table"
    ACCOUNT_LIST_ROWS = "table tbody tr"
    NEW_ACCOUNT_BUTTON = "a[title='New'], button[name='New']"
    SEARCH_LIST = "input[placeholder='Search this list...']"

    # Record Form
    ACCOUNT_NAME_INPUT = "input[name='Name']"
    PHONE_INPUT = "input[name='Phone']"
    WEBSITE_INPUT = "input[name='Website']"
    INDUSTRY_DROPDOWN = "button[aria-label='Industry']"
    TYPE_DROPDOWN = "button[aria-label='Type']"
    SAVE_BUTTON = "button[name='SaveEdit']"
    CANCEL_BUTTON = "button[name='CancelEdit']"

    # Detail View
    RECORD_HEADER = "lightning-formatted-name"
    DETAIL_TAB = "a[data-label='Details']"
    RELATED_TAB = "a[data-label='Related']"
    EDIT_BUTTON = "button[name='Edit']"
    DELETE_BUTTON = "button[name='Delete']"

    # Toast
    TOAST_MESSAGE = ".toastMessage"

    def click_new_account(self):
        """Click New Account button."""
        self.click(self.NEW_ACCOUNT_BUTTON)
        self.wait_for_element(self.ACCOUNT_NAME_INPUT)

    def fill_account_form(self, name: str, phone: str = "",
                          website: str = ""):
        """Fill the account creation/edit form.

        Args:
            name: Account name (required)
            phone: Phone number (optional)
            website: Website URL (optional)
        """
        self.fill(self.ACCOUNT_NAME_INPUT, name)
        if phone:
            self.fill(self.PHONE_INPUT, phone)
        if website:
            self.fill(self.WEBSITE_INPUT, website)

    def save_account(self):
        """Click Save button and wait for toast."""
        self.click(self.SAVE_BUTTON)
        self.wait_for_load_state("networkidle")

    def create_account(self, name: str, phone: str = "",
                       website: str = "") -> str:
        """Create a new account end-to-end.

        Args:
            name: Account name
            phone: Phone number
            website: Website URL

        Returns:
            Toast message text
        """
        self.click_new_account()
        self.fill_account_form(name, phone, website)
        self.save_account()
        return self.get_toast_message()

    def get_toast_message(self) -> str:
        """Get toast notification message."""
        if self.is_visible(self.TOAST_MESSAGE, timeout=5000):
            return self.get_text(self.TOAST_MESSAGE)
        return ""

    def search_accounts(self, search_term: str):
        """Search accounts in list view.

        Args:
            search_term: Text to search for
        """
        self.fill(self.SEARCH_LIST, search_term)
        self.press_key(self.SEARCH_LIST, "Enter")
        self.wait(2000)

    def get_account_count(self) -> int:
        """Get number of accounts in list view."""
        return self.count_elements(self.ACCOUNT_LIST_ROWS)

    def click_account_by_name(self, name: str):
        """Click an account link by name in list view.

        Args:
            name: Account name to click
        """
        self.find_by_text(name).click()
        self.wait_for_load_state("networkidle")

    def is_on_account_detail(self) -> bool:
        """Check if on account detail page."""
        return self.is_visible(self.RECORD_HEADER, timeout=5000)

    def click_edit(self):
        """Click Edit button on detail page."""
        self.click(self.EDIT_BUTTON)
        self.wait_for_element(self.ACCOUNT_NAME_INPUT)

    def click_delete(self):
        """Click Delete button on detail page."""
        self.click(self.DELETE_BUTTON)
        # Confirm deletion dialog
        self.find_by_text("Delete", exact=True).click()
        self.wait_for_load_state("networkidle")

    def get_account_name(self) -> str:
        """Get account name from detail page header."""
        return self.get_text(self.RECORD_HEADER)

    def navigate_to_details_tab(self):
        """Click the Details tab."""
        self.click(self.DETAIL_TAB)

    def navigate_to_related_tab(self):
        """Click the Related tab."""
        self.click(self.RELATED_TAB)
