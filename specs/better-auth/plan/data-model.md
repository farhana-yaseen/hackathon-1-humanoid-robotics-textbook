# Better-Auth Data Model

## 1. Entity Definitions

### 1.1 User Profile Entity
**Entity Name:** UserProfile
**Description:** Stores user profile information collected during onboarding

**Fields:**
- `user_id` (string, required, primary key, foreign key to Better-Auth user)
  - Uniquely identifies the user
  - References the Better-Auth user ID
  - Cannot be null

- `software_background` (text, optional)
  - User's software development experience
  - Nullable field for optional information

- `hardware_background` (text, optional)
  - User's hardware experience
  - Nullable field for optional information

- `robotics_experience` (text, optional)
  - User's robotics experience
  - Nullable field for optional information

- `programming_languages` (jsonb, optional)
  - Array of programming languages the user knows
  - Stored as JSONB for efficient querying
  - Example: ["Python", "C++", "ROS"]

- `hardware_platforms` (jsonb, optional)
  - Array of hardware platforms the user has experience with
  - Stored as JSONB for efficient querying
  - Example: ["Arduino", "Raspberry Pi", "NVIDIA Jetson"]

- `years_of_experience` (integer, optional, default: 0)
  - Number of years of experience
  - Default value of 0 for new users

- `primary_interest` (text, optional)
  - User's primary interest in robotics
  - Nullable field for optional information

- `education_level` (text, optional)
  - User's education level
  - Nullable field for optional information
  - Values: "high-school", "undergraduate", "graduate", "postgraduate", "professional"

- `created_at` (timestamp, required, default: current_timestamp)
  - Timestamp when the profile was created
  - Automatically set on creation

- `updated_at` (timestamp, required, default: current_timestamp)
  - Timestamp when the profile was last updated
  - Automatically updated on changes

**Relationships:**
- One-to-One: Better-Auth User (user_id → Better-Auth user ID)
- One-to-One: Qdrant Vector Record (user_id → Qdrant point ID)

### 1.2 Vector Record (Qdrant Collection)
**Collection Name:** user_attributes
**Description:** Stores vector embeddings of user profile attributes for personalization

**Fields:**
- `id` (string, required, primary key)
  - Matches the user_id from user_profiles table
  - Serves as the primary key in Qdrant

- `vector` (array of floats, required)
  - Embedding vector generated from user profile data
  - Used for similarity search

- `payload` (object, required)
  - Contains user profile data for reference
  - Includes: user_id, profile data, timestamps

## 2. Validation Rules

### 2.1 User Profile Validation
- `user_id`: Must be a valid Better-Auth user ID format
- `software_background`: Maximum 1000 characters
- `hardware_background`: Maximum 1000 characters
- `robotics_experience`: Maximum 1000 characters
- `programming_languages`: Maximum 20 items in array
- `hardware_platforms`: Maximum 20 items in array
- `years_of_experience`: Must be between 0 and 50
- `education_level`: Must be one of the allowed values

### 2.2 Constraints
- Foreign key constraint: user_id must reference a valid Better-Auth user
- Unique constraint: user_id must be unique across all profiles
- Not null constraints: user_id, created_at, updated_at

## 3. State Transitions

### 3.1 User Profile States
- **Uninitialized:** User exists but no profile created
- **Onboarding:** User has started but not completed onboarding
- **Complete:** User has completed onboarding and profile is fully populated

### 3.2 Transition Rules
- Uninitialized → Onboarding: User begins onboarding process
- Onboarding → Complete: User submits complete profile information
- Complete → Complete: User updates existing profile information

## 4. Indexing Strategy

### 4.1 Database Indexes
- Primary index on `user_id` (B-tree)
- Index on `created_at` (B-tree) for time-based queries
- Index on `updated_at` (B-tree) for cache invalidation
- GIN index on JSONB fields for efficient array queries

### 4.2 Qdrant Indexing
- Vector index on embedding vectors for similarity search
- Payload index on user_id for efficient lookups

## 5. Data Migration Strategy

### 5.1 Schema Changes
- Add new `user_profiles` table with foreign key to Better-Auth users
- No changes to existing tables (additive only)
- Maintain backward compatibility with existing data

### 5.2 Migration Steps
1. Create new `user_profiles` table
2. Add indexes to improve performance
3. Update application code to use new table
4. No data migration needed for existing users (profiles are optional)

## 6. Security Considerations

### 6.1 Data Protection
- Personal information stored with appropriate access controls
- Sensitive fields encrypted at rest where applicable
- Audit logging for profile access and modifications

### 6.2 Privacy Compliance
- Profile data retention policies
- User consent for data collection and usage
- Right to deletion for user profile data