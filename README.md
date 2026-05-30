Conversation Memory Module

Overview

The Conversation Memory Module is a FastAPI service that stores and retrieves conversation history. It helps applications such as chatbots, interview assistants, and AI agents remember previous conversations and maintain context.

---

Objectives

- Store conversation data
- Retrieve previous conversations
- Group conversations using session IDs
- Search conversations using tags
- Provide simple REST APIs

---

Key Features

- Save questions and answers
- Session-based memory management
- Tag-based search
- SQLite database storage
- FastAPI REST APIs
- Input validation with Pydantic

---

System Architecture

Client
   │
   ▼
FastAPI API
   │
   ▼
CRUD Operations
   │
   ▼
SQLAlchemy
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
└── requirements.txt

---

Module Description

main.py

Starts the FastAPI application.

database.py

Handles database connection.

models.py

Defines database tables.

schemas.py

Validates request and response data.

crud.py

Performs database operations.

routes.py

Contains API endpoints.

---

Installation

Install dependencies:

pip install -r requirements.txt

Run the application:

uvicorn main:app --reload

---

API Documentation

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

---

Database Model

ConversationMemory

Field| Description
id| Unique ID
session_id| Session identifier
question| Stored question
answer| Stored answer
tags| Optional tags
timestamp| Creation time

---

Example Record

{
  "id": 1,
  "session_id": "session-001",
  "question": "What is FastAPI?",
  "answer": "A Python web framework",
  "tags": "python,backend"
}

---

API Endpoints

Method| Endpoint| Purpose
GET| /health| Check service status
POST| /memory| Create memory
GET| /memory| Get all memories
GET| /memory/{id}| Get memory by ID
GET| /memory/session/{session_id}| Get session memories
GET| /memory/search/tags| Search by tags
PUT| /memory/{id}| Update memory
DELETE| /memory/{id}| Delete memory
DELETE| /memory/session/{session_id}| Delete session memories

---

Data Flow

User Request
      ↓
FastAPI API
      ↓
Validation
      ↓
CRUD Layer
      ↓
Database
      ↓
Response

---

Error Handling

400 Bad Request

Invalid input data.

404 Not Found

Memory record not found.

500 Internal Server Error

Unexpected server error.

---

Use Cases

- Interview Assistant
- AI Chatbot
- Customer Support System
- Virtual Assistant
- Learning Platform

---

Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

---

Conclusion

The Conversation Memory Module is a simple backend service that stores, retrieves, updates, and searches conversation history. It helps applications maintain context and remember previous interactions efficiently.