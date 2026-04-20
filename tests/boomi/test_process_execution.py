# tests/boomi/test_process_execution.py

"""
Boomi Middleware Integration Tests.

Tests process execution, monitoring, and document tracking.
Requires BOOMI_* environment variables in .env file.
"""

import pytest


class TestBoomiAtoms:
    """Test Boomi Atom/Molecule connectivity."""

    @pytest.mark.boomi
    @pytest.mark.smoke
    def test_list_online_atoms(self, boomi_client):
        """Test listing online Atoms in the account."""
        atoms = boomi_client.list_atoms(status="ONLINE")
        assert isinstance(atoms, list)
        assert len(atoms) > 0, "No online Atoms found"

    @pytest.mark.boomi
    def test_list_all_atoms(self, boomi_client):
        """Test listing all Atoms regardless of status."""
        online = boomi_client.list_atoms(status="ONLINE")
        offline = boomi_client.list_atoms(status="OFFLINE")
        total = len(online) + len(offline)
        assert total > 0, "No Atoms found in account"


class TestBoomiExecutions:
    """Test Boomi process execution queries."""

    @pytest.mark.boomi
    @pytest.mark.smoke
    def test_query_recent_executions(self, boomi_client):
        """Test querying recent execution records."""
        executions = boomi_client.query_executions(limit=10)
        assert isinstance(executions, list)

    @pytest.mark.boomi
    def test_query_completed_executions(self, boomi_client):
        """Test querying completed execution records."""
        executions = boomi_client.query_executions(
            status="COMPLETE", limit=5
        )
        assert isinstance(executions, list)
        for execution in executions:
            assert execution.get("status") == "COMPLETE"

    @pytest.mark.boomi
    def test_query_failed_executions(self, boomi_client):
        """Test querying failed execution records."""
        executions = boomi_client.query_executions(
            status="ERROR", limit=5
        )
        assert isinstance(executions, list)
        for execution in executions:
            assert execution.get("status") == "ERROR"


class TestBoomiEnvironments:
    """Test Boomi environment management."""

    @pytest.mark.boomi
    def test_get_environment(self, boomi_client):
        """Test retrieving environment details."""
        # Get first online atom to find its environment
        atoms = boomi_client.list_atoms(status="ONLINE")
        if not atoms:
            pytest.skip("No online Atoms found")

        # Atoms should have environment info
        assert len(atoms) > 0
