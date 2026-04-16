# CSV Logging Guide - Test Automation Framework

**Feature:** Automatic CSV logging of test data and validation results  
**Version:** 1.0.0  
**Date:** April 16, 2026

---

## 📊 Overview

The framework now automatically logs test data and validation results to CSV files for easy analysis, reporting, and record-keeping.

### CSV Files Generated

| CSV File | Purpose | Location |
|----------|---------|----------|
| `user_registrations.csv` | User registration details | `reports/csv/` |
| `order_details.csv` | Order information | `reports/csv/` |
| `cart_details.csv` | Shopping cart data | `reports/csv/` |
| `validation_results.csv` | Test validation results | `reports/csv/` |

---

## 🎯 What Gets Logged

### 1. User Registrations (`user_registrations.csv`)

**Columns:**
- Timestamp
- First Name
- Last Name
- Email
- Login Name
- Telephone
- Address
- City
- Postcode
- Country
- Validation Result (Success/Failed)
- Error Message

**Example Data:**
```csv
Timestamp,First Name,Last Name,Email,Login Name,Telephone,Address,City,Postcode,Country,Validation Result,Error Message
2026-04-16 08:14:47,Brian,Martin,david66@example.net,testuser_569499,208-244-7973x60,3623 Riggs Mall,North Kristina,48043,United States,Success,
```

**Use Cases:**
- Track all test user accounts created
- Verify registration success rates
- Audit test data for compliance
- Debug registration failures

---

### 2. Order Details (`order_details.csv`)

**Columns:**
- Timestamp
- Order ID
- Customer Name
- Customer Email
- Product Names
- Quantities
- Unit Prices
- Total Amount
- Payment Method
- Shipping Address
- Order Status
- Validation Result (Success/Failed)
- Error Message

**Example Data:**
```csv
Timestamp,Order ID,Customer Name,Customer Email,Product Names,Quantities,Unit Prices,Total Amount,Payment Method,Shipping Address,Order Status,Validation Result,Error Message
2026-04-16 08:23:18,TEST_ORDER_2981f455,Guest User,guest@test.com,SKINSHEEN BRONZER STICK,1,$31.50,$31.50,Guest Checkout,Test Address,Initiated,Failed,Did not reach checkout page
```

**Use Cases:**
- Track test orders
- Verify order processing
- Analyze order totals
- Debug checkout issues

---

### 3. Cart Details (`cart_details.csv`)

**Columns:**
- Timestamp
- Session ID
- Product Names
- Quantities
- Unit Prices
- Subtotal
- Tax
- Shipping
- Total
- Validation Result (Success/Failed)
- Error Message

**Example Data:**
```csv
Timestamp,Session ID,Product Names,Quantities,Unit Prices,Subtotal,Tax,Shipping,Total,Validation Result,Error Message
2026-04-16 08:23:00,test_session_79a1c4a5,SKINSHEEN BRONZER STICK,1,$29.50,N/A,N/A,N/A,$31.50,Success,
```

**Use Cases:**
- Track cart operations
- Verify price calculations
- Analyze cart abandonment
- Debug cart issues

---

### 4. Validation Results (`validation_results.csv`)

**Columns:**
- Timestamp
- Test Name
- Validation Type
- Expected Value
- Actual Value
- Result (Pass/Fail)
- Details

**Example Data:**
```csv
Timestamp,Test Name,Validation Type,Expected Value,Actual Value,Result,Details
2026-04-16 08:23:00,test_add_to_cart_with_validation_logging,Cart Item Count,> 0,9,Pass,Cart contains 9 item(s)
2026-04-16 08:23:18,test_checkout_with_order_logging,Checkout Navigation,checkout page,https://automationteststore.com/index.php?rt=account/login,Fail,Failed to navigate to checkout
```

**Use Cases:**
- Track validation pass/fail rates
- Identify failing validations
- Debug test failures
- Generate validation reports

---

## 🚀 How to Use CSV Logging

### In Your Tests

#### 1. Import the CSV Logger

```python
from framework.csv_logger import get_csv_logger

# Initialize logger
csv_logger = get_csv_logger()
```

#### 2. Log Registration Data

```python
# Prepare registration data
registration_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "login_name": "johndoe123",
    "telephone": "555-1234",
    "address": "123 Main St",
    "city": "New York",
    "postcode": "10001",
    "country": "United States"
}

# Log to CSV
csv_logger.write_registration(
    registration_data=registration_data,
    validation_result="Success",
    error_message=""
)
```

#### 3. Log Order Data

