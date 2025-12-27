# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

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
from api.auth_module import router as auth_module_router

# Import Better Auth components
from api.auth_better.better_auth_router import router as better_auth_router

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://hackathon-1-humanoid-robotics-textb.vercel.app"
    ],

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
app.include_router(auth_module_router, prefix="/api")

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
