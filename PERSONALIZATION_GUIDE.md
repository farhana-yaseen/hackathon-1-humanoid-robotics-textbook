# Adding Personalization to Chapters

This guide explains how to add the personalization button to chapters in the humanoid robotics textbook.

## Overview

The personalization feature allows logged-in users to customize textbook content based on their background information (experience level, programming languages known, hardware platforms familiar with, etc.).

## Implementation

### 1. Import the Component

Add the PersonalizeContent component import at the top of your chapter file:

```md
import PersonalizeContent from '@site/src/components/PersonalizeContent.tsx';
```

### 2. Add the Component

Add the PersonalizeContent component right after the chapter title and before the actual content:

```md
# Chapter Title

<PersonalizeContent
  chapterTitle="Chapter Title"
  chapterContent="Full chapter content as a string..."
/>

Actual chapter content goes here...
```

### 3. Complete Example

```md
---
sidebar_position: 2
---

import PersonalizeContent from '@site/src/components/PersonalizeContent.tsx';
import Chatbot from '@site/src/components/Chatbot.tsx';

# Chapter 1: Introduction to Humanoid Robotics

<PersonalizeContent
  chapterTitle="Chapter 1: Introduction to Humanoid Robotics"
  chapterContent="# Chapter 1: Introduction to Humanoid Robotics

Humanoid robots are robots that resemble the human body structure. They typically have a head, torso, two arms, and two legs, though some may have different configurations...

[Full chapter content here]"
/>

Humanoid robots are robots that resemble the human body structure. They typically have a head, torso, two arms, and two legs, though some may have different configurations...

<Chatbot />
```

## Component Props

- `chapterTitle`: (string) The title of the chapter
- `chapterContent`: (string) The full content of the chapter as a string

## How It Works

1. **Authentication Check**: The component first checks if the user is logged in
2. **Background Retrieval**: If logged in, it retrieves the user's background information
3. **Personalization Request**: When the user clicks "Personalize Content", it sends a request to the backend API
4. **AI Processing**: The backend uses AI (Google Gemini) to adjust the content based on user background
5. **Display**: The personalized content is displayed to the user

## User Background Fields Used

The personalization considers these user background fields:
- Software experience level
- Hardware experience level
- Robotics experience level
- Programming languages known
- Hardware platforms familiar with
- Years of experience
- Primary interest in robotics
- Education level

## Backend API

The personalization functionality uses the `/api/personalize-content` endpoint which:
- Accepts chapter title, content, and user background
- Uses AI to adjust content complexity and focus areas
- Returns personalized content optimized for the user's background

## Styling

The component uses CSS modules for styling and is responsive across different screen sizes.