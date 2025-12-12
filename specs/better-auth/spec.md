# Better-Auth Signup, Signin & Onboarding Feature Specification

## 1. Feature Overview

### 1.1 Description
This feature adds comprehensive authentication support using Better-Auth framework with custom onboarding flow, user profile management, and vector synchronization capabilities. The implementation follows a non-breaking extension approach, ensuring all existing functionality remains intact while adding new capabilities.

### 1.2 Scope
- **In Scope**:
  - Better-Auth integration (signup, signin, session validation)
  - Custom onboarding flow for software/hardware background
  - Neon Postgres user profile storage
  - Qdrant vector synchronization for personalization
  - New API endpoints for auth operations
  - Frontend components for auth and onboarding
  - Agent skill extensions

- **Out of Scope**:
  - Modification of existing authentication systems
  - Changes to existing database schemas (only additive changes)
  - Updates to existing frontend flows
  - Changes to existing agent skills

### 1.3 Success Criteria
- Users can sign up and sign in using Better-Auth
- Onboarding flow collects software and hardware background information
- User profiles stored in Neon Postgres
- User attributes synchronized to Qdrant for personalization
- All new functionality is backward compatible
- Performance meets defined standards (auth ops < 2s, vector search < 1s)

## 2. Authentication Requirements

### 2.1 Better-Auth Integration
- Implement Better-Auth server SDK for backend authentication
- Implement Better-Auth client SDK for frontend authentication
- Use HTTP-only cookies for session token storage
- Support email/password authentication
- Ensure secure session validation

### 2.2 Signup Flow
- User provides email and password
- Better-Auth creates user account
- System redirects to onboarding flow after successful signup
- Passwords must be securely hashed using industry-standard methods

### 2.3 Signin Flow
- User provides email and password
- Better-Auth validates credentials
- Session established using HTTP-only cookies
- User redirected to appropriate page based on onboarding status

### 2.4 Session Management
- Implement secure session validation
- Support session refresh/expiration
- Provide session verification endpoints
- Handle session invalidation on signout

## 3. Onboarding Flow Requirements

### 3.1 Onboarding Trigger
- Display onboarding form immediately after successful signup
- Do not show onboarding for existing users without profiles
- Allow onboarding to be completed at user's discretion

### 3.2 Onboarding Questions
- **Software Background**: Text area for user to describe software experience
- **Hardware Background**: Text area for user to describe hardware experience
- Additional fields for programming languages, hardware platforms, experience levels

### 3.3 Profile Storage
- Store onboarding responses in user profile
- Link profile data to user ID from Better-Auth
- Support profile updates after initial onboarding

## 4. Database Integration Requirements

### 4.1 Neon Postgres Schema
- Create a dedicated user_profiles table with foreign key to Better-Auth user ID
- Store: userId, softwareBackground, hardwareBackground, timestamps, optional metadata
- Do not store embedding vectors in Neon (use Qdrant for vectors)
- Maintain backward compatibility with existing schema
- Do not modify or drop existing fields

### 4.2 Profile Operations
- Create user profile after signup and onboarding
- Read user profile for personalization
- Update user profile with new information
- Ensure proper indexing for performance

### 4.3 Data Migration
- Implement safe, non-destructive migrations
- Support both old and new profile formats during transition
- Maintain data integrity during schema changes

## 5. Qdrant Vector Sync Requirements

### 5.1 Vector Storage
- Create new collection: `user_attributes` in Qdrant
- Use ChatKit Embeddings API to generate user attribute embeddings
- Store user vectors for personalization
- Do not alter or remove existing vectors/collections/embeddings

### 5.2 Synchronization Process
- Use async background processing with queue/job system for vector sync
- Sync user attributes to Qdrant after profile creation/update
- Implement error handling for sync failures
- Support async synchronization to avoid blocking operations
- Monitor sync status and provide logging

### 5.3 Vector Operations
- Support similarity search for personalized content
- Update vectors when user profile changes
- Handle vector deletion when user accounts are removed
- Ensure vector data consistency with profile data

## 6. Agent Extension Requirements

### 6.1 New Skills
- **`createUserProfile`**:
  - Save onboarding data into Neon DB
  - Return full profile record
  - Must not alter existing skill behavior

- **`verifySession`**:
  - Verify Better-Auth session token and return session info
  - Non-destructive, new ability only

- **`syncUserVector`**:
  - Generate embeddings with ChatKit
  - Store vector in Qdrant
  - No impact on existing vector logic

### 6.2 Agent Compatibility
- Extend existing agents without modifying old skills
- Maintain full backward compatibility
- Ensure new skills follow existing patterns
- Add proper error handling and validation

## 7. Backend Endpoint Requirements

### 7.1 New Endpoints
- `POST /auth/create-profile`: Create user profile with onboarding data
- `POST /auth/verify-session`: Public endpoint to verify Better-Auth session token, returns basic validity info
- `POST /auth/sync-vector`: Sync user attributes to Qdrant
- `POST /auth/signup`: Call Better-Auth signup
- `POST /auth/signin`: Call Better-Auth signin

