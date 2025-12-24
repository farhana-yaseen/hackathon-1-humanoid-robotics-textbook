"""
Better-Auth Integration component for the humanoid robotics textbook.

This module provides integration between Better-Auth authentication service,
Neon database for user profiles, and Qdrant vector database for personalized content.
"""
import os
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from api.utils.qdrant_client import qdrant, COLLECTION_NAME
from api.utils.gemini_client import embed_text
from api.utils.db import create_user_profile, get_user_profile, update_user_profile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import qdrant_client properly
import qdrant_client.http.models

# Pydantic models for request/response validation
class UserBackground(BaseModel):
    """Model for user background information."""
    software_experience: Optional[str] = None
    hardware_experience: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = 0
    primary_interest: Optional[str] = None
    education_level: Optional[str] = None

class UserSignupWithBackground(BaseModel):
    """Model for user signup requests with background information."""
    email: str
    password: str
    name: str
    background: Optional[UserBackground] = None

class UserUpdateBackground(BaseModel):
    """Model for updating user background information."""
    background: UserBackground

class BetterAuthIntegration:
    """
    Service class for Better-Auth integration with Neon and Qdrant.

    This class handles the integration between Better-Auth authentication service,
    Neon database for user profiles, and Qdrant vector database for personalized content.
    """

    def __init__(self):
        """Initialize the Better-Auth integration service."""
        logger.info("Initializing Better-Auth Integration Service")
        self.qdrant_collection_name = f"{COLLECTION_NAME}_users"
        self._ensure_user_collection_exists()

    def _ensure_user_collection_exists(self):
        """Ensure the user profiles collection exists in Qdrant."""
        try:
            collections = qdrant.get_collections().collections
            if any(c.name == self.qdrant_collection_name for c in collections):
                return

            qdrant.create_collection(
                collection_name=self.qdrant_collection_name,
                vectors_config=qdrant_client.http.models.VectorParams(
                    size=768,   # Google text-embedding-004 embedding size
                    distance=qdrant_client.http.models.Distance.COSINE
                )
            )
            logger.info(f"Created Qdrant collection: {self.qdrant_collection_name}")
        except Exception as e:
            logger.error(f"Error creating user profiles collection: {str(e)}")

    async def store_user_profile_in_db_and_qdrant(self, user_id: str, background: UserBackground) -> bool:
        """
        Store user profile in both Neon database and Qdrant for personalized content retrieval.

        Args:
            user_id: Unique identifier for the user
            background: User background information to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Store in Neon database
            await create_user_profile(
                user_id=user_id,
                software_experience=background.software_experience,
                hardware_experience=background.hardware_experience,
                robotics_experience=background.robotics_experience,
                programming_languages=background.programming_languages,
                hardware_platforms=background.hardware_platforms,
                years_of_experience=background.years_of_experience,
                primary_interest=background.primary_interest,
                education_level=background.education_level
            )

            # Store in Qdrant for vector similarity search
            success = await self.store_user_profile_in_qdrant(user_id, background)
            if not success:
                logger.warning(f"Failed to store user profile in Qdrant for user: {user_id}, but database was updated")
                return False

            logger.info(f"Stored user profile in both Neon and Qdrant for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing user profile in Neon and Qdrant: {str(e)}")
            return False

    async def store_user_profile_in_qdrant(self, user_id: str, background: UserBackground) -> bool:
        """
        Store user profile in Qdrant for personalized content retrieval.

        Args:
            user_id: Unique identifier for the user
            background: User background information to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a text representation of the user's background for embedding
            background_text = f"""
            Software Experience: {background.software_experience or 'Not specified'}
            Hardware Experience: {background.hardware_experience or 'Not specified'}
            Robotics Experience: {background.robotics_experience or 'Not specified'}
            Programming Languages: {', '.join(background.programming_languages or []) or 'Not specified'}
            Hardware Platforms: {', '.join(background.hardware_platforms or []) or 'Not specified'}
            Years of Experience: {background.years_of_experience or 0}
            Primary Interest: {background.primary_interest or 'Not specified'}
            Education Level: {background.education_level or 'Not specified'}
            """

            # Generate embedding for the background text
            embedding = embed_text(background_text)

            # Store in Qdrant
            qdrant.upsert(
                collection_name=self.qdrant_collection_name,
                points=[
                    qdrant_client.http.models.PointStruct(
                        id=user_id,
                        vector=embedding,
                        payload={
                            "user_id": user_id,
                            "background": background.dict(),
                            "created_at": datetime.utcnow().isoformat()
                        },
                    )
                ]
            )

            logger.info(f"Stored user profile in Qdrant for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing user profile in Qdrant: {str(e)}")
            return False

    async def get_user_profile_from_db_and_qdrant(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user profile from both Neon database and Qdrant.

        Args:
            user_id: Unique identifier for the user

        Returns:
            User profile dictionary if found, None otherwise
        """
        try:
            # Get profile from Neon database
            db_profile = await get_user_profile(user_id)
            if db_profile:
                return db_profile

            # If not in database, try Qdrant (for backward compatibility)
            qdrant_profile = await self.get_user_profile_from_qdrant(user_id)
            if qdrant_profile:
                return qdrant_profile

            return None
        except Exception as e:
            logger.error(f"Error retrieving user profile from Neon and Qdrant: {str(e)}")
            return None

    async def get_user_profile_from_qdrant(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user profile from Qdrant.

        Args:
            user_id: Unique identifier for the user

        Returns:
            User profile dictionary if found, None otherwise
        """
        try:
            results = qdrant.retrieve(
                collection_name=self.qdrant_collection_name,
                ids=[user_id]
            )

            if results and len(results) > 0:
                return results[0].payload

            return None
        except Exception as e:
            logger.error(f"Error retrieving user profile from Qdrant: {str(e)}")
            return None

    async def update_user_background(self, user_id: str, background: UserBackground) -> bool:
        """
        Update user background information in both Neon and Qdrant.

        Args:
            user_id: Unique identifier for the user
            background: Updated background information

        Returns:
            True if successful, False otherwise
        """
        try:
            # Update in Neon database
            await update_user_profile(
                user_id=user_id,
                software_experience=background.software_experience,
                hardware_experience=background.hardware_experience,
                robotics_experience=background.robotics_experience,
                programming_languages=background.programming_languages,
                hardware_platforms=background.hardware_platforms,
                years_of_experience=background.years_of_experience,
                primary_interest=background.primary_interest,
                education_level=background.education_level
            )

            # Update in Qdrant
            success = await self.store_user_profile_in_qdrant(user_id, background)
            if not success:
                logger.warning(f"Failed to update user profile in Qdrant for user: {user_id}, but database was updated")
                return False

            logger.info(f"Updated user background for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating user background: {str(e)}")
            return False

# Create router for enhanced auth endpoints
router = APIRouter(prefix="/better-auth", tags=["better-auth"])

# Dependency to get auth service instance
def get_auth_service():
    """Dependency to provide auth service instance."""
    return BetterAuthIntegration()

@router.post("/signup-with-background")
async def signup_with_background(
    user_data: UserSignupWithBackground,
    auth_service: BetterAuthIntegration = Depends(get_auth_service)
):
    """
    Register a new user with background information during signup.

    This endpoint handles the signup process with onboarding questions
    and stores user profiles for personalization.

    Args:
        user_data: UserSignupWithBackground model containing user information
        auth_service: Auth service instance (injected)

    Returns:
        Dictionary containing user ID and success message
    """
    logger.info(f"Processing signup with background for: {user_data.email}")

    try:
        # In a real implementation, this would call the Better-Auth API to create the user
        # For now, we'll simulate the user creation and return a success response
        # The actual Better-Auth service should handle user creation

        # Generate a simple user ID based on email hash (in real implementation, get from Better-Auth)
        user_id = f"user_{abs(hash(user_data.email)) % 1000000}"  # Simple hash for demo

        # Store user background in both Neon and Qdrant for personalization
        if user_data.background:
            success = await auth_service.store_user_profile_in_db_and_qdrant(user_id, user_data.background)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to store user profile")

        return {
            "message": "User registered successfully with background information",
            "user_id": user_id,
            "email": user_data.email
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup with background: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/update-background/{user_id}")
async def update_user_background(
    user_id: str,
    background_data: UserUpdateBackground,
    auth_service: BetterAuthIntegration = Depends(get_auth_service)
):
    """
    Update a user's background information for personalization.

    Args:
        user_id: ID of the user to update
        background_data: UserUpdateBackground model containing new background data
        auth_service: Auth service instance (injected)

    Returns:
        Success message
    """
    logger.info(f"Updating background for user: {user_id}")

    success = await auth_service.update_user_background(user_id, background_data.background)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update user background")

    return {
        "message": "User background updated successfully",
        "user_id": user_id
    }

@router.get("/user-profile/{user_id}")
async def get_user_profile(
    user_id: str,
    auth_service: BetterAuthIntegration = Depends(get_auth_service)
):
    """
    Retrieve a user's profile information from Qdrant.

    Args:
        user_id: ID of the user to retrieve profile for
        auth_service: Auth service instance (injected)

    Returns:
        Dictionary containing user's profile information
    """
    logger.info(f"Retrieving profile for user: {user_id}")

    profile = await auth_service.get_user_profile_from_qdrant(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return profile

@router.get("/health")
async def auth_health_check():
    """
    Health check endpoint for the enhanced authentication service.

    Returns the status of the authentication service.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "Better-Auth Integration",
        "message": "Better-Auth integration service is running and ready to process requests"
    }

# Export the service and router for use in other modules
__all__ = ["BetterAuthIntegration", "router", "UserBackground", "UserSignupWithBackground"]