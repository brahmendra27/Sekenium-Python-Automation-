"""Error classification for test failures based on pattern matching.

Categorizes error messages into cause buckets inspired by TestDino's approach:
- Assertion Failure: Expected vs actual value mismatches
- Element Not Found: Locator/selector failures
- Timeout Issues: Action or wait exceeded time limit
- Network Issues: Request failures, connection errors, HTTP status errors
- Other Failures: Errors that don't fit the above categories
"""

import re

# Patterns for each failure category (checked in order, first match wins)
FAILURE_PATTERNS: dict[str, list[re.Pattern]] = {
    "assertion": [
        re.compile(r"AssertionError", re.IGNORECASE),
        re.compile(r"assert\s+.+\s*==\s*", re.IGNORECASE),
        re.compile(r"expected\s+.*\s+to\s+(be|equal|match|contain|have)", re.IGNORECASE),
        re.compile(r"not equal", re.IGNORECASE),
        re.compile(r"mismatch", re.IGNORECASE),
        re.compile(r"assert_status_code", re.IGNORECASE),
        re.compile(r"assert_json", re.IGNORECASE),
    ],
    "element_not_found": [
        re.compile(r"element\s+not\s+found", re.IGNORECASE),
        re.compile(r"no\s+such\s+element", re.IGNORECASE),
        re.compile(r"locator\s+resolved\s+to\s+0", re.IGNORECASE),
        re.compile(r"selector\s+.+\s+not\s+found", re.IGNORECASE),
        re.compile(r"NoSuchElementException", re.IGNORECASE),
        re.compile(r"ElementNotFound", re.IGNORECASE),
        re.compile(r"waiting for locator", re.IGNORECASE),
        re.compile(r"could not find element", re.IGNORECASE),
    ],
    "timeout": [
        re.compile(r"TimeoutError", re.IGNORECASE),
        re.compile(r"Timeout\s+\d+ms\s+exceeded", re.IGNORECASE),
        re.compile(r"timed?\s*out", re.IGNORECASE),
        re.compile(r"ReadTimeout", re.IGNORECASE),
        re.compile(r"ConnectTimeout", re.IGNORECASE),
        re.compile(r"exceeded.*timeout", re.IGNORECASE),
        re.compile(r"wait_for.*timeout", re.IGNORECASE),
    ],
    "network": [
        re.compile(r"ConnectionError", re.IGNORECASE),
        re.compile(r"ConnectionRefused", re.IGNORECASE),
        re.compile(r"NetworkError", re.IGNORECASE),
        re.compile(r"ERR_CONNECTION", re.IGNORECASE),
        re.compile(r"ECONNREFUSED", re.IGNORECASE),
        re.compile(r"net::ERR_", re.IGNORECASE),
        re.compile(r"DNS.*fail", re.IGNORECASE),
        re.compile(r"HTTP\s+\d{3}", re.IGNORECASE),
        re.compile(r"status\s*code\s*[:=]\s*5\d{2}", re.IGNORECASE),
        re.compile(r"502|503|504", re.IGNORECASE),
        re.compile(r"requests\.exceptions", re.IGNORECASE),
    ],
}

# Flaky sub-categories
FLAKY_PATTERNS: dict[str, list[re.Pattern]] = {
    "timing": [
        re.compile(r"timeout", re.IGNORECASE),
        re.compile(r"race\s+condition", re.IGNORECASE),
        re.compile(r"wait", re.IGNORECASE),
        re.compile(r"too\s+slow", re.IGNORECASE),
    ],
    "environment": [
        re.compile(r"environment", re.IGNORECASE),
        re.compile(r"config", re.IGNORECASE),
        re.compile(r"permission", re.IGNORECASE),
        re.compile(r"not\s+configured", re.IGNORECASE),
    ],
    "network": [
        re.compile(r"connection", re.IGNORECASE),
        re.compile(r"network", re.IGNORECASE),
        re.compile(r"ERR_", re.IGNORECASE),
        re.compile(r"ECONNREFUSED", re.IGNORECASE),
    ],
    "assertion_intermittent": [
        re.compile(r"assert", re.IGNORECASE),
        re.compile(r"expected", re.IGNORECASE),
        re.compile(r"mismatch", re.IGNORECASE),
    ],
}

# Skip sub-categories
SKIP_PATTERNS: dict[str, list[re.Pattern]] = {
    "manual": [
        re.compile(r"pytest\.skip", re.IGNORECASE),
        re.compile(r"skip\(", re.IGNORECASE),
        re.compile(r"@pytest\.mark\.skip", re.IGNORECASE),
    ],
    "configuration": [
        re.compile(r"not\s+configured", re.IGNORECASE),
        re.compile(r"missing.*env", re.IGNORECASE),
        re.compile(r"disabled", re.IGNORECASE),
    ],
    "conditional": [
        re.compile(r"skipif", re.IGNORECASE),
        re.compile(r"condition", re.IGNORECASE),
        re.compile(r"platform", re.IGNORECASE),
    ],
}


def classify_failure(error_message: str | None, longrepr: str | None = None) -> str:
    """Classify a test failure into a cause category.

    Args:
        error_message: The crash/error message from the test.
        longrepr: The full traceback/longrepr string.

    Returns:
        One of: 'assertion', 'element_not_found', 'timeout', 'network', 'other'
    """
    text = f"{error_message or ''} {longrepr or ''}"
    if not text.strip():
        return "other"

    for category, patterns in FAILURE_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return category
    return "other"


def classify_flaky(error_message: str | None, longrepr: str | None = None) -> str:
    """Classify a flaky test into a sub-category.

    Args:
        error_message: The most recent error message.
        longrepr: The full traceback string.

    Returns:
        One of: 'timing', 'environment', 'network', 'assertion_intermittent', 'other'
    """
    text = f"{error_message or ''} {longrepr or ''}"
    if not text.strip():
        return "other"

    for category, patterns in FLAKY_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return category
    return "other"


def classify_skip(error_message: str | None, longrepr: str | None = None) -> str:
    """Classify a skipped test into a sub-category.

    Args:
        error_message: The skip reason message.
        longrepr: The full representation string.

    Returns:
        One of: 'manual', 'configuration', 'conditional', 'other'
    """
    text = f"{error_message or ''} {longrepr or ''}"
    if not text.strip():
        return "manual"

    for category, patterns in SKIP_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return category
    return "manual"


def normalize_error_message(error_message: str | None) -> str:
    """Normalize an error message for grouping purposes.

    Strips variable parts (IDs, timestamps, paths) to group similar errors together.

    Args:
        error_message: The raw error message.

    Returns:
        A normalized string suitable for grouping.
    """
    if not error_message:
        return "Unknown error"

    msg = error_message.strip()

    # Remove UUIDs
    msg = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<ID>", msg)
    # Remove hex IDs (e.g., 0x7f...)
    msg = re.sub(r"0x[0-9a-f]+", "<ADDR>", msg, flags=re.IGNORECASE)
    # Remove file paths
    msg = re.sub(r"[A-Za-z]:\\[^\s:]+", "<PATH>", msg)
    msg = re.sub(r"/[^\s:]+\.(py|js|ts|html|json)", "<PATH>", msg)
    # Remove line numbers
    msg = re.sub(r"line\s+\d+", "line <N>", msg, flags=re.IGNORECASE)
    # Remove timestamps
    msg = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}", "<TIMESTAMP>", msg)
    # Remove numeric IDs at end of URLs
    msg = re.sub(r"/\d+(?=[/\s]|$)", "/<ID>", msg)

    # Truncate very long messages
    if len(msg) > 200:
        msg = msg[:200]

    return msg
