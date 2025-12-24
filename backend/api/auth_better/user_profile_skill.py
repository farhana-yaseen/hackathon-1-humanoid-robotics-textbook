"""
createUserProfile Skill for Better-Auth feature
"""
from typing import Dict, Any, Optional
from .user_profile_service import UserProfileService, UserProfileCreate
from .user_profile_model import EducationLevel


async def createUserProfile(user_id: str, **profile_data) -> Dict[str, Any]:
    """
    Save onboarding data into Neon DB and return full profile record.

    Args:
        user_id: The user's unique identifier
        **profile_data: Profile information to save (software_background, hardware_background, etc.)

    Returns:
        Full profile record as a dictionary
    """
    service = UserProfileService()

    # Map the input fields to our model
    user_profile_create = UserProfileCreate(
        user_id=user_id,
        software_background=profile_data.get('software_background'),
        hardware_background=profile_data.get('hardware_background'),
        robotics_experience=profile_data.get('robotics_experience'),
        programming_languages=profile_data.get('programming_languages'),
        hardware_platforms=profile_data.get('hardware_platforms'),
        years_of_experience=profile_data.get('years_of_experience', 0),
        primary_interest=profile_data.get('primary_interest'),
        education_level=EducationLevel(profile_data['education_level']) if profile_data.get('education_level') else None
    )

    profile = await service.create_user_profile(user_id, user_profile_create)

    if profile:
        return {
            "user_id": profile.user_id,
            "software_background": profile.software_background,
            "hardware_background": profile.hardware_background,
            "robotics_experience": profile.robotics_experience,
            "programming_languages": profile.programming_languages,
            "hardware_platforms": profile.hardware_platforms,
            "years_of_experience": profile.years_of_experience,
            "primary_interest": profile.primary_interest,
            "education_level": profile.education_level.value if profile.education_level else None,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
        }

    return {"error": "Failed to create user profile"}


# For backward compatibility and testing
__all__ = ["createUserProfile"]