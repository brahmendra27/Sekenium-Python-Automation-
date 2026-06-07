# framework/performance_helper.py

"""
Performance Testing Helper for UI and API response time validation.

Provides:
  - Page load time measurement
  - Core Web Vitals (LCP, FID, CLS)
  - API response time assertions
  - Performance budget enforcement

Usage:
    perf = PerformanceHelper(page)
    metrics = perf.get_page_metrics()
    perf.assert_page_load_under(3000)
    perf.assert_lcp_under(2500)
"""

import time
import logging
from typing import Dict, Optional
from playwright.sync_api import Page
import allure

logger = logging.getLogger(__name__)


class PerformanceHelper:
    """Performance measurement and assertion helper."""

    def __init__(self, page: Page):
        """Initialize with a Playwright page.

        Args:
            page: Playwright Page instance
        """
        self.page = page

    @allure.step("Get page performance metrics")
    def get_page_metrics(self) -> Dict:
        """Get page load performance metrics using Navigation Timing API.

        Returns:
            Dict with timing metrics in milliseconds:
            - page_load_time: Total page load time
            - dom_content_loaded: DOMContentLoaded time
            - dom_interactive: DOM interactive time
            - first_byte: Time to first byte (TTFB)
            - dns_lookup: DNS lookup time
            - tcp_connect: TCP connection time
            - response_time: Server response time
        """
        metrics = self.page.evaluate("""() => {
            const perf = performance.getEntriesByType('navigation')[0];
            if (!perf) return {};
            return {
                page_load_time: Math.round(perf.loadEventEnd - perf.startTime),
                dom_content_loaded: Math.round(perf.domContentLoadedEventEnd - perf.startTime),
                dom_interactive: Math.round(perf.domInteractive - perf.startTime),
                first_byte: Math.round(perf.responseStart - perf.startTime),
                dns_lookup: Math.round(perf.domainLookupEnd - perf.domainLookupStart),
                tcp_connect: Math.round(perf.connectEnd - perf.connectStart),
                response_time: Math.round(perf.responseEnd - perf.requestStart),
                transfer_size: perf.transferSize || 0,
                dom_complete: Math.round(perf.domComplete - perf.startTime)
            };
        }""")

        logger.info(f"Page metrics: {metrics}")
        allure.attach(
            str(metrics), name="performance_metrics",
            attachment_type=allure.attachment_type.TEXT
        )
        return metrics

    @allure.step("Get Core Web Vitals")
    def get_web_vitals(self) -> Dict:
        """Get Core Web Vitals (LCP, CLS) from the page.

        Returns:
            Dict with:
            - lcp: Largest Contentful Paint (ms)
            - cls: Cumulative Layout Shift (score)
        """
        vitals = self.page.evaluate("""() => {
            return new Promise((resolve) => {
                const result = { lcp: 0, cls: 0 };

                // LCP
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    if (entries.length > 0) {
                        result.lcp = Math.round(entries[entries.length - 1].startTime);
                    }
                });
                try { lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true }); }
                catch(e) {}

                // CLS
                const clsObserver = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            result.cls += entry.value;
                        }
                    }
                    result.cls = Math.round(result.cls * 1000) / 1000;
                });
                try { clsObserver.observe({ type: 'layout-shift', buffered: true }); }
                catch(e) {}

                // Give observers time to collect
                setTimeout(() => {
                    lcpObserver.disconnect();
                    clsObserver.disconnect();
                    resolve(result);
                }, 1000);
            });
        }""")

        logger.info(f"Web Vitals: LCP={vitals.get('lcp')}ms, CLS={vitals.get('cls')}")
        return vitals

    @allure.step("Get resource loading stats")
    def get_resource_stats(self) -> Dict:
        """Get resource loading statistics.

        Returns:
            Dict with resource counts and sizes by type
        """
        stats = self.page.evaluate("""() => {
            const resources = performance.getEntriesByType('resource');
            const byType = {};
            let totalSize = 0;
            let totalDuration = 0;

            resources.forEach(r => {
                const type = r.initiatorType || 'other';
                if (!byType[type]) {
                    byType[type] = { count: 0, totalSize: 0, totalDuration: 0 };
                }
                byType[type].count++;
                byType[type].totalSize += r.transferSize || 0;
                byType[type].totalDuration += r.duration || 0;
                totalSize += r.transferSize || 0;
                totalDuration += r.duration || 0;
            });

            return {
                total_resources: resources.length,
                total_transfer_size_kb: Math.round(totalSize / 1024),
                by_type: byType
            };
        }""")

        logger.info(f"Resources: {stats.get('total_resources')} files, "
                     f"{stats.get('total_transfer_size_kb')}KB")
        return stats

    # ==================== ASSERTIONS ====================

    @allure.step("Assert page load under {max_ms}ms")
    def assert_page_load_under(self, max_ms: int):
        """Assert total page load time is under threshold.

        Args:
            max_ms: Maximum allowed page load time in milliseconds
        """
        metrics = self.get_page_metrics()
        actual = metrics.get("page_load_time", 0)
        assert actual <= max_ms, (
            f"Page load time {actual}ms exceeds budget of {max_ms}ms"
        )

    @allure.step("Assert TTFB under {max_ms}ms")
    def assert_ttfb_under(self, max_ms: int):
        """Assert Time to First Byte is under threshold.

        Args:
            max_ms: Maximum allowed TTFB in milliseconds
        """
        metrics = self.get_page_metrics()
        actual = metrics.get("first_byte", 0)
        assert actual <= max_ms, (
            f"TTFB {actual}ms exceeds budget of {max_ms}ms"
        )

    @allure.step("Assert LCP under {max_ms}ms")
    def assert_lcp_under(self, max_ms: int):
        """Assert Largest Contentful Paint is under threshold.

        Good: < 2500ms, Needs improvement: < 4000ms, Poor: > 4000ms

        Args:
            max_ms: Maximum allowed LCP in milliseconds
        """
        vitals = self.get_web_vitals()
        actual = vitals.get("lcp", 0)
        assert actual <= max_ms, (
            f"LCP {actual}ms exceeds budget of {max_ms}ms"
        )

    @allure.step("Assert CLS under {max_score}")
    def assert_cls_under(self, max_score: float):
        """Assert Cumulative Layout Shift is under threshold.

        Good: < 0.1, Needs improvement: < 0.25, Poor: > 0.25

        Args:
            max_score: Maximum allowed CLS score
        """
        vitals = self.get_web_vitals()
        actual = vitals.get("cls", 0)
        assert actual <= max_score, (
            f"CLS {actual} exceeds budget of {max_score}"
        )


