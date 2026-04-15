# framework/report_utils.py

import os
import json
from typing import Dict, List


class ReportUtils:
    """Utilities for report generation and management."""
    
    @staticmethod
    def ensure_report_dir(report_dir: str):
        """Create report directory structure if it doesn't exist."""
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(f"{report_dir}/screenshots", exist_ok=True)
        os.makedirs(f"{report_dir}/traces", exist_ok=True)
    
    @staticmethod
    def parse_json_report(report_path: str) -> Dict:
        """Parse JSON report and extract summary statistics."""
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        summary = report.get('summary', {})
        return {
            'total': summary.get('total', 0),
            'passed': summary.get('passed', 0),
            'failed': summary.get('failed', 0),
            'skipped': summary.get('skipped', 0),
            'duration': summary.get('duration', 0),
            'tests': report.get('tests', [])
        }
    
    @staticmethod
    def generate_summary_text(report_path: str) -> str:
        """Generate human-readable summary from JSON report."""
        stats = ReportUtils.parse_json_report(report_path)
        
        summary = f"""
Test Execution Summary
======================
Total Tests: {stats['total']}
Passed: {stats['passed']}
Failed: {stats['failed']}
Skipped: {stats['skipped']}
Duration: {stats['duration']:.2f}s

"""
        if stats['failed'] > 0:
            summary += "Failed Tests:\n"
            for test in stats['tests']:
                if test.get('outcome') == 'failed':
                    summary += f"  - {test.get('nodeid')}: {test.get('call', {}).get('longrepr', 'No error message')}\n"
        
        return summary
