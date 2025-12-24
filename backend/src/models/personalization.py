"""
PersonalizationProfile model for the Humanoid Robotics Textbook application.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PersonalizationProfile(BaseModel):
    """
    PersonalizationProfile entity for personalized chapter content.

    Attributes:
        profile_id: UUID identifier for the profile
        user_id: Reference to User
        chapter_id: Reference to Chapter
        personalized_content: Personalized version of chapter content
        personalization_rules: Rules used for personalization (JSON)
        created_at: Profile creation timestamp
        updated_at: Last profile update timestamp
    """
    profile_id: str  # Using string representation of UUID
    user_id: str
    chapter_id: str
    personalized_content: Optional[str] = None
    personalization_rules: Optional[dict] = None
    created_at: datetime
    updated_at: datetime