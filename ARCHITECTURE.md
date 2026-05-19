# Conversation Memory Module - Architecture Guide

## Overview

The Conversation Memory Module is a FastAPI-based service designed to store and retrieve conversation context for interview sessions. It provides a clean REST API with persistent storage using SQLite and SQLAlchemy ORM.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Client Application                 │
│                  (Browser / API Client)              │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTP/REST
                     │
┌────────────────────▼────────────────────────────────┐
│              FastAPI Application                     │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Routes Layer (routes.py)                     │   │
│  │ - REST endpoints                            │   │
│  │ - Request/Response handling                 │   │
│  │ - Error handling                            │   │
│  └────────────┬─────────────────────────────────┘   │
│               │                                      │
│  ┌────────────▼─────────────────────────────────┐   │
│  │ CRUD Layer (crud.py)                        │   │
│  │ - Business logic                            │   │
│  │ - Database operations                       │   │
│  │ - Query building                            │   │
│  └────────────┬─────────────────────────────────┘   │
│               │                                      │
│  ┌────────────▼─────────────────────────────────┐   │
│  │ Validation Layer (schemas.py)               │   │
│  │ - Pydantic models                           │   │
│  │ - Input validation                          │   │
│  │ - Output serialization                      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└────────────────────┬────────────────────────────────┘
                     │
                     │ SQL
                     │
┌────────────────────▼────────────────────────────────┐
│         Database Layer (SQLAlchemy + SQLite)        │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ ORM Models (models.py)                       │   │
│  │ - ConversationMemory model                  │   │
│  │ - Column definitions                        │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Database Connection (database.py)            │   │
│  │ - Engine configuration                       │   │
│  │ - Session management                        │   │
│  │ - Table initialization                      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              SQLite Database                         │
│           (conversation_memory.db)                   │
└──────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. **main.py** - Application Entry Point
- FastAPI application factory
- Route registration
- Middleware configuration (CORS)
- Startup/shutdown event handlers
- Health check and root endpoints
- Exception handling

**Key Responsibilities:**
- Bootstrap the application
- Initialize database on startup
- Register all routes
- Configure CORS for cross-origin requests

### 2. **database.py** - Database Configuration
- SQLAlchemy engine creation
- Session factory setup
- Base class for ORM models
- Dependency injection for database sessions
- Database initialization function

**Key Responsibilities:**
- Manage database connections
- Provide session dependency for routes
- Handle database setup and migrations

### 3. **models.py** - ORM Models
- SQLAlchemy declarative model: `ConversationMemory`
- Table structure and columns
- Database indexes for performance
- Relationships and constraints

**Model Structure:**
```
ConversationMemory
├── id (Integer, PK)
├── session_id (String, FK, Indexed)
├── question (Text)
├── answer (Text)
├── timestamp (DateTime, Indexed)
└── tags (String)
```

### 4. **schemas.py** - Pydantic Validation
- Request/Response schemas
- Input validation rules
- Field documentation
- Custom validators

**Schemas:**
- `ConversationMemoryBase`: Common fields
- `ConversationMemoryCreate`: POST request
- `ConversationMemoryUpdate`: PUT request
- `ConversationMemoryResponse`: API response
- `ConversationMemoryListResponse`: Paginated responses
- `ErrorResponse`: Error messages

### 5. **crud.py** - CRUD Operations
- Database query implementations
- Data manipulation methods
- Business logic encapsulation
- Error handling

**Methods:**
- `create()`: Insert new record
- `get_by_id()`: Retrieve by ID
- `get_by_session()`: Session-based queries
- `get_all()`: List all with filtering
- `search_by_tags()`: Tag-based search
- `update()`: Modify existing record
- `delete()`: Remove record
- `delete_by_session()`: Bulk delete
- `clear_all()`: Clear entire table

### 6. **routes.py** - REST API Endpoints
- FastAPI route definitions
- Request/response handling
- Dependency injection
- Error responses

**Endpoints:**
```
POST   /memory                    - Create memory
GET    /memory                    - List all memories
GET    /memory/{id}               - Get specific memory
GET    /memory/session/{session}  - Get session memories
GET    /memory/search/tags        - Search by tags
PUT    /memory/{id}               - Update memory
DELETE /memory/{id}               - Delete memory
DELETE /memory/session/{session}  - Delete session
```

## Data Flow

### Create Memory Flow
```
1. Client sends POST /memory with JSON payload
2. FastAPI receives request
3. Pydantic schema validates input
4. Route handler validates permission
5. CRUD layer creates model instance
6. SQLAlchemy ORM generates INSERT SQL
7. SQLite executes SQL and stores data
8. Row ID and timestamp are returned
9. Pydantic schema serializes response
10. Response is sent to client
```

### Retrieve Memory Flow
```
1. Client sends GET /memory/{id}
2. FastAPI parses path parameter
3. Route handler calls CRUD layer
4. CRUD queries database: SELECT * FROM memories WHERE id = ?
5. SQLAlchemy ORM maps result to model
6. CRUD returns model instance
7. Pydantic schema serializes to JSON
8. Response is sent to client
```

