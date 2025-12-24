# Better-Auth Module

This module provides comprehensive authentication support using Better-Auth framework with custom onboarding flow, user profile management, and vector synchronization capabilities.

## Features

- **User Authentication**: Complete signup, signin, and signout functionality
- **User Profiles**: Store user background information (software, hardware, robotics experience)
- **Onboarding Flow**: Multi-step form for collecting user background
- **Vector Synchronization**: Sync user attributes to Qdrant for personalization
- **Rate Limiting**: Prevents abuse with 5 attempts per 15 minutes per IP
- **Session Management**: HTTP-only cookies for secure session handling
- **Audit Logging**: Comprehensive logging of authentication events

## Architecture

```
auth_better/
├── better_auth_router.py    # Main API endpoints
├── user_profile_model.py    # Pydantic models for user profiles
├── user_profile_service.py  # Business logic for user profiles
├── vector_sync_service.py   # Vector synchronization logic
├── session_manager.py       # Session management with JWT
├── rate_limiter.py          # Rate limiting implementation
├── logging_config.py        # Authentication event logging
├── user_profile_skill.py    # Agent skill for profile creation
├── session_skill.py         # Agent skill for session verification
├── vector_sync_skill.py     # Agent skill for vector sync
└── README.md                # This file
```

## API Endpoints

- `POST /auth/signup` - User registration with profile data
- `POST /auth/signin` - User authentication
- `POST /auth/signout` - User logout
- `POST /auth/verify-session` - Verify session token
- `POST /auth/create-profile` - Create/update user profile
- `POST /auth/sync-vector` - Sync user profile to vector database

## Security Features

- Rate limiting (5 attempts per 15 minutes per IP)
- HTTP-only cookies for session tokens
- Input validation and sanitization
- Comprehensive audit logging
- Secure password handling (simulated)

## Integration

The module integrates with:
- Neon Postgres for user profile storage
- Qdrant for vector storage and personalization
- Existing agent framework through skills
- Docusaurus frontend via API endpoints