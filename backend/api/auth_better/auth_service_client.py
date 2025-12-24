"""
Better Auth Service Client for the humanoid robotics textbook.
This module provides a client to communicate with the Better Auth service.
"""
import os
import httpx
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    success: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


class BetterAuthServiceClient:
    """Client to communicate with the Better Auth service."""

    def __init__(self):
        self.auth_service_url = os.getenv(
            "BETTER_AUTH_SERVICE_URL",
            "http://localhost:3002"
        )
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=5.0)
        )

    async def signup(self, email: str, password: str, name: str,
                     background_data: Optional[Dict[str, Any]] = None) -> AuthResponse:
        """
        Create a new user via the Better Auth service.

        Args:
            email: User's email address
            password: User's password
            name: User's name
            background_data: Optional user background information

        Returns:
            AuthResponse with user information
        """
        try:
            # First, create the user in Better Auth
            signup_data = {
                "email": email,
                "password": password,
                "name": name
            }

            response = await self.http_client.post(
                f"{self.auth_service_url}/api/auth/signup",
                json=signup_data
            )

            if response.status_code != 200:
                return AuthResponse(
                    success=False,
                    error=f"Signup failed: {response.text}"
                )

            result = response.json()
            user_id = result.get("userId") or result.get("user", {}).get("id")

            # If background data is provided, save it to the auth service
            if background_data and user_id:
                background_response = await self.http_client.post(
                    f"{self.auth_service_url}/api/signup-background",
                    json={
                        "email": email,
                        "background": background_data
                    }
                )

                if background_response.status_code != 200:
                    # Don't fail the signup if background save fails
                    print(f"Warning: Failed to save background data: {background_response.text}")

            return AuthResponse(
                success=True,
                user_id=user_id,
                email=email,
                message=result.get("message", "User created successfully")
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                error=str(e)
            )

    async def signin(self, email: str, password: str) -> AuthResponse:
        """
        Authenticate a user via the Better Auth service.

        Args:
            email: User's email address
            password: User's password

        Returns:
            AuthResponse with user information
        """
        try:
            signin_data = {
                "email": email,
                "password": password
            }

            response = await self.http_client.post(
                f"{self.auth_service_url}/api/auth/signin",
                json=signin_data
            )

            if response.status_code != 200:
                return AuthResponse(
                    success=False,
                    error=f"Signin failed: {response.text}"
                )

            result = response.json()
            user_id = result.get("userId") or result.get("user", {}).get("id")

            return AuthResponse(
                success=True,
                user_id=user_id,
                email=email,
                message=result.get("message", "Sign in successful")
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                error=str(e)
            )

    async def get_user_background(self, user_id: str) -> Dict[str, Any]:
        """
        Get user background information from the Better Auth service.

        Args:
            user_id: ID of the user to retrieve background for

        Returns:
            Dictionary containing user's background information
        """
        try:
            response = await self.http_client.get(
                f"{self.auth_service_url}/api/user-background/{user_id}"
            )

            if response.status_code != 200:
                print(f"Error getting user background: {response.text}")
                return {}

            return response.json()

        except Exception as e:
            print(f"Error getting user background: {str(e)}")
            return {}

    async def update_user_background(self, user_id: str, background_data: Dict[str, Any]) -> AuthResponse:
        """
        Update user background information in the Better Auth service.

        Args:
            user_id: ID of the user to update
            background_data: Dictionary containing background information to update

        Returns:
            AuthResponse with success status
        """
        try:
            response = await self.http_client.post(
                f"{self.auth_service_url}/api/user-background",
                json={
                    "userId": user_id,
                    "background": background_data
                }
            )

            if response.status_code != 200:
                return AuthResponse(
                    success=False,
                    error=f"Update background failed: {response.text}"
                )

            result = response.json()

            return AuthResponse(
                success=True,
                user_id=user_id,
                message=result.get("message", "Background updated successfully")
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                error=str(e)
            )

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()


# Global client instance
auth_service_client = BetterAuthServiceClient()


async def get_auth_service_client():
    """Dependency to provide auth service client instance."""
    return auth_service_client