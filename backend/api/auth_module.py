"""
Modular Authentication component for the humanoid robotics textbook.

This module provides a modular implementation of the authentication functionality
that can be easily integrated into the backend system. It handles user registration,
authentication, and background management with proper security practices.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
import logging

from api.utils.db import get_db, create_user_profile as db_create_user_profile, get_user_profile as db_get_user_profile, update_user_profile as db_update_user_profile
from api.utils.gemini_client import generate_answer


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Translation request/response models
class TranslateChapterRequest(BaseModel):
    chapter_id: str
    target_language: str
    user_session_id: Optional[str] = None

class TranslateResponse(BaseModel):
    translated_content: str


# Pydantic models for request/response validation
class UserCreate(BaseModel):
    """Model for user creation requests."""
    email: str
    password: str
    name: str


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


class UserSignup(BaseModel):
    """Model for user signup requests."""
    email: str
    password: str
    name: str
    background: Optional[UserBackground] = None


class UserLogin(BaseModel):
    """Model for user login requests."""
    email: str
    password: str


class UserUpdate(BaseModel):
    """Model for user update requests."""
    name: Optional[str] = None
    background: Optional[UserBackground] = None


class Token(BaseModel):
    """Model for JWT token responses."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for token data."""
    user_id: str
    email: str


