---
title: Test Automation Framework Overview
description: Comprehensive guide to the framework structure, configuration, fixtures, CLI options, reports, and hooks
inclusion: auto
keywords: [framework, structure, configuration, fixtures, reports, hooks, setup, overview]
---

# Test Automation Framework Overview

## Introduction

The Test Automation Framework is a unified Python-based testing solution that enables QE teams to author, execute, and report on automated browser tests using both Selenium WebDriver and Playwright. This document provides a comprehensive overview of the framework's structure, available features, configuration options, and integration points.

## Project Structure

```
test-automation-framework/
├── .github/
│   └── workflows/
│       └── test.yml                 # GitHub Actions CI pipeline
├── .kiro/
│   ├── hooks/                       # Kiro IDE automation hooks
│   ├── specs/                       # Feature specifications
│   └── steering/                    # Kiro IDE steering files
│       ├── test-writing-guide.md    # Guide for writing tests
│       ├── framework-overview.md    # This file
│       └── docker-execution.md      # Docker build and run guide
├── tests/
│   ├── selenium/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Selenium fixtures
│   │   └── test_example_selenium.py # Example Selenium test
│   ├── playwright/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Playwright fixtures
│   │   └── test_example_playwright.py # Example Playwright test
│   └── conftest.py                  # Shared pytest fixtures and hooks
├── framework/
│   ├── __init__.py
│   ├── config.py                    # Configuration loader
│   ├── selenium_driver.py           # Selenium WebDriver wrapper
│   ├── playwright_driver.py         # Playwright browser wrapper
│   └── report_utils.py              # Report generation utilities
├── reports/                         # Generated test reports (gitignored)
│   ├── report.html                  # HTML test report
│   ├── report.json                  # JSON test report
│   ├── screenshots/                 # Test failure screenshots
│   └── traces/                      # Playwright trace files
├── docker/
│   ├── Dockerfile                   # Docker image definition
│   └── docker-compose.yml           # Docker Compose service
├── config.yaml                      # Central configuration file
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # pytest configuration
├── .gitignore                       # Git ignore rules
├── README.md                        # Setup and usage documentation
├── CONTRIBUTING.md                  # Contribution guidelines
└── CHANGELOG.md                     # Version history
```

### Key Directories

- **`tests/`**: All test files organized by driver type (selenium, playwright)
- **`framework/`**: Core framework components (config, drivers, utilities)
- **`reports/`**: Generated test reports, screenshots, and traces (not committed to git)
- **`.kiro/`**: Kiro IDE integration files (steering files and hooks)
- **`docker/`**: Docker containerization files for reproducible test execution

## Available Fixtures

The framework provides pytest fixtures for both Selenium and Playwright test execution.

### Selenium Fixtures

#### `selenium_driver`

**Location**: `tests/selenium/conftest.py`

**Scope**: Function (new driver instance per test)

**Description**: Provides a fully configured Selenium WebDriver instance with automatic screenshot capture on test failure.

**Features**:
- Initializes WebDriver based on `config.yaml` settings
- Sets implicit wait and page load timeout from configuration
- Captures screenshot on test failure and attaches to HTML report
- Automatically tears down driver after test completion

**Usage**:
```python
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.selenium
def test_example(selenium_driver):
    driver = selenium_driver
    driver.get("https://example.com")
    assert "Example" in driver.title
```

### Playwright Fixtures

#### `playwright_context`

**Location**: `tests/playwright/conftest.py`

**Scope**: Function (new context per test)

**Description**: Provides a Playwright browser context with tracing support and automatic trace file capture on test failure.

**Features**:
- Initializes browser context based on `config.yaml` settings
- Starts tracing with screenshots and snapshots if enabled
- Saves trace file on test failure for post-mortem debugging
- Automatically tears down context and browser after test completion

**Usage**:
```python
import pytest

@pytest.mark.playwright
def test_example(playwright_context):
    page = playwright_context.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    page.close()
```

#### `playwright_page`

**Location**: `tests/playwright/conftest.py`

**Scope**: Function (new page per test)

**Description**: Provides a Playwright page instance with automatic screenshot capture on test failure.

**Features**:
- Creates new page from browser context
- Captures screenshot on test failure and attaches to HTML report
- Automatically closes page after test completion

**Usage**:
```python
import pytest

@pytest.mark.playwright
def test_example(playwright_page):
    page = playwright_page
    page.goto("https://example.com")
    assert "Example" in page.title()
```

## Configuration Options

### Configuration File: `config.yaml`

The framework uses a central YAML configuration file for all settings. Configuration values can be overridden via command-line options.

#### Available Configuration Options

```yaml
# Base URL for application under test
base_url: "http://localhost:8080"

# Browser selection
# Selenium: chrome, firefox
# Playwright: chromium, firefox, webkit
browser: "chrome"

# Headless mode: true for CI, false for local debugging
headless: false

# Default timeout for element waits (seconds)
timeout: 30

# Number of parallel workers for pytest-xdist (1 = sequential)
parallel_workers: 1

# Report output directory
report_dir: "reports"

# Selenium-specific settings
selenium:
  implicit_wait: 10          # Implicit wait timeout (seconds)
  page_load_timeout: 60      # Page load timeout (seconds)

# Playwright-specific settings
playwright:
  slow_mo: 0                 # Slow down operations by N milliseconds
  tracing: true              # Enable tracing on failure
```

#### Configuration Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `base_url` | string | `http://localhost:8080` | Base URL for application under test |
| `browser` | string | `chrome` | Browser selection (chrome, firefox, chromium, webkit) |
| `headless` | boolean | `false` | Run browsers in headless mode |
| `timeout` | integer | `30` | Default timeout for element waits (seconds) |
| `parallel_workers` | integer | `1` | Number of parallel workers (1 = sequential) |
| `report_dir` | string | `reports` | Report output directory |
| `selenium.implicit_wait` | integer | `10` | Selenium implicit wait timeout (seconds) |
| `selenium.page_load_timeout` | integer | `60` | Selenium page load timeout (seconds) |
| `playwright.slow_mo` | integer | `0` | Slow down Playwright operations (milliseconds) |
| `playwright.tracing` | boolean | `true` | Enable Playwright tracing on failure |

### Accessing Configuration in Code

```python
from framework.config import Config

config = Config()

# Access configuration properties
base_url = config.base_url
browser = config.browser
headless = config.headless
timeout = config.timeout

# Access nested configuration
selenium_config = config.get('selenium', {})
implicit_wait = selenium_config.get('implicit_wait', 10)
```

## CLI Options

The framework supports command-line options to override configuration values at runtime.

### Available CLI Options

#### `--browser`

**Description**: Override browser selection from config.yaml

**Values**: 
- Selenium: `chrome`, `firefox`
- Playwright: `chromium`, `firefox`, `webkit`

**Example**:
```bash
pytest --browser=firefox
```

#### `--headless`

**Description**: Run browsers in headless mode (overrides config.yaml)

**Type**: Flag (no value required)

**Example**:
```bash
pytest --headless
```

#### `--base-url`

**Description**: Override base URL from config.yaml

**Type**: String (URL)

**Example**:
```bash
pytest --base-url=https://staging.example.com
```

### Additional pytest Options

#### `-m` (marker filtering)

**Description**: Run tests with specific markers

**Available Markers**:
- `selenium`: Selenium WebDriver tests
- `playwright`: Playwright tests
- `smoke`: Smoke tests for quick validation
- `regression`: Full regression suite

**Example**:
```bash
# Run only Selenium tests
pytest -m selenium

# Run only Playwright tests
pytest -m playwright

# Run smoke tests
pytest -m smoke
```

#### `-n` (parallel execution)

**Description**: Run tests in parallel using pytest-xdist

**Type**: Integer (number of workers) or `auto` (use all CPU cores)

**Example**:
```bash
# Run with 4 parallel workers
pytest -n 4

# Run with auto-detected number of workers
pytest -n auto
```

#### `-k` (keyword filtering)

**Description**: Run tests matching keyword expression

**Example**:
```bash
# Run tests with "login" in the name
pytest -k login

# Run tests with "login" but not "logout"
pytest -k "login and not logout"
```

#### Specific test file or function

**Example**:
```bash
# Run specific test file
pytest tests/selenium/test_example_selenium.py

# Run specific test function
pytest tests/selenium/test_example_selenium.py::test_example_navigation
```

### Common Command Combinations

