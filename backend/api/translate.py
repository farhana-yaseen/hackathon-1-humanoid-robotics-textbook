from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TranslateRequest(BaseModel):
    chapter_title: str
    chapter_content: str
    target_language: str

class TranslateResponse(BaseModel):
    translated_content: str

@router.post("/translate-content")
async def translate_content(request: TranslateRequest):
    """
    Translate chapter content to the specified language.
    In a real implementation, this would use a translation service like Google Translate API
    or leverage Gemini's translation capabilities.
    """
    try:
        chapter_content = request.chapter_content
        chapter_title = request.chapter_title
        target_language = request.target_language

        # Validate target language
        if target_language.lower() not in ['ur', 'urdu']:
            raise HTTPException(status_code=400, detail="Only Urdu (ur) translation is supported")

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
        """

        # Import and use the Gemini client for translation
        from api.utils.gemini_client import generate_answer
        translated_content = generate_answer("", prompt)

        return TranslateResponse(translated_content=translated_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error translating content: {str(e)}")