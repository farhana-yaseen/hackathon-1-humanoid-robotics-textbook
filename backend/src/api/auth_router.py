"""
Auth router for the Humanoid Robotics Textbook application.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta
from ..services.auth_service import AuthService
from ..services.profile_service import ProfileService
from ..database import get_db
from ..models.user import User


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# JWT token dependency
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """
    Get current user from JWT token.
    This is a placeholder implementation - in production, you'd use Better-Auth middleware
    """
    token = credentials.credentials
    auth_service = AuthService()
    user_id = auth_service.decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.user_id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# Create the auth router
auth_router = APIRouter()


# Request models
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    name: str
    software_background: str  # Required field
    hardware_background: str  # Required field


class UserProfileUpdateRequest(BaseModel):
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    preferences: Optional[dict] = None


# Response models
class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    created_at: str
    updated_at: str
    preferences: Optional[dict] = None

    class Config:
        from_attributes = True


@auth_router.post("/register", response_model=UserResponse)
async def register_user(request: UserRegistrationRequest, db: Session = Depends(get_db)):
    """
    Register a new user with background information.
    """
    # Validate that background fields are not empty
    if not request.software_background.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Software background is required"
        )

    if not request.hardware_background.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware background is required"
        )

    # Use AuthService to register the user
    auth_service = AuthService()
    try:
        user = auth_service.register_user(
            db=db,
            email=request.email,
            password="default_password",  # Better-Auth will handle password management
            name=request.name,
            software_background=request.software_background,
            hardware_background=request.hardware_background
        )

        # Return the user data (excluding password for security)
        return UserResponse(
            user_id=str(user.user_id),
            email=user.email,
            name=user.name,
            software_background=user.software_background,
            hardware_background=user.hardware_background,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None,
            preferences=user.preferences
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


@auth_router.post("/login")
async def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Login a user and return JWT token.
    """
    auth_service = AuthService()
    user = auth_service.authenticate_user(db, request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = auth_service.create_access_token(user.user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.user_id),
        "email": user.email
    }


@auth_router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's profile.
    """
    # Return the current user's profile
    return UserResponse(
        user_id=str(current_user.user_id),
        email=current_user.email,
        name=current_user.name,
        software_background=current_user.software_background,
        hardware_background=current_user.hardware_background,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
        updated_at=current_user.updated_at.isoformat() if current_user.updated_at else None,
        preferences=current_user.preferences
    )


@auth_router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    request: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the authenticated user's profile.
    """
    profile_service = ProfileService()

    # Update user backgrounds
    updated_user = profile_service.update_user_backgrounds(
        db,
        current_user.user_id,
        software_background=request.software_background,
        hardware_background=request.hardware_background
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        user_id=str(updated_user.user_id),
        email=updated_user.email,
        name=updated_user.name,
        software_background=updated_user.software_background,
        hardware_background=updated_user.hardware_background,
        created_at=updated_user.created_at.isoformat() if updated_user.created_at else None,
        updated_at=updated_user.updated_at.isoformat() if updated_user.updated_at else None,
        preferences=updated_user.preferences
    )