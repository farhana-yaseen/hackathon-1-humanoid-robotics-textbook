# Humanoid Robotics Textbook with RAG Chatbot

This project implements a comprehensive humanoid robotics textbook with an integrated Retrieval-Augmented Generation (RAG) chatbot system. The application allows users to read the textbook and ask questions about selected text, with the AI assistant providing answers based only on the selected content.

## Architecture

The system consists of:

- **Frontend**: Docusaurus-based textbook website with integrated chatbot
- **Backend**: FastAPI server with RAG functionality
- **Vector Database**: Qdrant Cloud for storing textbook embeddings
- **LLM**: Google Gemini for text generation and embeddings
- **Database**: Neon Serverless Postgres for query logging

## Technologies Used

- **Frontend**: React, Docusaurus, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI/ML**: Google Gemini, Qdrant vector database
- **Database**: Neon Serverless Postgres
- **Authentication**: Better Auth

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- Access to Google Gemini API
- Qdrant Cloud account
- Neon Postgres account

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   NEON_DATABASE_URL=your_neon_database_url
   ```

5. Start the backend server:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. Navigate to the website directory:
   ```bash
   cd website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

### Data Ingestion

To populate the vector database with textbook content:

1. Ensure the backend server is running
2. Run the ingestion script:
   ```bash
   cd backend
   python scripts/ingest_textbook.py
   ```

## Features

- Interactive textbook with modular documentation
- RAG chatbot that answers questions based on selected text
- Streaming responses for real-time interaction
- User authentication with automatic redirect to last accessed module
- Content translation to Urdu with toggle functionality
- User personalization and progress tracking
- Vector search for relevant textbook sections
- Caching for improved performance
- Error handling and timeout management

## API Endpoints

### Core Endpoints
- `GET /health` - Backend health check
- `GET /api/health` - API health check

### RAG Endpoints
- `GET /api/rag/health` - RAG module health check
- `GET /api/selected-chat-stream` - Streaming chatbot for selected text
- `POST /api/rag/chat-sync` - Synchronous RAG chat
- `GET /api/rag/chat-stream` - Streaming RAG chat

### Authentication Redirect Endpoints
- `POST /api/auth/signin` - Authenticate user and return redirect URL
- `GET /api/auth/redirect-url` - Get redirect URL for authenticated user
- `POST /api/auth/modules/{module_id}/access` - Record module access for redirect tracking

### Translation Endpoints
- `POST /api/translate-content` - Translate content to Urdu with caching
- `POST /api/v1/translation/chapters/{chapter_id}/translate` - Translate specific chapter with caching
- `POST /api/translate-chapter` - Simple chapter translation endpoint

## Environment Variables

Required environment variables for the backend:

- `GEMINI_API_KEY` - Google Gemini API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `NEON_DATABASE_URL` - Neon Postgres connection string
- `JWT_SECRET` - Secret for JWT token generation

## Running the Application

Use the start-all.bat script to start both frontend and backend:

```bash
start-all.bat
```

This will start:
- Backend server on http://localhost:8000
- Frontend on http://localhost:3000

## Usage

1. Browse the textbook content on the website
2. Select any text in the textbook
3. Open the chatbot (bottom-right corner)
4. Ask questions about the selected text
5. The AI assistant will provide answers based only on the selected content

## Project Structure

```
humanoid-robotics-textbook/
├── backend/                 # FastAPI backend
│   ├── api/                 # API routes
│   │   ├── utils/           # Utility functions
│   │   │   ├── gemini_client.py
│   │   │   ├── qdrant_client.py
│   │   │   ├── chatkit_client.py
│   │   │   └── db.py
│   │   ├── rag.py
│   │   ├── rag_module.py
│   │   └── ...
│   ├── scripts/             # Utility scripts
│   │   └── ingest_textbook.py
│   ├── main.py              # Main application
│   └── requirements.txt
├── website/                 # Docusaurus frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── Chatbot.tsx
│   │   ├── pages/
│   │   └── theme/
│   ├── docs/                # Textbook content
│   └── docusaurus.config.ts
└── start-all.bat            # Start script for both servers
```