```bash
# Run all tests in headless mode with 4 workers
pytest --headless -n 4

# Run Selenium tests with Firefox browser
pytest -m selenium --browser=firefox

# Run Playwright tests against staging environment
pytest -m playwright --base-url=https://staging.example.com

# Run smoke tests in headless mode
pytest -m smoke --headless

# Run specific test file with custom browser
pytest tests/selenium/test_login.py --browser=chrome --headless
```

## Report Output

The framework automatically generates comprehensive test reports after each test run.

### Report Locations

All reports are saved to the directory specified in `config.yaml` (default: `reports/`):

```
reports/
├── report.html              # HTML test report
├── report.json              # JSON test report
├── screenshots/             # Test failure screenshots
│   └── test_name.png
└── traces/                  # Playwright trace files
    └── test_name.zip
```

### HTML Report

**Location**: `reports/report.html`

**Format**: Self-contained HTML file with embedded CSS and JavaScript

**Contents**:
- Test execution summary (total, passed, failed, skipped, duration)
- Execution date and framework branding
- Detailed test results with pass/fail status
- Error messages and stack traces for failed tests
- Embedded screenshots for failed tests
- Test duration for each test case

**Viewing**: Open `reports/report.html` in any web browser

### JSON Report

**Location**: `reports/report.json`

**Format**: Machine-readable JSON with structured test data

**Contents**:
- Test execution summary statistics
- Detailed test results with outcomes
- Error messages and stack traces
- Test duration and timestamps
- Test metadata (markers, fixtures, etc.)

**Usage**: Parse with `framework.report_utils.ReportUtils.parse_json_report()`

### Screenshots

**Location**: `reports/screenshots/`

**Format**: PNG images

**Capture Trigger**: Automatically captured when a test fails

**Naming Convention**: `{test_name}.png`

**Attachment**: Screenshots are embedded in the HTML report for failed tests

### Trace Files (Playwright Only)

**Location**: `reports/traces/`

**Format**: ZIP archive containing trace data

**Capture Trigger**: Automatically captured when a Playwright test fails (if tracing enabled)

**Naming Convention**: `{test_name}.zip`

**Viewing**: Use Playwright Trace Viewer:
```bash
playwright show-trace reports/traces/test_name.zip
```

**Contents**:
- Screenshots at each step
- DOM snapshots
- Network activity
- Console logs
- Action timeline

## Hooks

Kiro IDE hooks automate repetitive tasks and provide intelligent assistance during test development. Hooks are defined in `.kiro/hooks/` directory.

### Available Hooks

#### Test File Review Hook

**File**: `.kiro/hooks/test-file-review.json`

**Trigger**: When a test file in `tests/**/*.py` is edited and saved

**Action**: Prompts Kiro agent to review the test file for framework convention violations

**Checks**:
1. Correct fixture usage (`selenium_driver` or `playwright_page`)
2. Appropriate marker (`@pytest.mark.selenium` or `@pytest.mark.playwright`)
3. Naming convention (`test_<action>_<result>`)
4. Docstring present
5. One assertion per test when possible

**Purpose**: Ensures test files follow framework conventions and best practices

#### Report Summary Hook

**File**: `.kiro/hooks/report-summary.json`

**Trigger**: User-triggered (manual invocation)

**Action**: Prompts Kiro agent to summarize the test execution report

**Summary Includes**:
1. Total tests, passed, failed, skipped
2. Total duration
3. Failed test names and error messages
4. Suggested next steps for failures

**Purpose**: Provides quick insights into test execution results without manually reviewing reports

#### Test Scaffolding Hook

**File**: `.kiro/hooks/scaffold-test.json`

**Trigger**: When a new test file in `tests/**/*.py` is created

**Action**: Prompts Kiro agent to scaffold the new test file with correct structure

**Scaffolding Includes**:
1. Appropriate imports (pytest, selenium/playwright modules)
2. Correct fixture in function signature
3. Appropriate marker decorator
4. Placeholder test function with docstring

**Purpose**: Accelerates test creation by automatically setting up boilerplate code

### Hook Configuration Format

Hooks are defined as JSON files with the following structure:

```json
{
  "id": "hook-id",
  "name": "Hook Name",
  "description": "Hook description",
  "eventType": "fileEdited|fileCreated|userTriggered",
  "filePatterns": "tests/**/*.py",
  "hookAction": "askAgent",
  "outputPrompt": "Prompt for Kiro agent"
}
```

### Enabling/Disabling Hooks

