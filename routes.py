"""
REST API routes for conversation memory management.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    ConversationMemoryCreate,
    ConversationMemoryUpdate,
    ConversationMemoryResponse,
    ConversationMemoryListResponse,
    ErrorResponse
)
from crud import ConversationMemoryCRUD

router = APIRouter(prefix="/memory", tags=["memory"])


@router.post(
    "",
    response_model=ConversationMemoryResponse,
    status_code=201,
    summary="Create a new conversation memory",
    responses={
        201: {"description": "Memory created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
    }
)
def create_memory(
    memory_in: ConversationMemoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation memory record.

    - **session_id**: Unique identifier for the conversation session
    - **question**: The question asked
    - **answer**: The answer provided
    - **tags**: Optional comma-separated tags for categorization
    """
    try:
        memory = ConversationMemoryCRUD.create(db, memory_in)
        return memory
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create memory: {str(e)}"
        )


@router.get(
    "",
    response_model=ConversationMemoryListResponse,
    summary="Retrieve all conversation memories",
    responses={
        200: {"description": "List of memories retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    }
)
def get_all_memories(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all conversation memories with optional filtering.

    Query Parameters:
    - **session_id**: Optional filter by specific session
    - **skip**: Pagination offset (default: 0)
    - **limit**: Pagination limit (default: 100, max: 1000)
    """
    try:
        memories, total = ConversationMemoryCRUD.get_all(
            db,
            skip=skip,
            limit=limit,
            session_id=session_id
        )
        return {
            "items": memories,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to retrieve memories: {str(e)}"
        )


@router.get(
    "/search/tags",
    response_model=ConversationMemoryListResponse,
    summary="Search memories by tags",
    responses={
        200: {"description": "Search results retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    }
)
def search_by_tags(
    tags: str = Query(..., min_length=1, description="Comma-separated tags to search"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """
    Search conversation memories by tags.

    - **tags**: Comma-separated tags to search for
    - **skip**: Pagination offset
    - **limit**: Pagination limit
    """
    try:
        memories, total = ConversationMemoryCRUD.search_by_tags(
            db,
            tags=tags,
            skip=skip,
            limit=limit
        )
        return {
            "items": memories,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to search memories: {str(e)}"
        )


@router.get(
    "/session/{session_id}",
    response_model=ConversationMemoryListResponse,
    summary="Retrieve all memories for a session",
    responses={
        200: {"description": "Session memories retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    }
)
def get_session_memories(
    session_id: str = Path(..., min_length=1, description="The session ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all memories for a specific session.

    - **session_id**: The session identifier
    - **skip**: Pagination offset
    - **limit**: Pagination limit
    """
    try:
        memories, total = ConversationMemoryCRUD.get_by_session(
            db,
            session_id=session_id,
            skip=skip,
            limit=limit
        )
        return {
            "items": memories,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to retrieve session memories: {str(e)}"
        )


@router.get(
    "/{memory_id}",
    response_model=ConversationMemoryResponse,
    summary="Retrieve a specific conversation memory",
    responses={
        200: {"description": "Memory retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Memory not found"},
    }
)
def get_memory(
    memory_id: int = Path(..., gt=0, description="The memory ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific conversation memory by ID.

    - **memory_id**: The unique identifier of the memory record
    """
    memory = ConversationMemoryCRUD.get_by_id(db, memory_id)
    if not memory:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with ID {memory_id} not found"
        )
    return memory





@router.put(
    "/{memory_id}",
    response_model=ConversationMemoryResponse,
    summary="Update a conversation memory",
    responses={
        200: {"description": "Memory updated successfully"},
        404: {"model": ErrorResponse, "description": "Memory not found"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
    }
)
def update_memory(
    memory_id: int = Path(..., gt=0, description="The memory ID"),
    memory_in: ConversationMemoryUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update a conversation memory record.

    - **memory_id**: The unique identifier of the memory to update
    - **memory_in**: Updated memory data (all fields optional)
    """
    memory = ConversationMemoryCRUD.get_by_id(db, memory_id)
    if not memory:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with ID {memory_id} not found"
        )

    try:
        updated_memory = ConversationMemoryCRUD.update(db, memory_id, memory_in)
        return updated_memory
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update memory: {str(e)}"
        )


@router.delete(
    "/{memory_id}",
    status_code=204,
    summary="Delete a conversation memory",
    responses={
        204: {"description": "Memory deleted successfully"},
        404: {"model": ErrorResponse, "description": "Memory not found"},
    }
)
def delete_memory(
    memory_id: int = Path(..., gt=0, description="The memory ID"),
    db: Session = Depends(get_db)
):
    """
    Delete a conversation memory record.

    - **memory_id**: The unique identifier of the memory to delete
    """
    deleted = ConversationMemoryCRUD.delete(db, memory_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with ID {memory_id} not found"
        )
    return None


@router.delete(
    "/session/{session_id}",
    status_code=200,
    summary="Delete all memories for a session",
    responses={
        200: {"description": "Session memories deleted successfully"},
    }
)
def delete_session(
    session_id: str = Path(..., min_length=1, description="The session ID"),
    db: Session = Depends(get_db)
):
    """
    Delete all conversation memories for a specific session.

    - **session_id**: The session identifier
    """
    try:
        deleted_count = ConversationMemoryCRUD.delete_by_session(db, session_id)
        return {
            "message": f"Deleted {deleted_count} memories for session {session_id}",
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete session memories: {str(e)}"
        )
