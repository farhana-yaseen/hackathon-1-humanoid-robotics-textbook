"""
Error handling for the Humanoid Robotics Textbook Platform.
This module provides standardized error handling and user-friendly error messages.
"""
from typing import Dict, Any, Optional
from enum import Enum
from fastapi import HTTPException, status
import logging
from .logging_config import log_error


class ErrorCode(Enum):
    """Standardized error codes for the application."""
    # Authentication errors
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_USER_NOT_FOUND = "AUTH_USER_NOT_FOUND"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_INSUFFICIENT_PERMISSIONS = "AUTH_INSUFFICIENT_PERMISSIONS"

    # RAG errors
    RAG_QUERY_FAILED = "RAG_QUERY_FAILED"
    RAG_NO_CONTEXT_FOUND = "RAG_NO_CONTEXT_FOUND"
    RAG_INVALID_SESSION = "RAG_INVALID_SESSION"

    # Translation errors
    TRANSLATION_FAILED = "TRANSLATION_FAILED"
    TRANSLATION_INVALID_LANGUAGE = "TRANSLATION_INVALID_LANGUAGE"
    TRANSLATION_UNSUPPORTED_FORMAT = "TRANSLATION_UNSUPPORTED_FORMAT"

    # General errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INVALID_INPUT = "INVALID_INPUT"


class AppError(Exception):
    """Base application error class."""

    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None,
                 original_exception: Optional[Exception] = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        self.original_exception = original_exception
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary representation."""
        return {
            "error_code": self.error_code.value,
            "message": self.message,
            "details": self.details,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }

    def to_http_exception(self) -> HTTPException:
        """Convert the AppError to an HTTPException."""
        status_code = self._get_status_code()
        return HTTPException(
            status_code=status_code,
            detail=self.to_dict()
        )

    def _get_status_code(self) -> int:
        """Map error codes to HTTP status codes."""
        error_code_to_status = {
            ErrorCode.AUTH_INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.AUTH_USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.AUTH_TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,
            ErrorCode.RAG_NO_CONTEXT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.RAG_INVALID_SESSION: status.HTTP_400_BAD_REQUEST,
            ErrorCode.TRANSLATION_INVALID_LANGUAGE: status.HTTP_400_BAD_REQUEST,
            ErrorCode.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
            ErrorCode.RATE_LIMIT_EXCEEDED: status.HTTP_429_TOO_MANY_REQUESTS,
            ErrorCode.INVALID_INPUT: status.HTTP_400_BAD_REQUEST,
        }

        return error_code_to_status.get(self.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ErrorHandler:
    """Centralized error handler for the application."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: str = "", user_facing: bool = True) -> AppError:
        """
        Handle an error and return a standardized AppError.

        Args:
            error: The exception that occurred
            context: Context information about where the error occurred
            user_facing: Whether the error message should be user-friendly

        Returns:
            AppError: Standardized error object
        """
        # Log the error with full details
        log_error(error, context)

        # If it's already an AppError, return it as is
        if isinstance(error, AppError):
            return error

        # Map common Python exceptions to AppError
        if isinstance(error, ValueError):
            message = "Invalid input provided" if user_facing else str(error)
            return AppError(
                error_code=ErrorCode.VALIDATION_ERROR,
                message=message,
                details={"raw_error": str(error) if not user_facing else None},
                original_exception=error
            )

        if isinstance(error, KeyError):
            message = "Required data not found" if user_facing else str(error)
            return AppError(
                error_code=ErrorCode.RESOURCE_NOT_FOUND,
                message=message,
                details={"raw_error": str(error) if not user_facing else None},
                original_exception=error
            )

        # For all other errors, treat as internal error
        message = "An unexpected error occurred. Please try again later." if user_facing else str(error)
        return AppError(
            error_code=ErrorCode.INTERNAL_ERROR,
            message=message,
            details={"raw_error": str(error) if not user_facing else None},
            original_exception=error
        )

    def handle_validation_error(self, field: str, value: Any, reason: str) -> AppError:
        """Handle validation errors with specific field information."""
        return AppError(
            error_code=ErrorCode.VALIDATION_ERROR,
            message=f"Invalid value for {field}",
            details={
                "field": field,
                "value": str(value),
                "reason": reason
            }
        )

    def handle_translation_error(self, source_text: str, target_language: str, reason: str) -> AppError:
        """Handle translation-specific errors."""
        return AppError(
            error_code=ErrorCode.TRANSLATION_FAILED,
            message=f"Translation from source text to {target_language} failed",
            details={
                "target_language": target_language,
                "text_length": len(source_text),
                "reason": reason
            }
        )

    def handle_rag_error(self, query: str, reason: str) -> AppError:
        """Handle RAG-specific errors."""
        return AppError(
            error_code=ErrorCode.RAG_QUERY_FAILED,
            message="Could not process your query",
            details={
                "query_length": len(query),
                "reason": reason
            }
        )


