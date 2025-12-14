# Quickstart Guide: Personalization and Translation Features

## Overview
This guide provides instructions for developers to understand and extend the personalization and translation features in the Humanoid Robotics Textbook.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.9+ for backend services
- Better Auth configured for authentication
- Gemini API key for AI processing
- Qdrant vector database for personalization
- Neon Postgres for user profiles

## Development Setup

### 1. Frontend Setup
```bash
cd website
npm install
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Variables
Create `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_url
```

## Feature Architecture

### 1. Personalization Feature
- **Location**: `/src/components/PersonalizeContent.tsx`
- **Integration**: Hooked into Docusaurus via `/src/theme/DocItem/Content/index.tsx`
- **Functionality**: Adjusts content based on user's software/hardware background

### 2. Translation Feature
- **Location**: `/src/components/TranslateContent.tsx`
- **Integration**: Hooked into Docusaurus via `/src/theme/DocItem/Content/index.tsx`
- **Functionality**: Translates content to Urdu while preserving technical meaning

## Key Integration Points

### 1. Docusaurus Theme Integration
The features are integrated at the theme level in:
```
website/src/theme/DocItem/Content/index.tsx
```

This ensures the personalization and translation controls appear at the beginning of every chapter without modifying individual chapter files.

### 2. Authentication Integration
Both features use the Better Auth session:
```typescript
import { useSession } from '@site/src/auth/betterAuthClient';
```

Features are only visible to authenticated users.

### 3. Backend API Integration
- Personalization: `/api/personalize-content`
- Translation: `/api/translate-content`
- User Profile: `/api/user-background/{user_id}`

## Running the Application

### 1. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd website
npm run start
```

## Testing the Features

### 1. Personalization Test Flow
1. Sign up with specific software/hardware background
2. Navigate to any chapter
3. Click "Personalize Content" button
4. Observe content adaptation based on your profile

### 2. Translation Test Flow
1. Sign in to the application
2. Navigate to any chapter
3. Click "Translate to Urdu" button
4. Observe content translated to Urdu with RTL layout

## Extending the Features

### 1. Adding New Personalization Criteria
1. Update the UserBackground interface in `/src/services/userBackground.ts`
2. Modify the personalization API in `backend/api/personalize.py`
3. Update the prompt in the personalization service to include new criteria

### 2. Adding New Translation Languages
1. Update the translation API in `backend/api/translate.py`
2. Modify the frontend to support additional language codes
3. Update the UI to include new language options

## Troubleshooting

### Common Issues

1. **Features not appearing for authenticated users**
   - Verify authentication is working properly
   - Check that `useSession` hook returns authenticated status
   - Ensure backend API endpoints are accessible

2. **API calls failing**
   - Verify backend server is running on correct port
   - Check that environment variables are properly set
   - Confirm API endpoints are correctly configured

3. **Translation quality issues**
   - Review Gemini API configuration
   - Verify prompt engineering in translation service
   - Check for proper Urdu text rendering and RTL support

## Performance Considerations

- API calls include loading states to maintain UI responsiveness
- Consider implementing caching for personalized/translated content
- Monitor API response times for personalization and translation services
- Implement proper error handling to prevent UI crashes

## Security Notes

- All features are restricted to authenticated users only
- User background data is stored securely in Neon Postgres
- API calls are protected by authentication tokens
- Input validation is performed on all user-provided data