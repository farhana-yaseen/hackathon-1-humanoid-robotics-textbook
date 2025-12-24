from sqlalchemy.orm import Session
from ..models.rag_session import RAGSession
from ..models.selected_text_context import SelectedTextContext
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional


class RAGSessionService:
    """Service class for managing RAG sessions and selected text contexts."""

    @staticmethod
    def create_session(db: Session, user_id: Optional[UUID] = None) -> RAGSession:
        """Create a new RAG session for a user or anonymous session."""
        session_token = str(uuid4()) if user_id is None else None

        db_session = RAGSession(
            user_id=user_id,
            session_token=session_token
        )

        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        return db_session

    @staticmethod
    def get_session(db: Session, session_id: UUID) -> Optional[RAGSession]:
        """Retrieve a RAG session by its ID."""
        return db.query(RAGSession).filter(RAGSession.session_id == session_id).first()

    @staticmethod
    def update_last_interaction(db: Session, session_id: UUID) -> RAGSession:
        """Update the last interaction time for a session."""
        db_session = db.query(RAGSession).filter(RAGSession.session_id == session_id).first()
        if db_session:
            db_session.last_interaction_at = datetime.utcnow()
            db.commit()
            db.refresh(db_session)
        return db_session

    @staticmethod
    def set_selection_context(db: Session, session_id: UUID, selected_text: str) -> RAGSession:
        """Set the active selection context for a session."""
        db_session = db.query(RAGSession).filter(RAGSession.session_id == session_id).first()
        if db_session:
            # Limit to 2000 tokens approximately (assuming ~4 chars per token)
            if len(selected_text) > 8000:  # Rough estimate for 2000 tokens
                selected_text = selected_text[:8000]

            db_session.active_selection_context = selected_text
            db.commit()
            db.refresh(db_session)
        return db_session

    @staticmethod
    def clear_selection_context(db: Session, session_id: UUID) -> RAGSession:
        """Clear the active selection context for a session."""
        db_session = db.query(RAGSession).filter(RAGSession.session_id == session_id).first()
        if db_session:
            db_session.active_selection_context = None
            db.commit()
            db.refresh(db_session)
        return db_session


class SelectedTextContextService:
    """Service class for managing selected text contexts."""

    @staticmethod
    def create_context(db: Session, session_id: UUID, chapter_id: UUID, selected_text: str) -> SelectedTextContext:
        """Create a new selected text context."""
        # Validate token limit (approximate 2000 tokens as ~8000 characters)
        if len(selected_text) > 8000:
            raise ValueError("Selected text exceeds 2000 token limit")

        # Set expiration time (short-lived for privacy) - 1 hour
        expires_at = datetime.utcnow() + timedelta(hours=1)

        context = SelectedTextContext(
            session_id=session_id,
            selected_text=selected_text,
            chapter_id=chapter_id,
            expires_at=expires_at
        )

        db.add(context)
        db.commit()
        db.refresh(context)

        return context

    @staticmethod
    def get_context_by_session(db: Session, session_id: UUID) -> Optional[SelectedTextContext]:
        """Get the active selected text context for a session."""
        return (
            db.query(SelectedTextContext)
            .filter(SelectedTextContext.session_id == session_id)
            .filter(SelectedTextContext.expires_at > datetime.utcnow())
            .order_by(SelectedTextContext.created_at.desc())
            .first()
        )

    @staticmethod
    def get_context_by_id(db: Session, context_id: UUID) -> Optional[SelectedTextContext]:
        """Get a selected text context by its ID."""
        return (
            db.query(SelectedTextContext)
            .filter(SelectedTextContext.context_id == context_id)
            .filter(SelectedTextContext.expires_at > datetime.utcnow())
            .first()
        )

    @staticmethod
    def delete_expired_contexts(db: Session) -> int:
        """Delete expired selected text contexts."""
        deleted_count = (
            db.query(SelectedTextContext)
            .filter(SelectedTextContext.expires_at <= datetime.utcnow())
            .delete()
        )
        db.commit()
        return deleted_count