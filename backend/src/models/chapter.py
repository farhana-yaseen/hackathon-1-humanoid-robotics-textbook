from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    chapter_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)  # Unique within textbook
    slug = Column(String, unique=True, nullable=False)  # URL-friendly identifier
    content = Column(Text, nullable=False)  # Original English Markdown content
    word_count = Column(Integer, nullable=True)  # Number of words in chapter
    module = Column(String, nullable=True)  # Module category (ROS 2, Digital Twin, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata = Column(Text, nullable=True)  # Additional chapter metadata as JSON string