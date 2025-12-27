from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class SelectedTextContext(Base):
    __tablename__ = "selected_text_contexts"

    context_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("rag_sessions.session_id"), nullable=False)  # Reference to the session
    selected_text = Column(Text, nullable=False)  # The selected text content (max 2000 tokens)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.chapter_id"), nullable=False)  # Reference to the source chapter
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Expiration time for privacy (short-lived)