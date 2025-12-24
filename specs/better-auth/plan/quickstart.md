# Better-Auth Quickstart Guide

## 1. Prerequisites

Before implementing Better-Auth functionality, ensure you have:

- Node.js 16+ for frontend development
- Python 3.8+ for backend development
- Access to Better-Auth documentation and support
- Neon Postgres database connection
- Qdrant Cloud account and API key
- Environment properly configured with required variables

## 2. Environment Setup

### 2.1 Required Environment Variables

Add these variables to your `.env` file:

```env
BETTER_AUTH_URL=your_better_auth_url
NEON_DATABASE_URL=your_neon_database_url
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
CHATKIT_API_KEY=your_chatkit_api_key
BACKEND_URL=your_backend_url
FRONTEND_URL=your_frontend_url
JWT_SECRET=your_jwt_secret
```

### 2.2 Database Setup

1. Ensure Neon Postgres database is accessible
2. No schema changes needed (new table will be created during migration)
3. Verify database connection settings

### 2.3 Qdrant Setup

1. Ensure Qdrant Cloud is accessible
2. Verify API key and URL configuration
3. No collection creation needed (will be created automatically)

## 3. Backend Implementation

### 3.1 Install Dependencies

```bash
# In backend directory
pip install better-auth
# Other required dependencies are already installed
```

### 3.2 Configure Better-Auth

1. Create `auth_module.py` with Better-Auth integration
2. Configure server-side SDK with proper settings
3. Set up HTTP-only cookie handling

### 3.3 Implement API Endpoints

The following endpoints will be added:

- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User authentication
- `POST /api/auth/verify-session` - Session validation
- `POST /api/auth/create-profile` - Profile management
- `POST /api/auth/sync-vector` - Vector synchronization

## 4. Frontend Implementation

### 4.1 Install Dependencies

```bash
# In website directory
npm install @better-auth/client
# Other dependencies are already installed
```

### 4.2 Create Authentication Components

1. `AuthButton.tsx` - Main authentication UI component
2. `OnboardingForm.tsx` - Profile collection form
3. Session management hooks for React

### 4.3 Integration Points

- Add auth button to navigation bar
- Implement onboarding flow after signup
- Update user context with profile information

## 5. Database Schema

### 5.1 New Table: user_profiles

```sql
CREATE TABLE user_profiles (
    user_id VARCHAR(255) PRIMARY KEY,
    software_background TEXT,
    hardware_background TEXT,
    robotics_experience TEXT,
    programming_languages JSONB,
    hardware_platforms JSONB,
    years_of_experience INTEGER DEFAULT 0,
    primary_interest TEXT,
    education_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES better_auth_users(id) -- or appropriate Better-Auth table
);
```

### 5.2 Indexes

```sql
CREATE INDEX idx_user_profiles_created_at ON user_profiles(created_at);
CREATE INDEX idx_user_profiles_updated_at ON user_profiles(updated_at);
CREATE INDEX idx_user_profiles_years_experience ON user_profiles(years_of_experience);
```

## 6. Testing

### 6.1 Unit Tests

- Test user profile creation and updates
- Test authentication flow functions
- Test vector synchronization service

### 6.2 Integration Tests

- Test full signup and onboarding flow
- Test authentication and session validation
- Test vector sync with Qdrant

### 6.3 End-to-End Tests

- Complete user journey from signup to profile completion
- Verify profile data persistence
- Test vector synchronization accuracy

## 7. Security Considerations

### 7.1 Authentication Security

- Use HTTPS for all authentication operations
- Implement rate limiting (5 attempts per 15 minutes per IP)
- Use HTTP-only cookies for session tokens
- Implement proper password hashing with PBKDF2

### 7.2 Data Protection

- Encrypt sensitive profile data where appropriate
- Implement proper access controls
- Log authentication events for audit purposes

## 8. Performance Optimization

### 8.1 Database Performance

- Use proper indexing for frequently queried fields
- Implement caching for frequently accessed user profiles
- Optimize queries for profile retrieval

### 8.2 Vector Operations

- Use async processing for vector synchronization
- Implement proper error handling and retry logic
- Monitor vector sync performance

## 9. Deployment

### 9.1 Staging Deployment

1. Deploy to staging environment
2. Test all authentication flows
3. Verify profile data persistence
4. Test vector synchronization

### 9.2 Production Deployment

1. Deploy with feature flags disabled initially
2. Enable gradually with monitoring
3. Monitor authentication metrics
4. Verify all existing functionality remains intact

## 10. Troubleshooting

### 10.1 Common Issues

- **Session not persisting**: Check HTTP-only cookie configuration
- **Profile not saving**: Verify database connection and foreign key relationships
- **Vector sync failing**: Check Qdrant connection and API key

### 10.2 Monitoring

- Authentication success/failure rates
- Profile creation completion rates
- Vector synchronization status
- Database query performance