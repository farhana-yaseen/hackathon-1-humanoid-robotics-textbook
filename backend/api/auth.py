from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import secrets
from api.utils.db import get_db

router = APIRouter()

# User models
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserBackground(BaseModel):
    software_experience: Optional[str] = None
    hardware_experience: Optional[str] = None
    robotics_experience: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    hardware_platforms: Optional[List[str]] = None
    years_of_experience: Optional[int] = 0
    primary_interest: Optional[str] = None
    education_level: Optional[str] = None

class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    background: UserBackground

class UserLogin(BaseModel):
    email: str
    password: str

# In-memory storage for development (use a real database in production)
users_db = {}

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return hashed.hex(), salt

@router.post("/signup")
async def signup(user_data: UserSignup):
    email = user_data.email
    password = user_data.password

    # Check if user already exists
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password, salt = hash_password(password)

    # Create user
    user_id = secrets.token_hex(16)  # Generate unique user ID
    user = {
        "id": user_id,
        "email": email,
        "password_hash": hashed_password,
        "salt": salt,
        "name": user_data.name,
        "background": user_data.background.dict()
    }

    users_db[email] = user

    # In a real implementation, you would store the background info in your database
    # For now, we'll just return success
    return {"message": "User created successfully", "user_id": user_id}

@router.post("/signin")
async def signin(login_data: UserLogin):
    email = login_data.email
    password = login_data.password

    # Check if user exists
    if email not in users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user = users_db[email]

    # Verify password
    hashed_password, _ = hash_password(password, user["salt"])
    if hashed_password != user["password_hash"]:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # In a real implementation, you would generate and return a JWT token
    # For now, we'll just return a mock token
    token = secrets.token_urlsafe(32)

    return {
        "message": "Sign in successful",
        "user_id": user["id"],
        "name": user["name"],
        "token": token
    }

@router.post("/user-background")
async def save_user_background(request_data: dict):
    user_id = request_data.get("user_id")
    background_data = {k: v for k, v in request_data.items() if k != "user_id"}

    # Find user by ID and update background
    user = None
    for u in users_db.values():
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user background with provided data
    if "background" not in user:
        user["background"] = {}
    user["background"].update(background_data)

    return {"message": "Background updated successfully"}

@router.get("/user-background/{user_id}")
async def get_user_background(user_id: str):
    # Find user by ID and return background
    user = None
    for u in users_db.values():
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get("background", {})


@router.get("/get-session")
async def get_session():
    """
    Get current session information.
    For now, returns a default anonymous session.
    In a real implementation, this would validate session tokens.
    """
    # For now, return a default anonymous session
    # In a real implementation, you would validate the session token from headers/cookies
    return {
        "user": None,
        "isAuthenticated": False,
        "sessionId": "anonymous-session",
        "message": "Anonymous session - user not logged in"
    }