### Update Memory Flow
```
1. Client sends PUT /memory/{id} with JSON payload
2. FastAPI receives and validates input
3. Route checks if record exists
4. CRUD fetches existing record
5. CRUD updates fields with new values
6. SQLAlchemy generates UPDATE SQL
7. SQLite executes update
8. Updated record is returned
9. Pydantic serializes response
10. Response sent to client
```

## Database Schema

### ConversationMemory Table
```sql
CREATE TABLE conversation_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tags VARCHAR(500),
    
    INDEX idx_session_timestamp (session_id, timestamp),
    INDEX idx_session_id (session_id)
);
```

## Design Patterns Used

### 1. **Repository Pattern** (crud.py)
- Abstracts data access logic
- Centralizes database queries
- Easy to test and maintain
- Allows switching database backends

### 2. **Dependency Injection** (routes.py, database.py)
```python
def get_memory(
    memory_id: int,
    db: Session = Depends(get_db)  # Injected dependency
):
    pass
```

### 3. **Layered Architecture**
- **Presentation Layer**: routes.py (REST endpoints)
- **Business Logic Layer**: crud.py (operations)
- **Validation Layer**: schemas.py (input/output)
- **Data Access Layer**: database.py (ORM)
- **Storage Layer**: SQLite (persistence)

### 4. **Model Mapping**
- **Database Model**: SQLAlchemy ORM models
- **API Schema**: Pydantic models
- **Clear separation** between data representation layers

### 5. **Error Handling**
- HTTPException for API errors
- Status codes (201, 404, 400, 500)
- Detailed error messages
- Exception handlers at application level

## Performance Considerations

### 1. **Indexing**
- Composite index on (session_id, timestamp)
- Single index on session_id
- Single index on timestamp
- Optimized for common queries

### 2. **Pagination**
- Prevents loading entire datasets
- Configurable skip/limit
- Maximum limit protection (1000 items)

### 3. **Query Optimization**
```python
# Efficient query with ordering
query = db.query(ConversationMemory).filter(
    ConversationMemory.session_id == session_id
).order_by(
    ConversationMemory.timestamp.desc()
).offset(skip).limit(limit)
```

### 4. **Lazy Loading**
- SQLAlchemy lazy loads related data
- Only fetches what's needed

## Security Considerations

### 1. **Input Validation**
- Pydantic validates all inputs
- Field length constraints
- Type checking

### 2. **SQL Injection Prevention**
- SQLAlchemy parameterized queries
- ORM prevents SQL injection
- No string concatenation in queries

### 3. **CORS Configuration**
- Configurable allowed origins
- Prevents unauthorized cross-origin requests

### 4. **Rate Limiting** (Optional)
- Can be added via middleware
- Prevent DoS attacks

### 5. **Authentication** (Optional)
- JWT tokens can be added
- Secure session management

## Extensibility

### Adding New Fields
1. Update `ConversationMemory` model in models.py
2. Add field to schemas
3. Migration (if using PostgreSQL)

### Adding New Endpoints
1. Add CRUD method in crud.py
2. Add route in routes.py
3. Create request/response schemas

### Switching Databases
1. Update DATABASE_URL in config
2. Adjust SQLAlchemy connection string
3. Same ORM code works across databases

## Testing Strategy

### Unit Tests
- Test each CRUD operation
- Test validation schemas
- Test endpoint responses
- Test error handling

### Integration Tests
- Test full request/response cycle
- Test database interactions
- Test business logic flows

### Test Database
- Use in-memory SQLite for tests
- Fresh database per test session
- Fast and isolated tests

## Deployment Options

### 1. **Local Development**
```bash
python main.py
```

### 2. **Production with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 3. **Docker Container**
```bash
docker build -t conversation-memory .
docker run -p 8000:8000 conversation-memory
```

### 4. **Docker Compose**
```bash
docker-compose up
```

## Configuration Management

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SERVER_HOST`: Server host address
- `SERVER_PORT`: Server port
- `DEBUG`: Debug mode
- `CORS_ORIGINS`: Allowed CORS origins
- `LOG_LEVEL`: Logging level

### .env File
- Local development configuration
- `.env.example` provided as template
- Never commit `.env` to version control

## Monitoring and Logging

### Health Check Endpoint
```
GET /health
Response: {"status": "healthy", "service": "Conversation Memory Module"}
```

### Application Logging
- Can be enhanced with logging module
- Request/response logging
- Error tracking

## Future Enhancements

1. **Authentication & Authorization**
   - JWT token support
   - Role-based access control
   - API key management

2. **Advanced Search**
   - Full-text search
   - Elasticsearch integration
   - Semantic search

3. **Analytics**
   - Query analytics
   - Usage statistics
   - Performance metrics

4. **Caching**
   - Redis cache layer
   - Query result caching
   - Session caching

5. **Export/Import**
   - CSV export
   - JSON export/import
   - Batch operations

6. **Audit Trail**
   - Track modifications
   - User attribution
   - Change history

## Summary

The Conversation Memory Module demonstrates best practices in:
- Clean architecture with separated concerns
- Proper layering (presentation, business, data)
- Input validation and error handling
- RESTful API design
- Database optimization
- Code maintainability and testability

The modular structure makes it easy to understand, test, extend, and deploy.
