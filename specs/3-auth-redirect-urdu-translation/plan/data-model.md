# Data Model: Authentication Redirect & Urdu Translation

## Entity: UserSessionExtension

Extension to the existing user session to track module access and language preferences.

### Fields
- `user_id` (string): Better-Auth user identifier (foreign key to users table)
- `last_module_id` (string, optional): Identifier of the last accessed module
- `language_preference` (string): Current language setting ("en", "ur", etc.)
- `last_access_time` (timestamp): Timestamp of last module access
- `default_module_id` (string, optional): User's default module preference

### Relationships
- Belongs to: Better-Auth User (via user_id)
- Foreign Key: References modules table for module_id fields

### Validation Rules
- `user_id` must exist in Better-Auth users table
- `language_preference` must be one of supported languages ("en", "ur")
- `last_access_time` must be a valid timestamp

## Entity: TranslationCache

Caches translated content to improve performance and reduce API calls.

### Fields
- `content_hash` (string): SHA-256 hash of original content (primary key)
- `target_language` (string): Target language code (e.g., "ur")
- `translated_content` (text): The translated content
- `created_at` (timestamp): Cache creation time
- `expires_at` (timestamp): Cache expiration time (24 hours from creation)
- `original_content_length` (integer): Length of original content in characters

### Relationships
- No direct relationships (standalone cache table)

### Validation Rules
- `content_hash` must be unique for each language
- `target_language` must be one of supported languages
- `expires_at` must be 24 hours after `created_at`
- `translated_content` must not exceed maximum text size limits

## Entity: ModuleAccessLog

Tracks user access to modules for determining "last accessed module".

### Fields
- `id` (uuid): Primary key
- `user_id` (string): Better-Auth user identifier
- `module_id` (string): Module identifier
- `access_time` (timestamp): When the module was accessed
- `session_id` (string, optional): Session identifier for tracking
- `position` (integer, optional): Scroll position or content position accessed

### Relationships
- Belongs to: Better-Auth User (via user_id)

### Validation Rules
- `user_id` must exist in Better-Auth users table
- `access_time` must be a valid timestamp
- `position` must be non-negative if provided

## State Transitions

### User Session State Transitions
1. **Unauthenticated** → **Authenticated** (on successful login)
   - Set default language preference to "en"
   - Check for last accessed module in database

2. **Authenticated** → **Module Redirect** (post-authentication)
   - Redirect to last accessed module if exists
   - Redirect to default module if no previous access

3. **Module View** → **Translation Request** (on translate button click)
   - Check cache for existing translation
   - Request new translation if not cached
   - Update language preference to "ur"

4. **Translation Active** → **Language Switch** (on toggle)
   - Switch between "en" and "ur" preferences
   - Maintain current position in module

## Constraints

### Referential Integrity
- All user_id fields must reference valid Better-Auth user records
- Module IDs should reference valid module identifiers in the system

### Data Volume Limits
- TranslationCache entries should be purged after expiration
- ModuleAccessLog entries may be archived after 30 days

### Performance Constraints
- Content hash generation should be efficient
- Database queries should use appropriate indexes