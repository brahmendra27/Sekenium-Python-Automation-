# 🎨 Allure Reporting - Complete Guide

**Beautiful, detailed test reports with graphs, charts, and complete test history**

---

## 📊 What is Allure?

Allure is a flexible, lightweight test reporting tool that provides:

- ✅ **Beautiful UI** - Modern, professional-looking reports
- ✅ **Detailed Test Steps** - See every action in your test
- ✅ **Screenshots** - Automatic screenshots at each step
- ✅ **Graphs & Charts** - Visual representation of test results
- ✅ **Test History** - Track trends over time
- ✅ **Categorization** - Group tests by feature, epic, story
- ✅ **Severity Levels** - Mark critical vs normal tests
- ✅ **Attachments** - Add logs, videos, files to reports
- ✅ **Test Parameters** - See test data used
- ✅ **Retries** - Track flaky tests

---

## 🚀 Quick Start

### Step 1: Install Allure (Already Done ✅)

```bash
pip install allure-pytest allure-python-commons
```

### Step 2: Install Allure Command-Line Tool

**Option A: Using Scoop (Windows - Recommended)**
```powershell
# Install Scoop if not installed
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

**Option B: Manual Download**
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract to `C:\allure`
3. Add `C:\allure\bin` to PATH

**Option C: Using npm**
```bash
npm install -g allure-commandline
```

### Step 3: Run Tests with Allure

```bash
# Run tests and generate Allure results
pytest tests/playwright/test_allure_demo.py --alluredir=reports/allure-results

# Generate and open Allure report
allure serve reports/allure-results
```

---

## 📝 Writing Tests with Allure

### Basic Test Structure

```python
import allure
import pytest

