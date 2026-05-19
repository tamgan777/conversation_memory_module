# Quick Start Guide - Conversation Memory Module

Get up and running with the Conversation Memory Module in 5 minutes!

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup (5 minutes)

### Step 1: Navigate to Project Directory
```bash
cd conversation-memory-module
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

You should see:
```
Initializing database...
Database initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Access the API

### Interactive API Documentation
Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/health
```

## Quick Examples

### 1. Create a Memory
```bash
curl -X POST http://localhost:8000/memory \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "interview-001",
    "question": "Tell us about yourself",
    "answer": "I am a software engineer",
    "tags": "introduction"
  }'
```

**Response:**
```json
{
  "id": 1,
  "session_id": "interview-001",
  "question": "Tell us about yourself",
  "answer": "I am a software engineer",
  "tags": "introduction",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Get All Memories
```bash
curl http://localhost:8000/memory
```

### 3. Get Specific Memory
```bash
curl http://localhost:8000/memory/1
```

### 4. Get Session Memories
```bash
curl http://localhost:8000/memory/session/interview-001
```

### 5. Update Memory
```bash
curl -X PUT http://localhost:8000/memory/1 \
  -H "Content-Type: application/json" \
  -d '{"answer": "Updated answer"}'
```

### 6. Delete Memory
```bash
curl -X DELETE http://localhost:8000/memory/1
```

### 7. Search by Tags
```bash
curl "http://localhost:8000/memory/search/tags?tags=introduction"
```

## Using with Python

### Install requests (if not already installed)
```bash
pip install requests
```

### Python Example Script
```python
import requests

BASE_URL = "http://localhost:8000"

# Create memory
response = requests.post(
    f"{BASE_URL}/memory",
    json={
        "session_id": "interview-001",
        "question": "What are your skills?",
        "answer": "Python, JavaScript, SQL",
        "tags": "technical"
    }
)
memory = response.json()
print(f"Created memory with ID: {memory['id']}")

# Get all memories
response = requests.get(f"{BASE_URL}/memory")
print(f"Total memories: {response.json()['total']}")

# Get session memories
response = requests.get(f"{BASE_URL}/memory/session/interview-001")
for item in response.json()['items']:
    print(f"Q: {item['question']}")
    print(f"A: {item['answer']}\n")
```

## Run Examples Script

We've provided a comprehensive examples script:

```bash
python examples.py
```

This will run various example scenarios including:
- Interview session management
- Multiple concurrent sessions
- Pagination
- Tag-based filtering
- Cleanup operations

## Docker Quick Start

### Build Docker Image
```bash
docker build -t conversation-memory .
```

### Run Container
```bash
docker run -p 8000:8000 conversation-memory
```

### Using Docker Compose
```bash
docker-compose up
```

## Running Tests

### Install pytest
```bash
pip install pytest
```

### Run Tests
```bash
pytest test_api.py -v
```

## Project Structure Overview

```
conversation-memory-module/
├── main.py              # Application entry point
├── database.py          # Database config
├── models.py            # Data models
├── schemas.py           # Validation schemas
├── crud.py              # Database operations
├── routes.py            # API endpoints
├── config.py            # Configuration
├── examples.py          # Usage examples
├── test_api.py          # Unit tests
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose config
└── README.md            # Full documentation
```

## Key Files Explained

| File | Purpose |
|------|---------|
| **main.py** | FastAPI app initialization and routes registration |
| **database.py** | SQLAlchemy setup and session management |
| **models.py** | Database table schema (ConversationMemory) |
| **schemas.py** | Request/response validation (Pydantic) |
| **crud.py** | Database operations (Create, Read, Update, Delete) |
| **routes.py** | REST API endpoints |

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/memory` | Create new memory |
| GET | `/memory` | List all memories |
| GET | `/memory/{id}` | Get specific memory |
| GET | `/memory/session/{id}` | Get session memories |
| GET | `/memory/search/tags` | Search by tags |
| PUT | `/memory/{id}` | Update memory |
| DELETE | `/memory/{id}` | Delete memory |
| DELETE | `/memory/session/{id}` | Delete session |

## Common Tasks

### Store Interview Q&A
```python
import requests

session_id = "candidate-john-001"
questions_answers = [
    ("Experience?", "5 years in software development"),
    ("Why us?", "Interested in your tech stack"),
    ("Availability?", "Two weeks notice")
]

for question, answer in questions_answers:
    requests.post(
        "http://localhost:8000/memory",
        json={
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "tags": "interview"
        }
    )
```

### Retrieve All Session Memories
```python
import requests

response = requests.get(
    "http://localhost:8000/memory/session/candidate-john-001"
)
memories = response.json()
for item in memories['items']:
    print(f"Q: {item['question']}\nA: {item['answer']}\n")
```

### Clear a Session
```python
import requests

requests.delete(
    "http://localhost:8000/memory/session/candidate-john-001"
)
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in main.py or use environment variable
set SERVER_PORT=8001  # Windows
export SERVER_PORT=8001  # macOS/Linux
python main.py
```

### Database Lock Error
- Ensure only one instance of the application is running
- Check file permissions on conversation_memory.db

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database File Issues
```bash
# Delete and recreate database
rm conversation_memory.db  # On macOS/Linux
del conversation_memory.db  # On Windows
python main.py  # Will recreate on startup
```

## Next Steps

1. **Read Full Documentation**: See README.md for comprehensive docs
2. **Understand Architecture**: Check ARCHITECTURE.md for design details
3. **Write Tests**: Add more tests in test_api.py
4. **Add Authentication**: Integrate JWT tokens for security
5. **Deploy**: Use Docker or cloud platforms (AWS, GCP, Azure)

## Getting Help

1. **API Docs**: http://localhost:8000/docs (interactive)
2. **README.md**: Comprehensive documentation
3. **ARCHITECTURE.md**: Design and structure overview
4. **examples.py**: Working code examples

## Performance Tips

- Use pagination (skip/limit) for large datasets
- Tag memories for better categorization
- Use session IDs to group related conversations
- Leverage the search endpoint for filtering

## Security Notes

- The default setup allows all CORS origins
- Configure CORS_ORIGINS in .env for production
- Consider adding authentication/authorization
- Validate all inputs (already built-in)
- Use HTTPS in production

## Deployment Checklist

- [ ] Set DEBUG=False in .env
- [ ] Configure DATABASE_URL for your database
- [ ] Set appropriate CORS origins
- [ ] Run tests: pytest test_api.py
- [ ] Use production WSGI server (gunicorn)
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy

Enjoy using the Conversation Memory Module! 🚀
