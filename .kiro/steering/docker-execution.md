---
title: Docker Execution Guide
description: Guide for running tests in Docker containers for reproducible test environments
inclusion: auto
keywords: [docker, container, execution, build, docker-compose, reproducible, ci, containerization]
---

# Docker Execution Guide

## Overview

This guide describes how to build and run the Test Automation Framework inside Docker containers. Docker provides a consistent, reproducible test environment that eliminates "works on my machine" issues and ensures tests run identically across local development, CI pipelines, and team member machines.

Use this guide when:
- Setting up the framework for the first time
- Running tests in a clean, isolated environment
- Preparing tests for CI/CD integration
- Troubleshooting environment-specific test failures
- Ensuring consistent browser and driver versions across the team

---

## Prerequisites

### Required Software

1. **Docker**: Version 20.10 or higher
   - Download: https://docs.docker.com/get-docker/
   - Verify installation: `docker --version`

2. **Docker Compose**: Version 2.0 or higher (included with Docker Desktop)
   - Verify installation: `docker-compose --version`

### System Requirements

- **Disk Space**: At least 2GB free for Docker image
- **Memory**: At least 4GB RAM allocated to Docker
- **Network**: Internet connection required for initial image build

---

## Docker Image

The framework includes a `Dockerfile` that creates a self-contained image with all dependencies pre-installed.

### Image Contents

The Docker image includes:
- **Base**: Python 3.11 on Debian-based Linux
- **System Dependencies**: Chrome, Firefox, Chromium, WebKit dependencies
- **Python Dependencies**: All packages from `requirements.txt` (selenium, playwright, pytest, etc.)
- **Browser Binaries**: Chrome, Firefox, Chromium, WebKit (installed at build time)
- **WebDriver Binaries**: ChromeDriver, GeckoDriver (managed by webdriver-manager)
- **Playwright Browsers**: Chromium, Firefox, WebKit (installed via `playwright install`)

### Image Location

**Dockerfile Path**: `docker/Dockerfile`

**Build Context**: Project root directory (contains `requirements.txt`, `config.yaml`, test files)

---

## Building the Docker Image

### Basic Build Command

Build the Docker image from the project root directory:

```bash
docker build -t test-automation-framework -f docker/Dockerfile .
```

**Command Breakdown**:
- `docker build`: Docker build command
- `-t test-automation-framework`: Tag the image with name "test-automation-framework"
- `-f docker/Dockerfile`: Specify Dockerfile location
- `.`: Build context (current directory - project root)

### Build Output

The build process will:
1. Pull Python 3.11 base image
2. Install system dependencies (Chrome, Firefox, browser dependencies)
3. Copy `requirements.txt` and install Python packages
4. Install Playwright browsers
5. Copy framework code and test files
6. Set up working directory and entrypoint

**Expected Build Time**: 5-10 minutes (first build), 1-2 minutes (subsequent builds with cache)

### Verifying the Build

After successful build, verify the image exists:

```bash
docker images | grep test-automation-framework
```

**Expected Output**:
```
test-automation-framework   latest   abc123def456   2 minutes ago   1.8GB
```

### Build Options

#### Rebuild Without Cache

Force a complete rebuild without using cached layers:

```bash
docker build --no-cache -t test-automation-framework -f docker/Dockerfile .
```

**Use Case**: When dependencies have changed or build cache is corrupted

#### Build with Custom Tag

Build with a specific version tag:

```bash
docker build -t test-automation-framework:v1.0.0 -f docker/Dockerfile .
```

**Use Case**: Version tracking, multiple image versions

---

## Running Tests with Docker Compose

Docker Compose simplifies running tests by managing container configuration, volume mounts, and environment variables.

### Docker Compose Configuration

**File Path**: `docker/docker-compose.yml`

**Service Definition**:
```yaml
services:
  test-runner:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    volumes:
      - ../reports:/app/reports
    environment:
      - HEADLESS=true
    command: pytest
```

**Configuration Details**:
- **Service Name**: `test-runner`
- **Build Context**: Parent directory (project root)
- **Volume Mount**: Maps host `reports/` to container `/app/reports` for report retrieval
- **Environment**: Sets `HEADLESS=true` to run browsers in headless mode
- **Command**: Runs `pytest` by default (can be overridden)

### Basic Execution Command

Run all tests using Docker Compose:

