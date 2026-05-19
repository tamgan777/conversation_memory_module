"""
SQLAlchemy ORM models for conversation memory.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from database import Base


class ConversationMemory(Base):
    """
    Model for storing conversation context and history.
    """
    __tablename__ = "conversation_memories"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Session identifier for grouping related conversations
    session_id = Column(String(255), nullable=False, index=True)

    # The question asked in the conversation
    question = Column(Text, nullable=False)

    # The answer or response provided
    answer = Column(Text, nullable=False)

    # Timestamp when the memory was created
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Optional tags for categorization and filtering
    tags = Column(String(500), nullable=True)  # Stored as comma-separated values

    # Create composite index for efficient querying
    __table_args__ = (
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )

    def __repr__(self):
        return f"<ConversationMemory(id={self.id}, session_id={self.session_id}, timestamp={self.timestamp})>"
