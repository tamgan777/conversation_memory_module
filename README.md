# Task 15 — Conversation Memory Module

**Assigned to:** Your Name  
**Phase:** Phase 4 — Backend Services  
**Module:** Conversation Memory Service

---

# Overview

This module stores and retrieves conversation history for AI assistants, interview systems, and chatbots. It maintains context across multiple sessions by saving questions, answers, timestamps, and tags in a database.

The service is built using FastAPI, SQLAlchemy, and SQLite, providing a lightweight and scalable solution for conversation memory management.

---

# Setup

Install project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API Documentation:

```text
Swagger UI:
http://localhost:8000/docs

ReDoc:
http://localhost:8000/redoc
```

---

# Project Structure

```text
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
```

---

# Components

## 1. Application Layer

Responsible for:

- Starting FastAPI server
- Registering routes
- Configuring middleware
- Initializing services

**File:** `main.py`

---

## 2. Database Layer

Responsible for:

- Database connection
- Session management
- Table creation
- Database configuration

**File:** `database.py`

---

## 3. Model Layer

Responsible for:

- Defining database tables
- Defining indexes
- Defining constraints

**File:** `models.py`

### Database Model

| Field | Description |
|---------|---------|
| id | Unique memory ID |
| session_id | Session identifier |
| question | Stored question |
| answer | Stored answer |
| timestamp | Creation timestamp |
| tags | Optional tags |

---

## 4. Validation Layer

Responsible for:

- Request validation
- Response serialization
- Data type checking

**File:** `schemas.py`

---

## 5. CRUD Layer

Responsible for:

- Create memory
- Retrieve memory
- Update memory
- Delete memory
- Search memory

**File:** `crud.py`

---

## 6. API Layer

Responsible for:

- Handling HTTP requests
- Processing responses
- Calling CRUD operations
- Error handling

**File:** `routes.py`

---

# Running the Module

## Start the Server

```bash
uvicorn main:app --reload
```

## Verify Health Endpoint

```http
GET /health
```

Expected Response:

```json
{
  "status": "healthy"
}
```

---

# API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /health | Service health check |
| POST | /memory | Create memory |
| GET | /memory | Get all memories |
| GET | /memory/{id} | Get memory by ID |
| GET | /memory/session/{session_id} | Get session memories |
| GET | /memory/search/tags | Search by tags |
| PUT | /memory/{id} | Update memory |
| DELETE | /memory/{id} | Delete memory |
| DELETE | /memory/session/{session_id} | Delete session memories |

---

# Example Request

```json
{
  "session_id": "session-001",
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern Python web framework.",
  "tags": "python,backend"
}
```

---

# Example Response

```json
{
  "id": 1,
  "session_id": "session-001",
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern Python web framework.",
  "tags": "python,backend",
  "timestamp": "2026-05-30T12:00:00"
}
```

---

# Test Coverage

The module supports testing for:

- Memory creation
- Memory retrieval
- Session filtering
- Tag-based searching
- Memory updates
- Memory deletion
- Session deletion
- API health checks
- Input validation
- Error handling

---

# Output

### Successful Memory Creation

```json
{
  "id": 1,
  "session_id": "session-001",
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern Python web framework.",
  "tags": "python,backend"
}
```

### Successful Session Retrieval

Returns all memories linked to a specific session.

### Successful Tag Search

Returns all memories matching provided tags.

---

# Error Handling

## 400 Bad Request

```json
{
  "detail": "Invalid request"
}
```

## 404 Not Found

```json
{
  "detail": "Memory not found"
}
```

## 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

---

# Performance Features

- Pagination support
- Indexed session lookups
- Indexed timestamp lookups
- Optimized SQLAlchemy queries
- Lightweight SQLite backend
- Fast CRUD operations

---

# Security Features

- Request validation using Pydantic
- SQL injection protection through SQLAlchemy ORM
- Structured error handling
- Safe database access
- Input sanitization

---

# Future Improvements

- JWT Authentication
- User Management
- Redis Caching
- Semantic Search
- Vector Database Integration
- Conversation Summarization
- Analytics Dashboard
- CSV/PDF Export
- Memory Expiration Policies
- Multi-Tenant Support

---

# Technology Stack

### Backend
- FastAPI

### Database
- SQLite

### ORM
- SQLAlchemy

### Validation
- Pydantic

### Server
- Uvicorn

### Language
- Python

---

# Conclusion

The Conversation Memory Module provides a reliable and efficient solution for storing, retrieving, and managing conversation history. It enables AI assistants, chatbots, and interview systems to maintain context across interactions while offering a clean REST API, persistent storage, and scalable architecture.