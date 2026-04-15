# tests/test_config.py

import pytest
import os
import tempfile
import yaml
from framework.config import Config


class TestConfig:
    """Unit tests for Config class."""
    
    def test_load_valid_config_file(self):
        """Test loading a valid config file with all properties."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'base_url': 'https://example.com',
                'browser': 'firefox',
                'headless': True,
                'timeout': 60,
                'parallel_workers': 4,
                'report_dir': 'custom_reports'
            }
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            # Load config from temporary file
            config = Config(config_path=temp_config_path)
            
            # Verify all properties are loaded correctly
            assert config.base_url == 'https://example.com'
            assert config.browser == 'firefox'
            assert config.headless is True
            assert config.timeout == 60
            assert config.parallel_workers == 4
            assert config.report_dir == 'custom_reports'
        finally:
            # Clean up temporary file
            os.unlink(temp_config_path)
    
    def test_fallback_to_defaults_when_config_missing(self):
        """Test that Config falls back to default values when config file is missing."""
        # Use a non-existent config file path
        config = Config(config_path='nonexistent_config.yaml')
        
        # Verify all properties return default values
        assert config.base_url == 'http://localhost:8080'
        assert config.browser == 'chrome'
        assert config.headless is False
        assert config.timeout == 30
        assert config.parallel_workers == 1
        assert config.report_dir == 'reports'
    
    def test_fallback_to_defaults_for_missing_keys(self):
        """Test that Config falls back to defaults for missing keys in config file."""
        # Create a temporary config file with only some properties
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'base_url': 'https://partial.com',
                'browser': 'firefox'
                # Missing: headless, timeout, parallel_workers, report_dir
            }
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Verify specified properties are loaded
            assert config.base_url == 'https://partial.com'
            assert config.browser == 'firefox'
            
            # Verify missing properties fall back to defaults
            assert config.headless is False
            assert config.timeout == 30
            assert config.parallel_workers == 1
            assert config.report_dir == 'reports'
        finally:
            os.unlink(temp_config_path)
    
    def test_property_accessors_return_correct_values(self):
        """Test that all property accessors return correct values from config."""
        # Create a temporary config file with custom values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'base_url': 'https://test.example.com',
                'browser': 'webkit',
                'headless': True,
                'timeout': 45,
                'parallel_workers': 8,
                'report_dir': 'test_reports'
            }
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Test each property accessor
            assert config.base_url == 'https://test.example.com'
            assert config.browser == 'webkit'
            assert config.headless is True
            assert config.timeout == 45
            assert config.parallel_workers == 8
            assert config.report_dir == 'test_reports'
        finally:
            os.unlink(temp_config_path)
    
    def test_get_method_with_existing_key(self):
        """Test get method returns value for existing key."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'custom_key': 'custom_value',
                'nested': {
                    'key': 'value'
                }
            }
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Test get method with existing keys
            assert config.get('custom_key') == 'custom_value'
            assert config.get('nested') == {'key': 'value'}
        finally:
            os.unlink(temp_config_path)
    
    def test_get_method_with_custom_defaults(self):
        """Test get method with custom default values for missing keys."""
        config = Config(config_path='nonexistent_config.yaml')
        
        # Test get method with custom defaults
        assert config.get('missing_key', 'default_value') == 'default_value'
        assert config.get('another_missing', 42) == 42
        assert config.get('bool_missing', True) is True
        assert config.get('list_missing', [1, 2, 3]) == [1, 2, 3]
        assert config.get('dict_missing', {'key': 'value'}) == {'key': 'value'}
    
    def test_get_method_returns_none_when_no_default(self):
        """Test get method returns None when key is missing and no default provided."""
        config = Config(config_path='nonexistent_config.yaml')
        
        # Test get method without default
        assert config.get('missing_key') is None
    
    def test_empty_config_file(self):
        """Test loading an empty config file falls back to defaults."""
        # Create an empty config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('')  # Empty file
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Verify all properties return default values
            assert config.base_url == 'http://localhost:8080'
            assert config.browser == 'chrome'
            assert config.headless is False
            assert config.timeout == 30
            assert config.parallel_workers == 1
            assert config.report_dir == 'reports'
        finally:
            os.unlink(temp_config_path)
    
    def test_config_with_null_values(self):
        """Test config file with null values returns None (not defaults)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('base_url: null\nbrowser: null\n')
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Verify null values are returned as None (key exists but value is None)
            # This is expected behavior - explicit null is different from missing key
            assert config.base_url is None
            assert config.browser is None
        finally:
            os.unlink(temp_config_path)
    
    def test_config_path_attribute(self):
        """Test that config_path attribute is set correctly."""
        config = Config(config_path='custom_path.yaml')
        assert config.config_path == 'custom_path.yaml'
        
        config_default = Config()
        assert config_default.config_path == 'config.yaml'
    
    def test_nested_config_values(self):
        """Test accessing nested configuration values using get method."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'selenium': {
                    'implicit_wait': 10,
                    'page_load_timeout': 60
                },
                'playwright': {
                    'slow_mo': 100,
                    'tracing': True
                }
            }
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = Config(config_path=temp_config_path)
            
            # Test accessing nested values
            selenium_config = config.get('selenium')
            assert selenium_config == {'implicit_wait': 10, 'page_load_timeout': 60}
            
            playwright_config = config.get('playwright')
            assert playwright_config == {'slow_mo': 100, 'tracing': True}
        finally:
            os.unlink(temp_config_path)
