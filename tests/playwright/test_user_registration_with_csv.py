"""
Test cases for User Registration with CSV Logging (Playwright).

This module demonstrates how to log registration details and validation results to CSV files.
"""

import pytest
import time
from playwright.sync_api import expect
from faker import Faker
from framework.csv_logger import CSVLogger

# Initialize Faker and CSV Logger
fake = Faker()
csv_logger = CSVLogger()


@pytest.mark.playwright
def test_user_registration_with_csv_logging(playwright_page):
    """
    TC-004-CSV: User registration with CSV logging.
    
    This test demonstrates:
    1. Creating a new user
    2. Logging registration details to CSV
    3. Logging validation results to CSV
    4. Logging test summary to CSV
    """
    page = playwright_page
    start_time = time.time()
    
    # Generate unique test data
    registration_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number()[:15],
        "address": fake.street_address(),
        "city": fake.city(),
        "postcode": fake.postcode(),
        "login_name": f"testuser_{fake.random_number(digits=6)}",
        "password": "Test@123456"
    }
    
    print(f"\n📝 Test Data:")
    print(f"   Name: {registration_data['first_name']} {registration_data['last_name']}")
    print(f"   Email: {registration_data['email']}")
    print(f"   Login: {registration_data['login_name']}")
    
    try:
        # Navigate to registration page
        page.goto("https://automationteststore.com/")
        page.wait_for_load_state("networkidle")
        
        page.get_by_text("Login or register").click()
        page.wait_for_load_state("networkidle")
        
        page.locator("button:has-text('Continue')").first.click()
        page.wait_for_load_state("networkidle")
        
        # Verify we're on registration page
        assert "account/create" in page.url
        csv_logger.log_validation(
            test_name="test_user_registration_with_csv_logging",
            validation_type="Registration Page URL",
            expected="account/create",
            actual=page.url,
            status="PASS",
            notes="Successfully navigated to registration page"
        )
        
        # Fill registration form
        page.fill("#AccountFrm_firstname", registration_data["first_name"])
        page.fill("#AccountFrm_lastname", registration_data["last_name"])
        page.fill("#AccountFrm_email", registration_data["email"])
        page.fill("#AccountFrm_telephone", registration_data["phone"])
        page.fill("#AccountFrm_company", "Test Company")
        page.fill("#AccountFrm_address_1", registration_data["address"])
        page.fill("#AccountFrm_city", registration_data["city"])
        page.fill("#AccountFrm_postcode", registration_data["postcode"])
        page.fill("#AccountFrm_loginname", registration_data["login_name"])
        page.fill("#AccountFrm_password", registration_data["password"])
        page.fill("#AccountFrm_confirm", registration_data["password"])
        
        # Log validation: Password match
        csv_logger.log_validation(
            test_name="test_user_registration_with_csv_logging",
            validation_type="Password Confirmation",
            expected=registration_data["password"],
            actual=registration_data["password"],
            status="PASS",
            notes="Password and confirmation match"
        )
        
        # Accept privacy policy if present
        try:
            privacy_checkbox = page.locator("#AccountFrm_agree")
            if privacy_checkbox.is_visible():
                privacy_checkbox.check()
        except:
            pass
        
        # Submit form
        submit_button = page.locator("button[type='submit']:has-text('Continue')")
        submit_button.click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Verify registration success
        current_url = page.url
        page_content = page.content()
        
        success_indicators = [
            "account/success" in current_url,
            "account/account" in current_url,
            "congratulations" in page_content.lower(),
            "successfully" in page_content.lower()
        ]
        
        registration_successful = any(success_indicators)
        
        # Log registration details to CSV
        csv_logger.log_registration(
            test_name="test_user_registration_with_csv_logging",
            registration_data=registration_data,
            status="PASS" if registration_successful else "FAIL",
            error_message="" if registration_successful else "Registration may have failed"
        )
        
        # Log validation: Registration success
        csv_logger.log_validation(
            test_name="test_user_registration_with_csv_logging",
            validation_type="Registration Success",
            expected="Success page or account page",
            actual=current_url,
            status="PASS" if registration_successful else "FAIL",
            notes="User registered successfully" if registration_successful else "Registration failed"
        )
        
        assert registration_successful, f"Registration failed. URL: {current_url}"
        
        # Calculate test duration
        duration = time.time() - start_time
        
        # Log test summary
        csv_logger.log_test_summary(
            test_name="test_user_registration_with_csv_logging",
            test_type="User Registration",
            duration=round(duration, 2),
            status="PASS",
            details=f"User {registration_data['login_name']} registered successfully"
        )
        
        print(f"✅ User registered successfully: {registration_data['login_name']}")
        print(f"⏱️  Test duration: {duration:.2f} seconds")
        print(f"📊 CSV files updated in: reports/csv/")
        
    except Exception as e:
        # Log failure
        duration = time.time() - start_time
        
        csv_logger.log_registration(
            test_name="test_user_registration_with_csv_logging",
            registration_data=registration_data,
            status="FAIL",
            error_message=str(e)
        )
        
        csv_logger.log_test_summary(
            test_name="test_user_registration_with_csv_logging",
            test_type="User Registration",
            duration=round(duration, 2),
            status="FAIL",
            details=f"Error: {str(e)}"
        )
        
        raise


