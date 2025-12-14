"""
Security utilities for the Humanoid Robotics Textbook application.
Implements security headers and CSRF protection.
"""
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional, Callable, Awaitable
import secrets
import hashlib
from .logger import app_logger


class SecurityHeaders:
    """Security headers configuration for the application."""

    @staticmethod
    def add_security_headers(response: Response) -> Response:
        """
        Add security headers to the response.

        Args:
            response: The FastAPI response object

        Returns:
            Response with security headers added
        """
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Cross-site scripting protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy (CSP)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Strict Transport Security (HSTS) - only for HTTPS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Prevent IE from opening downloads in the browser
        response.headers["X-Download-Options"] = "noopen"

        # Disable server header
        response.headers["X-Powered-By"] = ""

        return response


class CSRFProtection:
    """
    CSRF protection implementation for the application.
    """

    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize CSRF protection.

        Args:
            secret_key: Secret key for CSRF token generation
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.csrf_tokens = set()  # In a real app, use Redis or database

    def generate_csrf_token(self, user_id: str) -> str:
        """
        Generate a CSRF token for a user.

        Args:
            user_id: The ID of the user

        Returns:
            CSRF token string
        """
        # Create a unique token based on user ID and secret key
        token_data = f"{user_id}:{self.secret_key}:{secrets.token_urlsafe(16)}"
        token_hash = hashlib.sha256(token_data.encode()).hexdigest()

        # Store the token for validation
        self.csrf_tokens.add(token_hash)

        return token_hash

    def validate_csrf_token(self, token: str, user_id: str) -> bool:
        """
        Validate a CSRF token.

        Args:
            token: The CSRF token to validate
            user_id: The user ID associated with the token

        Returns:
            True if token is valid, False otherwise
        """
        # Check if token exists in our stored tokens
        if token in self.csrf_tokens:
            # Remove the token to prevent replay attacks
            self.csrf_tokens.remove(token)
            return True

        # In a real implementation, we would also check if the token
        # was generated for the specific user
        return False

    def get_csrf_token_from_request(self, request: Request) -> Optional[str]:
        """
        Extract CSRF token from request.

        Args:
            request: The FastAPI request object

        Returns:
            CSRF token if found, None otherwise
        """
        # Check for token in header first
        token = request.headers.get("X-CSRF-Token")

        if not token:
            # Check for token in form data
            token = request.form.get("csrf_token") if hasattr(request, "form") else None

        if not token:
            # Check for token in query parameters
            token = request.query_params.get("csrf_token")

        return token


# Global CSRF protection instance
csrf_protection = CSRFProtection()


def security_middleware_handler(request: Request, call_next: Callable) -> Response:
    """
    Security middleware to add security headers and handle CSRF protection.

    Args:
        request: The incoming request
        call_next: Function to call the next middleware/route handler

    Returns:
        Response with security measures applied
    """
    # Add security headers to all responses
    response = call_next(request)

    if isinstance(response, Response):
        SecurityHeaders.add_security_headers(response)

    return response


def require_csrf_protection(expected_user_id: Optional[str] = None):
    """
    Decorator to require CSRF protection for endpoints.

    Args:
        expected_user_id: Expected user ID (for validation)
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            # Skip CSRF check for GET, HEAD, OPTIONS, TRACE methods
            if request.method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
                return await func(request, *args, **kwargs)

            # Extract CSRF token from request
            csrf_token = csrf_protection.get_csrf_token_from_request(request)

            if not csrf_token:
                app_logger.log_user_action(
                    user_id="unknown",
                    action="csrf_protection_failed",
                    details={"reason": "no_csrf_token", "url": str(request.url)}
                )

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CSRF token missing"
                )

            # Validate the CSRF token
            # Note: In a real implementation, you would extract the user ID from the session/auth context
            user_id = expected_user_id or "unknown"  # This would come from authentication in a real app
            is_valid = csrf_protection.validate_csrf_token(csrf_token, user_id)

            if not is_valid:
                app_logger.log_user_action(
                    user_id=user_id,
                    action="csrf_protection_failed",
                    details={"reason": "invalid_csrf_token", "url": str(request.url)}
                )

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid CSRF token"
                )

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


# Additional security utilities
def sanitize_input(input_str: str) -> str:
    """
    Basic input sanitization to prevent XSS.

    Args:
        input_str: Input string to sanitize

    Returns:
        Sanitized string
    """
    if not input_str:
        return input_str

    # Remove potentially dangerous characters/sequences
    sanitized = input_str.replace("<script", "&lt;script").replace("</script>", "&lt;/script&gt;")
    sanitized = sanitized.replace("javascript:", "javascript&#58;").replace("vbscript:", "vbscript&#58;")
    sanitized = sanitized.replace("onerror", "onerror_").replace("onload", "onload_")

    return sanitized


def validate_content_type(content_type: str, allowed_types: list) -> bool:
    """
    Validate content type against allowed types.

    Args:
        content_type: Content type to validate
        allowed_types: List of allowed content types

    Returns:
        True if content type is allowed, False otherwise
    """
    return any(allowed_type.lower() in content_type.lower() for allowed_type in allowed_types)