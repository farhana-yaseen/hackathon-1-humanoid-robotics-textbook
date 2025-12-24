# Humanoid Robotics Textbook - Full Stack Application

This is a comprehensive educational platform for humanoid robotics, featuring both a frontend website built with Docusaurus and a backend API built with FastAPI. The application includes RAG (Retrieval-Augmented Generation) capabilities for interactive learning and authentication for personalized experiences.

## Architecture Overview

The application consists of two main components:

### Backend (FastAPI Server)
- **Location**: `../backend/`
- **Framework**: FastAPI
- **Features**:
  - RAG (Retrieval-Augmented Generation) for AI-powered Q&A
  - User authentication with JWT tokens
  - Vector database integration with Qdrant
  - Database management with Neon Postgres
  - Modular service architecture

### Frontend (Docusaurus Website)
- **Location**: `./` (current directory)
- **Framework**: Docusaurus
- **Features**:
  - Interactive textbook content
  - Integration with backend API
  - Responsive design
  - Modern static site generation

## Installation

### Prerequisites
- Node.js (version >= 20.0)
- Python (version >= 3.8)
- Yarn package manager
- Pip package manager

### Complete Installation Process

#### 1. Backend Setup
Navigate to the backend directory and install dependencies:

```bash
cd ../backend
pip install -r requirements.txt
```

Set up your environment variables in `../backend/.env`:

```env
PORT=8000
MONGO_URI=mongodb://localhost:27017/usage_metrics
JWT_SECRET=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DATABASE_URL=your_neon_postgres_connection_string_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
EMBEDDING_MODEL=models/text-embedding-004
LLM_MODEL=gemini-2.5-flash
```

Start the backend server:

```bash
# On Windows
start_server.bat

# On Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

#### 2. Frontend Setup
Return to the website directory and install dependencies:

```bash
cd ../website  # or the current directory if you're already here
yarn install
```

Set up your environment variables in `.env`:

```env
# API Configuration
BACKEND_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

Start the development server:

```bash
yarn start
```

Your application will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Required Services

Before running the application, you'll need to obtain:

1. **Google Gemini API Key**: From Google AI Studio for embeddings and text generation
2. **Qdrant Cloud Account**: Vector database service for similarity search
3. **Neon Postgres Database**: Serverless PostgreSQL for metadata storage
4. **Google OAuth Credentials**: From Google Cloud Console for authentication

## Development

### Backend Development
The backend provides several API modules:
- RAG Module: AI-powered question answering
- Authentication Module: User management and sessions
- Personalization Module: User-specific content
- Translation Module: Content translation capabilities

### Frontend Development
The frontend is built with Docusaurus and includes:
- Interactive textbook content
- Integration with backend APIs
- Responsive design for all devices
- Modern documentation features

## API Endpoints

### Backend Endpoints
- `GET /api/rag/chat-stream` - Streaming RAG chat response
- `POST /api/rag/chat-sync` - Synchronous RAG chat response
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `GET /health` - Health check for the entire application

### Frontend Scripts
- `yarn start` - Start development server
- `yarn build` - Build for production
- `yarn serve` - Serve production build
- `yarn deploy` - Deploy to hosting platform

## Security Considerations

- Passwords are hashed using PBKDF2 with salt
- JWT tokens are used for secure session management
- API keys are loaded from environment variables
- Input validation is performed using Pydantic models
- CORS is configured for secure frontend communication

## Architecture

The backend follows a modular architecture with separate components for different functionalities:
1. **RAG Module** - Handles question answering using vector search and AI generation
2. **Authentication Module** - Manages user registration, login, and background information
3. **Legacy Modules** - Existing functionality for backward compatibility

## Technologies Used

### Backend
- FastAPI: Web framework for the API endpoints
- Google Gemini API: For embeddings and language model responses
- Qdrant Cloud: Vector database for similarity search
- Neon Serverless Postgres: For query logging and metadata storage
- PyJWT: For secure token-based authentication
- PBKDF2: For secure password hashing

### Frontend
- Docusaurus: Static site generator
- React: Component-based UI framework
- TypeScript: Type safety

## Contributing

This project follows a modular architecture to facilitate easy development and testing of individual components. Both frontend and backend can be developed independently while maintaining consistent interfaces.

## Support

For issues with the installation process, please check the `INSTALLATION.md` file in this directory for detailed troubleshooting steps.