class APIPerformanceHelper:
    """API response time measurement and assertion helper."""

    @staticmethod
    @allure.step("Assert API response under {max_ms}ms")
    def assert_response_time(response, max_ms: int):
        """Assert API response time is under threshold.

        Args:
            response: requests.Response or APIResponse object
            max_ms: Maximum allowed response time in milliseconds
        """
        if hasattr(response, 'elapsed'):
            actual_ms = response.elapsed.total_seconds() * 1000
        elif hasattr(response, 'response'):
            actual_ms = response.response.elapsed.total_seconds() * 1000
        else:
            raise ValueError("Response object has no elapsed attribute")

        assert actual_ms <= max_ms, (
            f"API response time {actual_ms:.0f}ms exceeds "
            f"budget of {max_ms}ms"
        )

    @staticmethod
    def measure_endpoint(session, method: str, url: str,
                         iterations: int = 5, **kwargs) -> Dict:
        """Measure average response time for an endpoint.

        Args:
            session: requests.Session
            method: HTTP method
            url: Full URL
            iterations: Number of requests to average
            **kwargs: Additional request parameters

        Returns:
            Dict with min, max, avg, p95 response times in ms
        """
        times = []
        for _ in range(iterations):
            start = time.time()
            session.request(method, url, **kwargs)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)

        times.sort()
        p95_idx = int(len(times) * 0.95)

        result = {
            "min_ms": round(min(times), 1),
            "max_ms": round(max(times), 1),
            "avg_ms": round(sum(times) / len(times), 1),
            "p95_ms": round(times[p95_idx] if p95_idx < len(times) else times[-1], 1),
            "iterations": iterations
        }
        logger.info(f"Endpoint performance: {result}")
        return result
