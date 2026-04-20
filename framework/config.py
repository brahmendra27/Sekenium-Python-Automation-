# framework/config.py

"""
Central configuration loader with .env support, YAML fallback, and validation.

Priority order:
  1. Environment variables (highest)
  2. .env file values
  3. config.yaml values
  4. Hardcoded defaults (lowest)
"""

from typing import Optional, Any
import yaml
import os
import logging

logger = logging.getLogger(__name__)

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Central configuration loader with .env support and validation."""

    VALID_BROWSERS = ['chrome', 'chromium', 'firefox', 'webkit', 'edge']

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Config from .env + YAML with validation.

        Args:
            config_path: Path to the configuration YAML file (default: config.yaml)
        """
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from YAML file.

        Returns:
            Dictionary containing configuration values, or empty dict if file doesn't exist
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value. Checks env vars first, then YAML, then default.

        Args:
            key: Configuration key to retrieve
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        # Check environment variable first (uppercase, underscored)
        env_key = key.upper().replace('.', '_').replace('-', '_')
        env_val = os.environ.get(env_key)
        if env_val is not None:
            return env_val

        # Fall back to YAML config
        return self._config.get(key, default)

    def validate(self) -> list:
        """Validate configuration and return list of issues.

        Returns:
            List of validation error strings. Empty list means valid.
        """
        issues = []

        # Validate base_url
        base_url = self.base_url
        if not base_url or base_url == 'http://localhost:8080':
            issues.append("base_url is not configured (using default localhost)")

        # Validate browser
        if self.browser.lower() not in self.VALID_BROWSERS:
            issues.append(
                f"Invalid browser '{self.browser}'. "
                f"Valid options: {', '.join(self.VALID_BROWSERS)}"
            )

        # Validate timeout
        if self.timeout <= 0:
            issues.append(f"timeout must be > 0, got {self.timeout}")

        # Validate API timeout
        if self.api_timeout <= 0:
            issues.append(f"api.timeout must be > 0, got {self.api_timeout}")

        if issues:
            for issue in issues:
                logger.warning(f"Config validation: {issue}")

        return issues

    # ==================== Core Settings ====================

    @property
    def base_url(self) -> str:
        """Get base URL. Checks BASE_URL env var first."""
        return os.environ.get('BASE_URL', self.get('base_url', 'http://localhost:8080'))

    @property
    def browser(self) -> str:
        """Get browser selection. Checks BROWSER env var first."""
        return os.environ.get('BROWSER', self.get('browser', 'chrome'))

    @property
    def headless(self) -> bool:
        """Get headless mode. Checks HEADLESS env var first."""
        env_val = os.environ.get('HEADLESS')
        if env_val is not None:
            return env_val.lower() in ('true', '1', 'yes')
        return self.get('headless', False)

    @property
    def timeout(self) -> int:
        """Get default timeout for element waits (seconds)."""
        env_val = os.environ.get('TIMEOUT')
        if env_val is not None:
            return int(env_val)
        return self.get('timeout', 30)

    @property
    def parallel_workers(self) -> int:
        """Get number of parallel workers for pytest-xdist."""
        return self.get('parallel_workers', 1)

    @property
    def report_dir(self) -> str:
        """Get report output directory."""
        return self.get('report_dir', 'reports')

    # ==================== API Configuration ====================

    @property
    def api_base_url(self) -> str:
        """Get API base URL. Checks API_BASE_URL env var first."""
        env_val = os.environ.get('API_BASE_URL')
        if env_val:
            return env_val
        api_config = self.get('api', {})
        return api_config.get('base_url', 'http://localhost:8080/api')

    @property
    def api_timeout(self) -> int:
        """Get API request timeout (seconds)."""
        env_val = os.environ.get('REQUEST_TIMEOUT')
        if env_val:
            return int(env_val)
        api_config = self.get('api', {})
        return api_config.get('timeout', 30)

    @property
    def api_verify_ssl(self) -> bool:
        """Get SSL verification setting for API requests."""
        api_config = self.get('api', {})
        return api_config.get('verify_ssl', True)

    @property
    def api_default_headers(self) -> dict:
        """Get default headers for API requests."""
        api_config = self.get('api', {})
        return api_config.get('default_headers', {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    @property
    def api_auth_type(self) -> str:
        """Get API authentication type (bearer, oauth2, basic, none)."""
        return os.environ.get('API_AUTH_TYPE', 'none')

    @property
    def api_auth_token(self) -> str:
        """Get API auth token from environment."""
        return os.environ.get('API_AUTH_TOKEN', '')

    # ==================== MongoDB Configuration ====================

    @property
    def mongodb_connection_string(self) -> str:
        """Get MongoDB connection string. Checks MONGODB_CONNECTION_STRING env var first."""
        return os.environ.get(
            'MONGODB_CONNECTION_STRING',
            self.get('mongodb', {}).get('connection_string', 'mongodb://localhost:27017')
        )

    @property
    def mongodb_database(self) -> str:
        """Get MongoDB database name."""
        return os.environ.get(
            'MONGODB_DATABASE',
            self.get('mongodb', {}).get('database', 'test_db')
        )

    @property
    def mongodb_timeout(self) -> int:
        """Get MongoDB connection timeout (milliseconds)."""
        return self.get('mongodb', {}).get('timeout', 5000)

    @property
    def mongodb_max_pool_size(self) -> int:
        """Get MongoDB connection pool size."""
        return self.get('mongodb', {}).get('max_pool_size', 10)
