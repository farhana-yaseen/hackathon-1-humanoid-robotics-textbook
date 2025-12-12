---
id: 1
title: Fix process not defined error
stage: general
date: 2025-12-09
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 2-humanoid-textbook
user: user
command: manual
labels: [bug-fix, frontend, docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - D:/hackthon/hackathon1/humanoid-robotics-textbook/website/src/components/Chatbot.tsx
tests:
 - none
---

## Prompt

Fix the "Uncaught ReferenceError: process is not defined" error that was occurring in the Chatbot component of the Docusaurus application.

## Response snapshot

Fixed the error by modifying the Chatbot.tsx file to remove the reference to `process.env` which is not available in the browser environment. The code was changed from:
```javascript
const BACKEND_URL = typeof window !== 'undefined'
  ? (window as any).BACKEND_API_URL || "http://localhost:3001/api"
  : process.env.BACKEND_API_URL || "http://127.0.0.1:3001/api";
```

To:
```javascript
const BACKEND_URL = (window as any).BACKEND_API_URL || "http://localhost:3001/api";
```

This ensures the component works properly in the browser environment without throwing the error.

## Outcome

- ✅ Impact: Fixed the runtime error that was preventing the Chatbot component from loading
- 🧪 Tests: none
- 📁 Files: Modified Chatbot.tsx to remove process.env reference
- 🔁 Next prompts: none
- 🧠 Reflection: The issue was caused by trying to access Node.js-specific globals in browser environment

## Evaluation notes (flywheel)

- Failure modes observed: Runtime error in browser when component loaded
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A