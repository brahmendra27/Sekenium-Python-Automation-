# tests/test_playwright_driver.py

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from framework.playwright_driver import PlaywrightDriver


class TestPlaywrightDriver:
    """Unit tests for PlaywrightDriver class."""
    
    def test_chromium_driver_initialization(self):
        """Test Chromium driver initialization with correct options."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize Chromium driver
            driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
            context = driver_wrapper.initialize()
            
            # Verify Chromium was called with correct options
            assert mock_playwright.chromium.launch.called
            call_kwargs = mock_playwright.chromium.launch.call_args[1]
            assert call_kwargs['headless'] is False
            assert call_kwargs['slow_mo'] == 0
            
            # Verify context was created
            assert context == mock_context
            assert driver_wrapper.context == mock_context
            assert driver_wrapper.browser == mock_browser
    
    def test_chromium_driver_initialization_headless(self):
        """Test Chromium driver initialization in headless mode."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize Chromium driver in headless mode
            driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=True)
            context = driver_wrapper.initialize()
            
            # Verify headless option was set
            call_kwargs = mock_playwright.chromium.launch.call_args[1]
            assert call_kwargs['headless'] is True
            assert context == mock_context
    
    def test_firefox_driver_initialization(self):
        """Test Firefox driver initialization with correct options."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.firefox.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize Firefox driver
            driver_wrapper = PlaywrightDriver(browser_type='firefox', headless=False)
            context = driver_wrapper.initialize()
            
            # Verify Firefox was called with correct options
            assert mock_playwright.firefox.launch.called
            call_kwargs = mock_playwright.firefox.launch.call_args[1]
            assert call_kwargs['headless'] is False
            assert call_kwargs['slow_mo'] == 0
            
            # Verify context was created
            assert context == mock_context
            assert driver_wrapper.context == mock_context
    
    def test_webkit_driver_initialization(self):
        """Test WebKit driver initialization with correct options."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.webkit.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize WebKit driver
            driver_wrapper = PlaywrightDriver(browser_type='webkit', headless=False)
            context = driver_wrapper.initialize()
            
            # Verify WebKit was called with correct options
            assert mock_playwright.webkit.launch.called
            call_kwargs = mock_playwright.webkit.launch.call_args[1]
            assert call_kwargs['headless'] is False
            assert call_kwargs['slow_mo'] == 0
            
            # Verify context was created
            assert context == mock_context
            assert driver_wrapper.context == mock_context
    
    def test_slow_mo_parameter(self):
        """Test that slow_mo parameter is passed correctly."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize with slow_mo
            driver_wrapper = PlaywrightDriver(browser_type='chromium', slow_mo=500)
            context = driver_wrapper.initialize()
            
            # Verify slow_mo was passed
            call_kwargs = mock_playwright.chromium.launch.call_args[1]
            assert call_kwargs['slow_mo'] == 500
    
    def test_tracing_enabled(self):
        """Test that tracing is started when enabled."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing enabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=True)
            context = driver_wrapper.initialize()
            
            # Verify tracing was started with screenshots and snapshots
            assert mock_tracing.start.called
            call_kwargs = mock_tracing.start.call_args[1]
            assert call_kwargs['screenshots'] is True
            assert call_kwargs['snapshots'] is True
    
    def test_tracing_disabled(self):
        """Test that tracing is not started when disabled."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing disabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=False)
            context = driver_wrapper.initialize()
            
            # Verify tracing was not started
            assert not mock_tracing.start.called
    
    def test_unsupported_browser_raises_value_error(self):
        """Test that unsupported browser raises ValueError with descriptive message."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            
            driver_wrapper = PlaywrightDriver(browser_type='safari', headless=False)
            
            with pytest.raises(ValueError) as exc_info:
                driver_wrapper.initialize()
            
            # Verify error message contains browser name and supported browsers
            error_message = str(exc_info.value)
            assert 'safari' in error_message.lower()
            assert 'chromium' in error_message.lower()
            assert 'firefox' in error_message.lower()
            assert 'webkit' in error_message.lower()
            assert 'Unsupported browser' in error_message
    
    def test_browser_initialization_failure_raises_runtime_error(self):
        """Test that browser initialization failure raises RuntimeError with descriptive error."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks to raise exception
            mock_playwright = Mock()
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.side_effect = Exception('Browser launch failed')
            
            driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
            
            with pytest.raises(RuntimeError) as exc_info:
                driver_wrapper.initialize()
            
            # Verify error message contains browser name and error details
            error_message = str(exc_info.value)
            assert 'chromium' in error_message.lower()
            assert 'Failed to initialize' in error_message
            assert 'Browser launch failed' in error_message
    
    def test_quit_closes_all_resources(self):
        """Test that quit method closes context, browser, and playwright."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize and quit driver
            driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
            driver_wrapper.initialize()
            driver_wrapper.quit()
            
            # Verify all resources were closed
            assert mock_context.close.called
            assert mock_browser.close.called
            assert mock_playwright.stop.called
            assert driver_wrapper.context is None
            assert driver_wrapper.browser is None
            assert driver_wrapper.playwright is None
    
    def test_quit_without_initialization(self):
        """Test that quit method handles case when driver is not initialized."""
        driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
        
        # Should not raise exception
        driver_wrapper.quit()
        assert driver_wrapper.context is None
        assert driver_wrapper.browser is None
        assert driver_wrapper.playwright is None
    
    def test_quit_with_trace_path(self):
        """Test that quit saves trace file when tracing is enabled and path is provided."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing enabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=True)
            driver_wrapper.initialize()
            
            # Create temporary directory for trace
            with tempfile.TemporaryDirectory() as temp_dir:
                trace_path = os.path.join(temp_dir, 'traces', 'test.zip')
                
                # Quit with trace path
                driver_wrapper.quit(trace_path=trace_path)
                
                # Verify trace was stopped with path
                assert mock_tracing.stop.called
                call_kwargs = mock_tracing.stop.call_args[1]
                assert call_kwargs['path'] == trace_path
    
    def test_quit_without_trace_path(self):
        """Test that quit does not save trace when path is not provided."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing enabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=True)
            driver_wrapper.initialize()
            
            # Quit without trace path
            driver_wrapper.quit()
            
            # Verify trace was not stopped
            assert not mock_tracing.stop.called
    
    def test_quit_trace_disabled(self):
        """Test that quit does not save trace when tracing is disabled."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing disabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=False)
            driver_wrapper.initialize()
            
            # Quit with trace path
            driver_wrapper.quit(trace_path='/tmp/trace.zip')
            
            # Verify trace was not stopped
            assert not mock_tracing.stop.called
    
    def test_quit_handles_exception_gracefully(self):
        """Test that quit method handles exceptions during cleanup."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_context.close.side_effect = Exception('Close failed')
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            
            # Initialize and quit driver
            driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
            driver_wrapper.initialize()
            
            # Should not raise exception, but should print error
            driver_wrapper.quit()
            assert driver_wrapper.context is None
            assert driver_wrapper.browser is None
            assert driver_wrapper.playwright is None
    
    def test_quit_trace_save_handles_exception(self):
        """Test that quit handles exceptions during trace save gracefully."""
        with patch('framework.playwright_driver.sync_playwright') as mock_sync_playwright:
            # Setup mocks
            mock_playwright = Mock()
            mock_browser = Mock()
            mock_context = Mock()
            mock_tracing = Mock()
            mock_tracing.stop.side_effect = Exception('Trace save failed')
            
            mock_sync_playwright.return_value.start.return_value = mock_playwright
            mock_playwright.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.tracing = mock_tracing
            
            # Initialize with tracing enabled
            driver_wrapper = PlaywrightDriver(browser_type='chromium', tracing=True)
            driver_wrapper.initialize()
            
            # Should not raise exception
            driver_wrapper.quit(trace_path='/tmp/trace.zip')
            assert driver_wrapper.context is None
    
    def test_capture_screenshot_success(self):
        """Test successful screenshot capture."""
        mock_page = Mock()
        mock_page.screenshot.return_value = None
        
        driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
        
        # Create temporary directory for screenshot
        with tempfile.TemporaryDirectory() as temp_dir:
            screenshot_path = os.path.join(temp_dir, 'screenshots', 'test.png')
            
            # Capture screenshot
            result = driver_wrapper.capture_screenshot(mock_page, screenshot_path)
            
            # Verify screenshot was captured
            assert result is True
            assert mock_page.screenshot.called
            call_kwargs = mock_page.screenshot.call_args[1]
            assert call_kwargs['path'] == screenshot_path
            assert call_kwargs['full_page'] is True
    
    def test_capture_screenshot_creates_directory(self):
        """Test that capture_screenshot creates directory if it doesn't exist."""
        mock_page = Mock()
        mock_page.screenshot.return_value = None
        
        driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
        
        # Create temporary directory for screenshot
        with tempfile.TemporaryDirectory() as temp_dir:
            screenshot_path = os.path.join(temp_dir, 'new_dir', 'screenshots', 'test.png')
            
            # Capture screenshot
            result = driver_wrapper.capture_screenshot(mock_page, screenshot_path)
            
            # Verify directory was created
            assert result is True
            assert os.path.exists(os.path.dirname(screenshot_path))
    
    def test_capture_screenshot_handles_exception(self):
        """Test that capture_screenshot handles exceptions gracefully."""
        mock_page = Mock()
        mock_page.screenshot.side_effect = Exception('Screenshot failed')
        
        driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
        
        # Try to capture screenshot
        result = driver_wrapper.capture_screenshot(mock_page, '/tmp/test.png')
        
        # Verify screenshot capture failed gracefully
        assert result is False
    
    def test_capture_screenshot_with_empty_directory(self):
        """Test that capture_screenshot handles filepath with no directory."""
        mock_page = Mock()
        mock_page.screenshot.return_value = None
        
        driver_wrapper = PlaywrightDriver(browser_type='chromium', headless=False)
        
        # Capture screenshot with no directory path
        result = driver_wrapper.capture_screenshot(mock_page, 'test.png')
        
        # Verify screenshot was captured
        assert result is True
        assert mock_page.screenshot.called
    
    def test_initialization_attributes(self):
        """Test that PlaywrightDriver initializes with correct attributes."""
        driver_wrapper = PlaywrightDriver(
            browser_type='firefox',
            headless=True,
            slow_mo=100,
            tracing=True
        )
        
        assert driver_wrapper.browser_type == 'firefox'
        assert driver_wrapper.headless is True
        assert driver_wrapper.slow_mo == 100
        assert driver_wrapper.tracing is True
        assert driver_wrapper.playwright is None
        assert driver_wrapper.browser is None
        assert driver_wrapper.context is None
    
    def test_default_initialization_values(self):
        """Test that PlaywrightDriver uses default values when not specified."""
        driver_wrapper = PlaywrightDriver()
        
        assert driver_wrapper.browser_type == 'chromium'
        assert driver_wrapper.headless is False
        assert driver_wrapper.slow_mo == 0
        assert driver_wrapper.tracing is False
        assert driver_wrapper.playwright is None
        assert driver_wrapper.browser is None
        assert driver_wrapper.context is None
