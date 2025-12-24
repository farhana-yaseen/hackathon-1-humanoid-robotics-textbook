from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from api.utils.gemini_client import generate_answer

router = APIRouter()

class PersonalizeRequest(BaseModel):
    chapter_title: str
    chapter_content: str
    user_background: dict

class PersonalizeResponse(BaseModel):
    personalized_content: str

@router.post("/personalize-content")
async def personalize_content(request: PersonalizeRequest):
    """
    Personalize chapter content based on user background.
    In a real implementation, this would use the user's background information
    to adjust the content complexity, examples, and focus areas.
    """
    try:
        # Extract user background information
        user_background = request.user_background
        chapter_content = request.chapter_content
        chapter_title = request.chapter_title

        # Create a prompt for Gemini to personalize the content
        prompt = f"""
        Personalize the following textbook content based on the user's background:

        USER BACKGROUND:
        - Software Experience: {user_background.get('software_experience', 'Not specified')}
        - Hardware Experience: {user_background.get('hardware_experience', 'Not specified')}
        - Robotics Experience: {user_background.get('robotics_experience', 'Not specified')}
        - Programming Languages: {', '.join(user_background.get('programming_languages', [])) or 'Not specified'}
        - Hardware Platforms: {', '.join(user_background.get('hardware_platforms', [])) or 'Not specified'}
        - Years of Experience: {user_background.get('years_of_experience', 'Not specified')}
        - Primary Interest: {user_background.get('primary_interest', 'Not specified')}
        - Education Level: {user_background.get('education_level', 'Not specified')}

        CHAPTER TITLE: {chapter_title}

        ORIGINAL CONTENT:
        {chapter_content}

        Please return a personalized version of the content that:
        1. Adjusts complexity based on experience level
        2. Includes relevant examples based on known programming languages and hardware platforms
        3. Focuses on areas relevant to the user's interests
        4. Maintains the educational value and accuracy of the original content

        Return only the personalized content, no additional commentary.
        """

        # Generate personalized content using Gemini
        personalized_content = generate_answer("", prompt)

        return PersonalizeResponse(personalized_content=personalized_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error personalizing content: {str(e)}")