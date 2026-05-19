"""
Example usage and test scenarios for the Conversation Memory Module.
This file demonstrates how to use the API with various scenarios.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


class ConversationMemoryClient:
    """
    Client for interacting with the Conversation Memory API.
    """

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def health_check(self):
        """Check if the service is running."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def create_memory(self, session_id: str, question: str, answer: str, tags: str = None):
        """Create a new memory."""
        payload = {
            "session_id": session_id,
            "question": question,
            "answer": answer,
        }
        if tags:
            payload["tags"] = tags

        response = requests.post(f"{self.base_url}/memory", json=payload)
        return response

    def get_memory(self, memory_id: int):
        """Get a specific memory by ID."""
        response = requests.get(f"{self.base_url}/memory/{memory_id}")
        return response

    def get_all_memories(self, session_id: str = None, skip: int = 0, limit: int = 100):
        """Get all memories with optional filtering."""
        params = {"skip": skip, "limit": limit}
        if session_id:
            params["session_id"] = session_id

        response = requests.get(f"{self.base_url}/memory", params=params)
        return response

    def get_session_memories(self, session_id: str, skip: int = 0, limit: int = 100):
        """Get all memories for a specific session."""
        params = {"skip": skip, "limit": limit}
        response = requests.get(
            f"{self.base_url}/memory/session/{session_id}",
            params=params
        )
        return response

    def search_by_tags(self, tags: str, skip: int = 0, limit: int = 100):
        """Search memories by tags."""
        params = {"tags": tags, "skip": skip, "limit": limit}
        response = requests.get(f"{self.base_url}/memory/search/tags", params=params)
        return response

    def update_memory(self, memory_id: int, **kwargs):
        """Update a memory record."""
        response = requests.put(f"{self.base_url}/memory/{memory_id}", json=kwargs)
        return response

    def delete_memory(self, memory_id: int):
        """Delete a specific memory."""
        response = requests.delete(f"{self.base_url}/memory/{memory_id}")
        return response

    def delete_session(self, session_id: str):
        """Delete all memories for a session."""
        response = requests.delete(f"{self.base_url}/memory/session/{session_id}")
        return response


def example_interview_session():
    """
    Example: Store and retrieve an interview session's Q&A.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Interview Session Management")
    print("="*60)

    client = ConversationMemoryClient()
    session_id = "interview-candidate-001"

    # Interview questions and answers
    interview_data = [
        {
            "question": "Tell us about yourself",
            "answer": "I have 5 years of software development experience",
            "tags": "introduction,background"
        },
        {
            "question": "What are your technical skills?",
            "answer": "Python, JavaScript, SQL, and AWS",
            "tags": "technical,skills"
        },
        {
            "question": "Describe your recent project",
            "answer": "Built a microservices architecture using FastAPI",
            "tags": "projects,experience"
        }
    ]

    print("\n1. Creating interview memories...")
    created_memories = []
    for data in interview_data:
        response = client.create_memory(
            session_id=session_id,
            **data
        )
        if response.status_code == 201:
            memory = response.json()
            created_memories.append(memory)
            print(f"   ✓ Created memory ID {memory['id']}: {data['question'][:40]}...")
        else:
            print(f"   ✗ Failed to create memory: {response.text}")

    print("\n2. Retrieving all session memories...")
    response = client.get_session_memories(session_id)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Retrieved {data['total']} memories from session")
        for item in data['items']:
            print(f"     - {item['question'][:40]}... → {item['answer'][:40]}...")

    print("\n3. Searching by tags...")
    response = client.search_by_tags("technical")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Found {data['total']} memory with 'technical' tag")

    print("\n4. Updating a memory...")
    if created_memories:
        memory_id = created_memories[0]['id']
        response = client.update_memory(
            memory_id,
            answer="I have 6 years of software development experience"
        )
        if response.status_code == 200:
            print(f"   ✓ Updated memory ID {memory_id}")

    return session_id, created_memories


def example_multiple_sessions():
    """
    Example: Handle multiple concurrent interview sessions.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Multiple Interview Sessions")
    print("="*60)

    client = ConversationMemoryClient()
    sessions = ["interview-001", "interview-002", "interview-003"]

    print("\n1. Creating memories across multiple sessions...")
    for i, session_id in enumerate(sessions):
        response = client.create_memory(
            session_id=session_id,
            question=f"Question for session {i+1}",
            answer=f"Answer for session {i+1}",
            tags=f"session-{i+1}"
        )
        if response.status_code == 201:
            print(f"   ✓ Created memory for {session_id}")

    print("\n2. Retrieving all memories...")
    response = client.get_all_memories()
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Total memories across all sessions: {data['total']}")

    print("\n3. Getting memories per session...")
    for session_id in sessions:
        response = client.get_session_memories(session_id)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ {session_id}: {data['total']} memories")