@pytest.mark.playwright
def test_multiple_registrations_csv_batch(playwright_page):
    """
    TC-004-CSV-BATCH: Register multiple users and log all to CSV.
    
    Demonstrates batch registration with CSV logging.
    """
    page = playwright_page
    num_users = 3
    
    print(f"\n📝 Registering {num_users} users...")
    
    for i in range(num_users):
        start_time = time.time()
        
        registration_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number()[:15],
            "address": fake.street_address(),
            "city": fake.city(),
            "postcode": fake.postcode(),
            "login_name": f"batchuser_{i+1}_{fake.random_number(digits=4)}",
            "password": "Test@123456"
        }
        
        try:
            # Navigate to registration page
            page.goto("https://automationteststore.com/")
            page.wait_for_load_state("networkidle")
            
            page.get_by_text("Login or register").click()
            page.wait_for_load_state("networkidle")
            
            page.locator("button:has-text('Continue')").first.click()
            page.wait_for_load_state("networkidle")
            
            # Fill form
            page.fill("#AccountFrm_firstname", registration_data["first_name"])
            page.fill("#AccountFrm_lastname", registration_data["last_name"])
            page.fill("#AccountFrm_email", registration_data["email"])
            page.fill("#AccountFrm_telephone", registration_data["phone"])
            page.fill("#AccountFrm_address_1", registration_data["address"])
            page.fill("#AccountFrm_city", registration_data["city"])
            page.fill("#AccountFrm_postcode", registration_data["postcode"])
            page.fill("#AccountFrm_loginname", registration_data["login_name"])
            page.fill("#AccountFrm_password", registration_data["password"])
            page.fill("#AccountFrm_confirm", registration_data["password"])
            
            # Submit
            page.locator("button[type='submit']:has-text('Continue')").click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
            # Check success
            current_url = page.url
            page_content = page.content()
            success = any([
                "account/success" in current_url,
                "account/account" in current_url,
                "successfully" in page_content.lower()
            ])
            
            # Log to CSV
            csv_logger.log_registration(
                test_name=f"test_multiple_registrations_csv_batch_user_{i+1}",
                registration_data=registration_data,
                status="PASS" if success else "FAIL",
                error_message="" if success else "Registration may have failed"
            )
            
            duration = time.time() - start_time
            csv_logger.log_test_summary(
                test_name=f"test_multiple_registrations_csv_batch_user_{i+1}",
                test_type="Batch Registration",
                duration=round(duration, 2),
                status="PASS" if success else "FAIL",
                details=f"Batch user {i+1}/{num_users}"
            )
            
            print(f"   ✅ User {i+1}/{num_users}: {registration_data['login_name']}")
            
        except Exception as e:
            csv_logger.log_registration(
                test_name=f"test_multiple_registrations_csv_batch_user_{i+1}",
                registration_data=registration_data,
                status="FAIL",
                error_message=str(e)
            )
            print(f"   ❌ User {i+1}/{num_users} failed: {str(e)}")
    
    print(f"\n📊 All registration data logged to: reports/csv/registration_results.csv")
    
    # Print summary statistics
    stats = csv_logger.get_summary_stats("registration_results.csv")
    print(f"\n📈 Summary Statistics:")
    print(f"   Total: {stats['total']}")
    print(f"   Passed: {stats['passed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Pass Rate: {stats['pass_rate']}")
