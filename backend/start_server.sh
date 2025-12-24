#!/bin/bash
# Script to start the RAG chatbot backend

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate  # Windows compatibility
fi

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --reload --port 8000