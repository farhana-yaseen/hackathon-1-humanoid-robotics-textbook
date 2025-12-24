"""
Chapter router for the Humanoid Robotics Textbook application.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from pydantic import BaseModel
from ..services.chapter_service import ChapterService
from ..services.personalization_service import PersonalizationService
from ..services.user_service import UserService
from ..models.chapter import Chapter
from ..models.user import User


# Create the chapter router
chapter_router = APIRouter()


# Additional request/response models for content personalization
class PersonalizeContentRequest(BaseModel):
    chapter_title: str
    chapter_content: str
    user_background: dict


class PersonalizeContentResponse(BaseModel):
    personalized_content: str


# Response models
class ChapterResponse(BaseModel):
    chapter_id: str
    title: str
    slug: str
    module: str
    word_count: int
    created_at: str
    updated_at: str
    metadata: dict = {}


class ChapterListResponse(BaseModel):
    success: bool
    chapters: List[ChapterResponse]


class ChapterContentResponse(BaseModel):
    success: bool
    chapter: ChapterResponse
    content: str


class PersonalizationRequest(BaseModel):
    chapter_id: str


class PersonalizationResponse(BaseModel):
    success: bool
    content: str
    rules_applied: List[str]


@chapter_router.get("/", response_model=ChapterListResponse)
async def list_chapters():
    """
    List all chapters in the textbook.
    """
    service = ChapterService()
    chapters = await service.get_all_chapters()

    chapter_responses = []
    for chapter in chapters:
        chapter_responses.append(ChapterResponse(
            chapter_id=chapter.chapter_id,
            title=chapter.title,
            slug=chapter.slug,
            module=chapter.module,
            word_count=chapter.word_count,
            created_at=chapter.created_at.isoformat(),
            updated_at=chapter.updated_at.isoformat(),
            metadata=chapter.metadata or {}
        ))

    return ChapterListResponse(
        success=True,
        chapters=chapter_responses
    )


@chapter_router.get("/{chapter_id}", response_model=ChapterContentResponse)
async def get_chapter(
    chapter_id: str,
    personalized: bool = Query(default=False, description="Whether to return personalized content")
):
    """
    Get a specific chapter's content.
    """
    service = ChapterService()
    chapter = await service.get_chapter(chapter_id)

    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    content = await service.get_chapter_content(chapter_id, personalized)

    if not content:
        raise HTTPException(status_code=404, detail="Chapter content not found")

    return ChapterContentResponse(
        success=True,
        chapter=ChapterResponse(
            chapter_id=chapter.chapter_id,
            title=chapter.title,
            slug=chapter.slug,
            module=chapter.module,
            word_count=chapter.word_count,
            created_at=chapter.created_at.isoformat(),
            updated_at=chapter.updated_at.isoformat(),
            metadata=chapter.metadata or {}
        ),
        content=content
    )


@chapter_router.post("/{chapter_id}/personalize", response_model=PersonalizationResponse)
async def personalize_chapter(chapter_id: str):
    """
    Generate personalized content for a chapter based on user profile.
    This is a simplified version - in a real implementation, we would get the
    user from the authentication context.
    """
    # In a real implementation, we would get the user from the authentication context
    # For now, we'll create a mock user
    from datetime import datetime
    import uuid

    mock_user = User(
        user_id=str(uuid.uuid4()),
        email="user@example.com",
        name="Test User",
        software_background="Software Engineer with 5 years experience",
        hardware_background="Hardware enthusiast with basic knowledge",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        preferences={"theme": "light"}
    )

    # Get the chapter
    chapter_service = ChapterService()
    chapter = await chapter_service.get_chapter(chapter_id)

    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Get or create personalization profile
    personalization_service = PersonalizationService()
    profile = await personalization_service.get_personalization_profile(mock_user.user_id, chapter_id)

    if not profile:
        profile = await personalization_service.create_personalization_profile(
            mock_user.user_id, chapter_id, mock_user
        )

    # Generate personalized content
    personalized_content = await personalization_service.generate_personalized_content(
        chapter.content, mock_user
    )

    return PersonalizationResponse(
        success=True,
        content=personalized_content,
        rules_applied=list(profile.personalization_rules.keys()) if profile.personalization_rules else []
    )


@chapter_router.post("/personalize-content", response_model=PersonalizeContentResponse)
async def personalize_content(request: PersonalizeContentRequest):
    """
    Personalize content based on user background.
    This endpoint matches the frontend API call format.
    """
    # In a real implementation, this would integrate with authentication
    # For now, we'll create a mock user from the provided background
    from datetime import datetime
    import uuid

    # Create a mock user from the provided background
    mock_user = User(
        user_id=str(uuid.uuid4()),
        email="user@example.com",
        name="Test User",
        software_background=request.user_background.get("software_experience", ""),
        hardware_background=request.user_background.get("hardware_experience", ""),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        preferences={"theme": "light"}
    )

    # Generate personalized content
    personalization_service = PersonalizationService()
    personalized_content = await personalization_service.generate_personalized_content(
        request.chapter_content, mock_user
    )

    return PersonalizeContentResponse(
        personalized_content=personalized_content
    )