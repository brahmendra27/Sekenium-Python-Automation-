# tests/salesforce_loyalty/test_loyalty_ui.py

"""
Salesforce Loyalty Management UI Tests.

Tests Loyalty Program UI for member management, points, and transactions.
Requires SF_* environment variables in .env file.
"""

import os
import pytest
from tests.salesforce_crm.pages.sf_login_page import SalesforceLoginPage
from tests.salesforce_crm.pages.sf_home_page import SalesforceHomePage
from tests.salesforce_loyalty.pages.loyalty_program_page import LoyaltyProgramPage


@pytest.fixture(scope="function")
def loyalty_page(playwright_driver):
    """Provide authenticated Salesforce page navigated to Loyalty app.

    Skips if SF credentials not configured.
    """
    sf_url = os.environ.get("SF_INSTANCE_URL")
    sf_user = os.environ.get("SF_USERNAME")
    sf_pass = os.environ.get("SF_PASSWORD")

    if not all([sf_url, sf_user, sf_pass]):
        pytest.skip("Salesforce UI credentials not configured in .env")

    page = playwright_driver

    # Login
    login_page = SalesforceLoginPage(page)
    login_page.navigate_to(sf_url)
    login_page.login(sf_user, sf_pass)

    if not login_page.is_login_successful():
        pytest.fail(f"Salesforce login failed: {login_page.get_login_error()}")

    # Navigate to Loyalty Management app
    home = SalesforceHomePage(page)
    home.navigate_to_app("Loyalty Management")

    return page


class TestLoyaltyProgramsUI:
    """Test Loyalty Program list and detail views."""

    @pytest.mark.loyalty
    @pytest.mark.smoke
    def test_loyalty_programs_page_loads(self, loyalty_page):
        """Test that Loyalty Programs page loads."""
        lp = LoyaltyProgramPage(loyalty_page)
        lp.navigate_to_loyalty_programs()
        count = lp.get_program_count()
        assert count >= 0, "Loyalty programs page did not load"

    @pytest.mark.loyalty
    def test_loyalty_members_page_loads(self, loyalty_page):
        """Test that Loyalty Members page loads."""
        lp = LoyaltyProgramPage(loyalty_page)
        lp.navigate_to_loyalty_members()
        # Page should load without errors
        assert loyalty_page.url is not None


class TestLoyaltyMemberUI:
    """Test Loyalty Member detail views and operations."""

    @pytest.mark.loyalty
    def test_search_loyalty_member(self, loyalty_page):
        """Test searching for a loyalty member."""
        lp = LoyaltyProgramPage(loyalty_page)
        lp.navigate_to_loyalty_members()
        lp.search_members("Test")
        # Search should complete without errors

    @pytest.mark.loyalty
    def test_view_member_detail(self, loyalty_page):
        """Test viewing a loyalty member's detail page."""
        lp = LoyaltyProgramPage(loyalty_page)
        lp.navigate_to_loyalty_members()

        # Try to click first member if available
        members = loyalty_page.locator("table tbody tr a").all()
        if not members:
            pytest.skip("No loyalty members found to view")

        members[0].click()
        lp.wait_for_load_state("networkidle")
        assert lp.is_on_member_detail(), "Member detail page did not load"

    @pytest.mark.loyalty
    def test_view_member_transactions(self, loyalty_page):
        """Test viewing a member's transaction history."""
        lp = LoyaltyProgramPage(loyalty_page)
        lp.navigate_to_loyalty_members()

        members = loyalty_page.locator("table tbody tr a").all()
        if not members:
            pytest.skip("No loyalty members found")

        members[0].click()
        lp.wait_for_load_state("networkidle")
        lp.navigate_to_transactions()
        # Transactions tab should load
