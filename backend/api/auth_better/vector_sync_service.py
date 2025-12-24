"""
Vector Synchronization Service for Better-Auth feature
"""
from typing import Optional
from qdrant_client.http import models
import logging
from ..utils.qdrant_client import qdrant, QDRANT_AVAILABLE
from ..utils.gemini_client import embed_text
import json
from datetime import datetime


class VectorSyncService:
    def __init__(self):
        self.collection_name = "user_attributes"
        # Use the global QDRANT_AVAILABLE flag from qdrant_client
        if QDRANT_AVAILABLE:
            try:
                self._ensure_collection_exists()
            except Exception as e:
                logging.error(f"Error with Qdrant collection: {e}")

    def _ensure_collection_exists(self):
        """Ensure the user attributes collection exists in Qdrant."""
        try:
            collections = qdrant.get_collections().collections
            if any(c.name == self.collection_name for c in collections):
                return

            qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,   # Google text-embedding-004 embedding size
                    distance=models.Distance.COSINE
                )
            )
            logging.info(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logging.error(f"Error creating Qdrant collection: {e}")

    async def sync_user_profile_to_vector_db(self, user_id: str, profile_data: dict) -> bool:
        """
        Sync user profile data to Qdrant vector database
        """
        if not QDRANT_AVAILABLE:
            logging.warning(f"Qdrant service unavailable, skipping sync for user: {user_id}")
            return False

        try:
            # Create a text representation of the user's profile for embedding
            profile_text = self._create_profile_text(profile_data)

            # Generate embedding for the profile text
            try:
                embedding = embed_text(profile_text)
            except Exception as embed_error:
                logging.error(f"Failed to generate embedding for user {user_id}: {embed_error}")
                return False

            # Store in Qdrant
            qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=user_id,
                        vector=embedding,
                        payload={
                            "user_id": user_id,
                            "profile_data": profile_data,
                            "synced_at": datetime.utcnow().isoformat()
                        },
                    )
                ]
            )

            logging.info(f"Successfully synced user profile to vector DB: {user_id}")
            return True
        except Exception as e:
            logging.error(f"Error syncing user profile to vector DB: {e}")
            return False

    def _create_profile_text(self, profile_data: dict) -> str:
        """
        Create a text representation of the user's profile for embedding
        """
        profile_text = f"""
        Software Experience: {profile_data.get('software_background', 'Not specified')}
        Hardware Experience: {profile_data.get('hardware_background', 'Not specified')}
        Robotics Experience: {profile_data.get('robotics_experience', 'Not specified')}
        Programming Languages: {', '.join(profile_data.get('programming_languages', []) or ['Not specified'])}
        Hardware Platforms: {', '.join(profile_data.get('hardware_platforms', []) or ['Not specified'])}
        Years of Experience: {profile_data.get('years_of_experience', 0)}
        Primary Interest: {profile_data.get('primary_interest', 'Not specified')}
        Education Level: {profile_data.get('education_level', 'Not specified')}
        """
        return profile_text

    async def get_user_profile_from_vector_db(self, user_id: str) -> Optional[dict]:
        """
        Retrieve user profile from Qdrant vector database
        """
        if not QDRANT_AVAILABLE:
            logging.warning(f"Qdrant service unavailable, cannot retrieve user: {user_id}")
            return None

        try:
            results = qdrant.retrieve(
                collection_name=self.collection_name,
                ids=[user_id]
            )

            if results and len(results) > 0:
                return results[0].payload
            return None
        except Exception as e:
            logging.error(f"Error retrieving user profile from vector DB: {e}")
            return None

    async def delete_user_vector(self, user_id: str) -> bool:
        """
        Delete user vector from Qdrant when account is removed
        """
        if not QDRANT_AVAILABLE:
            logging.warning(f"Qdrant service unavailable, cannot delete user vector: {user_id}")
            return False

        try:
            qdrant.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[user_id]
                )
            )
            logging.info(f"Successfully deleted user vector: {user_id}")
            return True
        except Exception as e:
            logging.error(f"Error deleting user vector: {e}")
            return False

    async def update_user_vector(self, user_id: str, profile_data: dict) -> bool:
        """
        Update user vector in Qdrant when profile changes
        """
        return await self.sync_user_profile_to_vector_db(user_id, profile_data)