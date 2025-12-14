"""
Rate limiting for the Humanoid Robotics Textbook Platform.
This module provides functionality for limiting API requests.
"""
import time
import threading
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from .error_handler import AppError, ErrorCode


class RateLimitType(Enum):
    """Types of rate limits."""
    API_KEY = "api_key"
    IP_ADDRESS = "ip_address"
    USER_ID = "user_id"
    GLOBAL = "global"


@dataclass
class RateLimit:
    """Represents a rate limit configuration."""
    limit: int  # Number of requests allowed
    window: int  # Time window in seconds
    name: str  # Name of the rate limit


@dataclass
class RateLimitState:
    """Represents the current state of a rate limit."""
    count: int
    reset_time: float
    last_request_time: float


class RateLimiter:
    """Rate limiter for API endpoints."""

    def __init__(self):
        self._lock = threading.Lock()
        self._states: Dict[Tuple[RateLimitType, str], RateLimitState] = {}
        self._limits: Dict[str, RateLimit] = {}

        # Default rate limits
        self.add_limit("default_api", RateLimit(100, 3600, "Default API limit: 100 requests per hour"))
        self.add_limit("translation_api", RateLimit(50, 3600, "Translation API limit: 50 requests per hour"))
        self.add_limit("rag_api", RateLimit(200, 3600, "RAG API limit: 200 requests per hour"))
        self.add_limit("auth_api", RateLimit(10, 60, "Auth API limit: 10 requests per minute"))

    def add_limit(self, key: str, rate_limit: RateLimit):
        """Add a rate limit configuration."""
        with self._lock:
            self._limits[key] = rate_limit

    def check_limit(self, limit_key: str, identifier: str, limit_type: RateLimitType) -> Tuple[bool, Dict[str, int]]:
        """
        Check if a request is within the rate limit.

        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        if limit_key not in self._limits:
            # If no limit is defined for this key, allow the request
            return True, {}

        rate_limit = self._limits[limit_key]
        identifier_key = (limit_type, identifier)

        current_time = time.time()

        with self._lock:
            # Get or create the state for this identifier
            if identifier_key not in self._states:
                self._states[identifier_key] = RateLimitState(
                    count=1,
                    reset_time=current_time + rate_limit.window,
                    last_request_time=current_time
                )
                return True, self._get_rate_limit_headers(rate_limit, self._states[identifier_key])

            state = self._states[identifier_key]

            # Check if the window has reset
            if current_time >= state.reset_time:
                # Reset the counter
                state.count = 1
                state.reset_time = current_time + rate_limit.window
                state.last_request_time = current_time
                return True, self._get_rate_limit_headers(rate_limit, state)

            # Check if we're within the limit
            if state.count < rate_limit.limit:
                # Allow the request and increment the counter
                state.count += 1
                state.last_request_time = current_time
                return True, self._get_rate_limit_headers(rate_limit, state)
            else:
                # Rate limit exceeded
                return False, self._get_rate_limit_headers(rate_limit, state)

    def _get_rate_limit_headers(self, rate_limit: RateLimit, state: RateLimitState) -> Dict[str, int]:
        """Get rate limit headers for response."""
        current_time = time.time()
        time_remaining = max(0, int(state.reset_time - current_time))

        return {
            "X-RateLimit-Limit": rate_limit.limit,
            "X-RateLimit-Remaining": max(0, rate_limit.limit - state.count),
            "X-RateLimit-Reset": int(state.reset_time),
            "Retry-After": time_remaining
        }

    def get_remaining_requests(self, limit_key: str, identifier: str, limit_type: RateLimitType) -> Optional[int]:
        """Get the number of remaining requests for an identifier."""
        if limit_key not in self._limits:
            return None

        rate_limit = self._limits[limit_key]
        identifier_key = (limit_type, identifier)

        with self._lock:
            if identifier_key not in self._states:
                return rate_limit.limit

            state = self._states[identifier_key]
            current_time = time.time()

            # Check if the window has reset
            if current_time >= state.reset_time:
                return rate_limit.limit

            return max(0, rate_limit.limit - state.count)

    def get_reset_time(self, limit_key: str, identifier: str, limit_type: RateLimitType) -> Optional[float]:
        """Get the reset time for an identifier's rate limit."""
        if limit_key not in self._limits:
            return None

        identifier_key = (limit_type, identifier)

        with self._lock:
            if identifier_key not in self._states:
                return time.time() + self._limits[limit_key].window

            state = self._states[identifier_key]
            return state.reset_time