Hooks are automatically active when present in `.kiro/hooks/`. To disable a hook, remove or rename the JSON file.

## pytest Configuration

The framework uses `pytest.ini` for pytest-specific configuration.

### Test Discovery Patterns

```ini
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Tests must follow these naming conventions to be discovered automatically.

### Test Markers

```ini
markers =
    selenium: Selenium WebDriver tests
    playwright: Playwright tests
    smoke: Smoke tests for quick validation
    regression: Full regression suite
```

Use markers to categorize and filter tests.

### Report Configuration

```ini
addopts =
    --html=reports/report.html
    --self-contained-html
    --json-report
    --json-report-file=reports/report.json
    --json-report-indent=2
    -v
    --tb=short
```

These options are applied automatically to every test run.

### Logging Configuration

```ini
log_cli = true
log_cli_level = INFO
```

Console logging is enabled by default at INFO level.

### Test Timeout

```ini
timeout = 300
```

Tests that exceed 300 seconds (5 minutes) will be terminated automatically.

## Framework Components

### Configuration Loader (`framework/config.py`)

**Class**: `Config`

**Purpose**: Load and provide configuration values with fallback defaults

**Key Methods**:
- `__init__(config_path)`: Initialize and load configuration
- `get(key, default)`: Get configuration value with fallback
- Properties: `base_url`, `browser`, `headless`, `timeout`, `parallel_workers`, `report_dir`

### Selenium Driver Wrapper (`framework/selenium_driver.py`)

**Class**: `SeleniumDriver`

**Purpose**: Initialize and manage Selenium WebDriver instances

**Key Methods**:
- `__init__(browser, headless)`: Configure driver settings
- `initialize()`: Initialize WebDriver with automatic driver management
- `quit()`: Tear down WebDriver session
- `capture_screenshot(filepath)`: Capture screenshot to file

**Supported Browsers**: Chrome, Firefox

### Playwright Driver Wrapper (`framework/playwright_driver.py`)

**Class**: `PlaywrightDriver`

**Purpose**: Initialize and manage Playwright browser contexts

**Key Methods**:
- `__init__(browser_type, headless, slow_mo, tracing)`: Configure browser settings
- `initialize()`: Initialize browser and context with tracing support
- `quit(trace_path)`: Tear down context and browser, optionally save trace
- `capture_screenshot(page, filepath)`: Capture screenshot from page

**Supported Browsers**: Chromium, Firefox, WebKit

### Report Utilities (`framework/report_utils.py`)

**Class**: `ReportUtils`

**Purpose**: Utilities for report generation and management

**Key Methods**:
- `ensure_report_dir(report_dir)`: Create report directory structure
- `parse_json_report(report_path)`: Parse JSON report and extract statistics
- `generate_summary_text(report_path)`: Generate human-readable summary

## Quick Reference

### Running Tests

```bash
# Run all tests
pytest

# Run with specific browser
pytest --browser=firefox

# Run in headless mode
pytest --headless

# Run with parallel execution
pytest -n 4

# Run specific marker
pytest -m selenium

# Run specific test file
pytest tests/selenium/test_example_selenium.py
```

### Writing Tests

```python
# Selenium test
import pytest

@pytest.mark.selenium
def test_example(selenium_driver):
    driver = selenium_driver
    driver.get("https://example.com")
    assert "Example" in driver.title

# Playwright test
import pytest

@pytest.mark.playwright
def test_example(playwright_page):
    page = playwright_page
    page.goto("https://example.com")
    assert "Example" in page.title()
```

### Viewing Reports

```bash
# Open HTML report in browser
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows

# View Playwright trace
playwright show-trace reports/traces/test_name.zip
```

## Additional Resources

- **Test Writing Guide**: `.kiro/steering/test-writing-guide.md`
- **Docker Execution Guide**: `.kiro/steering/docker-execution.md`
- **Setup Documentation**: `README.md`
- **Contribution Guidelines**: `CONTRIBUTING.md`
- **Change History**: `CHANGELOG.md`

## Support

For questions, issues, or feedback:
1. Check existing documentation in `.kiro/steering/` directory
2. Review example tests in `tests/selenium/` and `tests/playwright/`
3. Consult `README.md` for setup and troubleshooting
4. Submit feedback using GitHub issue template (`.github/ISSUE_TEMPLATE/pilot-feedback.md`)
