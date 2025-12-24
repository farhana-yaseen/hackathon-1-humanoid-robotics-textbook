# Testing Plan: Authentication Redirect & Urdu Translation

## End-to-End Tests

### Authentication Redirect Flow
1. **Sign In Redirect Test**
   - Navigate to sign-in page
   - Enter valid credentials
   - Verify redirect to appropriate module page (not home page)
   - For new users: verify redirect to default module (e.g., "/modules/introduction")
   - For returning users: verify redirect to last accessed module

2. **Module Access Tracking Test**
   - Sign in as existing user
   - Navigate to different modules
   - Verify that access is recorded in the system
   - Sign out and sign back in
   - Verify redirect to the last accessed module

3. **Default Module Test**
   - Sign in as new user
   - Verify redirect to default module (e.g., "/modules/introduction")

### Translation Functionality Test
1. **Translate to Urdu Test**
   - Navigate to any module page
   - Click "Translate to Urdu" button
   - Verify content is translated to Urdu
   - Verify formatting is preserved (headings, paragraphs, lists)

2. **Toggle Language Test**
   - Translate content to Urdu
   - Click "Translate to English" button
   - Verify content switches back to English
   - Click "Translate to Urdu" button again
   - Verify content switches back to Urdu

3. **Language Preference Persistence Test**
   - Translate content to Urdu
   - Refresh the page
   - Verify language preference is maintained
   - Navigate to different module
   - Return to original module
   - Verify language preference is maintained per module

4. **Error Handling Test**
   - Disconnect from internet or disable backend
   - Attempt to translate content
   - Verify error message is displayed
   - Verify original content remains visible
   - Reconnect and try again
   - Verify translation works

5. **Timeout Handling Test**
   - Simulate slow backend response (>30 seconds)
   - Verify timeout error message is displayed
   - Verify original content remains visible

## Performance Tests

### Translation Response Times
1. **Cache Hit Test**
   - Translate content for the first time
   - Measure response time
   - Translate same content again
   - Verify faster response time due to caching

2. **Cache Miss Test**
   - Translate new/unseen content
   - Measure response time
   - Verify it takes longer than cached content

### System Performance
1. **Concurrent Users Test**
   - Simulate multiple users translating content simultaneously
   - Monitor system performance
   - Verify no degradation in service

## API Endpoint Tests

### Authentication Redirect Endpoints
1. `POST /api/auth/signin`
   - Test with valid credentials
   - Test with invalid credentials
   - Verify correct redirect URL in response

2. `GET /api/auth/redirect-url`
   - Test with existing user who has accessed modules
   - Test with new user
   - Verify correct redirect URL returned

3. `POST /api/auth/modules/{module_id}/access`
   - Test recording module access
   - Verify access is properly stored
   - Test with different users and modules

### Translation Endpoints
1. `POST /api/translate-content`
   - Test translation functionality
   - Test caching mechanism
   - Test error handling
   - Test timeout handling

2. `POST /api/v1/translation/chapters/{chapter_id}/translate`
   - Test chapter-specific translation
   - Test caching mechanism
   - Test error handling
   - Test timeout handling

3. `POST /api/translate-chapter`
   - Test simple translation endpoint
   - Test caching mechanism
   - Test error handling

## Integration Tests

### Full User Journey Test
1. User signs up
2. User signs in (redirected to default module)
3. User accesses several modules
4. User translates content in multiple modules
5. User toggles between languages
6. User signs out
7. User signs back in (redirected to last accessed module)
8. User's language preferences are maintained

## Regression Tests

### Existing Functionality
1. Verify RAG chatbot still works
2. Verify personalization features still work
3. Verify existing authentication flows still work
4. Verify all existing API endpoints still function
5. Verify database operations still work correctly

## Success Criteria

### Authentication Redirect
- [ ] Users are redirected to appropriate module after sign-in
- [ ] New users are redirected to default module
- [ ] Returning users are redirected to last accessed module
- [ ] Module access is properly recorded
- [ ] No regression in existing auth functionality

### Translation Functionality
- [ ] Content translates accurately to Urdu
- [ ] Formatting is preserved during translation
- [ ] Language toggle works correctly
- [ ] Language preferences persist across sessions
- [ ] Error handling is robust
- [ ] Caching improves performance
- [ ] Timeout handling is graceful

### Performance
- [ ] Translation responses are under 30 seconds
- [ ] Cached translations load quickly
- [ ] System handles multiple concurrent users
- [ ] No performance degradation

### User Experience
- [ ] UI is intuitive and user-friendly
- [ ] Error messages are clear and helpful
- [ ] Language toggle is easily discoverable
- [ ] Original content remains accessible