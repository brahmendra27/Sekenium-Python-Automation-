# tests/salesforce_crm/test_account_management.py

"""
Salesforce CRM Account Management Tests.

Tests CRUD operations on Account objects.
Requires SF_* environment variables in .env file.
"""

import pytest


class TestAccountCRUD:
    """Test Salesforce Account create, read, update, delete."""

    @pytest.mark.salesforce_crm
    @pytest.mark.smoke
    def test_create_and_read_account(self, sf_client, sf_cleanup, unique_id):
        """Test creating and reading a Salesforce Account."""
        account_name = f"Test Account {unique_id}"

        # Create
        result = sf_client.create("Account", {"Name": account_name})
        assert result["success"] is True, f"Failed to create account: {result}"
        account_id = result["id"]
        sf_cleanup("Account", account_id)

        # Read
        account = sf_client.read("Account", account_id, fields=["Id", "Name"])
        assert account["Name"] == account_name

    @pytest.mark.salesforce_crm
    def test_update_account(self, sf_client, sf_cleanup, unique_id):
        """Test updating a Salesforce Account."""
        # Create
        result = sf_client.create("Account", {"Name": f"Update Test {unique_id}"})
        account_id = result["id"]
        sf_cleanup("Account", account_id)

        # Update
        new_name = f"Updated Account {unique_id}"
        success = sf_client.update("Account", account_id, {"Name": new_name})
        assert success is True

        # Verify
        account = sf_client.read("Account", account_id, fields=["Name"])
        assert account["Name"] == new_name

    @pytest.mark.salesforce_crm
    def test_delete_account(self, sf_client, unique_id):
        """Test deleting a Salesforce Account."""
        # Create
        result = sf_client.create("Account", {"Name": f"Delete Test {unique_id}"})
        account_id = result["id"]

        # Delete
        success = sf_client.delete("Account", account_id)
        assert success is True


class TestAccountQueries:
    """Test SOQL queries on Account objects."""

    @pytest.mark.salesforce_crm
    @pytest.mark.smoke
    def test_query_accounts(self, sf_client):
        """Test querying accounts via SOQL."""
        result = sf_client.query("SELECT Id, Name FROM Account LIMIT 5")
        assert result["totalSize"] >= 0
        assert "records" in result

    @pytest.mark.salesforce_crm
    def test_query_accounts_with_filter(self, sf_client, sf_cleanup, unique_id):
        """Test querying accounts with a WHERE filter."""
        account_name = f"Query Test {unique_id}"

        # Create test account
        result = sf_client.create("Account", {"Name": account_name})
        sf_cleanup("Account", result["id"])

        # Query with filter
        query_result = sf_client.query(
            f"SELECT Id, Name FROM Account WHERE Name = '{account_name}'"
        )
        assert query_result["totalSize"] == 1
        assert query_result["records"][0]["Name"] == account_name
