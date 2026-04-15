# tests/test_report_utils.py

import pytest
import os
import json
import tempfile
import shutil
from framework.report_utils import ReportUtils


class TestReportUtils:
    """Unit tests for ReportUtils class."""
    
    def test_ensure_report_dir_creates_main_directory(self):
        """Test that ensure_report_dir creates the main report directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'test_reports')
            
            # Ensure directory doesn't exist
            assert not os.path.exists(report_dir)
            
            # Create report directory structure
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify main directory was created
            assert os.path.exists(report_dir)
            assert os.path.isdir(report_dir)
    
    def test_ensure_report_dir_creates_screenshots_subdirectory(self):
        """Test that ensure_report_dir creates screenshots subdirectory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'test_reports')
            
            # Create report directory structure
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify screenshots subdirectory was created
            screenshots_dir = os.path.join(report_dir, 'screenshots')
            assert os.path.exists(screenshots_dir)
            assert os.path.isdir(screenshots_dir)
    
    def test_ensure_report_dir_creates_traces_subdirectory(self):
        """Test that ensure_report_dir creates traces subdirectory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'test_reports')
            
            # Create report directory structure
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify traces subdirectory was created
            traces_dir = os.path.join(report_dir, 'traces')
            assert os.path.exists(traces_dir)
            assert os.path.isdir(traces_dir)
    
    def test_ensure_report_dir_handles_existing_directory(self):
        """Test that ensure_report_dir handles existing directories gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'test_reports')
            
            # Create directory manually
            os.makedirs(report_dir)
            
            # Should not raise exception
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify directory still exists
            assert os.path.exists(report_dir)
    
    def test_ensure_report_dir_handles_existing_subdirectories(self):
        """Test that ensure_report_dir handles existing subdirectories gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'test_reports')
            screenshots_dir = os.path.join(report_dir, 'screenshots')
            traces_dir = os.path.join(report_dir, 'traces')
            
            # Create directories manually
            os.makedirs(screenshots_dir)
            os.makedirs(traces_dir)
            
            # Should not raise exception
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify directories still exist
            assert os.path.exists(report_dir)
            assert os.path.exists(screenshots_dir)
            assert os.path.exists(traces_dir)
    
    def test_parse_json_report_extracts_total_tests(self):
        """Test that parse_json_report extracts total test count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 10,
                    'passed': 8,
                    'failed': 2,
                    'skipped': 0,
                    'duration': 15.5
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['total'] == 10
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_extracts_passed_tests(self):
        """Test that parse_json_report extracts passed test count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 10,
                    'passed': 8,
                    'failed': 2,
                    'skipped': 0,
                    'duration': 15.5
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['passed'] == 8
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_extracts_failed_tests(self):
        """Test that parse_json_report extracts failed test count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 10,
                    'passed': 8,
                    'failed': 2,
                    'skipped': 0,
                    'duration': 15.5
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['failed'] == 2
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_extracts_skipped_tests(self):
        """Test that parse_json_report extracts skipped test count."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 10,
                    'passed': 7,
                    'failed': 2,
                    'skipped': 1,
                    'duration': 15.5
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['skipped'] == 1
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_extracts_duration(self):
        """Test that parse_json_report extracts test duration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 10,
                    'passed': 8,
                    'failed': 2,
                    'skipped': 0,
                    'duration': 15.5
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['duration'] == 15.5
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_extracts_tests_list(self):
        """Test that parse_json_report extracts tests list."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 2,
                    'passed': 1,
                    'failed': 1,
                    'skipped': 0,
                    'duration': 5.0
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_pass', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_fail', 'outcome': 'failed'}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert len(stats['tests']) == 2
            assert stats['tests'][0]['nodeid'] == 'test_example.py::test_pass'
            assert stats['tests'][1]['nodeid'] == 'test_example.py::test_fail'
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_handles_missing_summary(self):
        """Test that parse_json_report handles missing summary gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['total'] == 0
            assert stats['passed'] == 0
            assert stats['failed'] == 0
            assert stats['skipped'] == 0
            assert stats['duration'] == 0
        finally:
            os.unlink(temp_report_path)
    
    def test_parse_json_report_handles_missing_tests(self):
        """Test that parse_json_report handles missing tests list gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'duration': 0
                }
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            assert stats['tests'] == []
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_with_passed_tests(self):
        """Test summary text generation with all tests passed."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 5,
                    'passed': 5,
                    'failed': 0,
                    'skipped': 0,
                    'duration': 10.25
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_1', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_2', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_3', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_4', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_5', 'outcome': 'passed'}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify summary contains expected information
            assert 'Test Execution Summary' in summary
            assert 'Total Tests: 5' in summary
            assert 'Passed: 5' in summary
            assert 'Failed: 0' in summary
            assert 'Skipped: 0' in summary
            assert 'Duration: 10.25s' in summary
            
            # Verify no failed tests section
            assert 'Failed Tests:' not in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_with_failed_tests(self):
        """Test summary text generation with failed tests."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 5,
                    'passed': 3,
                    'failed': 2,
                    'skipped': 0,
                    'duration': 12.5
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_1', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_2', 'outcome': 'failed', 'call': {'longrepr': 'AssertionError: Expected True'}},
                    {'nodeid': 'test_example.py::test_3', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_4', 'outcome': 'failed', 'call': {'longrepr': 'ValueError: Invalid input'}},
                    {'nodeid': 'test_example.py::test_5', 'outcome': 'passed'}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify summary contains expected information
            assert 'Test Execution Summary' in summary
            assert 'Total Tests: 5' in summary
            assert 'Passed: 3' in summary
            assert 'Failed: 2' in summary
            assert 'Skipped: 0' in summary
            assert 'Duration: 12.50s' in summary
            
            # Verify failed tests section
            assert 'Failed Tests:' in summary
            assert 'test_example.py::test_2' in summary
            assert 'AssertionError: Expected True' in summary
            assert 'test_example.py::test_4' in summary
            assert 'ValueError: Invalid input' in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_with_skipped_tests(self):
        """Test summary text generation with skipped tests."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 5,
                    'passed': 3,
                    'failed': 0,
                    'skipped': 2,
                    'duration': 8.0
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_1', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_2', 'outcome': 'skipped'},
                    {'nodeid': 'test_example.py::test_3', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_4', 'outcome': 'skipped'},
                    {'nodeid': 'test_example.py::test_5', 'outcome': 'passed'}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify summary contains expected information
            assert 'Total Tests: 5' in summary
            assert 'Passed: 3' in summary
            assert 'Failed: 0' in summary
            assert 'Skipped: 2' in summary
            assert 'Duration: 8.00s' in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_handles_missing_error_message(self):
        """Test summary text generation handles missing error messages gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 2,
                    'passed': 1,
                    'failed': 1,
                    'skipped': 0,
                    'duration': 5.0
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_1', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_2', 'outcome': 'failed', 'call': {}}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify summary contains failed test with default message
            assert 'Failed Tests:' in summary
            assert 'test_example.py::test_2' in summary
            assert 'No error message' in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_handles_missing_call_section(self):
        """Test summary text generation handles missing call section gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 2,
                    'passed': 1,
                    'failed': 1,
                    'skipped': 0,
                    'duration': 5.0
                },
                'tests': [
                    {'nodeid': 'test_example.py::test_1', 'outcome': 'passed'},
                    {'nodeid': 'test_example.py::test_2', 'outcome': 'failed'}
                ]
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify summary contains failed test with default message
            assert 'Failed Tests:' in summary
            assert 'test_example.py::test_2' in summary
            assert 'No error message' in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_generate_summary_text_formats_duration_correctly(self):
        """Test that summary text formats duration with 2 decimal places."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {
                    'total': 1,
                    'passed': 1,
                    'failed': 0,
                    'skipped': 0,
                    'duration': 3.14159
                },
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            summary = ReportUtils.generate_summary_text(temp_report_path)
            
            # Verify duration is formatted with 2 decimal places
            assert 'Duration: 3.14s' in summary
        finally:
            os.unlink(temp_report_path)
    
    def test_ensure_report_dir_with_nested_path(self):
        """Test that ensure_report_dir handles nested directory paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report_dir = os.path.join(temp_dir, 'nested', 'path', 'reports')
            
            # Create report directory structure
            ReportUtils.ensure_report_dir(report_dir)
            
            # Verify all directories were created
            assert os.path.exists(report_dir)
            assert os.path.exists(os.path.join(report_dir, 'screenshots'))
            assert os.path.exists(os.path.join(report_dir, 'traces'))
    
    def test_parse_json_report_with_empty_summary_values(self):
        """Test that parse_json_report handles empty summary values."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_data = {
                'summary': {},
                'tests': []
            }
            json.dump(report_data, f)
            temp_report_path = f.name
        
        try:
            stats = ReportUtils.parse_json_report(temp_report_path)
            
            # Verify defaults are returned
            assert stats['total'] == 0
            assert stats['passed'] == 0
            assert stats['failed'] == 0
            assert stats['skipped'] == 0
            assert stats['duration'] == 0
            assert stats['tests'] == []
        finally:
            os.unlink(temp_report_path)
