# Running the Humanoid Robotics Textbook Application

This guide explains how to run all services for the Humanoid Robotics Textbook application with OAuth authentication.

## Service Architecture

The application consists of three main services:

1. **Auth Service** - Runs on port 3002 (handles authentication)
2. **Backend Service** - Runs on port 8000 (handles RAG and AI features)
3. **Website (Frontend)** - Runs on port 3000 (Docusaurus frontend)

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn

## Setup Instructions

### 1. Auth Service Setup (Port 3002)

```bash
cd auth-service
npm install
```

Create a `.env` file in the `auth-service` directory with the following content:

```env
# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3002
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-me
DATABASE_URL=file:./auth.db

# Google OAuth (optional but recommended)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth (optional but recommended)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### 2. Backend Service Setup (Port 8000)

```bash
cd backend
pip install -r requirements.txt
```

### 3. Website Setup (Port 3000)

```bash
cd website
npm install
```

Create a `.env` file in the `website` directory with the following content:

```env
# API Configuration
BACKEND_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3002
```

## Running the Services

**Important**: Services must be started in the correct order due to dependencies.

### Method 1: Run Each Service Separately

1. **Start Auth Service** (required first):
   ```bash
   cd auth-service
   npm run dev
   ```

2. **Start Backend Service** (required second):
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

3. **Start Website** (last):
   ```bash
   cd website
   npm run start
   ```

### Method 2: Using Concurrently (Recommended)

Install concurrently globally:
```bash
npm install -g concurrently
```

Then run all services from the root directory:
```bash
concurrently "cd auth-service && npm run dev" "cd backend && uvicorn main:app --reload --port 8000" "cd website && npm run start"
```

## OAuth Provider Configuration

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:3002/api/auth/callback/google`
6. Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in auth-service `.env`

### GitHub OAuth Setup
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set Homepage URL: `http://localhost:3002`
4. Set Authorization callback URL: `http://localhost:3002/api/auth/callback/github`
5. Set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in auth-service `.env`

## Troubleshooting

### Common Issues:

1. **404 errors on auth endpoints**: Make sure the auth service is running on port 3002
2. **OAuth not working**: Verify your OAuth provider settings and callback URLs
3. **Environment variables not loading**: Ensure `.env` files are properly configured in each service directory

### Testing OAuth:
- Visit `http://localhost:3000/auth/signin` to test sign-in with OAuth
- Visit `http://localhost:3000/auth/signup` to test sign-up with OAuth