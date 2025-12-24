---
id: 4
title: Plan Architecture
stage: plan
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-humanoid-textbook
branch: 2-humanoid-textbook
user: claude
command: /sp.plan
labels: [planning, architecture, rag, textbook, humanoid-robotics]
links:
  spec: specs/2-humanoid-textbook/spec.md
  plan: specs/2-humanoid-textbook/plan.md
  data-model: specs/2-humanoid-textbook/data-model.md
  research: specs/2-humanoid-textbook/research.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-humanoid-textbook/plan.md
  - specs/2-humanoid-textbook/data-model.md
  - specs/2-humanoid-textbook/research.md
  - specs/2-humanoid-textbook/quickstart.md
tests:
---

## Prompt

```text
## Phase 0: Project Setup & Governance (Foundation)

### Goals
- Establish a stable development baseline
- Lock scope and prevent feature creep

---

## Phase 1: AI/Spec-Driven Book Creation (Core Requirement)

### Goals
- Publish a complete, structured textbook
- Reflect the Physical AI & Humanoid Robotics curriculum accurately

### Tasks
- Create Docusaurus site structure
- Write chapters based on modules:
  - Physical AI foundations
  - ROS 2
  - Gazebo & Unity
  - NVIDIA Isaac
  - Vision-Language-Action
  - Capstone project
- Use MDX for extensibility
- Add diagrams, code blocks, and structured explanations
- Ensure navigation consistency

### Exit Criteria
- Book is readable end-to-end
- All modules and weeks are represented
- Site deployed to GitHub Pages

---

## Phase 2: RAG Backend Infrastructure (Core Requirement)

### Goals
- Enable retrieval-based question answering over book content

### Tasks
- Build FastAPI backend
- Implement document ingestion pipeline:
  - Parse book content
  - Chunk text
  - Generate embeddings using **Gemini Embeddings API**
- Store embeddings in Qdrant Cloud
- Store metadata in Neon Postgres
- Implement RAG query endpoint:
  - Retrieve relevant chunks
  - Construct constrained prompt
  - Generate response via Gemini

### Exit Criteria
- Backend can answer questions based on book content
- No OpenAI APIs used
- Queries return accurate, grounded answers

---

## Phase 3: Embedded Chatbot UI (Core Requirement)

### Goals
- Provide an intuitive chatbot inside the book

### Tasks
- Build React-based chatbot component inside Docusaurus
- Connect chatbot to FastAPI backend
- Support:
  - Free-form book questions
  - Loading and error states
- Ensure chatbot works across all chapters

### Exit Criteria
- Add "chatbot" button placed on right bottom of the page when user click on this button chatbot visible.
- Chatbot visible and usable in the book UI
- Stable responses with acceptable latency

---

## Phase 4: Selection-Based Contextual RAG (NON-NEGOTIABLE)

### Goals
- Allow users to ask questions strictly about selected text

### Tasks
- Implement text selection listener in Docusaurus
- Capture selected text
- Enforce selection size limit (Option B):
  - Max ~2000 tokens / ~8000 characters
- Inject selected text into chatbot context
- Display UI indicator: "Selection Context Mode"
- Backend validation to reject oversized selections

### Exit Criteria
- Selecting text limits chatbot answers to that text
- Clear feedback when selection exceeds limits
- Judges can verify scoped answering

---

## Phase 5: Authentication & User Profiles (Bonus)

### Goals
- Enable personalized experiences for logged-in users

### Tasks
- Integrate Better-Auth:
  - Signup
  - Signin
- Collect user background at signup:
  - Software experience
  - Hardware/robotics experience
- Store profiles securely in Neon Postgres
- Protect authenticated routes

### Exit Criteria
- Users can sign up and log in
- Background data stored correctly
- Auth does not break core features

---

## Phase 6: Chapter-Level Personalization (Bonus)

### Goals
- Adapt content to user background

### Tasks
- Add "Personalize Chapter" button at chapter start
- Use user profile data to:
  - Adjust explanations
  - Highlight relevant examples
- Use Gemini for personalization generation
- Ensure original content remains accessible

### Exit Criteria
- Personalized content clearly differs from default
- Users can toggle personalization

---

## Phase 7: Urdu Translation (Bonus)

### Goals
- Enable multilingual accessibility

### Tasks
- Add "Translate to Urdu" button at chapter start
- Use Gemini for translation
- Preserve:
  - Code blocks
  - Headings
  - Technical terms
- Ensure translation is on-demand (not pre-generated)

### Exit Criteria
- Accurate Urdu translations
- No corruption of code or structure

---

## Phase 8: Reusable Intelligence (Bonus)

### Goals
- Demonstrate advanced AI engineering via reuse

### Tasks
- Create Claude Code Subagents:
  - Content summarizer
  - Chapter explainer
  - RAG prompt optimizer
- Define Agent Skills
- Reuse agents across multiple chapters

### Exit Criteria
- At least one reusable agent demonstrated
- Clear documentation of agent roles

---

## Phase 9: Testing, Hardening & Demo Prep

### Goals
- Ensure stability and judge-ready polish

### Tasks
- Test:
  - Chatbot accuracy
  - Selection-based constraints
  - Auth flows
- Validate performance on free-tier services
- Prepare demo script:
  - Book walkthrough
  - Chatbot Q&A
  - Selection-based question
  - Personalization / Urdu (if implemented)

### Exit Criteria
- No critical bugs
- Demo runs smoothly
- All hackathon requirements satisfied

---

## Risk Management

| Risk | Mitigation |
|-----|-----------|
| Token overuse | Strict selection limits |
| Latency | Cached embeddings + small context |
| Feature creep | Constitution enforcement |
| Auth complexity | Optional bonus phase |

---

## Completion Definition

The project is considered complete when:
- The book is live
- The RAG chatbot is embedded
- Selection-based QA works reliably
- Bonus features (if present) do not break core functionality

---

## Plan Version
**Version:** 1.0.0
**Status:** Approved for `/sp.tasks`
**Next Step:** `/sp.tasks`
```

## Response snapshot

Completed the implementation planning for the Physical AI & Humanoid Robotics Textbook Platform. The planning included:

1. Created a comprehensive implementation plan (plan.md) that emphasizes the RAG chatbot with selection-based contextual answers as the core feature, in line with the constitution's requirements.

2. Updated the data model (data-model.md) to include RAG-specific entities including RAGSession and SelectedTextContext, which are essential for the selection-based contextual RAG functionality.

3. Maintained the existing research summary (research.md) that covers technology stack selection, architecture patterns, and other important decisions.

4. The plan aligns with all constitution requirements including:
   - Selection-based contextual RAG (NON-NEGOTIABLE)
   - Google Gemini API as the primary LLM provider
   - Non-breaking extension architecture
   - Performance requirements (RAG responses ≤ 3 seconds)

The implementation plan provides a clear roadmap for building the interactive textbook platform with embedded RAG chatbot, authentication, personalization, and Urdu translation features.

## Outcome

- ✅ Impact: Comprehensive implementation plan created with RAG focus
- 🧪 Tests: No tests required for planning artifacts
- 📁 Files: Updated specs/2-humanoid-textbook/plan.md, data-model.md; referenced research.md, quickstart.md
- 🔁 Next prompts: Continue with task generation using /sp.tasks
- 🧠 Reflection: Plan properly emphasizes RAG chatbot as core feature with proper data models for selection context

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks with /sp.tasks