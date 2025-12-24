"""
Metrics collection for the Humanoid Robotics Textbook Platform.
This module provides functionality for tracking user engagement,
RAG response quality, translation success rates, and error rates.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import time
import threading
from collections import defaultdict, deque
import json
from pathlib import Path


class MetricType(Enum):
    """Types of metrics that can be collected."""
    USER_ENGAGEMENT = "user_engagement"
    RAG_RESPONSE = "rag_response"
    TRANSLATION = "translation"
    ERROR_RATE = "error_rate"
    API_CALL = "api_call"


@dataclass
class MetricEvent:
    """Represents a single metric event."""
    metric_type: MetricType
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    data: Dict[str, Any]


class MetricsCollector:
    """Collects and manages application metrics."""

    def __init__(self, storage_path: str = "metrics_data.json"):
        self.storage_path = Path(storage_path)
        self._lock = threading.Lock()
        self._events = deque(maxlen=10000)  # Keep last 10,000 events
        self._counters = defaultdict(int)
        self._timers = defaultdict(list)

        # Load existing metrics if file exists
        self._load_metrics()

    def _load_metrics(self):
        """Load metrics from storage file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    # For simplicity, we'll just track the counters from the saved data
                    if 'counters' in data:
                        for key, value in data['counters'].items():
                            self._counters[key] = value
            except Exception:
                pass  # If loading fails, start with empty metrics

    def _save_metrics(self):
        """Save metrics to storage file."""
        try:
            data = {
                'counters': dict(self._counters),
                'timestamp': datetime.utcnow().isoformat()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass  # If saving fails, continue without error

    def record_event(self, metric_type: MetricType, user_id: Optional[str] = None,
                     session_id: Optional[str] = None, **data):
        """Record a new metric event."""
        event = MetricEvent(
            metric_type=metric_type,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            session_id=session_id,
            data=data
        )

        with self._lock:
            self._events.append(event)

            # Update counters based on metric type
            counter_key = f"{metric_type.value}_count"
            self._counters[counter_key] += 1

            # Specific counter updates
            if metric_type == MetricType.TRANSLATION:
                success = data.get('success', True)
                self._counters['translation_success' if success else 'translation_failure'] += 1
            elif metric_type == MetricType.RAG_RESPONSE:
                self._counters['rag_query_count'] += 1
                response_time = data.get('response_time_ms', 0)
                self._timers['rag_response_times'].append(response_time)
            elif metric_type == MetricType.ERROR_RATE:
                self._counters['error_count'] += 1
            elif metric_type == MetricType.USER_ENGAGEMENT:
                action = data.get('action', 'unknown')
                self._counters[f'user_action_{action}'] += 1

        # Save metrics periodically
        if self._counters['total_events'] % 100 == 0:
            self._save_metrics()

    def increment_counter(self, name: str, value: int = 1):
        """Increment a named counter."""
        with self._lock:
            self._counters[name] += value

    def record_timer(self, name: str, value: float):
        """Record a timing value."""
        with self._lock:
            self._timers[name].append(value)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics."""
        with self._lock:
            summary = {
                'counters': dict(self._counters),
                'timers': {},
                'event_count': len(self._events)
            }

            # Calculate timer statistics
            for timer_name, values in self._timers.items():
                if values:
                    summary['timers'][timer_name] = {
                        'count': len(values),
                        'avg': sum(values) / len(values),
                        'min': min(values),
                        'max': max(values),
                        'p95': sorted(values)[int(len(values) * 0.95)] if len(values) > 0 else 0
                    }
                else:
                    summary['timers'][timer_name] = {
                        'count': 0,
                        'avg': 0,
                        'min': 0,
                        'max': 0,
                        'p95': 0
                    }

            return summary

    def get_user_engagement_metrics(self) -> Dict[str, Any]:
        """Get user engagement specific metrics."""
        with self._lock:
            total_users = len(set(e.user_id for e in self._events if e.user_id))
            total_sessions = len(set(e.session_id for e in self._events if e.session_id))

            # Count specific user actions
            action_counts = {}
            for key, value in self._counters.items():
                if key.startswith('user_action_'):
                    action_counts[key] = value

            return {
                'total_users': total_users,
                'total_sessions': total_sessions,
                'user_actions': action_counts,
                'total_events': self._counters.get('user_engagement_count', 0)
            }

    def get_rag_metrics(self) -> Dict[str, Any]:
        """Get RAG-specific metrics."""
        with self._lock:
            success_count = self._counters.get('rag_query_count', 0)
            response_times = self._timers.get('rag_response_times', [])

            avg_response_time = sum(response_times) / len(response_times) if response_times else 0

            return {
                'total_queries': success_count,
                'avg_response_time_ms': avg_response_time,
                'p95_response_time_ms': sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0,
                'min_response_time_ms': min(response_times) if response_times else 0,
                'max_response_time_ms': max(response_times) if response_times else 0
            }

    def get_translation_metrics(self) -> Dict[str, Any]:
        """Get translation-specific metrics."""
        with self._lock:
            success_count = self._counters.get('translation_success', 0)
            failure_count = self._counters.get('translation_failure', 0)
            total_attempts = success_count + failure_count
            success_rate = (success_count / total_attempts * 100) if total_attempts > 0 else 0

            return {
                'total_attempts': total_attempts,
                'success_count': success_count,
                'failure_count': failure_count,
                'success_rate_percent': success_rate
            }

    def get_error_metrics(self) -> Dict[str, Any]:
        """Get error-specific metrics."""
        with self._lock:
            total_errors = self._counters.get('error_count', 0)
            total_requests = sum(v for k, v in self._counters.items() if k.endswith('_count'))
            error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0

            return {
                'total_errors': total_errors,
                'total_requests': total_requests,
                'error_rate_percent': error_rate
            }


# Global metrics collector instance
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _metrics_collector


# Convenience functions for recording specific metrics
def record_user_engagement(user_id: str, action: str, session_id: str = None, **details):
    """Record a user engagement metric."""
    collector = get_metrics_collector()
    collector.record_event(
        MetricType.USER_ENGAGEMENT,
        user_id=user_id,
        session_id=session_id,
        action=action,
        **details
    )


def record_rag_response(user_id: str, session_id: str, query: str, response: str,
                       response_time_ms: float, context_type: str = "traditional"):
    """Record a RAG response metric."""
    collector = get_metrics_collector()
    collector.record_event(
        MetricType.RAG_RESPONSE,
        user_id=user_id,
        session_id=session_id,
        query_length=len(query),
        response_length=len(response),
        response_time_ms=response_time_ms,
        context_type=context_type
    )


def record_translation(user_id: str, chapter_id: str, success: bool,
                      source_language: str = "English", target_language: str = "Urdu",
                      content_length: int = 0):
    """Record a translation metric."""
    collector = get_metrics_collector()
    collector.record_event(
        MetricType.TRANSLATION,
        user_id=user_id,
        session_id=chapter_id,  # Using chapter_id as session_id for translation
        success=success,
        source_language=source_language,
        target_language=target_language,
        content_length=content_length
    )


def record_error(error_type: str, user_id: str = None, endpoint: str = None, **details):
    """Record an error metric."""
    collector = get_metrics_collector()
    collector.record_event(
        MetricType.ERROR_RATE,
        user_id=user_id,
        data={
            'error_type': error_type,
            'endpoint': endpoint,
            **details
        }
    )


def record_api_call(endpoint: str, method: str, response_time_ms: float,
                   status_code: int, user_id: str = None):
    """Record an API call metric."""
    collector = get_metrics_collector()
    collector.record_event(
        MetricType.API_CALL,
        user_id=user_id,
        data={
            'endpoint': endpoint,
            'method': method,
            'response_time_ms': response_time_ms,
            'status_code': status_code
        }
    )


def get_all_metrics() -> Dict[str, Any]:
    """Get all collected metrics."""
    collector = get_metrics_collector()
    return {
        'summary': collector.get_metrics_summary(),
        'user_engagement': collector.get_user_engagement_metrics(),
        'rag': collector.get_rag_metrics(),
        'translation': collector.get_translation_metrics(),
        'errors': collector.get_error_metrics()
    }


def get_metrics_endpoint():
    """FastAPI endpoint function to expose metrics."""
    def endpoint():
        return get_all_metrics()
    return endpoint


# Context manager for timing operations
class Timer:
    """Context manager for timing operations."""

    def __init__(self, name: str):
        self.name = name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            collector = get_metrics_collector()
            collector.record_timer(self.name, duration_ms)