# Quickstart Guide: Authentication Redirect & Urdu Translation

## Development Setup

### Prerequisites
- Node.js 18+ (for Docusaurus frontend)
- Python 3.9+ (for FastAPI backend)
- Git
- Access to Google Gemini API key

### Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd humanoid-robotics-textbook

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env to include:
# - GEMINI_API_KEY=your_api_key
# - DATABASE_URL=your_neon_postgres_url
# - BETTER_AUTH_SECRET=your_secret
# - BETTER_AUTH_URL=http://localhost:8000

# Set up frontend
cd ../website
npm install
```

### Running the Application

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Start frontend
cd website
npm start
```

The application will be available at `http://localhost:3000`

## Feature Implementation Guide

### 1. Authentication Redirect Implementation

The authentication redirect feature modifies the post-sign-in flow to redirect users to the Module Page instead of the Home Page.

#### Key Files to Modify:
- `auth-service/index.ts` - Update the sign-in callback
- `website/src/pages/auth/signin.js` - Update redirect logic
- `backend/api/auth_better/auth_service_client.py` - Handle redirect logic

#### Implementation Steps:
1. Update the auth callback to check for last accessed module
2. Redirect to `/modules/{module_id}` or `/modules/default` instead of `/`
3. Store last accessed module in database when user visits a module

### 2. Urdu Translation Implementation

The Urdu translation feature allows users to translate chapter content to Urdu with a button click.

#### Key Files to Use:
- `website/src/components/TranslateContent.js` - Existing translation component
- `backend/api/translate.py` - Translation API endpoint
- `backend/api/utils/gemini_client.py` - Gemini API integration

#### Implementation Steps:
1. Add "Translate to Urdu" button to module pages
2. Integrate existing `TranslateContent.js` component
3. Implement caching with 24-hour expiration
4. Add session storage for language preferences

## Testing the Feature

### Authentication Redirect Test
1. Navigate to `/auth/signin`
2. Complete sign-in flow
3. Verify redirect to `/modules` instead of `/`
4. Check that last accessed module is tracked

### Translation Functionality Test
1. Navigate to a module page
2. Click "Translate to Urdu" button
3. Verify content is translated while maintaining formatting
4. Test error handling when translation fails
5. Verify translation is cached and reused

### Error Handling Tests
1. Test translation when Gemini API is unavailable
2. Verify fallback to original content
3. Test redirect when no modules exist
4. Verify default module assignment

## API Endpoints

### Translation API
```
POST /api/translate-content
Headers: Authorization: Bearer {token}
Body: {
  "chapter_title": string,
  "chapter_content": string,
  "target_language": "ur"
}
Response: {
  "translated_content": string,
  "cache_key": string,
  "ttl_seconds": integer
}
```

### Module Access Tracking
```
POST /api/modules/{module_id}/access
Headers: Authorization: Bearer {token}
Body: {
  "position": integer (optional)
}
```

## Database Schema Changes

The feature requires adding tables to track user session extensions and translation caching:

```sql
-- Track user's last accessed module and language preferences
CREATE TABLE user_session_extensions (
  user_id VARCHAR(255) PRIMARY KEY,
  last_module_id VARCHAR(255),
  language_preference VARCHAR(10) DEFAULT 'en',
  last_access_time TIMESTAMP,
  default_module_id VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES user_accounts(id)
);

-- Cache translations to improve performance
CREATE TABLE translation_cache (
  content_hash VARCHAR(255) NOT NULL,
  target_language VARCHAR(10) NOT NULL,
  translated_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  original_content_length INTEGER,
  PRIMARY KEY (content_hash, target_language)
);

-- Log module access for redirect tracking
CREATE TABLE module_access_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id VARCHAR(255) NOT NULL,
  module_id VARCHAR(255) NOT NULL,
  access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  session_id VARCHAR(255),
  position INTEGER,
  FOREIGN KEY (user_id) REFERENCES user_accounts(id)
);
```

## Performance Considerations

- Translation requests should timeout after 30 seconds with progress indicator
- Translation cache expires after 24 hours to balance performance with content freshness
- Database queries should use appropriate indexes on user_id and module_id fields
- API responses should be kept under 3 seconds as per constitution requirements

## Security Notes

- Gemini API key must be stored in environment variables, never in code
- All translation requests must be authenticated
- User session data should be properly validated
- Content hashes should be securely generated