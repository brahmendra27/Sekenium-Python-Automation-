# framework/api_helpers.py

"""
API Testing Helpers: Data-driven tests, request chaining, correlation tracking,
OAuth2 auto-refresh, and Allure request/response logging.

Modules:
  - DataDrivenHelper: Load test payloads from JSON/CSV files
  - RequestChain: Chain API calls with data extraction between steps
  - CorrelationTracker: Track requests across E-commerce → Boomi → Salesforce
  - OAuth2Manager: Auto-refresh expired tokens
  - AllureAPILogger: Attach request/response details to Allure reports
"""

import csv
import json
import time
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import requests
import allure

logger = logging.getLogger(__name__)


# ==================== DATA-DRIVEN TESTING ====================

class DataDrivenHelper:
    """Load test data from JSON/CSV files for parameterized API tests.

    Usage:
        data = DataDrivenHelper.from_json("tests/test_data/orders.json")
        data = DataDrivenHelper.from_csv("tests/test_data/users.csv")

        @pytest.mark.parametrize("payload", DataDrivenHelper.from_json("data.json"))
        def test_create_order(api_client, payload):
            response = api_client.post("/orders", json_data=payload)
    """

    @staticmethod
    def from_json(file_path: str) -> List[Dict]:
        """Load test data from a JSON file.

        Args:
            file_path: Path to JSON file (array of objects)

        Returns:
            List of dicts for parametrize
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with open(path) as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "test_cases" in data:
            return data["test_cases"]
        else:
            return [data]

    @staticmethod
    def from_csv(file_path: str) -> List[Dict]:
        """Load test data from a CSV file.

        Args:
            file_path: Path to CSV file (header row + data rows)

        Returns:
            List of dicts (one per row)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    @staticmethod
    def generate_payload(template: Dict, overrides: Optional[Dict] = None,
                         unique_id: str = "") -> Dict:
        """Generate a test payload from a template with overrides.

        Replaces {{unique_id}} placeholders in string values.

        Args:
            template: Base payload template
            overrides: Fields to override
            unique_id: Unique identifier for placeholder replacement

        Returns:
            Generated payload dict
        """
        uid = unique_id or str(uuid.uuid4())[:8]
        payload = json.loads(
            json.dumps(template).replace("{{unique_id}}", uid)
        )
        if overrides:
            payload.update(overrides)
        return payload


# ==================== REQUEST CHAINING ====================

class RequestChain:
    """Chain API calls with data extraction between steps.

    Usage:
        chain = RequestChain(api_client)
        chain.post("/orders", json_data={"item": "shoes", "qty": 1})
        chain.extract("order_id", "$.id")
        chain.get("/orders/{order_id}")
        chain.assert_status(200)
        chain.assert_json_value("status", "pending")
    """

    def __init__(self, client):
        """Initialize request chain.

        Args:
            client: APIClient instance
        """
        self.client = client
        self.variables: Dict[str, Any] = {}
        self.last_response = None
        self.steps: List[Dict] = []

    def _resolve_url(self, url: str) -> str:
        """Replace {variable} placeholders in URL with extracted values."""
        for key, value in self.variables.items():
            url = url.replace(f"{{{key}}}", str(value))
        return url

    def _resolve_data(self, data: Optional[Dict]) -> Optional[Dict]:
        """Replace {{variable}} placeholders in request data."""
        if data is None:
            return None
        resolved = json.dumps(data)
        for key, value in self.variables.items():
            resolved = resolved.replace(f"{{{{{key}}}}}", str(value))
        return json.loads(resolved)

    @allure.step("Chain: {method} {endpoint}")
    def request(self, method: str, endpoint: str, **kwargs) -> 'RequestChain':
        """Execute a chained request.

        Args:
            method: HTTP method
            endpoint: URL (supports {variable} placeholders)
            **kwargs: Additional request parameters

        Returns:
            self for chaining
        """
        url = self._resolve_url(endpoint)
        if "json_data" in kwargs:
            kwargs["json_data"] = self._resolve_data(kwargs["json_data"])

        self.last_response = self.client.request(method, url, **kwargs)
        self.steps.append({
            "method": method,
            "url": url,
            "status": self.last_response.status_code
        })
        return self

    def get(self, endpoint: str, **kwargs) -> 'RequestChain':
        """Chain a GET request."""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> 'RequestChain':
        """Chain a POST request."""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> 'RequestChain':
        """Chain a PUT request."""
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> 'RequestChain':
        """Chain a DELETE request."""
        return self.request("DELETE", endpoint, **kwargs)

    def extract(self, variable_name: str, json_path: str) -> 'RequestChain':
        """Extract a value from the last response and store it.

        Args:
            variable_name: Name to store the value as
            json_path: Dot-notation path (e.g., "data.id", "items[0].name")

        Returns:
            self for chaining
        """
        data = self.last_response.json()
        for key in json_path.replace("[", ".").replace("]", "").split("."):
            if key == "" or key == "$":
                continue
            if isinstance(data, list):
                data = data[int(key)]
            elif isinstance(data, dict):
                data = data[key]

        self.variables[variable_name] = data
        logger.info(f"Extracted {variable_name} = {data}")
        return self

    def set_variable(self, name: str, value: Any) -> 'RequestChain':
        """Manually set a chain variable.

        Args:
            name: Variable name
            value: Variable value

        Returns:
            self for chaining
        """
        self.variables[name] = value
        return self

    def assert_status(self, expected: int) -> 'RequestChain':
        """Assert last response status code.

        Returns:
            self for chaining
        """
        actual = self.last_response.status_code
        assert actual == expected, (
            f"Expected status {expected}, got {actual}. "
            f"Response: {self.last_response.text[:300]}"
        )
        return self

    def assert_json_value(self, key: str, expected: Any) -> 'RequestChain':
        """Assert a JSON value in the last response.

        Returns:
            self for chaining
        """
        data = self.last_response.json()
        actual = data.get(key)
        assert actual == expected, (
            f"Expected {key}={expected!r}, got {actual!r}"
        )
        return self

    def wait(self, seconds: float) -> 'RequestChain':
        """Wait between chained requests (for async processing).

        Args:
            seconds: Time to wait

        Returns:
            self for chaining
        """
        time.sleep(seconds)
        return self

    def get_variable(self, name: str) -> Any:
        """Get a stored variable value."""
        return self.variables.get(name)

    def get_summary(self) -> List[Dict]:
        """Get summary of all chained steps."""
        return self.steps


