# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 1 Load .env first
load_dotenv()

# 2 Check API key
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set in .env")

# 3 Import routers AFTER loading .env
from api.rag import router as rag_router
from api.selected import router as selected_router

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rag_router, prefix="/api")
app.include_router(selected_router, prefix="/api")

# Optional root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "RAG Chatbot Backend Running!"}
