"""
Distributed tracing for the Humanoid Robotics Textbook Platform.
This module provides functionality for tracing request flows across services.
"""
import uuid
import time
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, Generator
import json
from pathlib import Path


@dataclass
class TraceSpan:
    """Represents a single span in a trace."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float]
    attributes: Dict[str, Any]
    status: str = "UNSET"  # UNSET, OK, ERROR


class Tracer:
    """Distributed tracer for tracking request flows."""

    def __init__(self, storage_path: str = "trace_data.json"):
        self.storage_path = Path(storage_path)
        self._lock = threading.Lock()
        self._spans = []
        self._active_spans = threading.local()  # Thread-local storage for active spans

    def start_trace(self, name: str, attributes: Dict[str, Any] = None) -> str:
        """Start a new trace with a root span."""
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())

        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            name=name,
            start_time=time.time(),
            end_time=None,
            attributes=attributes or {}
        )

        with self._lock:
            self._spans.append(span)

        # Store the active span in thread-local storage
        self._active_spans.current = span

        return trace_id

    def start_span(self, name: str, attributes: Dict[str, Any] = None) -> str:
        """Start a new span as a child of the current active span."""
        parent_span = getattr(self._active_spans, 'current', None)

        span_id = str(uuid.uuid4())
        trace_id = parent_span.trace_id if parent_span else str(uuid.uuid4())

        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span.span_id if parent_span else None,
            name=name,
            start_time=time.time(),
            end_time=None,
            attributes=attributes or {}
        )

        with self._lock:
            self._spans.append(span)

        # Temporarily store the previous span and set the new one as active
        if parent_span:
            span._previous = parent_span
        self._active_spans.current = span

        return span_id

    def end_span(self, span_id: str, status: str = "OK", attributes: Dict[str, Any] = None):
        """End a span with optional status and additional attributes."""
        with self._lock:
            for span in self._spans:
                if span.span_id == span_id:
                    span.end_time = time.time()
                    span.status = status
                    if attributes:
                        span.attributes.update(attributes)
                    break

        # Restore the previous span as active
        current_span = getattr(self._active_spans, 'current', None)
        if current_span and current_span.span_id == span_id:
            # This implementation assumes single level nesting for simplicity
            # In a real implementation, we'd need a proper stack
            self._active_spans.current = getattr(current_span, '_previous', None)

    @contextmanager
    def trace(self, name: str, attributes: Dict[str, Any] = None) -> Generator[str, None, None]:
        """Context manager for creating and managing spans."""
        span_id = self.start_span(name, attributes)
        try:
            yield span_id
            self.end_span(span_id, status="OK")
        except Exception as e:
            self.end_span(span_id, status="ERROR", attributes={"error": str(e)})
            raise

    def get_trace(self, trace_id: str) -> list:
        """Get all spans for a specific trace."""
        with self._lock:
            trace_spans = [span for span in self._spans if span.trace_id == trace_id]
            return sorted(trace_spans, key=lambda s: s.start_time)

    def get_recent_traces(self, limit: int = 100) -> list:
        """Get the most recent traces."""
        with self._lock:
            # Group spans by trace_id
            trace_groups = {}
            for span in self._spans[-1000:]:  # Look at last 1000 spans
                if span.trace_id not in trace_groups:
                    trace_groups[span.trace_id] = []
                trace_groups[span.trace_id].append(span)

            # Return the most recent traces
            recent_traces = list(trace_groups.values())[-limit:]
            return recent_traces

    def export_trace(self, trace_id: str, format: str = "json") -> str:
        """Export a trace in the specified format."""
        trace_spans = self.get_trace(trace_id)

        if format == "json":
            trace_data = []
            for span in trace_spans:
                span_data = {
                    "trace_id": span.trace_id,
                    "span_id": span.span_id,
                    "parent_span_id": span.parent_span_id,
                    "name": span.name,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                    "duration_ms": (span.end_time - span.start_time) * 1000 if span.end_time else None,
                    "attributes": span.attributes,
                    "status": span.status
                }
                trace_data.append(span_data)

            return json.dumps(trace_data, indent=2)

        return str(trace_spans)

    def save_traces(self):
        """Save traces to storage file."""
        try:
            # Export recent traces to file
            recent_traces = self.get_recent_traces(50)  # Save last 50 traces

            trace_data = []
            for trace in recent_traces:
                trace_dict = []
                for span in trace:
                    span_dict = {
                        "trace_id": span.trace_id,
                        "span_id": span.span_id,
                        "parent_span_id": span.parent_span_id,
                        "name": span.name,
                        "start_time": span.start_time,
                        "end_time": span.end_time,
                        "attributes": span.attributes,
                        "status": span.status
                    }
                    trace_dict.append(span_dict)
                trace_data.append(trace_dict)

            with open(self.storage_path, 'w') as f:
                json.dump(trace_data, f, indent=2)
        except Exception as e:
            print(f"Error saving traces: {e}")

    def load_traces(self):
        """Load traces from storage file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    trace_data = json.load(f)

                # Convert the loaded data back to TraceSpan objects
                spans = []
                for trace in trace_data:
                    for span_data in trace:
                        span = TraceSpan(
                            trace_id=span_data["trace_id"],
                            span_id=span_data["span_id"],
                            parent_span_id=span_data["parent_span_id"],
                            name=span_data["name"],
                            start_time=span_data["start_time"],
                            end_time=span_data["end_time"],
                            attributes=span_data["attributes"],
                            status=span_data.get("status", "UNSET")
                        )
                        spans.append(span)

                with self._lock:
                    self._spans = spans
            except Exception as e:
                print(f"Error loading traces: {e}")


