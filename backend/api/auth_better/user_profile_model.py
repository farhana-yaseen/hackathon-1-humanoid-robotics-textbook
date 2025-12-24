"""
User Profile Model for Better-Auth feature
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high-school"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    POSTGRADUATE = "postgraduate"
    PROFESSIONAL = "professional"


class UserProfileBase(BaseModel):
    user_id: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = 0
    primary_interest: Optional[str] = None
    education_level: Optional[EducationLevel] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = None
    primary_interest: Optional[str] = None
    education_level: Optional[EducationLevel] = None


class UserProfile(UserProfileBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True