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
