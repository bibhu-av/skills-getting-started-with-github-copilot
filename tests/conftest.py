"""
Pytest configuration and shared fixtures for testing the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making HTTP requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities(monkeypatch):
    """
    Fixture that provides a fresh copy of activities data for each test.
    Uses monkeypatch to isolate test data from other tests.
    
    Arrange: Set up test data that's isolated from other tests
    """
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Monkeypatch the module-level activities dict
    monkeypatch.setattr("src.app.activities", test_activities)
    
    return test_activities