```bash
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

**Command Breakdown**:
- `docker-compose`: Docker Compose command
- `-f docker/docker-compose.yml`: Specify compose file location
- `up`: Start services and run containers
- `--abort-on-container-exit`: Stop all containers when test runner exits

**Expected Behavior**:
1. Builds image if not already built
2. Creates and starts test-runner container
3. Runs pytest inside container
4. Saves reports to host `reports/` directory
5. Exits with same exit code as pytest (0 = pass, non-zero = fail)
6. Stops and removes container

### Viewing Test Output

Test output is streamed to the console in real-time. You'll see:
- pytest test discovery
- Test execution progress
- Pass/fail status for each test
- Summary statistics
- Report generation messages

**Example Output**:
```
test-runner_1  | ============================= test session starts ==============================
test-runner_1  | platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.3.0
test-runner_1  | rootdir: /app
test-runner_1  | plugins: html-3.2.0, json-report-1.5.0, xdist-3.3.1, playwright-0.4.0
test-runner_1  | collected 12 items
test-runner_1  | 
test-runner_1  | tests/selenium/test_example_selenium.py::test_example_navigation PASSED [  8%]
test-runner_1  | tests/playwright/test_example_playwright.py::test_example_navigation PASSED [ 16%]
test-runner_1  | 
test-runner_1  | ============================== 12 passed in 45.23s ==============================
```

### Retrieving Reports

After test execution, reports are available on the host machine:

```bash
# List generated reports
ls -la reports/

# Open HTML report in browser
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows

# View JSON report
cat reports/report.json

# View screenshots
ls -la reports/screenshots/

# View Playwright traces
ls -la reports/traces/
```

---

## Advanced Docker Execution

### Running Specific Tests

Override the default `pytest` command to run specific tests:

#### Run Specific Test File

```bash
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest tests/selenium/test_example_selenium.py
```

#### Run Specific Test Function

```bash
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest tests/selenium/test_example_selenium.py::test_example_navigation
```

#### Run Tests by Marker

```bash
# Run only Selenium tests
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -m selenium

# Run only Playwright tests
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -m playwright

# Run smoke tests
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -m smoke
```

**Command Breakdown**:
- `run`: Run a one-off command instead of default command
- `--rm`: Remove container after execution
- `test-runner`: Service name from docker-compose.yml
- `pytest ...`: Command to run inside container

### Running Tests in Parallel

Run tests with multiple workers for faster execution:

```bash
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -n 4
```

**Note**: Adjust worker count based on available CPU cores and memory

### Running with Custom Browser

Override browser selection via command-line option:

```bash
# Run with Firefox
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest --browser=firefox

# Run with Chromium (Playwright)
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest --browser=chromium
```

### Running with Custom Base URL

Override base URL for testing different environments:

```bash
# Run against staging environment
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest --base-url=https://staging.example.com

# Run against production environment
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest --base-url=https://example.com
```

### Running with Environment Variables

Pass additional environment variables to the container:

```bash
docker-compose -f docker/docker-compose.yml run --rm \
  -e HEADLESS=false \
  -e BROWSER=firefox \
  test-runner pytest
```

**Common Environment Variables**:
- `HEADLESS`: Set to `true` or `false` to control headless mode
- `BROWSER`: Override browser selection
- `BASE_URL`: Override base URL
- `PARALLEL_WORKERS`: Set number of parallel workers

---

## Headless Mode in Docker

### Default Behavior

By default, Docker containers run browsers in **headless mode** (no visible browser window). This is configured via:

1. **Environment Variable**: `HEADLESS=true` in `docker-compose.yml`
2. **Configuration File**: `headless: true` in `config.yaml`

### Why Headless Mode?

Headless mode is required in Docker because:
- Containers typically don't have a display server (X11)
- No GUI is available in containerized environments
- Headless mode is faster and uses less memory
- CI/CD pipelines require headless execution

### Forcing Headed Mode (Advanced)

To run browsers in headed mode inside Docker (for debugging), you need to:

1. **Install X11 Server** on host machine
2. **Mount X11 Socket** into container
3. **Set DISPLAY Environment Variable**

**Example** (Linux/macOS with X11):
```bash
docker-compose -f docker/docker-compose.yml run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e HEADLESS=false \
  test-runner pytest