```python
# Prepare order data
order_data = {
    "order_id": "ORD-12345",
    "customer_name": "John Doe",
    "customer_email": "john.doe@example.com",
    "product_names": "Product A | Product B",
    "quantities": "2 | 1",
    "unit_prices": "$10.00 | $20.00",
    "total_amount": "$40.00",
    "payment_method": "Credit Card",
    "shipping_address": "123 Main St, New York, NY 10001",
    "order_status": "Completed"
}

# Log to CSV
csv_logger.write_order(
    order_data=order_data,
    validation_result="Success",
    error_message=""
)
```

#### 4. Log Cart Details

```python
# Prepare cart data
cart_data = {
    "session_id": "session_12345",
    "product_names": "Product A | Product B",
    "quantities": "2 | 1",
    "unit_prices": "$10.00 | $20.00",
    "subtotal": "$40.00",
    "tax": "$3.20",
    "shipping": "$5.00",
    "total": "$48.20"
}

# Log to CSV
csv_logger.write_cart_details(
    cart_data=cart_data,
    validation_result="Success",
    error_message=""
)
```

#### 5. Log Validation Results

```python
# Log validation
csv_logger.write_validation(
    test_name="test_price_calculation",
    validation_type="Price Calculation",
    expected_value="$40.00",
    actual_value="$40.00",
    result="Pass",
    details="Unit price × quantity matches total"
)
```

---

## 📈 Analyzing CSV Data

### Method 1: Open in Excel/Google Sheets

```bash
# Open CSV file in Excel (Windows)
start reports\csv\user_registrations.csv

# Open in default application
explorer reports\csv\
```

### Method 2: Use Python Analysis Script

```bash
# Run analysis script
python analyze_csv_reports.py
```

**Output:**
```
================================================================================
📊 OVERALL TEST SUMMARY REPORT
================================================================================

📁 CSV Files Generated:
   - user_registrations.csv: 1 records
   - order_details.csv: 1 records
   - validation_results.csv: 3 records
   - cart_details.csv: 1 records

✅ Registration Success Rate: 100.0%
✅ Validation Pass Rate: 33.3%

📂 CSV files location: reports/csv/
```

### Method 3: Use Pandas for Custom Analysis

```python
import pandas as pd

# Read CSV
df = pd.read_csv('reports/csv/user_registrations.csv')

# Analyze
print(f"Total Registrations: {len(df)}")
print(f"Success Rate: {len(df[df['Validation Result'] == 'Success']) / len(df) * 100:.1f}%")

# Filter by date
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
today = df[df['Timestamp'].dt.date == pd.Timestamp.now().date()]
print(f"Registrations Today: {len(today)}")
```

---

## 🎓 Example Test with CSV Logging

```python
import pytest
from playwright.sync_api import expect
from faker import Faker
from framework.csv_logger import get_csv_logger

fake = Faker()
csv_logger = get_csv_logger()

@pytest.mark.playwright
def test_user_registration_with_logging(playwright_page):
    """Test user registration with CSV logging."""
    page = playwright_page
    
    # Generate test data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    login_name = f"testuser_{fake.random_number(digits=6)}"
    
    # Prepare data for logging
    registration_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "login_name": login_name,
        "telephone": fake.phone_number()[:15],
        "address": fake.street_address(),
        "city": fake.city(),
        "postcode": fake.postcode(),
        "country": "United States"
    }
    
    # Navigate and fill form
    page.goto("https://automationteststore.com/")
    page.get_by_text("Login or register").click()
    page.locator("button:has-text('Continue')").first.click()
    
    # Fill registration form
    page.fill("#AccountFrm_firstname", first_name)
    page.fill("#AccountFrm_lastname", last_name)
    page.fill("#AccountFrm_email", email)
    # ... fill other fields ...
    
    # Submit
    page.locator("button[type='submit']:has-text('Continue')").click()
    page.wait_for_load_state("networkidle")
    
    # Verify and log
    if "account/success" in page.url or "account/account" in page.url:
        csv_logger.write_registration(
            registration_data=registration_data,
            validation_result="Success",
            error_message=""
        )
        print(f"✅ Registration successful: {login_name}")
    else:
        csv_logger.write_registration(
            registration_data=registration_data,
            validation_result="Failed",
            error_message=f"Registration failed. URL: {page.url}"
        )
        assert False, "Registration failed"
```

---

## 📊 CSV File Features

### Automatic Features

✅ **Automatic Timestamps** - Every record includes timestamp  
✅ **Automatic Headers** - Headers written on first write  
✅ **Append Mode** - New records added without overwriting  
✅ **UTF-8 Encoding** - Supports international characters  
✅ **Error Handling** - Gracefully handles missing data  

### File Management

