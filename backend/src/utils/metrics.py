"""
Metrics collection utilities for the Humanoid Robotics Textbook application.
Implements metrics collection for user engagement, translation success rate, error rates (FR-012).
"""
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Any
import threading
import time


class MetricType(Enum):
    """Types of metrics collected by the system."""
    USER_ENGAGEMENT = "user_engagement"
    TRANSLATION_SUCCESS = "translation_success"
    ERROR_RATE = "error_rate"
    PERSONALIZATION_USAGE = "personalization_usage"


class MetricsCollector:
    """
    Metrics collector for tracking application performance and user behavior.
    """

    def __init__(self):
        """Initialize the metrics collector."""
        self.metrics = {}
        self.lock = threading.Lock()

        # Initialize metrics counters
        self.metrics = {
            MetricType.USER_ENGAGEMENT: {
                "total_sessions": 0,
                "active_users": set(),
                "page_views": 0,
                "time_spent": 0  # in seconds
            },
            MetricType.TRANSLATION_SUCCESS: {
                "total_requests": 0,
                "successful_translations": 0,
                "failed_translations": 0,
                "average_quality_score": 0.0
            },
            MetricType.ERROR_RATE: {
                "total_errors": 0,
                "error_details": []
            },
            MetricType.PERSONALIZATION_USAGE: {
                "total_requests": 0,
                "successful_personalizations": 0,
                "failed_personalizations": 0
            }
        }

    def increment_user_engagement(self, user_id: str, action: str = "page_view"):
        """
        Increment user engagement metrics.

        Args:
            user_id: The ID of the user
            action: The type of engagement action
        """
        with self.lock:
            self.metrics[MetricType.USER_ENGAGEMENT]["total_sessions"] += 1
            self.metrics[MetricType.USER_ENGAGEMENT]["active_users"].add(user_id)
            if action == "page_view":
                self.metrics[MetricType.USER_ENGAGEMENT]["page_views"] += 1

    def record_translation_event(self, success: bool, quality_score: Optional[float] = None):
        """
        Record a translation event for metrics tracking.

        Args:
            success: Whether the translation was successful
            quality_score: Quality score of the translation (0-1)
        """
        with self.lock:
            self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"] += 1
            if success:
                self.metrics[MetricType.TRANSLATION_SUCCESS]["successful_translations"] += 1
                if quality_score is not None:
                    # Calculate average quality score
                    current_avg = self.metrics[MetricType.TRANSLATION_SUCCESS]["average_quality_score"]
                    count = self.metrics[MetricType.TRANSLATION_SUCCESS]["successful_translations"]
                    new_avg = ((current_avg * (count - 1)) + quality_score) / count
                    self.metrics[MetricType.TRANSLATION_SUCCESS]["average_quality_score"] = new_avg
            else:
                self.metrics[MetricType.TRANSLATION_SUCCESS]["failed_translations"] += 1

    def record_error(self, error_type: str, error_message: str, severity: str = "medium"):
        """
        Record an error for metrics tracking.

        Args:
            error_type: Type of error
            error_message: Error message
            severity: Severity level (low, medium, high)
        """
        with self.lock:
            self.metrics[MetricType.ERROR_RATE]["total_errors"] += 1
            self.metrics[MetricType.ERROR_RATE]["error_details"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "type": error_type,
                "message": error_message,
                "severity": severity
            })

    def record_personalization_event(self, success: bool):
        """
        Record a personalization event for metrics tracking.

        Args:
            success: Whether the personalization was successful
        """
        with self.lock:
            self.metrics[MetricType.PERSONALIZATION_USAGE]["total_requests"] += 1
            if success:
                self.metrics[MetricType.PERSONALIZATION_USAGE]["successful_personalizations"] += 1
            else:
                self.metrics[MetricType.PERSONALIZATION_USAGE]["failed_personalizations"] += 1

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all collected metrics.

        Returns:
            Dictionary containing all metrics
        """
        with self.lock:
            # Calculate success rates and other derived metrics
            translation_success_rate = 0.0
            if self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"] > 0:
                translation_success_rate = (
                    self.metrics[MetricType.TRANSLATION_SUCCESS]["successful_translations"] /
                    self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"]
                ) * 100

            personalization_success_rate = 0.0
            if self.metrics[MetricType.PERSONALIZATION_USAGE]["total_requests"] > 0:
                personalization_success_rate = (
                    self.metrics[MetricType.PERSONALIZATION_USAGE]["successful_personalizations"] /
                    self.metrics[MetricType.PERSONALIZATION_USAGE]["total_requests"]
                ) * 100

            error_rate = 0.0
            if self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"] > 0:
                error_rate = (
                    self.metrics[MetricType.ERROR_RATE]["total_errors"] /
                    self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"]
                ) * 100

            return {
                "timestamp": datetime.utcnow().isoformat(),
                "user_engagement": {
                    "total_sessions": self.metrics[MetricType.USER_ENGAGEMENT]["total_sessions"],
                    "unique_active_users": len(self.metrics[MetricType.USER_ENGAGEMENT]["active_users"]),
                    "total_page_views": self.metrics[MetricType.USER_ENGAGEMENT]["page_views"]
                },
                "translation_metrics": {
                    "total_requests": self.metrics[MetricType.TRANSLATION_SUCCESS]["total_requests"],
                    "successful_translations": self.metrics[MetricType.TRANSLATION_SUCCESS]["successful_translations"],
                    "failed_translations": self.metrics[MetricType.TRANSLATION_SUCCESS]["failed_translations"],
                    "success_rate_percent": round(translation_success_rate, 2),
                    "average_quality_score": round(self.metrics[MetricType.TRANSLATION_SUCCESS]["average_quality_score"], 2)
                },
                "personalization_metrics": {
                    "total_requests": self.metrics[MetricType.PERSONALIZATION_USAGE]["total_requests"],
                    "successful_personalizations": self.metrics[MetricType.PERSONALIZATION_USAGE]["successful_personalizations"],
                    "failed_personalizations": self.metrics[MetricType.PERSONALIZATION_USAGE]["failed_personalizations"],
                    "success_rate_percent": round(personalization_success_rate, 2)
                },
                "error_metrics": {
                    "total_errors": self.metrics[MetricType.ERROR_RATE]["total_errors"],
                    "error_rate_percent": round(error_rate, 2),
                    "recent_errors": self.metrics[MetricType.ERROR_RATE]["error_details"][-5:]  # Last 5 errors
                }
            }


# Global metrics collector instance
metrics_collector = MetricsCollector()