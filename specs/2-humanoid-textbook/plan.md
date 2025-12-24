# Implementation Plan: Physical AI & Humanoid Robotics Textbook Platform

**Branch**: `2-humanoid-textbook` | **Date**: 2025-12-13 | **Spec**: specs/2-humanoid-textbook/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Interactive textbook platform with embedded RAG chatbot for Physical AI & Humanoid Robotics education. The system enables selection-based contextual question answering using Google Gemini API, with optional personalization and Urdu translation features. Built with Docusaurus frontend, FastAPI backend, Qdrant vector storage, and Neon Postgres database. The core value proposition is connecting fragmented learning materials with contextual AI assistance that understands both the specific content and user's background.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Markdown/MDX
**Primary Dependencies**: FastAPI, Docusaurus, Qdrant Cloud, Neon Postgres, Better-Auth, Google Gemini API
**Storage**: Neon Postgres (user data), Qdrant Cloud (vector embeddings), GitHub Pages (static content)
**Testing**: pytest (backend), Jest/Cypress (frontend - if time permits)
**Target Platform**: Web application (Docusaurus site) with FastAPI backend
**Project Type**: Web
**Performance Goals**: RAG responses ≤ 3 seconds for 95% of queries, vector search ≤ 1 second
**Constraints**: Max 2000 token selections, dozens of concurrent users, Gemini API as primary LLM, selection-based contextual RAG (NON-NEGOTIABLE)
**Scale/Scope**: Dozens of users, 5-7 textbook chapters, selection-based contextual RAG

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-Driven Development: Implementation follows latest approved plan
- [x] Non-Breaking Extension: New features are modular and optional, no rewrites of existing functionality
- [x] Pragmatic Testing: Core systems (RAG, auth, personalization) will be tested, UI changes may defer tests
- [x] CLI-First & Observable: Backend services will be runnable via CLI with proper logging
- [x] RAG Architecture: Selection-based contextual RAG is implemented (NON-NEGOTIABLE)
- [x] LLM Policy: Google Gemini API is primary LLM provider, no OpenAI APIs required
- [x] Performance: RAG responses ≤ 3 seconds, vector search ≤ 1 second
- [x] Security: No secrets committed to git, proper auth implementation

## Project Structure

### Documentation (this feature)

```text
specs/2-humanoid-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   ├── chapter.py
│   │   ├── rag_session.py
│   │   └── selected_text_context.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── auth_service.py
│   │   ├── profile_service.py
│   │   └── translation_service.py
│   ├── api/
│   │   ├── rag_router.py
│   │   ├── auth_router.py
│   │   └── translation_router.py
│   └── cli/
│       └── ingestion_cli.py
└── tests/
    ├── unit/
    └── integration/

website/
├── src/
│   ├── components/
│   │   ├── Chatbot.tsx
│   │   ├── AuthButton.tsx
│   │   ├── TranslationButton.tsx
│   │   └── PersonalizationControls.tsx
│   ├── pages/
│   └── services/
│       ├── api_client.ts
│       └── text_selection.ts
└── docs/
    └── [textbook chapters]

# Shared configuration
.env.example
requirements.txt
pyproject.toml
```

**Structure Decision**: Web application structure selected with separate backend/ and website/ directories to clearly separate concerns between FastAPI backend services and Docusaurus frontend. The backend handles RAG, auth, and translation services while the frontend provides the interactive textbook experience with embedded chatbot functionality. The RAG service is the core component enabling selection-based contextual question answering as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple services | RAG, auth, and translation have different concerns and dependencies | Single monolithic service would create tight coupling and make optional features harder to implement |
| Separate vector storage | Qdrant Cloud needed for efficient similarity search in RAG | Storing embeddings in Postgres would be inefficient for vector operations |