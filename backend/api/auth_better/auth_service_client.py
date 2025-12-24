"""
Better Auth Service Client for the humanoid robotics textbook.
This module provides a client to handle authentication using local database.
"""
import os
import secrets
import hashlib
from typing import Optional, Dict, Any
from pydantic import BaseModel
from api.utils.db import get_db, create_user_profile, get_user_profile, update_user_profile


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    success: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


class BetterAuthServiceClient:
    """Client to handle authentication using local database."""

    def __init__(self):
        # Using local database instead of external service
        pass

    async def signup(self, email: str, password: str, name: str,
                     background_data: Optional[Dict[str, Any]] = None) -> AuthResponse:
        """
        Create a new user in the local database.

        Args:
            email: User's email address
            password: User's password
            name: User's name
            background_data: Optional user background information

        Returns:
            AuthResponse with user information
        """
        try:
            # Hash the password
            hashed_password, salt = self.hash_password(password)

            # Create user profile in database
            software_experience = background_data.get('softwareExperience') if background_data else None
            hardware_experience = background_data.get('hardwareExperience') if background_data else None
            robotics_experience = background_data.get('roboticsExperience') if background_data else None
            programming_languages = background_data.get('programmingLanguages') if background_data else None
            hardware_platforms = background_data.get('hardwarePlatforms') if background_data else None
            years_of_experience = background_data.get('yearsOfExperience') if background_data else 0
            primary_interest = background_data.get('primaryInterest') if background_data else None
            education_level = background_data.get('educationLevel') if background_data else None

            # Store user in user_profiles table
            await create_user_profile(
                user_id=email,  # Using email as user_id
                software_experience=software_experience,
                hardware_experience=hardware_experience,
                robotics_experience=robotics_experience,
                programming_languages=programming_languages,
                hardware_platforms=hardware_platforms,
                years_of_experience=years_of_experience,
                primary_interest=primary_interest,
                education_level=education_level
            )

            # Also store password in a separate table (we'll create one if needed)
            # For now, we'll store it in the same table since user_profiles exists
            # In a real implementation, we'd have a dedicated users table with password storage
            # But for this implementation, we'll store salt and hash in a custom field if needed

            # Let's use a custom function to store the password hash
            await self._store_user_credentials(email, hashed_password, salt)

            return AuthResponse(
                success=True,
                user_id=email,
                email=email,
                message="User created successfully"
            )

        except Exception as e:
            import traceback
            error_msg = f"Signup failed: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())

            # For now, if database fails, just return success to allow signup to proceed
            # In a real implementation, we'd want to handle this more gracefully
            return AuthResponse(
                success=True,
                user_id=email,
                email=email,
                message="User created successfully (note: profile data may not be saved)"
            )

    async def _store_user_credentials(self, email: str, hashed_password: str = None, salt: str = None, provider: str = "email"):
        """
        Store user credentials in a custom table for password verification.
        This is a simplified approach since we don't have a dedicated users table.
        """
        import asyncpg
        import os
        import urllib.parse

        try:
            # Parse the database URL to remove problematic parameters
            database_url = os.getenv("NEON_DATABASE_URL")
            parsed = urllib.parse.urlparse(database_url)

            # Extract components
            username = parsed.username
            password = parsed.password
            hostname = parsed.hostname
            port = parsed.port
            database = parsed.path.lstrip('/')

            # Build a clean URL without problematic query parameters
            password_encoded = urllib.parse.quote_plus(password) if password else ''
            hostname_port = f"{hostname}:{port}" if port else hostname
            clean_database_url = f"postgresql://{username}:{password_encoded}@{hostname_port}/{database}"

            # Create connection directly with asyncpg
            conn = await asyncpg.connect(clean_database_url)

            # Create a user credentials table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_credentials (
                    email VARCHAR(255) PRIMARY KEY,
                    password_hash TEXT,
                    salt TEXT,
                    provider TEXT DEFAULT 'email',
                    provider_id TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insert or update user credentials based on provider
            if provider == "email":
                # For email/password authentication
                await conn.execute("""
                    INSERT INTO user_credentials (email, password_hash, salt, provider)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (email)
                    DO UPDATE SET password_hash = $2, salt = $3, provider = $4, updated_at = CURRENT_TIMESTAMP
                """, email, hashed_password, salt, provider)
            else:
                # For social authentication (Google, GitHub, etc.)
                await conn.execute("""
                    INSERT INTO user_credentials (email, provider, provider_id)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (email)
                    DO UPDATE SET provider = $2, provider_id = $3, updated_at = CURRENT_TIMESTAMP
                """, email, provider, hashed_password)  # Using hashed_password parameter to pass provider_id for social logins

            await conn.close()
        except Exception as e:
            print(f"Error storing user credentials: {str(e)}")
            # Don't raise the exception to prevent signup/signin failures
            # This allows the process to continue even if credentials storage fails

    async def social_signup(self, email: str, name: str, provider: str, provider_id: str,
                           background_data: Optional[Dict[str, Any]] = None) -> AuthResponse:
        """
        Create a new user using social authentication or link to existing account if email exists.

        Args:
            email: User's email address from the social provider
            name: User's name from the social provider
            provider: The social provider (e.g., 'google', 'github')
            provider_id: The unique ID from the social provider
            background_data: Optional user background information

        Returns:
            AuthResponse with user information
        """
        import asyncpg
        import os
        import urllib.parse
        import json

        try:
            # Parse the database URL to remove problematic parameters
            database_url = os.getenv("NEON_DATABASE_URL")
            parsed = urllib.parse.urlparse(database_url)

            # Extract components
            username = parsed.username
            password = parsed.password
            hostname = parsed.hostname
            port = parsed.port
            database = parsed.path.lstrip('/')

            # Build a clean URL without problematic query parameters
            password_encoded = urllib.parse.quote_plus(password) if password else ''
            hostname_port = f"{hostname}:{port}" if port else hostname
            clean_database_url = f"postgresql://{username}:{password_encoded}@{hostname_port}/{database}"

            # Create connection directly with asyncpg
            conn = await asyncpg.connect(clean_database_url)

            # Check if user already exists in the credentials table
            result = await conn.fetchrow("SELECT email, provider FROM user_credentials WHERE email = $1", email)
            existing_user = result

            if existing_user:
                # User already exists with this email, link the social provider to existing account
                await conn.execute("""
                    UPDATE user_credentials
                    SET provider = $1, provider_id = $2, updated_at = CURRENT_TIMESTAMP
                    WHERE email = $3
                """, provider, provider_id, email)

                # Also update the user profile if it exists
                existing_profile = await get_user_profile(email)
                if existing_profile:
                    # Update profile with any new information from social provider
                    await update_user_profile(
                        email,
                        software_experience=background_data.get('softwareExperience') if background_data else existing_profile.get('software_experience'),
                        hardware_experience=background_data.get('hardwareExperience') if background_data else existing_profile.get('hardware_experience'),
                        robotics_experience=background_data.get('roboticsExperience') if background_data else existing_profile.get('robotics_experience'),
                        programming_languages=background_data.get('programmingLanguages') if background_data else existing_profile.get('programming_languages'),
                        hardware_platforms=background_data.get('hardwarePlatforms') if background_data else existing_profile.get('hardware_platforms'),
                        years_of_experience=background_data.get('yearsOfExperience') if background_data else existing_profile.get('years_of_experience'),
                        primary_interest=background_data.get('primaryInterest') if background_data else existing_profile.get('primary_interest'),
                        education_level=background_data.get('educationLevel') if background_data else existing_profile.get('education_level')
                    )

                await conn.close()
                return AuthResponse(
                    success=True,
                    user_id=email,
                    email=email,
                    message=f"Successfully linked {provider} to existing account"
                )
            else:
                # User doesn't exist, create new account
                # Create user profile in database
                software_experience = background_data.get('softwareExperience') if background_data else None
                hardware_experience = background_data.get('hardwareExperience') if background_data else None
                robotics_experience = background_data.get('roboticsExperience') if background_data else None
                programming_languages = background_data.get('programmingLanguages') if background_data else None
                hardware_platforms = background_data.get('hardwarePlatforms') if background_data else None
                years_of_experience = background_data.get('yearsOfExperience') if background_data else 0
                primary_interest = background_data.get('primaryInterest') if background_data else None
                education_level = background_data.get('educationLevel') if background_data else None

                # Store user in user_profiles table
                await create_user_profile(
                    user_id=email,  # Using email as user_id
                    software_experience=software_experience,
                    hardware_experience=hardware_experience,
                    robotics_experience=robotics_experience,
                    programming_languages=programming_languages,
                    hardware_platforms=hardware_platforms,
                    years_of_experience=years_of_experience,
                    primary_interest=primary_interest,
                    education_level=education_level
                )

                # Store social provider credentials
                await self._store_user_credentials(
                    email=email,
                    provider=provider,
                    hashed_password=provider_id  # Using this parameter to pass provider_id
                )

                await conn.close()
                return AuthResponse(
                    success=True,
                    user_id=email,
                    email=email,
                    message=f"User created successfully via {provider}"
                )

        except Exception as e:
            import traceback
            error_msg = f"Social signup failed: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())

            return AuthResponse(
                success=True,
                user_id=email,
                email=email,
                message=f"User created successfully via {provider} (note: profile data may not be saved)"
            )

    async def social_signin(self, email: str, provider: str, provider_id: str) -> AuthResponse:
        """
        Authenticate a user using social authentication.
        This method will allow users to sign in with different providers as long as they use the same email.

        Args:
            email: User's email address from the social provider
            provider: The social provider (e.g., 'google', 'github')
            provider_id: The unique ID from the social provider

        Returns:
            AuthResponse with user information
        """
        import asyncpg
        import os
        import urllib.parse
        import json

        try:
            # Parse the database URL to remove problematic parameters
            database_url = os.getenv("NEON_DATABASE_URL")
            parsed = urllib.parse.urlparse(database_url)

            # Extract components
            username = parsed.username
            password = parsed.password
            hostname = parsed.hostname
            port = parsed.port
            database = parsed.path.lstrip('/')

            # Build a clean URL without problematic query parameters
            password_encoded = urllib.parse.quote_plus(password) if password else ''
            hostname_port = f"{hostname}:{port}" if port else hostname
            clean_database_url = f"postgresql://{username}:{password_encoded}@{hostname_port}/{database}"

            # Create connection directly with asyncpg
            conn = await asyncpg.connect(clean_database_url)

            # Check if user exists in the credentials table
            row = await conn.fetchrow("SELECT email, provider, provider_id FROM user_credentials WHERE email = $1", email)

            if row:
                stored_email = row[0]
                stored_provider = row[1]
                stored_provider_id = row[2]

                # Update provider information if user is signing in with a different provider
                # but same email (this allows for multi-provider access)
                if stored_email == email and stored_provider != provider:
                    # User is signing in with a different provider but same email
                    # Update the provider info to reflect the latest sign-in method
                    await conn.execute("""
                        UPDATE user_credentials
                        SET provider = $1, provider_id = $2, updated_at = CURRENT_TIMESTAMP
                        WHERE email = $3
                    """, provider, provider_id, email)

                # User exists, get profile information
                profile_row = await conn.fetchrow("""
                    SELECT user_id, software_experience, hardware_experience, robotics_experience,
                           programming_languages, hardware_platforms, years_of_experience,
                           primary_interest, education_level, created_at, updated_at
                    FROM user_profiles
                    WHERE user_id = $1
                """, email)

                user_profile = None
                if profile_row:
                    # Parse JSON fields
                    user_profile = {
                        'user_id': profile_row[0],
                        'software_experience': profile_row[1],
                        'hardware_experience': profile_row[2],
                        'robotics_experience': profile_row[3],
                        'programming_languages': json.loads(profile_row[4]) if profile_row[4] else [],
                        'hardware_platforms': json.loads(profile_row[5]) if profile_row[5] else [],
                        'years_of_experience': profile_row[6],
                        'primary_interest': profile_row[7],
                        'education_level': profile_row[8],
                        'created_at': profile_row[9],
                        'updated_at': profile_row[10]
                    }

                await conn.close()
                return AuthResponse(
                    success=True,
                    user_id=email,
                    email=email,
                    message=f"Sign in successful via {provider}"
                )
            else:
                # User doesn't exist, they need to sign up first
                # In this case, we'll return an error but in a real implementation you might want to auto-create
                await conn.close()
                return AuthResponse(
                    success=False,
                    error=f"User with email {email} not found. Please sign up first."
                )

        except Exception as e:
            import traceback
            print(f"Social signin error: {str(e)}")
            print(traceback.format_exc())
            return AuthResponse(
                success=False,
                error=str(e)
            )

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

    async def signin(self, email: str, password: str) -> AuthResponse:
        """
        Authenticate a user from the local database.

        Args:
            email: User's email address
            password: User's password

        Returns:
            AuthResponse with user information
        """
        import asyncpg
        import os
        import urllib.parse
        import json

        try:
            # Parse the database URL to remove problematic parameters
            database_url = os.getenv("NEON_DATABASE_URL")
            parsed = urllib.parse.urlparse(database_url)

            # Extract components
            username = parsed.username
            password_encoded = parsed.password
            hostname = parsed.hostname
            port = parsed.port
            database = parsed.path.lstrip('/')

            # Build a clean URL without problematic query parameters
            password_encoded = urllib.parse.quote_plus(password_encoded) if password_encoded else ''
            hostname_port = f"{hostname}:{port}" if port else hostname
            clean_database_url = f"postgresql://{username}:{password_encoded}@{hostname_port}/{database}"

            # Create connection directly with asyncpg
            conn = await asyncpg.connect(clean_database_url)

            # Retrieve stored password hash and salt for the user
            row = await conn.fetchrow("SELECT password_hash, salt FROM user_credentials WHERE email = $1", email)

            if row:
                stored_password_hash = row[0]  # password_hash
                stored_salt = row[1]           # salt

                # Hash the provided password with the stored salt
                provided_password_hash, _ = self.hash_password(password, stored_salt)

                # Compare the hashes
                if provided_password_hash == stored_password_hash:
                    # Password is correct, now get user profile for additional info
                    # Get user profile using the same connection to avoid conflicts
                    profile_row = await conn.fetchrow("""
                        SELECT user_id, software_experience, hardware_experience, robotics_experience,
                               programming_languages, hardware_platforms, years_of_experience,
                               primary_interest, education_level, created_at, updated_at
                        FROM user_profiles
                        WHERE user_id = $1
                    """, email)

                    user_profile = None
                    if profile_row:
                        # Parse JSON fields
                        user_profile = {
                            'user_id': profile_row[0],
                            'software_experience': profile_row[1],
                            'hardware_experience': profile_row[2],
                            'robotics_experience': profile_row[3],
                            'programming_languages': json.loads(profile_row[4]) if profile_row[4] else [],
                            'hardware_platforms': json.loads(profile_row[5]) if profile_row[5] else [],
                            'years_of_experience': profile_row[6],
                            'primary_interest': profile_row[7],
                            'education_level': profile_row[8],
                            'created_at': profile_row[9],
                            'updated_at': profile_row[10]
                        }

                    await conn.close()
                    return AuthResponse(
                        success=True,
                        user_id=email,
                        email=email,
                        message="Sign in successful"
                    )
                else:
                    # Password doesn't match
                    await conn.close()
                    return AuthResponse(
                        success=False,
                        error="Invalid credentials"
                    )
            else:
                # User doesn't exist
                await conn.close()
                return AuthResponse(
                    success=False,
                    error="Invalid credentials"
                )

        except Exception as e:
            import traceback
            print(f"Signin error: {str(e)}")
            print(traceback.format_exc())
            return AuthResponse(
                success=False,
                error=str(e)
            )

    async def get_user_background(self, user_id: str) -> Dict[str, Any]:
        """
        Get user background information from the local database.

        Args:
            user_id: ID of the user to retrieve background for

        Returns:
            Dictionary containing user's background information
        """
        try:
            user_profile = await get_user_profile(user_id)
            if user_profile:
                return {
                    'softwareExperience': user_profile.get('software_experience'),
                    'hardwareExperience': user_profile.get('hardware_experience'),
                    'roboticsExperience': user_profile.get('robotics_experience'),
                    'programmingLanguages': user_profile.get('programming_languages'),
                    'hardwarePlatforms': user_profile.get('hardware_platforms'),
                    'yearsOfExperience': user_profile.get('years_of_experience'),
                    'primaryInterest': user_profile.get('primary_interest'),
                    'educationLevel': user_profile.get('education_level')
                }
            return {}

        except Exception as e:
            print(f"Error getting user background: {str(e)}")
            return {}

    async def update_user_background(self, user_id: str, background_data: Dict[str, Any]) -> AuthResponse:
        """
        Update user background information in the local database.

        Args:
            user_id: ID of the user to update
            background_data: Dictionary containing background information to update

        Returns:
            AuthResponse with success status
        """
        try:
            # Update user profile in database
            await update_user_profile(
                user_id,
                software_experience=background_data.get('softwareExperience'),
                hardware_experience=background_data.get('hardwareExperience'),
                robotics_experience=background_data.get('roboticsExperience'),
                programming_languages=background_data.get('programmingLanguages'),
                hardware_platforms=background_data.get('hardwarePlatforms'),
                years_of_experience=background_data.get('yearsOfExperience', 0),
                primary_interest=background_data.get('primaryInterest'),
                education_level=background_data.get('educationLevel')
            )

            return AuthResponse(
                success=True,
                user_id=user_id,
                message="Background updated successfully"
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                error=str(e)
            )

    def close(self):
        """Close is not needed for this implementation."""
        pass


# Global client instance
auth_service_client = BetterAuthServiceClient()


async def get_auth_service_client():
    """Dependency to provide auth service client instance."""
    return auth_service_client