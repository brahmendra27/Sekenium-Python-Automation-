# framework/accessibility_helper.py

"""
Accessibility Testing Helper using axe-core.

Provides WCAG 2.1 compliance scanning for Playwright pages.
Injects axe-core JavaScript and runs accessibility audits.

Usage:
    a11y = AccessibilityHelper(page)
    results = a11y.scan()
    a11y.assert_no_violations()
    a11y.assert_wcag_aa()
"""

import json
import logging
from typing import Dict, List, Optional
from playwright.sync_api import Page
import allure

logger = logging.getLogger(__name__)

# axe-core CDN URL
AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


class AccessibilityHelper:
    """WCAG accessibility scanner using axe-core."""

    def __init__(self, page: Page):
        """Initialize with a Playwright page.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self._injected = False

    def _inject_axe(self):
        """Inject axe-core library into the page."""
        if self._injected:
            return

        # Check if axe is already loaded
        has_axe = self.page.evaluate("typeof window.axe !== 'undefined'")
        if not has_axe:
            self.page.add_script_tag(url=AXE_CDN)
            self.page.wait_for_function("typeof window.axe !== 'undefined'")
        self._injected = True

    @allure.step("Run accessibility scan")
    def scan(self, context: Optional[str] = None,
             tags: Optional[List[str]] = None) -> Dict:
        """Run axe-core accessibility scan.

        Args:
            context: CSS selector to limit scan scope (default: entire page)
            tags: WCAG tags to check (e.g., ['wcag2a', 'wcag2aa', 'wcag21aa'])

        Returns:
            Dict with 'violations', 'passes', 'incomplete', 'inapplicable'
        """
        self._inject_axe()

        options = {}
        if tags:
            options["runOnly"] = {"type": "tag", "values": tags}

        if context:
            results = self.page.evaluate(
                f"axe.run('{context}', {json.dumps(options)})"
            )
        else:
            results = self.page.evaluate(
                f"axe.run({json.dumps(options)})"
            )

        violation_count = len(results.get("violations", []))
        pass_count = len(results.get("passes", []))
        logger.info(
            f"Accessibility scan: {violation_count} violations, "
            f"{pass_count} passes"
        )

        # Attach results to Allure
        allure.attach(
            json.dumps(results.get("violations", []), indent=2),
            name="a11y_violations",
            attachment_type=allure.attachment_type.JSON
        )

        return results

    def get_violations(self, results: Optional[Dict] = None) -> List[Dict]:
        """Get violations from scan results.

        Args:
            results: Scan results (runs new scan if not provided)

        Returns:
            List of violation dicts with id, impact, description, nodes
        """
        if results is None:
            results = self.scan()
        return results.get("violations", [])

    def get_violation_summary(self, results: Optional[Dict] = None) -> str:
        """Get human-readable violation summary.

        Args:
            results: Scan results (runs new scan if not provided)

        Returns:
            Formatted string with violation details
        """
        violations = self.get_violations(results)
        if not violations:
            return "No accessibility violations found."

        lines = [f"Found {len(violations)} accessibility violations:\n"]
        for v in violations:
            impact = v.get("impact", "unknown")
            rule_id = v.get("id", "unknown")
            description = v.get("description", "")
            node_count = len(v.get("nodes", []))
            lines.append(
                f"  [{impact.upper()}] {rule_id}: {description} "
                f"({node_count} elements)"
            )
        return "\n".join(lines)

    @allure.step("Assert no accessibility violations")
    def assert_no_violations(self, context: Optional[str] = None,
                             tags: Optional[List[str]] = None):
        """Assert page has no accessibility violations.

        Args:
            context: CSS selector to limit scope
            tags: WCAG tags to check

        Raises:
            AssertionError with violation details
        """
        results = self.scan(context=context, tags=tags)
        violations = results.get("violations", [])
        if violations:
            summary = self.get_violation_summary(results)
            raise AssertionError(f"Accessibility violations found:\n{summary}")

    @allure.step("Assert WCAG 2.1 AA compliance")
    def assert_wcag_aa(self, context: Optional[str] = None):
        """Assert page meets WCAG 2.1 Level AA.

        Args:
            context: CSS selector to limit scope
        """
        self.assert_no_violations(
            context=context,
            tags=["wcag2a", "wcag2aa", "wcag21aa"]
        )

    @allure.step("Assert WCAG 2.1 A compliance")
    def assert_wcag_a(self, context: Optional[str] = None):
        """Assert page meets WCAG 2.1 Level A.

        Args:
            context: CSS selector to limit scope
        """
        self.assert_no_violations(
            context=context,
            tags=["wcag2a", "wcag21a"]
        )

    def get_critical_violations(self,
                                results: Optional[Dict] = None) -> List[Dict]:
        """Get only critical and serious violations.

        Args:
            results: Scan results

        Returns:
            List of critical/serious violations
        """
        violations = self.get_violations(results)
        return [
            v for v in violations
            if v.get("impact") in ("critical", "serious")
        ]
