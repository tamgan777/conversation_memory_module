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

Automatically generated Swagger UI and ReDoc documentation.

Database Abstraction

SQLAlchemy ORM allows switching databases without changing business logic.

---

System Architecture

Client Application
        │
        ▼
 FastAPI Routes
        │
        ▼
 Validation Layer
   (Pydantic)
        │
        ▼
    CRUD Layer
        │
        ▼
 SQLAlchemy ORM
        │
        ▼
 SQLite Database

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

- Create FastAPI application
- Register API routes
- Configure middleware
- Start application server

database.py

Database configuration module.

Responsibilities:

- Create SQLAlchemy engine
- Configure database session
- Provide dependency injection
- Initialize database tables

models.py

Contains SQLAlchemy ORM models.

Responsibilities:

- Define database tables
- Define indexes
- Define constraints

schemas.py

Contains Pydantic schemas.

Responsibilities:

- Request validation
- Response serialization
- Type checking

crud.py

Contains database operations.

Responsibilities:

- Create memory
- Retrieve memory
- Update memory
- Delete memory
- Search memory

routes.py

Contains REST API endpoints.

Responsibilities:

- Receive requests
- Validate data
- Execute CRUD operations
- Return responses

---

Installation

Prerequisites

- Python 3.8+
- pip

Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Linux/Mac

python -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

---

Configuration

The application supports configuration using environment variables.

Example:

DATABASE_URL=sqlite:///./conversation_memory.db

---

Environment Variables

Variable| Description
DATABASE_URL| Database connection string
HOST| Server host
PORT| Server port
DEBUG| Debug mode

Example:

DATABASE_URL=sqlite:///./conversation_memory.db
HOST=0.0.0.0
PORT=8000
DEBUG=True

---

Running the Application

Using Python:

python main.py

Using Uvicorn:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

---

API Documentation

After startup:

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

---

Database Model

ConversationMemory

Field| Type| Description
id| Integer| Primary Key
session_id| String| Session Identifier
question| Text| User Question
answer| Text| Stored Answer
timestamp| DateTime| Creation Time
tags| String| Optional Tags

---

Example Record

{
  "id": 1,
  "session_id": "interview-001",
  "question": "Tell me about yourself",
  "answer": "I am a software engineer",
  "tags": "introduction,profile",
  "timestamp": "2026-05-30T12:00:00"
}

---

API Endpoints

Health Check

GET /health

Response:

{
  "status": "healthy"
}

Create Memory

POST /memory

Get All Memories

GET /memory

Get Memory By ID

GET /memory/{id}

Get Session Memories

GET /memory/session/{session_id}

Search Memories By Tags

GET /memory/search/tags

Update Memory

PUT /memory/{id}

Delete Memory

DELETE /memory/{id}

Delete Session

DELETE /memory/session/{session_id}

---

Request / Response Examples

Create Memory

Request:

{
  "session_id": "session-123",
  "question": "What is FastAPI?",
  "answer": "A modern Python framework",
  "tags": "python,backend"
}

Response:

{
  "id": 1,
  "session_id": "session-123",
  "question": "What is FastAPI?",
  "answer": "A modern Python framework",
  "tags": "python,backend",
  "timestamp": "2026-05-30T12:00:00"
}

---

Data Flow

Step 1

User submits a request.

Client → API

Step 2

Input validation.

API → Pydantic

Step 3

Business logic execution.

Pydantic → CRUD

Step 4

Database operation.

CRUD → SQLAlchemy → Database

Step 5

Return response.

Database → API → Client

---

Error Handling

400 Bad Request

{
  "detail": "Invalid request"
}

404 Not Found

{
  "detail": "Memory not found"
}

500 Internal Server Error

{
  "detail": "Internal server error"
}

---

Testing

Run all tests:

pytest

Run with coverage:

pytest --cov=.

Testing areas:

- API endpoints
- Validation
- CRUD operations
- Database integration

---

Deployment

Using Uvicorn:

uvicorn main:app --host 0.0.0.0 --port 8000

Using Docker:

docker build -t conversation-memory .
docker run -p 8000:8000 conversation-memory

---

Performance Optimizations

- Pagination support
- Indexed session_id
- Indexed timestamp
- Efficient ORM queries
- Lightweight SQLite backend

---

Security Considerations

Current Security:

- Input validation
- SQLAlchemy ORM protection
- Controlled responses

Recommended Production Security:

- JWT Authentication
- HTTPS
- Rate Limiting
- Access Control
- Audit Logs

---

Logging and Monitoring

Recommended tools:

- Python Logging
- Prometheus
- Grafana
- ELK Stack

Metrics to monitor:

- API response time
- Error rates
- Memory creation rate
- Database performance

---

Limitations

- SQLite is not ideal for heavy production workloads.
- Tag search uses string matching.
- No built-in authentication.
- No semantic search capability.

---

Example Use Cases

Interview Assistant

Store candidate answers.

AI Chatbot

Maintain conversation context.

Customer Support

Track support interactions.

Virtual Assistant

Remember previous discussions.

Learning Platform

Store student interactions.

---

Future Enhancements

- JWT Authentication
- User Accounts
- Redis Caching
- Vector Database Integration
- Semantic Search
- AI Summarization
- Analytics Dashboard
- PDF/CSV Export
- Memory Expiration Policies
- Multi-Tenant Architecture

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

The Conversation Memory Module is a lightweight, scalable, and maintainable backend service for storing and managing conversational context. By combining FastAPI, SQLAlchemy, and SQLite, it provides a reliable foundation for AI assistants, interview systems, chatbots, and customer support platforms that require persistent conversation memory.