# 📊 CSV Logging Demo - Complete Guide

## ✅ What Was Created

### 1. CSV Logger Framework
**File:** `framework/csv_logger.py`

**Features:**
- ✅ Log user registrations
- ✅ Log order details
- ✅ Log cart operations
- ✅ Log validation results
- ✅ Log test summaries
- ✅ Read CSV data
- ✅ Get summary statistics

### 2. Test with CSV Logging
**File:** `tests/playwright/test_user_registration_with_csv.py`

**Features:**
- ✅ Logs registration data to CSV
- ✅ Logs validation results to CSV
- ✅ Logs test execution summary to CSV
- ✅ Batch registration with CSV logging
- ✅ Summary statistics

### 3. CSV Output Files
**Location:** `reports/csv/`

**Files Created:**
- `registration_results.csv` - User registration data
- `order_results.csv` - Order placement data
- `cart_operations.csv` - Shopping cart operations
- `validation_results.csv` - Validation results
- `test_summary.csv` - Test execution summaries

---

## 📝 CSV File Structure

### registration_results.csv

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | When test ran | 2026-04-16 09:03:24 |
| Test Name | Name of test | test_user_registration |
| Status | PASS/FAIL | PASS |
| First Name | User's first name | William |
| Last Name | User's last name | Hunter |
| Email | User's email | deanna69@example.org |
| Phone | Phone number | 001-911-259-115 |
| Address | Street address | 77473 Howard Turnpike |
| City | City name | Nathanshire |
| Postcode | Postal code | 37728 |
| Login Name | Username | testuser_785346 |
| Password | Always hidden | ***HIDDEN*** |
| Error Message | Error if failed | (empty if passed) |

### order_results.csv

| Column | Description |
|--------|-------------|
| Timestamp | When test ran |
| Test Name | Name of test |
| Status | PASS/FAIL |
| Order ID | Order number |
| Customer Name | Customer name |
| Email | Customer email |
| Product Name | Product ordered |
| Quantity | Number of items |
| Unit Price | Price per item |
| Total Price | Total order amount |
| Payment Method | Payment type |
| Shipping Address | Delivery address |
| Order Status | Order state |
| Error Message | Error if failed |

### cart_operations.csv

| Column | Description |
|--------|-------------|
| Timestamp | When test ran |
| Test Name | Name of test |
| Status | PASS/FAIL |
| Operation | add/remove/update |
| Product Name | Product name |
| Quantity | Number of items |
| Price | Product price |
| Cart Total | Total cart value |
| Items in Cart | Number of items |
| Error Message | Error if failed |

### validation_results.csv

| Column | Description |
|--------|-------------|
| Timestamp | When test ran |
| Test Name | Name of test |
| Validation Type | What was validated |
| Expected | Expected value |
| Actual | Actual value |
| Status | PASS/FAIL |
| Notes | Additional info |

### test_summary.csv

| Column | Description |
|--------|-------------|
| Timestamp | When test ran |
| Test Name | Name of test |
| Test Type | Type of test |
| Duration (seconds) | How long it took |
| Status | PASS/FAIL |
| Details | Additional details |

---

## 🚀 How to Use CSV Logging

### Step 1: Import CSV Logger

```python
from framework.csv_logger import CSVLogger

# Initialize logger
csv_logger = CSVLogger()
```

### Step 2: Log Registration Data

```python
def test_user_registration(playwright_page):
    # ... your registration code ...
    
    # Prepare registration data
    registration_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "555-1234",
        "address": "123 Main St",
        "city": "New York",
        "postcode": "10001",
        "login_name": "johndoe",
        "password": "SecurePass123"
    }
    
    # Log to CSV
    csv_logger.log_registration(
        test_name="test_user_registration",
        registration_data=registration_data,
        status="PASS",  # or "FAIL"
        error_message=""  # or error details if failed
    )
```

### Step 3: Log Order Data

