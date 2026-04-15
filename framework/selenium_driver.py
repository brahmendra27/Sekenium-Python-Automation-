# framework/selenium_driver.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Optional
import os


class SeleniumDriver:
    """Selenium WebDriver wrapper with automatic driver management."""
    
    def __init__(self, browser: str = "chrome", headless: bool = False):
        """Initialize SeleniumDriver with browser and headless configuration.
        
        Args:
            browser: Browser to use - 'chrome' or 'firefox' (default: chrome)
            headless: Whether to run browser in headless mode (default: False)
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver: Optional[webdriver.Remote] = None
    
    def initialize(self) -> webdriver.Remote:
        """Initialize WebDriver based on browser configuration.
        
        Returns:
            Initialized WebDriver instance
            
        Raises:
            ValueError: If unsupported browser is specified
            RuntimeError: If driver initialization fails with browser/version details
        """
        try:
            if self.browser == "chrome":
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            elif self.browser == "firefox":
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            
            else:
                raise ValueError(
                    f"Unsupported browser: {self.browser}. Supported: chrome, firefox"
                )
            
            return self.driver
        
        except ValueError:
            # Re-raise ValueError as-is (unsupported browser)
            raise
        except Exception as e:
            # Get browser version info if driver was partially initialized
            browser_version = "unknown"
            try:
                if self.driver:
                    browser_version = self.driver.capabilities.get('browserVersion', 'unknown')
            except:
                pass
            
            raise RuntimeError(
                f"Failed to initialize {self.browser} WebDriver. "
                f"Browser version: {browser_version}. "
                f"Check browser and driver version compatibility. "
                f"Error: {str(e)}"
            )
    
    def quit(self):
        """Tear down WebDriver session and clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error during driver quit: {e}")
            finally:
                self.driver = None
    
    def capture_screenshot(self, filepath: str) -> bool:
        """Capture screenshot to specified filepath.
        
        Args:
            filepath: Path where screenshot should be saved
            
        Returns:
            True if screenshot was captured successfully, False otherwise
        """
        if self.driver:
            try:
                # Create directory if it doesn't exist
                directory = os.path.dirname(filepath)
                if directory:
                    os.makedirs(directory, exist_ok=True)
                
                self.driver.save_screenshot(filepath)
                return True
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
                return False
        return False
