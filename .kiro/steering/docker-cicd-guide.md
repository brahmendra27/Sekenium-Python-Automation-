---
title: Docker and CI/CD Execution Guide
description: Comprehensive guide for running tests in Docker and CI/CD environments
inclusion: auto
tags: [docker, cicd, github-actions, testing, automation]
---

# Docker and CI/CD Execution Guide

## Overview

This guide provides instructions for running tests in Docker containers and CI/CD pipelines. Use this when working with containerized test execution or GitHub Actions workflows.

## Docker Execution

### Building the Docker Image

```bash
# Build from project root
docker build -f docker/Dockerfile -t test-automation:latest .

# Build with specific tag
docker build -f docker/Dockerfile -t test-automation:v1.0.0 .

# Build with no cache (clean build)
docker build --no-cache -f docker/Dockerfile -t test-automation:latest .
```

### Running Tests in Docker

#### Run All Tests
```bash
docker run --rm test-automation:latest pytest -v
```

#### Run Specific Test Suite
```bash
# Skechers tests
docker run --rm test-automation:latest pytest tests/skechers/ -v

# Demo e-commerce tests
docker run --rm test-automation:latest pytest tests/demo_ecommerce/ -v

# API tests only
docker run --rm test-automation:latest pytest tests/api/ -v
```

#### Run with Markers
```bash
# Smoke tests only
docker run --rm test-automation:latest pytest -m smoke -v

# Regression tests
docker run --rm test-automation:latest pytest -m regression -v

# API tests
docker run --rm test-automation:latest pytest -m api -v
```

#### Run with Custom Configuration
```bash
# Use specific config file
docker run --rm \
  -v $(pwd)/config.custom.yaml:/app/config.yaml \
  test-automation:latest pytest -v

# Override base URL
docker run --rm \
  -e BASE_URL="https://staging.example.com" \
  test-automation:latest pytest -v
```

#### Run with Reports
```bash
# Generate Allure reports
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  test-automation:latest \
  pytest --alluredir=reports/allure-results -v

# Generate HTML report
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  test-automation:latest \
  pytest --html=reports/report.html --self-contained-html -v
```

#### Run with Environment Variables
```bash
docker run --rm \
  -e HEADLESS=true \
  -e BROWSER=firefox \
  -e TIMEOUT=60 \
  test-automation:latest pytest -v
```

### Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  tests:
    build:
      context: .
      dockerfile: docker/Dockerfile
    volumes:
      - ./reports:/app/reports
    environment:
      - HEADLESS=true
      - BROWSER=chrome
    command: pytest -v --alluredir=reports/allure-results

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_DATABASE=test_db
```

Run with Docker Compose:
```bash
docker-compose up --abort-on-container-exit
```

## CI/CD Execution (GitHub Actions)

### Available Workflows

1. **PR Tests** (`.github/workflows/pr-tests.yml`)
   - Triggers on: Pull requests to main/develop
   - Runs: API, Database, UI tests in parallel
   - Generates: Allure reports, test summaries

2. **API Tests Only** (`.github/workflows/api-tests-only.yml`)
   - Triggers on: Push to main, manual dispatch
   - Runs: API tests on Python 3.9, 3.10, 3.11
   - Fast feedback for API changes

3. **Scheduled Tests** (`.github/workflows/scheduled-tests.yml`)
   - Triggers on: Daily schedule (cron)
   - Runs: Full test suite
   - Sends: Notifications on failure

4. **Parallel Tests** (`.github/workflows/parallel-tests.yml`)
   - Triggers on: Manual dispatch
   - Runs: 6 parallel test jobs
   - Maximum speed execution

### Triggering Workflows

#### Automatic Triggers
```bash
# Create PR (triggers pr-tests.yml)
git checkout -b feature/my-feature
git push origin feature/my-feature
# Create PR on GitHub

# Push to main (triggers api-tests-only.yml)
git checkout main
git push origin main
```

#### Manual Triggers
```bash
# Using GitHub CLI
gh workflow run api-tests-only.yml

gh workflow run parallel-tests.yml

# Using GitHub UI
# Go to Actions tab → Select workflow → Run workflow
```

### Monitoring CI/CD Runs

#### Check Status
```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# Watch run in real-time
gh run watch <run-id>
```

#### View Logs
```bash
# View logs for specific job
gh run view <run-id> --log

# Download logs
gh run download <run-id>
```

### CI/CD Environment Variables

Set these in GitHub repository settings (Settings → Secrets and variables → Actions):

#### Required Secrets
```
GITHUB_TOKEN          # Automatically provided
```

#### Optional Secrets
```
MONGODB_CONNECTION_STRING    # For database tests
SLACK_WEBHOOK_URL           # For notifications
TEST_USER_EMAIL             # For authentication tests
TEST_USER_PASSWORD          # For authentication tests
```

#### Environment Variables
```
HEADLESS=true              # Run browsers in headless mode
BROWSER=chrome             # Browser selection
TIMEOUT=30                 # Default timeout
PARALLEL_WORKERS=4         # Number of parallel workers
```

### Debugging CI/CD Failures

#### Enable Debug Logging
Add to workflow file:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

#### SSH into Runner (for debugging)
Add step to workflow:
```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: failure()
```

#### Check Docker Build Logs
```yaml
- name: Build Docker image
  run: |
    docker build -f docker/Dockerfile -t test-automation:latest . --progress=plain
