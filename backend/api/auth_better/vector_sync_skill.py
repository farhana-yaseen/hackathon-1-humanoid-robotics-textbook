"""
syncUserVector Skill for Better-Auth feature
"""
from typing import Dict, Any
from .vector_sync_service import VectorSyncService


async def syncUserVector(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate embeddings with ChatKit and store vector in Qdrant.

    Args:
        user_id: The user's unique identifier
        profile_data: User profile data to generate embeddings for

    Returns:
        Status of the vector synchronization
    """
    service = VectorSyncService()

    success = await service.sync_user_profile_to_vector_db(user_id, profile_data)

    if success:
        return {
            "status": "success",
            "message": "User vector synchronized successfully",
            "user_id": user_id
        }
    else:
        return {
            "status": "error",
            "message": "Failed to synchronize user vector",
            "user_id": user_id
        }


# For backward compatibility and testing
__all__ = ["syncUserVector"]