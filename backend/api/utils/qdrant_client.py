from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Instantiate global shared client
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

COLLECTION_NAME = "humanoid_robotics_book"


def create_collection_if_not_exists():
    """Ensure the collection exists in Qdrant."""
    collections = qdrant.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        return

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=1536,   # OpenAI embedding size
            distance=models.Distance.COSINE
        )
    )


def add_document_to_qdrant(doc_id: str, text: str, embedding: list):
    """Insert a document chunk into Qdrant."""
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


def search_qdrant(query_embedding: list, limit: int = 5):
    """Retrieve the most relevant chunks."""
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit,
    )
    return [hit.payload["text"] for hit in results]
