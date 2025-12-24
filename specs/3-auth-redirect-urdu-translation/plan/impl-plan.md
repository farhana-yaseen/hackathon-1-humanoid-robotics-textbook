# Implementation Plan: Authentication Redirect & Urdu Translation

**Feature**: Authentication Redirect & Urdu Translation
**Branch**: 3-auth-redirect-urdu-translation
**Created**: 2025-12-21
**Status**: Draft
**Spec**: [specs/3-auth-redirect-urdu-translation/spec.md](../spec.md)

## Technical Context

This feature implements two key enhancements to the humanoid robotics textbook platform:
1. Authentication redirect to Module Page instead of Home Page after sign-in
2. Urdu translation functionality for chapter content

The system follows the architecture defined in the constitution:
- Backend: FastAPI with Better-Auth for authentication
- Database: Neon Serverless Postgres for user profiles
- LLM: Google Gemini API for translation
- Frontend: Docusaurus-based with React components

### System Architecture Overview

The feature integrates with:
- **Authentication Flow**: Better-Auth handles user sessions
- **Content Management**: Docusaurus-based chapter system
- **Translation Service**: Gemini-powered API endpoint
- **User State Management**: Session and browser storage

### Key Dependencies

- Better-Auth (authentication)
- Google Gemini API (translation)
- Neon Postgres (user data)
- Qdrant Cloud (vector storage)
- FastAPI backend services

### Unknowns / "NEEDS CLARIFICATION"

- Module Page structure and routing mechanism
- How "last accessed module" state is tracked and stored
- Integration point for translation button in Docusaurus pages
- Specific Gemini translation endpoint configuration
- Session persistence strategy for language preferences

## Constitution Check

### Compliance Verification

✅ **Spec-Driven Development**: Following approved spec from `/sp.specify`
✅ **Non-Breaking Extension**: Adding features without breaking existing functionality
✅ **Pragmatic Testing**: Planning appropriate test coverage
✅ **CLI-First & Observable**: Backend services will be CLI-runnable
✅ **RAG Chatbot Architecture**: Maintaining selection-based contextual RAG compatibility
✅ **LLM Policy**: Using Google Gemini API as required
✅ **Authentication Policy**: Using Better-Auth as required
✅ **Security & Secrets**: Following environment variable pattern
✅ **Performance Expectations**: Planning for 3-second response times

### Gate 1: Architecture Alignment
**Status**: PASSED - Aligns with FastAPI/React/Docusaurus architecture

### Gate 2: Constitution Compliance
**Status**: PASSED - All constitution requirements met

### Gate 3: Non-Breaking Extension
**Status**: PASSED - All new features are optional and additive

## Research Phase (Phase 0)

### research.md

#### Decision: Module Page Structure and Routing
**Rationale**: Need to understand the existing routing mechanism to implement post-auth redirect
**Alternatives considered**:
- Docusaurus-based routing
- React Router integration
- Custom FastAPI endpoints

#### Decision: Last Accessed Module Tracking
**Rationale**: User experience improvement to return to previous position
**Alternatives considered**:
- Browser local storage
- Server-side session tracking
- Database persistence in Neon Postgres

#### Decision: Translation Button Integration
**Rationale**: Must integrate seamlessly with Docusaurus chapter pages
**Alternatives considered**:
- React component injection
- Docusaurus plugin
- Custom MDX component

#### Decision: Translation Caching Strategy
**Rationale**: Balance performance with content freshness as specified
**Alternatives considered**:
- Browser local storage (24-hour cache)
- Server-side caching
- CDN-level caching

#### Decision: Language Preference Persistence
**Rationale**: Maintain user's language choice within module navigation
**Alternatives considered**:
- Browser session storage
- URL parameters
- Local storage with expiration

## Design Phase (Phase 1)

### data-model.md

#### Entity: UserSession
- **Fields**:
  - `user_id` (string): Better-Auth user identifier
  - `last_module_id` (string, optional): Last accessed module identifier
  - `language_preference` (string): Current language setting ("en", "ur")
  - `last_access_time` (timestamp): When module was last accessed

#### Entity: TranslationCache
- **Fields**:
  - `content_hash` (string): Hash of original content
  - `target_language` (string): Language code (e.g., "ur")
  - `translated_content` (text): Translated content
  - `created_at` (timestamp): Cache creation time
  - `expires_at` (timestamp): Cache expiration time (24 hours)

#### Entity: ModuleAccess
- **Fields**:
  - `user_id` (string): Better-Auth user identifier
  - `module_id` (string): Module identifier
  - `access_time` (timestamp): When accessed
  - `last_position` (integer): Scroll position or chapter progress

### API Contracts

#### Authentication Redirect Contract
```
POST /api/auth/callback
Request: Better-Auth callback with user session
Response:
  - Success: Redirect to /modules/{last_accessed_module} or /modules/default
  - Failure: Redirect to /auth/error
```

#### Translation API Contract
```
POST /api/translate-content
Request:
  {
    "chapter_title": string,
    "chapter_content": string,
    "target_language": "ur",
    "user_session_id": string (optional)
  }
Response:
  {
    "translated_content": string,
    "cache_key": string,
    "ttl_seconds": integer
  }
Error Responses:
  - 400: Invalid target language
  - 401: Unauthenticated user
  - 500: Translation service error
```

#### Module Access Tracking API Contract
```
POST /api/modules/{module_id}/access
Request:
  {
    "user_session_id": string,
    "position": integer (optional)
  }
Response: {}
```

### quickstart.md

#### Development Setup
```bash
# Clone repository
git clone <repo-url>
cd humanoid-robotics-textbook

# Install dependencies
cd backend
pip install -r requirements.txt

cd ../website
npm install

# Set up environment variables
cp .env.example .env
# Configure GEMINI_API_KEY, DATABASE_URL, etc.

# Run backend
cd backend
uvicorn main:app --reload

# Run frontend
cd website
npm start
```

#### Testing the Feature
1. Navigate to auth/signin page
2. Complete authentication
3. Verify redirect to Module Page instead of Home Page
4. Access a module/chapter
5. Click "Translate to Urdu" button
6. Verify content is translated while maintaining formatting
7. Test error handling when translation fails

## Agent Context Update

### Technologies Added to Context
- Better-Auth integration patterns
- Docusaurus module routing
- Gemini translation API usage
- Session-based redirect logic
- Browser storage for preferences

## Re-evaluated Constitution Check

### Post-Design Compliance
All constitution requirements continue to be met after design decisions:
- ✅ Non-breaking extension maintained
- ✅ Gemini API usage confirmed
- ✅ Better-Auth integration confirmed
- ✅ Performance targets achievable
- ✅ Security patterns followed

## Implementation Strategy

### Phase 1: Authentication Redirect
1. Update auth callback to redirect to Module Page
2. Implement last accessed module tracking
3. Create default module fallback

### Phase 2: Translation UI
1. Add "Translate to Urdu" button to module pages
2. Implement translation state management
3. Add loading and error states

### Phase 3: Translation Service
1. Create backend translation endpoint
2. Implement Gemini API integration
3. Add caching mechanism
4. Add error handling and fallbacks

### Phase 4: Integration & Testing
1. End-to-end testing of redirect flow
2. Translation functionality testing
3. Error scenario testing
4. Performance validation