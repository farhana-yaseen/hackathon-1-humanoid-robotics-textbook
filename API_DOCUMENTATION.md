# API Documentation: Authentication Redirect & Urdu Translation

## Overview
This document describes the new API endpoints added for authentication redirect and Urdu translation functionality.

## Authentication Redirect Endpoints

### POST /api/auth/signin
Authenticate a user and return redirect URL.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```

**Response:**
```json
{
  "message": "Sign in successful",
  "user_id": "user_123456",
  "name": "user",
  "email": "user@example.com",
  "redirect_url": "/modules/introduction"
}
```

### GET /api/auth/redirect-url
Get the appropriate redirect URL after authentication based on user's last accessed module.

**Query Parameters:**
- `user_id` (string): ID of the authenticated user

**Response:**
```json
{
  "redirect_url": "/modules/introduction",
  "user_id": "user_123456",
  "last_module_id": "introduction",
  "error": null
}
```

### POST /api/auth/modules/{module_id}/access
Record when a user accesses a module for redirect tracking.

**Path Parameters:**
- `module_id` (string): ID of the module being accessed

**Request:**
```json
{
  "user_id": "user_123456",
  "module_id": "module-1",
  "session_id": "session_789",
  "position": 0
}
```

**Response:**
```json
{
  "message": "Module access recorded successfully",
  "user_id": "user_123456",
  "module_id": "module-1"
}
```

## Translation Endpoints

### POST /api/translate-content
Translate chapter content to the specified language with caching.

**Request:**
```json
{
  "chapter_title": "Introduction to Robotics",
  "chapter_content": "Robotics is an interdisciplinary branch of engineering...",
  "target_language": "ur"
}
```

**Response:**
```json
{
  "translated_content": "روبوٹکس انجینئرنگ کی ایک بین الاضلاعی شاخ ہے..."
}
```

### POST /api/v1/translation/chapters/{chapter_id}/translate
Translate a specific chapter to the target language with caching and timeout.

**Path Parameters:**
- `chapter_id` (string): ID of the chapter to translate

**Request:**
```json
{
  "chapter_id": "chapter-1",
  "target_language": "ur",
  "user_session_id": "session_789"
}
```

**Response:**
```json
{
  "translated_content": "روبوٹکس انجینئرنگ کی ایک بین الاضلاعی شاخ ہے..."
}
```

### POST /api/translate-chapter
Simple translation endpoint for testing with caching and timeout.

**Request:**
```json
{
  "chapter_id": "chapter-1",
  "target_language": "ur",
  "user_session_id": "session_789"
}
```

**Response:**
```json
{
  "translated_content": "روبوٹکس انجینئرنگ کی ایک بین الاضلاعی شاخ ہے..."
}
```

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request:**
```json
{
  "detail": "Error description"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Invalid credentials"
}
```

**408 Request Timeout:**
```json
{
  "detail": "Translation request timed out. Please try again."
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

All authentication endpoints are subject to rate limiting to prevent abuse. Excessive requests will result in a 429 status code.

## Caching

Translation endpoints use caching with a 24-hour expiration time to improve performance and reduce API calls to the translation service.