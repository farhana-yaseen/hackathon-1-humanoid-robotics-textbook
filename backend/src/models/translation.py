from sqlalchemy import Column, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.src.database import Base


class Translation(Base):
    __tablename__ = "translations"

    translation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.chapter_id"), nullable=False)  # Reference to Chapter
    user_session_id = Column(String, nullable=True)  # Session identifier for temporary translations
    urdu_content = Column(Text, nullable=True)  # Urdu translation of chapter content
    translation_quality_score = Column(Float, nullable=True)  # Quality score from 0-1
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Expiration timestamp for temporary translations