"""
CRUD operations for conversation memory.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import ConversationMemory
from schemas import ConversationMemoryCreate, ConversationMemoryUpdate


class ConversationMemoryCRUD:
    """
    CRUD operations for conversation memory records.
    """

    @staticmethod
    def create(db: Session, memory_in: ConversationMemoryCreate) -> ConversationMemory:
        """
        Create a new conversation memory record.

        Args:
            db: Database session
            memory_in: Schema with memory data

        Returns:
            Created ConversationMemory object
        """
        db_memory = ConversationMemory(
            session_id=memory_in.session_id,
            question=memory_in.question,
            answer=memory_in.answer,
            tags=memory_in.tags,
            timestamp=datetime.utcnow()
        )
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        return db_memory

    @staticmethod
    def get_by_id(db: Session, memory_id: int) -> ConversationMemory:
        """
        Retrieve a conversation memory by ID.

        Args:
            db: Database session
            memory_id: The memory ID

        Returns:
            ConversationMemory object or None
        """
        return db.query(ConversationMemory).filter(
            ConversationMemory.id == memory_id
        ).first()

    @staticmethod
    def get_by_session(
        db: Session,
        session_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[ConversationMemory], int]:
        """
        Retrieve all memories for a specific session.

        Args:
            db: Database session
            session_id: The session ID
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            Tuple of (memories list, total count)
        """
        query = db.query(ConversationMemory).filter(
            ConversationMemory.session_id == session_id
        )
        total = query.count()
        memories = query.order_by(
            ConversationMemory.timestamp.desc()
        ).offset(skip).limit(limit).all()
        return memories, total

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        session_id: str = None
    ) -> tuple[list[ConversationMemory], int]:
        """
        Retrieve all conversation memories with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            session_id: Optional filter by session

        Returns:
            Tuple of (memories list, total count)
        """
        query = db.query(ConversationMemory)

        if session_id:
            query = query.filter(ConversationMemory.session_id == session_id)

        total = query.count()
        memories = query.order_by(
            ConversationMemory.timestamp.desc()
        ).offset(skip).limit(limit).all()
        return memories, total

    @staticmethod
    def search_by_tags(
        db: Session,
        tags: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[ConversationMemory], int]:
        """
        Search memories by tags.

        Args:
            db: Database session
            tags: Comma-separated tags to search
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            Tuple of (memories list, total count)
        """
        # Split tags and create search conditions
        tag_list = [tag.strip().lower() for tag in tags.split(',')]
        conditions = [
            ConversationMemory.tags.ilike(f'%{tag}%')
            for tag in tag_list
        ]

        query = db.query(ConversationMemory).filter(or_(*conditions))
        total = query.count()
        memories = query.order_by(
            ConversationMemory.timestamp.desc()
        ).offset(skip).limit(limit).all()
        return memories, total

    @staticmethod
    def update(
        db: Session,
        memory_id: int,
        memory_in: ConversationMemoryUpdate
    ) -> ConversationMemory:
        """
        Update a conversation memory record.

        Args:
            db: Database session
            memory_id: The memory ID to update
            memory_in: Schema with updated data

        Returns:
            Updated ConversationMemory object
        """
        db_memory = db.query(ConversationMemory).filter(
            ConversationMemory.id == memory_id
        ).first()

        if db_memory:
            update_data = memory_in.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_memory, field, value)
            db.add(db_memory)
            db.commit()
            db.refresh(db_memory)

        return db_memory

    @staticmethod
    def delete(db: Session, memory_id: int) -> bool:
        """
        Delete a conversation memory record.

        Args:
            db: Database session
            memory_id: The memory ID to delete

        Returns:
            True if deleted, False if not found
        """
        db_memory = db.query(ConversationMemory).filter(
            ConversationMemory.id == memory_id
        ).first()

        if db_memory:
            db.delete(db_memory)
            db.commit()
            return True

        return False

    @staticmethod
    def delete_by_session(db: Session, session_id: str) -> int:
        """
        Delete all memories for a specific session.

        Args:
            db: Database session
            session_id: The session ID

        Returns:
            Number of deleted records
        """
        memories = db.query(ConversationMemory).filter(
            ConversationMemory.session_id == session_id
        ).all()

        for memory in memories:
            db.delete(memory)

        db.commit()
        return len(memories)

    @staticmethod
    def clear_all(db: Session) -> int:
        """
        Delete all conversation memories.

        Args:
            db: Database session

        Returns:
            Number of deleted records
        """
        count = db.query(ConversationMemory).delete()
        db.commit()
        return count
