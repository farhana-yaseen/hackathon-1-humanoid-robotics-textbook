from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    software_background = Column(Text, nullable=True)
    hardware_background = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    data_retention_expires_at = Column(DateTime(timezone=True), nullable=True)
    preferences = Column(Text, nullable=True)  # JSON stored as text
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Relationships
    personalization_profiles = relationship("PersonalizationProfile", back_populates="user")