@allure.epic("E-Commerce")
@allure.feature("User Registration")
@allure.story("New User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "registration")
@pytest.mark.playwright
def test_user_registration(playwright_page):
    """Test user registration with Allure reporting."""
    
    with allure.step("Navigate to homepage"):
        page.goto("https://example.com")
        
        # Take screenshot
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="Homepage",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Fill registration form"):
        with allure.step("Enter email"):
            page.fill("#email", "test@example.com")
        
        with allure.step("Enter password"):
            page.fill("#password", "password123")
    
    with allure.step("Submit form"):
        page.click("#submit")
        
        # Attach test data
        allure.attach(
            "Email: test@example.com",
            name="Test Data",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## 🎯 Allure Features

### 1. Test Organization

#### Epics, Features, and Stories

```python
@allure.epic("E-Commerce Platform")  # High-level business requirement
@allure.feature("User Management")    # Feature within epic
@allure.story("User Registration")    # User story within feature
def test_example():
    pass
```

**Hierarchy:**
```
Epic: E-Commerce Platform
  ├── Feature: User Management
  │   ├── Story: User Registration
  │   ├── Story: User Login
  │   └── Story: Password Reset
  └── Feature: Shopping Cart
      ├── Story: Add to Cart
      └── Story: Checkout
```

### 2. Severity Levels

```python
@allure.severity(allure.severity_level.BLOCKER)   # Blocks testing
@allure.severity(allure.severity_level.CRITICAL)  # Critical functionality
@allure.severity(allure.severity_level.NORMAL)    # Normal functionality
@allure.severity(allure.severity_level.MINOR)     # Minor issues
@allure.severity(allure.severity_level.TRIVIAL)   # Cosmetic issues
```

### 3. Tags and Labels

```python
@allure.tag("smoke", "regression", "api")
@allure.label("owner", "QA Team")
@allure.label("layer", "ui")
@allure.label("browser", "chrome")
```

### 4. Links

```python
@allure.link("https://jira.company.com/PROJ-123", name="JIRA Ticket")
@allure.issue("PROJ-456", "Bug Report")
@allure.testcase("TC-789", "Test Case")
```

### 5. Test Steps

```python
with allure.step("Step 1: Navigate to page"):
    page.goto("https://example.com")
    
    with allure.step("Substep: Verify page loaded"):
        assert "Example" in page.title()
```

### 6. Attachments

#### Screenshots
```python
screenshot = page.screenshot()
allure.attach(
    screenshot,
    name="Page Screenshot",
    attachment_type=allure.attachment_type.PNG
)
```

#### Text
```python
allure.attach(
    "Test data: email=test@example.com",
    name="Test Data",
    attachment_type=allure.attachment_type.TEXT
)
```

#### HTML
```python
html_content = page.content()
allure.attach(
    html_content,
    name="Page HTML",
    attachment_type=allure.attachment_type.HTML
)
```

#### JSON
```python
import json

data = {"user": "john", "email": "john@example.com"}
allure.attach(
    json.dumps(data, indent=2),
    name="User Data",
    attachment_type=allure.attachment_type.JSON
)
```

#### CSV
```python
csv_content = "Name,Email\nJohn,john@example.com"
allure.attach(
    csv_content,
    name="Test Data",
    attachment_type=allure.attachment_type.CSV
)
```

### 7. Dynamic Properties

```python
def test_example(playwright_page):
    # Set title dynamically
    allure.dynamic.title("User Registration Test")
    
    # Set description dynamically
    allure.dynamic.description("This test verifies user registration")
    
    # Set tags dynamically
    allure.dynamic.tag("smoke")
    
    # Set severity dynamically
    allure.dynamic.severity(allure.severity_level.CRITICAL)
```

### 8. Parametrized Tests

```python
@pytest.mark.parametrize("username,password", [
    pytest.param("user1", "pass1", id="valid-credentials"),
    pytest.param("user2", "pass2", id="another-user"),
])
def test_login(playwright_page, username, password):
    allure.dynamic.title(f"Login with {username}")
    # ... test code ...
```

---

## 📊 Report Features

### 1. Overview Dashboard

- **Total tests** - Pass/Fail/Broken/Skipped
- **Success rate** - Percentage of passed tests
- **Duration** - Total execution time
- **Trend chart** - Historical pass/fail trends
- **Environment** - Test environment details

### 2. Test Suites

- Organized by package/module
- Shows all tests in each suite
- Pass/fail status for each test
- Duration for each test

### 3. Graphs

- **Status chart** - Pie chart of test statuses
- **Severity chart** - Tests by severity level
- **Duration chart** - Test execution times
- **Categories** - Tests by category
- **Features** - Tests by feature

### 4. Timeline

- Visual timeline of test execution
- Shows parallel execution
- Identifies bottlenecks
- Duration of each test

### 5. Behaviors

- Tests organized by Epic → Feature → Story
- Business-oriented view
- Easy to understand for non-technical stakeholders

### 6. Packages

- Tests organized by code structure
- Shows test distribution
- Helps identify test coverage gaps

### 7. Test Details

For each test, you can see:
- ✅ Test steps with descriptions
- ✅ Screenshots at each step
- ✅ Test parameters
- ✅ Attachments (logs, data, etc.)
- ✅ Execution time
- ✅ Error messages (if failed)
- ✅ Stack traces (if failed)
- ✅ Retry history (if retried)

---

## 🎨 Customization

### pytest.ini Configuration

```ini
[pytest]
# Allure options
addopts = 
    --alluredir=reports/allure-results
    --clean-alluredir
    --allure-no-capture

# Allure environment
allure_environment = 
    Browser=Chrome
    OS=Windows 10
    Environment=Test
```

### Environment Properties

Create `reports/allure-results/environment.properties`:

```properties
Browser=Chrome
Browser.Version=120.0
OS=Windows 10
Python.Version=3.10.4
Test.Environment=Staging
Application.URL=https://automationteststore.com
```

### Categories

Create `reports/allure-results/categories.json`:

```json
[
  {
    "name": "Product Defects",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*AssertionError.*"
  },
  {
    "name": "Test Defects",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*"
  },
  {
    "name": "Ignored Tests",
    "matchedStatuses": ["skipped"]
  }
]
```

---

## 🚀 Running Tests

### Basic Run

```bash
# Run all tests
pytest tests/ --alluredir=reports/allure-results

# Run specific test file
pytest tests/playwright/test_allure_demo.py --alluredir=reports/allure-results

# Run with markers
pytest tests/ -m smoke --alluredir=reports/allure-results
```

### Generate Report

```bash
# Option 1: Serve report (opens in browser)
allure serve reports/allure-results

# Option 2: Generate static report
allure generate reports/allure-results -o reports/allure-report --clean

# Option 3: Open existing report
allure open reports/allure-report
```

### Clean Old Results

```bash
# Clean before running
pytest tests/ --alluredir=reports/allure-results --clean-alluredir
```

---

## 📈 Advanced Features

### 1. Test Retries

```python
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_flaky():
    # Allure will show retry history
    pass
```

### 2. Test Fixtures

```python
@pytest.fixture
def test_data():
    data = {"user": "john", "email": "john@example.com"}
    
    allure.attach(
        json.dumps(data, indent=2),
        name="Test Fixture Data",
        attachment_type=allure.attachment_type.JSON
    )
    
    return data
```

### 3. Conditional Steps

```python
def test_example(playwright_page):
    with allure.step("Step 1"):
        result = some_function()
        
        if result:
            with allure.step("Step 1a: Success path"):
                # ... success code ...
                pass
        else:
            with allure.step("Step 1b: Failure path"):
                # ... failure code ...
                pass
```

### 4. Test Data Tables

```python
import allure
from allure_commons.types import AttachmentType

def test_example():
    # Create HTML table
    table_html = """
    <table>
        <tr><th>Name</th><th>Email</th><th>Status</th></tr>
        <tr><td>John</td><td>john@example.com</td><td>Active</td></tr>
        <tr><td>Jane</td><td>jane@example.com</td><td>Inactive</td></tr>
    </table>
    """
    
    allure.attach(
        table_html,
        name="User Data Table",
        attachment_type=AttachmentType.HTML
    )
```

---

## 🎯 Best Practices

### 1. Use Descriptive Step Names

```python
# ✅ Good
with allure.step("Enter email 'test@example.com' in login form"):
    page.fill("#email", "test@example.com")

# ❌ Bad
with allure.step("Fill field"):
    page.fill("#email", "test@example.com")
```

### 2. Take Screenshots at Key Points

```python
with allure.step("Submit form"):
    # Before
    screenshot = page.screenshot()
    allure.attach(screenshot, name="Before Submit", attachment_type=allure.attachment_type.PNG)
    
    page.click("#submit")
    
    # After
    screenshot = page.screenshot()
    allure.attach(screenshot, name="After Submit", attachment_type=allure.attachment_type.PNG)
```

### 3. Attach Test Data

```python
def test_example():
    test_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    
    allure.attach(
        json.dumps(test_data, indent=2),
        name="Test Input Data",
        attachment_type=allure.attachment_type.JSON
    )
```

### 4. Use Severity Appropriately

- **BLOCKER**: Blocks all testing
- **CRITICAL**: Core functionality
- **NORMAL**: Standard features
- **MINOR**: Minor features
- **TRIVIAL**: UI/cosmetic issues

### 5. Organize with Epics/Features/Stories

```python
# Organize by business value
@allure.epic("E-Commerce")
@allure.feature("Checkout")
@allure.story("Guest Checkout")
def test_guest_checkout():
    pass
```

---

## 📊 Report Examples

### Example 1: Registration Test Report

**Test:** User Registration  
**Status:** ✅ Passed  
**Duration:** 15.3s  
**Severity:** Critical

**Steps:**
1. ✅ Navigate to homepage (2.1s)
   - Screenshot: Homepage.png
2. ✅ Click 'Login or register' link (1.5s)
   - Screenshot: Login Page.png
3. ✅ Navigate to registration page (1.2s)
   - Screenshot: Registration Form.png
4. ✅ Fill registration form (5.3s)
   - Enter first name: John
   - Enter last name: Doe
   - Enter email: john@example.com
   - Screenshot: Filled Form.png
5. ✅ Submit registration form (3.1s)
   - Screenshot: After Submission.png
6. ✅ Verify registration success (2.1s)
   - Screenshot: Success Page.png

**Attachments:**
- Test Data.txt
- Homepage.png
- Login Page.png
- Registration Form.png
- Filled Form.png
- After Submission.png
- Success Page.png

---

## 🔧 Troubleshooting

### Issue: Allure command not found

**Solution:**
```powershell
# Install via Scoop
scoop install allure

# Or add to PATH manually
$env:PATH += ";C:\allure\bin"
```

### Issue: No test results

**Solution:**
```bash
# Make sure --alluredir is specified
pytest tests/ --alluredir=reports/allure-results

# Check if results directory exists
ls reports/allure-results
```

### Issue: Report not opening

**Solution:**
```bash
# Try generating static report first
allure generate reports/allure-results -o reports/allure-report --clean

# Then open
allure open reports/allure-report
```

---

## 📚 Additional Resources

- **Official Docs**: https://docs.qameta.io/allure/
- **GitHub**: https://github.com/allure-framework/allure-python
- **Examples**: https://github.com/allure-examples

---

## 🎉 Summary

### What You Get with Allure:

1. ✅ **Beautiful Reports** - Professional, modern UI
2. ✅ **Detailed Steps** - See every action
3. ✅ **Screenshots** - Visual proof of test execution
4. ✅ **Graphs & Charts** - Visual analytics
5. ✅ **Test History** - Track trends over time
6. ✅ **Categorization** - Organize by epic/feature/story
7. ✅ **Attachments** - Logs, data, files
8. ✅ **Parameters** - See test data
9. ✅ **Retries** - Track flaky tests
10. ✅ **Timeline** - Execution timeline

### Next Steps:

1. Install Allure command-line tool
2. Run tests with `--alluredir`
3. Generate report with `allure serve`
4. Explore the beautiful reports!

---

**Happy Testing with Allure!** 🎨✨
