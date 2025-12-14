from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
from ..services.translation_service import TranslationService
from ..database import get_db
from ..models.chapter import Chapter


# Create the translation router
translation_router = APIRouter()


# Request models
class TranslateChapterRequest(BaseModel):
    chapter_id: str  # Will be converted to UUID
    target_language: str = "Urdu"
    user_session_id: Optional[str] = None


class TranslateTextRequest(BaseModel):
    text: str
    target_language: str = "Urdu"


# Response models
class TranslateChapterResponse(BaseModel):
    translated_content: str
    chapter_id: str
    target_language: str
    cached: bool


class TranslateTextResponse(BaseModel):
    translated_text: str
    target_language: str


@translation_router.post("/chapters/{chapter_id}/translate", response_model=TranslateChapterResponse)
async def translate_chapter(
    chapter_id: str,
    request: TranslateChapterRequest,
    db: Session = Depends(get_db)
):
    """
    Translate a chapter to the target language with caching.
    """
    try:
        chapter_uuid = UUID(chapter_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chapter ID format"
        )

    # Verify the chapter exists
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_uuid).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    translation_service = TranslationService()

    # Translate the chapter content with caching
    translated_content = translation_service.translate_content_with_cache(
        db,
        chapter_uuid,
        chapter.content,
        request.target_language,
        request.user_session_id
    )

    # Check if this was a cached translation
    cached_translation = translation_service.get_cached_translation(
        db,
        chapter_uuid,
        request.user_session_id
    )
    is_cached = cached_translation is not None and cached_translation.urdu_content == translated_content

    return TranslateChapterResponse(
        translated_content=translated_content,
        chapter_id=str(chapter_uuid),
        target_language=request.target_language,
        cached=is_cached
    )


@translation_router.post("/text", response_model=TranslateTextResponse)
async def translate_text(request: TranslateTextRequest):
    """
    Translate a piece of text to the target language.
    """
    translation_service = TranslationService()

    # Translate the provided text
    translated_text = translation_service.translate_text_chunk(
        request.text,
        request.target_language
    )

    return TranslateTextResponse(
        translated_text=translated_text,
        target_language=request.target_language
    )


@translation_router.post("/chatbot-response", response_model=TranslateTextResponse)
async def translate_chatbot_response(request: TranslateTextRequest):
    """
    Translate a chatbot response to the target language.
    """
    translation_service = TranslationService()

    # Translate the chatbot response
    translated_response = translation_service.translate_chatbot_response(
        request.text,
        request.target_language
    )

    return TranslateTextResponse(
        translated_text=translated_response,
        target_language=request.target_language
    )