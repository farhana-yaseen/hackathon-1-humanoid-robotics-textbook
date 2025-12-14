"""
Distributed tracing utilities for the Humanoid Robotics Textbook application.
Implements distributed tracing for request flows (FR-013).
"""
import uuid
import time
from contextvars import ContextVar
from datetime import datetime
from typing import Dict, Any, Optional
import threading


# Context variable to store the current trace ID
current_trace_id: ContextVar[Optional[str]] = ContextVar('current_trace_id', default=None)
current_span_id: ContextVar[Optional[str]] = ContextVar('current_span_id', default=None)


class TraceSpan:
    """
    Represents a single span in a distributed trace.
    """

    def __init__(self, name: str, trace_id: str, parent_span_id: Optional[str] = None):
        """
        Initialize a trace span.

        Args:
            name: Name of the span
            trace_id: ID of the overall trace
            parent_span_id: ID of the parent span (if any)
        """
        self.name = name
        self.trace_id = trace_id
        self.span_id = str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.attributes: Dict[str, Any] = {}
        self.events: list = []

    def set_attribute(self, key: str, value: Any):
        """
        Set an attribute on the span.

        Args:
            key: Attribute key
            value: Attribute value
        """
        self.attributes[key] = value

    def add_event(self, name: str, timestamp: Optional[float] = None, attributes: Optional[Dict[str, Any]] = None):
        """
        Add an event to the span.

        Args:
            name: Event name
            timestamp: Event timestamp (defaults to now)
            attributes: Event attributes
        """
        if timestamp is None:
            timestamp = time.time()

        self.events.append({
            "name": name,
            "timestamp": timestamp,
            "attributes": attributes or {}
        })

    def end(self):
        """End the span and record its duration."""
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        """Get the duration of the span in seconds."""
        if self.end_time is not None:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the span to a dictionary representation.

        Returns:
            Dictionary representation of the span
        """
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat() + "Z",
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() + "Z" if self.end_time else None,
            "duration_ms": round(self.duration * 1000, 2),
            "attributes": self.attributes,
            "events": self.events
        }


class Tracer:
    """
    Distributed tracer for tracking request flows across services.
    """

    def __init__(self):
        """Initialize the tracer."""
        self.spans: Dict[str, TraceSpan] = {}
        self.lock = threading.Lock()

    def start_trace(self, name: str, parent_span_id: Optional[str] = None) -> TraceSpan:
        """
        Start a new trace with a root span.

        Args:
            name: Name of the trace/root span
            parent_span_id: ID of the parent span (for distributed tracing)

        Returns:
            The root span of the trace
        """
        trace_id = str(uuid.uuid4())
        span = TraceSpan(name, trace_id, parent_span_id)

        with self.lock:
            self.spans[span.span_id] = span

        # Set the current trace and span in context
        current_trace_id.set(trace_id)
        current_span_id.set(span.span_id)

        return span

    def start_span(self, name: str, parent_span_id: Optional[str] = None) -> TraceSpan:
        """
        Start a new span within the current trace.

        Args:
            name: Name of the span
            parent_span_id: ID of the parent span (defaults to current span)

        Returns:
            The new span
        """
        trace_id = current_trace_id.get()
        if trace_id is None:
            # If no current trace, start a new one
            return self.start_trace(name, parent_span_id)

        if parent_span_id is None:
            parent_span_id = current_span_id.get()

        span = TraceSpan(name, trace_id, parent_span_id)

        with self.lock:
            self.spans[span.span_id] = span

        # Update the current span in context
        current_span_id.set(span.span_id)

        return span

    def end_span(self, span: TraceSpan):
        """
        End a span and record its completion.

        Args:
            span: The span to end
        """
        span.end()
        # In a real implementation, we would export the span to a tracing backend
        # For now, we'll just keep it in memory

    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        """
        Get all spans for a given trace ID.

        Args:
            trace_id: The ID of the trace to retrieve

        Returns:
            Dictionary containing trace information and all spans
        """
        trace_spans = []
        with self.lock:
            for span in self.spans.values():
                if span.trace_id == trace_id:
                    trace_spans.append(span.to_dict())

        return {
            "trace_id": trace_id,
            "spans": trace_spans,
            "total_spans": len(trace_spans)
        }

    def get_current_trace_info(self) -> Dict[str, Optional[str]]:
        """
        Get information about the current trace.

        Returns:
            Dictionary with current trace and span IDs
        """
        return {
            "trace_id": current_trace_id.get(),
            "span_id": current_span_id.get()
        }


# Global tracer instance
tracer = Tracer()


def trace_function(func_name: Optional[str] = None):
    """
    Decorator to trace a function call.

    Args:
        func_name: Optional name for the span (defaults to function name)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            span_name = func_name or func.__name__
            span = tracer.start_span(f"function.{span_name}")

            try:
                result = func(*args, **kwargs)
                span.set_attribute("status", "success")
                return result
            except Exception as e:
                span.set_attribute("status", "error")
                span.set_attribute("error.message", str(e))
                span.set_attribute("error.type", type(e).__name__)
                raise
            finally:
                tracer.end_span(span)

        return wrapper
    return decorator