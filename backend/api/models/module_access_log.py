"""
Module Access Log Model for Authentication Redirect & Urdu Translation feature
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ModuleAccessLogBase(BaseModel):
    user_id: str
    module_id: str
    session_id: Optional[str] = None
    position: Optional[int] = 0


class ModuleAccessLogCreate(ModuleAccessLogBase):
    pass


class ModuleAccessLogUpdate(BaseModel):
    position: Optional[int] = None
    session_id: Optional[str] = None


class ModuleAccessLog(ModuleAccessLogBase):
    id: uuid.UUID
    access_time: datetime

    class Config:
        from_attributes = True