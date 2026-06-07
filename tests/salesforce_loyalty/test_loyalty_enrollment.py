# tests/salesforce_loyalty/test_loyalty_enrollment.py

"""
Salesforce Loyalty Management Tests.

Tests member enrollment, points, and transactions.
Requires SF_* environment variables in .env file.
"""

import pytest


class TestLoyaltyMemberQueries:
    """Test querying loyalty program members."""

    @pytest.mark.loyalty
    @pytest.mark.smoke
    def test_query_loyalty_members(self, sf_client):
        """Test querying loyalty program members."""
        members = sf_client.get_loyalty_members(limit=10)
        assert isinstance(members, list)

    @pytest.mark.loyalty
    def test_query_members_by_program(self, sf_client):
        """Test querying members filtered by program name."""
        members = sf_client.get_loyalty_members(
            program_name="Skechers Plus", limit=5
        )
        assert isinstance(members, list)


class TestLoyaltyPoints:
    """Test loyalty point operations."""

    @pytest.mark.loyalty
    def test_get_member_point_balance(self, sf_client):
        """Test retrieving member point balance."""
        # Query for an existing member
        members = sf_client.get_loyalty_members(limit=1)
        if not members:
            pytest.skip("No loyalty members found in org")

        member_id = members[0]["Id"]
        points = sf_client.get_member_points(member_id)
        assert "TotalPointsBalance" in points

    @pytest.mark.loyalty
    def test_get_member_transactions(self, sf_client):
        """Test retrieving member transaction history."""
        members = sf_client.get_loyalty_members(limit=1)
        if not members:
            pytest.skip("No loyalty members found in org")

        member_id = members[0]["Id"]
        transactions = sf_client.get_member_transactions(member_id, limit=10)
        assert isinstance(transactions, list)
