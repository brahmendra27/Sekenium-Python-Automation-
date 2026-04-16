# Changelog

All notable changes to the Test Automation Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional browser support (Edge, Safari)
- Visual regression testing capabilities
- API testing integration
- Performance testing metrics
- Enhanced reporting with historical trends
- Test data management utilities

---

## [0.1.0] - 2024-01-15

### Added

#### Core Framework
- **Unified Test Runner**: pytest-based execution model supporting both Selenium and Playwright tests
- **Configuration Management**: YAML-based configuration (`config.yaml`) with CLI overrides
- **Dual Driver Support**: 
  - Selenium WebDriver with Chrome and Firefox support
  - Playwright with Chromium, Firefox, and WebKit support
- **Automatic Driver Management**: webdriver-manager for Selenium, built-in browser management for Playwright

#### Test Execution Features
- **Parallel Execution**: pytest-xdist integration for concurrent test execution
- **Headless Mode**: Support for headless browser execution (local and CI)
- **Test Markers**: Filtering by driver type (selenium, playwright), test type (smoke, regression)
- **CLI Options**: Command-line overrides for browser, headless mode, and base URL
- **Timeout Configuration**: Configurable timeouts for element waits and page loads

#### Reporting
- **HTML Reports**: pytest-html integration with embedded screenshots
- **JSON Reports**: Machine-readable pytest-json-report output
- **Screenshot Capture**: Automatic screenshot capture on test failure (Selenium and Playwright)
- **Trace Files**: Playwright trace capture on failure for post-mortem debugging
- **Report Utilities**: Helper functions for report directory management and summary generation

#### Fixtures
- **Selenium Fixtures**: `selenium_driver` fixture with automatic WebDriver initialization and teardown
- **Playwright Fixtures**: `playwright_context` and `playwright_page` fixtures with browser context management
- **Shared Configuration**: Session-scoped fixtures for configuration loading and report setup

#### Docker Support
- **Dockerfile**: Multi-stage Docker image with Python 3.11, browsers, and dependencies
- **Docker Compose**: Service definition for running tests in containers
- **Volume Mounts**: Report directory mounted to host for artifact retrieval
- **Headless Execution**: Automatic headless mode in Docker environment
- **Exit Code Propagation**: Container returns pytest exit code for CI integration

#### CI/CD Integration
- **GitHub Actions Workflow**: Automated test execution on pull requests and pushes to main
- **Docker Layer Caching**: GitHub Actions cache integration for faster builds
- **Artifact Uploads**: HTML/JSON reports, screenshots, and traces uploaded as workflow artifacts
- **Failure Detection**: Workflow marked as failed when tests fail

#### Kiro IDE Integration
- **Steering Files**:
  - `test-writing-guide.md`: Conventions for writing Selenium and Playwright tests
  - `framework-overview.md`: Project structure, fixtures, configuration, and CLI options
  - `docker-execution.md`: Docker build and execution instructions
- **Hooks**:
  - `test-file-review.json`: Reviews test files for framework convention violations
  - `report-summary.json`: Summarizes test execution reports and highlights failures
  - `scaffold-test.json`: Scaffolds new test files with correct imports and structure

#### Documentation
- **README.md**: Project overview, setup instructions, execution commands, and troubleshooting
- **CONTRIBUTING.md**: Guidelines for adding tests, updating configuration, and submitting PRs
- **CHANGELOG.md**: Version history and release notes (this file)
- **Docker README**: Detailed Docker execution guide with troubleshooting

#### Example Tests
- **Selenium Example**: `tests/selenium/test_example_selenium.py` demonstrating Selenium test structure
- **Playwright Example**: `tests/playwright/test_example_playwright.py` demonstrating Playwright test structure

#### Project Structure
- Organized directory layout: `tests/`, `framework/`, `reports/`, `.kiro/`, `.github/`, `docker/`
- `.gitignore` configuration excluding virtual environments, reports, and build artifacts
- `requirements.txt` with pinned dependency versions
- `pytest.ini` with test discovery patterns, markers, and report configuration

### Framework Components
- `framework/config.py`: Configuration loader with YAML parsing and property accessors
- `framework/selenium_driver.py`: Selenium WebDriver wrapper with automatic driver management
- `framework/playwright_driver.py`: Playwright browser wrapper with tracing support
- `framework/report_utils.py`: Report generation utilities and directory management

### Testing
- Unit tests for all framework components (Config, SeleniumDriver, PlaywrightDriver, ReportUtils)
- Integration tests for test runner configuration and CLI options
- Example tests demonstrating correct usage patterns

### Requirements Satisfied
- **Requirement 1**: Project structure and repository layout
- **Requirement 2**: Selenium test execution with Chrome/Firefox support
- **Requirement 3**: Playwright test execution with Chromium/Firefox/WebKit support
- **Requirement 4**: Unified pytest-based test runner with filtering and parallelization
- **Requirement 5**: Automated HTML and JSON report generation with screenshots
- **Requirement 6**: Kiro steering files for AI-assisted test authoring
- **Requirement 7**: Kiro IDE hooks for automation and code review
- **Requirement 8**: Docker-based test execution with reproducible environments
- **Requirement 9**: GitHub Actions CI pipeline with automated testing
- **Requirement 10**: Team collaboration readiness with documentation and examples

---

## Version History

### Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality in a backwards-compatible manner
- **PATCH** version: Backwards-compatible bug fixes

### Release Types

- **[Unreleased]**: Changes in development, not yet released
- **[X.Y.Z]**: Released version with date

---

## How to Update This Changelog

When contributing changes, update the `[Unreleased]` section with your changes under the appropriate category:

### Categories

- **Added**: New features, tests, or capabilities
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed in future versions
- **Removed**: Features that have been removed
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

### Example Entry

```markdown
## [Unreleased]

### Added
- New API testing module with REST client support
- Support for Edge browser in Selenium tests

### Fixed
- Resolved timeout issue in Playwright checkout test
- Fixed screenshot capture on Windows paths
```

When a release is made, move the `[Unreleased]` changes to a new version section with the release date.

---

## Links

- [Repository](https://github.com/your-org/test-automation-framework)
- [Issue Tracker](https://github.com/your-org/test-automation-framework/issues)
- [Contributing Guidelines](CONTRIBUTING.md)
- [README](README.md)
