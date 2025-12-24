"""
SQLAlchemy Database Model for Translation Cache
"""
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TranslationCacheDB(Base):
    __tablename__ = "translation_cache"

    content_hash = Column(String(255), primary_key=True, nullable=False)
    target_language = Column(String(10), primary_key=True, nullable=False)
    translated_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    original_content_length = Column(Integer, nullable=True)