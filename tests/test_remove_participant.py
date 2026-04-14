"""
Tests for the DELETE /activities/{activity_name}/participant endpoint.
"""

import pytest


class TestRemoveParticipant:
    """Tests for removing a participant from an activity."""

    def test_remove_participant_succeeds(self, client, sample_activities):
        """
        Arrange: Participant is registered for an activity
        Act: Remove participant from activity
        Assert: Removal succeeds with 200 status and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
        assert email not in sample_activities[activity_name]["participants"]
        assert len(sample_activities[activity_name]["participants"]) == initial_count - 1

    def test_remove_nonexistent_participant_fails(self, client, sample_activities):
        """
        Arrange: Participant does not exist for the activity
        Act: Attempt to remove non-existent participant
        Assert: Removal fails with 404 status
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not in participants
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
        assert len(sample_activities[activity_name]["participants"]) == initial_count

    def test_remove_from_nonexistent_activity_fails(self, client, sample_activities):
        """
        Arrange: Activity does not exist in the database
        Act: Attempt to remove participant from non-existent activity
        Assert: Removal fails with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_multiple_participants(self, client, sample_activities):
        """
        Arrange: Activity has multiple participants
        Act: Remove each participant one by one
        Assert: All removals succeed and final participants list is empty
        """
        # Arrange
        activity_name = "Chess Club"
        participants = sample_activities[activity_name]["participants"].copy()
        initial_count = len(participants)

        # Act & Assert
        for email in participants:
            response = client.delete(
                f"/activities/{activity_name}/participant",
                params={"email": email}
            )
            assert response.status_code == 200
            assert email not in sample_activities[activity_name]["participants"]

        # Verify final count
        assert len(sample_activities[activity_name]["participants"]) == 0

    def test_remove_then_readd_participant(self, client, sample_activities):
        """
        Arrange: Participant is registered for activity
        Act: Remove participant, then sign them up again
        Assert: Both operations succeed correctly
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        # Act - Remove
        remove_response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"email": email}
        )

        # Assert removal succeeded
        assert remove_response.status_code == 200
        assert email not in sample_activities[activity_name]["participants"]

        # Act - Re-add
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert re-add succeeded
        assert signup_response.status_code == 200
        assert email in sample_activities[activity_name]["participants"]
