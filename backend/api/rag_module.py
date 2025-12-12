"""
Modular RAG (Retrieval-Augmented Generation) component for the humanoid robotics textbook.

This module provides a modular implementation of the RAG functionality that can be easily
integrated into the backend system. It handles the complete RAG pipeline:
1. Embedding user queries
2. Retrieving relevant context from vector database
3. Generating responses using LLM
4. Streaming responses to the client
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
import logging
from pydantic import BaseModel

from api.utils.gemini_client import embed_text
from api.utils.qdrant_client import search_qdrant
from api.utils.db import save_query
from api.utils.chatkit_client import create_chat_session, stream_message
from api.utils.better_auth_integration import BetterAuthIntegration


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGQuery(BaseModel):
    """Request model for RAG queries."""
    user_id: str
    question: str
    context_limit: Optional[int] = 5
    stream_response: Optional[bool] = True


class RAGService:
    """
    Service class for RAG operations.

    This class encapsulates all RAG-related functionality in a modular,
    testable way that can be easily integrated with other components.
    """

    def __init__(self):
        """Initialize the RAG service with required dependencies."""
        logger.info("Initializing RAG Service")

    def embed_query(self, question: str) -> List[float]:
        """
        Generate embeddings for the input question.

        Args:
            question: The user's question to embed

        Returns:
            List of embedding values as floats
        """
        try:
            logger.debug(f"Embedding query: {question[:50]}...")
            embedding = embed_text(question)
            logger.debug(f"Generated embedding of length: {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")

    def retrieve_context(self, query_embedding: List[float], limit: int = 5) -> str:
        """
        Retrieve relevant context from the vector database.

        Args:
            query_embedding: The embedding of the user's question
            limit: Maximum number of context chunks to retrieve

        Returns:
            Combined context string from retrieved chunks
        """
        try:
            logger.debug(f"Retrieving context with limit: {limit}")
            retrieved_chunks = search_qdrant(query_embedding, limit)
            combined_context = "\n\n".join(retrieved_chunks) if retrieved_chunks else ""
            logger.debug(f"Retrieved context with {len(retrieved_chunks)} chunks")
            return combined_context
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve context from database")

    async def generate_streaming_response(self, session_id: str, user_id: str, question: str, context: str):
        """
        Generate a streaming response for the user's question with personalization.

        Args:
            session_id: Unique identifier for the chat session
            user_id: Unique identifier for the user (for personalization)
            question: The user's question
            context: Retrieved context to inform the response

        Yields:
            String chunks of the generated response
        """
        try:
            logger.debug(f"Generating streaming response for session: {session_id}, user: {user_id}")
            answer_chunks = []

            # Get user profile for personalization if available
            auth_service = BetterAuthIntegration()
            user_profile = await auth_service.get_user_profile_from_db_and_qdrant(user_id) if user_id else None

            # Prepare personalized context if user profile exists
            personalized_context = context
            if user_profile:
                # Enhance context with user background for personalization
                background_info = f"""
                USER BACKGROUND FOR PERSONALIZATION:
                - Software Experience: {user_profile.get('software_experience', 'Not specified')}
                - Hardware Experience: {user_profile.get('hardware_experience', 'Not specified')}
                - Robotics Experience: {user_profile.get('robotics_experience', 'Not specified')}
                - Programming Languages: {', '.join(user_profile.get('programming_languages', [])) or 'Not specified'}
                - Hardware Platforms: {', '.join(user_profile.get('hardware_platforms', [])) or 'Not specified'}
                - Years of Experience: {user_profile.get('years_of_experience', 'Not specified')}
                - Primary Interest: {user_profile.get('primary_interest', 'Not specified')}
                - Education Level: {user_profile.get('education_level', 'Not specified')}

                ADAPT THE RESPONSE TO THE USER'S EXPERIENCE LEVEL AND INTERESTS.
                """
                personalized_context = f"{context}\n\n{background_info}"

            for chunk in stream_message(session_id=session_id, message=question, context=personalized_context):
                answer_chunks.append(chunk)
                yield f"data: {chunk}\n\n"

            # Save the full answer to the database
            full_answer = "".join(answer_chunks)
            logger.info(f"Saving query to database: {question[:50]}...")
            save_query_sync = lambda q, a: save_query(q, a)
            save_query_sync(question, full_answer)

        except Exception as e:
            logger.error(f"Error generating streaming response: {str(e)}")
            yield f"data: Error: {str(e)}\n\n"

    async def process_query(self, user_id: str, question: str, context_limit: int = 5) -> str:
        """
        Process a complete RAG query synchronously with personalization.

        Args:
            user_id: Unique identifier for the user
            question: The user's question
            context_limit: Maximum number of context chunks to retrieve

        Returns:
            Complete response string
        """
        # 1. Embed the question
        query_embedding = self.embed_query(question)

        # 2. Retrieve relevant context
        context = self.retrieve_context(query_embedding, context_limit)

        # 3. Get user profile for personalization if available
        auth_service = BetterAuthIntegration()
        user_profile = await auth_service.get_user_profile_from_db_and_qdrant(user_id) if user_id else None

        # 4. Prepare personalized context if user profile exists
        personalized_context = context
        if user_profile:
            # Enhance context with user background for personalization
            background_info = f"""
            USER BACKGROUND FOR PERSONALIZATION:
            - Software Experience: {user_profile.get('software_experience', 'Not specified')}
            - Hardware Experience: {user_profile.get('hardware_experience', 'Not specified')}
            - Robotics Experience: {user_profile.get('robotics_experience', 'Not specified')}
            - Programming Languages: {', '.join(user_profile.get('programming_languages', [])) or 'Not specified'}
            - Hardware Platforms: {', '.join(user_profile.get('hardware_platforms', [])) or 'Not specified'}
            - Years of Experience: {user_profile.get('years_of_experience', 'Not specified')}
            - Primary Interest: {user_profile.get('primary_interest', 'Not specified')}
            - Education Level: {user_profile.get('education_level', 'Not specified')}

            ADAPT THE RESPONSE TO THE USER'S EXPERIENCE LEVEL AND INTERESTS.
            """
            personalized_context = f"{context}\n\n{background_info}"

        # 5. Create or get chat session
        session = create_chat_session(user_id)

        # 6. Generate response
        response_chunks = []
        for chunk in stream_message(session_id=session, message=question, context=personalized_context):
            response_chunks.append(chunk)

        return "".join(response_chunks)


# Create router for RAG endpoints
router = APIRouter(prefix="/rag", tags=["rag"])


@router.get("/chat-stream")
async def rag_chat_stream_endpoint(user_id: str, question: str):
    """
    Streaming RAG chatbot endpoint using Google Gemini.

    This endpoint streams the AI response as it is generated, providing
    a real-time chat experience for users.

    Args:
        user_id: Unique identifier for the requesting user
        question: The question to ask the RAG system

    Returns:
        StreamingResponse: Server-sent events with response chunks
    """
    logger.info(f"Received RAG stream request for user: {user_id}")

    # Initialize RAG service
    rag_service = RAGService()

    # 1. Embed question
    query_embedding = rag_service.embed_query(question)

    # 2. Retrieve context from Qdrant
    context = rag_service.retrieve_context(query_embedding)

    # 3. Create or get ChatKit session
    session = create_chat_session(user_id)

    # 4. Generator function to yield SSE data
    async def event_generator():
        async for chunk in rag_service.generate_streaming_response(session, user_id, question, context):
            yield chunk

    logger.info(f"Starting streaming response for user: {user_id}")
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/chat-sync")
async def rag_chat_sync_endpoint(query: RAGQuery):
    """
    Synchronous RAG chatbot endpoint.

    This endpoint processes the RAG query and returns the complete response
    when it's ready, useful for applications that need the full response
    at once.

    Args:
        query: RAGQuery model containing user_id, question, and optional parameters

    Returns:
        dict: Contains the complete response and metadata
    """
    logger.info(f"Received synchronous RAG request for user: {query.user_id}")

    try:
        rag_service = RAGService()
        response = await rag_service.process_query(
            query.user_id,
            query.question,
            query.context_limit
        )

        return {
            "user_id": query.user_id,
            "question": query.question,
            "response": response,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error in synchronous RAG endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def rag_health_check():
    """
    Health check endpoint for the RAG service.

    Returns the status of the RAG service and its dependencies.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "RAG",
        "message": "RAG service is running and ready to process queries"
    }


# Export the service and router for use in other modules
__all__ = ["RAGService", "router"]