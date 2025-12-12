# Authentication Architecture

## Overview

The humanoid robotics textbook project implements a comprehensive authentication system using Better Auth with OAuth capabilities and custom user background information collection. The system is designed with a microservice architecture to separate concerns while maintaining integration.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Auth Service   │    │   Backend       │
│  (Docusaurus)   │◄──►│  (Better Auth)   │◄──►│  (FastAPI)      │
│                 │    │                  │    │                 │
│ - React UI      │    │ - OAuth Login    │    │ - RAG Service   │
│ - Better Auth   │    │ - User Mgmt      │    │ - Qdrant        │
│   Client        │    │ - Background     │    │ - Neon DB       │
│ - Background    │    │   Info Storage   │    │ - Content API   │
│   Forms         │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Components

### 1. Auth Service (Node.js + Better Auth)

**Location**: `/auth-service/`
**Port**: 3002

**Features**:
- OAuth authentication (Google, GitHub, etc.)
- Email/password authentication
- Custom user fields for background information
- Session management
- JWT token generation

**Custom User Fields**:
- `softwareExperience`: User's software experience level
- `hardwareExperience`: User's hardware experience level
- `roboticsExperience`: User's robotics experience level
- `programmingLanguages`: Array of programming languages (JSON string)
- `hardwarePlatforms`: Array of hardware platforms (JSON string)
- `yearsOfExperience`: Number of years of experience
- `primaryInterest`: Primary interest in robotics
- `educationLevel`: Education level

### 2. Frontend Integration (Docusaurus)

**Location**: `/website/src/`
**Port**: 3000

**Components**:
- `/auth/signup`: Multi-step signup with background questions
- `/auth/signin`: OAuth and password-based signin
- Better Auth React client integration
- Background information collection UI

### 3. Backend Service (Python FastAPI)

**Location**: `/backend/`
**Port**: 3001

**Integration**:
- RAG chatbot functionality
- Content personalization based on user background
- Data synchronization with auth service

## API Endpoints

### Auth Service Endpoints

**Better Auth Standard Endpoints**:
- `POST /api/auth/sign-in` - Sign in
- `POST /api/auth/sign-up` - Sign up
- `POST /api/auth/sign-out` - Sign out
- `GET /api/auth/session` - Get session

**Custom Background Endpoints**:
- `POST /api/user-background` - Save user background info
- `GET /api/user-background/:userId` - Get user background info
- `POST /api/signup-background` - Save background during signup

### Backend Endpoints

- `GET /api/rag-chat-stream` - RAG chatbot streaming
- `GET /api/selected-chat-stream` - Selected text Q&A
- Other RAG-related endpoints

## Flow

### Sign Up Flow
1. User visits `/auth/signup`
2. User provides email/password or uses OAuth
3. Better Auth creates the account
4. Custom background form collects user information
5. Background information is saved to auth service
6. User is redirected to homepage

### Sign In Flow
1. User visits `/auth/signin`
2. User provides credentials or uses OAuth
3. Better Auth authenticates and creates session
4. User is redirected to homepage

### Personalized Content Flow
1. Authenticated user requests content
2. Frontend retrieves user background from auth service
3. Frontend sends background info to backend
4. Backend personalizes content based on user background
5. RAG responses are tailored to user's experience level

## Environment Variables

### Auth Service (.env)
```bash
AUTH_SECRET=your-super-secret-jwt-key-change-me
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
DATABASE_URL=file:./auth.db
PORT=3002
```

### Frontend (.env)
```bash
AUTH_API_URL=http://localhost:3002/api
BACKEND_API_URL=http://localhost:3001/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3002
```

## Setup Instructions

1. **Install Auth Service Dependencies**:
   ```bash
   cd auth-service
   npm install
   ```

2. **Install Backend Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Website Dependencies**:
   ```bash
   cd website
   npm install
   ```

4. **Configure Environment Variables**:
   - Set up `.env` files in each service directory

5. **Start Services**:
   ```bash
   # Start auth service
   cd auth-service
   npm run dev

   # Start backend
   cd backend
   uvicorn main:app --reload --port 3001

   # Start website
   cd website
   npm run start
   ```

## OAuth Provider Setup

### Google OAuth
1. Go to Google Cloud Console
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:3002/api/auth/callback/google`
6. Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`

## Security Considerations

- JWT tokens are signed with a secret key
- OAuth providers are securely configured
- User data is stored with appropriate privacy controls
- CORS is configured to allow only necessary origins
- Passwords are hashed using industry-standard methods

## Future Enhancements

- Additional OAuth providers (GitHub, Microsoft, etc.)
- Two-factor authentication
- Account verification via email
- Password reset functionality
- Admin dashboard for user management
- Integration with analytics for personalized recommendations