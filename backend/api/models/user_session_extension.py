"""
User Session Extension Model for Authentication Redirect & Urdu Translation feature
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSessionExtensionBase(BaseModel):
    user_id: str
    last_module_id: Optional[str] = None
    language_preference: Optional[str] = "en"
    default_module_id: Optional[str] = None


class UserSessionExtensionCreate(UserSessionExtensionBase):
    pass


class UserSessionExtensionUpdate(BaseModel):
    last_module_id: Optional[str] = None
    language_preference: Optional[str] = None
    default_module_id: Optional[str] = None


class UserSessionExtension(UserSessionExtensionBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True