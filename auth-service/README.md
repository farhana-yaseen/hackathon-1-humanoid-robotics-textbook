# Better Auth Service for Humanoid Robotics Textbook

This service handles authentication using Better Auth with OAuth support and user background information collection.

## Architecture

This project uses a microservice architecture:
- **auth-service**: Node.js service with Better Auth for authentication
- **backend**: Python FastAPI service for RAG and other business logic
- **website**: Docusaurus frontend that integrates with both services

## Setup

### 1. Environment Variables

Create a `.env` file in the auth-service directory:

```bash
AUTH_SECRET=your-super-secret-jwt-key-change-me
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
DATABASE_URL=file:./auth.db
PORT=3002
```

### 2. Installation

```bash
npm install
```

### 3. Running the Service

```bash
npm run dev  # For development
npm start    # For production
```

## Features

1. **OAuth Support**: Google OAuth and other providers
2. **Custom User Fields**: Stores user background information:
   - Software/hardware/robotics experience
   - Programming languages known
   - Hardware platforms experience
   - Years of experience
   - Primary interests
   - Education level
3. **API Endpoints**:
   - `/api/auth/*` - Better Auth standard endpoints
   - `/api/user-background` - Save user background info
   - `/api/user-background/:userId` - Get user background info
   - `/api/signup-background` - Save background during signup

## Integration with Frontend

The Docusaurus frontend integrates with this service using the Better Auth client and custom API calls for background information.

## Integration with Backend

The Python backend can sync user information as needed with the auth service.