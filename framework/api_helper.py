# framework/api_helper.py

"""
ApiHelper — Single source of truth for HTTP operations.

This is the shared HTTP client used by all API tests.
Tests should NEVER instantiate this directly — use the api_client fixture.

Supports:
  - send() with request builder bundles (preferred)
  - Direct get/post/put/patch/delete methods
  - Automatic auth token management per request
  - Base URL override per request
  - Allure step logging
  - Response time tracking

Usage via fixture:
    def test_create_order(api_client):
        response = api_client.send(build_order_payload())
        assert response.status_code == 201

DO NOT DUPLICATE this file. Projects should re-export:
    from framework.api_helper import ApiHelper
"""

import json
import logging
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import allure

logger = logging.getLogger(__name__)


class ApiHelper:
    """Shared HTTP client for all API tests.

    Preferred usage is via send() with request builder bundles.
    Direct methods (get, post, put, delete) are available as fallback.
    """

    def __init__(self, base_url: str = "", auth_token: str = "",
                 timeout: int = 30):
        """Initialize ApiHelper.

        Args:
            base_url: Default base URL (can be overridden per request)
            auth_token: Default auth token (can be overridden per request)
            timeout: Default request timeout in seconds
        """
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.auth_token = auth_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        # Setup retry strategy
        retry = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=0.3
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        if auth_token:
            self.session.headers["Authorization"] = f"Bearer {auth_token}"

    # ==================== SEND (PREFERRED) ====================

    @allure.step("API: {request_bundle[method]} {request_bundle[endpoint]}")
    def send(self, request_bundle: Dict[str, Any]) -> requests.Response:
        """Execute a request from a builder bundle.

        This is the PREFERRED method. Builders in api_endpoints.py
        return bundles with all request details.

        Bundle keys:
            method (str): HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint (str): URL path (e.g., "/orders")
            base_url (str, optional): Override base URL for this request
            auth_token (str, optional): Override auth token for this request
            payload (dict, optional): Request body (JSON)
            params (dict, optional): Query parameters
            headers (dict, optional): Additional headers

        Args:
            request_bundle: Dict from a builder function

        Returns:
            requests.Response
        """
        method = request_bundle.get("method", "GET").upper()
        endpoint = request_bundle.get("endpoint", "")
        base_url = request_bundle.get("base_url", self.base_url)
        auth_token = request_bundle.get("auth_token", self.auth_token)
        payload = request_bundle.get("payload")
        params = request_bundle.get("params")
        extra_headers = request_bundle.get("headers", {})

        # Build full URL
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}" if base_url else endpoint

        # Temporarily override auth if bundle provides one
        original_auth = self.session.headers.get("Authorization")
        if auth_token:
            self.session.headers["Authorization"] = f"Bearer {auth_token}"

        # Merge extra headers
        if extra_headers:
            self.session.headers.update(extra_headers)

        try:
            # Log request
            self._log_request(method, url, payload, params)

            # Execute request
            kwargs = {"timeout": self.timeout}
            if payload:
                kwargs["json"] = payload
            if params:
                kwargs["params"] = params

            response = self.session.request(method, url, **kwargs)

            # Log response
            self._log_response(response)

            # Attach to Allure
            self._allure_attach(method, url, payload, params, response)

            return response

        finally:
            # Restore original auth
            if original_auth:
                self.session.headers["Authorization"] = original_auth
            elif "Authorization" in self.session.headers and not self.auth_token:
                del self.session.headers["Authorization"]

            # Remove extra headers
            for key in extra_headers:
                if key in self.session.headers:
                    del self.session.headers[key]

    # ==================== DIRECT METHODS ====================

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict] = None,
            **kwargs) -> requests.Response:
        """Direct GET request."""
        url = self._build_url(endpoint)
        self._log_request("GET", url, params=params)
        response = self.session.get(url, params=params,
                                     timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, payload: Optional[Dict] = None,
             **kwargs) -> requests.Response:
        """Direct POST request."""
        url = self._build_url(endpoint)
        self._log_request("POST", url, payload)
        response = self.session.post(url, json=payload,
                                      timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, payload: Optional[Dict] = None,
            **kwargs) -> requests.Response:
        """Direct PUT request."""
        url = self._build_url(endpoint)
        self._log_request("PUT", url, payload)
        response = self.session.put(url, json=payload,
                                     timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    @allure.step("PATCH {endpoint}")
    def patch(self, endpoint: str, payload: Optional[Dict] = None,
              **kwargs) -> requests.Response:
        """Direct PATCH request."""
        url = self._build_url(endpoint)
        self._log_request("PATCH", url, payload)
        response = self.session.patch(url, json=payload,
                                       timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Direct DELETE request."""
        url = self._build_url(endpoint)
        self._log_request("DELETE", url)
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    # ==================== AUTH ====================

    def set_auth_token(self, token: str, token_type: str = "Bearer"):
        """Set default auth token."""
        self.auth_token = token
        self.session.headers["Authorization"] = f"{token_type} {token}"

    def set_basic_auth(self, username: str, password: str):
        """Set HTTP Basic authentication."""
        self.session.auth = (username, password)

    def set_header(self, key: str, value: str):
        """Set a custom default header."""
        self.session.headers[key] = value

    # ==================== INTERNAL ====================

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint

    def _log_request(self, method: str, url: str,
                     payload: Optional[Dict] = None,
                     params: Optional[Dict] = None):
        """Log request details."""
        logger.info(f"→ {method} {url}")
        if payload:
            logger.debug(f"  Body: {json.dumps(payload, indent=2)[:500]}")
        if params:
            logger.debug(f"  Params: {params}")

    def _log_response(self, response: requests.Response):
        """Log response details."""
        elapsed = response.elapsed.total_seconds()
        logger.info(f"← {response.status_code} ({elapsed:.3f}s)")
        if not (200 <= response.status_code < 300):
            logger.warning(f"  Body: {response.text[:500]}")

    def _allure_attach(self, method: str, url: str,
                       payload: Optional[Dict],
                       params: Optional[Dict],
                       response: requests.Response):
        """Attach request/response to Allure report."""
        # Request
        req_info = f"{method} {url}\n"
        if params:
            req_info += f"Params: {json.dumps(params, indent=2)}\n"
        if payload:
            req_info += f"Body:\n{json.dumps(payload, indent=2)[:2000]}"
        allure.attach(req_info, name="Request",
                      attachment_type=allure.attachment_type.TEXT)

        # Response
        resp_info = f"Status: {response.status_code}\n"
        resp_info += f"Time: {response.elapsed.total_seconds():.3f}s\n"
        try:
            resp_info += f"Body:\n{json.dumps(response.json(), indent=2)[:2000]}"
        except (json.JSONDecodeError, ValueError):
            resp_info += f"Body:\n{response.text[:2000]}"
        allure.attach(resp_info, name="Response",
                      attachment_type=allure.attachment_type.TEXT)

    # ==================== CLEANUP ====================

    def close(self):
        """Close the HTTP session."""
        self.session.close()