```

**Note**: This is rarely needed and not recommended for CI/CD pipelines

---

## Volume Mounts for Report Retrieval

### Default Volume Mount

The `docker-compose.yml` file mounts the `reports/` directory:

```yaml
volumes:
  - ../reports:/app/reports
```

**Behavior**:
- Host directory: `<project-root>/reports/`
- Container directory: `/app/reports/`
- Reports generated inside container are immediately available on host
- Bidirectional sync (changes on host visible in container and vice versa)

### Verifying Volume Mount

After running tests, verify reports are accessible on host:

```bash
# Check reports directory exists
ls -la reports/

# Verify report files
ls -la reports/report.html reports/report.json

# Check screenshots
ls -la reports/screenshots/

# Check traces
ls -la reports/traces/
```

### Custom Volume Mounts

Mount additional directories for custom test data or configuration:

```bash
docker-compose -f docker/docker-compose.yml run --rm \
  -v $(pwd)/test-data:/app/test-data \
  test-runner pytest
```

**Use Case**: Mounting external test data files, custom configuration, or shared resources

---

## Exit Codes and CI Integration

### Exit Code Behavior

The Docker container returns the same exit code as the pytest runner:

- **Exit Code 0**: All tests passed
- **Exit Code 1**: One or more tests failed
- **Exit Code 2**: Test execution interrupted (e.g., KeyboardInterrupt)
- **Exit Code 3**: Internal pytest error
- **Exit Code 4**: pytest usage error
- **Exit Code 5**: No tests collected

### Checking Exit Code

```bash
# Run tests and capture exit code
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
echo "Exit code: $?"

# Or with docker-compose run
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest
echo "Exit code: $?"
```

### CI/CD Integration

The exit code behavior makes Docker execution ideal for CI/CD pipelines:

**GitHub Actions Example**:
```yaml
- name: Run tests in Docker
  run: |
    docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
    
- name: Upload test reports
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: reports/
```

**GitLab CI Example**:
```yaml
test:
  script:
    - docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
  artifacts:
    when: always
    paths:
      - reports/
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Docker build fails with "no space left on device"

**Cause**: Insufficient disk space for Docker images

**Solution**:
```bash
# Remove unused Docker images and containers
docker system prune -a

# Check available disk space
df -h
```

#### Issue: Tests fail with "WebDriver not found" or "Browser not found"

**Cause**: Browsers or drivers not properly installed in Docker image

**Solution**:
```bash
# Rebuild image without cache
docker build --no-cache -t test-automation-framework -f docker/Dockerfile .

# Verify Playwright browsers are installed
docker run --rm test-automation-framework playwright --version
```

#### Issue: Reports not appearing in host `reports/` directory

**Cause**: Volume mount not configured correctly or permissions issue

**Solution**:
```bash
# Verify volume mount in docker-compose.yml
cat docker/docker-compose.yml | grep -A 2 volumes

# Check reports directory permissions
ls -la reports/

# Create reports directory if missing
mkdir -p reports/screenshots reports/traces
```

#### Issue: Container exits immediately without running tests

**Cause**: Syntax error in docker-compose.yml or Dockerfile

**Solution**:
```bash
# Validate docker-compose.yml syntax
docker-compose -f docker/docker-compose.yml config

# Check container logs
docker-compose -f docker/docker-compose.yml logs test-runner

# Run container interactively for debugging
docker run -it --rm test-automation-framework /bin/bash
```

#### Issue: Tests pass locally but fail in Docker

**Cause**: Environment differences (timing, display, network)

**Solution**:
1. Verify headless mode is enabled in Docker
2. Increase timeouts in `config.yaml`
3. Check base URL configuration
4. Review test logs for timing-related failures
5. Run tests with verbose output: `pytest -vv`

#### Issue: Docker build is very slow

**Cause**: Downloading large browser binaries, no build cache

**Solution**:
```bash
# Use Docker BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t test-automation-framework -f docker/Dockerfile .

# Ensure build cache is enabled (default)
docker build -t test-automation-framework -f docker/Dockerfile .
```

#### Issue: Permission denied when accessing reports

**Cause**: Container runs as root, creates files with root ownership

**Solution**:
```bash
# Change ownership of reports directory
sudo chown -R $USER:$USER reports/

# Or run container with current user ID (add to docker-compose.yml)
user: "${UID}:${GID}"
```

