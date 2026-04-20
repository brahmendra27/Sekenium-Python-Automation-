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
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                
                # Try multiple approaches to initialize Chrome
                driver_initialized = False
                last_error = None
                
                # Approach 1: Try webdriver-manager with cache
                try:
                    print("Attempting to initialize Chrome with webdriver-manager...")
                    service = ChromeService(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    driver_initialized = True
                    print("✓ Chrome initialized successfully with webdriver-manager")
                except Exception as e1:
                    last_error = e1
                    print(f"✗ webdriver-manager failed: {e1}")
                
                # Approach 2: Try webdriver-manager with fresh download
                if not driver_initialized:
                    try:
                        print("Attempting fresh Chrome driver download...")
                        from webdriver_manager.core.os_manager import ChromeType
                        service = ChromeService(
                            ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                        )
                        self.driver = webdriver.Chrome(service=service, options=options)
                        driver_initialized = True
                        print("✓ Chrome initialized with fresh download")
                    except Exception as e2:
                        last_error = e2
                        print(f"✗ Fresh download failed: {e2}")
                
                # Approach 3: Try system Chrome driver
                if not driver_initialized:
                    try:
                        print("Attempting to use system Chrome driver...")
                        self.driver = webdriver.Chrome(options=options)
                        driver_initialized = True
                        print("✓ Chrome initialized with system driver")
                    except Exception as e3:
                        last_error = e3
                        print(f"✗ System driver failed: {e3}")
                
                if not driver_initialized:
                    raise last_error
            
            elif self.browser == "firefox":
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
                
                # Try multiple approaches for Firefox
                driver_initialized = False
                last_error = None
                
                # Approach 1: Try webdriver-manager
                try:
                    print("Attempting to initialize Firefox with webdriver-manager...")
                    service = FirefoxService(GeckoDriverManager().install())
                    self.driver = webdriver.Firefox(service=service, options=options)
                    driver_initialized = True
                    print("✓ Firefox initialized successfully")
                except Exception as e1:
                    last_error = e1
                    print(f"✗ webdriver-manager failed: {e1}")
                
                # Approach 2: Try system Firefox driver
                if not driver_initialized:
                    try:
                        print("Attempting to use system Firefox driver...")
                        self.driver = webdriver.Firefox(options=options)
                        driver_initialized = True
                        print("✓ Firefox initialized with system driver")
                    except Exception as e2:
                        last_error = e2
                        print(f"✗ System driver failed: {e2}")
                
                if not driver_initialized:
                    raise last_error
            
            else:
                raise ValueError(
                    f"Unsupported browser: {self.browser}. Supported: chrome, firefox"
                )
            
            # Set implicit wait
            self.driver.implicitly_wait(10)
            
            return self.driver
        
        except ValueError:
            # Re-raise ValueError as-is (unsupported browser)
            raise
        except Exception as e:
            # Get browser version info if driver was partially initialized
            browser_version = "unknown"
            driver_error = str(e)
            
            try:
                if self.driver:
                    browser_version = self.driver.capabilities.get('browserVersion', 'unknown')
            except:
                pass
            
            # Provide helpful error message
            error_msg = (
                f"Failed to initialize {self.browser} WebDriver. Browser version: {browser_version}. "
                f"Check browser and driver version compatibility.\n\n"
                f"Quick fixes:\n"
                f"1. Update webdriver-manager: pip install --upgrade webdriver-manager selenium\n"
                f"2. Use Firefox instead: pytest --browser=firefox\n"
                f"3. Install/update Chrome browser\n"
                f"4. Clear webdriver cache: rm -rf ~/.wdm\n\n"
                f"Error details: {driver_error}"
            )
            
            raise RuntimeError(error_msg)
    
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
