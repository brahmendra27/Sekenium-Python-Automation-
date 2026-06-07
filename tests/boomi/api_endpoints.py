# tests/boomi/api_endpoints.py

"""
Boomi Middleware API Endpoints and Request Builders.

All Boomi API knowledge lives here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================

BOOMI_ACCOUNT_ID = os.getenv("BOOMI_ACCOUNT_ID", "")
BOOMI_BASE_URL = f"https://api.boomi.com/api/rest/v1/{BOOMI_ACCOUNT_ID}"

# ==================== ENDPOINTS ====================

EXECUTE_PROCESS = "/executeProcess"
EXECUTION_RECORD = "/ExecutionRecord/{execution_id}"
QUERY_EXECUTIONS = "/ExecutionRecord/query"
QUERY_ATOMS = "/Atom/query"
ENVIRONMENT = "/Environment/{env_id}"


# ==================== BUILDERS ====================

def build_execute_process(process_id, atom_id, properties=None, **overrides):
    """Build process execution request."""
    payload = {
        "processId": process_id,
        "atomId": atom_id,
        "ProcessProperties": {"@type": "ProcessProperties"}
    }
    if properties:
        prop_list = [
            {"@type": "ProcessProperty", "Name": k, "Value": str(v)}
            for k, v in properties.items()
        ]
        payload["ProcessProperties"]["ProcessProperty"] = prop_list
    payload.update(overrides)
    return {
        "method": "POST",
        "base_url": BOOMI_BASE_URL,
        "endpoint": EXECUTE_PROCESS,
        "payload": payload,
    }


def build_get_execution(execution_id):
    """Build get execution record request."""
    return {
        "method": "GET",
        "base_url": BOOMI_BASE_URL,
        "endpoint": EXECUTION_RECORD.format(execution_id=execution_id),
    }


def build_query_executions(process_id=None, status=None, limit=100):
    """Build execution query request."""
    filters = {}
    if process_id:
        filters["processId"] = process_id
    if status:
        filters["status"] = status
    return {
        "method": "POST",
        "base_url": BOOMI_BASE_URL,
        "endpoint": QUERY_EXECUTIONS,
        "payload": filters,
        "params": {"limit": limit},
    }


def build_query_atoms(status="ONLINE"):
    """Build atom query request."""
    return {
        "method": "POST",
        "base_url": BOOMI_BASE_URL,
        "endpoint": QUERY_ATOMS,
        "payload": {
            "QueryFilter": {
                "expression": {
                    "operator": "EQUALS",
                    "property": "status",
                    "argument": [status]
                }
            }
        },
    }


def build_get_environment(env_id):
    """Build get environment request."""
    return {
        "method": "GET",
        "base_url": BOOMI_BASE_URL,
        "endpoint": ENVIRONMENT.format(env_id=env_id),
    }
