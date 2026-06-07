"""Sample Point of Sale (POS) Desktop Application for automation testing.

A simple Tkinter-based POS with:
- Login screen (username/password)
- Product catalog with search
- Shopping cart (add/remove/quantity)
- Checkout with payment method selection
- Receipt generation

Launch: python sample_apps/pos_app.py

Test credentials:
    username: admin
    password: admin123
    (or any user in the USERS dict)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# --- Data ---

USERS = {
    "admin": "admin123",
    "cashier": "cash456",
    "manager": "mgr789",
}

PRODUCTS = [
    {"id": "P001", "name": "Running Shoes", "category": "Footwear", "price": 89.99, "stock": 50},
    {"id": "P002", "name": "Casual Sneakers", "category": "Footwear", "price": 64.99, "stock": 35},
    {"id": "P003", "name": "Sport Socks (3-Pack)", "category": "Accessories", "price": 12.99, "stock": 100},
    {"id": "P004", "name": "Athletic T-Shirt", "category": "Apparel", "price": 29.99, "stock": 75},
    {"id": "P005", "name": "Training Shorts", "category": "Apparel", "price": 34.99, "stock": 60},
    {"id": "P006", "name": "Water Bottle 750ml", "category": "Accessories", "price": 14.99, "stock": 200},
    {"id": "P007", "name": "Gym Backpack", "category": "Accessories", "price": 49.99, "stock": 40},
    {"id": "P008", "name": "Hiking Boots", "category": "Footwear", "price": 129.99, "stock": 25},
    {"id": "P009", "name": "Yoga Mat", "category": "Equipment", "price": 24.99, "stock": 80},
    {"id": "P010", "name": "Resistance Bands Set", "category": "Equipment", "price": 19.99, "stock": 90},
    {"id": "P011", "name": "Compression Leggings", "category": "Apparel", "price": 44.99, "stock": 55},
    {"id": "P012", "name": "Sports Sunglasses", "category": "Accessories", "price": 39.99, "stock": 30},
]

PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Gift Card"]


# --- Application ---

class POSApp:
    """Main POS Application class."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QE Sample POS - Login")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        # State
        self.current_user = None
        self.cart = []  # list of {"product": dict, "quantity": int}
        self.transaction_count = 0

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Show login
        self._show_login()

    def _clear_window(self):
        """Remove all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Login Screen ---

    def _show_login(self):
        """Display the login screen."""
        self._clear_window()
        self.root.title("QE Sample POS - Login")

        frame = ttk.Frame(self.root, padding=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Point of Sale System", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 30)
        )

        ttk.Label(frame, text="Username:", font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=5
        )
        self.username_entry = ttk.Entry(frame, width=25, font=("Segoe UI", 11))
        self.username_entry.grid(row=1, column=1, pady=5)
        self.username_entry.focus()

        ttk.Label(frame, text="Password:", font=("Segoe UI", 11)).grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=5
        )
        self.password_entry = ttk.Entry(frame, width=25, show="*", font=("Segoe UI", 11))
        self.password_entry.grid(row=2, column=1, pady=5)

        self.login_btn = ttk.Button(frame, text="Login", command=self._do_login, width=20)
        self.login_btn.grid(row=3, column=0, columnspan=2, pady=(20, 5))

        self.login_error_label = ttk.Label(frame, text="", foreground="red", font=("Segoe UI", 9))
        self.login_error_label.grid(row=4, column=0, columnspan=2)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._do_login())

    def _do_login(self):
        """Validate credentials and proceed to main screen."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.login_error_label.config(text="Please enter username and password")
            return

        if username in USERS and USERS[username] == password:
            self.current_user = username
            self.root.unbind("<Return>")
            self._show_main()
        else:
            self.login_error_label.config(text="Invalid username or password")
            self.password_entry.delete(0, tk.END)

    # --- Main POS Screen ---

    def _show_main(self):
        """Display the main POS screen with products and cart."""
        self._clear_window()
        self.root.title(f"QE Sample POS - {self.current_user}")

        # Top bar
        top_frame = ttk.Frame(self.root, padding=(10, 5))
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text=f"Cashier: {self.current_user}", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(top_frame, text="Logout", command=self._logout).pack(side="right")

        # Main content: left = products, right = cart
        content = ttk.PanedWindow(self.root, orient="horizontal")
        content.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Left: Product Catalog ---
        left_frame = ttk.LabelFrame(content, text="Product Catalog", padding=10)
        content.add(left_frame, weight=3)

        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_products())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=(5, 10))

        ttk.Label(search_frame, text="Category:").pack(side="left")
        categories = ["All"] + sorted(set(p["category"] for p in PRODUCTS))
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(
            search_frame, textvariable=self.category_var,
            values=categories, state="readonly", width=12
        )
        self.category_combo.pack(side="left", padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self._filter_products())

        # Product table
        columns = ("id", "name", "category", "price", "stock")
        self.product_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("category", text="Category")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("stock", text="Stock")
        self.product_tree.column("id", width=50)
        self.product_tree.column("name", width=160)
        self.product_tree.column("category", width=90)
        self.product_tree.column("price", width=60)
        self.product_tree.column("stock", width=50)

        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)

        self.product_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add to Cart button
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        self.add_to_cart_btn = ttk.Button(btn_frame, text="Add to Cart", command=self._add_to_cart)
        self.add_to_cart_btn.pack(side="left")

        ttk.Label(btn_frame, text="Qty:").pack(side="left", padx=(15, 5))
        self.qty_var = tk.StringVar(value="1")
        self.qty_spin = ttk.Spinbox(btn_frame, from_=1, to=99, textvariable=self.qty_var, width=5)
        self.qty_spin.pack(side="left")

        self._populate_products()

        # --- Right: Shopping Cart ---
        right_frame = ttk.LabelFrame(content, text="Shopping Cart", padding=10)
        content.add(right_frame, weight=2)

        # Cart table
        cart_cols = ("name", "qty", "price", "subtotal")
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_cols, show="headings", height=12)
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.heading("subtotal", text="Subtotal")
        self.cart_tree.column("name", width=130)
        self.cart_tree.column("qty", width=40)
        self.cart_tree.column("price", width=60)
        self.cart_tree.column("subtotal", width=70)
        self.cart_tree.pack(fill="both", expand=True)

        # Cart actions
        cart_btn_frame = ttk.Frame(right_frame)
        cart_btn_frame.pack(fill="x", pady=(10, 5))

        self.remove_btn = ttk.Button(cart_btn_frame, text="Remove Selected", command=self._remove_from_cart)
        self.remove_btn.pack(side="left")

        self.clear_cart_btn = ttk.Button(cart_btn_frame, text="Clear Cart", command=self._clear_cart)
        self.clear_cart_btn.pack(side="left", padx=10)

        # Totals
        totals_frame = ttk.Frame(right_frame)
        totals_frame.pack(fill="x", pady=(5, 0))

        self.items_label = ttk.Label(totals_frame, text="Items: 0", font=("Segoe UI", 10))
        self.items_label.pack(side="left")

        self.total_label = ttk.Label(totals_frame, text="Total: $0.00", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(side="right")

        # Checkout button
        self.checkout_btn = ttk.Button(right_frame, text="Checkout", command=self._show_checkout)
        self.checkout_btn.pack(fill="x", pady=(10, 0))

    def _populate_products(self, products=None):
        """Fill the product treeview."""
        self.product_tree.delete(*self.product_tree.get_children())
        for p in (products or PRODUCTS):
            self.product_tree.insert("", "end", values=(
                p["id"], p["name"], p["category"], f"${p['price']:.2f}", p["stock"]
            ))

    def _filter_products(self):
        """Filter products by search text and category."""
        query = self.search_var.get().lower().strip()
        category = self.category_var.get()

        filtered = PRODUCTS
        if category != "All":
            filtered = [p for p in filtered if p["category"] == category]
        if query:
            filtered = [p for p in filtered if query in p["name"].lower() or query in p["id"].lower()]

        self._populate_products(filtered)

    def _add_to_cart(self):
        """Add selected product to the cart."""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to add.")
            return

        item_values = self.product_tree.item(selection[0], "values")
        product_id = item_values[0]
        product = next(p for p in PRODUCTS if p["id"] == product_id)

        try:
            qty = int(self.qty_var.get())
            if qty < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")
            return

        if qty > product["stock"]:
            messagebox.showwarning("Insufficient Stock", f"Only {product['stock']} available.")
            return

        # Check if already in cart
        for item in self.cart:
            if item["product"]["id"] == product_id:
                item["quantity"] += qty
                self._refresh_cart()
                return

        self.cart.append({"product": product, "quantity": qty})
        self._refresh_cart()

    def _remove_from_cart(self):
        """Remove selected item from cart."""
        selection = self.cart_tree.selection()
        if not selection:
            return

        idx = self.cart_tree.index(selection[0])
        if 0 <= idx < len(self.cart):
            self.cart.pop(idx)
            self._refresh_cart()

    def _clear_cart(self):
        """Clear all items from the cart."""
        self.cart.clear()
        self._refresh_cart()

    def _refresh_cart(self):
        """Refresh the cart display and totals."""
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0.0
        total_items = 0

        for item in self.cart:
            subtotal = item["product"]["price"] * item["quantity"]
            total += subtotal
            total_items += item["quantity"]
            self.cart_tree.insert("", "end", values=(
                item["product"]["name"],
                item["quantity"],
                f"${item['product']['price']:.2f}",
                f"${subtotal:.2f}",
            ))

        self.items_label.config(text=f"Items: {total_items}")
        self.total_label.config(text=f"Total: ${total:.2f}")

    # --- Checkout Screen ---

    def _show_checkout(self):
        """Show checkout dialog."""
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Please add items to the cart before checkout.")
            return

        total = sum(item["product"]["price"] * item["quantity"] for item in self.cart)

        checkout_win = tk.Toplevel(self.root)
        checkout_win.title("Checkout")
        checkout_win.geometry("400x350")
        checkout_win.resizable(False, False)
        checkout_win.grab_set()

        frame = ttk.Frame(checkout_win, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Checkout", font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

        # Order summary
        summary_frame = ttk.LabelFrame(frame, text="Order Summary", padding=10)
        summary_frame.pack(fill="x", pady=(0, 10))

        for item in self.cart:
            subtotal = item["product"]["price"] * item["quantity"]
            ttk.Label(
                summary_frame,
                text=f"{item['product']['name']} x{item['quantity']}  -  ${subtotal:.2f}"
            ).pack(anchor="w")

        ttk.Separator(summary_frame, orient="horizontal").pack(fill="x", pady=5)
        ttk.Label(summary_frame, text=f"Total: ${total:.2f}", font=("Segoe UI", 11, "bold")).pack(anchor="e")

        # Payment method
        pay_frame = ttk.Frame(frame)
        pay_frame.pack(fill="x", pady=10)

        ttk.Label(pay_frame, text="Payment Method:").pack(side="left")
        self.payment_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(
            pay_frame, textvariable=self.payment_var,
            values=PAYMENT_METHODS, state="readonly", width=15
        )
        payment_combo.pack(side="left", padx=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text="Cancel", command=checkout_win.destroy).pack(side="left")
        self.complete_btn = ttk.Button(
            btn_frame, text="Complete Sale",
            command=lambda: self._complete_sale(checkout_win, total)
        )
        self.complete_btn.pack(side="right")

    def _complete_sale(self, checkout_win, total):
        """Process the sale and show receipt."""
        self.transaction_count += 1
        payment = self.payment_var.get()
        checkout_win.destroy()

        # Update stock
        for item in self.cart:
            for p in PRODUCTS:
                if p["id"] == item["product"]["id"]:
                    p["stock"] -= item["quantity"]
                    break

        # Generate receipt
        self._show_receipt(total, payment)

        # Clear cart
        self.cart.clear()
        self._refresh_cart()
        self._filter_products()

    def _show_receipt(self, total, payment):
        """Show receipt in a dialog."""
        receipt_win = tk.Toplevel(self.root)
        receipt_win.title("Receipt")
        receipt_win.geometry("350x450")
        receipt_win.resizable(False, False)

        frame = ttk.Frame(receipt_win, padding=20)
        frame.pack(fill="both", expand=True)

        receipt_text = tk.Text(frame, font=("Courier", 9), wrap="word", height=20)
        receipt_text.pack(fill="both", expand=True)

        now = datetime.now()
        lines = [
            "=" * 40,
            "        QE SAMPLE POS - RECEIPT",
            "=" * 40,
            f"  Date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Cashier: {self.current_user}",
            f"  Transaction #: {self.transaction_count:04d}",
            "-" * 40,
        ]

        for item in self.cart:
            subtotal = item["product"]["price"] * item["quantity"]
            lines.append(f"  {item['product']['name']}")
            lines.append(f"    {item['quantity']} x ${item['product']['price']:.2f} = ${subtotal:.2f}")

        lines.extend([
            "-" * 40,
            f"  TOTAL: ${total:.2f}",
            f"  Payment: {payment}",
            "=" * 40,
            "       Thank you for your purchase!",
            "=" * 40,
        ])

        receipt_text.insert("1.0", "\n".join(lines))
        receipt_text.config(state="disabled")

        ttk.Button(frame, text="Close", command=receipt_win.destroy).pack(pady=(10, 0))

    # --- Logout ---

    def _logout(self):
        """Log out and return to login screen."""
        self.current_user = None
        self.cart.clear()
        self._show_login()

    # --- Run ---

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = POSApp()
    app.run()
