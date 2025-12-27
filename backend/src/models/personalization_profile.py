from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..database import Base


class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"

    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)  # Reference to User
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.chapter_id"), nullable=True)  # Reference to Chapter, optional
    personalized_content = Column(Text, nullable=True)  # Personalized version of chapter content
    personalization_rules = Column(Text, nullable=True)  # Rules used for personalization as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="personalization_profiles")