"""
Allure Reporting Demo - Test with detailed reporting.

This test demonstrates Allure's rich reporting features:
- Test steps with descriptions
- Screenshots on failure
- Test parameters
- Severity levels
- Test categories
- Links to test cases
- Attachments
"""

import pytest
import allure
from playwright.sync_api import expect
from faker import Faker

fake = Faker()


@allure.epic("E-Commerce")
@allure.feature("User Registration")
@allure.story("New User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "registration", "user-management")
@allure.label("owner", "QA Team")
@allure.link("https://automationteststore.com/", name="Application URL")
@pytest.mark.playwright
def test_user_registration_with_allure(playwright_page):
    """
    Test user registration with complete Allure reporting.
    
    This test demonstrates all Allure features:
    - Step-by-step reporting
    - Screenshots
    - Test data logging
    - Assertions with descriptions
    """
    page = playwright_page
    
    # Generate test data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    login_name = f"user_{fake.random_number(digits=6)}"
    
    # Attach test data to report
    allure.attach(
        f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nLogin: {login_name}",
        name="Test Data",
        attachment_type=allure.attachment_type.TEXT
    )
    
    with allure.step("Navigate to homepage"):
        page.goto("https://automationteststore.com/")
        page.wait_for_load_state("networkidle")
        
        # Take screenshot
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Homepage",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Verify homepage loaded
        with allure.step("Verify homepage URL"):
            assert "automationteststore.com" in page.url, "Homepage did not load"
    
    with allure.step("Click 'Login or register' link"):
        login_link = page.get_by_text("Login or register")
        
        # Log the action
        allure.attach(
            "Clicking on 'Login or register' link",
            name="Action",
            attachment_type=allure.attachment_type.TEXT
        )
        
        login_link.click()
        page.wait_for_load_state("networkidle")
        
        # Screenshot after click
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Login Page",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Navigate to registration page"):
        continue_button = page.locator("button:has-text('Continue')").first
        
        allure.attach(
            "Clicking 'Continue' button to access registration form",
            name="Action",
            attachment_type=allure.attachment_type.TEXT
        )
        
        continue_button.click()
        page.wait_for_load_state("networkidle")
        
        # Verify registration page
        with allure.step("Verify registration page loaded"):
            assert "account/create" in page.url, "Registration page did not load"
        
        # Screenshot
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Registration Form",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Fill registration form"):
        with allure.step(f"Enter first name: {first_name}"):
            page.fill("#AccountFrm_firstname", first_name)
        
        with allure.step(f"Enter last name: {last_name}"):
            page.fill("#AccountFrm_lastname", last_name)
        
        with allure.step(f"Enter email: {email}"):
            page.fill("#AccountFrm_email", email)
        
        with allure.step("Enter phone number"):
            page.fill("#AccountFrm_telephone", fake.phone_number()[:15])
        
        with allure.step("Enter address"):
            page.fill("#AccountFrm_address_1", fake.street_address())
        
        with allure.step("Enter city"):
            page.fill("#AccountFrm_city", fake.city())
        
        with allure.step("Enter postcode"):
            page.fill("#AccountFrm_postcode", fake.postcode())
        
        with allure.step(f"Enter login name: {login_name}"):
            page.fill("#AccountFrm_loginname", login_name)
        
        with allure.step("Enter password"):
            page.fill("#AccountFrm_password", "Test@123456")
            page.fill("#AccountFrm_confirm", "Test@123456")
        
        # Screenshot of filled form
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Filled Registration Form",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Submit registration form"):
        submit_button = page.locator("button[type='submit']:has-text('Continue')")
        
        allure.attach(
            "Clicking submit button to register user",
            name="Action",
            attachment_type=allure.attachment_type.TEXT
        )
        
        submit_button.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Screenshot after submission
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="After Submission",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Verify registration success"):
        current_url = page.url
        page_content = page.content()
        
        # Log verification details
        allure.attach(
            f"Current URL: {current_url}\nPage contains 'success': {'success' in page_content.lower()}",
            name="Verification Details",
            attachment_type=allure.attachment_type.TEXT
        )
        
        success_indicators = [
            "account/success" in current_url,
            "account/account" in current_url,
            "successfully" in page_content.lower()
        ]
        
        registration_successful = any(success_indicators)
        
        with allure.step(f"Assert registration successful: {registration_successful}"):
            assert registration_successful, f"Registration failed. URL: {current_url}"
        
        # Final screenshot
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Registration Success",
            attachment_type=allure.attachment_type.PNG
        )
    
    # Attach final summary
    allure.attach(
        f"✅ User '{login_name}' registered successfully!\nEmail: {email}",
        name="Test Summary",
        attachment_type=allure.attachment_type.TEXT
    )