### 7.2 Endpoint Specifications
- All endpoints must be properly documented with request/response schemas
- Implement appropriate authentication and authorization
- Include comprehensive error handling
- Support both JSON and appropriate content types

### 7.3 API Contract
- Use consistent error response format
- Implement proper HTTP status codes
- Support request validation and sanitization
- Include rate limiting on auth endpoints (5 attempts per 15 minutes per IP)

## 8. Frontend Integration Requirements

### 8.1 New Components
- **Signup Screen**: Integrate with Better-Auth signup
- **Signin Screen**: Integrate with Better-Auth signin
- **Onboarding Form**: Collect software/hardware background information

### 8.2 Component Specifications
- All components must be new and not alter existing functionality
- Integrate cleanly with existing Docusaurus theme
- Follow existing styling and UI patterns
- Support responsive design

### 8.3 User Experience
- Seamless integration with existing navigation
- Clear error messaging and validation feedback
- Loading states for async operations
- Proper session management and redirects

## 9. Environment Variables

### 9.1 Required Variables
- `BETTER_AUTH_URL`: Better-Auth server URL
- `NEON_DATABASE_URL`: Neon Postgres connection string
- `QDRANT_URL`: Qdrant Cloud URL
- `QDRANT_API_KEY`: Qdrant API key
- `CHATKIT_API_KEY`: ChatKit API key for embeddings
- `BACKEND_URL`: Backend server URL
- `FRONTEND_URL`: Frontend application URL

### 9.2 Configuration Requirements
- All variables are additive (no existing vars modified)
- Proper validation and error handling for missing variables
- Secure handling of sensitive credentials
- Support for different environments (dev, staging, prod)

## 10. Non-Breaking Design Guarantees

### 10.1 Backward Compatibility
- All existing features continue to work without changes
- No breaking changes to API, frontend, database, or agents
- Safe, additive-only modifications
- Proper migration paths for existing users

### 10.2 Integration Safety
- New functionality is optional and additive
- Existing authentication systems remain intact
- No destructive operations on existing data
- Comprehensive testing to ensure no regressions

## 11. Performance Requirements

### 11.1 Response Times
- Authentication operations: < 2 seconds
- User profile retrieval: < 1 second
- Vector search operations: < 1 second
- Session validation: minimal overhead

### 11.2 Scalability
- Support concurrent user authentication
- Efficient database queries with proper indexing
- Asynchronous vector synchronization
- Caching strategies for frequently accessed data

## 12. Security Requirements

### 12.1 Authentication Security
- Use HTTPS for all authentication operations
- Implement proper password hashing (PBKDF2)
- Secure session management with HTTP-only cookies
- Protection against common vulnerabilities (CSRF, XSS, etc.)

### 12.2 Data Protection
- Encrypt sensitive user data in transit and at rest
- Proper input validation and sanitization
- Secure API endpoint access controls
- Audit logging for authentication events

## 13. Testing Requirements

### 13.1 Test Coverage
- Unit tests for all new authentication functions
- Integration tests for auth flows and database operations
- End-to-end tests for signup/onboarding flows
- Security tests for authentication vulnerabilities

### 13.2 Test Scenarios
- Successful signup and onboarding
- Failed authentication attempts
- Session expiration and renewal
- Profile creation and updates
- Vector synchronization success/failure cases

## 14. Deployment Requirements

### 14.1 Deployment Process
- Support for staged rollouts
- Database migration scripts
- Configuration for different environments
- Rollback procedures for failed deployments

### 14.2 Monitoring
- Authentication success/failure metrics
- Performance monitoring for auth operations
- Error tracking and alerting
- Vector sync status monitoring

## Clarifications

### Session 2025-12-12
- Q: Should we create a dedicated user_profiles table or extend the Better-Auth users table? → A: Create a dedicated user_profiles table with foreign key to Better-Auth user ID
- Q: How should vector synchronization be implemented - synchronous or async? → A: Async background processing with queue/job system
- Q: Should the session verification endpoint be public or private? → A: Public endpoint that returns basic validity info
- Q: Should rate limiting be implemented on auth endpoints? → A: Yes, 5 attempts per 15 minutes per IP
- Q: Should embedding vectors be stored in Neon Postgres or Qdrant? → A: Vectors only in Qdrant, not in Neon

## 15. Acceptance Criteria

- [ ] Users can successfully sign up using Better-Auth
- [ ] Users can successfully sign in using Better-Auth
- [ ] Onboarding form collects software and hardware background
- [ ] User profiles stored in Neon Postgres
- [ ] User attributes synchronized to Qdrant
- [ ] All new endpoints return proper responses
- [ ] Frontend components integrate without breaking existing UI
- [ ] All existing functionality remains intact
- [ ] Performance requirements are met
- [ ] Security requirements are satisfied
- [ ] Tests pass for all new functionality
- [ ] Environment variables are properly configured
