"""
Rate limiting utilities for the Humanoid Robotics Textbook application.
Implements rate limiting for API endpoints.
"""
import time
from collections import defaultdict, deque
from typing import Dict, Optional
from threading import Lock
from fastapi import Request, HTTPException, status
from .logger import app_logger


class RateLimiter:
    """
    In-memory rate limiter using a sliding window algorithm.
    """

    def __init__(self):
        """Initialize the rate limiter."""
        self.requests = defaultdict(deque)  # key -> deque of timestamps
        self.lock = Lock()

    def is_allowed(self, key: str, max_requests: int, window_size: int) -> bool:
        """
        Check if a request is allowed based on rate limits.

        Args:
            key: Unique identifier for the client (e.g., IP address, user ID)
            max_requests: Maximum number of requests allowed
            window_size: Time window in seconds

        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            window_start = now - window_size

            # Remove old requests outside the window
            while self.requests[key] and self.requests[key][0] <= window_start:
                self.requests[key].popleft()

            # Check if we're under the limit
            if len(self.requests[key]) < max_requests:
                # Add the current request
                self.requests[key].append(now)
                return True

            return False

    def get_reset_time(self, key: str, window_size: int) -> float:
        """
        Get the time when the rate limit will reset.

        Args:
            key: Unique identifier for the client
            window_size: Time window in seconds

        Returns:
            Unix timestamp when the rate limit will reset
        """
        with self.lock:
            if self.requests[key]:
                oldest_request = self.requests[key][0]
                return oldest_request + window_size
            return time.time()


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests: int, window_size: int, key_func=None):
    """
    Decorator to apply rate limiting to a FastAPI endpoint.

    Args:
        max_requests: Maximum number of requests allowed
        window_size: Time window in seconds
        key_func: Function to extract the rate limit key from the request
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            # Default key function uses client IP
            if key_func:
                key = key_func(request)
            else:
                key = request.client.host if request.client else "unknown"

            if not rate_limiter.is_allowed(key, max_requests, window_size):
                reset_time = rate_limiter.get_reset_time(key, window_size)
                retry_after = int(reset_time - time.time())

                app_logger.log_user_action(
                    user_id=key,
                    action="rate_limit_exceeded",
                    details={
                        "max_requests": max_requests,
                        "window_size": window_size,
                        "retry_after": retry_after
                    }
                )

                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Please try again in {retry_after} seconds.",
                        "retry_after": retry_after
                    }
                )

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


# Predefined rate limit configurations
class RateLimitConfigs:
    """Common rate limit configurations."""

    # General API endpoints
    API_GENERAL = {"max_requests": 100, "window_size": 3600}  # 100 requests per hour

    # Authentication endpoints (stricter limits)
    AUTH = {"max_requests": 10, "window_size": 300}  # 10 requests per 5 minutes

    # Translation endpoints (resource-intensive)
    TRANSLATION = {"max_requests": 20, "window_size": 3600}  # 20 requests per hour

    # Personalization endpoints
    PERSONALIZATION = {"max_requests": 50, "window_size": 3600}  # 50 requests per hour


def apply_rate_limit(endpoint_type: str):
    """
    Apply rate limiting based on endpoint type.

    Args:
        endpoint_type: Type of endpoint ('auth', 'translation', 'personalization', 'general')
    """
    configs = {
        'auth': RateLimitConfigs.AUTH,
        'translation': RateLimitConfigs.TRANSLATION,
        'personalization': RateLimitConfigs.PERSONALIZATION,
        'general': RateLimitConfigs.API_GENERAL
    }

    config = configs.get(endpoint_type, RateLimitConfigs.API_GENERAL)
    return rate_limit(**config, key_func=lambda req: req.client.host)