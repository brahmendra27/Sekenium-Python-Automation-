# Test Automation Framework

A unified Python-based test automation framework supporting both Selenium WebDriver and Playwright browser automation, with pytest as the test runner. Built for team collaboration with Docker containerization, GitHub Actions CI/CD, and deep Kiro IDE integration.

## Key Features

- **Dual Driver Support**: Write tests using Selenium WebDriver or Playwright (Python)
- **Unified Test Runner**: Single pytest-based execution model for all tests
- **AI Self-Healing**: Automatic element locator healing with multiple fallback strategies (NEW!)
- **Automated Reporting**: HTML and JSON reports with embedded screenshots and traces
- **Docker Ready**: Reproducible test execution in containerized environments
- **CI/CD Integration**: GitHub Actions workflow with automated test execution and artifact uploads
- **Kiro IDE Integration**: Steering files and hooks for AI-assisted test authoring and healing
- **Parallel Execution**: Run tests concurrently with pytest-xdist
- **Flexible Configuration**: YAML-based config with CLI overrides

## Prerequisites

- **Python 3.11+** (Python 3.11 or higher)
- **Docker** (optional, for containerized execution)
- **Git** (for cloning the repository)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd test-automation-framework
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

### 5. Verify Installation

```bash
# Run example tests
pytest tests/selenium/test_example_selenium.py tests/playwright/test_example_playwright.py
```

## Execution Commands

### Run All Tests

```bash
pytest
```

### Run by Driver Type

```bash
# Run only Selenium tests
pytest -m selenium

# Run only Playwright tests
pytest -m playwright
```

### Run Specific Test File

```bash
pytest tests/selenium/test_example_selenium.py
```

### Run with Parallel Execution

```bash
# Run with 4 parallel workers
pytest -n 4
```

### CLI Options

```bash
# Run in headless mode
pytest --headless

# Run with specific browser
pytest --browser=firefox

# Run with custom base URL
pytest --base-url=https://example.com

# Combine options
pytest -m selenium --headless --browser=chrome -n 2
```

### Run by Test Markers

```bash
# Run smoke tests only
pytest -m smoke

# Run regression suite
pytest -m regression
```

## Docker Execution

Docker provides a reproducible, isolated environment for test execution.

### Build Docker Image

```bash
docker build -t test-automation-framework -f docker/Dockerfile .
```

### Run Tests with Docker Compose

```bash
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

### Run Tests with Docker (Manual)

```bash
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -e HEADLESS=true \
  test-automation-framework:latest \
  pytest --headless
```

**Note**: First build takes 5-10 minutes (downloads browsers). Subsequent builds are faster due to Docker layer caching.

For detailed Docker instructions, see [`docker/README.md`](docker/README.md).

## Report Locations

After test execution, reports are generated in the `reports/` directory:

- **HTML Report**: `reports/report.html` - Human-readable report with embedded screenshots
- **JSON Report**: `reports/report.json` - Machine-readable report for automation
- **Screenshots**: `reports/screenshots/` - Screenshots captured on test failures
- **Traces**: `reports/traces/` - Playwright trace files for debugging (`.zip` format)

### Viewing Reports

```bash
# Open HTML report in browser
# On Windows:
start reports/report.html
# On Linux:
xdg-open reports/report.html
# On Mac:
open reports/report.html
```

### Viewing Playwright Traces

```bash
# View trace file in Playwright Trace Viewer
playwright show-trace reports/traces/<test-name>.zip
```

## Configuration

### config.yaml

The `config.yaml` file contains default configuration values:

```yaml
base_url: "http://localhost:8080"
browser: "chrome"  # chrome, firefox, chromium, webkit
headless: false
timeout: 30
parallel_workers: 1
report_dir: "reports"

selenium:
  implicit_wait: 10
  page_load_timeout: 60

playwright:
  slow_mo: 0
  tracing: true
```

### CLI Overrides

Command-line options override `config.yaml` values:

```bash
pytest --browser=firefox --headless --base-url=https://staging.example.com
```

## Project Structure

```
test-automation-framework/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions CI pipeline
├── .kiro/
│   ├── hooks/                    # Kiro IDE automation hooks
│   └── steering/                 # Kiro IDE guidance files
├── tests/
│   ├── selenium/                 # Selenium WebDriver tests
│   │   ├── conftest.py           # Selenium fixtures
│   │   └── test_example_selenium.py
│   ├── playwright/               # Playwright tests
│   │   ├── conftest.py           # Playwright fixtures
│   │   └── test_example_playwright.py
│   └── conftest.py               # Shared pytest configuration
├── framework/
│   ├── config.py                 # Configuration loader
│   ├── selenium_driver.py        # Selenium WebDriver wrapper
│   ├── playwright_driver.py      # Playwright browser wrapper
│   └── report_utils.py           # Report generation utilities
├── docker/
│   ├── Dockerfile                # Docker image definition
│   ├── docker-compose.yml        # Docker Compose service
│   └── README.md                 # Docker execution guide
├── reports/                      # Generated test reports (gitignored)
├── config.yaml                   # Central configuration file
├── requirements.txt              # Python dependencies
├── pytest.ini                    # pytest configuration
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guidelines
└── CHANGELOG.md                  # Version history
```

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new tests
- Updating configuration
- Submitting pull requests
- Code style and testing guidelines

## GitHub Actions CI

The framework includes a GitHub Actions workflow that:

- Triggers on pull requests and pushes to `main`
- Builds the Docker image with layer caching
- Runs the full test suite in a container
- Uploads HTML/JSON reports and artifacts
- Marks the workflow as failed if tests fail

View workflow runs in the **Actions** tab of the GitHub repository.

## Kiro IDE Integration

The framework includes steering files and hooks for AI-assisted development:

- **Steering Files**: Provide contextual guidance for test authoring (`.kiro/steering/`)
- **Hooks**: Automate repetitive tasks like scaffolding tests and reviewing code (`.kiro/hooks/`)
- **AI Self-Healing**: Automatic element locator healing when selectors fail (NEW!)

For details, see:
- `.kiro/steering/framework-overview.md` - Framework overview
- `KIRO_INTEGRATION_FAQ.md` - 36 Q&A about Kiro integration
- `AI_SELF_HEALING_GUIDE.md` - Self-healing capabilities (NEW!)

## Troubleshooting

### Tests fail with "WebDriver not found"

**Solution**: Install browser drivers using webdriver-manager (included in requirements.txt) or install Playwright browsers:

```bash
playwright install
```

### Reports not generated

**Solution**: Ensure the `reports/` directory exists or let pytest create it automatically. Check pytest output for errors.

### Docker build fails

**Solution**: Check internet connectivity and Docker daemon status. Verify `requirements.txt` is valid.

### Tests pass locally but fail in Docker

**Solution**: Ensure tests are compatible with headless mode. Review Docker logs:

```bash
docker logs test-automation-framework
```

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
3. Check Docker-specific issues in [`docker/README.md`](docker/README.md)
4. Open an issue using the pilot feedback template

## License

[Add your license information here]

## Version

Current version: **v0.1.0** (See [CHANGELOG.md](CHANGELOG.md) for version history)
