"""Main POS page object for the QE Sample POS application."""

import allure

from framework.base_desktop_page import BaseDesktopPage


class MainPOSPage(BaseDesktopPage):
    """Page object for the main POS screen (product catalog + cart).

    Provides methods for searching products, adding to cart,
    managing the cart, and initiating checkout.
    """

    def __init__(self, app, username: str = "admin"):
        """Initialize with the expected window title based on logged-in user.

        Args:
            app: The pywinauto Application instance.
            username: The logged-in username (used in window title).
        """
        super().__init__(app)
        self.WINDOW_TITLE = f"QE Sample POS - {username}"

    @allure.step("Search for product: {query}")
    def search_product(self, query: str) -> "MainPOSPage":
        """Enter text in the product search field.

        Args:
            query: The search text to filter products.

        Returns:
            Self for chaining.
        """
        entries = [c for c in self.window.descendants() if "Edit" in c.friendly_class_name()]
        if entries:
            entries[0].set_edit_text(query)
        return self

    @allure.step("Select product at row {index}")
    def select_product_by_index(self, index: int) -> "MainPOSPage":
        """Select a product in the catalog by row index.

        Args:
            index: Zero-based row index in the product treeview.

        Returns:
            Self for chaining.
        """
        trees = [c for c in self.window.descendants()
                 if "TreeView" in c.friendly_class_name() or "SysTreeView" in c.class_name()]
        if trees:
            tree = trees[0]
            items = tree.items()
            if 0 <= index < len(items):
                items[index].select()
        return self

    @allure.step("Set quantity: {qty}")
    def set_quantity(self, qty: int) -> "MainPOSPage":
        """Set the quantity spinbox value.

        Args:
            qty: The quantity to set.

        Returns:
            Self for chaining.
        """
        edits = [c for c in self.window.descendants() if "Edit" in c.friendly_class_name()]
        if len(edits) >= 2:
            edits[-1].set_edit_text(str(qty))
        return self

    @allure.step("Click Add to Cart")
    def click_add_to_cart(self) -> "MainPOSPage":
        """Click the 'Add to Cart' button.

        Returns:
            Self for chaining.
        """
        buttons = [c for c in self.window.descendants() if "Button" in c.friendly_class_name()]
        for btn in buttons:
            if "Add to Cart" in btn.window_text():
                btn.click()
                break
        return self

    @allure.step("Click Remove Selected")
    def click_remove_selected(self) -> "MainPOSPage":
        """Click 'Remove Selected' button to remove cart item.

        Returns:
            Self for chaining.
        """
        buttons = [c for c in self.window.descendants() if "Button" in c.friendly_class_name()]
        for btn in buttons:
            if "Remove" in btn.window_text():
                btn.click()
                break
        return self

    @allure.step("Click Clear Cart")
    def click_clear_cart(self) -> "MainPOSPage":
        """Click 'Clear Cart' button.

        Returns:
            Self for chaining.
        """
        buttons = [c for c in self.window.descendants() if "Button" in c.friendly_class_name()]
        for btn in buttons:
            if "Clear" in btn.window_text():
                btn.click()
                break
        return self

    @allure.step("Click Checkout")
    def click_checkout(self) -> "MainPOSPage":
        """Click 'Checkout' button to proceed to checkout.

        Returns:
            Self for chaining.
        """
        buttons = [c for c in self.window.descendants() if "Button" in c.friendly_class_name()]
        for btn in buttons:
            if "Checkout" in btn.window_text():
                btn.click()
                break
        return self

    @allure.step("Click Logout")
    def click_logout(self) -> "MainPOSPage":
        """Click the Logout button.

        Returns:
            Self for chaining.
        """
        buttons = [c for c in self.window.descendants() if "Button" in c.friendly_class_name()]
        for btn in buttons:
            if "Logout" in btn.window_text():
                btn.click()
                break
        return self

    def get_total_text(self) -> str:
        """Get the cart total label text.

        Returns:
            The total display string (e.g., 'Total: $89.99').
        """
        labels = [c for c in self.window.descendants() if "Static" in c.friendly_class_name()]
        for label in labels:
            text = label.window_text()
            if "Total:" in text and "$" in text:
                return text
        return ""

    def get_items_count_text(self) -> str:
        """Get the items count label text.

        Returns:
            The items count string (e.g., 'Items: 3').
        """
        labels = [c for c in self.window.descendants() if "Static" in c.friendly_class_name()]
        for label in labels:
            text = label.window_text()
            if "Items:" in text:
                return text
        return ""

    def get_cashier_text(self) -> str:
        """Get the cashier label text from the top bar.

        Returns:
            The cashier display text (e.g., 'Cashier: admin').
        """
        labels = [c for c in self.window.descendants() if "Static" in c.friendly_class_name()]
        for label in labels:
            text = label.window_text()
            if "Cashier:" in text:
                return text
        return ""

    def is_displayed(self) -> bool:
        """Check if the main POS page is currently displayed.

        Returns:
            True if the main POS window is visible.
        """
        try:
            return self.window.exists() and "Login" not in self.window.window_text()
        except Exception:
            return False
