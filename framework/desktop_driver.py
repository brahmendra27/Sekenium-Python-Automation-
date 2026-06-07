"""Desktop application driver wrapper using pywinauto.

Provides app lifecycle management (launch, connect, close) and serves as
the entry point for desktop automation tests. Works with both 'uia' backend
(WPF, WinForms, UWP, Qt5) and 'win32' backend (classic Win32/MFC apps).

Tkinter apps use the 'win32' backend.
"""

import logging
import time

from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError

logger = logging.getLogger(__name__)


class DesktopDriver:
    """Manages desktop application lifecycle for test automation.

    Supports launching apps by path, connecting to running apps,
    and provides access to the pywinauto Application instance.
    """

    def __init__(self, backend: str = "win32"):
        """Initialize the desktop driver.

        Args:
            backend: 'uia' for modern apps (WPF, WinForms, UWP, Qt5)
                     'win32' for classic Win32/MFC/Tkinter apps
        """
        self.backend = backend
        self.app: Application | None = None
        self._process = None

    def launch(self, path: str, wait_ready: bool = True, timeout: int = 10, **kwargs) -> "DesktopDriver":
        """Launch a desktop application by executable path.

        Args:
            path: Full path to the .exe or script to run.
            wait_ready: Wait for the main window to be ready.
            timeout: Seconds to wait for the app to be ready.
            **kwargs: Additional args passed to Application.start()

        Returns:
            Self for chaining.
        """
        logger.info(f"Launching application: {path} (backend={self.backend})")
        self.app = Application(backend=self.backend).start(path, **kwargs)

        if wait_ready:
            self._wait_for_ready(timeout)

        return self

    def connect(self, timeout: int = 10, **kwargs) -> "DesktopDriver":
        """Connect to an already running application.

        Args:
            timeout: Seconds to wait for connection.
            **kwargs: Connection criteria (title, title_re, process, path, etc.)
                Examples:
                    connect(title="QE Sample POS - Login")
                    connect(process=1234)
                    connect(title_re=".*POS.*")

        Returns:
            Self for chaining.
        """
        logger.info(f"Connecting to application: {kwargs}")
        end_time = time.time() + timeout
        last_error = None

        while time.time() < end_time:
            try:
                self.app = Application(backend=self.backend).connect(**kwargs)
                logger.info("Connected to application successfully")
                return self
            except (ElementNotFoundError, Exception) as e:
                last_error = e
                time.sleep(0.5)

        raise TimeoutError(
            f"Could not connect to application within {timeout}s. "
            f"Criteria: {kwargs}. Last error: {last_error}"
        )

    def close(self):
        """Close the application gracefully, then kill if needed."""
        if self.app:
            try:
                self.app.kill()
                logger.info("Application closed")
            except Exception as e:
                logger.warning(f"Failed to close app: {e}")
            self.app = None

    def is_running(self) -> bool:
        """Check if the application process is still running."""
        if not self.app:
            return False
        try:
            return self.app.is_process_running()
        except Exception:
            return False

    @property
    def desktop(self) -> Desktop:
        """Access the Windows desktop for finding top-level windows."""
        return Desktop(backend=self.backend)

    def get_window(self, **kwargs):
        """Get a specific window from the application.

        Args:
            **kwargs: Window specification (title, title_re, class_name, etc.)

        Returns:
            A WindowSpecification object.
        """
        if not self.app:
            raise RuntimeError("Application not launched. Call launch() or connect() first.")
        return self.app.window(**kwargs)

    def _wait_for_ready(self, timeout: int):
        """Wait for the application's main window to be ready."""
        if not self.app:
            return
        try:
            self.app.wait_cpu_usage_lower(threshold=5, timeout=timeout)
        except Exception:
            # Fallback: just wait a moment
            time.sleep(1)
