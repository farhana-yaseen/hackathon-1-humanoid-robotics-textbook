"""
Session Manager for Better-Auth feature
"""
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse


class SessionManager:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "supersecretjwtkey")
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=30)  # 30 minutes
        self.refresh_token_expire = timedelta(days=7)    # 7 days

    def create_access_token(self, data: dict) -> str:
        """
        Create an access token with the given data.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + self.access_token_expire
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """
        Create a refresh token with the given data.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + self.refresh_token_expire
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify the given token and return the payload if valid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None

    def set_auth_cookies(self, response: Response, access_token: str, refresh_token: str):
        """
        Set HTTP-only cookies for access and refresh tokens.
        """
        # Set access token cookie (short-lived, http-only, secure)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=int(self.access_token_expire.total_seconds())
        )

        # Set refresh token cookie (longer-lived, http-only, secure)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=int(self.refresh_token_expire.total_seconds())
        )

    def get_token_from_cookie(self, request: Request, token_type: str = "access") -> Optional[str]:
        """
        Get token from cookie.
        """
        if token_type == "access":
            return request.cookies.get("access_token")
        elif token_type == "refresh":
            return request.cookies.get("refresh_token")
        return None

    def clear_auth_cookies(self, response: Response):
        """
        Clear auth cookies.
        """
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            max_age=0
        )
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            max_age=0
        )

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Refresh the access token using the refresh token.
        """
        payload = self.verify_token(refresh_token)
        if payload and payload.get("type") == "refresh":
            # Create new access token with the same user data
            user_data = {k: v for k, v in payload.items() if k not in ["exp", "type"]}
            return self.create_access_token(user_data)
        return None


# Global session manager instance
session_manager = SessionManager()