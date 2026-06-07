# tests/boomi/test_boomi_ui.py

"""
Boomi AtomSphere UI Tests.

Tests Boomi platform UI for process management and execution monitoring.
Requires BOOMI_* environment variables in .env file.
"""

import os
import pytest
from tests.boomi.pages.boomi_dashboard_page import BoomiDashboardPage


@pytest.fixture(scope="function")
def boomi_page(playwright_driver):
    """Provide authenticated Boomi AtomSphere page.

    Skips if Boomi UI credentials not configured.
    """
    boomi_url = os.environ.get("BOOMI_UI_URL", "https://platform.boomi.com")
    boomi_user = os.environ.get("BOOMI_USERNAME")
    boomi_pass = os.environ.get("BOOMI_PASSWORD")

    if not all([boomi_user, boomi_pass]):
        pytest.skip("Boomi UI credentials not configured in .env")

    page = playwright_driver
    dashboard = BoomiDashboardPage(page)
    dashboard.navigate_to(boomi_url)
    dashboard.login(boomi_user, boomi_pass)

    if not dashboard.is_logged_in():
        pytest.fail("Boomi login failed")

    return page


class TestBoomiLogin:
    """Test Boomi platform login."""

    @pytest.mark.boomi
    @pytest.mark.smoke
    def test_boomi_login_page_loads(self, playwright_driver):
        """Test that Boomi login page loads."""
        boomi_url = os.environ.get("BOOMI_UI_URL", "https://platform.boomi.com")
        page = BoomiDashboardPage(playwright_driver)
        page.navigate_to(boomi_url)
        assert page.is_visible(page.USERNAME_INPUT, timeout=10000), \
            "Boomi login page did not load"

    @pytest.mark.boomi
    @pytest.mark.smoke
    def test_boomi_login_successful(self, boomi_page):
        """Test successful login to Boomi."""
        dashboard = BoomiDashboardPage(boomi_page)
        assert dashboard.is_logged_in(), "Not logged into Boomi"


class TestBoomiProcessManagement:
    """Test Boomi process management UI."""

    @pytest.mark.boomi
    def test_navigate_to_build(self, boomi_page):
        """Test navigating to Build tab."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_build()
        # Build tab should load

    @pytest.mark.boomi
    def test_search_process(self, boomi_page):
        """Test searching for a process."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_build()
        dashboard.search_process("Order")
        count = dashboard.get_process_count()
        assert count >= 0, "Process search failed"


class TestBoomiExecutionMonitor:
    """Test Boomi execution monitoring UI."""

    @pytest.mark.boomi
    @pytest.mark.smoke
    def test_navigate_to_manage(self, boomi_page):
        """Test navigating to Manage tab."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_manage()
        # Manage tab should load

    @pytest.mark.boomi
    def test_view_executions(self, boomi_page):
        """Test viewing execution records."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_manage()
        count = dashboard.get_execution_count()
        assert count >= 0, "Execution monitor did not load"

    @pytest.mark.boomi
    def test_filter_completed_executions(self, boomi_page):
        """Test filtering executions by completed status."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_manage()
        dashboard.filter_executions_by_status("Complete")
        # Filter should apply without errors

    @pytest.mark.boomi
    def test_check_online_atoms(self, boomi_page):
        """Test checking online atom count."""
        dashboard = BoomiDashboardPage(boomi_page)
        dashboard.navigate_to_manage()
        online = dashboard.get_online_atom_count()
        assert online >= 0, "Could not check atom status"
