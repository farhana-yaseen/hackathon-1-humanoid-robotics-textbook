from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.src.database import Base


class RAGSession(Base):
    __tablename__ = "rag_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)  # Reference to user (null for anonymous sessions)
    session_token = Column(String, nullable=True)  # Token for anonymous session identification
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_interaction_at = Column(DateTime(timezone=True), onupdate=func.now())
    active_selection_context = Column(Text, nullable=True)  # Current selected text context (max 2000 tokens)