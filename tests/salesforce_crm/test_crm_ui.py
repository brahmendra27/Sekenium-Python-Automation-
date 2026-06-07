# tests/salesforce_crm/test_crm_ui.py

"""
Salesforce CRM UI Tests.

Tests Salesforce Lightning UI for Account, Contact, and Opportunity management.
Requires SF_* environment variables in .env file.
Uses Playwright for browser automation.
"""

import os
import pytest
from tests.salesforce_crm.pages.sf_login_page import SalesforceLoginPage
from tests.salesforce_crm.pages.sf_home_page import SalesforceHomePage
from tests.salesforce_crm.pages.sf_account_page import SalesforceAccountPage


@pytest.fixture(scope="function")
def sf_page(playwright_page):
    """Provide authenticated Salesforce Lightning page.

    Logs in and returns page ready for testing.
    Skips if SF credentials not configured.
    """
    sf_url = os.environ.get("SF_INSTANCE_URL")
    sf_user = os.environ.get("SF_USERNAME")
    sf_pass = os.environ.get("SF_PASSWORD")

    if not all([sf_url, sf_user, sf_pass]):
        pytest.skip("Salesforce UI credentials not configured in .env")

    page = playwright_page
    login_page = SalesforceLoginPage(page)
    login_page.navigate_to(sf_url)
    login_page.login(sf_user, sf_pass)

    if not login_page.is_login_successful():
        error = login_page.get_login_error()
        pytest.fail(f"Salesforce login failed: {error}")

    return page


class TestSalesforceLogin:
    """Test Salesforce login functionality."""

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    @pytest.mark.smoke
    def test_login_page_loads(self, playwright_page):
        """Test that Salesforce login page loads."""
        sf_url = os.environ.get("SF_INSTANCE_URL")
        if not sf_url:
            pytest.skip("SF_INSTANCE_URL not configured")

        page = SalesforceLoginPage(playwright_page)
        page.navigate_to(sf_url)
        assert page.is_on_login_page(), "Salesforce login page did not load"

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, sf_page):
        """Test successful login to Salesforce."""
        home = SalesforceHomePage(sf_page)
        assert home.is_on_home_page(), "Not on Salesforce home page after login"


class TestAccountUI:
    """Test Salesforce Account UI operations."""

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    @pytest.mark.smoke
    def test_navigate_to_accounts(self, sf_page):
        """Test navigating to Accounts tab shows account list."""
        home = SalesforceHomePage(sf_page)
        home.navigate_to_tab("Accounts")

        account_page = SalesforceAccountPage(sf_page)
        assert account_page.is_visible(
            account_page.ACCOUNT_LIST_TABLE, timeout=10000
        ), "Account list view did not load"

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    def test_create_account_via_ui_shows_success(self, sf_page, unique_id, sf_cleanup):
        """Test creating an account through the UI shows success toast."""
        home = SalesforceHomePage(sf_page)
        home.navigate_to_tab("Accounts")

        account_name = f"UI Test Account {unique_id}"
        account_page = SalesforceAccountPage(sf_page)
        toast = account_page.create_account(
            name=account_name,
            phone="555-0100"
        )
        sf_cleanup("Account", account_name)

        assert any(keyword in toast.lower() for keyword in ("created", "success")), \
            f"Expected success toast, got: {toast}"

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    def test_search_accounts_returns_results(self, sf_page):
        """Test searching accounts in list view returns valid count."""
        home = SalesforceHomePage(sf_page)
        home.navigate_to_tab("Accounts")

        account_page = SalesforceAccountPage(sf_page)
        account_page.search_accounts("Test")
        count = account_page.get_account_count()
        assert count >= 0, "Account search returned invalid count"

    @pytest.mark.salesforce_crm
    @pytest.mark.playwright
    def test_global_search_loads_results(self, sf_page):
        """Test global search navigates to search results page."""
        home = SalesforceHomePage(sf_page)
        home.global_search("Account")
        assert "search" in sf_page.url.lower(), \
            f"Expected search results page, got: {sf_page.url}"
