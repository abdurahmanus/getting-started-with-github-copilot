import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Fixture that provides fresh activity data for each test.
    Uses monkeypatch to replace the app's activities dict with a clean copy.
    """
    original_activities = {
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
        },
        "Basketball Team": {
            "description": "Compete in competitive basketball matches and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Create and perform theatrical productions and skits",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["sarah@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation skills and compete in debate competitions",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu"]
        }
    }
    
    # Replace the app's activities with a fresh copy for this test
    monkeypatch.setitem(activities, "Chess Club", copy.deepcopy(original_activities["Chess Club"]))
    monkeypatch.setitem(activities, "Programming Class", copy.deepcopy(original_activities["Programming Class"]))
    monkeypatch.setitem(activities, "Gym Class", copy.deepcopy(original_activities["Gym Class"]))
    monkeypatch.setitem(activities, "Basketball Team", copy.deepcopy(original_activities["Basketball Team"]))
    monkeypatch.setitem(activities, "Tennis Club", copy.deepcopy(original_activities["Tennis Club"]))
    monkeypatch.setitem(activities, "Drama Club", copy.deepcopy(original_activities["Drama Club"]))
    monkeypatch.setitem(activities, "Art Studio", copy.deepcopy(original_activities["Art Studio"]))
    monkeypatch.setitem(activities, "Science Club", copy.deepcopy(original_activities["Science Club"]))
    monkeypatch.setitem(activities, "Debate Team", copy.deepcopy(original_activities["Debate Team"]))
    
    return activities