def example_pagination():
    """
    Example: Handle large datasets with pagination.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Pagination")
    print("="*60)

    client = ConversationMemoryClient()
    session_id = "pagination-test"

    # Create 25 memories
    print("\n1. Creating 25 test memories...")
    for i in range(25):
        client.create_memory(
            session_id=session_id,
            question=f"Question {i+1}",
            answer=f"Answer {i+1}",
            tags="test"
        )
    print(f"   ✓ Created 25 memories")

    print("\n2. Retrieving with pagination (10 per page)...")
    for page in range(3):
        response = client.get_session_memories(
            session_id=session_id,
            skip=page * 10,
            limit=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Page {page+1}: {len(data['items'])} items (Total: {data['total']})")


def example_tag_based_filtering():
    """
    Example: Use tags for memory categorization and filtering.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Tag-Based Filtering")
    print("="*60)

    client = ConversationMemoryClient()
    session_id = "tag-test"

    # Create memories with different tags
    memories = [
        {
            "question": "Experience?",
            "answer": "10 years in tech",
            "tags": "experience,professional"
        },
        {
            "question": "Skills?",
            "answer": "Python, Java, SQL",
            "tags": "skills,technical"
        },
        {
            "question": "Availability?",
            "answer": "Immediate",
            "tags": "availability,employment"
        }
    ]

    print("\n1. Creating tagged memories...")
    for data in memories:
        response = client.create_memory(session_id=session_id, **data)
        if response.status_code == 201:
            print(f"   ✓ Created: {data['tags']}")

    print("\n2. Searching by individual tags...")
    for tag in ["experience", "technical", "employment"]:
        response = client.search_by_tags(tag)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Tag '{tag}': Found {data['total']} memories")


def example_cleanup():
    """
    Example: Clean up memories.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Cleanup Operations")
    print("="*60)

    client = ConversationMemoryClient()
    session_id = "cleanup-test"

    # Create some memories
    print("\n1. Creating memories for cleanup test...")
    response_ids = []
    for i in range(5):
        response = client.create_memory(
            session_id=session_id,
            question=f"Q{i}",
            answer=f"A{i}"
        )
        if response.status_code == 201:
            response_ids.append(response.json()['id'])
    print(f"   ✓ Created 5 memories")

    print("\n2. Deleting individual memory...")
    if response_ids:
        response = client.delete_memory(response_ids[0])
        if response.status_code == 204:
            print(f"   ✓ Deleted memory ID {response_ids[0]}")

    print("\n3. Deleting entire session...")
    response = client.delete_session(session_id)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ {data['message']}")


def run_all_examples():
    """
    Run all examples in sequence.
    """
    print("\n" + "="*60)
    print("CONVERSATION MEMORY MODULE - EXAMPLES")
    print("="*60)

    client = ConversationMemoryClient()

    # Check service health
    print("\nChecking service health...")
    try:
        health = client.health_check()
        print(f"✓ Service Status: {health['status']}")
    except Exception as e:
        print(f"✗ Cannot connect to service: {e}")
        print(f"  Make sure the service is running at {BASE_URL}")
        return

    # Run examples
    try:
        example_interview_session()
        example_multiple_sessions()
        example_pagination()
        example_tag_based_filtering()
        example_cleanup()

        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nVisit http://localhost:8000/docs for interactive API documentation")

    except Exception as e:
        print(f"\n✗ Error running examples: {e}")


if __name__ == "__main__":
    run_all_examples()
