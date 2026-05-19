# Conversation Memory Module

A robust FastAPI-based service for storing and retrieving conversation context for interview sessions. This module maintains conversation continuity across sessions by storing questions, answers, and related metadata.

## Features

- ✅ Store and retrieve conversation history
- ✅ Session-based memory management
- ✅ Tag-based memory filtering and search
- ✅ SQLite database for persistent storage
- ✅ SQLAlchemy ORM for database operations
- ✅ Comprehensive REST API endpoints
- ✅ Input validation and error handling
- ✅ Interactive API documentation (Swagger UI)
- ✅ CORS support for cross-origin requests

## Project Structure

```
conversation-memory-module/
├── main.py                 # FastAPI application entry point
├── database.py            # Database configuration and session management
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic validation schemas
├── crud.py                # CRUD operations for database
├── routes.py              # REST API endpoints
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. Clone or download the project:
```bash
cd conversation-memory-module
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running
- `GET /` - API information

### Memory Management

#### Create Memory
```
POST /memory
Content-Type: application/json

{
  "session_id": "session-123",
  "question": "What is your experience?",
  "answer": "I have 5 years of experience",
  "tags": "experience,background"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "session_id": "session-123",
  "question": "What is your experience?",
  "answer": "I have 5 years of experience",
  "tags": "experience,background",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Get All Memories
```
GET /memory?skip=0&limit=100&session_id=session-123
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "session_id": "session-123",
      "question": "What is your experience?",
      "answer": "I have 5 years of experience",
      "tags": "experience,background",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Get Memory by ID
```
GET /memory/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "session_id": "session-123",
  "question": "What is your experience?",
  "answer": "I have 5 years of experience",
  "tags": "experience,background",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Get Session Memories
```
GET /memory/session/session-123?skip=0&limit=100
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "session_id": "session-123",
      "question": "What is your experience?",
      "answer": "I have 5 years of experience",
      "tags": "experience,background",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Search by Tags
```
GET /memory/search/tags?tags=experience,background&skip=0&limit=100
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "session_id": "session-123",
      "question": "What is your experience?",
      "answer": "I have 5 years of experience",
      "tags": "experience,background",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Update Memory
```
PUT /memory/1
Content-Type: application/json

{
  "answer": "Updated answer"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "session_id": "session-123",
  "question": "What is your experience?",
  "answer": "Updated answer",
  "tags": "experience,background",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Delete Memory
```
DELETE /memory/1
```

**Response (204 No Content)**

#### Delete Session
```
DELETE /memory/session/session-123
```

**Response (200 OK):**
```json
{
  "message": "Deleted 5 memories for session session-123",
  "deleted_count": 5
}
```

## Data Model

### ConversationMemory

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | ✅ | Unique identifier (auto-generated) |
| session_id | String(255) | ✅ | Session identifier for grouping conversations |
| question | Text | ✅ | The question asked |
| answer | Text | ✅ | The answer or response provided |
| timestamp | DateTime | ✅ | When the memory was created (auto-generated) |
| tags | String(500) | ❌ | Optional comma-separated tags for categorization |

## Database

The module uses SQLite for storage by default. Database configuration can be customized via the `DATABASE_URL` environment variable:

```bash
# Use SQLite (default)
export DATABASE_URL="sqlite:///./conversation_memory.db"

# Use other databases (PostgreSQL example)
export DATABASE_URL="postgresql://user:password@localhost/conversation_memory"
```

## Error Handling

The API provides comprehensive error responses:

### 400 Bad Request
```json
{
  "detail": "Failed to create memory: Invalid input"
}
```

### 404 Not Found
```json
{
  "detail": "Memory with ID 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Detailed error message"
}
```

## Input Validation

All input fields are validated:
- **session_id**: Required, 1-255 characters, alphanumeric with hyphens/underscores
- **question**: Required, non-empty text
- **answer**: Required, non-empty text
- **tags**: Optional, max 500 characters

## Usage Examples

### Python with requests
```python
import requests

BASE_URL = "http://localhost:8000"

# Create a memory
response = requests.post(
    f"{BASE_URL}/memory",
    json={
        "session_id": "interview-001",
        "question": "Tell us about yourself",
        "answer": "I'm a software engineer with 5 years of experience",
        "tags": "introduction,background"
    }
)
print(response.json())

# Get all memories
response = requests.get(
    f"{BASE_URL}/memory",
    params={"session_id": "interview-001"}
)
print(response.json())

# Get specific memory
response = requests.get(f"{BASE_URL}/memory/1")
print(response.json())

# Update memory
response = requests.put(
    f"{BASE_URL}/memory/1",
    json={"answer": "Updated answer"}
)
print(response.json())

# Delete memory
response = requests.delete(f"{BASE_URL}/memory/1")
print(response.status_code)
```

### cURL
```bash
# Create a memory
curl -X POST http://localhost:8000/memory \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "interview-001",
    "question": "Tell us about yourself",
    "answer": "I am a software engineer",
    "tags": "introduction"
  }'

# Get all memories
curl http://localhost:8000/memory

# Get specific memory
curl http://localhost:8000/memory/1

# Update memory
curl -X PUT http://localhost:8000/memory/1 \
  -H "Content-Type: application/json" \
  -d '{"answer": "Updated answer"}'

# Delete memory
curl -X DELETE http://localhost:8000/memory/1
```

## Performance Considerations

- **Pagination**: Use `skip` and `limit` parameters to handle large datasets
- **Indexing**: The database uses indexes on `session_id` and `timestamp` for faster queries
- **Tag Search**: Tags are stored as strings and support partial matching

## Security Considerations

- Input validation is performed on all fields
- SQL injection is prevented through SQLAlchemy ORM
- CORS is configured (can be restricted by origin)
- Consider adding authentication/authorization for production use

## Development

### Running Tests
```bash
# Run pytest on the project
pytest
```

### Code Structure

- **main.py**: Application factory and entry point
- **database.py**: Database configuration and session management
- **models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic validation schemas
- **crud.py**: CRUD operation implementations
- **routes.py**: API endpoint definitions

## Extending the Module

### Adding New Fields

1. Update the model in `models.py`
2. Update schemas in `schemas.py`
3. Update CRUD methods if needed in `crud.py`
4. Update routes if needed in `routes.py`

### Adding New Endpoints

1. Add method to `ConversationMemoryCRUD` class in `crud.py`
2. Add route decorator and method to `routes.py`
3. Create/update schemas as needed

## Troubleshooting

### Database Lock Error
```
sqlite3.OperationalError: database is locked
```
- Ensure only one process is accessing the database
- Check if the database file has proper permissions

### Connection Error
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL
```
- Verify DATABASE_URL environment variable format
- Check database server is running (if using PostgreSQL, etc.)

### Port Already in Use
```
Address already in use
```
```bash
# Change port
uvicorn main:app --port 8001
```

## License

This project is provided as-is for educational and business use.

## Support

For issues or questions, please refer to the code documentation and docstrings within each module.
#   c o n v e r s a t i o n _ m e m o r y _ m o d u l e  
 