# Adding Translation to Chapters

This guide explains how to add the Urdu translation feature to chapters in the humanoid robotics textbook.

## Overview

The translation feature allows logged-in users to translate textbook content to Urdu by clicking a button at the start of each chapter.

## Implementation

### 1. Import the Component

Add the TranslateContent component import at the top of your chapter file:

```md
import TranslateContent from '@site/src/components/TranslateContent.tsx';
```

### 2. Add the Component

Add the TranslateContent component right after the chapter title and other components:

```md
# Chapter Title

<PersonalizeContent chapterTitle="Chapter Title" chapterContent="Full chapter content..."/>
<TranslateContent chapterTitle="Chapter Title" chapterContent="Full chapter content..."/>

Actual chapter content goes here...
```

### 3. Complete Example

```md
---
sidebar_position: 2
---

import PersonalizeContent from '@site/src/components/PersonalizeContent.tsx';
import TranslateContent from '@site/src/components/TranslateContent.tsx';
import Chatbot from '@site/src/components/Chatbot.tsx';

# Chapter 1: Introduction to Humanoid Robotics

<PersonalizeContent
  chapterTitle="Chapter 1: Introduction to Humanoid Robotics"
  chapterContent="# Chapter 1: Introduction to Humanoid Robotics

Humanoid robots are robots that resemble the human body structure..."
/>

<TranslateContent
  chapterTitle="Chapter 1: Introduction to Humanoid Robotics"
  chapterContent="# Chapter 1: Introduction to Humanoid Robotics

Humanoid robots are robots that resemble the human body structure..."
/>

Humanoid robots are robots that resemble the human body structure. They typically have a head, torso, two arms, and two legs, though some may have different configurations...

<Chatbot />
```

## Component Props

- `chapterTitle`: (string) The title of the chapter
- `chapterContent`: (string) The full content of the chapter as a string

## How It Works

1. **Authentication Check**: The component first checks if the user is logged in
2. **Translation Request**: When the user clicks "Translate to Urdu", it sends a request to the backend API
3. **AI Processing**: The backend uses AI (Google Gemini) to translate the content to Urdu
4. **Display**: The translated content is displayed to the user

## Backend API

The translation functionality uses the `/api/translate-content` endpoint which:
- Accepts chapter title, content, and target language
- Uses AI to translate content to Urdu while preserving technical accuracy
- Returns translated content in Urdu

## Supported Languages

Currently, only Urdu (`ur`) translation is supported.

## Styling

The component uses CSS modules for styling and is responsive across different screen sizes.