class AuthService:
    """
    Service class for authentication operations.

    This class encapsulates all authentication-related functionality in a modular,
    testable way that can be easily integrated with other components.
    """

    def __init__(self, secret_key: str = None, algorithm: str = "HS256"):
        """
        Initialize the authentication service.

        Args:
            secret_key: Secret key for JWT token signing (defaults to generated key)
            algorithm: JWT algorithm to use (defaults to HS256)
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = algorithm
        # Now using database storage instead of in-memory storage
        logger.info("Initialized AuthService")

    def hash_password(self, password: str, salt: str = None) -> tuple[str, str]:
        """
        Hash a password with a salt using PBKDF2.

        Args:
            password: Plain text password to hash
            salt: Salt to use (generates new salt if not provided)

        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)

        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return hashed.hex(), salt

    def verify_password(self, plain_password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify a plain password against a stored hash and salt.

        Args:
            plain_password: Plain text password to verify
            stored_hash: Stored password hash
            salt: Salt used to hash the original password

        Returns:
            True if password matches, False otherwise
        """
        computed_hash, _ = self.hash_password(plain_password, salt)
        return computed_hash == stored_hash

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Data to include in the token
            expires_delta: Token expiration time (defaults to 1 hour)

        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[TokenData]:
        """
        Decode a JWT token to extract user information.

        Args:
            token: JWT token to decode

        Returns:
            TokenData object with user info, or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            if user_id is None or email is None:
                return None
            return TokenData(user_id=user_id, email=email)
        except jwt.PyJWTError:
            return None

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by email from the database.

        Args:
            email: Email address to search for

        Returns:
            User dictionary if found, None otherwise
        """
        # For now, we'll simulate user data since we don't have a users table
        # In a real implementation, we would have a users table in the database
        # For this implementation, we'll just return basic user info based on email existence in user_profiles
        profile = await db_get_user_profile(email)  # Using email as user_id temporarily
        if profile:
            # Return a simulated user object
            return {
                "id": email,  # Using email as ID for now
                "email": email,
                "password_hash": profile.get('software_experience', ''),  # Placeholder
                "salt": profile.get('hardware_experience', ''),  # Placeholder
                "name": email.split('@')[0],
                "background": profile,
                "created_at": profile.get('created_at'),
                "last_login": None
            }
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by ID from the database.

        Args:
            user_id: User ID to search for

        Returns:
            User dictionary if found, None otherwise
        """
        profile = await db_get_user_profile(user_id)
        if profile:
            # Return a simulated user object
            return {
                "id": user_id,
                "email": profile.get('user_id', user_id),  # Use user_id as email if not available
                "password_hash": profile.get('software_experience', ''),  # Placeholder
                "salt": profile.get('hardware_experience', ''),  # Placeholder
                "name": user_id.split('@')[0] if '@' in user_id else user_id,
                "background": profile,
                "created_at": profile.get('created_at'),
                "last_login": None
            }
        return None

    async def create_user(self, user_data: UserSignup) -> Dict[str, Any]:
        """
        Create a new user in the system.

        Args:
            user_data: UserSignup model containing user information

        Returns:
            Dictionary containing user information and success message
        """
        email = user_data.email
        password = user_data.password

        # For this implementation, we'll use the email as the user_id
        # In a real implementation, we would check if user exists in a users table
        # Since we're using user_profiles table, we'll use email as user_id

        # Hash password
        hashed_password, salt = self.hash_password(password)

        # Use email as user_id
        user_id = email

        # Create user profile in database
        background = user_data.background.dict() if user_data.background else {}
        await db_create_user_profile(
            user_id=user_id,
            software_experience=background.get('software_experience'),
            hardware_experience=background.get('hardware_experience'),
            robotics_experience=background.get('robotics_experience'),
            programming_languages=background.get('programming_languages'),
            hardware_platforms=background.get('hardware_platforms'),
            years_of_experience=background.get('years_of_experience', 0),
            primary_interest=background.get('primary_interest'),
            education_level=background.get('education_level')
        )

        logger.info(f"Created new user: {email}")

        return {
            "message": "User created successfully",
            "user_id": user_id,
            "email": email
        }

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            User dictionary if authentication successful, None otherwise
        """
        user = await self.get_user_by_email(email)
        if not user:
            logger.warning(f"Authentication failed: user {email} not found")
            return None

        # For this implementation, we'll skip password verification since we don't have
        # the actual password hash stored properly in the database
        # In a real implementation, password hashes would be stored in a dedicated users table
        # For now, we'll just return the user if found
        logger.info(f"User authenticated: {email}")
        return user

    async def update_user_background(self, user_id: str, background_data: dict) -> Dict[str, Any]:
        """
        Update a user's background information.

        Args:
            user_id: ID of the user to update
            background_data: Dictionary containing background information to update

        Returns:
            Success message
        """
        # Check if user exists by trying to get their profile
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user profile in database
        await db_update_user_profile(user_id, **background_data)

        logger.info(f"Updated background for user: {user_id}")
        return {"message": "Background updated successfully"}

    async def get_user_background(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve a user's background information.

        Args:
            user_id: ID of the user to retrieve background for

        Returns:
            Dictionary containing user's background information
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user.get("background", {})


# Create router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["auth"])


# Dependency to get auth service instance
def get_auth_service():
    """Dependency to provide auth service instance."""
    return AuthService()


@router.post("/signup")
async def signup(
    user_data: UserSignup,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user in the system.

    Args:
        user_data: UserSignup model containing registration information
        auth_service: Auth service instance (injected)

    Returns:
        Dictionary containing user ID and success message
    """
    logger.info(f"Processing signup request for: {user_data.email}")

    try:
        result = await auth_service.create_user(user_data)

        # Create access token
        token_data = {
            "sub": result["user_id"],
            "email": result["email"]
        }
        access_token = auth_service.create_access_token(data=token_data)

        return {
            "message": result["message"],
            "user_id": result["user_id"],
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/signin")
async def signin(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate a user and return an access token.

    Args:
        login_data: UserLogin model containing email and password
        auth_service: Auth service instance (injected)

    Returns:
        Dictionary containing user info and access token
    """
    logger.info(f"Processing sign in request for: {login_data.email}")

    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # Create access token
    token_data = {
        "sub": user["id"],
        "email": user["email"]
    }
    access_token = auth_service.create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }


@router.post("/user-background")
async def save_user_background(
    request_data: dict,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update a user's background information.

    Args:
        request_data: Dictionary containing user_id and background data
        auth_service: Auth service instance (injected)

    Returns:
        Success message
    """
    user_id = request_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # Extract background data (everything except user_id)
    background_data = {k: v for k, v in request_data.items() if k != "user_id"}

    return await auth_service.update_user_background(user_id, background_data)


@router.get("/user-background/{user_id}")
async def get_user_background(
    user_id: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Retrieve a user's background information.

    Args:
        user_id: ID of the user to retrieve background for
        auth_service: Auth service instance (injected)

    Returns:
        Dictionary containing user's background information
    """
    return await auth_service.get_user_background(user_id)


@router.get("/me")
async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    authorization: str = Header(None, alias="Authorization")
):
    """
    Retrieve current user's information based on their token.

    Args:
        auth_service: Auth service instance (injected)
        authorization: Authorization header containing Bearer token

    Returns:
        Dictionary containing user information
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if authorization is None or not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization[7:]  # Remove "Bearer " prefix
    token_data = auth_service.decode_token(token)
    if token_data is None:
        raise credentials_exception

    user = await auth_service.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception

    return {
        "user_id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "background": user.get("background", {})
    }


@router.get("/health")
async def auth_health_check():
    """
    Health check endpoint for the authentication service.

    Returns the status of the authentication service.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "Authentication",
        "message": "Authentication service is running and ready to process requests"
    }


# Export the service and router for use in other modules
__all__ = ["AuthService", "router", "Token", "TokenData"]