```python
def test_place_order(playwright_page):
    # ... your order code ...
    
    order_data = {
        "order_id": "ORD-12345",
        "customer_name": "John Doe",
        "email": "john@example.com",
        "product_name": "Skincare Product",
        "quantity": "2",
        "unit_price": "$25.00",
        "total_price": "$50.00",
        "payment_method": "Credit Card",
        "shipping_address": "123 Main St, New York, 10001",
        "order_status": "Confirmed"
    }
    
    csv_logger.log_order(
        test_name="test_place_order",
        order_data=order_data,
        status="PASS",
        error_message=""
    )
```

### Step 4: Log Cart Operations

```python
def test_add_to_cart(playwright_page):
    # ... your cart code ...
    
    cart_data = {
        "operation": "add",  # or "remove", "update"
        "product_name": "Skincare Product",
        "quantity": "1",
        "price": "$25.00",
        "cart_total": "$25.00",
        "items_count": "1"
    }
    
    csv_logger.log_cart_operation(
        test_name="test_add_to_cart",
        cart_data=cart_data,
        status="PASS",
        error_message=""
    )
```

### Step 5: Log Validations

```python
def test_email_validation(playwright_page):
    # ... your validation code ...
    
    csv_logger.log_validation(
        test_name="test_email_validation",
        validation_type="Email Format",
        expected="valid email format",
        actual="john@example.com",
        status="PASS",
        notes="Email format is valid"
    )
```

### Step 6: Log Test Summary

```python
import time

def test_example(playwright_page):
    start_time = time.time()
    
    # ... your test code ...
    
    duration = time.time() - start_time
    
    csv_logger.log_test_summary(
        test_name="test_example",
        test_type="User Registration",
        duration=round(duration, 2),
        status="PASS",
        details="User registered successfully"
    )
```

---

## 📊 Reading CSV Data

### Read All Data

```python
from framework.csv_logger import CSVLogger

csv_logger = CSVLogger()

# Read registration data
registrations = csv_logger.read_csv("registration_results.csv")

for reg in registrations:
    print(f"User: {reg['First Name']} {reg['Last Name']}")
    print(f"Email: {reg['Email']}")
    print(f"Status: {reg['Status']}")
    print("---")
```

### Get Summary Statistics

```python
# Get stats for registration tests
stats = csv_logger.get_summary_stats("registration_results.csv")

print(f"Total Tests: {stats['total']}")
print(f"Passed: {stats['passed']}")
print(f"Failed: {stats['failed']}")
print(f"Pass Rate: {stats['pass_rate']}")
```

**Output:**
```
Total Tests: 10
Passed: 8
Failed: 2
Pass Rate: 80.0%
```

---

## 🎯 Real-World Example

### Complete Test with CSV Logging

```python
import pytest
import time
from playwright.sync_api import expect
from faker import Faker
from framework.csv_logger import CSVLogger

fake = Faker()
csv_logger = CSVLogger()


@pytest.mark.playwright
def test_complete_user_journey_with_csv(playwright_page):
    """Complete user journey with CSV logging at each step."""
    page = playwright_page
    start_time = time.time()
    
    # Step 1: Register user
    registration_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number()[:15],
        "address": fake.street_address(),
        "city": fake.city(),
        "postcode": fake.postcode(),
        "login_name": f"user_{fake.random_number(digits=6)}",
        "password": "Test@123"
    }
    
    # ... registration code ...
    
    csv_logger.log_registration(
        test_name="test_complete_user_journey",
        registration_data=registration_data,
        status="PASS",
        error_message=""
    )
    
    # Step 2: Add product to cart
    cart_data = {
        "operation": "add",
        "product_name": "Skincare Product",
        "quantity": "2",
        "price": "$25.00",
        "cart_total": "$50.00",
        "items_count": "2"
    }
    
    csv_logger.log_cart_operation(
        test_name="test_complete_user_journey",
        cart_data=cart_data,
        status="PASS",
        error_message=""
    )
    
    # Step 3: Place order
    order_data = {
        "order_id": "ORD-12345",
        "customer_name": f"{registration_data['first_name']} {registration_data['last_name']}",
        "email": registration_data['email'],
        "product_name": "Skincare Product",
        "quantity": "2",
        "unit_price": "$25.00",
        "total_price": "$50.00",
        "payment_method": "Credit Card",
        "shipping_address": registration_data['address'],
        "order_status": "Confirmed"
    }
    
    csv_logger.log_order(
        test_name="test_complete_user_journey",
        order_data=order_data,
        status="PASS",
        error_message=""
    )
    
    # Step 4: Log test summary
    duration = time.time() - start_time
    csv_logger.log_test_summary(
        test_name="test_complete_user_journey",
        test_type="Complete User Journey",
        duration=round(duration, 2),
        status="PASS",
        details="User registered, added items to cart, and placed order successfully"
    )
    
    print("✅ Complete user journey logged to CSV files")
```

