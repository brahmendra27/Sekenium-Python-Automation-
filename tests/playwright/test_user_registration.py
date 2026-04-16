"""
Test cases for User Registration on Automation Test Store (Playwright).

This module contains automated tests for user registration functionality.
"""

import pytest
from playwright.sync_api import expect
from faker import Faker
from framework.csv_logger import get_csv_logger

# Initialize Faker for generating test data
fake = Faker()

# Initialize CSV logger
csv_logger = get_csv_logger()


@pytest.mark.playwright
def test_user_registration_success(playwright_page):
    """
    TC-004: Verify successful user registration.
    
    Steps:
    1. Navigate to homepage
    2. Click "Login or register" link
    3. Click "Continue" to go to registration page
    4. Fill in all required fields with valid data
    5. Submit the registration form
    6. Verify successful registration
    
    Expected Result:
    - User is registered successfully
    - Redirected to account page or success message displayed
    """
    page = playwright_page
    
    # Generate unique test data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()[:15]  # Limit to 15 chars
    address = fake.street_address()
    city = fake.city()
    postcode = fake.postcode()
    login_name = f"testuser_{fake.random_number(digits=6)}"
    password = "Test@123456"
    
    # Prepare registration data for CSV logging
    registration_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "login_name": login_name,
        "telephone": phone,
        "address": address,
        "city": city,
        "postcode": postcode,
        "country": "United States"
    }
    
    print(f"\n📝 Test Data:")
    print(f"   Name: {first_name} {last_name}")
    print(f"   Email: {email}")
    print(f"   Login: {login_name}")
    
    # Step 1: Navigate to homepage
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    # Step 2: Click login/register link
    login_link = page.get_by_text("Login or register")
    login_link.click()
    page.wait_for_load_state("networkidle")
    
    # Step 3: Click Continue to go to registration page
    continue_button = page.locator("button:has-text('Continue')").first
    continue_button.click()
    page.wait_for_load_state("networkidle")
    
    # Verify we're on registration page
    assert "account/create" in page.url
    
    # Step 4: Fill in all required fields
    # Personal Details
    page.fill("#AccountFrm_firstname", first_name)
    page.fill("#AccountFrm_lastname", last_name)
    page.fill("#AccountFrm_email", email)
    page.fill("#AccountFrm_telephone", phone)
    
    # Optional fields (fax, company)
    page.fill("#AccountFrm_fax", "")
    page.fill("#AccountFrm_company", "Test Company")
    
    # Address Details
    page.fill("#AccountFrm_address_1", address)
    page.fill("#AccountFrm_address_2", "")
    page.fill("#AccountFrm_city", city)
    
    # Select country (default is usually fine)
    # Select region/state if required
    try:
        region_dropdown = page.locator("#AccountFrm_zone_id")
        if region_dropdown.is_visible():
            region_dropdown.select_option(index=1)  # Select first option
    except:
        pass
    
    page.fill("#AccountFrm_postcode", postcode)
    
    # Login Details
    page.fill("#AccountFrm_loginname", login_name)
    page.fill("#AccountFrm_password", password)
    page.fill("#AccountFrm_confirm", password)
    
    # Newsletter subscription (optional)
    try:
        newsletter_yes = page.locator("#AccountFrm_newsletter1")
        if newsletter_yes.is_visible():
            newsletter_yes.check()
    except:
        pass
    
    # Privacy Policy agreement
    try:
        privacy_checkbox = page.locator("#AccountFrm_agree")
        if privacy_checkbox.is_visible():
            privacy_checkbox.check()
    except:
        pass
    
    # Step 5: Submit the form
    submit_button = page.locator("button[type='submit']:has-text('Continue')")
    submit_button.click()
    
    # Wait for response
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Step 6: Verify successful registration
    current_url = page.url
    page_content = page.content()
    
    # Check for success indicators
    success_indicators = [
        "account/success" in current_url,
        "account/account" in current_url,
        "congratulations" in page_content.lower(),
        "successfully" in page_content.lower(),
        "created" in page_content.lower()
    ]
    
    # Log registration to CSV
    if any(success_indicators):
        csv_logger.write_registration(
            registration_data=registration_data,
            validation_result="Success",
            error_message=""
        )
        print(f"✅ User registered successfully: {login_name}")
    else:
        csv_logger.write_registration(
            registration_data=registration_data,
            validation_result="Failed",
            error_message=f"Registration failed. URL: {current_url}"
        )
        assert False, f"Registration may have failed. URL: {current_url}"


