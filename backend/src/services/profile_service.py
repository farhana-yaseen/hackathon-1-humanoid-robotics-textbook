from sqlalchemy.orm import Session
from ..models.user import User
from ..models.personalization_profile import PersonalizationProfile
from uuid import UUID
from typing import Optional
from datetime import datetime


class ProfileService:
    """Service class for managing user profiles and personalization."""

    def __init__(self):
        pass

    def get_user_profile(self, db: Session, user_id: UUID) -> Optional[User]:
        """Get user profile by user ID."""
        return db.query(User).filter(User.user_id == user_id).first()

    def update_user_backgrounds(self, db: Session, user_id: UUID, software_background: Optional[str] = None,
                               hardware_background: Optional[str] = None) -> Optional[User]:
        """Update user's software and hardware backgrounds."""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        if software_background is not None:
            user.software_background = software_background
        if hardware_background is not None:
            user.hardware_background = hardware_background

        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def create_personalization_profile(self, db: Session, user_id: UUID, chapter_id: UUID,
                                     personalized_content: Optional[str] = None) -> PersonalizationProfile:
        """Create a personalization profile for a user and chapter."""
        # Check if a profile already exists for this user and chapter
        existing_profile = db.query(PersonalizationProfile).filter(
            PersonalizationProfile.user_id == user_id,
            PersonalizationProfile.chapter_id == chapter_id
        ).first()

        if existing_profile:
            # Update existing profile
            if personalized_content:
                existing_profile.personalized_content = personalized_content
            existing_profile.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_profile)
            return existing_profile

        # Create new profile
        profile = PersonalizationProfile(
            user_id=user_id,
            chapter_id=chapter_id,
            personalized_content=personalized_content
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    def get_personalization_profile(self, db: Session, user_id: UUID, chapter_id: UUID) -> Optional[PersonalizationProfile]:
        """Get personalization profile for a user and chapter."""
        return db.query(PersonalizationProfile).filter(
            PersonalizationProfile.user_id == user_id,
            PersonalizationProfile.chapter_id == chapter_id
        ).first()

    def update_personalization_profile(self, db: Session, user_id: UUID, chapter_id: UUID,
                                     personalized_content: Optional[str] = None) -> Optional[PersonalizationProfile]:
        """Update personalization profile for a user and chapter."""
        profile = self.get_personalization_profile(db, user_id, chapter_id)
        if not profile:
            return self.create_personalization_profile(db, user_id, chapter_id, personalized_content)

        if personalized_content:
            profile.personalized_content = personalized_content
        profile.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(profile)
        return profile

    def get_all_personalization_profiles(self, db: Session, user_id: UUID) -> list[PersonalizationProfile]:
        """Get all personalization profiles for a user."""
        return db.query(PersonalizationProfile).filter(
            PersonalizationProfile.user_id == user_id
        ).all()