# Global rate limiter instance
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _rate_limiter


def check_api_rate_limit(identifier: str, limit_type: RateLimitType = RateLimitType.IP_ADDRESS) -> Tuple[bool, Dict[str, int]]:
    """Check the default API rate limit for an identifier."""
    return get_rate_limiter().check_limit("default_api", identifier, limit_type)


def check_translation_rate_limit(identifier: str, limit_type: RateLimitType = RateLimitType.IP_ADDRESS) -> Tuple[bool, Dict[str, int]]:
    """Check the translation API rate limit for an identifier."""
    return get_rate_limiter().check_limit("translation_api", identifier, limit_type)


def check_rag_rate_limit(identifier: str, limit_type: RateLimitType = RateLimitType.IP_ADDRESS) -> Tuple[bool, Dict[str, int]]:
    """Check the RAG API rate limit for an identifier."""
    return get_rate_limiter().check_limit("rag_api", identifier, limit_type)


def check_auth_rate_limit(identifier: str, limit_type: RateLimitType = RateLimitType.IP_ADDRESS) -> Tuple[bool, Dict[str, int]]:
    """Check the auth API rate limit for an identifier."""
    return get_rate_limiter().check_limit("auth_api", identifier, limit_type)


# Decorator for applying rate limits to functions
from functools import wraps
from .error_handler import handle_error


def rate_limit(limit_key: str, limit_type: RateLimitType = RateLimitType.IP_ADDRESS, identifier_getter=None):
    """
    Decorator to apply rate limiting to a function.

    Args:
        limit_key: The key of the rate limit to apply
        limit_type: The type of identifier to use for rate limiting
        identifier_getter: Function to get the identifier from the function arguments
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get identifier - try to get from kwargs first, then from args
            identifier = None
            if identifier_getter:
                identifier = identifier_getter(*args, **kwargs)
            elif 'user_id' in kwargs:
                identifier = kwargs['user_id']
            elif 'request' in kwargs:
                # Try to get IP from request object
                request = kwargs['request']
                if hasattr(request, 'client'):
                    identifier = request.client.host
            else:
                # Default to a generic identifier
                identifier = "default"

            is_allowed, headers = get_rate_limiter().check_limit(limit_key, identifier, limit_type)

            if not is_allowed:
                from .error_handler import AppError, ErrorCode
                raise AppError(
                    error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
                    message="Rate limit exceeded. Please try again later.",
                    details={
                        "limit": headers.get("X-RateLimit-Limit"),
                        "remaining": headers.get("X-RateLimit-Remaining"),
                        "reset_time": headers.get("X-RateLimit-Reset")
                    }
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


# Middleware for FastAPI
from fastapi import Request


async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting to all requests."""
    # Get client IP address
    client_ip = request.client.host if request.client else "unknown"

    # Apply default API rate limit
    is_allowed, headers = check_api_rate_limit(client_ip, RateLimitType.IP_ADDRESS)

    if not is_allowed:
        from fastapi.responses import JSONResponse
        from .error_handler import AppError, ErrorCode

        error = AppError(
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message="Rate limit exceeded. Please try again later.",
            details={
                "limit": headers.get("X-RateLimit-Limit"),
                "remaining": headers.get("X-RateLimit-Remaining"),
                "reset_time": headers.get("X-RateLimit-Reset")
            }
        )

        response = JSONResponse(
            status_code=429,
            content=error.to_dict()
        )

        # Add rate limit headers
        for header, value in headers.items():
            response.headers[header] = str(value)

        return response

    # Add rate limit headers to the response
    response = await call_next(request)

    # Check rate limit again to get updated headers
    _, headers = check_api_rate_limit(client_ip, RateLimitType.IP_ADDRESS)

    for header, value in headers.items():
        response.headers[header] = str(value)

    return response


# Initialize some common rate limits
get_rate_limiter().add_limit(
    "chat_endpoint",
    RateLimit(50, 3600, "Chat endpoint limit: 50 requests per hour")
)
get_rate_limiter().add_limit(
    "translation_endpoint",
    RateLimit(30, 3600, "Translation endpoint limit: 30 requests per hour")
)