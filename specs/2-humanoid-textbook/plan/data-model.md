# Data Model: Personalization and Translation Features

## User Profile Data Model

### User Background Schema
```json
{
  "user_id": "string (primary key)",
  "software_experience": "string (optional)",
  "hardware_experience": "string (optional)",
  "robotics_experience": "string (optional)",
  "programming_languages": "string[] (optional)",
  "hardware_platforms": "string[] (optional)",
  "years_of_experience": "number (optional)",
  "primary_interest": "string (optional)",
  "education_level": "string (optional)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Content Data Model

### Chapter Content Schema
```json
{
  "chapter_id": "string (primary key)",
  "title": "string",
  "content": "string (markdown)",
  "original_language": "string (default: 'en')",
  "word_count": "number",
  "sources_count": "number",
  "peer_reviewed_sources_count": "number",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Personalization Data Model

### Personalization Request Schema
```json
{
  "chapter_title": "string",
  "chapter_content": "string",
  "user_background": {
    "software_experience": "string (optional)",
    "hardware_experience": "string (optional)",
    "robotics_experience": "string (optional)",
    "programming_languages": "string[] (optional)",
    "hardware_platforms": "string[] (optional)",
    "years_of_experience": "number (optional)",
    "primary_interest": "string (optional)",
    "education_level": "string (optional)"
  }
}
```

### Personalization Response Schema
```json
{
  "personalized_content": "string",
  "personalization_metadata": {
    "user_profile_used": "object",
    "personalization_timestamp": "timestamp",
    "confidence_score": "number (0-1)"
  }
}
```

## Translation Data Model

### Translation Request Schema
```json
{
  "chapter_title": "string",
  "chapter_content": "string",
  "target_language": "string (e.g., 'ur' for Urdu)"
}
```

### Translation Response Schema
```json
{
  "translated_content": "string",
  "translation_metadata": {
    "source_language": "string",
    "target_language": "string",
    "translation_timestamp": "timestamp",
    "character_count_original": "number",
    "character_count_translated": "number"
  }
}
```

## API Contract Definitions

### User Background API
- **GET** `/api/user-background/{user_id}` - Retrieve user background
  - Response: 200 with User Background Schema
  - Response: 404 if user not found
  - Response: 500 for server errors

- **POST** `/api/user-background` - Save user background
  - Request: User Background Schema (without user_id)
  - Response: 200 on success
  - Response: 400 for validation errors
  - Response: 500 for server errors

### Personalization API
- **POST** `/api/personalize-content` - Personalize chapter content
  - Request: Personalization Request Schema
  - Response: 200 with Personalization Response Schema
  - Response: 400 for invalid input
  - Response: 500 for server errors

### Translation API
- **POST** `/api/translate-content` - Translate chapter content
  - Request: Translation Request Schema
  - Response: 200 with Translation Response Schema
  - Response: 400 for invalid input or unsupported language
  - Response: 500 for server errors

## Database Schema (Neon Postgres)

### users_background table
```sql
CREATE TABLE users_background (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) UNIQUE NOT NULL,
  software_experience VARCHAR(255),
  hardware_experience VARCHAR(255),
  robotics_experience VARCHAR(255),
  programming_languages TEXT[],
  hardware_platforms TEXT[],
  years_of_experience INTEGER,
  primary_interest VARCHAR(255),
  education_level VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES better_auth_users(id)
);
```

## Vector Database Schema (Qdrant)

### User Attribute Vectors
- **Collection**: `user_profiles`
- **Vector Size**: Determined by embedding model (typically 768-1536 dimensions)
- **Payload**: User background attributes for similarity search
- **Use Case**: Personalized content recommendations based on user profile similarity