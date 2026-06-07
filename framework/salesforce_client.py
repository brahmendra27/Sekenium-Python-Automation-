# framework/salesforce_client.py

"""
Salesforce API Client for CRM and Loyalty Management testing.

Supports:
  - OAuth2 authentication (username-password flow, client credentials)
  - SOQL queries
  - CRUD operations on Salesforce objects
  - Bulk API operations
  - Loyalty Management specific operations
  - Composite API for multi-object transactions

Usage:
    client = SalesforceClient(config)
    client.authenticate()
    accounts = client.query("SELECT Id, Name FROM Account LIMIT 10")
    client.create("Contact", {"FirstName": "Test", "LastName": "User"})
"""

import json
import logging
from typing import Optional, Dict, Any, List
import requests
import allure

logger = logging.getLogger(__name__)


class SalesforceClient:
    """Salesforce REST API client for CRM and Loyalty Management testing."""

    API_VERSION = "v59.0"

    def __init__(self, config=None, **kwargs):
        """Initialize Salesforce client.

        Args:
            config: Config object with salesforce settings, or pass kwargs:
                instance_url, client_id, client_secret, username, password,
                security_token, login_url
        """
        import os

        self.instance_url = kwargs.get('instance_url') or os.environ.get(
            'SF_INSTANCE_URL', ''
        )
        self.client_id = kwargs.get('client_id') or os.environ.get(
            'SF_CLIENT_ID', ''
        )
        self.client_secret = kwargs.get('client_secret') or os.environ.get(
            'SF_CLIENT_SECRET', ''
        )
        self.username = kwargs.get('username') or os.environ.get(
            'SF_USERNAME', ''
        )
        self.password = kwargs.get('password') or os.environ.get(
            'SF_PASSWORD', ''
        )
        self.security_token = kwargs.get('security_token') or os.environ.get(
            'SF_SECURITY_TOKEN', ''
        )
        self.login_url = kwargs.get('login_url') or os.environ.get(
            'SF_LOGIN_URL', 'https://login.salesforce.com'
        )

        self.access_token = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    # ==================== AUTHENTICATION ====================

    @allure.step("Authenticate with Salesforce")
    def authenticate(self, flow: str = "password") -> bool:
        """Authenticate with Salesforce using OAuth2.

        Args:
            flow: Auth flow type - 'password' or 'client_credentials'

        Returns:
            True if authentication successful
        """
        if flow == "password":
            return self._auth_password_flow()
        elif flow == "client_credentials":
            return self._auth_client_credentials()
        else:
            raise ValueError(f"Unsupported auth flow: {flow}")

    def _auth_password_flow(self) -> bool:
        """OAuth2 username-password flow."""
        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': f"{self.password}{self.security_token}"
        }
        resp = requests.post(
            f"{self.login_url}/services/oauth2/token",
            data=data, timeout=30
        )
        if resp.status_code == 200:
            token_data = resp.json()
            self.access_token = token_data['access_token']
            self.instance_url = token_data['instance_url']
            self.session.headers['Authorization'] = f"Bearer {self.access_token}"
            logger.info(f"Authenticated with Salesforce: {self.instance_url}")
            return True
        else:
            logger.error(f"SF auth failed: {resp.status_code} {resp.text[:300]}")
            return False

    def _auth_client_credentials(self) -> bool:
        """OAuth2 client credentials flow."""
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        resp = requests.post(
            f"{self.login_url}/services/oauth2/token",
            data=data, timeout=30
        )
        if resp.status_code == 200:
            token_data = resp.json()
            self.access_token = token_data['access_token']
            if 'instance_url' in token_data:
                self.instance_url = token_data['instance_url']
            self.session.headers['Authorization'] = f"Bearer {self.access_token}"
            logger.info("Authenticated with Salesforce (client credentials)")
            return True
        else:
            logger.error(f"SF auth failed: {resp.status_code} {resp.text[:300]}")
            return False

    def _api_url(self, path: str) -> str:
        """Build Salesforce API URL."""
        return f"{self.instance_url}/services/data/{self.API_VERSION}/{path}"

    # ==================== SOQL QUERIES ====================

    @allure.step("SOQL Query: {query}")
    def query(self, query: str) -> Dict[str, Any]:
        """Execute SOQL query.

        Args:
            query: SOQL query string

        Returns:
            Query result dict with 'records', 'totalSize', 'done'
        """
        resp = self.session.get(
            self._api_url("query"),
            params={'q': query}, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(f"SOQL returned {result.get('totalSize', 0)} records")
        return result

    def query_all(self, query: str) -> List[Dict]:
        """Execute SOQL query and return all records (handles pagination).

        Args:
            query: SOQL query string

        Returns:
            List of all record dicts
        """
        records = []
        result = self.query(query)
        records.extend(result.get('records', []))

        while not result.get('done', True):
            next_url = f"{self.instance_url}{result['nextRecordsUrl']}"
            resp = self.session.get(next_url, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            records.extend(result.get('records', []))

        return records

    # ==================== CRUD OPERATIONS ====================

    @allure.step("Create {sobject}")
    def create(self, sobject: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Salesforce object.

        Args:
            sobject: Object type (e.g., 'Account', 'Contact', 'LoyaltyProgram')
            data: Field values

        Returns:
            Response dict with 'id', 'success', 'errors'
        """
        resp = self.session.post(
            self._api_url(f"sobjects/{sobject}"),
            json=data, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(f"Created {sobject}: {result.get('id')}")
        return result

    @allure.step("Read {sobject}/{record_id}")
    def read(self, sobject: str, record_id: str,
             fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Read a Salesforce object by ID.

        Args:
            sobject: Object type
            record_id: Record ID
            fields: Optional list of fields to retrieve

        Returns:
            Record dict
        """
        url = self._api_url(f"sobjects/{sobject}/{record_id}")
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @allure.step("Update {sobject}/{record_id}")
    def update(self, sobject: str, record_id: str,
               data: Dict[str, Any]) -> bool:
        """Update a Salesforce object.

        Args:
            sobject: Object type
            record_id: Record ID
            data: Fields to update

        Returns:
            True if successful (204 No Content)
        """
        resp = self.session.patch(
            self._api_url(f"sobjects/{sobject}/{record_id}"),
            json=data, timeout=30
        )
        success = resp.status_code == 204
        if success:
            logger.info(f"Updated {sobject}/{record_id}")
        else:
            logger.error(f"Update failed: {resp.status_code} {resp.text[:300]}")
        return success

    @allure.step("Delete {sobject}/{record_id}")
    def delete(self, sobject: str, record_id: str) -> bool:
        """Delete a Salesforce object.

        Args:
            sobject: Object type
            record_id: Record ID

        Returns:
            True if successful (204 No Content)
        """
        resp = self.session.delete(
            self._api_url(f"sobjects/{sobject}/{record_id}"),
            timeout=30
        )
        success = resp.status_code == 204
        if success:
            logger.info(f"Deleted {sobject}/{record_id}")
        return success

    # ==================== COMPOSITE API ====================

    @allure.step("Composite request ({count} operations)")
    def composite(self, requests_list: List[Dict]) -> Dict:
        """Execute composite API request (multiple operations in one call).

        Args:
            requests_list: List of request dicts with method, url, referenceId, body

        Returns:
            Composite response dict
        """
        resp = self.session.post(
            self._api_url("composite"),
            json={"compositeRequest": requests_list},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()

    # ==================== LOYALTY MANAGEMENT ====================

    @allure.step("Get loyalty program members")
    def get_loyalty_members(self, program_name: Optional[str] = None,
                            limit: int = 100) -> List[Dict]:
        """Query Loyalty Program Members.

        Args:
            program_name: Filter by program name (optional)
            limit: Max records to return

        Returns:
            List of LoyaltyProgramMember records
        """
        query = f"SELECT Id, Name, MembershipNumber, MemberStatus, " \
                f"LoyaltyProgramId, TotalPointsBalance " \
                f"FROM LoyaltyProgramMember"
        if program_name:
            query += f" WHERE LoyaltyProgram.Name = '{program_name}'"
        query += f" LIMIT {limit}"
        return self.query_all(query)

    @allure.step("Enroll loyalty member")
    def enroll_loyalty_member(self, member_data: Dict[str, Any]) -> Dict:
        """Enroll a new loyalty program member.

        Args:
            member_data: Member fields (ContactId, LoyaltyProgramId, etc.)

        Returns:
            Created member record
        """
        return self.create("LoyaltyProgramMember", member_data)

    @allure.step("Get member transactions")
    def get_member_transactions(self, member_id: str,
                                limit: int = 50) -> List[Dict]:
        """Get transactions for a loyalty member.

        Args:
            member_id: LoyaltyProgramMember ID
            limit: Max records

        Returns:
            List of TransactionJournal records
        """
        query = f"SELECT Id, TransactionType, TransactionDate, " \
                f"PointsChange, ActivityDate, Status " \
                f"FROM TransactionJournal " \
                f"WHERE LoyaltyProgramMemberId = '{member_id}' " \
                f"ORDER BY TransactionDate DESC LIMIT {limit}"
        return self.query_all(query)

    @allure.step("Get member point balance")
    def get_member_points(self, member_id: str) -> Dict:
        """Get point balance for a loyalty member.

        Args:
            member_id: LoyaltyProgramMember ID

        Returns:
            Record with point balances
        """
        return self.read(
            "LoyaltyProgramMember", member_id,
            fields=["Id", "Name", "TotalPointsBalance",
                     "TotalPointsExpired", "TotalPointsRedeemed"]
        )

    @allure.step("Credit points to member")
    def credit_points(self, member_id: str, points: int,
                      reason: str = "Test credit") -> Dict:
        """Credit points to a loyalty member via transaction.

        Args:
            member_id: LoyaltyProgramMember ID
            points: Points to credit
            reason: Transaction reason

        Returns:
            Created TransactionJournal record
        """
        return self.create("TransactionJournal", {
            "LoyaltyProgramMemberId": member_id,
            "TransactionType": "Accrual",
            "PointsChange": points,
            "Status": "Processed",
            "JournalSubType": reason
        })

    # ==================== DESCRIBE ====================

    def describe(self, sobject: str) -> Dict:
        """Get metadata for a Salesforce object.

        Args:
            sobject: Object type

        Returns:
            Object describe result
        """
        resp = self.session.get(
            self._api_url(f"sobjects/{sobject}/describe"),
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def get_object_fields(self, sobject: str) -> List[str]:
        """Get list of field names for a Salesforce object.

        Args:
            sobject: Object type

        Returns:
            List of field API names
        """
        desc = self.describe(sobject)
        return [f['name'] for f in desc.get('fields', [])]

    # ==================== CLEANUP ====================

    def close(self):
        """Close the HTTP session."""
        self.session.close()
