import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from ..main import app
from ..database import get_db, Base
from ..models import Session, Interruption

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_session_data():
    return {
        "title": "Test Session",
        "goal": "Complete test implementation",
        "scheduled_duration": 30.0
    }

class TestSessionCreation:
    def test_create_session_success(self, client, sample_session_data):
        """Test successful session creation"""
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_session_data["title"]
        assert data["goal"] == sample_session_data["goal"]
        assert data["scheduled_duration"] == sample_session_data["scheduled_duration"]
        assert data["status"] == "planned"
        assert data["id"] is not None

    def test_create_session_invalid_data(self, client):
        """Test session creation with invalid data"""
        invalid_data = {
            "title": "",  # Empty title
            "goal": "Test goal",
            "scheduled_duration": 30.0
        }
        response = client.post("/api/v1/sessions/", json=invalid_data)
        assert response.status_code == 422

class TestSessionStateTransitions:
    def test_start_session_success(self, client, sample_session_data):
        """Test successful session start"""
        # Create session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        
        # Start session
        response = client.patch(f"/api/v1/sessions/{session_id}/start")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"
        assert data["start_time"] is not None

    def test_start_session_wrong_status(self, client, sample_session_data):
        """Test starting session in wrong status"""
        # Create and start session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        
        # Try to start again
        response = client.patch(f"/api/v1/sessions/{session_id}/start")
        assert response.status_code == 400

    def test_pause_session_success(self, client, sample_session_data):
        """Test successful session pause"""
        # Create and start session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        
        # Pause session
        pause_data = {"reason": "Phone call"}
        response = client.patch(f"/api/v1/sessions/{session_id}/pause", json=pause_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "paused"

    def test_pause_session_wrong_status(self, client, sample_session_data):
        """Test pausing session in wrong status"""
        # Create session (not started)
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        
        # Try to pause
        pause_data = {"reason": "Phone call"}
        response = client.patch(f"/api/v1/sessions/{session_id}/pause", json=pause_data)
        assert response.status_code == 400

    def test_resume_session_success(self, client, sample_session_data):
        """Test successful session resume"""
        # Create, start, and pause session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        client.patch(f"/api/v1/sessions/{session_id}/pause", json={"reason": "Phone call"})
        
        # Resume session
        response = client.patch(f"/api/v1/sessions/{session_id}/resume")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"

    def test_complete_session_success(self, client, sample_session_data):
        """Test successful session completion"""
        # Create and start session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        
        # Complete session
        response = client.patch(f"/api/v1/sessions/{session_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["end_time"] is not None

class TestInterruptionLogic:
    def test_multiple_interruptions(self, client, sample_session_data):
        """Test session becomes interrupted after 3+ pauses"""
        # Create and start session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        
        # Pause 4 times
        for i in range(4):
            client.patch(f"/api/v1/sessions/{session_id}/pause", json={"reason": f"Interruption {i+1}"})
            client.patch(f"/api/v1/sessions/{session_id}/resume")
        
        # Complete session
        response = client.patch(f"/api/v1/sessions/{session_id}/complete")
        data = response.json()
        assert data["status"] == "interrupted"

    def test_overdue_session(self, client):
        """Test session becomes overdue when duration exceeds 110%"""
        # Create session with very short duration
        session_data = {
            "title": "Quick Test",
            "goal": "Test overdue logic",
            "scheduled_duration": 0.1  # 0.1 minutes = 6 seconds
        }
        
        response = client.post("/api/v1/sessions/", json=session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        
        # Wait a bit to exceed 110% of scheduled duration
        import time
        time.sleep(1)  # Wait 1 second (much more than 6 seconds * 1.1)
        
        # Complete session
        response = client.patch(f"/api/v1/sessions/{session_id}/complete")
        data = response.json()
        assert data["status"] == "overdue"

    def test_abandoned_session(self, client, sample_session_data):
        """Test session becomes abandoned when paused but never resumed"""
        # Create, start, and pause session
        response = client.post("/api/v1/sessions/", json=sample_session_data)
        session_id = response.json()["id"]
        client.patch(f"/api/v1/sessions/{session_id}/start")
        client.patch(f"/api/v1/sessions/{session_id}/pause", json={"reason": "Got distracted"})
        
        # Complete without resuming
        response = client.patch(f"/api/v1/sessions/{session_id}/complete")
        data = response.json()
        assert data["status"] == "abandoned"

class TestSessionHistory:
    def test_get_session_history(self, client, sample_session_data):
        """Test getting session history with statistics"""
        # Create a few sessions
        for i in range(3):
            session_data = sample_session_data.copy()
            session_data["title"] = f"Test Session {i+1}"
            client.post("/api/v1/sessions/", json=session_data)
        
        # Get history
        response = client.get("/api/v1/sessions/history")
        assert response.status_code == 200
        data = response.json()
        assert data["total_sessions"] == 3
        assert len(data["sessions"]) == 3

    def test_session_not_found(self, client):
        """Test getting non-existent session"""
        response = client.get("/api/v1/sessions/999")
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])
