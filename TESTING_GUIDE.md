# Testing Guide: Test Automation Framework

**Version:** v0.1.0  
**Last Updated:** 2024-01-15

---

## Table of Contents

1. [Quick Start Testing](#quick-start-testing)
2. [Local Testing](#local-testing)
3. [Docker Testing](#docker-testing)
4. [CI/CD Testing](#cicd-testing)
5. [Kiro IDE Integration Testing](#kiro-ide-integration-testing)
6. [Validation Checklist](#validation-checklist)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start Testing

### Prerequisites Check

Before testing, verify you have:

```bash
# Check Python version (3.11+ required, 3.10+ compatible)
python --version

# Check pip is installed
pip --version

# Check Docker is installed (optional, for Docker testing)
docker --version
docker-compose --version

# Check Git is installed
git --version
```

### 5-Minute Smoke Test

```bash
# 1. Clone repository (if not already cloned)
git clone <repository-url>
cd test-automation-framework

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install

# 5. Run Playwright example tests (fastest, most reliable)
pytest tests/playwright/test_example_playwright.py -v

# 6. Check reports were generated
ls reports/
# Should see: report.html, report.json, screenshots/, traces/

# 7. Open HTML report
# On Windows:
start reports/report.html
# On Linux:
xdg-open reports/report.html
# On Mac:
open reports/report.html
```

**Expected Result:** 5 Playwright tests pass, reports generated in `reports/` directory.

---

## Local Testing

### Test 1: Configuration Loading

**Purpose:** Verify configuration is loaded correctly from `config.yaml`.

```bash
# Run this Python script to test config loading
python -c "
from framework.config import Config
config = Config()
print(f'Base URL: {config.base_url}')
print(f'Browser: {config.browser}')
print(f'Headless: {config.headless}')
print(f'Timeout: {config.timeout}')
print(f'Report Dir: {config.report_dir}')
"
```

**Expected Output:**
```
Base URL: http://localhost:8080
Browser: chrome
Headless: False
Timeout: 30
Report Dir: reports
```

**Validation:** ✅ Configuration values match `config.yaml` defaults.

---

### Test 2: Playwright Tests - All Browsers

**Purpose:** Verify Playwright works with all supported browsers.

#### Test 2.1: Chromium

```bash
pytest tests/playwright/test_example_playwright.py --browser=chromium -v
```

**Expected Output:**
```
tests/playwright/test_example_playwright.py::test_example_homepage PASSED
tests/playwright/test_example_playwright.py::test_example_search PASSED
tests/playwright/test_example_playwright.py::test_example_navigation PASSED
tests/playwright/test_example_playwright.py::test_example_form_interaction PASSED
tests/playwright/test_example_playwright.py::test_example_screenshot PASSED

====== 5 passed in 15-20s ======
```

**Validation:** ✅ All 5 tests pass, execution time 15-20 seconds.

#### Test 2.2: Firefox

```bash
pytest tests/playwright/test_example_playwright.py --browser=firefox -v
```

**Expected Output:** Same as Chromium (5 passed).

**Validation:** ✅ All 5 tests pass.

#### Test 2.3: WebKit

```bash
pytest tests/playwright/test_example_playwright.py --browser=webkit -v
```

**Expected Output:** Same as Chromium (5 passed).

**Validation:** ✅ All 5 tests pass.

---

### Test 3: Selenium Tests

**Purpose:** Verify Selenium works with supported browsers.

#### Test 3.1: Chrome

```bash
pytest tests/selenium/test_example_selenium.py --browser=chrome -v
```

**Expected Output (if ChromeDriver is properly installed):**
```
tests/selenium/test_example_selenium.py::test_example_homepage PASSED
tests/selenium/test_example_selenium.py::test_example_search PASSED
tests/selenium/test_example_selenium.py::test_example_navigation PASSED

====== 3 passed in 10-15s ======
```

**Known Issue on Windows:**
If you see `[WinError 193] %1 is not a valid Win32 application`, this is a ChromeDriver compatibility issue. Use Docker execution instead (see Test 6).

**Validation:** ✅ All 3 tests pass (or use Docker workaround).

#### Test 3.2: Firefox

```bash
pytest tests/selenium/test_example_selenium.py --browser=firefox -v
```

**Expected Output:** Same as Chrome (3 passed).

**Validation:** ✅ All 3 tests pass.

---

### Test 4: Report Generation

**Purpose:** Verify HTML and JSON reports are generated correctly.

```bash
# Run tests
pytest tests/playwright/test_example_playwright.py -v

# Check reports exist
ls -lh reports/

# Verify HTML report
cat reports/report.html | grep "Test Automation Framework"

# Verify JSON report
python -c "
import json
with open('reports/report.json', 'r') as f:
    report = json.load(f)
    print(f\"Total tests: {report['summary']['total']}\")
    print(f\"Passed: {report['summary']['passed']}\")
    print(f\"Failed: {report['summary']['failed']}\")
"
```

**Expected Output:**
```
reports/report.html (30-40 KB)
reports/report.json (25-30 KB)
reports/screenshots/ (directory)
reports/traces/ (directory)

Total tests: 5
Passed: 5
Failed: 0
```

**Validation:** ✅ Both reports generated, correct test counts.

---

### Test 5: CLI Options

**Purpose:** Verify command-line options override config.yaml.

#### Test 5.1: Headless Mode

```bash
pytest tests/playwright/test_example_playwright.py --headless -v
```

**Expected Output:** Tests run in headless mode (no browser window visible).

**Validation:** ✅ Tests pass, no browser window appears.

#### Test 5.2: Custom Browser

```bash
pytest tests/playwright/test_example_playwright.py --browser=firefox -v
```

**Expected Output:** Tests run with Firefox browser.

**Validation:** ✅ Tests pass with Firefox.

#### Test 5.3: Custom Base URL

```bash
pytest tests/playwright/test_example_playwright.py --base-url=https://example.com -v
```

**Expected Output:** Tests run against https://example.com.

**Validation:** ✅ Tests use custom base URL.

---

### Test 6: Parallel Execution

**Purpose:** Verify tests can run in parallel with pytest-xdist.

```bash
# Run with 4 parallel workers
pytest tests/playwright/test_example_playwright.py -n 4 -v
```

**Expected Output:**
```
gw0 [5] / gw1 [5] / gw2 [5] / gw3 [5]
...
====== 5 passed in 5-8s ======
```

**Validation:** ✅ Tests complete faster than sequential execution (15-20s → 5-8s).

---

### Test 7: Test Markers

**Purpose:** Verify test filtering by markers.

#### Test 7.1: Run Only Selenium Tests

```bash
pytest -m selenium -v
```

**Expected Output:** Only Selenium tests run (3 tests).

**Validation:** ✅ Only tests marked with `@pytest.mark.selenium` execute.

#### Test 7.2: Run Only Playwright Tests

```bash
pytest -m playwright -v
```

**Expected Output:** Only Playwright tests run (5 tests).

**Validation:** ✅ Only tests marked with `@pytest.mark.playwright` execute.

---

## Docker Testing

### Test 8: Docker Build

**Purpose:** Verify Docker image builds successfully.

```bash
# Build Docker image
docker build -t test-automation-framework -f docker/Dockerfile .
```

**Expected Output:**
```
[+] Building 300-600s (15/15) FINISHED
...
Successfully tagged test-automation-framework:latest
```

**Note:** First build takes 5-10 minutes (downloads browsers). Subsequent builds are faster.

**Validation:** ✅ Image builds without errors.

---

### Test 9: Docker Execution with Docker Compose

**Purpose:** Verify tests run correctly in Docker container.

```bash
# Run tests in Docker
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

**Expected Output:**
```
test-runner_1  | ====== 8 passed in 20-30s ======
test-runner_1 exited with code 0
```

**Validation:** 
- ✅ Tests pass in container
- ✅ Exit code is 0 (success)
- ✅ Reports generated in `reports/` directory on host

---

### Test 10: Docker Execution - Manual

**Purpose:** Verify manual Docker execution with custom options.

```bash
# Run specific tests
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  test-automation-framework:latest \
  pytest tests/playwright/test_example_playwright.py -v

# Run with custom browser
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  test-automation-framework:latest \
  pytest --browser=firefox -v

# Run in parallel
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  test-automation-framework:latest \
  pytest -n 4 -v
```

**Validation:** ✅ All variations work correctly.

---

## CI/CD Testing

### Test 11: GitHub Actions Workflow Validation

**Purpose:** Verify GitHub Actions workflow is configured correctly.

```bash
# Validate workflow syntax
cat .github/workflows/test.yml

# Check for required steps
grep -E "checkout|docker|pytest|upload" .github/workflows/test.yml
```

**Expected Output:**
```yaml
- uses: actions/checkout@v3
- uses: docker/setup-buildx-action@v2
- run: docker build ...
- run: docker run ... pytest ...
- uses: actions/upload-artifact@v3
```

**Validation:** ✅ All required steps present.

---

### Test 12: GitHub Actions - Local Simulation

**Purpose:** Simulate GitHub Actions workflow locally.

```bash
# Simulate CI environment
export CI=true
export HEADLESS=true

# Run tests as CI would
docker build -t test-automation-framework -f docker/Dockerfile .
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -e HEADLESS=true \
  test-automation-framework:latest \
  pytest --headless -v

# Check exit code
echo $?
# Should be 0 for success, non-zero for failure
```

**Validation:** ✅ Exit code is 0, reports generated.

---

## Kiro IDE Integration Testing

### Test 13: Steering Files

**Purpose:** Verify steering files are accessible and well-formatted.

```bash
# Check steering files exist
ls -lh .kiro/steering/

# Validate frontmatter in steering files
head -n 10 .kiro/steering/test-writing-guide.md
head -n 10 .kiro/steering/framework-overview.md
head -n 10 .kiro/steering/docker-execution.md
```

**Expected Output:**
```
test-writing-guide.md (10-15 KB)
framework-overview.md (15-20 KB)
docker-execution.md (10-15 KB)

---
title: Test Writing Guide
description: Guide for writing Selenium and Playwright tests
inclusion: auto
keywords: [test, selenium, playwright, write test, create test]
---
```

**Validation:** ✅ All steering files have proper frontmatter.

---

### Test 14: Hooks Configuration

**Purpose:** Verify hooks are configured correctly.

```bash
# Check hooks exist
ls -lh .kiro/hooks/

# Validate hook JSON structure
cat .kiro/hooks/test-file-review.kiro.hook | python -m json.tool
cat .kiro/hooks/report-summary.kiro.hook | python -m json.tool
cat .kiro/hooks/scaffold-test.kiro.hook | python -m json.tool
```

**Expected Output:**
```
test-file-review.kiro.hook (valid JSON)
report-summary.kiro.hook (valid JSON)
scaffold-test.kiro.hook (valid JSON)

{
  "name": "Test File Convention Review",
  "version": "1.0.0",
  "description": "...",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "..."
  }
}
```

**Validation:** ✅ All hooks have valid JSON structure.

---

### Test 15: Kiro IDE - Manual Testing

**Purpose:** Manually test Kiro IDE integration (requires Kiro IDE).

#### Test 15.1: Test File Review Hook

1. Open Kiro IDE
2. Open or create a test file in `tests/selenium/` or `tests/playwright/`
3. Make a change and save the file
4. **Expected:** Kiro agent reviews the file for convention violations

**Validation:** ✅ Hook triggers, agent provides feedback.

#### Test 15.2: Report Summary Hook

1. Run tests: `pytest -v`
2. In Kiro IDE, manually trigger the "Test Report Summary" hook
3. **Expected:** Kiro agent summarizes the report from `reports/report.json`

**Validation:** ✅ Hook triggers, agent provides summary.

#### Test 15.3: Scaffold Test Hook

1. In Kiro IDE, create a new file in `tests/selenium/` or `tests/playwright/`
2. Name it `test_new_feature.py`
3. **Expected:** Kiro agent scaffolds the file with correct imports and structure

**Validation:** ✅ Hook triggers, agent scaffolds file.

---

## Validation Checklist

Use this checklist to validate the framework is working correctly:

### Core Functionality
- [ ] Configuration loads from `config.yaml`
- [ ] Playwright tests pass (Chromium, Firefox, WebKit)
- [ ] Selenium tests pass (Chrome, Firefox) or Docker workaround works
- [ ] HTML report generated in `reports/report.html`
- [ ] JSON report generated in `reports/report.json`
- [ ] Screenshots captured on test failure
- [ ] Traces captured on Playwright test failure

### CLI Options
- [ ] `--browser` option overrides config
- [ ] `--headless` option enables headless mode
- [ ] `--base-url` option overrides base URL
- [ ] `-m selenium` filters Selenium tests
- [ ] `-m playwright` filters Playwright tests
- [ ] `-n 4` enables parallel execution

### Docker
- [ ] Docker image builds successfully
- [ ] Tests run in Docker container
- [ ] Reports generated in host `reports/` directory
- [ ] Exit code propagates correctly (0 for pass, non-zero for fail)

### CI/CD
- [ ] GitHub Actions workflow syntax is valid
- [ ] Workflow has all required steps (checkout, build, test, upload)
- [ ] Workflow configured to trigger on push and pull_request

### Kiro IDE Integration
- [ ] Steering files exist and have proper frontmatter
- [ ] Hooks exist and have valid JSON structure
- [ ] Test file review hook triggers on file save
- [ ] Report summary hook can be manually triggered
- [ ] Scaffold test hook triggers on file creation

### Documentation
- [ ] README.md is complete and accurate
- [ ] CONTRIBUTING.md is complete and accurate
- [ ] CHANGELOG.md has v0.1.0 release notes
- [ ] docker/README.md has Docker instructions
- [ ] Pilot feedback template exists

---

## Troubleshooting

### Issue: Playwright browsers not installed

**Symptom:**
```
playwright._impl._api_types.Error: Executable doesn't exist at ...
```

**Solution:**
```bash
playwright install
```

---

### Issue: Selenium ChromeDriver error on Windows

**Symptom:**
```
[WinError 193] %1 is not a valid Win32 application
```

**Solution:**
Use Docker execution:
```bash
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

---

### Issue: Reports not generated

**Symptom:**
No `reports/` directory or empty directory.

**Solution:**
```bash
# Ensure pytest plugins are installed
pip install pytest-html pytest-json-report

# Run tests with explicit report options
pytest --html=reports/report.html --json-report --json-report-file=reports/report.json
```

---

### Issue: Docker build fails

**Symptom:**
```
ERROR [internal] load metadata for docker.io/library/python:3.11-slim
```

**Solution:**
```bash
# Check Docker daemon is running
docker ps

# Check internet connectivity
ping google.com

# Try building with --no-cache
docker build --no-cache -t test-automation-framework -f docker/Dockerfile .
```

---

### Issue: Tests fail in Docker but pass locally

**Symptom:**
Tests pass locally but fail in Docker container.

**Solution:**
```bash
# Ensure tests are compatible with headless mode
pytest --headless -v

# Check Docker logs for errors
docker logs <container-id>

# Run Docker container interactively for debugging
docker run -it --rm test-automation-framework:latest /bin/bash
```

---

## Testing Summary

After completing all tests, you should have validated:

1. ✅ **Local Execution:** Playwright and Selenium tests work
2. ✅ **Reports:** HTML and JSON reports generated correctly
3. ✅ **CLI Options:** All command-line options work
4. ✅ **Docker:** Tests run successfully in containers
5. ✅ **CI/CD:** GitHub Actions workflow configured correctly
6. ✅ **Kiro IDE:** Steering files and hooks are functional
7. ✅ **Documentation:** All documentation is complete

**Framework Status:** Ready for pilot rollout! 🚀

---

**Testing Guide Version:** v0.1.0  
**Last Updated:** 2024-01-15  
**Next Review:** After pilot phase feedback