```python
from framework.csv_logger import get_csv_logger

csv_logger = get_csv_logger()

# Read CSV data
data = csv_logger.read_csv("user_registrations")
print(f"Total records: {len(data)}")

# Clear CSV file
csv_logger.clear_csv("user_registrations")
print("CSV file cleared")

# Custom CSV
csv_logger.write_custom(
    filename="custom_data",
    headers=["Timestamp", "Test Name", "Result"],
    data={"Test Name": "My Test", "Result": "Pass"}
)
```

---

## 🎯 Best Practices

### 1. Log at Key Points

```python
# ✅ Good - Log after verification
if registration_successful:
    csv_logger.write_registration(data, "Success", "")
else:
    csv_logger.write_registration(data, "Failed", error_msg)

# ❌ Bad - Log before verification
csv_logger.write_registration(data, "Success", "")
# ... then test fails
```

### 2. Include Error Messages

```python
# ✅ Good - Descriptive error
csv_logger.write_registration(
    data, 
    "Failed", 
    "Email validation failed: Invalid format"
)

# ❌ Bad - No error details
csv_logger.write_registration(data, "Failed", "")
```

### 3. Use Consistent Formats

```python
# ✅ Good - Consistent format
product_names = "Product A | Product B | Product C"
quantities = "1 | 2 | 1"

# ❌ Bad - Inconsistent format
product_names = "Product A, Product B; Product C"
quantities = "1 2 1"
```

### 4. Log Validations Separately

```python
# ✅ Good - Separate validation logging
csv_logger.write_cart_details(cart_data, "Success", "")
csv_logger.write_validation(
    "test_cart", 
    "Price Calculation", 
    "$40.00", 
    "$40.00", 
    "Pass"
)

# ❌ Bad - Mixed logging
csv_logger.write_cart_details(
    cart_data, 
    "Success", 
    "Price calculation passed"
)
```

---

## 📁 File Locations

```
reports/
└── csv/
    ├── user_registrations.csv
    ├── order_details.csv
    ├── cart_details.csv
    ├── validation_results.csv
    └── custom_data.csv (if created)
```

---

## 🔧 Configuration

### Change Output Directory

```python
# Default: reports/csv
csv_logger = get_csv_logger()

# Custom directory
csv_logger = get_csv_logger(output_dir="test_results/csv_logs")
```

### Custom CSV Files

```python
# Create custom CSV with your own structure
csv_logger.write_custom(
    filename="performance_metrics",
    headers=["Timestamp", "Test Name", "Duration", "Memory Usage"],
    data={
        "Test Name": "test_homepage_load",
        "Duration": "2.5s",
        "Memory Usage": "45MB"
    }
)
```

---

## 📊 Sample Reports

### Registration Success Rate Report

```python
import pandas as pd

df = pd.read_csv('reports/csv/user_registrations.csv')
success_rate = len(df[df['Validation Result'] == 'Success']) / len(df) * 100

print(f"Registration Success Rate: {success_rate:.1f}%")
print(f"Total Registrations: {len(df)}")
print(f"Successful: {len(df[df['Validation Result'] == 'Success'])}")
print(f"Failed: {len(df[df['Validation Result'] == 'Failed'])}")
```

### Validation Pass Rate Report

```python
import pandas as pd

df = pd.read_csv('reports/csv/validation_results.csv')
pass_rate = len(df[df['Result'] == 'Pass']) / len(df) * 100

print(f"Validation Pass Rate: {pass_rate:.1f}%")
print(f"\nBy Validation Type:")
print(df.groupby(['Validation Type', 'Result']).size())
```

---

## 🎉 Benefits

✅ **Easy Analysis** - Open in Excel, Google Sheets, or Python  
✅ **Historical Data** - Track trends over time  
✅ **Debugging** - Quickly identify failures  
✅ **Reporting** - Generate reports for stakeholders  
✅ **Compliance** - Audit trail of test data  
✅ **Integration** - Import into BI tools  

---

## 📚 Related Files

- `framework/csv_logger.py` - CSV logging implementation
- `tests/playwright/test_user_registration.py` - Registration tests with CSV logging
- `tests/playwright/test_cart_with_csv.py` - Cart tests with CSV logging
- `analyze_csv_reports.py` - Analysis script

---

## 🚀 Quick Start

1. **Run tests** (CSV files generated automatically):
   ```bash
   pytest tests/playwright/test_user_registration.py -v
   pytest tests/playwright/test_cart_with_csv.py -v
   ```

2. **View CSV files**:
   ```bash
   start reports\csv\user_registrations.csv
   ```

3. **Analyze data**:
   ```bash
   python analyze_csv_reports.py
   ```

---

**Happy Testing with CSV Logging!** 📊✅
