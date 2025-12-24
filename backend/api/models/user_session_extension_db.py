"""
SQLAlchemy Database Model for User Session Extension
"""
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class UserSessionExtensionDB(Base):
    __tablename__ = "user_session_extensions"

    user_id = Column(String(255), primary_key=True, nullable=False)
    last_module_id = Column(String(255), nullable=True)
    language_preference = Column(String(10), default='en', nullable=False)
    last_access_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    default_module_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Define the foreign key relationship to user_profiles table
    # Note: This relationship is defined in the database schema but not as a direct SQLAlchemy relationship
    # to avoid circular imports