# tests/test_selenium_driver.py

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from framework.selenium_driver import SeleniumDriver


class TestSeleniumDriver:
    """Unit tests for SeleniumDriver class."""
    
    def test_chrome_driver_initialization(self):
        """Test Chrome driver initialization with correct options."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_chrome.return_value = mock_driver
            
            # Initialize Chrome driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver = driver_wrapper.initialize()
            
            # Verify Chrome was called
            assert mock_chrome.called
            assert driver == mock_driver
            assert driver_wrapper.driver == mock_driver
            
            # Verify ChromeOptions were configured
            call_kwargs = mock_chrome.call_args[1]
            options = call_kwargs['options']
            
            # Check that required arguments are present
            assert '--no-sandbox' in options.arguments
            assert '--disable-dev-shm-usage' in options.arguments
            assert '--headless' not in options.arguments  # headless=False
    
    def test_chrome_driver_initialization_headless(self):
        """Test Chrome driver initialization in headless mode."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_chrome.return_value = mock_driver
            
            # Initialize Chrome driver in headless mode
            driver_wrapper = SeleniumDriver(browser='chrome', headless=True)
            driver = driver_wrapper.initialize()
            
            # Verify Chrome was called
            assert mock_chrome.called
            assert driver == mock_driver
            
            # Verify headless option was set
            call_kwargs = mock_chrome.call_args[1]
            options = call_kwargs['options']
            assert '--headless' in options.arguments
    
    def test_firefox_driver_initialization(self):
        """Test Firefox driver initialization with correct options."""
        with patch('framework.selenium_driver.webdriver.Firefox') as mock_firefox, \
             patch('framework.selenium_driver.GeckoDriverManager') as mock_manager, \
             patch('framework.selenium_driver.FirefoxService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/geckodriver'
            mock_driver = Mock()
            mock_firefox.return_value = mock_driver
            
            # Initialize Firefox driver
            driver_wrapper = SeleniumDriver(browser='firefox', headless=False)
            driver = driver_wrapper.initialize()
            
            # Verify Firefox was called
            assert mock_firefox.called
            assert driver == mock_driver
            assert driver_wrapper.driver == mock_driver
            
            # Verify FirefoxOptions were configured
            call_kwargs = mock_firefox.call_args[1]
            options = call_kwargs['options']
            
            # Check that headless is not set
            assert '--headless' not in options.arguments
    
    def test_firefox_driver_initialization_headless(self):
        """Test Firefox driver initialization in headless mode."""
        with patch('framework.selenium_driver.webdriver.Firefox') as mock_firefox, \
             patch('framework.selenium_driver.GeckoDriverManager') as mock_manager, \
             patch('framework.selenium_driver.FirefoxService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/geckodriver'
            mock_driver = Mock()
            mock_firefox.return_value = mock_driver
            
            # Initialize Firefox driver in headless mode
            driver_wrapper = SeleniumDriver(browser='firefox', headless=True)
            driver = driver_wrapper.initialize()
            
            # Verify Firefox was called
            assert mock_firefox.called
            assert driver == mock_driver
            
            # Verify headless option was set
            call_kwargs = mock_firefox.call_args[1]
            options = call_kwargs['options']
            assert '--headless' in options.arguments
    
    def test_unsupported_browser_raises_value_error(self):
        """Test that unsupported browser raises ValueError with descriptive message."""
        driver_wrapper = SeleniumDriver(browser='safari', headless=False)
        
        with pytest.raises(ValueError) as exc_info:
            driver_wrapper.initialize()
        
        # Verify error message contains browser name and supported browsers
        error_message = str(exc_info.value)
        assert 'safari' in error_message.lower()
        assert 'chrome' in error_message.lower()
        assert 'firefox' in error_message.lower()
        assert 'Unsupported browser' in error_message
    
    def test_browser_name_case_insensitive(self):
        """Test that browser name is case-insensitive."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_chrome.return_value = mock_driver
            
            # Test with uppercase browser name
            driver_wrapper = SeleniumDriver(browser='CHROME', headless=False)
            driver = driver_wrapper.initialize()
            
            # Verify Chrome was called
            assert mock_chrome.called
            assert driver == mock_driver
    
    def test_driver_initialization_failure_raises_runtime_error(self):
        """Test that driver initialization failure raises RuntimeError with browser details."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks to raise exception
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_chrome.side_effect = Exception('WebDriver initialization failed')
            
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            
            with pytest.raises(RuntimeError) as exc_info:
                driver_wrapper.initialize()
            
            # Verify error message contains browser name and error details
            error_message = str(exc_info.value)
            assert 'chrome' in error_message.lower()
            assert 'Failed to initialize' in error_message
            assert 'WebDriver initialization failed' in error_message
    
    def test_quit_closes_driver_session(self):
        """Test that quit method closes the driver session."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_chrome.return_value = mock_driver
            
            # Initialize and quit driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            driver_wrapper.quit()
            
            # Verify quit was called on driver
            assert mock_driver.quit.called
            assert driver_wrapper.driver is None
    
    def test_quit_without_initialization(self):
        """Test that quit method handles case when driver is not initialized."""
        driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
        
        # Should not raise exception
        driver_wrapper.quit()
        assert driver_wrapper.driver is None
    
    def test_quit_handles_exception_gracefully(self):
        """Test that quit method handles exceptions during driver quit."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.quit.side_effect = Exception('Quit failed')
            mock_chrome.return_value = mock_driver
            
            # Initialize and quit driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            
            # Should not raise exception, but should print error
            driver_wrapper.quit()
            assert driver_wrapper.driver is None
    
    def test_capture_screenshot_success(self):
        """Test successful screenshot capture."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.save_screenshot.return_value = True
            mock_chrome.return_value = mock_driver
            
            # Initialize driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            
            # Create temporary directory for screenshot
            with tempfile.TemporaryDirectory() as temp_dir:
                screenshot_path = os.path.join(temp_dir, 'screenshots', 'test.png')
                
                # Capture screenshot
                result = driver_wrapper.capture_screenshot(screenshot_path)
                
                # Verify screenshot was captured
                assert result is True
                assert mock_driver.save_screenshot.called
                assert mock_driver.save_screenshot.call_args[0][0] == screenshot_path
    
    def test_capture_screenshot_creates_directory(self):
        """Test that capture_screenshot creates directory if it doesn't exist."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.save_screenshot.return_value = True
            mock_chrome.return_value = mock_driver
            
            # Initialize driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            
            # Create temporary directory for screenshot
            with tempfile.TemporaryDirectory() as temp_dir:
                screenshot_path = os.path.join(temp_dir, 'new_dir', 'screenshots', 'test.png')
                
                # Capture screenshot
                result = driver_wrapper.capture_screenshot(screenshot_path)
                
                # Verify directory was created
                assert result is True
                assert os.path.exists(os.path.dirname(screenshot_path))
    
    def test_capture_screenshot_without_driver(self):
        """Test that capture_screenshot returns False when driver is not initialized."""
        driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
        
        # Try to capture screenshot without initializing driver
        result = driver_wrapper.capture_screenshot('/tmp/test.png')
        
        # Verify screenshot capture failed
        assert result is False
    
    def test_capture_screenshot_handles_exception(self):
        """Test that capture_screenshot handles exceptions gracefully."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.save_screenshot.side_effect = Exception('Screenshot failed')
            mock_chrome.return_value = mock_driver
            
            # Initialize driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            
            # Try to capture screenshot
            result = driver_wrapper.capture_screenshot('/tmp/test.png')
            
            # Verify screenshot capture failed gracefully
            assert result is False
    
    def test_capture_screenshot_with_empty_directory(self):
        """Test that capture_screenshot handles filepath with no directory."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.save_screenshot.return_value = True
            mock_chrome.return_value = mock_driver
            
            # Initialize driver
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            driver_wrapper.initialize()
            
            # Capture screenshot with no directory path
            result = driver_wrapper.capture_screenshot('test.png')
            
            # Verify screenshot was captured
            assert result is True
            assert mock_driver.save_screenshot.called
    
    def test_initialization_attributes(self):
        """Test that SeleniumDriver initializes with correct attributes."""
        driver_wrapper = SeleniumDriver(browser='firefox', headless=True)
        
        assert driver_wrapper.browser == 'firefox'
        assert driver_wrapper.headless is True
        assert driver_wrapper.driver is None
    
    def test_default_initialization_values(self):
        """Test that SeleniumDriver uses default values when not specified."""
        driver_wrapper = SeleniumDriver()
        
        assert driver_wrapper.browser == 'chrome'
        assert driver_wrapper.headless is False
        assert driver_wrapper.driver is None
    
    def test_runtime_error_includes_browser_version(self):
        """Test that RuntimeError includes browser version when available."""
        with patch('framework.selenium_driver.webdriver.Chrome') as mock_chrome, \
             patch('framework.selenium_driver.ChromeDriverManager') as mock_manager, \
             patch('framework.selenium_driver.ChromeService') as mock_service:
            
            # Setup mocks
            mock_manager.return_value.install.return_value = '/path/to/chromedriver'
            mock_driver = Mock()
            mock_driver.capabilities = {'browserVersion': '120.0.6099.109'}
            
            # Make Chrome initialization fail after driver is partially initialized
            def side_effect(*args, **kwargs):
                # Set the driver before raising exception
                driver_wrapper.driver = mock_driver
                raise Exception('Driver initialization failed')
            
            mock_chrome.side_effect = side_effect
            
            driver_wrapper = SeleniumDriver(browser='chrome', headless=False)
            
            with pytest.raises(RuntimeError) as exc_info:
                driver_wrapper.initialize()
            
            # Verify error message contains browser version
            error_message = str(exc_info.value)
            assert 'Browser version' in error_message or 'browser version' in error_message.lower()