@allure.epic("E-Commerce")
@allure.feature("Shopping Cart")
@allure.story("Add Product to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "cart", "shopping")
@pytest.mark.playwright
def test_add_to_cart_with_allure(playwright_page):
    """Test adding product to cart with Allure reporting."""
    page = playwright_page
    
    with allure.step("Navigate to homepage"):
        page.goto("https://automationteststore.com/")
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(screenshot, name="Homepage", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Click on first product"):
        first_product = page.locator("a.prdocutname").first
        product_name = first_product.inner_text()
        
        allure.attach(
            f"Clicking on product: {product_name}",
            name="Action",
            attachment_type=allure.attachment_type.TEXT
        )
        
        first_product.click()
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(screenshot, name="Product Page", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Add product to cart"):
        add_to_cart_button = page.locator(".cart").first
        add_to_cart_button.click()
        page.wait_for_timeout(2000)
        
        allure.attach(
            f"Product '{product_name}' added to cart",
            name="Cart Operation",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Navigate to cart"):
        page.goto("https://automationteststore.com/index.php?rt=checkout/cart")
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(screenshot, name="Shopping Cart", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Verify product in cart"):
        cart_items = page.locator(".table.table-striped tbody tr")
        
        with allure.step("Assert cart has items"):
            expect(cart_items.first).to_be_visible()
        
        allure.attach(
            f"✅ Product successfully added to cart",
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("E-Commerce")
@allure.feature("Product Search")
@allure.story("Search Functionality")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("search", "products")
@pytest.mark.playwright
@pytest.mark.parametrize("search_term", [
    pytest.param("skincare", id="search-skincare"),
    pytest.param("makeup", id="search-makeup"),
    pytest.param("fragrance", id="search-fragrance"),
])
def test_product_search_with_allure(playwright_page, search_term):
    """Test product search with different terms."""
    page = playwright_page
    
    allure.dynamic.title(f"Search for '{search_term}'")
    allure.dynamic.description(f"Test searching for products with term: {search_term}")
    
    with allure.step("Navigate to homepage"):
        page.goto("https://automationteststore.com/")
        page.wait_for_load_state("networkidle")
    
    with allure.step(f"Search for '{search_term}'"):
        page.fill("#filter_keyword", search_term)
        page.locator("#filter_keyword").press("Enter")
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"Search Results for '{search_term}'",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Verify search executed"):
        current_url = page.url
        
        allure.attach(
            f"Search URL: {current_url}",
            name="Search Result URL",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert ("keyword=" in current_url or "product" in current_url), \
            f"Search did not execute for term '{search_term}'"
        
        allure.attach(
            f"✅ Search for '{search_term}' executed successfully",
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("E-Commerce")
@allure.feature("User Registration")
@allure.story("Form Validation")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("validation", "negative-test")
@pytest.mark.playwright
def test_registration_validation_with_allure(playwright_page):
    """Test registration form validation with empty fields."""
    page = playwright_page
    
    with allure.step("Navigate to registration page"):
        page.goto("https://automationteststore.com/")
        page.wait_for_load_state("networkidle")
        
        page.get_by_text("Login or register").click()
        page.wait_for_load_state("networkidle")
        
        page.locator("button:has-text('Continue')").first.click()
        page.wait_for_load_state("networkidle")
        
        screenshot = page.screenshot()
        allure.attach(screenshot, name="Empty Registration Form", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Submit empty form"):
        submit_button = page.locator("button[type='submit']:has-text('Continue')")
        submit_button.click()
        page.wait_for_timeout(1000)
        
        screenshot = page.screenshot()
        allure.attach(screenshot, name="After Empty Submission", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Verify validation prevents submission"):
        current_url = page.url
        
        allure.attach(
            f"Current URL: {current_url}\nExpected: Still on registration page",
            name="Validation Check",
            attachment_type=allure.attachment_type.TEXT
        )
        
        with allure.step("Assert still on registration page"):
            assert "account/create" in current_url, "Form validation did not prevent submission"
        
        allure.attach(
            "✅ Form validation working correctly",
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )
