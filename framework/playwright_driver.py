# framework/playwright_driver.py

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright, Playwright
from typing import Optional, Literal
import os


BrowserType = Literal["chromium", "firefox", "webkit"]


class PlaywrightDriver:
    """Playwright browser wrapper with tracing support."""
    
    def __init__(
        self,
        browser_type: BrowserType = "chromium",
        headless: bool = False,
        slow_mo: int = 0,
        tracing: bool = False
    ):
        """Initialize PlaywrightDriver with browser and configuration options.
        
        Args:
            browser_type: Browser to use - 'chromium', 'firefox', or 'webkit' (default: chromium)
            headless: Whether to run browser in headless mode (default: False)
            slow_mo: Slow down operations by N milliseconds (default: 0)
            tracing: Enable tracing with screenshots and snapshots (default: False)
        """
        self.browser_type = browser_type
        self.headless = headless
        self.slow_mo = slow_mo
        self.tracing = tracing
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    def initialize(self) -> BrowserContext:
        """Initialize Playwright browser and context.
        
        Returns:
            Initialized BrowserContext instance
            
        Raises:
            ValueError: If unsupported browser type is specified
            RuntimeError: If browser initialization fails with descriptive error
        """
        try:
            self.playwright = sync_playwright().start()
            
            if self.browser_type == "chromium":
                self.browser = self.playwright.chromium.launch(
                    headless=self.headless,
                    slow_mo=self.slow_mo
                )
            elif self.browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(
                    headless=self.headless,
                    slow_mo=self.slow_mo
                )
            elif self.browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(
                    headless=self.headless,
                    slow_mo=self.slow_mo
                )
            else:
                raise ValueError(
                    f"Unsupported browser: {self.browser_type}. "
                    f"Supported: chromium, firefox, webkit"
                )
            
            self.context = self.browser.new_context()
            
            # Start tracing with screenshots and snapshots if enabled
            if self.tracing:
                self.context.tracing.start(screenshots=True, snapshots=True)
            
            return self.context
        
        except ValueError:
            # Re-raise ValueError as-is (unsupported browser)
            raise
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Playwright {self.browser_type} browser. "
                f"Error: {str(e)}"
            )
    
    def quit(self, trace_path: Optional[str] = None):
        """Tear down Playwright browser and context.
        
        Args:
            trace_path: Optional path to save trace file if tracing is enabled
        """
        if self.context:
            # Save trace file if tracing was enabled and path is provided
            if self.tracing and trace_path:
                try:
                    # Create directory if it doesn't exist
                    directory = os.path.dirname(trace_path)
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    
                    self.context.tracing.stop(path=trace_path)
                except Exception as e:
                    print(f"Failed to save trace: {e}")
            
            try:
                self.context.close()
            except Exception as e:
                print(f"Error during context close: {e}")
            finally:
                self.context = None
        
        if self.browser:
            try:
                self.browser.close()
            except Exception as e:
                print(f"Error during browser close: {e}")
            finally:
                self.browser = None
        
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception as e:
                print(f"Error during playwright stop: {e}")
            finally:
                self.playwright = None
    
    def capture_screenshot(self, page: Page, filepath: str) -> bool:
        """Capture screenshot from page to specified filepath.
        
        Args:
            page: Playwright Page object to capture screenshot from
            filepath: Path where screenshot should be saved
            
        Returns:
            True if screenshot was captured successfully, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            page.screenshot(path=filepath, full_page=True)
            return True
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
            return False
