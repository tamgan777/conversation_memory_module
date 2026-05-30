Conversation Memory Module

Overview

The Conversation Memory Module is a FastAPI-based backend service designed to store, retrieve, manage, and search conversation history. It enables applications such as interview assistants, chatbots, AI agents, customer support systems, and virtual assistants to maintain context across multiple interactions.

The module stores conversations in a database and organizes them using session identifiers. Each memory record contains a question, an answer, optional tags, and a timestamp.

---

Objectives

The primary goals of this module are:

- Maintain conversation continuity across sessions.
- Store structured conversation records.
- Enable quick retrieval of historical conversations.
- Support filtering and searching through tags.
- Provide a simple REST API for integration.
- Support scalable database backends through SQLAlchemy.

---

Key Features

Memory Storage

Store questions and answers for future retrieval.

Session Management

Group conversations using unique session identifiers.

Memory Search

Search stored conversations using tags.

Persistent Storage

Save data permanently using SQLite or other supported databases.

RESTful API

Access all functionality through HTTP endpoints.

Input Validation

Validate all incoming requests using Pydantic schemas.

Interactive Documentation

Automatically generated Swagger and ReDoc documentation.

Database Abstraction

SQLAlchemy ORM allows switching databases without changing business logic.

---

System Architecture

+------------------+
| Client Application |
+---------+--------+
          |
          v
+------------------+
| FastAPI Routes   |
+---------+--------+
          |
          v
+------------------+
| Validation Layer |
| (Pydantic)       |
+---------+--------+
          |
          v
+------------------+
| CRUD Layer       |
+---------+--------+
          |
          v
+------------------+
| SQLAlchemy ORM   |
+---------+--------+
          |
          v
+------------------+
| SQLite Database  |
+------------------+

---

Project Structure

conversation-memory-module/

├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── routes.py
├── requirements.txt
├── .gitignore
└── README.md

---

Module Descriptions

main.py

Application entry point.

Responsibilities:

- Create FastAPI application.
- Register API routes.
- Configure middleware.
- Start application server.

---

database.py

Database configuration module.

Responsibilities:

- Create SQLAlchemy engine.
- Configure database session.
- Provide dependency injection for database access.
- Initialize database tables.

---

models.py

Contains SQLAlchemy ORM models.

Responsibilities:

- Define database tables.
- Define relationships.
- Define indexes and constraints.

---

schemas.py

Contains Pydantic schemas.

Responsibilities:

- Request validation.
- Response serialization.
- Type checking.

---

crud.py

Contains database operations.

Responsibilities:

- Create memory records.
- Retrieve memory records.
- Update memory records.
- Delete memory records.
- Search memories.

---

routes.py

Contains REST API endpoints.

Responsibilities:

- Receive HTTP requests.
- Validate input.
- Call CRUD functions.
- Return responses.

---

Installation

Prerequisites

- Python 3.8+
- pip

---

Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/Mac:

python -m venv venv
source venv/bin/activate

---

Install Dependencies

pip install -r requirements.txt

---

Running the Application

Using Python:

python main.py

Using Uvicorn:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

---

API Documentation

After starting the application:

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

---

Database Model

ConversationMemory

Represents a single conversation memory.

Field| Type| Description
id| Integer| Primary key
session_id| String| Session identifier
question| Text| Stored question
answer| Text| Stored answer
timestamp| DateTime| Creation timestamp
tags| String| Optional tags

---

Example Record

{
    "id": 1,
    "session_id": "interview-001",
    "question": "Tell me about yourself",
    "answer": "I am a software engineer.",
    "tags": "introduction,profile",
    "timestamp": "2026-05-30T12:00:00"
}

---

API Endpoints

Health Check

GET /health

Checks service status.

Response:

{
    "status": "healthy"
}

---

Create Memory

POST /memory

Stores a new memory.

Request:

{
    "session_id": "session-123",
    "question": "What is FastAPI?",
    "answer": "A modern Python web framework.",
    "tags": "python,backend"
}

Response:

{
    "id": 1,
    "session_id": "session-123",
    "question": "What is FastAPI?",
    "answer": "A modern Python web framework.",
    "tags": "python,backend",
    "timestamp": "2026-05-30T12:00:00"
}

---

Get All Memories

GET /memory

Query Parameters:

skip
limit
session_id

Example:

GET /memory?skip=0&limit=50

---

Get Memory By ID

GET /memory/{id}

Example:

GET /memory/1

---

Get Session Memories

GET /memory/session/{session_id}

Example:

GET /memory/session/interview-001

---

Search Memories By Tags

GET /memory/search/tags

Example:

GET /memory/search/tags?tags=python,backend

---

Update Memory

PUT /memory/{id}

Request:

{
    "answer": "Updated answer"
}

---

Delete Memory

DELETE /memory/{id}

Removes a single memory record.

---

Delete Session

DELETE /memory/session/{session_id}

Deletes all memories belonging to a session.

---

Data Flow

Step 1:

User submits a conversation.

Question -> API

Step 2:

Pydantic validates input.

API -> Validation

Step 3:

CRUD layer processes request.

Validation -> CRUD

Step 4:

SQLAlchemy stores data.

CRUD -> Database

Step 5:

Response returned.

Database -> API -> User

---

Error Handling

400 Bad Request

{
    "detail": "Invalid request"
}

---

404 Not Found

{
    "detail": "Memory not found"
}

---

500 Internal Server Error

{
    "detail": "Internal server error"
}

---

Performance Optimizations

- Pagination support.
- Indexed session_id.
- Indexed timestamp.
- Lightweight SQLite storage.
- Efficient ORM queries.

---

Security Considerations

Current Security:

- Input validation.
- ORM-based SQL injection protection.
- Controlled API responses.

Recommended Production Security:

- JWT Authentication.
- HTTPS.
- Rate Limiting.
- User Authorization.
- Audit Logging.

---

Example Use Cases

Interview Assistant

Store candidate responses across interview rounds.

AI Chatbot

Maintain conversation context.

Customer Support

Track customer interactions.

Virtual Assistant

Remember previous user discussions.

Learning Platforms

Store student question-answer history.

---

Future Enhancements

- User Accounts
- JWT Authentication
- Redis Cache
- Vector Database Integration
- Semantic Search
- Conversation Summarization
- Export to CSV/PDF
- Analytics Dashboard
- Memory Expiration Policies
- Multi-Tenant Support

---

Technology Stack

Backend:

- FastAPI

Database:

- SQLite

ORM:

- SQLAlchemy

Validation:

- Pydantic

Server:

- Uvicorn

Language:

- Python

---

Conclusion

The Conversation Memory Module is a lightweight, scalable, and production-ready backend service for storing and managing conversational context. It provides session-based memory management, efficient retrieval mechanisms, search capabilities, and a clean REST API, making it suitable for AI assistants, interview systems, chatbots, customer support solutions, and any application that requires persistent conversational memory.