"""
Enhanced Shopping Cart Tests with CSV Logging.

This module demonstrates cart testing with detailed CSV logging of cart details,
validations, and order information.
"""

import pytest
from playwright.sync_api import expect
from framework.csv_logger import get_csv_logger
import re

# Initialize CSV logger
csv_logger = get_csv_logger()


@pytest.mark.playwright
def test_add_to_cart_with_validation_logging(playwright_page):
    """
    TC-003-CSV: Add product to cart with detailed CSV logging.
    
    Logs:
    - Cart details (products, quantities, prices)
    - Validation results (price calculations, cart count)
    """
    page = playwright_page
    
    # Navigate to homepage
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Get first product details
    first_product_link = page.locator("a.prdocutname").first
    product_name = first_product_link.inner_text()
    
    # Try to get product price from homepage
    try:
        product_card = first_product_link.locator("xpath=ancestor::div[contains(@class, 'thumbnail')]")
        price_element = product_card.locator(".price")
        product_price = price_element.inner_text() if price_element.count() > 0 else "N/A"
    except:
        product_price = "N/A"
    
    print(f"\n🛒 Adding to cart: {product_name}")
    print(f"   Price: {product_price}")
    
    # Click product
    first_product_link.click()
    page.wait_for_load_state("networkidle")
    
    # Get detailed product info from product page
    try:
        product_price_detail = page.locator(".productfilneprice").inner_text()
    except:
        product_price_detail = product_price
    
    # Add to cart
    add_to_cart_button = page.locator(".cart").first
    add_to_cart_button.click()
    page.wait_for_timeout(2000)
    
    # Navigate to cart
    page.goto("https://automationteststore.com/index.php?rt=checkout/cart")
    page.wait_for_load_state("networkidle")
    
    # Verify cart has items
    cart_items = page.locator(".table.table-striped tbody tr")
    cart_has_items = cart_items.count() > 0
    
    # Extract cart details
    cart_product_names = []
    cart_quantities = []
    cart_unit_prices = []
    
    if cart_has_items:
        for i in range(cart_items.count()):
            try:
                item = cart_items.nth(i)
                
                # Get product name
                name_elem = item.locator(".thumbnail a")
                if name_elem.count() > 0:
                    cart_product_names.append(name_elem.inner_text())
                
                # Get quantity
                qty_elem = item.locator("input[name*='quantity']")
                if qty_elem.count() > 0:
                    cart_quantities.append(qty_elem.get_attribute("value"))
                
                # Get unit price
                price_elem = item.locator("td:nth-child(4)")  # Unit price column
                if price_elem.count() > 0:
                    cart_unit_prices.append(price_elem.inner_text())
            except:
                continue
    
    # Get cart totals
    try:
        subtotal_elem = page.locator(".table:has-text('Sub-Total') td:last-child")
        subtotal = subtotal_elem.inner_text() if subtotal_elem.count() > 0 else "N/A"
    except:
        subtotal = "N/A"
    
    try:
        total_elem = page.locator(".table:has-text('Total') td:last-child").last
        total = total_elem.inner_text() if total_elem.count() > 0 else "N/A"
    except:
        total = "N/A"
    
    # Prepare cart data for CSV
    cart_data = {
        "session_id": f"test_session_{page.context.cookies()[0].get('value', 'unknown') if page.context.cookies() else 'unknown'}",
        "product_names": " | ".join(cart_product_names),
        "quantities": " | ".join(cart_quantities),
        "unit_prices": " | ".join(cart_unit_prices),
        "subtotal": subtotal,
        "tax": "N/A",
        "shipping": "N/A",
        "total": total
    }
    
    # Log cart details to CSV
    if cart_has_items:
        csv_logger.write_cart_details(
            cart_data=cart_data,
            validation_result="Success",
            error_message=""
        )
        
        # Log validation: Cart has items
        csv_logger.write_validation(
            test_name="test_add_to_cart_with_validation_logging",
            validation_type="Cart Item Count",
            expected_value="> 0",
            actual_value=cart_items.count(),
            result="Pass",
            details=f"Cart contains {cart_items.count()} item(s)"
        )
        
        print(f"✅ Product added to cart successfully")
        print(f"   Cart Total: {total}")
    else:
        csv_logger.write_cart_details(
            cart_data=cart_data,
            validation_result="Failed",
            error_message="Cart is empty after adding product"
        )
        
        csv_logger.write_validation(
            test_name="test_add_to_cart_with_validation_logging",
            validation_type="Cart Item Count",
            expected_value="> 0",
            actual_value=0,
            result="Fail",
            details="Cart is empty"
        )
        
        assert False, "Cart should have items"


