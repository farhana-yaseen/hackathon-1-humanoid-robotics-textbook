# Data Model: Physical AI & Humanoid Robotics Textbook Platform

## Entity: User
**Identity**: `user_id` (UUID)
**Uniqueness**: `email` must be unique

### Attributes
- `user_id`: UUID (Primary Key) - System-generated unique identifier
- `email`: String (Unique) - User's email address for authentication
- `name`: String - User's full name
- `software_background`: Text - User's software background and experience level
- `hardware_background`: Text - User's hardware background and experience level
- `created_at`: DateTime - Account creation timestamp
- `updated_at`: DateTime - Last profile update timestamp
- `data_retention_expires_at`: DateTime - Calculated retention expiry (2 years after last_active)
- `preferences`: JSON - User preferences for content delivery

### Relationships
- One-to-many with PersonalizationProfile
- One-to-many with Translation (session-based)
- One-to-many with RAGSession (optional for authenticated sessions)

## Entity: Chapter
**Identity**: `chapter_id` (UUID)
**Uniqueness**: `title` must be unique within the textbook

### Attributes
- `chapter_id`: UUID (Primary Key) - Unique identifier for each chapter
- `title`: String (Unique within textbook) - Chapter title
- `slug`: String (Unique) - URL-friendly identifier
- `content`: Text - Original English Markdown content
- `word_count`: Integer - Number of words in chapter
- `module`: String - Module category (ROS 2, Digital Twin, etc.)
- `created_at`: DateTime - Creation timestamp
- `updated_at`: DateTime - Last update timestamp
- `metadata`: JSON - Additional chapter metadata

### Relationships
- One-to-many with PersonalizationProfile (via chapter_id reference)
- One-to-many with Translation (via chapter_id reference)
- One-to-many with SelectedTextContext (via chapter_id reference)

## Entity: PersonalizationProfile
**Identity**: `profile_id` (UUID)
**Uniqueness**: One profile per user per chapter

### Attributes
- `profile_id`: UUID (Primary Key) - Unique identifier for each profile
- `user_id`: UUID (Foreign Key) - Reference to User
- `chapter_id`: UUID (Foreign Key) - Reference to Chapter
- `personalized_content`: Text - Personalized version of chapter content
- `personalization_rules`: JSON - Rules used for personalization
- `created_at`: DateTime - Creation timestamp
- `updated_at`: DateTime - Last update timestamp

### Relationships
- Many-to-one with User
- Many-to-one with Chapter
- One-to-one with user per chapter (uniqueness constraint)

## Entity: Translation
**Identity**: `translation_id` (UUID)
**Uniqueness**: One Urdu translation per chapter per user session

### Attributes
- `translation_id`: UUID (Primary Key) - Unique identifier for each translation
- `chapter_id`: UUID (Foreign Key) - Reference to Chapter
- `user_session_id`: UUID - Session identifier for temporary translations
- `urdu_content`: Text - Urdu translation of chapter content
- `translation_quality_score`: Float - Quality score from 0-1
- `created_at`: DateTime - Creation timestamp
- `expires_at`: DateTime - Expiration timestamp for temporary translations

### Relationships
- Many-to-one with Chapter
- One-to-many with user session (temporary storage)

## Entity: RAGSession
**Identity**: `session_id` (UUID)
**Uniqueness**: One active session per user context

### Attributes
- `session_id`: UUID (Primary Key) - Unique identifier for each RAG session
- `user_id`: UUID (Foreign Key to User, optional) - Reference to user (null for anonymous sessions)
- `session_token`: String - Token for anonymous session identification
- `created_at`: DateTime - Session creation time
- `last_interaction_at`: DateTime - Last interaction time
- `active_selection_context`: Text (optional, max 2000 tokens) - Current selected text context

### Relationships
- Many-to-one with User (via user_id, optional)
- One-to-many with SelectedTextContext (via session_id)

## Entity: SelectedTextContext
**Identity**: `context_id` (UUID)
**Uniqueness**: One active selection per session

### Attributes
- `context_id`: UUID (Primary Key) - Unique identifier for each selected text context
- `session_id`: UUID (Foreign Key to RAGSession) - Reference to the session
- `selected_text`: Text (max 2000 tokens) - The selected text content
- `chapter_id`: UUID (Foreign Key to Chapter) - Reference to the source chapter
- `created_at`: DateTime - Creation timestamp
- `expires_at`: DateTime - Expiration time for privacy (short-lived)

### Relationships
- Many-to-one with RAGSession (via session_id)
- Many-to-one with Chapter (via chapter_id)

## Validation Rules
- User email must be unique and valid email format
- Chapter title must be unique within the textbook
- PersonalizationProfile must have unique user_id + chapter_id combination
- Content fields must not exceed reasonable length limits
- Background fields must be non-empty for registered users
- Selected text must not exceed 2000 tokens (enforced for RAG context window)
- Data retention policy: User data expires 2 years after last_active
- SelectedTextContext expires_at must be in the future (short-lived for privacy)

## State Transitions
- User: Created → Active (after email verification) → Inactive (after retention period)
- Chapter: Draft → Published → Archived
- PersonalizationProfile: Created → Generated → Updated
- Translation: Requested → Processing → Completed → Cached
- RAGSession: Created → Active → Expired
- SelectedTextContext: Created → Active → Expired (short-lived)

## Indexes
- User.email: Unique index for authentication performance
- User.last_active: Index for retention policy queries
- Chapter.slug: Unique index for routing
- PersonalizationProfile.user_id + chapter_id: Composite unique index
- Translation.chapter_id: Index for translation retrieval
- RAGSession.user_id: Index for user session queries
- SelectedTextContext.session_id: Index for session context queries
- SelectedTextContext.expires_at: Index for cleanup operations