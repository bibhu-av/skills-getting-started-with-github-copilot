"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up a student for an activity."""

    def test_signup_new_student_succeeds(self, client, sample_activities):
        """
        Arrange: Activity exists with initial participants
        Act: New student signs up for activity
        Assert: Signup succeeds with 200 status and student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in sample_activities[activity_name]["participants"]
        assert len(sample_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_student_fails(self, client, sample_activities):
        """
        Arrange: Student is already signed up for activity
        Act: Same student attempts to sign up again
        Assert: Signup fails with 400 status and duplicate signup error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"
        assert len(sample_activities[activity_name]["participants"]) == initial_count

    def test_signup_to_nonexistent_activity_fails(self, client, sample_activities):
        """
        Arrange: Activity does not exist in the database
        Act: Student attempts to sign up for non-existent activity
        Assert: Signup fails with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_multiple_different_students(self, client, sample_activities):
        """
        Arrange: Activity exists with space for multiple students
        Act: Multiple different students sign up for same activity
        Assert: All signups succeed and all emails are in participants
        """
        # Arrange
        activity_name = "Programming Class"
        emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
            assert email in sample_activities[activity_name]["participants"]

        # Verify final count
        assert len(sample_activities[activity_name]["participants"]) == initial_count + len(emails)
