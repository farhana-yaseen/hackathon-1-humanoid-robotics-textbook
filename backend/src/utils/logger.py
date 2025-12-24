"""
Logging utilities for the Humanoid Robotics Textbook application.
Implements comprehensive logging for all user actions and system events (FR-011).
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class Logger:
    """
    Custom logger class for the application with structured logging.
    """

    def __init__(self, name: str = "humanoid_textbook"):
        """
        Initialize the logger with the given name.

        Args:
            name: Name of the logger (defaults to 'humanoid_textbook')
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)

            # Create formatter with structured logging format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(handler)

    def log_user_action(self, user_id: str, action: str, details: Optional[Dict[str, Any]] = None):
        """
        Log a user action with relevant details.

        Args:
            user_id: The ID of the user performing the action
            action: The action being performed (e.g., 'login', 'personalize_content', 'translate_chapter')
            details: Additional details about the action
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "user_action",
            "user_id": user_id,
            "action": action,
            "details": details or {}
        }

        self.logger.info(f"USER_ACTION: {log_data}")

    def log_content_access(self, user_id: str, chapter_id: str, content_type: str):
        """
        Log content access events.

        Args:
            user_id: The ID of the user accessing content
            chapter_id: The ID of the chapter being accessed
            content_type: Type of content access ('view', 'personalize', 'translate')
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "content_access",
            "user_id": user_id,
            "chapter_id": chapter_id,
            "content_type": content_type
        }

        self.logger.info(f"CONTENT_ACCESS: {log_data}")

    def log_translation_event(self, user_id: str, chapter_id: str, success: bool,
                            quality_score: Optional[float] = None):
        """
        Log translation events with success/failure and quality metrics.

        Args:
            user_id: The ID of the user requesting translation
            chapter_id: The ID of the chapter being translated
            success: Whether the translation was successful
            quality_score: Quality score of the translation (0-1)
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "translation_event",
            "user_id": user_id,
            "chapter_id": chapter_id,
            "success": success,
            "quality_score": quality_score
        }

        status = "SUCCESS" if success else "FAILURE"
        self.logger.info(f"TRANSLATION_{status}: {log_data}")

    def log_personalization_event(self, user_id: str, chapter_id: str, success: bool,
                                rules_applied: Optional[list] = None):
        """
        Log personalization events with success/failure and rules applied.

        Args:
            user_id: The ID of the user requesting personalization
            chapter_id: The ID of the chapter being personalized
            success: Whether the personalization was successful
            rules_applied: List of personalization rules applied
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "personalization_event",
            "user_id": user_id,
            "chapter_id": chapter_id,
            "success": success,
            "rules_applied": rules_applied or []
        }

        status = "SUCCESS" if success else "FAILURE"
        self.logger.info(f"PERSONALIZATION_{status}: {log_data}")

    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Log an error with context information.

        Args:
            error: The exception that occurred
            context: Additional context about the error
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }

        self.logger.error(f"ERROR: {log_data}")

    def log_api_request(self, method: str, endpoint: str, user_id: Optional[str] = None,
                       response_time: Optional[float] = None, status_code: Optional[int] = None):
        """
        Log API request details.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint that was called
            user_id: ID of the user making the request (if authenticated)
            response_time: Time taken to process the request in seconds
            status_code: HTTP status code of the response
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "api_request",
            "method": method,
            "endpoint": endpoint,
            "user_id": user_id,
            "response_time_ms": int(response_time * 1000) if response_time else None,
            "status_code": status_code
        }

        self.logger.info(f"API_REQUEST: {log_data}")


# Global logger instance
app_logger = Logger()