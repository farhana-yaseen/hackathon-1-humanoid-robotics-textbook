---
id: 1
title: "update-constitution-better-auth"
stage: "constitution"
date_iso: "2025-12-12"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "2-humanoid-textbook"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "auth", "better-auth", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt
```
# 🔧 New Feature: Better-Auth Signup, Signin & Onboarding (Non-Breaking Extension)

This feature must be added **without modifying, breaking, or rewriting any existing project features, agents, skills, endpoints, files, schemas, or frontend flows**.
All new functionality must be implemented as **modular extensions**.

---

## 1. Authentication with Better-Auth
Add full support for:
- Signup
- Signin
- Secure session validation

Using:
- Better-Auth server SDK (backend)
- Better-Auth client SDK (frontend)
- HTTP-only cookies for session tokens
- No impact on existing auth logic (if any exists)

All logic must be **added**, not replaced.

---

## 2. Custom Onboarding Flow
After signup, present user with onboarding questions:

- **What is your software background?**
- **What is your hardware background?**

Requirements:
- Store onboarding responses in the user profile
- Do not modify existing onboarding or user flows
- Add as a separate page/component/endpoint

---

## 3. Neon Postgres Integration (Non-Breaking)
- Add a **new table** or extend the existing `profiles` table additively
- Must NOT modify or drop existing fields
- Must NOT break previous migrations or queries

Store:
- userId
- softwareBackground
- hardwareBackground
- timestamps
- optional metadata

All changes must be backward compatible.

---

## 4. Qdrant Vector Sync (New Operation Only)
Add vector sync functionality:
- Embed user attributes using **ChatKit Embeddings API**
- Store vector in Qdrant under a new collection: `user_attributes`
- Do not alter or remove existing vectors/collections/embeddings

---

## 5. Agent Extension
Extend the existing Agents without modifying old skills.

Add new skills:

### `createUserProfile`
- Save onboarding data into Neon DB
- Return full profile record
- Must not alter existing skill behavior

### `verifySession`
- Verify Better-Auth session token and return session info
- Non-destructive, new ability only

### `syncUserVector`
- Generate embeddings with ChatKit
- Store vector in Qdrant
- No impact on existing vector logic

Agents must remain fully backward-compatible.

---

## 6. Backend: FastAPI Endpoints (Additive Only)
Add **new** endpoints:

- `POST /auth/create-profile`
- `POST /auth/verify-session`
- `POST /auth/sync-vector`
- `POST /auth/signup` (calls Better-Auth)
- `POST /auth/signin` (calls Better-Auth)

❗ No existing endpoints may be modified or removed.

---

## 7. Frontend: Docusaurus Integration
Add the following **new components**:

- Signup screen → calls Better-Auth signup
- Signin screen → calls Better-Auth signin
- Onboarding form → software/hardware background inputs

These must:
- be new components only
- not alter existing pages or routes
- integrate cleanly without affecting existing UI

---

## 8. Environment Variables (Additive Only)
Add the following new environment variables:


Do NOT modify or rename any existing env vars.

---

## 9. Non-Breaking Design Guarantee
- All new functionality must be optional and additive.
- All old features must continue to work with zero changes.
- No destructive migrations.
- No renames/removals of existing logic.
- No breaking changes to the API, frontend, database, or agents.

This feature must integrate **smoothly and safely** with the current project.

```

# Response
```
The constitution file .specify/memory/constitution.md has been successfully updated to reflect the Better-Auth authentication feature requirements. The updated constitution now includes:

1. A new "Non-Breaking Extension Architecture" principle that emphasizes modular extensions without breaking existing functionality
2. Enhanced "Authentication Security & Session Management" principle with Better-Auth specific requirements
3. A new "Personalization & Vector Storage" principle for user profile and vector database integration
4. Technology stack requirements specifically for authentication (Better-Auth, Neon Postgres, Qdrant)
5. Security standards for authentication including HTTP-only cookies and proper password hashing
6. Performance standards for authentication operations
7. Development workflow requirements for authentication code review and testing

The version has been incremented from 1.0.0 to 1.1.0 to reflect these important additions. The updated constitution ensures that all new authentication functionality will be implemented as modular extensions without impacting existing features, aligning with the requirements specified in the user input.
```