### Debugging Inside Container

For advanced troubleshooting, run an interactive shell inside the container:

```bash
# Start container with bash shell
docker run -it --rm test-automation-framework /bin/bash

# Inside container, you can:
# - Check installed packages: pip list
# - Verify browsers: which google-chrome firefox
# - Check Playwright: playwright --version
# - Run tests manually: pytest -v
# - Inspect configuration: cat config.yaml
```

### Viewing Container Logs

View logs from a running or stopped container:

```bash
# View logs from docker-compose
docker-compose -f docker/docker-compose.yml logs test-runner

# Follow logs in real-time
docker-compose -f docker/docker-compose.yml logs -f test-runner

# View logs from specific container
docker logs <container-id>
```

---

## Best Practices

### 1. Always Use Headless Mode in Docker

Browsers should always run in headless mode inside containers:
- Set `HEADLESS=true` in docker-compose.yml
- Set `headless: true` in config.yaml
- Avoid attempting to run headed browsers in containers

### 2. Mount Reports Directory

Always mount the `reports/` directory to retrieve test results:
```yaml
volumes:
  - ../reports:/app/reports
```

### 3. Use `--abort-on-container-exit` with `docker-compose up`

Ensure containers stop after test execution:
```bash
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

### 4. Clean Up Containers After Execution

Use `--rm` flag with `docker-compose run` to remove containers:
```bash
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest
```

### 5. Rebuild Image After Dependency Changes

Rebuild the Docker image when `requirements.txt` or `Dockerfile` changes:
```bash
docker-compose -f docker/docker-compose.yml build
```

### 6. Use Docker for CI/CD Pipelines

Run tests in Docker for consistent CI/CD execution:
- Same environment as local development
- No need to install dependencies on CI runners
- Reproducible test results

### 7. Tag Images with Versions

Tag Docker images with version numbers for tracking:
```bash
docker build -t test-automation-framework:v1.0.0 -f docker/Dockerfile .
```

### 8. Monitor Resource Usage

Monitor Docker resource usage to optimize performance:
```bash
# Check container resource usage
docker stats

# Check disk usage
docker system df
```

---

## Quick Reference

### Essential Commands

```bash
# Build Docker image
docker build -t test-automation-framework -f docker/Dockerfile .

# Run all tests with Docker Compose
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit

# Run specific tests
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest tests/selenium/

# Run tests by marker
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -m selenium

# Run tests in parallel
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest -n 4

# Run with custom browser
docker-compose -f docker/docker-compose.yml run --rm test-runner pytest --browser=firefox

# Rebuild image
docker-compose -f docker/docker-compose.yml build

# Clean up Docker resources
docker system prune -a

# View container logs
docker-compose -f docker/docker-compose.yml logs test-runner

# Interactive shell in container
docker run -it --rm test-automation-framework /bin/bash
```

### Docker Compose File Structure

```yaml
services:
  test-runner:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    volumes:
      - ../reports:/app/reports
    environment:
      - HEADLESS=true
    command: pytest
```

### Dockerfile Key Sections

```dockerfile
# Base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    firefox-esr \
    ...

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy application code
COPY . /app
WORKDIR /app

# Run tests
CMD ["pytest"]
```

---

## Additional Resources

- **Framework Overview**: See `.kiro/steering/framework-overview.md` for project structure and configuration
- **Test Writing Guide**: See `.kiro/steering/test-writing-guide.md` for test authoring conventions
- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **GitHub Actions with Docker**: https://docs.github.com/en/actions/using-containerized-services

---

## Summary

Docker execution provides:
- ✅ **Reproducible Environments**: Same environment across all machines
- ✅ **Isolated Execution**: No conflicts with host system dependencies
- ✅ **CI/CD Ready**: Easy integration with GitHub Actions, GitLab CI, etc.
- ✅ **Consistent Browser Versions**: Pre-installed browsers and drivers
- ✅ **Headless by Default**: Optimized for automated execution
- ✅ **Report Retrieval**: Volume mounts for accessing test results

Use Docker execution for:
- Running tests in CI/CD pipelines
- Ensuring consistent test environments across team
- Isolating test execution from host system
- Reproducing test failures in clean environment
- Validating framework setup before deployment

---

**Last Updated**: 2024
**Framework Version**: 0.1.0
