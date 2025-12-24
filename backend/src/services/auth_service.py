from sqlalchemy.orm import Session
from ..models.user import User
from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from ..logging_config import get_logger, log_user_action


class AuthService:
    """Service class for handling user authentication and authorization."""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.logger = get_logger('auth')

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        pwd_bytes = password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hash_bytes)

    def create_access_token(self, user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
        """Create an access token for a user."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes

        to_encode = {
            "sub": str(user_id),
            "exp": expire.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[UUID]:
        """Decode an access token to get the user ID."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return UUID(user_id)
        except jwt.exceptions.ExpiredSignatureError:
            return None
        except jwt.exceptions.JWTError:
            return None

    def register_user(self, db: Session, email: str, password: str, name: Optional[str] = None,
                     software_background: Optional[str] = None, hardware_background: Optional[str] = None) -> User:
        """Register a new user with hashed password."""
        self.logger.info(f"Attempting to register user with email: {email}")

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            self.logger.warning(f"Registration attempt for already registered email: {email}")
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = self.hash_password(password)

        # Create the user
        user = User(
            email=email,
            name=name,
            software_background=software_background,
            hardware_background=hardware_background,
            preferences=None  # Will be set separately if needed
        )
        user.hashed_password = hashed_password  # This will be stored separately

        db.add(user)
        db.commit()
        db.refresh(user)

        self.logger.info(f"Successfully registered user with ID: {user.user_id}, email: {email}")
        log_user_action(str(user.user_id), "user_registration", {
            "email": email,
            "name": name,
            "software_background": software_background,
            "hardware_background": hardware_background
        })

        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password."""
        self.logger.info(f"Authentication attempt for email: {email}")

        user = db.query(User).filter(User.email == email).first()
        if not user or not hasattr(user, 'hashed_password') or not self.verify_password(password, user.hashed_password):
            self.logger.warning(f"Failed authentication attempt for email: {email}")
            return None

        self.logger.info(f"Successful authentication for user ID: {user.user_id}, email: {email}")
        log_user_action(str(user.user_id), "user_authentication", {"email": email})

        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        return db.query(User).filter(User.user_id == user_id).first()

    def update_user_profile(self, db: Session, user_id: UUID, **kwargs) -> Optional[User]:
        """Update user profile information."""
        self.logger.info(f"Updating profile for user ID: {user_id}")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            self.logger.warning(f"Attempt to update non-existent user ID: {user_id}")
            return None

        # Update allowed fields
        allowed_fields = {
            'name', 'software_background', 'hardware_background', 'preferences', 'is_active'
        }

        # Track which fields are being updated
        updated_fields = {}
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(user, field):
                old_value = getattr(user, field)
                setattr(user, field, value)
                updated_fields[field] = {"old": old_value, "new": value}

        user.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(user)

        self.logger.info(f"Successfully updated profile for user ID: {user_id}")
        log_user_action(str(user_id), "profile_update", {"updated_fields": list(updated_fields.keys()), "changes": updated_fields})

        return user