```

## Common Issues and Solutions

### Docker Build Issues

#### Issue: Package Installation Fails
```
ERROR: failed to solve: process "/bin/sh -c apt-get install..." exit code: 100
```

**Solution:**
- Use full `python:3.11` image instead of `python:3.11-slim`
- Install dependencies manually
- Update package lists: `apt-get update`

#### Issue: Playwright Installation Fails
```
ERROR: playwright install --with-deps failed
```

**Solution:**
- Don't use `--with-deps` flag in Docker
- Install system dependencies manually via apt-get
- Use: `python -m playwright install chromium firefox`

#### Issue: Out of Memory
```
ERROR: failed to build: out of memory
```

**Solution:**
- Increase Docker memory limit
- Use multi-stage builds
- Clean up in same RUN command: `&& rm -rf /var/lib/apt/lists/*`

### CI/CD Issues

#### Issue: Tests Timeout
```
Error: The operation was canceled.
```

**Solution:**
- Increase timeout in workflow:
  ```yaml
  timeout-minutes: 30
  ```
- Reduce test scope
- Use parallel execution

#### Issue: Artifacts Not Uploaded
```
Warning: No files were found with the provided path
```

**Solution:**
- Verify report paths are correct
- Use `if: always()` to upload even on failure
- Check volume mounts in Docker

#### Issue: Flaky Tests
```
Tests pass locally but fail in CI
```

**Solution:**
- Increase timeouts for CI environment
- Add explicit waits
- Use headless mode consistently
- Check for timing issues

## Best Practices

### Docker

1. **Use Multi-Stage Builds** (if needed)
   ```dockerfile
   FROM python:3.11 as builder
   # Build dependencies
   
   FROM python:3.11-slim
   # Copy only what's needed
   ```

2. **Minimize Image Size**
   - Clean up in same RUN command
   - Use `.dockerignore` file
   - Install only required browsers

3. **Cache Dependencies**
   - Copy requirements.txt first
   - Install dependencies before copying code
   - Use BuildKit cache mounts

4. **Security**
   - Don't run as root (add USER directive)
   - Scan images for vulnerabilities
   - Use specific version tags

### CI/CD

1. **Fail Fast**
   - Run smoke tests first
   - Use `continue-on-error: false`
   - Set appropriate timeouts

2. **Parallel Execution**
   - Split tests by type (API, UI, DB)
   - Use matrix strategy
   - Balance job distribution

3. **Caching**
   - Cache Docker layers
   - Cache pip dependencies
   - Cache Playwright browsers

4. **Reporting**
   - Always upload artifacts
   - Generate test summaries
   - Send notifications on failure

5. **Resource Management**
   - Set memory limits
   - Use appropriate runner sizes
   - Clean up after tests

## Configuration Examples

### Dockerfile Best Practices
```dockerfile
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

# Install system dependencies (in one layer)
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium firefox

# Copy application code
COPY framework/ ./framework/
COPY tests/ ./tests/
COPY conftest.py pytest.ini config.yaml ./

# Create directories
RUN mkdir -p reports/screenshots reports/traces

# Run tests
CMD ["pytest", "--headless"]
```

### GitHub Actions Workflow Best Practices
```yaml
name: Test Execution

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile
          tags: test-automation:latest
          load: true
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Run tests
        id: tests
        continue-on-error: true
        run: |
          docker run --rm \
            -v ${{ github.workspace }}/reports:/app/reports \
            -e HEADLESS=true \
            test-automation:latest \
            pytest -v --alluredir=reports/allure-results
      
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: reports/
      
      - name: Check test results
        if: steps.tests.outcome == 'failure'
        run: exit 1
```

## Quick Reference

### Docker Commands
```bash
# Build
docker build -f docker/Dockerfile -t test-automation:latest .

# Run all tests
docker run --rm test-automation:latest pytest -v

# Run with reports
docker run --rm -v $(pwd)/reports:/app/reports test-automation:latest pytest --alluredir=reports/allure-results

# Run specific tests
docker run --rm test-automation:latest pytest tests/skechers/ -m smoke -v

# Interactive shell
docker run --rm -it test-automation:latest /bin/bash
```

### GitHub Actions Commands
```bash
# List workflows
gh workflow list

# Run workflow
gh workflow run <workflow-name>

# View runs
gh run list

# Watch run
gh run watch <run-id>

# Download artifacts
gh run download <run-id>
```

## Troubleshooting Checklist

- [ ] Docker image builds successfully
- [ ] All dependencies installed
- [ ] Playwright browsers available
- [ ] Tests can be discovered
- [ ] Configuration files present
- [ ] Environment variables set
- [ ] Network connectivity working
- [ ] Sufficient memory allocated
- [ ] Timeouts configured appropriately
- [ ] Reports generated correctly

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright Docker Guide](https://playwright.dev/docs/docker)
- [pytest Documentation](https://docs.pytest.org/)

---

**Last Updated:** 2026-04-18  
**Maintained By:** Test Automation Team
