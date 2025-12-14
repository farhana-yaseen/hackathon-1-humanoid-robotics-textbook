from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rag_router import router as rag_router
from .auth_router import router as auth_router
from .translation_router import router as translation_router
from .. import __version__
from ..security import add_security_headers

app = FastAPI(
    title="Humanoid Robotics Textbook Platform API",
    description="Interactive textbook platform with RAG chatbot for Physical AI & Humanoid Robotics education",
    version=__version__,
)

# Set up security
from ..security import setup_security
setup_security(app)

# Include routers
app.include_router(rag_router, prefix="/api/v1", tags=["rag"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(translation_router, prefix="/api/v1", tags=["translation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Humanoid Robotics Textbook Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}