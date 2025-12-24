"""
Error handling utilities for the Humanoid Robotics Textbook application.
Implements proper error handling and user-friendly error messages.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from .logger import app_logger
import traceback


class AppError(Exception):
    """
    Base application error class with user-friendly messages.
    """

    def __init__(self, message: str, error_code: str, http_status_code: int = status.HTTP_400_BAD_REQUEST):
        """
        Initialize an application error.

        Args:
            message: User-friendly error message
            error_code: Machine-readable error code
            http_status_code: HTTP status code for the error
        """
        self.message = message
        self.error_code = error_code
        self.http_status_code = http_status_code
        super().__init__(message)


class ValidationError(AppError):
    """Error for validation failures."""
    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.field = field
        self.details = details


class AuthenticationError(AppError):
    """Error for authentication failures."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            http_status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(AppError):
    """Error for authorization failures."""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            http_status_code=status.HTTP_403_FORBIDDEN
        )


class ResourceNotFoundError(AppError):
    """Error for when a requested resource is not found."""
    def __init__(self, resource_type: str, resource_id: str = None):
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        else:
            message = f"{resource_type} not found"

        super().__init__(
            message=message,
            error_code="RESOURCE_NOT_FOUND",
            http_status_code=status.HTTP_404_NOT_FOUND
        )


class ServiceError(AppError):
    """Error for service-level failures."""
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(
            message=message,
            error_code="SERVICE_ERROR",
            http_status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for the application.

    Args:
        request: The incoming request
        exc: The exception that occurred

    Returns:
        JSONResponse with error details
    """
    # Log the error with full traceback
    error_id = f"err_{id(exc)}_{int(__import__('time').time())}"
    app_logger.log_error(
        exc,
        context={
            "error_id": error_id,
            "url": str(request.url),
            "method": request.method,
            "user_agent": request.headers.get("user-agent"),
            "traceback": traceback.format_exc()
        }
    )

    # Handle different types of exceptions
    if isinstance(exc, AppError):
        # Return user-friendly error message for application errors
        return JSONResponse(
            status_code=exc.http_status_code,
            content={
                "error": {
                    "error_code": exc.error_code,
                    "message": exc.message,
                    "error_id": error_id
                }
            }
        )
    elif isinstance(exc, HTTPException):
        # Handle FastAPI HTTP exceptions
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "error_code": f"HTTP_{exc.status_code}",
                    "message": exc.detail if exc.detail else "An error occurred",
                    "error_id": error_id
                }
            }
        )
    else:
        # Handle unexpected errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "error_code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                    "error_id": error_id
                }
            }
        )


def add_error_handlers(app):
    """
    Add error handlers to the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(AppError, global_exception_handler)
    app.add_exception_handler(HTTPException, global_exception_handler)


# Error response utilities
def create_error_response(error_code: str, message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        error_code: Machine-readable error code
        message: User-friendly error message
        details: Additional error details

    Returns:
        Dictionary with error response structure
    """
    response = {
        "success": False,
        "error": {
            "error_code": error_code,
            "message": message
        }
    }

    if details:
        response["error"]["details"] = details

    return response


def create_success_response(data: Any = None) -> Dict[str, Any]:
    """
    Create a standardized success response.

    Args:
        data: Response data

    Returns:
        Dictionary with success response structure
    """
    response = {"success": True}

    if data is not None:
        response["data"] = data

    return response