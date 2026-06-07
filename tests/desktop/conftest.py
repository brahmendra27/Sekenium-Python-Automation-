"""Desktop testing fixtures for the QE Sample POS application."""

import os
import subprocess
import sys
import time
import logging

import pytest

from framework.desktop_driver import DesktopDriver

logger = logging.getLogger(__name__)

# Path to the POS application
POS_APP_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "sample_apps",
    "pos_app.py",
)


@pytest.fixture(scope="function")
def desktop_driver():
    """Provide a DesktopDriver instance with automatic cleanup.

    Yields:
        A DesktopDriver ready for launching applications.
    """
    driver = DesktopDriver(backend="win32")
    yield driver
    driver.close()


@pytest.fixture(scope="function")
def pos_app(desktop_driver):
    """Launch the QE Sample POS application.

    Uses subprocess.Popen to start the app, then connects via window title.
    This avoids the 'WaitForInputIdle' error that occurs when pywinauto
    tries to launch python.exe (a console process) directly.

    Yields:
        The DesktopDriver connected to the running POS app.
    """
    # Use pythonw.exe if available (no console window), fallback to python.exe
    python_exe = sys.executable
    pythonw = python_exe.replace("python.exe", "pythonw.exe")
    if os.path.exists(pythonw):
        exe = pythonw
    else:
        exe = python_exe

    # Start the app as a subprocess
    proc = subprocess.Popen(
        [exe, POS_APP_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    logger.info(f"Started POS app (PID={proc.pid}) using {exe}")

    # Wait for the window to appear and connect
    time.sleep(2)
    desktop_driver.connect(title_re=".*QE Sample POS.*", timeout=10)

    yield desktop_driver

    # Cleanup: terminate the subprocess
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
