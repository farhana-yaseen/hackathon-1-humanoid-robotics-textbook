"""
Utility functions for content hashing and cache key generation
"""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional


def generate_content_hash(content: str, target_language: str = "ur") -> str:
    """
    Generate a hash for the content and target language combination.

    Args:
        content: The content to hash
        target_language: The target language code (default: "ur" for Urdu)

    Returns:
        SHA-256 hash of the content and language combination
    """
    content_to_hash = f"{content}:{target_language}".encode('utf-8')
    return hashlib.sha256(content_to_hash).hexdigest()


def generate_cache_key(content: str, target_language: str = "ur") -> str:
    """
    Generate a cache key for the content and target language combination.

    Args:
        content: The content to create a cache key for
        target_language: The target language code (default: "ur" for Urdu)

    Returns:
        Cache key combining the hash and language
    """
    content_hash = generate_content_hash(content, target_language)
    return f"{content_hash}:{target_language}"


def get_cache_expiration(hours: int = 24) -> datetime:
    """
    Get the cache expiration time.

    Args:
        hours: Number of hours until expiration (default: 24)

    Returns:
        Datetime object representing the expiration time
    """
    return datetime.now(timezone.utc) + timedelta(hours=hours)


def is_cache_expired(expires_at: datetime) -> bool:
    """
    Check if a cache entry has expired.

    Args:
        expires_at: The expiration datetime

    Returns:
        True if expired, False otherwise
    """
    return datetime.now(timezone.utc) > expires_at


def get_content_length(content: str) -> int:
    """
    Get the length of the content in characters.

    Args:
        content: The content to measure

    Returns:
        Length of the content in characters
    """
    return len(content)