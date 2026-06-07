# framework/graphql_client.py

"""
GraphQL Client for Salesforce GraphQL API and other GraphQL endpoints.

Supports:
  - Query and mutation execution
  - Variable substitution
  - Fragment support
  - Introspection queries
  - Error extraction and assertion
  - Allure step integration

Usage:
    client = GraphQLClient("https://your-org.my.salesforce.com/services/data/v59.0/graphql")
    client.set_bearer_token(token)
    result = client.query('''
        query { Account(first: 10) { edges { node { Name } } } }
    ''')
    client.assert_no_errors(result)
"""

import json
import logging
from typing import Dict, Any, Optional, List
import requests
import allure

logger = logging.getLogger(__name__)


class GraphQLClient:
    """GraphQL API client with query, mutation, and introspection support."""

    def __init__(self, endpoint: str, headers: Optional[Dict] = None,
                 timeout: int = 30):
        """Initialize GraphQL client.

        Args:
            endpoint: GraphQL endpoint URL
            headers: Default headers
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if headers:
            self.session.headers.update(headers)

    def set_bearer_token(self, token: str):
        """Set Bearer authentication token."""
        self.session.headers["Authorization"] = f"Bearer {token}"

    @allure.step("GraphQL Query")
    def query(self, query: str, variables: Optional[Dict] = None,
              operation_name: Optional[str] = None) -> Dict:
        """Execute a GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables dict
            operation_name: Operation name (for multi-operation documents)

        Returns:
            Response dict with 'data' and optionally 'errors'
        """
        return self._execute(query, variables, operation_name)

    @allure.step("GraphQL Mutation")
    def mutate(self, mutation: str, variables: Optional[Dict] = None,
               operation_name: Optional[str] = None) -> Dict:
        """Execute a GraphQL mutation.

        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables dict
            operation_name: Operation name

        Returns:
            Response dict with 'data' and optionally 'errors'
        """
        return self._execute(mutation, variables, operation_name)

    def _execute(self, query: str, variables: Optional[Dict] = None,
                 operation_name: Optional[str] = None) -> Dict:
        """Execute a GraphQL operation.

        Args:
            query: GraphQL query/mutation string
            variables: Variables dict
            operation_name: Operation name

        Returns:
            Parsed JSON response
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        logger.info(f"GraphQL request to {self.endpoint}")
        logger.debug(f"Query: {query[:200]}")

        resp = self.session.post(
            self.endpoint, json=payload, timeout=self.timeout
        )
        resp.raise_for_status()
        result = resp.json()

        # Log errors if present
        if "errors" in result:
            for err in result["errors"]:
                logger.warning(f"GraphQL error: {err.get('message')}")

        # Attach to Allure
        allure.attach(
            json.dumps(payload, indent=2),
            name="graphql_request",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(result, indent=2),
            name="graphql_response",
            attachment_type=allure.attachment_type.JSON
        )

        return result

    @allure.step("GraphQL Introspection")
    def introspect(self) -> Dict:
        """Run introspection query to discover schema.

        Returns:
            Schema introspection result
        """
        introspection_query = """
        query IntrospectionQuery {
            __schema {
                types { name kind description }
                queryType { name }
                mutationType { name }
            }
        }
        """
        return self.query(introspection_query)

    # ==================== ASSERTIONS ====================

    @staticmethod
    def assert_no_errors(result: Dict):
        """Assert GraphQL response has no errors.

        Args:
            result: GraphQL response dict

        Raises:
            AssertionError with error details
        """
        errors = result.get("errors", [])
        if errors:
            messages = [e.get("message", str(e)) for e in errors]
            raise AssertionError(
                f"GraphQL errors: {'; '.join(messages)}"
            )

    @staticmethod
    def get_data(result: Dict, path: str = "") -> Any:
        """Extract data from GraphQL response using dot-notation path.

        Args:
            result: GraphQL response dict
            path: Dot-notation path (e.g., "account.edges[0].node.Name")

        Returns:
            Extracted value
        """
        data = result.get("data", {})
        if not path:
            return data

        for key in path.replace("[", ".").replace("]", "").split("."):
            if key == "":
                continue
            if isinstance(data, list):
                data = data[int(key)]
            elif isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

    @staticmethod
    def get_errors(result: Dict) -> List[str]:
        """Extract error messages from GraphQL response.

        Returns:
            List of error message strings
        """
        return [
            e.get("message", str(e))
            for e in result.get("errors", [])
        ]

    def close(self):
        """Close the HTTP session."""
        self.session.close()
