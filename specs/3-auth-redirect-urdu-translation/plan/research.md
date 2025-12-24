# Research Summary: Authentication Redirect & Urdu Translation

## Module Page Structure and Routing

### Decision: Module Page Structure and Routing
**Rationale**: Based on the existing codebase, the Module Page is likely a Docusaurus page that displays educational content. The redirect should be handled by updating the auth callback to redirect to a module-specific route instead of the home page.

**Research Findings**:
- Docusaurus uses React-based pages in the `website/src/pages` directory
- Authentication is handled via Better-Auth with callback endpoints
- The redirect can be implemented by modifying the sign-in callback to point to `/modules` or a specific module route

**Alternatives considered**:
- Docusaurus-based routing: Use Docusaurus's built-in routing system to handle redirects
- React Router integration: Add React Router for more complex navigation
- Custom FastAPI endpoints: Create backend endpoints to handle the redirect logic

**Chosen Approach**: Docusaurus-based routing with auth callback modification

## Last Accessed Module Tracking

### Decision: Last Accessed Module Tracking
**Rationale**: User experience improvement to return to previous position. The most effective approach is to store the last accessed module in the database and retrieve it during the auth callback.

**Research Findings**:
- User session data can be stored in the Neon Postgres database
- Better-Auth provides hooks to store additional user data
- Module access can be tracked via API calls when users navigate to modules

**Alternatives considered**:
- Browser local storage: Simple but not persistent across devices
- Server-side session tracking: Requires server-side session management
- Database persistence in Neon Postgres: Most reliable and persistent solution

**Chosen Approach**: Database persistence in Neon Postgres with Better-Auth integration

## Translation Button Integration

### Decision: Translation Button Integration
**Rationale**: The translation functionality needs to integrate seamlessly with the existing Docusaurus chapter pages. A React component approach allows for dynamic content translation without page reloads.

**Research Findings**:
- The existing `TranslateContent.js` component already implements translation functionality
- The button should be placed near chapter content as specified
- Integration can be done by importing and using the existing component

**Alternatives considered**:
- React component injection: Add the translation component to existing pages
- Docusaurus plugin: Create a custom plugin for translation functionality
- Custom MDX component: Extend MDX to include translation features

**Chosen Approach**: React component injection using the existing `TranslateContent.js`

## Translation Caching Strategy

### Decision: Translation Caching Strategy
**Rationale**: As specified in the clarifications, translations should be cached temporarily (24 hours) to reduce API calls while ensuring content freshness.

**Research Findings**:
- Browser local storage can store translations temporarily
- Cache key can be based on content hash and target language
- Expiration can be handled by storing timestamps

**Alternatives considered**:
- Browser local storage (24-hour cache): Simple and effective
- Server-side caching: Requires backend infrastructure
- CDN-level caching: Overkill for this use case

**Chosen Approach**: Browser local storage with 24-hour expiration

## Language Preference Persistence

### Decision: Language Preference Persistence
**Rationale**: To maintain user's language choice within module navigation, we need to store the preference in a way that persists during the session.

**Research Findings**:
- Browser session storage is ideal for temporary persistence
- Local storage can be used for longer persistence if needed
- The preference should be scoped to the current module

**Alternatives considered**:
- Browser session storage: Perfect for current session persistence
- URL parameters: Would clutter URLs and not persist
- Local storage with expiration: Good for longer-term persistence

**Chosen Approach**: Browser session storage for the current session

## Backend Translation API

### Decision: Backend Translation API
**Rationale**: The translation functionality requires a backend service to interface with the Gemini API, which should be implemented as a FastAPI endpoint.

**Research Findings**:
- FastAPI is already used in the backend
- Gemini API integration exists in the codebase
- The API should follow the existing patterns in `backend/api/translate.py`

**Alternatives considered**:
- Direct frontend Gemini API calls: Security risk due to API key exposure
- Server-side translation service: More secure and maintainable
- Third-party translation service: Would require additional dependencies

**Chosen Approach**: Server-side translation service using existing Gemini integration