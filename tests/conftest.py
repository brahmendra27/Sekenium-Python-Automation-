# tests/conftest.py

import pytest
import os
from datetime import datetime
from framework.config import Config


def pytest_addoption(parser):
    """Add custom command-line options for test execution.
    
    This hook allows users to override configuration values via CLI arguments,
    providing flexibility for different test environments and scenarios.
    
    The following CLI options are available for configuration override:
    - --browser: Browser selection (provided by pytest-playwright plugin)
    - --headless: Run in headless mode (added by this conftest)
    - --base-url: Base URL for tests (provided by pytest-base-url plugin)
    
    Args:
        parser: Pytest command-line parser
    """
    # Add --headless option (not provided by standard plugins)
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browsers in headless mode"
    )


@pytest.fixture(scope="session", autouse=True)
def configure_from_cli(request):
    """Override configuration from command-line options.
    
    This fixture runs automatically before any tests and updates the global
    configuration with values provided via CLI arguments. CLI arguments take
    precedence over config.yaml values.
    
    Args:
        request: Pytest request object for accessing CLI options
    """
    config = Config()
    
    # Override config with CLI options if provided
    browser = request.config.getoption("--browser")
    if browser is not None:
        config._config['browser'] = browser
    
    headless = request.config.getoption("--headless")
    if headless is not None:
        config._config['headless'] = headless
    
    base_url = request.config.getoption("--base-url")
    if base_url is not None:
        config._config['base_url'] = base_url


@pytest.fixture(scope="session", autouse=True)
def setup_reports():
    """Ensure report directories exist before test run.
    
    This fixture runs automatically before any tests and creates the necessary
    directory structure for reports, screenshots, and traces if they don't exist.
    """
    config = Config()
    report_dir = config.report_dir
    
    # Create report directory structure
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(f"{report_dir}/screenshots", exist_ok=True)
    os.makedirs(f"{report_dir}/traces", exist_ok=True)


def pytest_configure(config):
    """Configure pytest with dynamic report paths from configuration.
    
    This hook runs during pytest initialization and sets report output paths
    based on the application configuration, ensuring reports are written to
    the correct location.
    
    Args:
        config: Pytest config object
    """
    # Load application configuration
    app_config = Config()
    
    # Set report paths dynamically from config
    config.option.htmlpath = f"{app_config.report_dir}/report.html"
    config.option.json_report_file = f"{app_config.report_dir}/report.json"


def pytest_html_report_title(report):
    """Customize HTML report title.
    
    Args:
        report: pytest-html report object
    """
    report.title = "Test Automation Framework - Execution Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary section to HTML report.
    
    This hook adds framework branding and execution timestamp to the top
    of the HTML report for better context and traceability.
    
    Args:
        prefix: List to prepend content to summary
        summary: Summary content
        postfix: List to append content to summary
    """
    prefix.extend([
        "<h2>Test Automation Framework</h2>",
        f"<p>Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
    ])
