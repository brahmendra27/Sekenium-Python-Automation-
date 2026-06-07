"""Tests for the POS application login functionality.

Validates login behavior: successful login with valid credentials,
rejection with invalid credentials, and empty field handling.

Note: These tests use keyboard-based interaction (type_keys) because
Tkinter doesn't expose standard control types to Windows UI Automation.
The window title change is the primary assertion mechanism.
"""

import time

import pytest

from tests.desktop.pages.login_page import LoginPage


@pytest.mark.desktop
class TestPOSLogin:
    """Verify login behavior of the QE Sample POS application."""

    @pytest.mark.smoke
    def test_valid_login_navigates_to_main_screen(self, pos_app):
        """Verify that valid credentials change the window title to show username."""
        # Arrange
        login_page = LoginPage(pos_app.app)
        time.sleep(0.5)

        # Act
        login_page.login("admin", "admin123")

        # Assert
        assert login_page.is_main_screen(), (
            f"Expected main screen but got title: '{login_page.get_window_title()}'"
        )

    def test_invalid_password_stays_on_login(self, pos_app):
        """Verify that invalid password keeps user on the login screen."""
        # Arrange
        login_page = LoginPage(pos_app.app)
        time.sleep(0.5)

        # Act
        login_page.login("admin", "wrongpass")

        # Assert
        assert login_page.is_login_screen(), (
            f"Expected login screen but got title: '{login_page.get_window_title()}'"
        )

    def test_empty_fields_stays_on_login(self, pos_app):
        """Verify that submitting with empty fields stays on login screen."""
        # Arrange
        login_page = LoginPage(pos_app.app)
        time.sleep(0.5)

        # Act
        login_page.click_login()

        # Assert
        assert login_page.is_login_screen(), (
            f"Expected login screen but got title: '{login_page.get_window_title()}'"
        )

    def test_invalid_username_stays_on_login(self, pos_app):
        """Verify that a non-existent username keeps user on login screen."""
        # Arrange
        login_page = LoginPage(pos_app.app)
        time.sleep(0.5)

        # Act
        login_page.login("nonexistent_user", "somepass")

        # Assert
        assert login_page.is_login_screen(), (
            f"Expected login screen but got title: '{login_page.get_window_title()}'"
        )

    def test_successful_login_shows_cashier_name_in_title(self, pos_app):
        """Verify the window title contains the logged-in username."""
        # Arrange
        login_page = LoginPage(pos_app.app)
        time.sleep(0.5)

        # Act
        login_page.login("cashier", "cash456")

        # Assert
        title = login_page.get_window_title()
        assert "cashier" in title, f"Expected 'cashier' in title but got: '{title}'"
