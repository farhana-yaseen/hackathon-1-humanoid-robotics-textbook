"""
Rate Limiter for Better-Auth endpoints
"""
import time
from typing import Dict
from collections import defaultdict, deque
import threading


class RateLimiter:
    def __init__(self, max_attempts: int = 5, window_size: int = 900):  # 900 seconds = 15 minutes
        self.max_attempts = max_attempts
        self.window_size = window_size
        self.attempts: Dict[str, deque] = defaultdict(deque)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if the request from the given identifier is allowed based on rate limits.

        Args:
            identifier: A unique identifier for the source of requests (e.g., IP address)

        Returns:
            True if the request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()

            # Remove attempts that are outside the window
            while (self.attempts[identifier] and
                   current_time - self.attempts[identifier][0] > self.window_size):
                self.attempts[identifier].popleft()

            # Check if the number of attempts is within the limit
            if len(self.attempts[identifier]) < self.max_attempts:
                # Add the current attempt
                self.attempts[identifier].append(current_time)
                return True

            return False

    def get_reset_time(self, identifier: str) -> float:
        """
        Get the time when the rate limit will reset for the given identifier.

        Args:
            identifier: A unique identifier for the source of requests

        Returns:
            The time (in seconds) when the rate limit will reset
        """
        with self.lock:
            if identifier in self.attempts and self.attempts[identifier]:
                return self.attempts[identifier][0] + self.window_size
            return time.time()


import os

# Check if we're in development mode
is_development = os.getenv('ENVIRONMENT', 'development').lower() == 'development'

# Global rate limiter instance
if is_development:
    # Very lenient rate limits for development (effectively no rate limiting for testing)
    rate_limiter = RateLimiter(max_attempts=100, window_size=1)  # 100 attempts per second in development
else:
    # Strict rate limits for production
    rate_limiter = RateLimiter(max_attempts=5, window_size=900)  # 5 attempts per 15 minutes