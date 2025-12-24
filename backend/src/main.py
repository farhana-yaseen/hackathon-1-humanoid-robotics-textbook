"""
Main FastAPI application for the Humanoid Robotics Textbook backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
import time
from .utils.logger import app_logger
from .utils.error_handler import add_error_handlers
from .utils.security import SecurityHeaders, security_middleware_handler
from .api.auth_router import auth_router
from .api.chapter_router import chapter_router
from .api.translation_router import translation_router


# Create the main FastAPI application
app = FastAPI(
    title="Humanoid Robotics Textbook API",
    description="API for the Humanoid Robotics Textbook with Personalization and Interaction",
    version="1.0.0"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add middleware to apply security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    SecurityHeaders.add_security_headers(response)
    return response


# Add error handlers
add_error_handlers(app)


# Add middleware to log API requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    app_logger.log_api_request(
        method=request.method,
        endpoint=str(request.url.path),
        response_time=process_time,
        status_code=response.status_code
    )

    return response


# Include the API routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(chapter_router, prefix="/chapters", tags=["chapters"])
app.include_router(translation_router, prefix="/translate", tags=["translation"])


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Humanoid Robotics Textbook API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for the API.
    """
    return {"status": "healthy", "service": "Humanoid Robotics Textbook API"}