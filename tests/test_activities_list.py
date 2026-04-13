"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving the list of available activities."""

    def test_get_activities_returns_all_activities(self, client, sample_activities):
        """
        Arrange: Test data with 3 activities is available
        Act: Make GET request to /activities
        Assert: Response contains all activities with correct data
        """
        # Arrange
        expected_activity_count = len(sample_activities)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client, sample_activities):
        """
        Arrange: Test data is loaded
        Act: Make GET request to /activities
        Assert: Each activity has all required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_have_emails(self, client, sample_activities):
        """
        Arrange: Test data with participants
        Act: Make GET request to /activities
        Assert: All participants are valid email strings
        """
        # Arrange
        # (data from sample_activities fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
