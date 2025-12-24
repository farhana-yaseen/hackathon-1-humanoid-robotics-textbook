"""
Better-Auth Router for the humanoid robotics textbook.
This module provides API endpoints for Better-Auth integration.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging
from ..utils.db import get_db
from .user_profile_service import UserProfileService, UserProfileCreate
from .vector_sync_service import VectorSyncService
from .user_profile_model import UserProfile, UserProfileUpdate
from .rate_limiter import rate_limiter
from .session_manager import session_manager
from .logging_config import auth_logger
from .auth_service_client import auth_service_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = 0
    primary_interest: Optional[str] = None
    education_level: Optional[str] = None


class UserSignin(BaseModel):
    email: str
    password: str


class VerifySessionRequest(BaseModel):
    token: str


class CreateProfileRequest(BaseModel):
    user_id: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = 0
    primary_interest: Optional[str] = None
    education_level: Optional[str] = None


class SyncVectorRequest(BaseModel):
    user_id: str


# Create router for Better-Auth endpoints
router = APIRouter(prefix="/auth", tags=["better-auth"])

# Dependency to get services
def get_user_profile_service():
    return UserProfileService()


def get_vector_sync_service():
    return VectorSyncService()


@router.post("/signup")
async def signup(
    request: Request,
    user_data: UserSignup,
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
    vector_sync_service: VectorSyncService = Depends(get_vector_sync_service)
):
    """
    Register a new user with Better-Auth and create their profile.

    Args:
        request: FastAPI request object to get client IP for rate limiting
        user_data: UserSignup model containing registration information and profile data
        user_profile_service: UserProfileService instance (injected)
        vector_sync_service: VectorSyncService instance (injected)

    Returns:
        Dictionary containing user ID and success message
    """
    # Get client IP for rate limiting
    client_ip = request.client.host if request.client else "unknown"

    # Check rate limit
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many signup attempts. Please try again later."
        )

    logger.info(f"Processing signup request for: {user_data.email} from IP: {client_ip}")

    try:
        # Prepare background data for the auth service
        background_data = {
            "softwareExperience": user_data.software_background,
            "hardwareExperience": user_data.hardware_background,
            "roboticsExperience": user_data.robotics_experience,
            "programmingLanguages": user_data.programming_languages,
            "hardwarePlatforms": user_data.hardware_platforms,
            "yearsOfExperience": user_data.years_of_experience,
            "primaryInterest": user_data.primary_interest,
            "educationLevel": user_data.education_level
        }

        # Call the Better Auth service to create the user
        auth_response = await auth_service_client.signup(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            background_data=background_data
        )

        if not auth_response.success:
            raise HTTPException(
                status_code=400,
                detail=auth_response.error or "Signup failed"
            )

        user_id = auth_response.user_id

        # Log the signup event
        auth_logger.log_auth_event(
            event_type="signup",
            user_id=user_id,
            details={"email": user_data.email, "ip": client_ip}
        )

        # Create user profile with onboarding data if provided in our local database
        if (user_data.software_background or user_data.hardware_background or
            user_data.robotics_experience or user_data.programming_languages or
            user_data.hardware_platforms or user_data.primary_interest):

            profile_data = UserProfileCreate(
                user_id=user_id,
                software_background=user_data.software_background,
                hardware_background=user_data.hardware_background,
                robotics_experience=user_data.robotics_experience,
                programming_languages=user_data.programming_languages,
                hardware_platforms=user_data.hardware_platforms,
                years_of_experience=user_data.years_of_experience,
                primary_interest=user_data.primary_interest,
                education_level=user_data.education_level
            )

            profile = await user_profile_service.create_user_profile(user_id, profile_data)

            if profile:
                # Sync user attributes to Qdrant for personalization
                profile_dict = {
                    'software_background': profile.software_background,
                    'hardware_background': profile.hardware_background,
                    'robotics_experience': profile.robotics_experience,
                    'programming_languages': profile.programming_languages,
                    'hardware_platforms': profile.hardware_platforms,
                    'years_of_experience': profile.years_of_experience,
                    'primary_interest': profile.primary_interest,
                    'education_level': profile.education_level.value if profile.education_level else None,
                    'created_at': profile.created_at.isoformat() if profile.created_at else None,
                    'updated_at': profile.updated_at.isoformat() if profile.updated_at else None
                }

                success = await vector_sync_service.sync_user_profile_to_vector_db(user_id, profile_dict)
                if not success:
                    logger.warning(f"Failed to sync user profile to vector DB for user: {user_id}")

        return {
            "message": auth_response.message,
            "user_id": user_id,
            "email": user_data.email
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        # Log the error
        auth_logger.log_auth_error(
            event_type="signup",
            user_id="unknown",
            error=str(e),
            details={"email": user_data.email, "ip": client_ip}
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/signin")
async def signin(
    request: Request,
    response: Response,
    login_data: UserSignin
):
    """
    Authenticate a user with Better-Auth.

    Args:
        request: FastAPI request object to get client IP for rate limiting
        response: FastAPI response object to set cookies
        login_data: UserSignin model containing email and password

    Returns:
        Dictionary containing user info
    """
    # Get client IP for rate limiting
    client_ip = request.client.host if request.client else "unknown"

    # Check rate limit
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many signin attempts. Please try again later."
        )

    logger.info(f"Processing sign in request for: {login_data.email} from IP: {client_ip}")

    try:
        # Call the Better Auth service to authenticate the user
        auth_response = await auth_service_client.signin(
            email=login_data.email,
            password=login_data.password
        )

        if not auth_response.success:
            raise HTTPException(
                status_code=401,
                detail=auth_response.error or "Invalid credentials"
            )

        user_id = auth_response.user_id

        # Log the signin event
        auth_logger.log_auth_event(
            event_type="signin",
            user_id=user_id,
            details={"email": login_data.email, "ip": client_ip}
        )

        # Create tokens
        access_token_data = {"user_id": user_id, "email": login_data.email}
        access_token = session_manager.create_access_token(access_token_data)
        refresh_token = session_manager.create_refresh_token(access_token_data)

        # Set HTTP-only cookies
        session_manager.set_auth_cookies(response, access_token, refresh_token)

        return {
            "message": auth_response.message,
            "user_id": user_id,
            "name": login_data.email.split('@')[0],  # Use part of email as name
            "email": login_data.email
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signin: {str(e)}")
        # Log the error
        auth_logger.log_auth_error(
            event_type="signin",
            user_id="unknown",
            error=str(e),
            details={"email": login_data.email, "ip": client_ip}
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/verify-session")
async def verify_session(
    request_data: VerifySessionRequest
):
    """
    Public endpoint to verify Better-Auth session token, returns basic validity info.

    Args:
        request_data: VerifySessionRequest model containing token

    Returns:
        Dictionary containing session validity info
    """
    # In a real implementation, this would call the Better-Auth API to verify the token
    # For now, we'll simulate the verification and return basic validity info
    # The actual Better-Auth service should handle token verification

    # This is a simplified verification - in reality, you'd validate the JWT token
    is_valid = len(request_data.token) > 10  # Basic check for demo purposes

    if is_valid:
        # Extract user info from token in real implementation
        return {
            "valid": True,
            "user_id": "user_123456",  # Would extract from token in real implementation
            "email": "user@example.com"  # Would extract from token in real implementation
        }
    else:
        return {
            "valid": False
        }


@router.post("/signout")
async def signout(
    request: Request,
    response: Response
):
    """
    Sign out the user by clearing auth cookies.

    Args:
        request: FastAPI request object to get client IP
        response: FastAPI response object to clear cookies

    Returns:
        Success message
    """
    # Clear auth cookies
    session_manager.clear_auth_cookies(response)

    # Get client IP for logging
    client_ip = request.client.host if request.client else "unknown"

    # Log the signout event
    auth_logger.log_auth_event(
        event_type="signout",
        user_id="unknown",  # In a real implementation, we'd extract user ID from the token
        details={"ip": client_ip}
    )

    return {
        "message": "Sign out successful"
    }


@router.post("/create-profile")
async def create_profile(
    request_data: CreateProfileRequest,
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
    vector_sync_service: VectorSyncService = Depends(get_vector_sync_service)
):
    """
    Create user profile with onboarding information.

    Args:
        request_data: CreateProfileRequest model containing user profile data
        user_profile_service: UserProfileService instance (injected)
        vector_sync_service: VectorSyncService instance (injected)

    Returns:
        Success message
    """
    logger.info(f"Creating profile for user: {request_data.user_id}")

    try:
        # First, update the user profile in the Better Auth service
        background_data = {
            "softwareExperience": request_data.software_background,
            "hardwareExperience": request_data.hardware_background,
            "roboticsExperience": request_data.robotics_experience,
            "programmingLanguages": request_data.programming_languages,
            "hardwarePlatforms": request_data.hardware_platforms,
            "yearsOfExperience": request_data.years_of_experience,
            "primaryInterest": request_data.primary_interest,
            "educationLevel": request_data.education_level
        }

        auth_response = await auth_service_client.update_user_background(
            user_id=request_data.user_id,
            background_data=background_data
        )

        if not auth_response.success:
            logger.warning(f"Failed to update background in auth service: {auth_response.error}")

        # Create/update the user profile in our local database
        profile_data = UserProfileCreate(
            user_id=request_data.user_id,
            software_background=request_data.software_background,
            hardware_background=request_data.hardware_background,
            robotics_experience=request_data.robotics_experience,
            programming_languages=request_data.programming_languages,
            hardware_platforms=request_data.hardware_platforms,
            years_of_experience=request_data.years_of_experience,
            primary_interest=request_data.primary_interest,
            education_level=request_data.education_level
        )

        profile = await user_profile_service.create_user_profile(request_data.user_id, profile_data)

        if profile:
            # Log the profile creation event
            auth_logger.log_profile_event(
                event_type="create",
                user_id=request_data.user_id,
                details={
                    "software_background": profile.software_background,
                    "hardware_background": profile.hardware_background,
                    "robotics_experience": profile.robotics_experience
                }
            )

            # Sync user attributes to Qdrant for personalization
            profile_dict = {
                'software_background': profile.software_background,
                'hardware_background': profile.hardware_background,
                'robotics_experience': profile.robotics_experience,
                'programming_languages': profile.programming_languages,
                'hardware_platforms': profile.hardware_platforms,
                'years_of_experience': profile.years_of_experience,
                'primary_interest': profile.primary_interest,
                'education_level': profile.education_level.value if profile.education_level else None,
                'created_at': profile.created_at.isoformat() if profile.created_at else None,
                'updated_at': profile.updated_at.isoformat() if profile.updated_at else None
            }

            success = await vector_sync_service.sync_user_profile_to_vector_db(request_data.user_id, profile_dict)
            if not success:
                logger.warning(f"Failed to sync user profile to vector DB for user: {request_data.user_id}")

        return {
            "message": "Profile created successfully",
            "user_id": request_data.user_id
        }
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        # Log the error
        auth_logger.log_auth_error(
            event_type="create_profile",
            user_id=request_data.user_id,
            error=str(e),
            details={
                "software_background": request_data.software_background,
                "hardware_background": request_data.hardware_background
            }
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/sync-vector")
async def sync_vector(
    request_data: SyncVectorRequest,
    user_profile_service: UserProfileService = Depends(get_user_profile_service),
    vector_sync_service: VectorSyncService = Depends(get_vector_sync_service)
):
    """
    Initiate async vector synchronization for user profile.

    Args:
        request_data: SyncVectorRequest model containing user ID
        user_profile_service: UserProfileService instance (injected)
        vector_sync_service: VectorSyncService instance (injected)

    Returns:
        Success message with status
    """
    logger.info(f"Syncing vector for user: {request_data.user_id}")

    try:
        # Get the user profile to sync
        profile = await user_profile_service.get_user_profile(request_data.user_id)

        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        # Convert profile to dictionary
        profile_dict = {
            'software_background': profile.software_background,
            'hardware_background': profile.hardware_background,
            'robotics_experience': profile.robotics_experience,
            'programming_languages': profile.programming_languages,
            'hardware_platforms': profile.hardware_platforms,
            'years_of_experience': profile.years_of_experience,
            'primary_interest': profile.primary_interest,
            'education_level': profile.education_level.value if profile.education_level else None,
            'created_at': profile.created_at.isoformat() if profile.created_at else None,
            'updated_at': profile.updated_at.isoformat() if profile.updated_at else None
        }

        success = await vector_sync_service.sync_user_profile_to_vector_db(request_data.user_id, profile_dict)

        if success:
            return {
                "message": "Vector sync initiated successfully",
                "status": "success"
            }
        else:
            return {
                "message": "Vector sync failed",
                "status": "error"
            }
    except Exception as e:
        logger.error(f"Error syncing vector: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def auth_health_check():
    """
    Health check endpoint for the Better-Auth integration service.

    Returns the status of the authentication service.
    """
    return {
        "status": "healthy",
        "service": "Better-Auth Integration",
        "message": "Better-Auth integration service is running and ready to process requests"
    }


# Export the router for use in other modules
__all__ = ["router"]