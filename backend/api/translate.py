from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.database import get_db
from api.repositories.translation_cache_repository import TranslationCacheRepository
from api.utils.content_hasher import generate_content_hash, get_cache_expiration, is_cache_expired, get_content_length
import asyncio
import time

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslateRequest(BaseModel):
    chapter_title: str = ""
    chapter_content: str
    target_language: str

class TranslateChapterRequest(BaseModel):
    chapter_id: str
    target_language: str
    user_session_id: Optional[str] = None

class TranslateResponse(BaseModel):
    translated_content: str

@router.post("/translate-content")
async def translate_content(request: TranslateRequest, db: AsyncSession = Depends(get_db)):
    """
    Translate chapter content to the specified language with caching and timeout.
    """
    start_time = time.time()

    try:
        chapter_content = request.chapter_content
        chapter_title = request.chapter_title
        target_language = request.target_language

        # Validate target language
        if target_language.lower() not in ['ur', 'urdu']:
            raise HTTPException(status_code=400, detail="Only Urdu (ur) translation is supported")

        # Generate content hash for cache lookup
        content_hash = generate_content_hash(chapter_content, target_language)

        # Check if translation is already cached
        translation_cache_repo = TranslationCacheRepository(db)
        cached_translation = await translation_cache_repo.get_by_hash_and_language(content_hash, target_language)

        if cached_translation and not is_cache_expired(cached_translation.expires_at):
            logger.info("Returning cached translation")
            return TranslateResponse(translated_content=cached_translation.translated_content)

        # Create a prompt for Gemini to translate the content
        prompt = f"""
        Translate the following textbook content to Urdu (اردو) while preserving:
        1. Technical accuracy
        2. Educational value
        3. Proper terminology
        4. Context and meaning

        CHAPTER TITLE: {chapter_title}

        ORIGINAL CONTENT:
        {chapter_content}

        Please return only the translated content in Urdu, no additional commentary.
        Use appropriate Urdu text direction and formatting.
        Use proper formatting for headings, paragraphs, lists, etc. to maintain readability.
        """

        # Import gemini_client at the module level to ensure it's available
        from api.utils.gemini_client import generate_translation

        # Add timeout functionality
        try:
            # Create an async task for the translation with timeout
            async def run_translation():
                return generate_translation(prompt)

            # Execute with 30 second timeout
            translated_content = await asyncio.wait_for(
                run_translation(),
                timeout=30.0  # 30 seconds timeout
            )
        except asyncio.TimeoutError:
            logger.error("Translation request timed out after 30 seconds")
            raise HTTPException(
                status_code=408,
                detail="Translation request timed out. Please try again."
            )

        # Save to cache with expiration
        expiration_time = get_cache_expiration(hours=24)  # Cache for 24 hours
        original_content_length = get_content_length(chapter_content)
        await translation_cache_repo.create(
            content_hash=content_hash,
            target_language=target_language,
            translated_content=translated_content,
            expires_at=expiration_time,
            original_content_length=original_content_length
        )

        elapsed_time = time.time() - start_time
        logger.info(f"Translation completed in {elapsed_time:.2f} seconds")

        return TranslateResponse(translated_content=translated_content)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error translating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error translating content: {str(e)}")

