"""
verifySession Skill for Better-Auth feature
"""
from typing import Dict, Any, Optional
from .session_manager import session_manager


async def verifySession(token: str) -> Dict[str, Any]:
    """
    Verify Better-Auth session token and return session info.

    Args:
        token: The session token to verify

    Returns:
        Session information if valid, error info if invalid
    """
    payload = session_manager.verify_token(token)

    if payload:
        # Check if token is an access token
        token_type = payload.get("type", "access")
        if token_type in ["access", "refresh"]:
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "token_type": token_type,
                "expires_at": payload.get("exp")
            }
        else:
            return {
                "valid": False,
                "error": "Invalid token type"
            }
    else:
        return {
            "valid": False,
            "error": "Invalid or expired token"
        }


# For backward compatibility and testing
__all__ = ["verifySession"]