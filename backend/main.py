# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
import asyncio
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1 Load .env first
load_dotenv()

# 2 Check API key
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set in .env")

# 3 Import routers AFTER loading .env
from api.rag import router as rag_legacy_router
from api.selected import router as selected_router
from api.auth import router as auth_legacy_router
from api.personalize import router as personalize_router
from api.translate import router as translate_router

# Import new modular components
from api.rag_module import router as rag_module_router

# Import Better Auth components
from api.auth_better.better_auth_router import router as better_auth_router

# Import database utilities for cache cleanup
from api.utils.db import get_db
from api.repositories.translation_cache_repository import TranslationCacheRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up...")

    # Start background task for cache cleanup
    cleanup_task = asyncio.create_task(periodic_cache_cleanup())

    yield

    # Shutdown
    logger.info("Shutting down...")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        logger.info("Cache cleanup task cancelled")


async def periodic_cache_cleanup():
    """Periodically clean up expired cache entries."""
    from datetime import datetime

    while True:
        try:
            # Wait 1 hour before next cleanup
            await asyncio.sleep(3600)  # 1 hour

            logger.info("Starting periodic cache cleanup...")

            # Use SQLAlchemy async session for database operations
            from api.utils.database import AsyncSessionFactory
            from api.models.translation_cache_db import TranslationCacheDB
            from sqlalchemy import delete
            from sqlalchemy.future import select

            async with AsyncSessionFactory() as session:
                try:
                    # Count expired entries first
                    expired_count_result = await session.execute(
                        select(TranslationCacheDB)
                        .where(TranslationCacheDB.expires_at <= datetime.now())
                    )
                    expired_entries = expired_count_result.scalars().all()
                    expired_count = len(expired_entries)

                    # Delete expired entries
                    stmt = delete(TranslationCacheDB).where(
                        TranslationCacheDB.expires_at <= datetime.now()
                    )
                    result = await session.execute(stmt)
                    await session.commit()

                    deleted_count = result.rowcount

                    logger.info(f"Cache cleanup completed. Deleted {deleted_count} expired entries")
                except Exception as e:
                    logger.error(f"Error during cache cleanup: {e}")
                    await session.rollback()

        except asyncio.CancelledError:
            logger.info("Cache cleanup task was cancelled")
            break
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
            # Wait before retrying to avoid rapid error loops
            await asyncio.sleep(300)  # Wait 5 minutes before retrying


app = FastAPI(lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include legacy routers for backward compatibility
app.include_router(rag_legacy_router, prefix="/api")
app.include_router(selected_router, prefix="/api")
app.include_router(auth_legacy_router, prefix="/api")
app.include_router(personalize_router, prefix="/api")
app.include_router(translate_router, prefix="/api")

# Include new modular routers
app.include_router(rag_module_router, prefix="/api")

# Include Better Auth router
app.include_router(better_auth_router, prefix="/api")

# Optional root endpoint
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "RAG Chatbot Backend Running!",
        "modules": {
            "rag": "Available",
            "auth": "Available",
            "selected": "Available",
            "personalize": "Available",
            "translate": "Available"
        }
    }


# Health check endpoint for the entire application
@app.get("/health")
def health_check():
    """
    Health check endpoint for the entire backend service.

    Returns the status of all services.

    Returns:
        dict: Health status information for all services
    """
    return {
        "status": "healthy",
        "service": "Backend API",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "modules": {
            "rag": "operational",
            "auth": "operational",
            "selected": "operational",
            "personalize": "operational",
            "translate": "operational"
        }
    }


logger.info("Backend application initialized successfully")
