# framework/config.py

from typing import Optional, Any
import yaml
import os


class Config:
    """Central configuration loader with fallback defaults."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Config and load configuration from YAML file.
        
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
        """Get configuration value with fallback to default.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key is not found
            
        Returns:
            Configuration value or default if key doesn't exist
        """
        return self._config.get(key, default)
    
    @property
    def base_url(self) -> str:
        """Get base URL for application under test.
        
        Returns:
            Base URL string (default: http://localhost:8080)
        """
        return self.get('base_url', 'http://localhost:8080')
    
    @property
    def browser(self) -> str:
        """Get browser selection.
        
        Returns:
            Browser name (default: chrome)
        """
        return self.get('browser', 'chrome')
    
    @property
    def headless(self) -> bool:
        """Get headless mode setting.
        
        Returns:
            True if headless mode enabled, False otherwise (default: False)
        """
        return self.get('headless', False)
    
    @property
    def timeout(self) -> int:
        """Get default timeout for element waits.
        
        Returns:
            Timeout in seconds (default: 30)
        """
        return self.get('timeout', 30)
    
    @property
    def parallel_workers(self) -> int:
        """Get number of parallel workers for pytest-xdist.
        
        Returns:
            Number of workers (default: 1 for sequential execution)
        """
        return self.get('parallel_workers', 1)
    
    @property
    def report_dir(self) -> str:
        """Get report output directory.
        
        Returns:
            Report directory path (default: reports)
        """
        return self.get('report_dir', 'reports')
    
    # API Testing Configuration
    @property
    def api_base_url(self) -> str:
        """Get API base URL.
        
        Returns:
            API base URL string
        """
        api_config = self.get('api', {})
        return api_config.get('base_url', 'http://localhost:8080/api')
    
    @property
    def api_timeout(self) -> int:
        """Get API request timeout.
        
        Returns:
            Timeout in seconds (default: 30)
        """
        api_config = self.get('api', {})
        return api_config.get('timeout', 30)
    
    @property
    def api_verify_ssl(self) -> bool:
        """Get SSL verification setting for API requests.
        
        Returns:
            True if SSL verification enabled (default: True)
        """
        api_config = self.get('api', {})
        return api_config.get('verify_ssl', True)
    
    @property
    def api_default_headers(self) -> dict:
        """Get default headers for API requests.
        
        Returns:
            Dictionary of default headers
        """
        api_config = self.get('api', {})
        return api_config.get('default_headers', {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    # MongoDB Configuration
    @property
    def mongodb_connection_string(self) -> str:
        """Get MongoDB connection string.
        
        Returns:
            MongoDB connection string
        """
        mongodb_config = self.get('mongodb', {})
        return mongodb_config.get('connection_string', 'mongodb://localhost:27017')
    
    @property
    def mongodb_database(self) -> str:
        """Get MongoDB database name.
        
        Returns:
            Database name (default: test_db)
        """
        mongodb_config = self.get('mongodb', {})
        return mongodb_config.get('database', 'test_db')
    
    @property
    def mongodb_timeout(self) -> int:
        """Get MongoDB connection timeout.
        
        Returns:
            Timeout in milliseconds (default: 5000)
        """
        mongodb_config = self.get('mongodb', {})
        return mongodb_config.get('timeout', 5000)
    
    @property
    def mongodb_max_pool_size(self) -> int:
        """Get MongoDB connection pool size.
        
        Returns:
            Max pool size (default: 10)
        """
        mongodb_config = self.get('mongodb', {})
        return mongodb_config.get('max_pool_size', 10)
