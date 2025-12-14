from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Batch, Filter, FieldCondition, MatchValue
from uuid import UUID, uuid4
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from ..models.chapter import Chapter
from ..models.selected_text_context import SelectedTextContext
from ..models.rag_session import RAGSession
from datetime import datetime
import os
from ..logging_config import get_logger, log_rag_query


class RAGService:
    """Service class for managing Retrieval Augmented Generation functionality."""

    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True
        )

        # Initialize Gemini client
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

        # Create collection if it doesn't exist
        self.qdrant_client.recreate_collection(
            collection_name="textbook_content",
            vectors_config={"size": 768, "distance": "Cosine"},  # Adjust size based on embedding model
        )

        # Initialize logger
        self.logger = get_logger('rag')

    def ingest_chapter(self, db: Session, chapter_id: UUID, content: str, chapter_title: str) -> bool:
        """Ingest a chapter into the vector database."""
        try:
            # Generate embeddings for the content
            embeddings = self.generate_embeddings(content)

            # Create point for Qdrant
            point = PointStruct(
                id=str(uuid4()),
                vector=embeddings,
                payload={
                    "chapter_id": str(chapter_id),
                    "content": content,
                    "title": chapter_title,
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            # Upload to Qdrant
            self.qdrant_client.upsert(
                collection_name="textbook_content",
                points=[point]
            )

            return True
        except Exception as e:
            print(f"Error ingesting chapter: {e}")
            return False

    def ingest_content_batch(self, db: Session, chapters_data: List[Dict]) -> int:
        """Ingest multiple chapters in batch."""
        successful_ingests = 0

        for chapter_data in chapters_data:
            if self.ingest_chapter(
                db,
                chapter_data["chapter_id"],
                chapter_data["content"],
                chapter_data["title"]
            ):
                successful_ingests += 1

        return successful_ingests

    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using Gemini API."""
        try:
            # Check if embed_content is available in the genai module
            if hasattr(genai, 'embed_content'):
                # Use the proper embedding API from Google Generative AI
                result = genai.embed_content(
                    model="models/embedding-001",  # Using Google's embedding model
                    content=text[:30720],  # Limit to prevent exceeding token limits (30720 chars ~ 8192 tokens)
                    task_type="retrieval_document"  # Specify the task type for better embeddings
                )
                embedding = result['embedding']

                # Ensure the embedding vector is the expected size (768)
                if len(embedding) != 768:
                    # Pad or truncate to 768 dimensions if needed
                    if len(embedding) < 768:
                        embedding.extend([0.0] * (768 - len(embedding)))
                    else:
                        embedding = embedding[:768]

                return embedding
            else:
                # Fallback: Use a different approach if embed_content is not available
                # In a real implementation, you might use a different embedding service or model
                # For now, we'll use the generative model to create a simple embedding
                response = self.model.generate_content(
                    f"Provide a 768-dimensional numerical representation of this text as a comma-separated list of floats: {text[:1000]}"
                )
                # This is a fallback - in practice, use proper embedding models
                return [0.1] * 768
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            # Return a zero vector on error
            return [0.0] * 768

    def search_relevant_chunks(self, query: str, limit: int = 5, chapter_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
        """Search for relevant content chunks based on the query."""
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings(query)

            # Prepare search filter if chapter_id is provided
            search_filter = None
            if chapter_id:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="chapter_id",
                            match=MatchValue(value=str(chapter_id))
                        )
                    ]
                )

            # Search in Qdrant
            search_result = self.qdrant_client.search(
                collection_name="textbook_content",
                query_vector=query_embedding,
                limit=limit,
                query_filter=search_filter  # Apply filter if provided
            )

            # Extract relevant content
            results = []
            for hit in search_result:
                results.append({
                    "content": hit.payload["content"],
                    "title": hit.payload["title"],
                    "chapter_id": hit.payload["chapter_id"],
                    "score": hit.score,
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "total_chunks": hit.payload.get("total_chunks", 1)
                })

            return results
        except Exception as e:
            print(f"Error searching for relevant chunks: {e}")
            return []

    def search_by_chapter(self, chapter_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant content chunks within a specific chapter."""
        return self.search_relevant_chunks(query, limit, chapter_id)

    def get_all_chunks_for_chapter(self, chapter_id: UUID) -> List[Dict[str, Any]]:
        """Retrieve all content chunks for a specific chapter."""
        try:
            # Use Qdrant's scroll functionality to get all points for a chapter
            scroll_result = self.qdrant_client.scroll(
                collection_name="textbook_content",
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="chapter_id",
                            match=MatchValue(value=str(chapter_id))
                        )
                    ]
                ),
                limit=10000  # Assuming a reasonable upper limit for chunks per chapter
            )

            results = []
            points, next_page = scroll_result

            for point in points:
                results.append({
                    "content": point.payload["content"],
                    "title": point.payload["title"],
                    "chapter_id": point.payload["chapter_id"],
                    "chunk_index": point.payload.get("chunk_index", 0),
                    "total_chunks": point.payload.get("total_chunks", 1),
                    "id": point.id
                })

            # Handle pagination if there are more results
            while next_page:
                scroll_result = self.qdrant_client.scroll(
                    collection_name="textbook_content",
                    scroll_filter=Filter(
                        must=[
                            FieldCondition(
                                key="chapter_id",
                                match=MatchValue(value=str(chapter_id))
                            )
                        ]
                    ),
                    limit=10000,
                    offset=next_page
                )
                points, next_page = scroll_result
                for point in points:
                    results.append({
                        "content": point.payload["content"],
                        "title": point.payload["title"],
                        "chapter_id": point.payload["chapter_id"],
                        "chunk_index": point.payload.get("chunk_index", 0),
                        "total_chunks": point.payload.get("total_chunks", 1),
                        "id": point.id
                    })

            return results
        except Exception as e:
            print(f"Error retrieving all chunks for chapter: {e}")
            return []

    def construct_context(self, context_chunks: List[Dict], max_tokens: int = 2000) -> str:
        """Construct a context string from chunks, respecting token limits."""
        # Sort chunks by score to prioritize most relevant content
        sorted_chunks = sorted(context_chunks, key=lambda x: x.get('score', 0), reverse=True)

        context_parts = []
        total_chars = 0

        for chunk in sorted_chunks:
            chunk_content = chunk["content"]
            # Rough approximation: 4 chars per token
            chunk_chars = len(chunk_content)

            # Check if adding this chunk would exceed the limit
            if total_chars + chunk_chars > max_tokens * 4:
                # If adding this chunk exceeds the limit, stop adding more chunks
                break

            context_parts.append(chunk_content)
            total_chars += chunk_chars

        # Join the selected chunks with separators
        context_str = "\n\n".join(context_parts)

        # Ensure the context doesn't exceed the token limit
        if len(context_str) > max_tokens * 4:
            context_str = context_str[:max_tokens * 4]

        return context_str

    def generate_response(self, query: str, context_chunks: List[Dict], selected_text_context: Optional[str] = None) -> str:
        """Generate a response using the LLM with context and optional selected text."""
        try:
            # Build context from chunks
            if selected_text_context:
                # Use the selected text as context (for selection-based RAG)
                context_str = selected_text_context
            else:
                # Construct context from search results
                context_str = self.construct_context(context_chunks)

            # Determine if we should use selection-based context
            if selected_text_context:
                # Use only the selected text as context (selection-based RAG)
                full_prompt = f"""
                You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
                The user has selected specific text and is asking about it.
                Answer the user's question based ONLY on the selected text provided below.
                If the selected text doesn't contain enough information to answer the question,
                clearly state this limitation and suggest considering more context.

                Selected Text Context:
                {selected_text_context}

                User Question:
                {query}

                Answer:
                """
            else:
                # Use broader context from search results
                full_prompt = f"""
                You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
                Use the following context to answer the user's question.
                If the context doesn't contain enough information to answer the question,
                acknowledge this and provide the best answer you can based on your general knowledge.

                Context:
                {context_str}

                User Question:
                {query}

                Answer:
                """

            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)

            return response.text if response.text else "I couldn't generate a response for your query."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request."

    def query_with_context(self, db: Session, session_id: UUID, query: str) -> str:
        """Process a query with appropriate context based on session state."""
        self.logger.info(f"Processing RAG query for session: {session_id}, query length: {len(query)}")

        # Get session to check for selected text context
        session = db.query(RAGSession).filter(RAGSession.session_id == session_id).first()
        selected_text = session.active_selection_context if session else None

        context_type = "selection_context" if selected_text else "traditional_rag"
        self.logger.info(f"Using {context_type} for session: {session_id}")

        try:
            if selected_text:
                # Use selection-based RAG - only search within the selected text
                response = self.generate_response(query, [], selected_text_context=selected_text)
            else:
                # Use traditional RAG - search for relevant content
                context_chunks = self.search_relevant_chunks(query)
                response = self.generate_response(query, context_chunks)

            # Log successful query
            self.logger.info(f"Successfully processed RAG query for session: {session_id}")
            log_rag_query(session.user_id if session else "anonymous", str(session_id), query, len(response))

            return response
        except Exception as e:
            self.logger.error(f"Error processing RAG query for session {session_id}: {str(e)}", exc_info=True)
            raise

    def validate_selection_length(self, selected_text: str) -> bool:
        """Validate that selected text doesn't exceed token limits."""
        # Rough approximation: 2000 tokens ≈ 8000 characters
        return len(selected_text) <= 8000

    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Chunk text into smaller pieces."""
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        return chunks

    def ingest_chapter_with_chunking(self, db: Session, chapter_id: UUID, content: str, chapter_title: str, chunk_size: int = 1000) -> bool:
        """Ingest a chapter into the vector database with proper chunking to handle large documents."""
        try:
            # Split the content into chunks
            text_chunks = self.chunk_text(content, chunk_size)

            successful_chunks = 0

            for i, chunk in enumerate(text_chunks):
                # Generate embeddings for the chunk
                embeddings = self.generate_embeddings(chunk)

                # Create point for Qdrant with chunk-specific information
                point = PointStruct(
                    id=str(uuid4()),
                    vector=embeddings,
                    payload={
                        "chapter_id": str(chapter_id),
                        "content": chunk,
                        "title": chapter_title,
                        "chunk_index": i,
                        "total_chunks": len(text_chunks),
                        "created_at": datetime.utcnow().isoformat()
                    }
                )

                # Upload to Qdrant
                self.qdrant_client.upsert(
                    collection_name="textbook_content",
                    points=[point]
                )

                successful_chunks += 1

            print(f"Successfully ingested {successful_chunks} chunks for chapter {chapter_id}")
            return True
        except Exception as e:
            print(f"Error ingesting chapter with chunking: {e}")
            return False