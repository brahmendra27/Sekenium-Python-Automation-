# framework/boomi_client.py

"""
Boomi Middleware Client for integration/middleware testing.

Supports:
  - Boomi AtomSphere API authentication
  - Process execution and monitoring
  - Execution record queries
  - Document tracking
  - Environment and Atom management
  - Integration flow validation

Usage:
    client = BoomiClient(account_id="BOOMI-XXXXX", username="user", password="pass")
    client.authenticate()
    result = client.execute_process(process_id, atom_id)
    client.wait_for_execution(result['executionId'])
"""

import time
import logging
from typing import Optional, Dict, Any, List
import requests
from requests.auth import HTTPBasicAuth
import allure

logger = logging.getLogger(__name__)


class BoomiClient:
    """Boomi AtomSphere API client for middleware integration testing."""

    BASE_URL = "https://api.boomi.com/api/rest/v1"

    def __init__(self, account_id: str = "", username: str = "",
                 password: str = "", **kwargs):
        """Initialize Boomi client.

        Args:
            account_id: Boomi account ID
            username: Boomi username (or API token user)
            password: Boomi password (or API token)
        """
        import os

        self.account_id = account_id or os.environ.get('BOOMI_ACCOUNT_ID', '')
        self.username = username or os.environ.get('BOOMI_USERNAME', '')
        self.password = password or os.environ.get('BOOMI_PASSWORD', '')

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _api_url(self, path: str) -> str:
        """Build Boomi API URL."""
        return f"{self.BASE_URL}/{self.account_id}/{path}"

    # ==================== PROCESS EXECUTION ====================

    @allure.step("Execute Boomi process: {process_id}")
    def execute_process(self, process_id: str, atom_id: str,
                        properties: Optional[Dict] = None) -> Dict:
        """Execute a Boomi process.

        Args:
            process_id: Process component ID
            atom_id: Atom/Molecule ID to run on
            properties: Optional dynamic process properties

        Returns:
            Execution request result with requestId
        """
        payload = {
            "ProcessProperties": {
                "@type": "ProcessProperties"
            },
            "processId": process_id,
            "atomId": atom_id
        }

        if properties:
            prop_list = []
            for key, value in properties.items():
                prop_list.append({
                    "@type": "ProcessProperty",
                    "Name": key,
                    "Value": str(value)
                })
            payload["ProcessProperties"]["ProcessProperty"] = prop_list

        resp = self.session.post(
            self._api_url("executeProcess"),
            json=payload, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(f"Process execution requested: {result.get('requestId')}")
        return result

    @allure.step("Wait for execution: {execution_id}")
    def wait_for_execution(self, execution_id: str,
                           timeout: int = 300,
                           poll_interval: int = 10) -> Dict:
        """Wait for a process execution to complete.

        Args:
            execution_id: Execution request ID
            timeout: Max wait time in seconds
            poll_interval: Seconds between status checks

        Returns:
            Final execution record

        Raises:
            TimeoutError: If execution doesn't complete within timeout
        """
        start = time.time()
        while time.time() - start < timeout:
            record = self.get_execution_record(execution_id)
            status = record.get('status', 'UNKNOWN')

            if status in ('COMPLETE', 'COMPLETE_WARN'):
                logger.info(f"Execution {execution_id} completed: {status}")
                return record
            elif status in ('ERROR', 'ABORTED', 'DISCARDED'):
                logger.error(f"Execution {execution_id} failed: {status}")
                return record

            logger.info(f"Execution {execution_id} status: {status}, waiting...")
            time.sleep(poll_interval)

        raise TimeoutError(
            f"Execution {execution_id} did not complete within {timeout}s"
        )

    # ==================== EXECUTION RECORDS ====================

    @allure.step("Get execution record: {execution_id}")
    def get_execution_record(self, execution_id: str) -> Dict:
        """Get execution record by ID.

        Args:
            execution_id: Execution ID

        Returns:
            Execution record dict
        """
        resp = self.session.get(
            self._api_url(f"ExecutionRecord/{execution_id}"),
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    @allure.step("Query execution records")
    def query_executions(self, process_id: Optional[str] = None,
                         status: Optional[str] = None,
                         limit: int = 100) -> List[Dict]:
        """Query execution records with filters.

        Args:
            process_id: Filter by process ID
            status: Filter by status (COMPLETE, ERROR, etc.)
            limit: Max records

        Returns:
            List of execution records
        """
        filters = []
        if process_id:
            filters.append({
                "argument": [process_id],
                "expression": {"operator": "EQUALS", "property": "processId"}
            })
        if status:
            filters.append({
                "argument": [status],
                "expression": {"operator": "EQUALS", "property": "status"}
            })

        payload = {
            "QueryFilter": {
                "expression": {
                    "operator": "and",
                    "nestedExpression": [f["expression"] for f in filters]
                } if len(filters) > 1 else (
                    filters[0]["expression"] if filters else {}
                ),
                "argument": [a for f in filters for a in f["argument"]]
            }
        } if filters else {}

        resp = self.session.post(
            self._api_url("ExecutionRecord/query"),
            json=payload, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        records = result.get('result', [])
        logger.info(f"Found {len(records)} execution records")
        return records[:limit]

    # ==================== DOCUMENT TRACKING ====================

    @allure.step("Get execution documents: {execution_id}")
    def get_execution_documents(self, execution_id: str) -> List[Dict]:
        """Get documents processed in an execution.

        Args:
            execution_id: Execution ID

        Returns:
            List of document records
        """
        resp = self.session.get(
            self._api_url(f"ExecutionRecord/{execution_id}/documents"),
            timeout=30
        )
        resp.raise_for_status()
        return resp.json().get('result', [])

    @allure.step("Get document content: {document_id}")
    def get_document_content(self, execution_id: str,
                             document_id: str) -> str:
        """Get content of a processed document.

        Args:
            execution_id: Execution ID
            document_id: Document ID

        Returns:
            Document content as string
        """
        resp = self.session.get(
            self._api_url(
                f"ExecutionRecord/{execution_id}/documents/{document_id}"
            ),
            timeout=30
        )
        resp.raise_for_status()
        return resp.text

    # ==================== ENVIRONMENT & ATOMS ====================

    @allure.step("List atoms")
    def list_atoms(self, status: str = "ONLINE") -> List[Dict]:
        """List Atoms/Molecules in the account.

        Args:
            status: Filter by status (ONLINE, OFFLINE)

        Returns:
            List of Atom records
        """
        payload = {
            "QueryFilter": {
                "expression": {
                    "operator": "EQUALS",
                    "property": "status",
                    "argument": [status]
                }
            }
        }
        resp = self.session.post(
            self._api_url("Atom/query"),
            json=payload, timeout=30
        )
        resp.raise_for_status()
        return resp.json().get('result', [])

    @allure.step("Get environment: {env_id}")
    def get_environment(self, env_id: str) -> Dict:
        """Get environment details.

        Args:
            env_id: Environment ID

        Returns:
            Environment record
        """
        resp = self.session.get(
            self._api_url(f"Environment/{env_id}"),
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    # ==================== INTEGRATION VALIDATION ====================

    @allure.step("Validate integration flow: {process_id}")
    def validate_integration(self, process_id: str, atom_id: str,
                             input_data: Optional[Dict] = None,
                             expected_status: str = "COMPLETE",
                             timeout: int = 300) -> Dict:
        """Execute a process and validate it completes successfully.

        This is a high-level helper for integration tests.

        Args:
            process_id: Process component ID
            atom_id: Atom ID
            input_data: Optional process properties
            expected_status: Expected final status
            timeout: Max wait time

        Returns:
            Final execution record

        Raises:
            AssertionError: If status doesn't match expected
        """
        result = self.execute_process(process_id, atom_id, input_data)
        request_id = result.get('requestId')

        if not request_id:
            raise RuntimeError(f"No requestId in response: {result}")

        record = self.wait_for_execution(request_id, timeout=timeout)
        actual_status = record.get('status', 'UNKNOWN')

        assert actual_status == expected_status, (
            f"Integration flow failed. "
            f"Expected: {expected_status}, Got: {actual_status}. "
            f"Execution ID: {request_id}"
        )

        return record

    # ==================== CLEANUP ====================

    def close(self):
        """Close the HTTP session."""
        self.session.close()
