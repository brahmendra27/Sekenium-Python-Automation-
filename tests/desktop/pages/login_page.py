"""Login page object for the QE Sample POS application.

Since Tkinter widgets don't expose standard control types to UI Automation,
this page object uses keyboard-based interaction (type_keys) which works
reliably with Tkinter's focus/tab order:
    Tab order: Username → Password → Login button
"""

import time
import logging

import allure
from pywinauto import Application

logger = logging.getLogger(__name__)


class LoginPage:
    """Page object for the POS login screen.

    Uses keyboard-driven interaction since Tkinter controls
    appear as generic 'TkChild'/'Pane' to pywinauto.
    """

    WINDOW_TITLE_PATTERN = "QE Sample POS - Login"

    def __init__(self, app: Application):
        """Initialize with a pywinauto Application instance.

        Args:
            app: The pywinauto Application connected to the POS process.
        """
        self.app = app
        self._window = None

    @property
    def window(self):
        """Get the login window."""
        if self._window is None:
            self._window = self.app.window(title=self.WINDOW_TITLE_PATTERN)
        return self._window

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> "LoginPage":
        """Type username into the username field (first focused field).

        Args:
            username: The username to enter.

        Returns:
            Self for chaining.
        """
        self.window.set_focus()
        time.sleep(0.3)
        # Select all and type to replace any existing text
        self.window.type_keys("^a{DELETE}", with_spaces=True)
        self.window.type_keys(username, with_spaces=True)
        return self

    @allure.step("Enter password")
    def enter_password(self, password: str) -> "LoginPage":
        """Tab to password field and type the password.

        Args:
            password: The password to enter.

        Returns:
            Self for chaining.
        """
        # Tab from username to password field
        self.window.type_keys("{TAB}", with_spaces=True)
        time.sleep(0.1)
        self.window.type_keys("^a{DELETE}", with_spaces=True)
        self.window.type_keys(password, with_spaces=True)
        return self

    @allure.step("Click Login button")
    def click_login(self) -> "LoginPage":
        """Press Enter or Tab to Login button and activate it.

        Returns:
            Self for chaining.
        """
        # Press Enter (bound to login action in the app)
        self.window.type_keys("{ENTER}", with_spaces=True)
        time.sleep(0.5)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Perform complete login flow.

        Args:
            username: The username credential.
            password: The password credential.

        Returns:
            Self for chaining.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_window_title(self) -> str:
        """Get the current window title.

        Returns:
            The window title text.
        """
        try:
            return self.app.top_window().window_text()
        except Exception:
            return ""

    def is_login_screen(self) -> bool:
        """Check if we're still on the login screen.

        Returns:
            True if window title contains 'Login'.
        """
        return "Login" in self.get_window_title()

    def is_main_screen(self) -> bool:
        """Check if login succeeded and main screen is shown.

        Returns:
            True if window title no longer contains 'Login'.
        """
        title = self.get_window_title()
        return "QE Sample POS" in title and "Login" not in title
