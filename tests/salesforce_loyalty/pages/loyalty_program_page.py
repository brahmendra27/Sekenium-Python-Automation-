# tests/salesforce_loyalty/pages/loyalty_program_page.py

"""
Salesforce Loyalty Program Page Object.

Handles Loyalty Program views, member management, and point operations in the UI.
"""

from framework.base_page import BasePagePlaywright


class LoyaltyProgramPage(BasePagePlaywright):
    """Page object for Salesforce Loyalty Management UI."""

    # Navigation
    LOYALTY_PROGRAMS_TAB = "a[title='Loyalty Programs']"
    LOYALTY_MEMBERS_TAB = "a[title='Loyalty Program Members']"

    # Program List
    PROGRAM_LIST_TABLE = ".slds-table"
    PROGRAM_LIST_ROWS = "table tbody tr"

    # Member List
    MEMBER_LIST_TABLE = ".slds-table"
    MEMBER_SEARCH = "input[placeholder='Search this list...']"
    NEW_MEMBER_BUTTON = "a[title='New'], button[name='New']"

    # Member Detail
    MEMBER_NAME = "lightning-formatted-name"
    MEMBER_STATUS = "lightning-formatted-text[data-field='MemberStatus']"
    POINTS_BALANCE = "lightning-formatted-number"
    MEMBERSHIP_NUMBER = "[data-field='MembershipNumber']"
    TRANSACTIONS_TAB = "a[data-label='Transaction Journals']"
    TIERS_TAB = "a[data-label='Loyalty Member Tiers']"

    # Enrollment Form
    CONTACT_LOOKUP = "input[placeholder='Search Contacts...']"
    PROGRAM_LOOKUP = "input[placeholder='Search Loyalty Programs...']"
    ENROLLMENT_DATE = "input[name='EnrollmentDate']"
    SAVE_BUTTON = "button[name='SaveEdit']"

    # Toast
    TOAST_MESSAGE = ".toastMessage"

    def navigate_to_loyalty_programs(self):
        """Navigate to Loyalty Programs tab."""
        self.click(self.LOYALTY_PROGRAMS_TAB)
        self.wait_for_load_state("networkidle")

    def navigate_to_loyalty_members(self):
        """Navigate to Loyalty Program Members tab."""
        self.click(self.LOYALTY_MEMBERS_TAB)
        self.wait_for_load_state("networkidle")

    def search_members(self, search_term: str):
        """Search loyalty members in list view.

        Args:
            search_term: Member name or number to search
        """
        self.fill(self.MEMBER_SEARCH, search_term)
        self.press_key(self.MEMBER_SEARCH, "Enter")
        self.wait(2000)

    def click_member_by_name(self, name: str):
        """Click a member link by name.

        Args:
            name: Member name to click
        """
        self.find_by_text(name).click()
        self.wait_for_load_state("networkidle")

    def get_member_status(self) -> str:
        """Get member status from detail page."""
        if self.is_visible(self.MEMBER_STATUS, timeout=5000):
            return self.get_text(self.MEMBER_STATUS)
        return ""

    def get_points_balance(self) -> str:
        """Get points balance from detail page."""
        if self.is_visible(self.POINTS_BALANCE, timeout=5000):
            return self.get_text(self.POINTS_BALANCE)
        return ""

    def navigate_to_transactions(self):
        """Click the Transaction Journals related tab."""
        self.click(self.TRANSACTIONS_TAB)
        self.wait(1000)

    def navigate_to_tiers(self):
        """Click the Loyalty Member Tiers related tab."""
        self.click(self.TIERS_TAB)
        self.wait(1000)

    def click_new_member(self):
        """Click New Member button."""
        self.click(self.NEW_MEMBER_BUTTON)
        self.wait(1000)

    def get_toast_message(self) -> str:
        """Get toast notification message."""
        if self.is_visible(self.TOAST_MESSAGE, timeout=5000):
            return self.get_text(self.TOAST_MESSAGE)
        return ""

    def get_program_count(self) -> int:
        """Get number of programs in list view."""
        return self.count_elements(self.PROGRAM_LIST_ROWS)

    def is_on_member_detail(self) -> bool:
        """Check if on member detail page."""
        return self.is_visible(self.MEMBER_NAME, timeout=5000)