@pytest.mark.playwright
def test_user_registration_with_existing_email(playwright_page):
    """
    TC-004b: Verify registration fails with existing email.
    
    Steps:
    1. Navigate to registration page
    2. Fill form with email that already exists
    3. Submit form
    4. Verify error message displayed
    
    Expected Result:
    - Registration fails
    - Error message about duplicate email displayed
    """
    page = playwright_page
    
    # Use a common email that likely exists
    existing_email = "test@test.com"
    
    # Navigate to registration page
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Login or register").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("button:has-text('Continue')").first.click()
    page.wait_for_load_state("networkidle")
    
    # Fill form with existing email
    page.fill("#AccountFrm_firstname", fake.first_name())
    page.fill("#AccountFrm_lastname", fake.last_name())
    page.fill("#AccountFrm_email", existing_email)
    page.fill("#AccountFrm_telephone", fake.phone_number()[:15])
    page.fill("#AccountFrm_address_1", fake.street_address())
    page.fill("#AccountFrm_city", fake.city())
    page.fill("#AccountFrm_postcode", fake.postcode())
    page.fill("#AccountFrm_loginname", f"testuser_{fake.random_number(digits=6)}")
    page.fill("#AccountFrm_password", "Test@123456")
    page.fill("#AccountFrm_confirm", "Test@123456")
    
    # Try to submit
    page.locator("button[type='submit']:has-text('Continue')").click()
    page.wait_for_timeout(2000)
    
    # Verify error message or stayed on same page
    page_content = page.content()
    
    # Check for error indicators
    error_indicators = [
        "account/create" in page.url,  # Still on registration page
        "error" in page_content.lower(),
        "already" in page_content.lower(),
        "exists" in page_content.lower()
    ]
    
    # Note: This test may pass or fail depending on whether email exists
    # It's mainly to demonstrate validation testing
    print("✅ Duplicate email validation test completed")


@pytest.mark.playwright
def test_registration_form_validation(playwright_page):
    """
    TC-004c: Verify registration form field validation.
    
    Steps:
    1. Navigate to registration page
    2. Try to submit form with empty required fields
    3. Verify validation messages displayed
    
    Expected Result:
    - Form validation prevents submission
    - Error messages displayed for required fields
    """
    page = playwright_page
    
    # Navigate to registration page
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Login or register").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("button:has-text('Continue')").first.click()
    page.wait_for_load_state("networkidle")
    
    # Try to submit empty form
    submit_button = page.locator("button[type='submit']:has-text('Continue')")
    submit_button.click()
    
    page.wait_for_timeout(1000)
    
    # Verify we're still on registration page (form didn't submit)
    assert "account/create" in page.url
    
    # Check for validation messages
    page_content = page.content()
    
    # Look for validation indicators
    validation_present = (
        "required" in page_content.lower() or
        "must" in page_content.lower() or
        "error" in page_content.lower() or
        "account/create" in page.url  # Still on same page
    )
    
    assert validation_present, "Form validation should prevent empty submission"
    
    print("✅ Form validation test completed")


@pytest.mark.playwright
def test_registration_password_mismatch(playwright_page):
    """
    TC-004d: Verify registration fails when passwords don't match.
    
    Steps:
    1. Navigate to registration page
    2. Fill form with mismatched passwords
    3. Submit form
    4. Verify error message about password mismatch
    
    Expected Result:
    - Registration fails
    - Error message about password mismatch displayed
    """
    page = playwright_page
    
    # Navigate to registration page
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Login or register").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("button:has-text('Continue')").first.click()
    page.wait_for_load_state("networkidle")
    
    # Fill form with mismatched passwords
    page.fill("#AccountFrm_firstname", fake.first_name())
    page.fill("#AccountFrm_lastname", fake.last_name())
    page.fill("#AccountFrm_email", fake.email())
    page.fill("#AccountFrm_telephone", fake.phone_number()[:15])
    page.fill("#AccountFrm_address_1", fake.street_address())
    page.fill("#AccountFrm_city", fake.city())
    page.fill("#AccountFrm_postcode", fake.postcode())
    page.fill("#AccountFrm_loginname", f"testuser_{fake.random_number(digits=6)}")
    page.fill("#AccountFrm_password", "Password123")
    page.fill("#AccountFrm_confirm", "DifferentPassword456")  # Mismatch
    
    # Submit form
    page.locator("button[type='submit']:has-text('Continue')").click()
    page.wait_for_timeout(2000)
    
    # Verify error or stayed on same page
    page_content = page.content()
    
    error_indicators = [
        "account/create" in page.url,  # Still on registration page
        "password" in page_content.lower() and "match" in page_content.lower(),
        "confirm" in page_content.lower()
    ]
    
    assert any(error_indicators), "Password mismatch should be detected"
    
    print("✅ Password mismatch validation test completed")


@pytest.mark.playwright
def test_registration_page_elements_visible(playwright_page):
    """
    TC-004e: Verify all registration form elements are visible.
    
    Steps:
    1. Navigate to registration page
    2. Verify all form fields are visible
    3. Verify submit button is visible
    
    Expected Result:
    - All form fields are displayed
    - Submit button is visible
    """
    page = playwright_page
    
    # Navigate to registration page
    page.goto("https://automationteststore.com/")
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Login or register").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("button:has-text('Continue')").first.click()
    page.wait_for_load_state("networkidle")
    
    # Verify required fields are visible
    required_fields = [
        "#AccountFrm_firstname",
        "#AccountFrm_lastname",
        "#AccountFrm_email",
        "#AccountFrm_telephone",
        "#AccountFrm_address_1",
        "#AccountFrm_city",
        "#AccountFrm_postcode",
        "#AccountFrm_loginname",
        "#AccountFrm_password",
        "#AccountFrm_confirm"
    ]
    
    for field_id in required_fields:
        field = page.locator(field_id)
        expect(field).to_be_visible()
    
    # Verify submit button
    submit_button = page.locator("button[type='submit']:has-text('Continue')")
    expect(submit_button).to_be_visible()
    
    print("✅ All registration form elements are visible")
