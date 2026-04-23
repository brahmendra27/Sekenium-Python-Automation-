# framework/ai_insights.py

"""
AI Test Insights Engine.

Analyzes test execution results and provides intelligent recommendations.
Inspired by TestDino's AI-powered test analysis patterns.

Features:
  - Test failure root cause classification
  - Actionable fix suggestions per failure type
  - Test suite health scoring
  - Trend detection (flaky tests, slow tests, coverage gaps)
  - Allure-integrated insight reports
  - Execution summary with AI recommendations

Usage:
    insights = AITestInsights()
    insights.load_results("reports/report.json")
    report = insights.analyze()
    insights.print_summary()
    insights.attach_to_allure()
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import allure

logger = logging.getLogger(__name__)


class TestResult:
    """Represents a single test execution result."""

    def __init__(self, data: Dict):
        self.name = data.get("nodeid", data.get("name", "unknown"))
        self.outcome = data.get("outcome", "unknown")
        self.duration = data.get("duration", 0)
        self.setup_duration = data.get("setup", {}).get("duration", 0)
        self.teardown_duration = data.get("teardown", {}).get("duration", 0)
        self.error_message = ""
        self.error_traceback = ""

        # Extract error info
        call_data = data.get("call", {})
        if call_data.get("crash"):
            self.error_message = call_data["crash"].get("message", "")
        if call_data.get("longrepr"):
            self.error_traceback = str(call_data["longrepr"])

    @property
    def total_duration(self) -> float:
        return self.setup_duration + self.duration + self.teardown_duration

    @property
    def is_passed(self) -> bool:
        return self.outcome == "passed"

    @property
    def is_failed(self) -> bool:
        return self.outcome == "failed"

    @property
    def is_error(self) -> bool:
        return self.outcome == "error"

    @property
    def is_skipped(self) -> bool:
        return self.outcome == "skipped"


class FailureClassifier:
    """Classifies test failures by root cause with fix suggestions."""

    CATEGORIES = {
        "timing": {
            "keywords": [
                "timeout", "timed out", "waitfor", "wait_for",
                "not visible", "not attached", "detached",
                "page.wait_for", "locator.wait_for"
            ],
            "description": "Element timing / visibility issue",
            "fix": (
                "1. Use Playwright auto-waiting instead of explicit waits\n"
                "2. Use web-first assertions: expect(locator).to_be_visible()\n"
                "3. Check if element is inside an iframe or shadow DOM\n"
                "4. Increase timeout for slow-loading pages"
            ),
            "severity": "medium"
        },
        "locator": {
            "keywords": [
                "selector", "locator", "no such element",
                "stale element", "not interactable", "element not found",
                "could not find", "unable to locate"
            ],
            "description": "Element locator / selector issue",
            "fix": (
                "1. Switch to semantic locators: get_by_role(), get_by_test_id()\n"
                "2. Check if DOM structure changed (inspect element)\n"
                "3. Verify element is not inside iframe or shadow DOM\n"
                "4. Add data-testid attributes to the application"
            ),
            "severity": "high"
        },
        "assertion": {
            "keywords": [
                "assertionerror", "assert", "expected", "not equal",
                "mismatch", "!=", "to_have_text", "to_have_url",
                "to_be_visible", "to_contain_text"
            ],
            "description": "Test assertion failure",
            "fix": (
                "1. Verify expected values match current application state\n"
                "2. Check if test data is stale or environment-specific\n"
                "3. Use unique_id fixture for test data isolation\n"
                "4. Check if application behavior changed (feature update)"
            ),
            "severity": "high"
        },
        "environment": {
            "keywords": [
                "connection", "refused", "unreachable", "dns",
                "ssl", "certificate", "network", "econnreset",
                "err_connection", "name resolution"
            ],
            "description": "Environment / network connectivity issue",
            "fix": (
                "1. Verify target environment is accessible\n"
                "2. Check VPN connection\n"
                "3. Verify BASE_URL in .env file\n"
                "4. Check if environment is under maintenance"
            ),
            "severity": "critical"
        },
        "authentication": {
            "keywords": [
                "login", "auth", "unauthorized", "403", "401",
                "forbidden", "access denied", "token expired",
                "session expired", "invalid credentials"
            ],
            "description": "Authentication / authorization failure",
            "fix": (
                "1. Check credentials in .env file\n"
                "2. Verify OAuth tokens haven't expired\n"
                "3. Check Connected App settings (Salesforce)\n"
                "4. Verify API permissions and IP restrictions"
            ),
            "severity": "critical"
        },
        "data": {
            "keywords": [
                "not found in", "missing key", "keyerror",
                "indexerror", "empty", "null", "none",
                "no records", "does not exist"
            ],
            "description": "Test data issue",
            "fix": (
                "1. Use unique_id fixture for unique test data\n"
                "2. Verify test data setup completed successfully\n"
                "3. Check if another test modified shared data\n"
                "4. Use sf_cleanup fixture for Salesforce records"
            ),
            "severity": "medium"
        },
        "driver": {
            "keywords": [
                "webdriver", "chromedriver", "geckodriver",
                "browser", "playwright", "browser closed",
                "target closed", "session not created"
            ],
            "description": "Browser / driver initialization issue",
            "fix": (
                "1. Update webdriver-manager: pip install --upgrade webdriver-manager\n"
                "2. Check browser installation\n"
                "3. Clear webdriver cache: rm -rf ~/.wdm\n"
                "4. Try different browser: --browser=firefox"
            ),
            "severity": "critical"
        },
        "import": {
            "keywords": [
                "importerror", "modulenotfounderror", "no module named",
                "cannot import", "attributeerror"
            ],
            "description": "Import / module error",
            "fix": (
                "1. Run: pip install -r requirements.txt\n"
                "2. Check if module name is correct\n"
                "3. Verify __init__.py files exist\n"
                "4. Check Python path configuration"
            ),
            "severity": "critical"
        }
    }

    @classmethod
    def classify(cls, error_message: str, traceback: str = "") -> Dict:
        """Classify a test failure and return insights.

        Args:
            error_message: Error message from test failure
            traceback: Full traceback string

        Returns:
            Dict with category, description, fix, severity, confidence
        """
        combined = f"{error_message} {traceback}".lower()

        best_match = None
        best_score = 0

        for category, info in cls.CATEGORIES.items():
            score = sum(
                1 for kw in info["keywords"]
                if kw in combined
            )
            if score > best_score:
                best_score = score
                best_match = category

        if best_match and best_score > 0:
            info = cls.CATEGORIES[best_match]
            confidence = min(best_score / 3.0, 1.0)
            return {
                "category": best_match,
                "description": info["description"],
                "fix": info["fix"],
                "severity": info["severity"],
                "confidence": round(confidence, 2),
                "matched_keywords": best_score
            }

        return {
            "category": "unknown",
            "description": "Unclassified failure",
            "fix": "Review the full error trace and stack trace for details.",
            "severity": "medium",
            "confidence": 0,
            "matched_keywords": 0
        }


class AITestInsights:
    """AI-powered test execution analysis engine."""

    def __init__(self):
        self.results: List[TestResult] = []
        self.analysis: Optional[Dict] = None

    def load_results(self, report_path: str = "reports/report.json"):
        """Load test results from pytest-json-report output.

        Args:
            report_path: Path to report.json file
        """
        path = Path(report_path)
        if not path.exists():
            logger.warning(f"Report not found: {report_path}")
            return

        with open(path) as f:
            data = json.load(f)

        tests = data.get("tests", [])
        self.results = [TestResult(t) for t in tests]
        logger.info(f"Loaded {len(self.results)} test results from {report_path}")

    def analyze(self) -> Dict:
        """Analyze test results and generate insights.

        Returns:
            Comprehensive analysis dict with metrics, failures, recommendations
        """
        if not self.results:
            return {"error": "No test results loaded"}

        passed = [r for r in self.results if r.is_passed]
        failed = [r for r in self.results if r.is_failed]
        errors = [r for r in self.results if r.is_error]
        skipped = [r for r in self.results if r.is_skipped]

        # Classify failures
        failure_insights = []
        for result in failed + errors:
            classification = FailureClassifier.classify(
                result.error_message, result.error_traceback
            )
            failure_insights.append({
                "test": result.name,
                "duration": round(result.total_duration, 2),
                **classification
            })

        # Identify slow tests (> 30 seconds)
        slow_tests = [
            {"test": r.name, "duration": round(r.total_duration, 2)}
            for r in self.results
            if r.total_duration > 30
        ]
        slow_tests.sort(key=lambda x: x["duration"], reverse=True)

        # Calculate health score
        total = len(self.results)
        pass_rate = len(passed) / total if total > 0 else 0
        health_score = self._calculate_health_score(
            pass_rate, len(slow_tests), len(failure_insights)
        )

        # Group failures by category
        failure_categories = {}
        for insight in failure_insights:
            cat = insight["category"]
            if cat not in failure_categories:
                failure_categories[cat] = 0
            failure_categories[cat] += 1

        # Generate recommendations
        recommendations = self._generate_recommendations(
            pass_rate, failure_categories, slow_tests
        )

        self.analysis = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": len(passed),
                "failed": len(failed),
                "errors": len(errors),
                "skipped": len(skipped),
                "pass_rate": round(pass_rate * 100, 1),
                "health_score": health_score
            },
            "failure_insights": failure_insights,
            "failure_categories": failure_categories,
            "slow_tests": slow_tests[:10],
            "recommendations": recommendations
        }

        return self.analysis

    def _calculate_health_score(self, pass_rate: float,
                                slow_count: int,
                                failure_count: int) -> str:
        """Calculate overall test suite health score.

        Returns:
            Score string: 'Excellent', 'Good', 'Fair', 'Poor', 'Critical'
        """
        score = pass_rate * 100

        # Penalize for slow tests
        score -= slow_count * 2

        # Penalize for failures
        score -= failure_count * 5

        if score >= 95:
            return "Excellent"
        elif score >= 85:
            return "Good"
        elif score >= 70:
            return "Fair"
        elif score >= 50:
            return "Poor"
        else:
            return "Critical"

    def _generate_recommendations(self, pass_rate: float,
                                  categories: Dict,
                                  slow_tests: List) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recs = []

        if pass_rate < 0.95:
            recs.append(
                f"Pass rate is {pass_rate*100:.1f}%. "
                f"Target is 95%. Focus on fixing failures below."
            )

        if categories.get("environment", 0) > 0:
            recs.append(
                "Environment issues detected. Run environment health "
                "check before tests: validate_environment fixture."
            )

        if categories.get("locator", 0) > 0:
            recs.append(
                "Locator failures found. Migrate to semantic locators: "
                "get_by_role(), get_by_test_id(), get_by_label()."
            )

        if categories.get("timing", 0) > 0:
            recs.append(
                "Timing issues detected. Remove time.sleep() and "
                "use Playwright auto-waiting or explicit wait conditions."
            )

        if categories.get("authentication", 0) > 0:
            recs.append(
                "Auth failures found. Check credentials in .env file "
                "and verify OAuth token expiration."
            )

        if categories.get("driver", 0) > 0:
            recs.append(
                "Driver initialization failures. Update webdriver-manager "
                "and clear cache: pip install --upgrade webdriver-manager"
            )

        if len(slow_tests) > 5:
            recs.append(
                f"{len(slow_tests)} slow tests detected (>30s). "
                f"Consider parallelizing with pytest-xdist: pytest -n auto"
            )

        if not recs:
            recs.append("Test suite is healthy. No immediate actions needed.")

        return recs

    def print_summary(self):
        """Print a formatted summary to console."""
        if not self.analysis:
            self.analyze()

        if not self.analysis or "error" in self.analysis:
            print("No test results to analyze.")
            return

        s = self.analysis["summary"]
        print("\n" + "=" * 60)
        print("  AI TEST INSIGHTS REPORT")
        print("=" * 60)
        print(f"\n  Health Score: {s['health_score']}")
        print(f"  Pass Rate:    {s['pass_rate']}%")
        print(f"  Total:        {s['total']} tests")
        print(f"  Passed:       {s['passed']}")
        print(f"  Failed:       {s['failed']}")
        print(f"  Errors:       {s['errors']}")
        print(f"  Skipped:      {s['skipped']}")

        # Failure breakdown
        if self.analysis["failure_categories"]:
            print(f"\n  Failure Categories:")
            for cat, count in self.analysis["failure_categories"].items():
                print(f"    {cat}: {count}")

        # Top failures with fixes
        if self.analysis["failure_insights"]:
            print(f"\n  Top Failures & Fixes:")
            for insight in self.analysis["failure_insights"][:5]:
                print(f"\n    [{insight['severity'].upper()}] {insight['test']}")
                print(f"    Category: {insight['category']}")
                print(f"    Issue: {insight['description']}")
                for line in insight['fix'].split('\n'):
                    print(f"    {line}")

        # Slow tests
        if self.analysis["slow_tests"]:
            print(f"\n  Slow Tests (>30s):")
            for t in self.analysis["slow_tests"][:5]:
                print(f"    {t['test']}: {t['duration']}s")

        # Recommendations
        print(f"\n  Recommendations:")
        for i, rec in enumerate(self.analysis["recommendations"], 1):
            print(f"    {i}. {rec}")

        print("\n" + "=" * 60)

    @allure.step("Attach AI Test Insights to Allure")
    def attach_to_allure(self):
        """Attach analysis results to Allure report."""
        if not self.analysis:
            self.analyze()

        if self.analysis:
            allure.attach(
                json.dumps(self.analysis, indent=2),
                name="AI Test Insights",
                attachment_type=allure.attachment_type.JSON
            )

    def save_report(self, output_path: str = "reports/ai_insights.json"):
        """Save analysis to JSON file.

        Args:
            output_path: Path to save the report
        """
        if not self.analysis:
            self.analyze()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        logger.info(f"AI insights saved to {output_path}")
