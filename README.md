# Task 15 — Conversation Memory Module

**Phase:** Backend Services  
**Module:** Conversation Memory Service

---

## Overview

This module stores and retrieves conversation history for chatbots, AI assistants, and interview systems. It helps maintain conversation context across multiple sessions.

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

API Docs:

```text
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## Project Structure

```text
conversation-memory-module/

├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── routes.py
└── requirements.txt
```

---

## Components

| File | Purpose |
|--------|---------|
| main.py | Starts FastAPI app |
| database.py | Database connection |
| models.py | Database tables |
| schemas.py | Data validation |
| crud.py | Database operations |
| routes.py | API endpoints |

---

## API Endpoints

| Method | Endpoint |
|----------|----------|
| GET | /health |
| POST | /memory |
| GET | /memory |
| GET | /memory/{id} |
| GET | /memory/session/{session_id} |
| GET | /memory/search/tags |
| PUT | /memory/{id} |
| DELETE | /memory/{id} |
| DELETE | /memory/session/{session_id} |

---

## Database Model

| Field | Description |
|---------|---------|
| id | Memory ID |
| session_id | Session identifier |
| question | Stored question |
| answer | Stored answer |
| tags | Search tags |
| timestamp | Creation time |

---

## Example Record

```json
{
  "id": 1,
  "session_id": "session-001",
  "question": "What is FastAPI?",
  "answer": "A Python web framework",
  "tags": "python,backend"
}
```

---

## Features

- Store conversation history
- Retrieve previous conversations
- Session-based memory tracking
- Tag-based search
- REST API support
- SQLite database storage

---

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

---

## Conclusion

The Conversation Memory Module is a simple FastAPI service that stores, manages, and retrieves conversation history, helping AI applications maintain context across interactions.