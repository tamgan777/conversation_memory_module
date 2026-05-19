"""
Unit tests for the Conversation Memory Module.
Run with: pytest test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import ConversationMemory


# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestCreateMemory:
    """Test memory creation."""

    def test_create_memory_success(self):
        """Test successful memory creation."""
        payload = {
            "session_id": "test-session-001",
            "question": "What is your name?",
            "answer": "My name is John",
            "tags": "introduction"
        }
        response = client.post("/memory", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["session_id"] == "test-session-001"
        assert data["question"] == "What is your name?"
        assert data["answer"] == "My name is John"
        assert "id" in data
        assert "timestamp" in data

    def test_create_memory_without_tags(self):
        """Test memory creation without tags."""
        payload = {
            "session_id": "test-session-002",
            "question": "What is your experience?",
            "answer": "5 years"
        }
        response = client.post("/memory", json=payload)
        assert response.status_code == 201
        assert response.json()["tags"] is None

    def test_create_memory_invalid_session_id(self):
        """Test memory creation with empty session_id."""
        payload = {
            "session_id": "",
            "question": "What is your name?",
            "answer": "My name is John"
        }
        response = client.post("/memory", json=payload)
        assert response.status_code == 422  # Validation error

    def test_create_memory_missing_question(self):
        """Test memory creation without question."""
        payload = {
            "session_id": "test-session-003",
            "answer": "My answer"
        }
        response = client.post("/memory", json=payload)
        assert response.status_code == 422  # Validation error


class TestGetMemory:
    """Test retrieving memories."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data."""
        payload = {
            "session_id": "test-session",
            "question": "Test question",
            "answer": "Test answer",
            "tags": "test"
        }
        response = client.post("/memory", json=payload)
        self.memory_id = response.json()["id"]

    def test_get_memory_by_id(self):
        """Test retrieving a specific memory."""
        response = client.get(f"/memory/{self.memory_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.memory_id
        assert data["question"] == "Test question"

    def test_get_nonexistent_memory(self):
        """Test retrieving non-existent memory."""
        response = client.get("/memory/9999")
        assert response.status_code == 404

    def test_get_all_memories(self):
        """Test retrieving all memories."""
        response = client.get("/memory")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_get_memories_with_pagination(self):
        """Test pagination."""
        response = client.get("/memory?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        assert data["limit"] == 10


class TestSessionMemories:
    """Test session-based operations."""

    def test_get_session_memories(self):
        """Test retrieving memories for a session."""
        session_id = "session-test-001"
        
        # Create multiple memories in same session
        for i in range(3):
            payload = {
                "session_id": session_id,
                "question": f"Question {i}",
                "answer": f"Answer {i}"
            }
            client.post("/memory", json=payload)

        response = client.get(f"/memory/session/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3


class TestUpdateMemory:
    """Test memory update operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data."""
        payload = {
            "session_id": "update-test",
            "question": "Original question",
            "answer": "Original answer"
        }
        response = client.post("/memory", json=payload)
        self.memory_id = response.json()["id"]

    def test_update_memory_success(self):
        """Test successful update."""
        update_payload = {
            "answer": "Updated answer"
        }
        response = client.put(f"/memory/{self.memory_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Updated answer"
        assert data["question"] == "Original question"

    def test_update_nonexistent_memory(self):
        """Test updating non-existent memory."""
        update_payload = {"answer": "New answer"}
        response = client.put("/memory/9999", json=update_payload)
        assert response.status_code == 404


class TestDeleteMemory:
    """Test memory deletion operations."""

    def test_delete_memory_success(self):
        """Test successful deletion."""
        # Create a memory
        payload = {
            "session_id": "delete-test",
            "question": "To be deleted",
            "answer": "This will be deleted"
        }
        create_response = client.post("/memory", json=payload)
        memory_id = create_response.json()["id"]

        # Delete it
        delete_response = client.delete(f"/memory/{memory_id}")
        assert delete_response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/memory/{memory_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_memory(self):
        """Test deleting non-existent memory."""
        response = client.delete("/memory/9999")
        assert response.status_code == 404


class TestSearchByTags:
    """Test tag-based search."""

    def test_search_by_tags(self):
        """Test searching by tags."""
        # Create memories with tags
        payload1 = {
            "session_id": "search-test",
            "question": "Q1",
            "answer": "A1",
            "tags": "python,backend"
        }
        payload2 = {
            "session_id": "search-test",
            "question": "Q2",
            "answer": "A2",
            "tags": "javascript,frontend"
        }
        client.post("/memory", json=payload1)
        client.post("/memory", json=payload2)

        # Search for python tag
        response = client.get("/memory/search/tags?tags=python")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
