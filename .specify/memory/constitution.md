<!--
SYNC IMPACT REPORT
Version change: 1.1.0 → 1.3.0
Modified principles: RAG Stack, Embeddings, LLM Provider
Added sections: Gemini LLM Policy
Removed sections: OpenAI-specific references
Templates requiring updates:
  - .specify/templates/plan-template.md ✅
  - .specify/templates/spec-template.md ✅
  - .specify/templates/tasks-template.md ✅
  - .specify/templates/commands/sp.constitution.md ✅
-->

# Humanoid Robotics Textbook – Hackathon Constitution

## Purpose

This constitution governs the **AI / Spec-Driven creation of a Humanoid Robotics textbook**, authored using **Docusaurus** and deployed on **GitHub Pages**, with an **embedded Retrieval-Augmented Generation (RAG) chatbot**.

The project is developed during a **hackathon**, prioritizing:
- working functionality
- clarity of scope
- extensibility for bonus features
- correctness without unnecessary complexity

---

## Core Principles

### I. Spec-Driven Development (Primary Rule)

All meaningful work must follow **Spec-Kit Plus** workflow:

- Plans may be updated during hackathon time pressure
- Implementation must follow the **latest approved plan**
- Any deviation must be documented in the spec or plan

---

### II. Non-Breaking Extension Architecture

Existing functionality **must never be broken**.

New features (auth, personalization, translation, chatbot upgrades) must be:
- modular
- optional
- additive

No rewrites of:
- existing book content
- Docusaurus build system
- RAG ingestion pipeline

---

### III. Pragmatic Testing (Hackathon-Aware)

Testing is required, but **practical**:

- Core systems (RAG, auth, personalization logic) must be tested
- UI-only changes may defer tests
- Tests may be written **after implementation**, but before final submission

Goal: **confidence, not perfection**

---

### IV. CLI-First & Observable Systems

All backend systems must be:
- runnable via CLI
- debuggable without UI
- observable via logs

Guidelines:
- stdin / args → input
- stdout → success output
- stderr → errors
- JSON preferred, human-readable allowed

---

## Hackathon Scope

### In-Scope (Base Points)

- AI-assisted textbook creation using Docusaurus
- vercel deployment
- Embedded RAG chatbot
- Question answering over:
  - full book
  - user-selected text only


## RAG Chatbot Architecture
Selection-Based Contextual RAG (NON-NEGOTIABLE)

The system must support selection-based contextual question answering.
When a user selects any portion of textbook content, the selected text must be automatically injected into the RAG chatbot context.

Rules:
- The chatbot must clearly distinguish between:
  - Global book knowledge
  - User-selected local context
- When selection exists, answers must be constrained strictly to the selected text unless the user explicitly opts out.
- The UI must provide clear visual feedback that the chatbot is operating in "Selection Context Mode".
- Selected text must not be permanently stored unless explicitly approved by the user.
- This behavior must work consistently across all chapters and translations.

### Backend
- **FastAPI**
- Modular services for ingestion, retrieval, and generation

### Vector Storage
- **Qdrant Cloud (Free Tier)**
- Separate collections for:
  - book content
  - user personalization signals (optional)

### Database
- **Neon Serverless Postgres**
- Stores:
  - user profiles
  - auth metadata
  - personalization preferences

---

## LLM & Embeddings Policy (IMPORTANT)

### Primary LLM Provider
- **Google Gemini API**
- Gemini models used for:
  - answer generation
  - summarization
  - translation
  - personalization logic

❌ **OpenAI APIs must NOT be required**

---

### Embeddings
- **Gemini Embeddings API**
- Used for:
  - book content vectors
  - optional user profile vectors

Embedding logic must be:
- replaceable
- provider-agnostic at interface level

---

## Authentication (Bonus Feature)

### Auth System
- **Better-Auth**
- Entire auth system must be **optional**

### Signup Requirements
During signup, ask the user:
- software background
- hardware / robotics experience

Collected data may be used for personalization.

---

## Personalization (Bonus Feature)

- Available only for logged-in users
- Triggered via a **button at the start of each chapter**
- May include:
  - simplified explanations
  - advanced explanations
  - filtered sections

Personalization must:
- never modify original content
- be reversible
- be safe to disable globally

---

## Urdu Translation (Bonus Feature)

- Available to logged-in users
- Triggered via a **chapter-level button**
- Translation performed using **Gemini**
- English remains the source of truth

Caching is allowed but not required.

---

## Claude Code Intelligence Reuse (Bonus Feature)

Reusable intelligence is encouraged via:
- Claude Code Subagents
- Agent Skills

Examples:
- RAG query refinement agent
- Chapter summarization agent
- Translation agent
- Personalization agent

Agents must:
- be reusable
- be documented
- avoid chapter-specific hard-coding

---

## Security & Secrets

- No secrets committed to git
- `.env` files must be gitignored
- API keys loaded via environment variables
- HTTPS required in production

---

## Performance Expectations

- RAG responses ≤ 3 seconds
- Vector search ≤ 1 second
- Chatbot must not block page rendering
- vercel must remain stable

---

## Governance

- Working systems > theoretical perfection
- Base requirements must be completed before bonus features
- Any shortcut must be documented
- Architecture must remain extensible post-hackathon

---

**Version**: 1.3.0
**Ratified**: 2025-12-13
**Context**: Hackathon / Prototype Phase