# ==================== CORRELATION TRACKING ====================

class CorrelationTracker:
    """Track requests across systems with correlation IDs.

    Adds a unique correlation ID to every request header, enabling
    end-to-end tracing across E-commerce → Boomi → Salesforce.

    Usage:
        tracker = CorrelationTracker()
        tracker.apply_to(api_client)
        tracker.apply_to(sf_client.session)
        # All requests now carry X-Correlation-ID header
        tracker.log_flow("order_created", {"order_id": "123"})
        tracker.log_flow("boomi_processed", {"execution_id": "abc"})
        tracker.log_flow("sf_updated", {"account_id": "001xxx"})
        tracker.print_flow()
    """

    def __init__(self, correlation_id: Optional[str] = None,
                 header_name: str = "X-Correlation-ID"):
        """Initialize correlation tracker.

        Args:
            correlation_id: Custom correlation ID (auto-generated if not provided)
            header_name: HTTP header name for the correlation ID
        """
        self.correlation_id = correlation_id or f"test-{uuid.uuid4().hex[:12]}"
        self.header_name = header_name
        self.flow_log: List[Dict] = []
        self.start_time = time.time()

    def apply_to(self, client_or_session):
        """Apply correlation ID header to an API client or session.

        Args:
            client_or_session: APIClient, SalesforceClient, BoomiClient,
                               or requests.Session
        """
        if hasattr(client_or_session, 'session'):
            client_or_session.session.headers[self.header_name] = self.correlation_id
        elif hasattr(client_or_session, 'headers'):
            client_or_session.headers[self.header_name] = self.correlation_id
        elif hasattr(client_or_session, 'default_headers'):
            client_or_session.default_headers[self.header_name] = self.correlation_id

        logger.info(f"Applied correlation ID {self.correlation_id} to client")

    def log_flow(self, step_name: str, data: Optional[Dict] = None):
        """Log a step in the cross-system flow.

        Args:
            step_name: Descriptive step name
            data: Additional data for this step
        """
        entry = {
            "step": step_name,
            "timestamp": time.time() - self.start_time,
            "correlation_id": self.correlation_id,
            "data": data or {}
        }
        self.flow_log.append(entry)
        logger.info(
            f"[{self.correlation_id}] {step_name}: {data}"
        )

    def print_flow(self):
        """Print the complete flow log."""
        print(f"\n{'='*50}")
        print(f"  Correlation Flow: {self.correlation_id}")
        print(f"{'='*50}")
        for entry in self.flow_log:
            elapsed = f"{entry['timestamp']:.1f}s"
            print(f"  [{elapsed}] {entry['step']}")
            if entry['data']:
                for k, v in entry['data'].items():
                    print(f"         {k}: {v}")
        print(f"{'='*50}\n")

    @allure.step("Attach correlation flow to Allure")
    def attach_to_allure(self):
        """Attach flow log to Allure report."""
        allure.attach(
            json.dumps(self.flow_log, indent=2),
            name=f"correlation_flow_{self.correlation_id}",
            attachment_type=allure.attachment_type.JSON
        )

    def get_flow(self) -> List[Dict]:
        """Get the complete flow log."""
        return self.flow_log


