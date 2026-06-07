# framework/reliability_helper.py

"""
Test Reliability Helper for flaky test management.

Provides:
  - Flaky test classification (timing, data, environment, locator)
  - Retry decorator with root cause logging
  - Test stability tracking
  - Quarantine marker for known flaky tests

Usage:
    @retry_on_flake(max_retries=2, classify=True)
    def test_checkout_flow(page):
        ...

    @pytest.mark.quarantine(reason="Flaky due to animation timing", ticket="JIRA-123")
    def test_modal_animation():
        ...
"""

import functools
import logging
import time
from typing import Optional, Callable
import pytest

logger = logging.getLogger(__name__)


class FlakyTestClassifier:
    """Classifies flaky test failures by root cause."""

    TIMING_KEYWORDS = [
        "timeout", "timed out", "waitfor", "wait_for",
        "not visible", "not attached", "detached"
    ]
    DATA_KEYWORDS = [
        "assert", "expected", "not equal", "mismatch",
        "not found in", "missing key", "empty"
    ]
    ENVIRONMENT_KEYWORDS = [
        "connection", "refused", "unreachable", "dns",
        "ssl", "certificate", "network", "econnreset"
    ]
    LOCATOR_KEYWORDS = [
        "selector", "locator", "element", "no such element",
        "stale element", "not interactable"
    ]

    @classmethod
    def classify(cls, error: Exception) -> str:
        """Classify a test failure by root cause.

        Args:
            error: The exception that caused the failure

        Returns:
            Category string: 'timing', 'data', 'environment',
            'locator', or 'unknown'
        """
        error_str = str(error).lower()

        if any(kw in error_str for kw in cls.TIMING_KEYWORDS):
            return "timing"
        if any(kw in error_str for kw in cls.LOCATOR_KEYWORDS):
            return "locator"
        if any(kw in error_str for kw in cls.ENVIRONMENT_KEYWORDS):
            return "environment"
        if any(kw in error_str for kw in cls.DATA_KEYWORDS):
            return "data"
        return "unknown"

    @classmethod
    def get_fix_suggestion(cls, category: str) -> str:
        """Get fix suggestion for a flaky test category.

        Args:
            category: Failure category from classify()

        Returns:
            Suggested fix string
        """
        suggestions = {
            "timing": (
                "Add explicit wait for the specific condition. "
                "Avoid fixed timeouts. Use Playwright auto-waiting."
            ),
            "locator": (
                "Use more stable selectors (data-testid, getByRole). "
                "Check if the DOM structure changed."
            ),
            "environment": (
                "Check network connectivity and service health. "
                "Add environment health check before tests."
            ),
            "data": (
                "Use unique test data per run (unique_id fixture). "
                "Ensure test data isolation."
            ),
            "unknown": (
                "Review the full error trace. Consider adding "
                "more specific error handling."
            )
        }
        return suggestions.get(category, suggestions["unknown"])


def retry_on_flake(max_retries: int = 2, delay: float = 1.0,
                   classify: bool = True):
    """Decorator to retry flaky tests with classification.

    Args:
        max_retries: Maximum retry attempts
        delay: Delay between retries in seconds
        classify: Whether to classify the failure type

    Usage:
        @retry_on_flake(max_retries=2)
        def test_something(page):
            ...
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries:
                        category = "unknown"
                        if classify:
                            category = FlakyTestClassifier.classify(e)
                        logger.warning(
                            f"Test {func.__name__} failed (attempt "
                            f"{attempt + 1}/{max_retries + 1}). "
                            f"Category: {category}. "
                            f"Error: {str(e)[:200]}"
                        )
                        time.sleep(delay)
                    else:
                        if classify:
                            category = FlakyTestClassifier.classify(e)
                            suggestion = FlakyTestClassifier.get_fix_suggestion(
                                category
                            )
                            logger.error(
                                f"Test {func.__name__} failed after "
                                f"{max_retries + 1} attempts. "
                                f"Category: {category}. "
                                f"Suggestion: {suggestion}"
                            )
                        raise
        return wrapper
    return decorator


# Custom pytest marker for quarantined tests
quarantine = pytest.mark.skip(reason="Quarantined: known flaky test")
