"""
Logging Configuration for Better-Auth feature
"""
import logging
from datetime import datetime


class AuthLogger:
    def __init__(self):
        self.logger = logging.getLogger("better_auth")
        self.logger.setLevel(logging.INFO)

        # Create a handler for authentication events
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_auth_event(self, event_type: str, user_id: str, details: dict = None):
        """
        Log an authentication event.

        Args:
            event_type: Type of authentication event (signup, signin, signout, etc.)
            user_id: The user ID associated with the event
            details: Additional details about the event
        """
        message = f"AUTH_EVENT - Type: {event_type}, User: {user_id}"
        if details:
            message += f", Details: {details}"

        self.logger.info(message)

    def log_auth_error(self, event_type: str, user_id: str, error: str, details: dict = None):
        """
        Log an authentication error.

        Args:
            event_type: Type of authentication event that failed
            user_id: The user ID associated with the event (if available)
            error: The error message
            details: Additional details about the error
        """
        message = f"AUTH_ERROR - Type: {event_type}, User: {user_id}, Error: {error}"
        if details:
            message += f", Details: {details}"

        self.logger.error(message)

    def log_profile_event(self, event_type: str, user_id: str, details: dict = None):
        """
        Log a profile-related event.

        Args:
            event_type: Type of profile event (create, update, delete)
            user_id: The user ID associated with the event
            details: Additional details about the event
        """
        message = f"PROFILE_EVENT - Type: {event_type}, User: {user_id}"
        if details:
            message += f", Details: {details}"

        self.logger.info(message)


# Global auth logger instance
auth_logger = AuthLogger()