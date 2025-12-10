# Installation Guide for Humanoid Robotics Textbook Application

This guide provides comprehensive instructions for installing and setting up the Humanoid Robotics Textbook application, which consists of both a frontend (Docusaurus website) and a backend (FastAPI server).

## Prerequisites

- Node.js (version >= 20.0) - for the frontend
- Python (version >= 3.8) - for the backend
- Yarn package manager - for the frontend
- Pip package manager - for the backend
- MongoDB (optional, if using local database)
- Access to Google Cloud Console for API keys

## Installation Steps

### 1. Backend Setup

#### Navigate to the backend directory:
```bash
cd ../backend
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
```

#### Set up environment variables:
Create or update the `.env` file in the backend directory with the following variables:
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

#### Run the backend server:
Option 1: Using the provided startup script
```bash
# On Windows
start_server.bat

# On Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

Option 2: Directly with uvicorn
```bash
uvicorn main:app --reload --port 8000
```

The backend server will be accessible at `http://localhost:8000`.

### 2. Frontend Setup

#### Navigate to the website directory:
```bash
cd ../website  # or cd website if you're in the root directory
```

#### Install JavaScript dependencies:
```bash
yarn install
```

#### Set up environment variables:
Create or update the `.env` file in the website directory with the following variables:
```env
# API Configuration
BACKEND_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

#### Run the frontend development server:
```bash
yarn start
```

The frontend will be accessible at `http://localhost:3000`.

### 3. Complete Application Setup

Once both the backend and frontend are running:

1. Backend API will be available at `http://localhost:8000`
2. Frontend will be available at `http://localhost:3000`
3. API documentation will be available at `http://localhost:8000/docs`

## Required Services & API Keys

Before running the application, ensure you have:

1. **Google Gemini API Key**: Obtain from Google AI Studio
2. **Qdrant Cloud Account**: Vector database for RAG functionality
3. **Neon Postgres Database**: Serverless PostgreSQL for metadata
4. **Google OAuth Credentials**: Client ID and secret from Google Cloud Console

## Development Scripts

The backend provides the following utility scripts:

- `start_server.bat` - Windows startup script
- `start_server.sh` - Linux/Mac startup script

## Troubleshooting

1. **Port Issues**: Ensure ports 8000 (backend) and 3000 (frontend) are available
2. **Environment Variables**: Verify all required environment variables are set
3. **Dependency Issues**: Reinstall dependencies if modules are missing
4. **API Connection**: Confirm backend is running before starting frontend

## Building for Production

#### Backend:
The backend runs as a FastAPI application with uvicorn in production mode.

#### Frontend:
```bash
yarn build
```

This creates a `build` directory with the production-ready static files.

## Environment Variables Reference

### Backend (.env):
- `GEMINI_API_KEY`: Google Gemini API key for embeddings and generation
- `QDRANT_URL`: Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `NEON_DATABASE_URL`: Neon Postgres connection string
- `JWT_SECRET`: Secret key for JWT token generation
- `MONGO_URI`: MongoDB connection string (if using MongoDB)

### Frontend (.env):
- `BACKEND_API_URL`: URL to the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Authentication base URL
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret