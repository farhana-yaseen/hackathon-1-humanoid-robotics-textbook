# Humanoid Robotics Textbook - Modular Backend System

This backend implements a modular system for the humanoid robotics textbook with RAG (Retrieval-Augmented Generation) and authentication capabilities. The system uses vector embeddings to retrieve relevant context and then generates answers based on that context.

## Architecture Overview

The backend follows a modular architecture with separate components for different functionalities:

1. **RAG Module** - Handles question answering using vector search and AI generation
2. **Authentication Module** - Manages user registration, login, and background information
3. **Legacy Modules** - Existing functionality for backward compatibility

### Technologies Used

- **FastAPI**: Web framework for the API endpoints
- **Google Gemini API**: For embeddings and language model responses
- **Qdrant Cloud**: Vector database for similarity search
- **Neon Serverless Postgres**: For query logging and metadata storage
- **PyJWT**: For secure token-based authentication
- **PBKDF2**: For secure password hashing

## Modular Components

### RAG (Retrieval-Augmented Generation) Module

The RAG module provides AI-powered question answering capabilities:

#### Key Features:
- Vector similarity search using Qdrant
- Google Gemini integration for embeddings and text generation
- Streaming responses for real-time chat experience
- Context-aware responses based on humanoid robotics textbook content
- Modular service architecture for easy testing and maintenance

#### Endpoints:
- `GET /api/rag/chat-stream` - Streaming chat response
- `POST /api/rag/chat-sync` - Synchronous chat response
- `GET /api/rag/health` - Health check

#### Implementation:
- `api/rag_module.py` - Modular RAG service implementation
- Uses `api/utils/gemini_client.py` for embeddings and generation
- Uses `api/utils/qdrant_client.py` for vector database operations

### Authentication Module

The authentication module provides secure user management:

#### Key Features:
- User registration and login with password hashing (PBKDF2)
- JWT-based token authentication
- User background information management for personalization
- Secure session management
- Modular service architecture for easy testing and maintenance

#### Endpoints:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/user-background` - Update user background
- `GET /api/auth/user-background/{user_id}` - Get user background
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/health` - Health check

#### Implementation:
- `api/auth_module.py` - Modular authentication service implementation
- Uses JWT tokens for session management
- PBKDF2 with salt for password security

### Legacy Components

The original implementation is maintained for backward compatibility:

#### API Endpoints
1. **`/api/rag-chat-stream`** - Main RAG endpoint that:
   - Embeds user questions using Google's embedding model
   - Searches Qdrant for relevant context
   - Generates answers using Gemini based on retrieved context
   - Streams responses back to the client

2. **`/api/selected-chat-stream`** - Endpoint for answering questions based only on user-selected text

3. **`/api/auth`** - Legacy authentication endpoints

### Utility Modules
- `gemini_client.py`: Handles embeddings and text generation using Google Gemini
- `qdrant_client.py`: Manages vector storage and similarity search
- `chatkit_client.py`: Provides chat session management and streaming responses
- `db.py`: Handles database operations with Neon Postgres

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `QDRANT_URL`: Qdrant Cloud instance URL
   - `QDRANT_API_KEY`: Qdrant Cloud API key
   - `NEON_DATABASE_URL`: Neon Postgres connection string

3. Run the server:
   ```bash
   # Using the batch file (Windows)
   start_server.bat

   # Or directly with uvicorn
   uvicorn main:app --reload --port 8000
   ```

4. Access the API:
   - API Root: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

## Development Guidelines

### RAG Service Usage:
```python
from api.rag_module import RAGService

rag_service = RAGService()
response = rag_service.process_query(user_id, question, context_limit=5)
```

### Auth Service Usage:
```python
from api.auth_module import AuthService

auth_service = AuthService()
user = auth_service.authenticate_user(email, password)
```

## Security Considerations

- Passwords are hashed using PBKDF2 with salt
- JWT tokens are used for session management
- API keys are loaded from environment variables
- Input validation is performed using Pydantic models
- CORS is configured for frontend communication

## Testing the Modules

The modular design allows for easy testing:

1. Each service class can be instantiated independently
2. Dependencies are clearly defined
3. Error handling is implemented consistently
4. Logging is available for debugging

## Environment Variables

The following environment variables must be set:

- `GEMINI_API_KEY` - Google Gemini API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `NEON_DATABASE_URL` - Neon Postgres database URL

## API Documentation

The API includes automatic documentation available at `/docs` endpoint when running the server.

## Note on Implementation Choice

While the original requirements specified using OpenAI Agents/ChatKit SDKs, this implementation uses Google's Gemini API due to the user having a Gemini API key available. All other architectural requirements (FastAPI, Qdrant, Neon Postgres, RAG functionality) have been fully implemented.

The system maintains the same interface and functionality regardless of the underlying LLM provider, ensuring the RAG pipeline works effectively with the provided textbook content.

The modular architecture allows for easy extension and maintenance of the system while keeping the same core functionality.