# Global error handler instance
_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    return _error_handler


# Convenience functions
def handle_error(error: Exception, context: str = "", user_facing: bool = True) -> AppError:
    """Convenience function to handle an error."""
    return get_error_handler().handle_error(error, context, user_facing)


def handle_validation_error(field: str, value: Any, reason: str) -> AppError:
    """Convenience function to handle validation errors."""
    return get_error_handler().handle_validation_error(field, value, reason)


def handle_translation_error(source_text: str, target_language: str, reason: str) -> AppError:
    """Convenience function to handle translation errors."""
    return get_error_handler().handle_translation_error(source_text, target_language, reason)


def handle_rag_error(query: str, reason: str) -> AppError:
    """Convenience function to handle RAG errors."""
    return get_error_handler().handle_rag_error(query, reason)


# Exception handlers for FastAPI
def register_exception_handlers(app):
    """Register exception handlers with a FastAPI application."""

    @app.exception_handler(AppError)
    async def handle_app_error(request, exc: AppError):
        """Handle AppError exceptions."""
        return exc.to_http_exception()

    @app.exception_handler(Exception)
    async def handle_general_error(request, exc: Exception):
        """Handle general exceptions."""
        error = handle_error(exc, f"Unhandled exception in {request.url.path}")
        return error.to_http_exception()


# Custom validation functions
def validate_email(email: str) -> str:
    """Validate email format."""
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        raise handle_validation_error("email", email, "Invalid email format")

    return email


def validate_token_length(text: str, max_tokens: int = 2000) -> str:
    """Validate text length against token limits."""
    # Rough approximation: 4 characters per token
    max_chars = max_tokens * 4

    if len(text) > max_chars:
        raise handle_validation_error(
            "text",
            f"Text length: {len(text)} chars",
            f"Text exceeds maximum length of {max_tokens} tokens ({max_chars} characters)"
        )

    return text


def validate_language_code(language: str) -> str:
    """Validate language code."""
    supported_languages = {"Urdu", "English", "Spanish", "French", "German", "Chinese", "Japanese"}

    if language not in supported_languages:
        raise handle_validation_error(
            "language",
            language,
            f"Language not supported. Supported languages: {', '.join(supported_languages)}"
        )

    return language


# Context manager for safe operations
from contextlib import contextmanager


@contextmanager
def safe_operation(operation_name: str, user_facing: bool = True):
    """Context manager for performing operations with error handling."""
    try:
        yield
    except AppError:
        # Re-raise AppError as-is
        raise
    except Exception as e:
        # Convert other exceptions to AppError
        error = handle_error(e, operation_name, user_facing)
        raise error


# Decorator for automatic error handling
def with_error_handling(operation_name: str, user_facing: bool = True):
    """Decorator to wrap functions with automatic error handling."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with safe_operation(operation_name, user_facing):
                return func(*args, **kwargs)
        return wrapper
    return decorator