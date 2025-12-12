<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (added new principles)
Added sections: Authentication Security, Personalization & Vector Storage
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/sp.constitution.md ✅ updated
Follow-up TODOs: None
-->
# Humanoid Robotics Textbook Constitution

## Core Principles

### I. Non-Breaking Extension Architecture
All new functionality must be implemented as modular extensions without modifying, breaking, or rewriting existing project features, agents, skills, endpoints, files, schemas, or frontend flows. New components must integrate cleanly without affecting existing functionality. This ensures backward compatibility and allows gradual system evolution.

### II. CLI Interface
Every library and service exposes functionality via standardized interfaces; Text-based protocols ensure debuggability: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats for all major operations and system interactions.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all new functionality including authentication, personalization, and vector storage features.

### IV. Integration Testing
Focus areas requiring integration tests: New authentication contract tests, User profile storage integration, Vector database synchronization, Inter-service communication between auth, database, and vector systems, Shared schemas across auth and personalization services.

### V. Authentication Security & Session Management
Secure authentication must use industry-standard practices: Better-Auth server SDK for backend, Better-Auth client SDK for frontend, HTTP-only cookies for session tokens, Proper password hashing with PBKDF2, JWT token validation, Secure session validation, and protection against common security vulnerabilities (CSRF, XSS, etc.).

### VI. Personalization & Vector Storage
User personalization must integrate with vector storage for personalized content delivery: Embed user attributes using ChatKit Embeddings API, Store vectors in Qdrant under dedicated collections, Maintain user profile data in Neon Postgres, Ensure vector synchronization with user profile updates, Support similarity search for personalized textbook content.

## Additional Constraints

### Technology Stack Requirements
- Authentication: Better-Auth framework with server-side SDK
- Database: Neon Serverless Postgres for user profiles
- Vector Database: Qdrant Cloud for user attribute embeddings
- Backend: FastAPI with proper dependency injection
- Frontend: React/Docusaurus with secure client-side auth integration
- Embeddings: Google Gemini for text embedding generation

### Security Standards
- All authentication endpoints must use HTTPS in production
- Passwords must be hashed using PBKDF2 with salt
- JWT tokens must have appropriate expiration times
- Session tokens must be stored in HTTP-only cookies
- All database queries must use parameterized statements
- Input validation must be performed on all user inputs
- Rate limiting should be implemented for auth endpoints

### Performance Standards
- Authentication operations should complete within 2 seconds
- User profile retrieval should be cached appropriately
- Vector search operations should return results within 1 second
- Session validation should have minimal overhead
- Database queries should use appropriate indexing

## Development Workflow

### Code Review Requirements
- All authentication-related code must be reviewed by security-conscious team members
- Database schema changes must be reviewed for migration safety
- Vector storage changes must consider performance implications
- New endpoints must include proper error handling and validation

### Testing Gates
- Authentication functionality must have 100% test coverage
- User profile operations must include both positive and negative test cases
- Vector synchronization must be tested for data consistency
- Session management must include tests for token expiration and renewal

### Deployment Approval Process
- Authentication changes require security review
- Database migrations must be tested on staging
- Vector database changes must not impact existing functionality
- All auth endpoints must pass security scanning

## Governance

All PRs/reviews must verify compliance with authentication security standards, personalization data handling, and vector storage best practices; Complexity must be justified with clear performance and security implications; Use [GUIDANCE_FILE] for runtime development guidance; Amendments require documentation of security impact assessment.

**Version**: 1.1.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-12