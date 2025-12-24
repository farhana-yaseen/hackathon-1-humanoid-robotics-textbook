"""
User Profile Service for Better-Auth feature
"""
from typing import Optional, List
from datetime import datetime
from ..utils.db import create_user_profile, get_user_profile, update_user_profile
from .user_profile_model import UserProfile, UserProfileCreate, UserProfileUpdate, EducationLevel


class UserProfileService:
    def __init__(self):
        pass

    async def create_user_profile(self, user_id: str, profile_data: UserProfileCreate) -> Optional[UserProfile]:
        """
        Create a new user profile in the database
        """
        try:
            # Convert our model fields to match the existing db function
            await create_user_profile(
                user_id=user_id,
                software_experience=profile_data.software_background,
                hardware_experience=profile_data.hardware_background,
                robotics_experience=profile_data.robotics_experience,
                programming_languages=profile_data.programming_languages,
                hardware_platforms=profile_data.hardware_platforms,
                years_of_experience=profile_data.years_of_experience,
                primary_interest=profile_data.primary_interest,
                education_level=profile_data.education_level.value if profile_data.education_level else None
            )

            # Return the created profile
            return await self.get_user_profile(user_id)
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user profile by user_id
        """
        try:
            profile_data = await get_user_profile(user_id)
            if profile_data:
                return UserProfile(
                    user_id=profile_data['user_id'],
                    software_background=profile_data['software_experience'],
                    hardware_background=profile_data['hardware_experience'],
                    robotics_experience=profile_data['robotics_experience'],
                    programming_languages=profile_data['programming_languages'],
                    hardware_platforms=profile_data['hardware_platforms'],
                    years_of_experience=profile_data['years_of_experience'],
                    primary_interest=profile_data['primary_interest'],
                    education_level=EducationLevel(profile_data['education_level']) if profile_data['education_level'] else None,
                    created_at=profile_data['created_at'],
                    updated_at=profile_data['updated_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None

    async def update_user_profile(self, user_id: str, profile_data: UserProfileUpdate) -> Optional[UserProfile]:
        """
        Update a user profile by user_id
        """
        try:
            # Prepare update fields, mapping our model fields to existing db function fields
            update_fields = {}

            if profile_data.software_background is not None:
                update_fields['software_experience'] = profile_data.software_background
            if profile_data.hardware_background is not None:
                update_fields['hardware_experience'] = profile_data.hardware_background
            if profile_data.robotics_experience is not None:
                update_fields['robotics_experience'] = profile_data.robotics_experience
            if profile_data.programming_languages is not None:
                update_fields['programming_languages'] = profile_data.programming_languages
            if profile_data.hardware_platforms is not None:
                update_fields['hardware_platforms'] = profile_data.hardware_platforms
            if profile_data.years_of_experience is not None:
                update_fields['years_of_experience'] = profile_data.years_of_experience
            if profile_data.primary_interest is not None:
                update_fields['primary_interest'] = profile_data.primary_interest
            if profile_data.education_level is not None:
                update_fields['education_level'] = profile_data.education_level.value

            # Call the existing update function
            await update_user_profile(user_id, **update_fields)

            # Return the updated profile
            return await self.get_user_profile(user_id)
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return None