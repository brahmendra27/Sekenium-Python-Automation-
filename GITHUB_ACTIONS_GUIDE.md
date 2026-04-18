# GitHub Actions CI/CD Guide

This guide explains how to use the GitHub Actions workflows for automated testing with Docker.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Available Workflows](#available-workflows)
3. [Setup Instructions](#setup-instructions)
4. [Workflow Details](#workflow-details)
5. [Configuration](#configuration)
6. [Viewing Reports](#viewing-reports)
7. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The framework includes multiple GitHub Actions workflows for different testing scenarios:

- **Pull Request Tests** - Comprehensive testing on PRs
- **API Tests Only** - Fast API-focused testing
- **Scheduled Tests** - Daily automated test runs
- **Parallel Tests** - Matrix-based parallel execution

All workflows run tests in Docker containers for consistency and isolation.

## 📦 Available Workflows

### 1. Pull Request Tests (`pr-tests.yml`)

**Triggers:**
- Pull requests to `main` or `develop` branches
- On PR open, synchronize, or reopen

**What it does:**
- Runs API tests (fast, no dependencies)
- Runs Database tests (with MongoDB service)
- Runs UI tests (Selenium/Playwright)
- Generates combined Allure report
- Posts test summary to PR
- Deploys Allure report to GitHub Pages

**Jobs:**
1. `api-tests` - API testing
2. `database-tests` - MongoDB testing
3. `ui-tests` - UI testing
4. `allure-report` - Generate combined report
5. `test-summary` - Create summary

### 2. API Tests Only (`api-tests-only.yml`)

**Triggers:**
- Pull requests affecting API-related files
- Manual workflow dispatch
- Changes to:
  - `tests/api/**`
  - `framework/api_client.py`
  - `framework/config.py`
  - `config.yaml`
  - `requirements.txt`

**What it does:**
- Runs API tests on multiple Python versions (3.9, 3.10, 3.11)
- Generates test reports for each version
- Comments PR with test results
- Creates combined Allure report

**Features:**
- Matrix strategy for Python versions
- Test pattern filtering (manual dispatch)
- PR comments with results
- Detailed test metrics

### 3. Scheduled Tests (`scheduled-tests.yml`)

**Triggers:**
- Daily at 2 AM UTC (cron schedule)
- Manual workflow dispatch with test suite selection

**What it does:**
- Runs selected test suite (all, api, database, ui, smoke, regression)
- Generates comprehensive reports
- Sends Slack notifications
- Sends email on failures
- Deploys reports to GitHub Pages

**Test Suites:**
- `all` - All tests
- `api` - API tests only
- `database` - Database tests only
- `ui` - UI tests only
- `smoke` - Smoke tests (marked with `@pytest.mark.smoke`)
- `regression` - Regression tests (marked with `@pytest.mark.regression`)

### 4. Parallel Tests (`parallel-tests.yml`)

**Triggers:**
- Pull requests to `main`
- Manual workflow dispatch

**What it does:**
- Runs tests in parallel using matrix strategy
- Tests multiple browsers (Chrome, Firefox)
- Tests multiple test suites simultaneously
- Aggregates results from all jobs
- Generates combined reports

**Matrix:**
- Test Suites: api, database, ui-selenium, ui-playwright
- Browsers: chrome, firefox
- Parallel workers: 4 per job

## 🚀 Setup Instructions

### 1. Enable GitHub Actions

GitHub Actions is enabled by default for public repositories. For private repositories:

1. Go to repository **Settings**
2. Click **Actions** → **General**
3. Enable **Allow all actions and reusable workflows**

### 2. Configure Secrets

Add the following secrets in **Settings** → **Secrets and variables** → **Actions**:

#### Required Secrets

None required for basic functionality.

#### Optional Secrets (for notifications)

```
SLACK_WEBHOOK_URL       # Slack webhook for notifications
EMAIL_USERNAME          # SMTP username for email notifications
EMAIL_PASSWORD          # SMTP password for email notifications
EMAIL_RECIPIENTS        # Comma-separated email addresses
```

### 3. Enable GitHub Pages (for Allure reports)

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / **root**
4. Click **Save**

### 4. Configure Branch Protection (Optional)

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - Select: `api-tests`, `database-tests`, `ui-tests`

## 📖 Workflow Details

### Pull Request Tests Workflow

```yaml
# Trigger
on:
  pull_request:
    branches: [main, develop]
    types: [opened, synchronize, reopened]

# Jobs
jobs:
  api-tests:        # Fast API tests
  database-tests:   # MongoDB tests with service
  ui-tests:         # Selenium/Playwright tests
  allure-report:    # Combined Allure report
  test-summary:     # PR summary comment
```

**Execution Flow:**
1. API, Database, and UI tests run in parallel
2. Each job uploads its artifacts
3. Allure report job merges all results
4. Summary job creates PR comment
5. Reports deployed to GitHub Pages

**Artifacts:**
- `api-test-report` - HTML report
- `database-test-report` - HTML report
- `ui-test-report` - HTML report
- `ui-screenshots` - Test screenshots
- `ui-traces` - Playwright traces
- `allure-report` - Combined Allure report

### API Tests Only Workflow

```yaml
# Matrix Strategy
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']

# Manual Dispatch Input
inputs:
  test_pattern:
    description: 'Test pattern to run'
    default: ''
```

**Usage:**

**Automatic (on PR):**
```bash
# Triggered automatically when API files change
```

**Manual:**
1. Go to **Actions** tab
2. Select **API Tests Only**
3. Click **Run workflow**
4. Enter test pattern (optional): `test_get_request`
5. Click **Run workflow**

### Scheduled Tests Workflow

```yaml
# Schedule
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC

# Manual Dispatch
inputs:
  test_suite:
    type: choice
    options: [all, api, database, ui, smoke, regression]
```

**Usage:**

**Automatic:**
- Runs daily at 2 AM UTC

**Manual:**
1. Go to **Actions** tab
2. Select **Scheduled Tests**
3. Click **Run workflow**
4. Select test suite
5. Click **Run workflow**

**Notifications:**
- ✅ Slack notification (all runs)
- ✅ Email notification (failures only)

### Parallel Tests Workflow

```yaml
# Matrix Strategy
strategy:
  fail-fast: false
  matrix:
    test-suite: [api, database, ui-selenium, ui-playwright]
    browser: [chrome, firefox]
    exclude:
      - test-suite: api
        browser: firefox
      - test-suite: database
        browser: firefox
```

**Execution:**
- 6 parallel jobs (2 API/DB + 4 UI combinations)
- Each job runs with 4 parallel workers
- Total parallelization: 24 workers

## ⚙️ Configuration

### Environment Variables

Set in workflow files or as repository variables:

```yaml
env:
  HEADLESS: true                                    # Run browsers in headless mode
  BROWSER: chrome                                   # Browser selection
  MONGODB_CONNECTION_STRING: mongodb://localhost:27017
  PARALLEL_WORKERS: 4                               # Number of parallel workers
```

### Docker Configuration

Workflows use the Dockerfile in `docker/Dockerfile`:

```yaml
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: docker/Dockerfile
    tags: test-automation:latest
    load: true
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Build Arguments:**
```yaml
build-args: |
  PYTHON_VERSION=3.10
```

### Test Commands

Customize test execution:

```bash
# API tests
pytest tests/api/ -v

# Database tests
pytest tests/database/ -v

# UI tests
pytest tests/ --ignore=tests/api --ignore=tests/database -v

# Smoke tests
pytest tests/ -m smoke -v

# Parallel execution
pytest tests/ -v -n auto

# With specific pattern
pytest tests/ -k "test_get_request" -v
```

## 📊 Viewing Reports

### GitHub Actions UI

1. Go to **Actions** tab
2. Click on workflow run
3. Click on job name
4. View logs and download artifacts

### Allure Reports

**PR-specific reports:**
```
https://<username>.github.io/<repo>/pr-<number>
```

**Scheduled reports:**
```
https://<username>.github.io/<repo>/scheduled-<date>
```

### Artifacts

Download from workflow run:
1. Scroll to **Artifacts** section
2. Click artifact name to download
3. Extract and open HTML reports

### PR Comments

Test results are automatically commented on PRs:

```markdown
## ✅ API Tests - Python 3.10

| Metric | Value |
|--------|-------|
| Total Tests | 20 |
| Passed | ✅ 20 |
| Failed | ❌ 0 |
| Duration | ⏱️ 1.5s |
```

## 🐛 Troubleshooting

### Tests Failing in CI but Passing Locally

**Possible causes:**
1. Environment differences
2. Timing issues (CI is slower)
3. Missing dependencies

**Solutions:**
```yaml
# Increase timeouts
-e TIMEOUT=60

# Add explicit waits
-e IMPLICIT_WAIT=20

# Enable debug logging
-e LOG_LEVEL=DEBUG
```

### Docker Build Failures

**Check:**
1. Dockerfile syntax
2. Base image availability
3. Dependency installation

**Debug:**
```bash
# Build locally
docker build -f docker/Dockerfile -t test-automation:latest .

# Run interactively
docker run -it test-automation:latest /bin/bash
```

### MongoDB Connection Issues

**Ensure:**
1. MongoDB service is configured
2. Network mode is `host`
3. Connection string is correct

```yaml
services:
  mongodb:
    image: mongo:7.0
    ports:
      - 27017:27017

# In docker run
--network host
-e MONGODB_CONNECTION_STRING="mongodb://localhost:27017"
```

### Allure Report Not Generated

**Check:**
1. Allure results directory exists
2. Test results were generated
3. Allure action configuration

```yaml
- name: Generate Allure Report
  uses: simple-elf/allure-report-action@master
  with:
    allure_results: allure-results-merged
    allure_history: allure-history
```

### Artifacts Not Uploaded

**Verify:**
1. Path is correct
2. Files exist
3. Upload action configuration

```yaml
- name: Upload test reports
  if: always()  # Important: upload even on failure
  uses: actions/upload-artifact@v4
  with:
    name: test-reports
    path: reports/
    if-no-files-found: warn  # or 'error' or 'ignore'
```

## 📝 Best Practices

### 1. Use Matrix Strategy for Parallel Execution

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    browser: [chrome, firefox]
```

### 2. Cache Docker Layers

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

### 3. Always Upload Artifacts

```yaml
if: always()  # Upload even on failure
```

### 4. Use Continue-on-Error for Test Jobs

```yaml
continue-on-error: true  # Don't fail workflow, just mark job
```

### 5. Add Test Summaries

```yaml
echo "# Test Results" >> $GITHUB_STEP_SUMMARY
```

### 6. Use Secrets for Sensitive Data

```yaml
-e API_KEY=${{ secrets.API_KEY }}
```

### 7. Set Appropriate Timeouts

```yaml
timeout-minutes: 30  # Prevent hanging jobs
```

## 🔗 Quick Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Allure Report Action](https://github.com/simple-elf/allure-report-action)
- [Upload Artifact Action](https://github.com/actions/upload-artifact)

## 📚 Additional Resources

- [Docker Testing Guide](docker/README.md)
- [API Testing Guide](API_TESTING_GUIDE.md)
- [MongoDB Testing Guide](MONGODB_TESTING_GUIDE.md)
- [Allure Reporting Guide](ALLURE_REPORTING_GUIDE.md)

---

**Need Help?**
- Check workflow logs in Actions tab
- Review Docker container logs
- Verify configuration in workflow files
- Test Docker build locally first
