@echo off
REM Script to start the RAG chatbot backend on Windows

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Install dependencies if not already installed
pip install -r requirements.txt

REM Run the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload