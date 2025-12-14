from sqlalchemy.orm import Session
from ..models.translation import Translation
from ..models.chapter import Chapter
from ..models.rag_session import RAGSession
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional
import google.generativeai as genai
import os
from ..logging_config import get_logger, log_translation_request, log_error


class TranslationService:
    """Service class for managing Urdu translations of textbook content."""

    def __init__(self):
        # Initialize Gemini client for translation
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

        # Initialize logger
        self.logger = get_logger('translation')

    def translate_chapter_content(self, chapter_content: str, target_language: str = "Urdu") -> str:
        """Translate chapter content to the target language."""
        try:
            prompt = f"""
            Translate the following text to {target_language}. Preserve technical terms and concepts accurately.
            Maintain the structure and meaning of the original text.
            Return only the translated content without any additional commentary.

            Original Text:
            {chapter_content[:4000]}  # Limit to prevent exceeding token limits

            Translated Text:
            """

            response = self.model.generate_content(prompt)
            return response.text if response.text else chapter_content
        except Exception as e:
            print(f"Error translating content: {e}")
            return chapter_content  # Return original if translation fails

    def translate_text_chunk(self, text_chunk: str, target_language: str = "Urdu") -> str:
        """Translate a specific text chunk to the target language."""
        try:
            prompt = f"""
            Translate the following text to {target_language}. Preserve technical terms and concepts accurately.
            Maintain the structure and meaning of the original text.
            Return only the translated content without any additional commentary.

            Original Text:
            {text_chunk}

            Translated Text:
            """

            response = self.model.generate_content(prompt)
            translated_result = response.text if response.text else text_chunk

            # Preserve structure in the translated result
            return self.preserve_code_blocks_and_structure(text_chunk, translated_result)
        except Exception as e:
            print(f"Error translating chunk: {e}")
            return text_chunk  # Return original if translation fails

    def translate_chatbot_response(self, response: str, target_language: str = "Urdu") -> str:
        """Translate a chatbot response to the target language."""
        try:
            prompt = f"""
            Translate the following AI response to {target_language}. Preserve the helpful tone and technical accuracy.
            Maintain the structure and meaning of the original response.
            Return only the translated response without any additional commentary.

            Original Response:
            {response}

            Translated Response:
            """

            translation_response = self.model.generate_content(prompt)
            translated_result = translation_response.text if translation_response.text else response

            # Preserve structure in the translated result
            return self.preserve_code_blocks_and_structure(response, translated_result)
        except Exception as e:
            print(f"Error translating chatbot response: {e}")
            return response  # Return original if translation fails

    def create_translation_record(self, db: Session, chapter_id: UUID, urdu_content: str, user_session_id: Optional[str] = None) -> Translation:
        """Create a translation record in the database."""
        # Set expiration time for temporary translations (24 hours)
        expires_at = datetime.utcnow() + timedelta(hours=24)

        translation = Translation(
            chapter_id=chapter_id,
            user_session_id=user_session_id,
            urdu_content=urdu_content,
            created_at=datetime.utcnow(),
            expires_at=expires_at
        )

        db.add(translation)
        db.commit()
        db.refresh(translation)

        return translation

    def get_cached_translation(self, db: Session, chapter_id: UUID, user_session_id: Optional[str] = None) -> Optional[Translation]:
        """Get a cached translation if it exists and hasn't expired."""
        query = db.query(Translation).filter(
            Translation.chapter_id == chapter_id
        )

        if user_session_id:
            query = query.filter(Translation.user_session_id == user_session_id)
        else:
            query = query.filter(Translation.user_session_id.is_(None))

        translation = query.filter(
            Translation.expires_at > datetime.utcnow()
        ).first()

        return translation

    def validate_translation_quality(self, original_text: str, translated_text: str) -> float:
        """Validate translation quality by comparing lengths and content."""
        # Basic quality validation - ensure translation is not too short compared to original
        if len(translated_text) < len(original_text) * 0.5:
            return 0.0  # Poor quality if translated text is less than 50% of original

        # Placeholder for more sophisticated quality checks
        return 0.9  # Return high quality score for now

    def preserve_code_blocks_and_structure(self, original_content: str, translated_content: str) -> str:
        """Preserve code blocks, headings, and structure during translation."""
        import re

        # Extract code blocks from original content
        code_blocks = re.findall(r'(```[\s\S]*?```|`[^`]*`)', original_content)

        # Extract headings from original content
        headings = re.findall(r'(^#{1,6}\s+.*?$)', original_content, re.MULTILINE)

        # Replace code blocks in translated content with placeholders
        temp_content = re.sub(r'(```[\s\S]*?```|`[^`]*`)', '<CODE_BLOCK_PLACEHOLDER>', translated_content)

        # Replace headings in translated content with placeholders
        temp_content = re.sub(r'(^#{1,6}\s+.*?$)', '<HEADING_PLACEHOLDER>', temp_content, flags=re.MULTILINE)

        # Replace placeholders with original code blocks and headings
        result = temp_content
        for code_block in code_blocks:
            result = result.replace('<CODE_BLOCK_PLACEHOLDER>', code_block, 1)

        for heading in headings:
            result = result.replace('<HEADING_PLACEHOLDER>', heading, 1)

        return result

    def translate_preserving_structure(self, original_content: str, target_language: str = "Urdu") -> str:
        """Translate content while preserving code blocks and structure."""
        import re

        # Extract code blocks and store them separately
        code_blocks = re.findall(r'(```[\s\S]*?```|`[^`]*`)', original_content)
        code_placeholders = []

        # Replace code blocks with placeholders
        processed_content = original_content
        for i, code_block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            code_placeholders.append((placeholder, code_block))
            processed_content = processed_content.replace(code_block, placeholder, 1)

        # Translate the content without code blocks
        translated_content = self.translate_chapter_content(processed_content, target_language)

        # Restore the original code blocks
        result = translated_content
        for placeholder, original_code in code_placeholders:
            result = result.replace(placeholder, original_code, 1)

        return result

    def translate_content_with_cache(self, db: Session, chapter_id: UUID, content: str,
                                   target_language: str = "Urdu", user_session_id: Optional[str] = None) -> str:
        """Translate content with caching mechanism."""
        self.logger.info(f"Starting translation for chapter {chapter_id}, target language: {target_language}, session: {user_session_id}")

        # Check for cached translation first
        cached_translation = self.get_cached_translation(db, chapter_id, user_session_id)

        if cached_translation:
            self.logger.info(f"Using cached translation for chapter {chapter_id}")
            log_translation_request(user_session_id or "anonymous", str(chapter_id), "original", target_language, True)
            return cached_translation.urdu_content

        # Translate the content while preserving structure
        try:
            translated_content = self.translate_preserving_structure(content, target_language)

            # Store in database for caching
            self.create_translation_record(db, chapter_id, translated_content, user_session_id)

            self.logger.info(f"Successfully translated and cached content for chapter {chapter_id}")
            log_translation_request(user_session_id or "anonymous", str(chapter_id), "original", target_language, True)

            return translated_content
        except Exception as e:
            self.logger.error(f"Translation failed for chapter {chapter_id}: {str(e)}", exc_info=True)
            log_error(e, f"TranslationService.translate_content_with_cache for chapter {chapter_id}")
            log_translation_request(user_session_id or "anonymous", str(chapter_id), "original", target_language, False)
            raise