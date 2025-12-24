from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import logging

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Initialize client safely
qdrant = None
QDRANT_AVAILABLE = False

if QDRANT_URL and QDRANT_API_KEY:
    try:
        qdrant = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        # Test connection
        qdrant.get_collections()
        QDRANT_AVAILABLE = True
        logging.info("Qdrant client initialized successfully")
    except Exception as e:
        logging.error(f"Failed to connect to Qdrant: {e}")
        qdrant = None
        QDRANT_AVAILABLE = False
else:
    logging.warning("QDRANT_URL or QDRANT_API_KEY not set, Qdrant functionality disabled")

COLLECTION_NAME = "humanoid_robotics_book"


def create_collection_if_not_exists():
    """Ensure the collection exists in Qdrant."""
    if not QDRANT_AVAILABLE:
        logging.warning("Qdrant not available, skipping collection creation")
        return

    try:
        collections = qdrant.get_collections().collections
        if any(c.name == COLLECTION_NAME for c in collections):
            return

        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=768,   # Google text-embedding-004 embedding size
                distance=models.Distance.COSINE
            )
        )
    except Exception as e:
        logging.error(f"Failed to create Qdrant collection: {e}")


def add_document_to_qdrant(doc_id: str, text: str, embedding: list):
    """Insert a document chunk into Qdrant."""
    if not QDRANT_AVAILABLE:
        logging.warning("Qdrant not available, skipping document addition")
        return

    try:
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={"text": text},
                )
            ]
        )
    except Exception as e:
        logging.error(f"Failed to add document to Qdrant: {e}")


def search_qdrant(query_embedding: list, limit: int = 5):
    """Retrieve the most relevant chunks."""
    if not QDRANT_AVAILABLE:
        logging.warning("Qdrant not available, returning empty results")
        return []

    try:
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit,
        )
        return [hit.payload["text"] for hit in results]
    except Exception as e:
        logging.error(f"Failed to search Qdrant: {e}")
        return []
