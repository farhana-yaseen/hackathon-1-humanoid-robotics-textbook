"""
Translation Cache Model for Authentication Redirect & Urdu Translation feature
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TranslationCacheBase(BaseModel):
    content_hash: str
    target_language: str
    translated_content: str
    original_content_length: Optional[int] = None


class TranslationCacheCreate(TranslationCacheBase):
    expires_at: datetime


class TranslationCacheUpdate(BaseModel):
    translated_content: Optional[str] = None
    expires_at: Optional[datetime] = None


class TranslationCache(TranslationCacheBase):
    created_at: datetime
    expires_at: datetime
    original_content_length: Optional[int] = None

    class Config:
        from_attributes = True