"""
Security configuration for the Humanoid Robotics Textbook Platform.
This module provides security headers and CSRF protection.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import secrets
import hashlib
from typing import Optional, List
from datetime import datetime, timedelta
from .error_handler import AppError, ErrorCode


class SecurityConfig:
    """Security configuration class."""

    def __init__(self):
        self.csrf_tokens = {}  # In production, use a proper storage like Redis
        self.csrf_token_expiration = 3600  # 1 hour

    def add_security_headers(self, app: FastAPI):
        """Add security headers to the FastAPI application."""
        # Add security headers middleware
        @app.middleware("http")
        async def security_headers(request: Request, call_next):
            response: Response = await call_next(request)

            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://api.example.com; "  # Replace with actual API domains
                "frame-ancestors 'none';"
            )

            return response

        # Add CORS middleware with security in mind
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://yourdomain.com"],  # Replace with your actual domain
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            # In production, specify exact headers instead of ["*"]
        )

        # Add trusted host middleware
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["yourdomain.com", "www.yourdomain.com", "localhost", "127.0.0.1"]
        )

    def generate_csrf_token(self, user_id: Optional[str] = None) -> str:
        """Generate a CSRF token."""
        token = secrets.token_urlsafe(32)
        token_key = f"csrf_{user_id or 'anonymous'}_{datetime.utcnow().timestamp()}"

        # Store token with expiration
        self.csrf_tokens[token_key] = {
            "token": token,
            "expires_at": datetime.utcnow() + timedelta(seconds=self.csrf_token_expiration),
            "user_id": user_id
        }

        return token

    def validate_csrf_token(self, token: str, user_id: Optional[str] = None) -> bool:
        """Validate a CSRF token."""
        # Find the token in storage
        for key, data in list(self.csrf_tokens.items()):  # Use list to avoid modification during iteration
            # Clean up expired tokens
            if datetime.utcnow() > data["expires_at"]:
                del self.csrf_tokens[key]
                continue

            if data["token"] == token:
                # Optionally check if the user_id matches
                if user_id and data["user_id"] and data["user_id"] != user_id:
                    return False
                # Remove token after use (for one-time tokens)
                del self.csrf_tokens[key]
                return True

        return False

    def add_csrf_protection(self, app: FastAPI):
        """Add CSRF protection to the application."""
        @app.middleware("http")
        async def csrf_protection(request: Request, call_next):
            # Skip CSRF check for safe methods
            if request.method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
                response = await call_next(request)
                # Add CSRF token to response headers for GET requests
                csrf_token = self.generate_csrf_token()
                response.headers["X-CSRF-Token"] = csrf_token
                return response

            # For unsafe methods, check for CSRF token
            csrf_token_header = request.headers.get("X-CSRF-Token")
            csrf_token_cookie = request.cookies.get("csrf_token")
            csrf_token = csrf_token_header or csrf_token_cookie

            if not csrf_token:
                return JSONResponse(
                    status_code=403,
                    content={
                        "error_code": ErrorCode.INVALID_INPUT.value,
                        "message": "CSRF token missing",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )

            # Validate the CSRF token
            user_id = None  # In a real app, extract user_id from auth
            if not self.validate_csrf_token(csrf_token, user_id):
                return JSONResponse(
                    status_code=403,
                    content={
                        "error_code": ErrorCode.INVALID_INPUT.value,
                        "message": "Invalid or expired CSRF token",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )

            response = await call_next(request)
            return response


# Global security configuration instance
_security_config = SecurityConfig()


def get_security_config() -> SecurityConfig:
    """Get the global security configuration instance."""
    return _security_config


def add_security_headers(app: FastAPI):
    """Add security headers to the application."""
    security_config = get_security_config()
    security_config.add_security_headers(app)


def add_csrf_protection(app: FastAPI):
    """Add CSRF protection to the application."""
    security_config = get_security_config()
    security_config.add_csrf_protection(app)


# Additional security utilities
def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """Hash a password with a salt."""
    import bcrypt

    if salt is None:
        salt = bcrypt.gensalt().decode('utf-8')
    else:
        salt = salt.encode('utf-8')

    pwd_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

    return hashed, salt.decode('utf-8') if isinstance(salt, bytes) else salt


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    import bcrypt

    pwd_bytes = password.encode('utf-8')
    hash_bytes = hashed.encode('utf-8')

    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def sanitize_input(input_str: str) -> str:
    """Basic input sanitization to prevent XSS."""
    # Remove potentially dangerous characters/sequences
    dangerous_patterns = [
        '<script', 'javascript:', 'vbscript:', '<iframe', '<object', '<embed',
        '<form', 'onerror', 'onload', 'onclick', 'onmouseover', 'onfocus'
    ]

    sanitized = input_str
    for pattern in dangerous_patterns:
        # Case insensitive replacement
        sanitized = sanitized.replace(pattern, f"&lt;{pattern[1:]}" if pattern.startswith('<') else f"removed:{pattern}")

    return sanitized


def validate_jwt_token(token: str, secret_key: str) -> Optional[dict]:
    """Validate a JWT token."""
    import jwt
    from datetime import datetime

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        # Check if token is expired
        exp = payload.get('exp')
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# Initialize security configuration
def setup_security(app: FastAPI):
    """Set up all security measures for the application."""
    add_security_headers(app)
    add_csrf_protection(app)


# Example usage in main app initialization
def get_security_headers_for_response() -> dict:
    """Get security headers for direct use in responses."""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "no-referrer-when-downgrade",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
    }