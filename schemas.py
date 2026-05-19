"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class ConversationMemoryBase(BaseModel):
    """
    Base schema for conversation memory data.
    """
    session_id: str = Field(..., min_length=1, max_length=255, description="Session identifier")
    question: str = Field(..., min_length=1, description="The question asked")
    answer: str = Field(..., min_length=1, description="The answer provided")
    tags: Optional[str] = Field(None, max_length=500, description="Optional comma-separated tags")

    @field_validator('session_id', 'question', 'answer', 'tags', mode='before')
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from string fields."""
        if isinstance(v, str):
            return v.strip()
        return v


class ConversationMemoryCreate(ConversationMemoryBase):
    """
    Schema for creating a new conversation memory.
    """
    pass


class ConversationMemoryUpdate(BaseModel):
    """
    Schema for updating a conversation memory.
    All fields are optional.
    """
    session_id: Optional[str] = Field(None, min_length=1, max_length=255)
    question: Optional[str] = Field(None, min_length=1)
    answer: Optional[str] = Field(None, min_length=1)
    tags: Optional[str] = Field(None, max_length=500)

    @field_validator('session_id', 'question', 'answer', 'tags', mode='before')
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from string fields."""
        if isinstance(v, str):
            return v.strip()
        return v


class ConversationMemoryResponse(ConversationMemoryBase):
    """
    Schema for responding with conversation memory data.
    """
    id: int = Field(..., description="Memory record ID")
    timestamp: datetime = Field(..., description="When the memory was created")

    class Config:
        from_attributes = True  # Support ORM objects


class ConversationMemoryListResponse(BaseModel):
    """
    Schema for list responses with pagination metadata.
    """
    items: List[ConversationMemoryResponse]
    total: int
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
