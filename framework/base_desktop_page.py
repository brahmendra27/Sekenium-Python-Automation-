"""Base page object for desktop application testing.

Provides common actions for interacting with desktop application controls:
find, click, type, wait, and window management. Analogous to BasePagePlaywright
for web testing but targets native Windows desktop controls via pywinauto.
"""

import logging

import allure
from pywinauto import Application

logger = logging.getLogger(__name__)


class BaseDesktopPage:
    """Base class for desktop application page objects.

    Provides common actions: find controls, click, type, wait,
    and window management. Subclasses override WINDOW_TITLE to
    target a specific window.
    """

    WINDOW_TITLE: str = ""  # Override in subclasses

    def __init__(self, app: Application):
        """Initialize with a pywinauto Application instance.

        Args:
            app: The pywinauto Application connected to the target process.
        """
        self.app = app
        self._window = None

    @property
    def window(self):
        """Get the main window for this page (lazy-loaded)."""
        if self._window is None:
            if self.WINDOW_TITLE:
                self._window = self.app.window(title=self.WINDOW_TITLE)
            else:
                self._window = self.app.top_window()
        return self._window

    def set_window(self, **kwargs):
        """Switch to a different window by specification.

        Args:
            **kwargs: Window specification (title, title_re, class_name, etc.)

        Returns:
            Self for chaining.
        """
        self._window = self.app.window(**kwargs)
        return self

    @allure.step("Click: {title}")
    def click_button(self, title: str):
        """Click a button by its title/text.

        Args:
            title: The button text (e.g., 'Login', 'Add to Cart').

        Returns:
            Self for chaining.
        """
        logger.info(f"Clicking button: {title}")
        self.window[title].click()
        return self

    @allure.step("Type text into: {control_title}")
    def type_text(self, control_title: str, text: str):
        """Type text into an editable control identified by title.

        Args:
            control_title: The control's title or best_match name.
            text: The text to type.

        Returns:
            Self for chaining.
        """
        logger.info(f"Typing into '{control_title}': {text[:20]}...")
        ctrl = self.window[control_title]
        ctrl.set_edit_text(text)
        return self

    @allure.step("Set text in edit control")
    def set_edit_text(self, control, text: str):
        """Set text in a specific control reference.

        Args:
            control: A pywinauto control wrapper.
            text: The text to set.

        Returns:
            Self for chaining.
        """
        control.set_edit_text(text)
        return self

    @allure.step("Get text from: {control_title}")
    def get_text(self, control_title: str) -> str:
        """Get text content from a control.

        Args:
            control_title: The control's title or best_match name.

        Returns:
            The control's text content.
        """
        return self.window[control_title].window_text()

    def get_control(self, **kwargs):
        """Find a child control by properties.

        Args:
            **kwargs: Control properties (title, control_type, class_name, etc.)

        Returns:
            The matching control wrapper.
        """
        return self.window.child_window(**kwargs)

    @allure.step("Wait for window: {timeout}s")
    def wait_for_window(self, timeout: int = 10):
        """Wait until the page's window is visible and ready.

        Args:
            timeout: Max seconds to wait.

        Returns:
            Self for chaining.
        """
        self.window.wait("visible", timeout=timeout)
        return self

    @allure.step("Wait for control ready: {timeout}s")
    def wait_for_control(self, timeout: int = 10, **kwargs):
        """Wait for a specific control to be visible and enabled.

        Args:
            timeout: Max seconds to wait.
            **kwargs: Control properties to find.

        Returns:
            The control wrapper once ready.
        """
        ctrl = self.window.child_window(**kwargs)
        ctrl.wait("visible", timeout=timeout)
        return ctrl

    def exists(self) -> bool:
        """Check if the window exists and is visible."""
        try:
            return self.window.exists() and self.window.is_visible()
        except Exception:
            return False

    @allure.step("Select menu: {path}")
    def select_menu(self, path: str):
        """Select a menu item by path.

        Args:
            path: Menu path separated by '->' (e.g., 'File->Save As').

        Returns:
            Self for chaining.
        """
        logger.info(f"Selecting menu: {path}")
        self.window.menu_select(path)
        return self

    @allure.step("Select item in treeview at row {index}")
    def select_treeview_item(self, treeview_ctrl, index: int):
        """Select an item in a Treeview/ListView by index.

        Args:
            treeview_ctrl: The treeview control wrapper.
            index: Zero-based index of the item to select.

        Returns:
            Self for chaining.
        """
        item = treeview_ctrl.get_item(index)
        item.select()
        return self

    def capture_screenshot(self, filename: str = "desktop_screenshot.png"):
        """Capture a screenshot of the window and attach to Allure.

        Args:
            filename: Output filename for the screenshot.

        Returns:
            Self for chaining.
        """
        try:
            img = self.window.capture_as_image()
            img.save(filename)
            allure.attach.file(filename, attachment_type=allure.attachment_type.PNG)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.warning(f"Failed to capture screenshot: {e}")
        return self

    def print_control_tree(self):
        """Print the control tree for debugging/inspection.

        Useful during test development to discover control identifiers.
        """
        self.window.print_control_identifiers()

    @property
    def title(self) -> str:
        """Get the current window title."""
        return self.window.window_text()
