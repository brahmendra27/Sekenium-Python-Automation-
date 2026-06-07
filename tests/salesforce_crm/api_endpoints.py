# tests/salesforce_crm/api_endpoints.py

"""
Salesforce CRM API Endpoints and Request Builders.

All Salesforce API knowledge lives here.
Uses SalesforceClient for auth, but builders define the operations.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================

SF_INSTANCE_URL = os.getenv("SF_INSTANCE_URL", "")
SF_API_VERSION = "v59.0"

# ==================== ENDPOINTS ====================

QUERY = "/services/data/{version}/query"
SOBJECT = "/services/data/{version}/sobjects/{sobject}"
SOBJECT_BY_ID = "/services/data/{version}/sobjects/{sobject}/{record_id}"
COMPOSITE = "/services/data/{version}/composite"


# ==================== BUILDERS ====================

def build_query_accounts(limit=10, name_filter=None, **overrides):
    """Build SOQL query for Accounts."""
    query = "SELECT Id, Name, Phone, Website FROM Account"
    if name_filter:
        query += f" WHERE Name LIKE '%{name_filter}%'"
    query += f" LIMIT {limit}"
    return {
        "operation": "query",
        "soql": query,
    }


def build_create_account(name="Test Account", phone="", website="",
                         **overrides):
    """Build Account creation payload."""
    payload = {"Name": name}
    if phone:
        payload["Phone"] = phone
    if website:
        payload["Website"] = website
    payload.update(overrides)
    return {
        "operation": "create",
        "sobject": "Account",
        "payload": payload,
    }


def build_create_contact(first_name="Test", last_name="User",
                         email="", account_id=None, **overrides):
    """Build Contact creation payload."""
    payload = {"FirstName": first_name, "LastName": last_name}
    if email:
        payload["Email"] = email
    if account_id:
        payload["AccountId"] = account_id
    payload.update(overrides)
    return {
        "operation": "create",
        "sobject": "Contact",
        "payload": payload,
    }


def build_create_opportunity(name="Test Opportunity", stage="Prospecting",
                             close_date="2026-12-31", amount=0,
                             account_id=None, **overrides):
    """Build Opportunity creation payload."""
    payload = {
        "Name": name,
        "StageName": stage,
        "CloseDate": close_date,
    }
    if amount:
        payload["Amount"] = amount
    if account_id:
        payload["AccountId"] = account_id
    payload.update(overrides)
    return {
        "operation": "create",
        "sobject": "Opportunity",
        "payload": payload,
    }


def build_update_account(record_id, **fields):
    """Build Account update payload."""
    return {
        "operation": "update",
        "sobject": "Account",
        "record_id": record_id,
        "payload": fields,
    }


def build_delete_record(sobject, record_id):
    """Build record deletion request."""
    return {
        "operation": "delete",
        "sobject": sobject,
        "record_id": record_id,
    }


def build_query_contacts_by_account(account_id, limit=20):
    """Build SOQL query for Contacts by Account."""
    return {
        "operation": "query",
        "soql": (
            f"SELECT Id, FirstName, LastName, Email "
            f"FROM Contact "
            f"WHERE AccountId = '{account_id}' "
            f"LIMIT {limit}"
        ),
    }