---

## 📈 Analyzing CSV Data

### Using Python

```python
import pandas as pd

# Read CSV with pandas
df = pd.read_csv("reports/csv/registration_results.csv")

# Get statistics
print(f"Total Registrations: {len(df)}")
print(f"Success Rate: {(df['Status'] == 'PASS').sum() / len(df) * 100:.1f}%")

# Group by status
print("\nBy Status:")
print(df['Status'].value_counts())

# Recent registrations
print("\nRecent 5 Registrations:")
print(df[['Timestamp', 'Login Name', 'Email', 'Status']].tail())
```

### Using Excel

1. Open `reports/csv/registration_results.csv` in Excel
2. Use filters to analyze data
3. Create pivot tables for summaries
4. Generate charts for visualization

---

## 🎓 Best Practices

### 1. Always Log Test Data

```python
# ✅ Good - Log both success and failure
try:
    # ... test code ...
    csv_logger.log_registration(..., status="PASS", error_message="")
except Exception as e:
    csv_logger.log_registration(..., status="FAIL", error_message=str(e))
    raise
```

### 2. Use Descriptive Test Names

```python
# ✅ Good
csv_logger.log_registration(
    test_name="test_user_registration_with_valid_data",
    ...
)

# ❌ Bad
csv_logger.log_registration(
    test_name="test1",
    ...
)
```

### 3. Log Validation Steps

```python
# Log each validation
csv_logger.log_validation(
    test_name="test_registration",
    validation_type="Email Format",
    expected="valid format",
    actual=email,
    status="PASS"
)

csv_logger.log_validation(
    test_name="test_registration",
    validation_type="Password Strength",
    expected="8+ chars with special char",
    actual=password,
    status="PASS"
)
```

### 4. Track Test Duration

```python
import time

start_time = time.time()
# ... test code ...
duration = time.time() - start_time

csv_logger.log_test_summary(
    test_name="test_example",
    test_type="Registration",
    duration=round(duration, 2),
    status="PASS",
    details="Completed in {duration:.2f}s"
)
```

### 5. Never Log Sensitive Data

```python
# ✅ Good - Password hidden
registration_data = {
    "login_name": "johndoe",
    "password": "SecurePass123"  # Will be replaced with ***HIDDEN***
}

# ❌ Bad - Don't log credit card numbers, SSN, etc.
order_data = {
    "credit_card": "1234-5678-9012-3456"  # DON'T DO THIS
}
```

---

## 🔧 Customization

### Custom CSV File Location

```python
# Use custom directory
csv_logger = CSVLogger(output_dir="my_reports/csv_data")
```

### Custom CSV Fields

Extend the CSVLogger class to add custom fields:

```python
class CustomCSVLogger(CSVLogger):
    def log_custom_data(self, test_name, custom_data, status):
        csv_file = self.output_dir / "custom_results.csv"
        # ... your custom implementation ...
```

---

## 📚 Summary

### What You Can Do Now

1. ✅ Log user registrations to CSV
2. ✅ Log order details to CSV
3. ✅ Log cart operations to CSV
4. ✅ Log validation results to CSV
5. ✅ Log test summaries to CSV
6. ✅ Read CSV data programmatically
7. ✅ Get summary statistics
8. ✅ Analyze data in Excel/Python

### CSV Files Location

All CSV files are in: `reports/csv/`

### Next Steps

1. Run tests with CSV logging
2. Open CSV files in Excel
3. Analyze test data
4. Create reports and dashboards
5. Track trends over time

---

**Happy Testing with CSV Logging!** 📊✨