# Global tracer instance
_tracer = Tracer()


def get_tracer() -> Tracer:
    """Get the global tracer instance."""
    return _tracer


# Convenience functions for tracing
def start_request_trace(request_id: str, user_id: str = None, endpoint: str = None) -> str:
    """Start a trace for an incoming request."""
    attributes = {"request_id": request_id}
    if user_id:
        attributes["user_id"] = user_id
    if endpoint:
        attributes["endpoint"] = endpoint

    return get_tracer().start_trace("request", attributes)


def trace_service_call(service_name: str, operation: str, attributes: Dict[str, Any] = None) -> Generator[str, None, None]:
    """Context manager to trace a service call."""
    attrs = attributes or {}
    attrs["service"] = service_name
    attrs["operation"] = operation

    return get_tracer().trace(f"{service_name}.{operation}", attrs)


def trace_database_operation(operation: str, table: str, attributes: Dict[str, Any] = None) -> Generator[str, None, None]:
    """Context manager to trace a database operation."""
    attrs = attributes or {}
    attrs["operation"] = operation
    attrs["table"] = table

    return get_tracer().trace(f"database.{operation}", attrs)


def trace_external_api_call(api_name: str, endpoint: str, attributes: Dict[str, Any] = None) -> Generator[str, None, None]:
    """Context manager to trace an external API call."""
    attrs = attributes or {}
    attrs["api"] = api_name
    attrs["endpoint"] = endpoint

    return get_tracer().trace(f"external_api.{api_name}", attrs)


def get_trace_info(trace_id: str) -> Dict[str, Any]:
    """Get information about a specific trace."""
    tracer = get_tracer()
    spans = tracer.get_trace(trace_id)

    if not spans:
        return {"error": "Trace not found"}

    # Calculate total duration
    start_time = min(span.start_time for span in spans)
    end_time = max(span.end_time or time.time() for span in spans)

    return {
        "trace_id": trace_id,
        "spans": len(spans),
        "total_duration_ms": (end_time - start_time) * 1000,
        "spans_info": [
            {
                "name": span.name,
                "duration_ms": (span.end_time - span.start_time) * 1000 if span.end_time else None,
                "status": span.status,
                "attributes": span.attributes
            }
            for span in spans
        ]
    }


# Middleware-like function for tracing requests
def trace_request_middleware(request_id: str, user_id: str = None, endpoint: str = None):
    """Middleware function to wrap request processing with tracing."""
    trace_id = start_request_trace(request_id, user_id, endpoint)

    class TracingContext:
        def __enter__(self):
            return trace_id

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                # In a real implementation, we might want to update spans with error info
                pass

    return TracingContext()


# Example usage decorator
def traced_function(service_name: str, operation: str):
    """Decorator to automatically trace function calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with trace_service_call(service_name, operation) as span_id:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    # In a real implementation, we'd want to update the span with error details
                    raise
        return wrapper
    return decorator


# Initialize the tracer
get_tracer().load_traces()