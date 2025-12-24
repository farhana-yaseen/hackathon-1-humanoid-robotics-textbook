from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from ..services.rag_service import RAGService
from ..services.rag_session_service import RAGSessionService, SelectedTextContextService
from ..database import get_db
from ..models.rag_session import RAGSession


# Create the RAG router
rag_router = APIRouter()


# Request models
class RAGQueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None  # Will be converted to UUID if provided


class SetSelectionContextRequest(BaseModel):
    selected_text: str
    session_id: str  # Required for setting selection context


class CreateSessionRequest(BaseModel):
    user_id: Optional[str] = None  # Will be converted to UUID if provided


# Response models
class RAGQueryResponse(BaseModel):
    response: str
    session_id: str
    selection_context_active: bool


class SessionResponse(BaseModel):
    session_id: str
    user_id: Optional[str] = None


class SetSelectionResponse(BaseModel):
    session_id: str
    selection_set: bool
    token_count: int


@rag_router.post("/sessions", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest, db: Session = Depends(get_db)):
    """
    Create a new RAG session for a user or anonymous session.
    """
    user_id_uuid = None
    if request.user_id:
        try:
            user_id_uuid = UUID(request.user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

    session = RAGSessionService.create_session(db, user_id_uuid)

    return SessionResponse(
        session_id=str(session.session_id),
        user_id=str(session.user_id) if session.user_id else None
    )


@rag_router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest, db: Session = Depends(get_db)):
    """
    Query the RAG system with optional session context.
    If a session is provided and has active selection context, the query will be answered based only on that selection.
    """
    rag_service = RAGService()

    # Convert session_id to UUID if provided
    session_id_uuid = None
    if request.session_id:
        try:
            session_id_uuid = UUID(request.session_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid session ID format"
            )

    # If no session ID provided, create a temporary session
    if not session_id_uuid:
        session = RAGSessionService.create_session(db, user_id=None)
        session_id_uuid = session.session_id

    # Update last interaction time for the session
    RAGSessionService.update_last_interaction(db, session_id_uuid)

    # Query the RAG system
    response = rag_service.query_with_context(db, session_id_uuid, request.query)

    # Check if selection context is active for this session
    session = RAGSessionService.get_session(db, session_id_uuid)
    selection_context_active = session.active_selection_context is not None if session else False

    return RAGQueryResponse(
        response=response,
        session_id=str(session_id_uuid),
        selection_context_active=selection_context_active
    )


@rag_router.post("/selection-context", response_model=SetSelectionResponse)
async def set_selection_context(request: SetSelectionContextRequest, db: Session = Depends(get_db)):
    """
    Set the active selection context for a session.
    This enables selection-based contextual RAG for subsequent queries.
    """
    try:
        session_id = UUID(request.session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )

    # Validate token length
    if len(request.selected_text) > 8000:  # Approx 2000 tokens
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected text exceeds 2000 token limit"
        )

    # Set the selection context
    updated_session = RAGSessionService.set_selection_context(db, session_id, request.selected_text)

    # Calculate approximate token count (4 chars per token)
    token_count = len(request.selected_text) // 4

    return SetSelectionResponse(
        session_id=str(session_id),
        selection_set=True,
        token_count=token_count
    )


@rag_router.post("/clear-selection", response_model=SessionResponse)
async def clear_selection_context(session_id: str, db: Session = Depends(get_db)):
    """
    Clear the active selection context for a session.
    This returns the RAG system to normal mode.
    """
    try:
        session_id_uuid = UUID(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )

    updated_session = RAGSessionService.clear_selection_context(db, session_id_uuid)

    if not updated_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    return SessionResponse(
        session_id=str(updated_session.session_id),
        user_id=str(updated_session.user_id) if updated_session.user_id else None
    )