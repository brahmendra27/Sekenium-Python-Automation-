# framework/api_client.py

import requests
from typing import Optional, Dict, Any, Union
import json
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from framework.config import Config


class APIClient:
    """REST API client with built-in retry logic, logging, and response validation."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize API client with configuration.
        
        Args:
            config: Configuration object (creates new if not provided)
        """
        self.config = config or Config()
        self.base_url = self.config.api_base_url
        self.timeout = self.config.api_timeout
        self.verify_ssl = self.config.api_verify_ssl
        self.default_headers = self.config.api_default_headers.copy()
        
        self.session = requests.Session()
        self._setup_retry_strategy()
        
        self.logger = logging.getLogger(__name__)
    
    def _setup_retry_strategy(self, retries: int = 3, backoff_factor: float = 0.3):
        """Configure retry strategy for failed requests.
        
        Args:
            retries: Number of retry attempts
            backoff_factor: Backoff factor for exponential delay
        """
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=backoff_factor
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def set_auth_token(self, token: str, token_type: str = "Bearer"):
        """Set authentication token in default headers.
        
        Args:
            token: Authentication token
            token_type: Token type (default: Bearer)
        """
        self.default_headers['Authorization'] = f"{token_type} {token}"
    
    def set_header(self, key: str, value: str):
        """Set a custom header for all requests.
        
        Args:
            key: Header name
            value: Header value
        """
        self.default_headers[key] = value
    
    def remove_header(self, key: str):
        """Remove a header from default headers.
        
        Args:
            key: Header name to remove
        """
        self.default_headers.pop(key, None)
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL string
        """
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def _merge_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merge custom headers with default headers.
        
        Args:
            headers: Custom headers to merge
            
        Returns:
            Merged headers dictionary
        """
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log request details.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
        """
        self.logger.info(f"API Request: {method} {url}")
        if 'json' in kwargs:
            self.logger.debug(f"Request Body: {json.dumps(kwargs['json'], indent=2)}")
        if 'params' in kwargs:
            self.logger.debug(f"Query Params: {kwargs['params']}")
    
    def _log_response(self, response: requests.Response):
        """Log response details.
        
        Args:
            response: Response object
        """
        self.logger.info(f"API Response: {response.status_code} {response.reason}")
        try:
            self.logger.debug(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except ValueError:
            self.logger.debug(f"Response Body: {response.text[:500]}")
    
    def request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, Dict[str, Any]]] = None,
        timeout: Optional[int] = None,
        verify: Optional[bool] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with comprehensive options.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            headers: Custom headers
            params: Query parameters
            json_data: JSON request body
            data: Form data or raw body
            timeout: Request timeout (uses default if not provided)
            verify: SSL verification (uses default if not provided)
            **kwargs: Additional requests parameters
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        verify = verify if verify is not None else self.verify_ssl
        
        request_kwargs = {
            'headers': merged_headers,
            'timeout': timeout,
            'verify': verify,
            **kwargs
        }
        
        if params:
            request_kwargs['params'] = params
        if json_data:
            request_kwargs['json'] = json_data
        if data:
            request_kwargs['data'] = data
        
        self._log_request(method, url, **request_kwargs)
        
        response = self.session.request(method, url, **request_kwargs)
        
        self._log_response(response)
        
        return response
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make POST request.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PUT request.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request('PUT', endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PATCH request.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request('PATCH', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request('DELETE', endpoint, **kwargs)
    
    def close(self):
        """Close the session and cleanup resources."""
        self.session.close()


class APIResponse:
    """Wrapper for API response with validation and assertion helpers."""
    
    def __init__(self, response: requests.Response):
        """Initialize API response wrapper.
        
        Args:
            response: Requests response object
        """
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.text = response.text
        
        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None
    
    def assert_status_code(self, expected_code: int, message: str = ""):
        """Assert response status code.
        
        Args:
            expected_code: Expected status code
            message: Custom error message
            
        Raises:
            AssertionError: If status code doesn't match
        """
        msg = message or f"Expected status code {expected_code}, got {self.status_code}"
        assert self.status_code == expected_code, msg
    
    def assert_status_in(self, expected_codes: list, message: str = ""):
        """Assert response status code is in list of expected codes.
        
        Args:
            expected_codes: List of expected status codes
            message: Custom error message
            
        Raises:
            AssertionError: If status code not in list
        """
        msg = message or f"Expected status code in {expected_codes}, got {self.status_code}"
        assert self.status_code in expected_codes, msg
    
    def assert_json_contains(self, key: str, message: str = ""):
        """Assert JSON response contains key.
        
        Args:
            key: Key to check for
            message: Custom error message
            
        Raises:
            AssertionError: If key not found
        """
        assert self.json_data is not None, "Response is not JSON"
        msg = message or f"Expected key '{key}' in response"
        assert key in self.json_data, msg
    
    def assert_json_value(self, key: str, expected_value: Any, message: str = ""):
        """Assert JSON response key has expected value.
        
        Args:
            key: Key to check
            expected_value: Expected value
            message: Custom error message
            
        Raises:
            AssertionError: If value doesn't match
        """
        self.assert_json_contains(key)
        actual_value = self.json_data[key]
        msg = message or f"Expected {key}={expected_value}, got {actual_value}"
        assert actual_value == expected_value, msg
    
    def assert_header_exists(self, header_name: str, message: str = ""):
        """Assert response header exists.
        
        Args:
            header_name: Header name to check
            message: Custom error message
            
        Raises:
            AssertionError: If header not found
        """
        msg = message or f"Expected header '{header_name}' in response"
        assert header_name in self.headers, msg
    
    def get_json_value(self, key: str, default: Any = None) -> Any:
        """Get value from JSON response.
        
        Args:
            key: Key to retrieve
            default: Default value if key not found
            
        Returns:
            Value from JSON or default
        """
        if self.json_data is None:
            return default
        return self.json_data.get(key, default)
