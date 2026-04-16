# 🎯 Complete Guide: Hooks and Steering Files

**Framework:** Test Automation Framework v0.2.0  
**Purpose:** Automate workflows and provide context-aware guidance

---

## 📚 Table of Contents

1. [What are Hooks?](#what-are-hooks)
2. [What are Steering Files?](#what-are-steering-files)
3. [How to Use Hooks](#how-to-use-hooks)
4. [How to Use Steering Files](#how-to-use-steering-files)
5. [Real-World Examples](#real-world-examples)
6. [Best Practices](#best-practices)

---

## 🪝 What are Hooks?

**Hooks** are automated triggers that execute actions when specific events occur in your IDE or testing workflow.

### Key Concepts

- **Event-Driven**: Hooks respond to events (file saved, test failed, etc.)
- **Automated**: No manual intervention needed
- **Customizable**: You define what happens when events occur

### Hook Types

| Event Type | When It Triggers | Use Case |
|------------|------------------|----------|
| `fileEdited` | When you save a file | Auto-run linter, format code |
| `fileCreated` | When you create a new file | Auto-add headers, templates |
| `fileDeleted` | When you delete a file | Clean up related files |
| `promptSubmit` | When you send a message to Kiro | Log conversations, track requests |
| `agentStop` | When Kiro finishes a task | Generate reports, notify team |
| `preToolUse` | Before Kiro uses a tool | Validate permissions, log actions |
| `postToolUse` | After Kiro uses a tool | Verify results, update logs |
| `preTaskExecution` | Before a spec task starts | Check prerequisites, backup files |
| `postTaskExecution` | After a spec task completes | Run tests, update documentation |
| `userTriggered` | When you manually trigger | Run on-demand scripts |

### Hook Actions

1. **`askAgent`**: Send a message to Kiro
   - Example: "Review this code for security issues"
   
2. **`runCommand`**: Execute a shell command
   - Example: `npm run lint`, `pytest tests/`

---

## 📋 What are Steering Files?

**Steering files** provide additional context and instructions to Kiro for specific situations.

### Key Concepts

- **Context-Aware**: Provide relevant information when needed
- **Automatic**: Kiro loads them based on conditions
- **Flexible**: Can be always-on, conditional, or manual

### Steering File Types

| Inclusion Type | When Loaded | Use Case |
|----------------|-------------|----------|
| **Always** | Every conversation | Team standards, coding guidelines |
| **Conditional** | When specific files are read | File-specific instructions |
| **Manual** | When you reference with `#` | On-demand guidance |

### Location

All steering files are stored in: `.kiro/steering/`

---

## 🎯 How to Use Hooks

### Method 1: Using Kiro (Easiest)

Just tell Kiro what you want:

```
"Create a hook that runs tests whenever I save a Python file"
"Add a hook to lint my code when I save TypeScript files"
"Create a hook that asks you to review my code before committing"
```

Kiro will create the hook file for you!

### Method 2: Manual Creation

#### Step 1: Create Hook File

Location: `.kiro/hooks/my-hook-name.kiro.hook`

#### Step 2: Define Hook Structure

```json
{
  "name": "Run Tests on Save",
  "version": "1.0.0",
  "description": "Automatically run tests when test files are saved",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "pytest tests/ -v"
  }
}
```

#### Step 3: Save and Test

The hook activates automatically!

### Hook Examples

#### Example 1: Auto-Lint on Save

```json
{
  "name": "Auto Lint Python Files",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.py", "tests/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "pylint ${file}"
  }
}
```

#### Example 2: Ask Kiro to Review Code

```json
{
  "name": "Code Review on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this code for bugs, security issues, and best practices"
  }
}
```

#### Example 3: Run Tests After Task Completion

```json
{
  "name": "Test After Task",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "runCommand",
    "command": "pytest tests/ -v"
  }
}
```

#### Example 4: CSV Logging Hook

```json
{
  "name": "Log Test Results to CSV",
  "version": "1.0.0",
  "description": "Automatically log test results to CSV after test execution",
  "when": {
    "type": "postToolUse",
    "toolTypes": ["shell"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Parse the test results and log them to CSV using the CSVLogger"
  }
}
```

---

## 📝 How to Use Steering Files

### Method 1: Using Kiro (Easiest)

Just tell Kiro:

```
"Add a steering file with our Python coding standards"
"Create a steering file for test writing guidelines"
"Add a steering file that loads when I work on API files"
```

### Method 2: Manual Creation

#### Step 1: Create Steering File

Location: `.kiro/steering/my-guideline.md`

#### Step 2: Add Front Matter (Optional)

```markdown
---
inclusion: fileMatch
fileMatchPattern: "tests/**/*.py"
---

# Test Writing Guidelines

When writing tests:
1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. One assertion per test
...
```

#### Step 3: Write Content

The rest of the file is regular Markdown with your guidelines.

### Steering File Examples

#### Example 1: Always-Included Standards

**File:** `.kiro/steering/coding-standards.md`

```markdown
# Python Coding Standards

## Naming Conventions
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_CASE

## Documentation
- All functions must have docstrings
- Use Google-style docstrings

## Testing
- Minimum 80% code coverage
- All tests must pass before commit
```

#### Example 2: Conditional (File-Specific)

**File:** `.kiro/steering/api-guidelines.md`

```markdown
---
inclusion: fileMatch
fileMatchPattern: "**/api/**/*.py"
---

# API Development Guidelines

## When working on API files:

1. **Authentication**: All endpoints require authentication
2. **Validation**: Validate all input parameters
3. **Error Handling**: Return proper HTTP status codes
4. **Documentation**: Update OpenAPI spec
```

#### Example 3: Manual (On-Demand)

**File:** `.kiro/steering/security-checklist.md`

```markdown
---
inclusion: manual
---

# Security Review Checklist

Use this when reviewing code for security:

- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Authentication on sensitive endpoints
- [ ] Authorization checks
- [ ] Secrets not hardcoded
- [ ] HTTPS only
- [ ] Rate limiting implemented
```

**Usage:** In chat, type `#security-checklist` to load it.

---

## 🌟 Real-World Examples

### Example 1: CSV Logging Workflow

**Goal:** Automatically log test results to CSV after every test run

#### Hook: `.kiro/hooks/csv-logger.kiro.hook`

```json
{
  "name": "CSV Test Logger",
  "version": "1.0.0",
  "description": "Log test results to CSV after test execution",
  "when": {
    "type": "postToolUse",
    "toolTypes": ["shell"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "If the command was a pytest run, parse the results and log to CSV using CSVLogger"
  }
}
```

#### Steering File: `.kiro/steering/csv-logging-guide.md`

```markdown
# CSV Logging Guidelines

## When to Log

Log to CSV for:
- User registrations (registration_results.csv)
- Order placements (order_results.csv)
- Cart operations (cart_operations.csv)
- Validation results (validation_results.csv)

## How to Log

```python
from framework.csv_logger import CSVLogger

csv_logger = CSVLogger()

# Log registration
csv_logger.log_registration(
    test_name="test_user_registration",
    registration_data={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        ...
    },
    status="PASS",
    error_message=""
)
```

## CSV File Locations

All CSV files are saved to: `reports/csv/`
```

### Example 2: Test Quality Enforcement

**Goal:** Ensure all tests follow best practices

#### Hook: `.kiro/hooks/test-quality-check.kiro.hook`

```json
{
  "name": "Test Quality Check",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this test file and check: 1) Descriptive test names, 2) Proper docstrings, 3) Clear assertions, 4) No hardcoded values"
  }
}
```

#### Steering File: `.kiro/steering/test-standards.md`

```markdown
---
inclusion: fileMatch
fileMatchPattern: "tests/**/*.py"
---

# Test Writing Standards

## Test Structure

Every test must follow AAA pattern:
```python
def test_example():
    # Arrange: Set up test data
    user = create_test_user()
    
    # Act: Perform the action
    result = user.login()
    
    # Assert: Verify the outcome
    assert result.success == True
```

## Test Naming

- Start with `test_`
- Use descriptive names: `test_user_login_with_valid_credentials`
- Not: `test_login` or `test1`

## Docstrings

Every test needs a docstring:
```python
def test_example():
    """
    TC-001: Test description.
    
    Steps:
    1. Step 1
    2. Step 2
    
    Expected: Expected result
    """
```
```

### Example 3: Registration Data Tracking

**Goal:** Track all user registrations in CSV for analysis

#### Test with CSV Logging

```python
from framework.csv_logger import CSVLogger

csv_logger = CSVLogger()

def test_user_registration(playwright_page):
    # ... registration code ...
    
    # Log to CSV
    csv_logger.log_registration(
        test_name="test_user_registration",
        registration_data={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "postcode": postcode,
            "login_name": login_name,
            "password": "***HIDDEN***"
        },
        status="PASS" if success else "FAIL",
        error_message=error_msg if not success else ""
    )
```

#### Hook to Generate Summary

```json
{
  "name": "Registration Summary",
  "version": "1.0.0",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Generate a summary of registration_results.csv showing total registrations, pass rate, and any failures"
  }
}
```

---

## 💡 Best Practices

### Hooks

1. **Keep Commands Fast**
   - Hooks run automatically, so use quick commands
   - For slow operations, use `userTriggered` type

2. **Use Specific Patterns**
   - Good: `tests/**/*.py`
   - Bad: `**/*` (too broad)

3. **Test Your Hooks**
   - Create a test file and trigger the hook
   - Verify it does what you expect

4. **Don't Overuse**
   - Too many hooks can slow down your workflow
   - Start with 2-3 essential hooks

### Steering Files

1. **Be Specific**
   - Provide clear, actionable guidelines
   - Include examples

2. **Keep Updated**
   - Review and update regularly
   - Remove outdated information

3. **Use Conditional Loading**
   - Don't load everything always
   - Use `fileMatch` for file-specific guidance

4. **Reference External Docs**
   - Link to full documentation
   - Keep steering files concise

---

## 🎓 Common Use Cases

### Use Case 1: Automated Testing Workflow

```json
// .kiro/hooks/auto-test.kiro.hook
{
  "name": "Auto Test on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py", "framework/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "pytest tests/ -v --tb=short"
  }
}
```

### Use Case 2: Code Review Automation

```json
// .kiro/hooks/code-review.kiro.hook
{
  "name": "Auto Code Review",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this code for: 1) Bugs, 2) Security issues, 3) Performance problems, 4) Best practices"
  }
}
```

### Use Case 3: CSV Data Tracking

```python
# In your test file
from framework.csv_logger import CSVLogger

csv_logger = CSVLogger()

# Log every important operation
csv_logger.log_registration(...)
csv_logger.log_order(...)
csv_logger.log_cart_operation(...)
csv_logger.log_validation(...)
```

### Use Case 4: Documentation Updates

```json
// .kiro/hooks/update-docs.kiro.hook
{
  "name": "Update Documentation",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Update the README.md with any new features or changes from this task"
  }
}
```

---

## 📊 CSV Logging Integration

### Available CSV Loggers

```python
from framework.csv_logger import CSVLogger

csv_logger = CSVLogger()

# 1. Log Registration
csv_logger.log_registration(test_name, registration_data, status, error_message)

# 2. Log Order
csv_logger.log_order(test_name, order_data, status, error_message)

# 3. Log Cart Operation
csv_logger.log_cart_operation(test_name, cart_data, status, error_message)

# 4. Log Validation
csv_logger.log_validation(test_name, validation_type, expected, actual, status, notes)

# 5. Log Test Summary
csv_logger.log_test_summary(test_name, test_type, duration, status, details)
```

### CSV File Locations

All CSV files are saved to: `reports/csv/`

- `registration_results.csv` - User registration data
- `order_results.csv` - Order placement data
- `cart_operations.csv` - Shopping cart operations
- `validation_results.csv` - Validation results
- `test_summary.csv` - Test execution summaries

### Reading CSV Data

```python
# Read CSV file
data = csv_logger.read_csv("registration_results.csv")

# Get summary statistics
stats = csv_logger.get_summary_stats("registration_results.csv")
print(f"Total: {stats['total']}")
print(f"Passed: {stats['passed']}")
print(f"Failed: {stats['failed']}")
print(f"Pass Rate: {stats['pass_rate']}")
```

---

## 🚀 Quick Start

### 1. Create Your First Hook

Tell Kiro:
```
"Create a hook that runs pytest whenever I save a test file"
```

### 2. Create Your First Steering File

Tell Kiro:
```
"Create a steering file with our test writing guidelines"
```

### 3. Use CSV Logging

Tell Kiro:
```
"Update my registration test to log results to CSV"
```

### 4. View Your Hooks

- Open VS Code Explorer
- Look for "Agent Hooks" section
- Click to view/edit hooks

### 5. View Your Steering Files

- Navigate to `.kiro/steering/`
- Open any `.md` file to view/edit

---

## 📚 Additional Resources

- **Framework Documentation**: `README.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Kiro Integration FAQ**: `KIRO_INTEGRATION_FAQ.md`
- **CSV Logger API**: `framework/csv_logger.py`

---

## 💬 Getting Help

### Ask Kiro!

- "Show me my current hooks"
- "Create a hook for [specific task]"
- "Add a steering file for [specific guidance]"
- "How do I log test results to CSV?"
- "Show me examples of hooks"

Kiro will help you create, modify, and understand hooks and steering files!

---

**Happy Automating!** 🎉