@router.post("/v1/translation/chapters/{chapter_id}/translate")
async def translate_chapter(chapter_id: str, translate_request: TranslateChapterRequest, db: AsyncSession = Depends(get_db)):
    """
    Translate a specific chapter to the target language with caching and timeout.
    This endpoint matches the frontend API expectation.
    """
    start_time = time.time()

    try:
        logger.info(f"Translating chapter {chapter_id} to {translate_request.target_language}")

        # Validate target language
        if translate_request.target_language.lower() not in ['urdu', 'ur']:
            raise HTTPException(status_code=400, detail="Only Urdu translation is supported")

        # For this implementation, we'll use the chapter_id as part of the content hash
        # In a real implementation, you would fetch the actual chapter content by chapter_id
        content_to_translate = f"Chapter ID: {chapter_id}"
        content_hash = generate_content_hash(content_to_translate, translate_request.target_language)

        # Check if translation is already cached
        translation_cache_repo = TranslationCacheRepository(db)
        cached_translation = await translation_cache_repo.get_by_hash_and_language(content_hash, translate_request.target_language)

        if cached_translation and not is_cache_expired(cached_translation.expires_at):
            logger.info("Returning cached translation for chapter")
            return TranslateResponse(translated_content=cached_translation.translated_content)

        # Create a prompt for Gemini to translate the content
        # In a real implementation, you would fetch the actual chapter content by chapter_id
        # For now, we'll create a translation prompt based on the chapter_id
        prompt = f"""
        Translate the following textbook chapter content to Urdu (اردو) while preserving:
        1. Technical accuracy
        2. Educational value
        3. Proper terminology
        4. Context and meaning

        CHAPTER ID/NAME: {chapter_id}

        Since we don't have the actual chapter content in this context, please provide a general
        translation framework for a chapter with this identifier. The translation should be
        educational, technically accurate, and preserve the meaning of robotics/humanoid concepts.

        Please return only the translated content in Urdu, no additional commentary.
        Use appropriate Urdu text direction and formatting.
        Use proper formatting for headings, paragraphs, lists, etc. to maintain readability.
        """

        # Import gemini_client at the module level to ensure it's available
        from api.utils.gemini_client import generate_translation

        # Add timeout functionality
        try:
            # Create an async task for the translation with timeout
            async def run_translation():
                return generate_translation(prompt)

            # Execute with 30 second timeout
            translated_content = await asyncio.wait_for(
                run_translation(),
                timeout=30.0  # 30 seconds timeout
            )
        except asyncio.TimeoutError:
            logger.error(f"Translation request for chapter {chapter_id} timed out after 30 seconds")
            raise HTTPException(
                status_code=408,
                detail="Translation request timed out. Please try again."
            )

        # Save to cache with expiration
        expiration_time = get_cache_expiration(hours=24)  # Cache for 24 hours
        original_content_length = get_content_length(content_to_translate)
        await translation_cache_repo.create(
            content_hash=content_hash,
            target_language=translate_request.target_language,
            translated_content=translated_content,
            expires_at=expiration_time,
            original_content_length=original_content_length
        )

        elapsed_time = time.time() - start_time
        logger.info(f"Chapter translation completed in {elapsed_time:.2f} seconds")

        return TranslateResponse(translated_content=translated_content)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error translating chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error translating chapter: {str(e)}")

# Alternative simple route for testing
@router.post("/translate-chapter")
async def translate_chapter_simple(translate_request: TranslateChapterRequest, db: AsyncSession = Depends(get_db)):
    """
    Simple translation endpoint for testing with caching and timeout.
    """
    start_time = time.time()

    try:
        logger.info(f"Translating chapter {translate_request.chapter_id} to {translate_request.target_language}")

        # Validate target language
        if translate_request.target_language.lower() not in ['urdu', 'ur']:
            raise HTTPException(status_code=400, detail="Only Urdu translation is supported")

        # For this implementation, we'll use the chapter_id as part of the content hash
        # In a real implementation, you would fetch the actual chapter content by chapter_id
        content_to_translate = f"Chapter ID: {translate_request.chapter_id}"
        content_hash = generate_content_hash(content_to_translate, translate_request.target_language)

        # Check if translation is already cached
        translation_cache_repo = TranslationCacheRepository(db)
        cached_translation = await translation_cache_repo.get_by_hash_and_language(content_hash, translate_request.target_language)

        if cached_translation and not is_cache_expired(cached_translation.expires_at):
            logger.info("Returning cached translation for chapter")
            return TranslateResponse(translated_content=cached_translation.translated_content)

        # Create a prompt for Gemini to translate the content
        prompt = f"""
        Translate the following textbook chapter content to Urdu (اردو) while preserving:
        1. Technical accuracy
        2. Educational value
        3. Proper terminology
        4. Context and meaning

        CHAPTER ID/NAME: {translate_request.chapter_id}

        Since we don't have the actual chapter content in this context, please provide a general
        translation framework for a chapter with this identifier. The translation should be
        educational, technically accurate, and preserve the meaning of robotics/humanoid concepts.

        Please return only the translated content in Urdu, no additional commentary.
        Use appropriate Urdu text direction and formatting.
        Use proper formatting for headings, paragraphs, lists, etc. to maintain readability.
        """

        # Import gemini_client at the module level to ensure it's available
        from api.utils.gemini_client import generate_translation

        # Add timeout functionality
        try:
            # Create an async task for the translation with timeout
            async def run_translation():
                return generate_translation(prompt)

            # Execute with 30 second timeout
            translated_content = await asyncio.wait_for(
                run_translation(),
                timeout=30.0  # 30 seconds timeout
            )
        except asyncio.TimeoutError:
            logger.error(f"Translation request for chapter {translate_request.chapter_id} timed out after 30 seconds")
            raise HTTPException(
                status_code=408,
                detail="Translation request timed out. Please try again."
            )

        # Save to cache with expiration
        expiration_time = get_cache_expiration(hours=24)  # Cache for 24 hours
        original_content_length = get_content_length(content_to_translate)
        await translation_cache_repo.create(
            content_hash=content_hash,
            target_language=translate_request.target_language,
            translated_content=translated_content,
            expires_at=expiration_time,
            original_content_length=original_content_length
        )

        elapsed_time = time.time() - start_time
        logger.info(f"Simple chapter translation completed in {elapsed_time:.2f} seconds")

        return TranslateResponse(translated_content=translated_content)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error translating chapter {translate_request.chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error translating chapter: {str(e)}")