# ==================== OAUTH2 AUTO-REFRESH ====================

class OAuth2Manager:
    """OAuth2 token manager with automatic refresh.

    Handles token expiration and auto-refresh for long test runs.

    Usage:
        oauth = OAuth2Manager(
            token_url="https://login.salesforce.com/services/oauth2/token",
            client_id="xxx", client_secret="yyy"
        )
        oauth.authenticate()
        oauth.apply_to(api_client)
        # Token auto-refreshes when expired
    """

    def __init__(self, token_url: str, client_id: str,
                 client_secret: str, grant_type: str = "client_credentials",
                 username: str = "", password: str = "",
                 buffer_seconds: int = 300):
        """Initialize OAuth2 manager.

        Args:
            token_url: OAuth2 token endpoint
            client_id: Client ID
            client_secret: Client secret
            grant_type: Grant type (client_credentials, password)
            username: Username (for password grant)
            password: Password (for password grant)
            buffer_seconds: Refresh token this many seconds before expiry
        """
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.buffer_seconds = buffer_seconds

        self.access_token: Optional[str] = None
        self.token_expiry: float = 0
        self.refresh_token: Optional[str] = None
        self._clients: List = []

    def authenticate(self) -> bool:
        """Authenticate and obtain access token.

        Returns:
            True if successful
        """
        data = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        if self.grant_type == "password":
            data["username"] = self.username
            data["password"] = self.password

        resp = requests.post(self.token_url, data=data, timeout=30)
        if resp.status_code == 200:
            token_data = resp.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in
            self.refresh_token = token_data.get("refresh_token")
            logger.info(f"OAuth2 authenticated. Expires in {expires_in}s")
            self._update_clients()
            return True
        else:
            logger.error(f"OAuth2 auth failed: {resp.status_code}")
            return False

    def get_token(self) -> str:
        """Get current access token, refreshing if needed.

        Returns:
            Valid access token string
        """
        if self._is_expired():
            logger.info("Token expired, refreshing...")
            self.authenticate()
        return self.access_token or ""

    def _is_expired(self) -> bool:
        """Check if token is expired or about to expire."""
        return time.time() >= (self.token_expiry - self.buffer_seconds)

    def apply_to(self, client):
        """Apply token to an API client (auto-refreshes on expiry).

        Args:
            client: Any client with session.headers or default_headers
        """
        self._clients.append(client)
        self._update_client(client)

    def _update_clients(self):
        """Update all registered clients with current token."""
        for client in self._clients:
            self._update_client(client)

    def _update_client(self, client):
        """Update a single client's auth header."""
        token = self.access_token
        if hasattr(client, 'session'):
            client.session.headers["Authorization"] = f"Bearer {token}"
        elif hasattr(client, 'default_headers'):
            client.default_headers["Authorization"] = f"Bearer {token}"


# ==================== ALLURE API LOGGER ====================

class AllureAPILogger:
    """Attach API request/response details to Allure reports.

    Usage:
        logger = AllureAPILogger()
        response = api_client.get("/products")
        logger.log(response, "Get Products")
    """

    @staticmethod
    @allure.step("API: {name}")
    def log(response, name: str = "API Request"):
        """Log API request and response to Allure.

        Args:
            response: requests.Response object
            name: Step name for Allure
        """
        # Request details
        req = response.request
        request_info = (
            f"Method: {req.method}\n"
            f"URL: {req.url}\n"
            f"Headers: {dict(req.headers)}\n"
        )
        if req.body:
            try:
                body = json.dumps(json.loads(req.body), indent=2)
                request_info += f"Body:\n{body}"
            except (json.JSONDecodeError, TypeError):
                request_info += f"Body: {req.body[:500]}"

        allure.attach(
            request_info, name=f"{name} - Request",
            attachment_type=allure.attachment_type.TEXT
        )

        # Response details
        response_info = (
            f"Status: {response.status_code} {response.reason}\n"
            f"Time: {response.elapsed.total_seconds():.3f}s\n"
            f"Headers: {dict(response.headers)}\n"
        )
        try:
            body = json.dumps(response.json(), indent=2)
            response_info += f"Body:\n{body[:2000]}"
        except (json.JSONDecodeError, ValueError):
            response_info += f"Body: {response.text[:2000]}"

        allure.attach(
            response_info, name=f"{name} - Response",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def log_chain(chain: RequestChain, name: str = "Request Chain"):
        """Log a complete request chain to Allure.

        Args:
            chain: RequestChain instance
            name: Step name
        """
        summary = json.dumps(chain.get_summary(), indent=2)
        variables = json.dumps(chain.variables, indent=2, default=str)

        allure.attach(
            f"Steps:\n{summary}\n\nVariables:\n{variables}",
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