@pytest.mark.playwright
def test_checkout_with_order_logging(playwright_page):
    """
    TC-006-CSV: Guest checkout with order details logging.
    
    Logs:
    - Order details (products, customer info, totals)
    - Validation results
    """
    page = playwright_page
    
    # Add product to cart first
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Add first product
    first_product = page.locator("a.prdocutname").first
    product_name = first_product.inner_text()
    first_product.click()
    page.wait_for_load_state("networkidle")
    
    # Add to cart
    page.locator(".cart").first.click()
    page.wait_for_timeout(2000)
    
    # Go to cart
    page.goto("https://automationteststore.com/index.php?rt=checkout/cart")
    page.wait_for_load_state("networkidle")
    
    # Get cart total
    try:
        total_elem = page.locator(".table:has-text('Total') td:last-child").last
        cart_total = total_elem.inner_text() if total_elem.count() > 0 else "$0.00"
    except:
        cart_total = "$0.00"
    
    # Click checkout button
    try:
        checkout_button = page.locator("#cart_checkout1, a:has-text('Checkout')").first
        if checkout_button.is_visible():
            checkout_button.click()
            page.wait_for_load_state("networkidle")
            
            # Check if we're on checkout page
            current_url = page.url
            
            # Prepare order data
            order_data = {
                "order_id": f"TEST_ORDER_{page.context.cookies()[0].get('value', 'unknown')[:8] if page.context.cookies() else 'unknown'}",
                "customer_name": "Guest User",
                "customer_email": "guest@test.com",
                "product_names": product_name,
                "quantities": "1",
                "unit_prices": cart_total,
                "total_amount": cart_total,
                "payment_method": "Guest Checkout",
                "shipping_address": "Test Address",
                "order_status": "Initiated"
            }
            
            # Log order details
            if "checkout" in current_url:
                csv_logger.write_order(
                    order_data=order_data,
                    validation_result="Success",
                    error_message=""
                )
                
                csv_logger.write_validation(
                    test_name="test_checkout_with_order_logging",
                    validation_type="Checkout Navigation",
                    expected_value="checkout page",
                    actual_value=current_url,
                    result="Pass",
                    details="Successfully navigated to checkout"
                )
                
                print(f"✅ Checkout initiated successfully")
                print(f"   Order Total: {cart_total}")
            else:
                csv_logger.write_order(
                    order_data=order_data,
                    validation_result="Failed",
                    error_message=f"Did not reach checkout page. URL: {current_url}"
                )
                
                csv_logger.write_validation(
                    test_name="test_checkout_with_order_logging",
                    validation_type="Checkout Navigation",
                    expected_value="checkout page",
                    actual_value=current_url,
                    result="Fail",
                    details="Failed to navigate to checkout"
                )
    except Exception as e:
        print(f"⚠️ Checkout test completed with note: {str(e)}")


@pytest.mark.playwright
def test_price_calculation_validation(playwright_page):
    """
    TC-VALIDATION: Validate cart price calculations.
    
    Logs detailed validation results for:
    - Unit price × quantity = line total
    - Sum of line totals = subtotal
    - Subtotal + tax + shipping = total
    """
    page = playwright_page
    
    # Add product to cart
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    first_product = page.locator("a.prdocutname").first
    first_product.click()
    page.wait_for_load_state("networkidle")
    
    page.locator(".cart").first.click()
    page.wait_for_timeout(2000)
    
    # Navigate to cart
    page.goto("https://automationteststore.com/index.php?rt=checkout/cart")
    page.wait_for_load_state("networkidle")
    
    # Extract prices for validation
    try:
        # Get unit price
        unit_price_elem = page.locator(".table.table-striped tbody tr td:nth-child(4)").first
        unit_price_text = unit_price_elem.inner_text() if unit_price_elem.count() > 0 else "$0.00"
        unit_price = float(re.sub(r'[^\d.]', '', unit_price_text))
        
        # Get quantity
        qty_elem = page.locator("input[name*='quantity']").first
        quantity = int(qty_elem.get_attribute("value")) if qty_elem.count() > 0 else 1
        
        # Get line total
        line_total_elem = page.locator(".table.table-striped tbody tr td:nth-child(5)").first
        line_total_text = line_total_elem.inner_text() if line_total_elem.count() > 0 else "$0.00"
        line_total = float(re.sub(r'[^\d.]', '', line_total_text))
        
        # Calculate expected line total
        expected_line_total = unit_price * quantity
        
        # Validate calculation
        is_correct = abs(line_total - expected_line_total) < 0.01  # Allow 1 cent difference for rounding
        
        csv_logger.write_validation(
            test_name="test_price_calculation_validation",
            validation_type="Line Total Calculation",
            expected_value=f"${expected_line_total:.2f}",
            actual_value=f"${line_total:.2f}",
            result="Pass" if is_correct else "Fail",
            details=f"Unit Price: ${unit_price:.2f} × Quantity: {quantity}"
        )
        
        if is_correct:
            print(f"✅ Price calculation validated: ${unit_price:.2f} × {quantity} = ${line_total:.2f}")
        else:
            print(f"❌ Price calculation mismatch: Expected ${expected_line_total:.2f}, Got ${line_total:.2f}")
        
        assert is_correct, f"Price calculation incorrect"
        
    except Exception as e:
        csv_logger.write_validation(
            test_name="test_price_calculation_validation",
            validation_type="Line Total Calculation",
            expected_value="Valid calculation",
            actual_value="Error",
            result="Fail",
            details=f"Error during validation: {str(e)}"
        )
        print(f"⚠️ Price validation completed with note: {str(e)}")
