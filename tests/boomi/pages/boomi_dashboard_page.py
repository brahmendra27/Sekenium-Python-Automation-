# tests/boomi/pages/boomi_dashboard_page.py

"""
Boomi AtomSphere Dashboard Page Object.

Handles Boomi platform UI navigation, process management, and execution monitoring.
"""

from framework.base_page import BasePagePlaywright


class BoomiDashboardPage(BasePagePlaywright):
    """Page object for Boomi AtomSphere platform UI."""

    # Login
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#loginButton, button[type='submit']"

    # Navigation
    BUILD_TAB = "a[title='Build'], [data-testid='build-tab']"
    DEPLOY_TAB = "a[title='Deploy'], [data-testid='deploy-tab']"
    MANAGE_TAB = "a[title='Manage'], [data-testid='manage-tab']"
    DASHBOARD_TAB = "a[title='Dashboard']"

    # Process Library
    PROCESS_SEARCH = "input[placeholder*='Search']"
    PROCESS_LIST = ".process-list, .component-list"
    PROCESS_ITEMS = ".process-item, .component-item"

    # Execution Monitor
    EXECUTION_TABLE = ".execution-table, table.executions"
    EXECUTION_ROWS = "table tbody tr"
    STATUS_FILTER = "select[name='status'], .status-filter"
    REFRESH_BUTTON = "button[title='Refresh'], .refresh-btn"

    # Atom Management
    ATOM_LIST = ".atom-list"
    ATOM_STATUS_ONLINE = ".status-online, .atom-online"
    ATOM_STATUS_OFFLINE = ".status-offline, .atom-offline"

    def login(self, username: str, password: str):
        """Login to Boomi AtomSphere.

        Args:
            username: Boomi username
            password: Boomi password
        """
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_load_state("networkidle")

    def navigate_to_build(self):
        """Navigate to Build tab."""
        self.click(self.BUILD_TAB)
        self.wait_for_load_state("networkidle")

    def navigate_to_deploy(self):
        """Navigate to Deploy tab."""
        self.click(self.DEPLOY_TAB)
        self.wait_for_load_state("networkidle")

    def navigate_to_manage(self):
        """Navigate to Manage tab."""
        self.click(self.MANAGE_TAB)
        self.wait_for_load_state("networkidle")

    def search_process(self, process_name: str):
        """Search for a process by name.

        Args:
            process_name: Process name to search
        """
        self.fill(self.PROCESS_SEARCH, process_name)
        self.press_key(self.PROCESS_SEARCH, "Enter")
        self.wait(2000)

    def get_process_count(self) -> int:
        """Get number of processes in the list."""
        return self.count_elements(self.PROCESS_ITEMS)

    def click_process_by_name(self, name: str):
        """Click a process by name.

        Args:
            name: Process name to click
        """
        self.find_by_text(name).click()
        self.wait_for_load_state("networkidle")

    def get_execution_count(self) -> int:
        """Get number of executions in the monitor table."""
        return self.count_elements(self.EXECUTION_ROWS)

    def refresh_executions(self):
        """Click refresh button on execution monitor."""
        self.click(self.REFRESH_BUTTON)
        self.wait(2000)

    def filter_executions_by_status(self, status: str):
        """Filter executions by status.

        Args:
            status: Status to filter (Complete, Error, etc.)
        """
        self.select_option(self.STATUS_FILTER, label=status)
        self.wait(1000)

    def is_logged_in(self) -> bool:
        """Check if logged into Boomi."""
        return self.is_visible(self.DASHBOARD_TAB, timeout=10000)

    def get_online_atom_count(self) -> int:
        """Get number of online atoms."""
        return self.count_elements(self.ATOM_STATUS_ONLINE)
