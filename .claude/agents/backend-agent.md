---
name: backend-agent
description: use this agent for generate backend code
model: sonnet
---

# backend-agent

**Frontend**: Docusaurus running on port 3000.  
**Backend**: Python FastAPI, running on port 8000.  
**Backend database**: Neon Serverless Postgres.  
**Vector search**: Qdrant Cloud (Free Tier).  
**Authentication**: Better Auth.

I want Claude to generate **complete working code** for me, including:

1. **Backend (FastAPI)**:
   - Endpoints for login, signup, and logout using Better Auth.
   - Endpoint to accept a user query, convert it into embeddings, search similar vectors in Qdrant, fetch related text from Postgres metadata, and return the context + answer.
   - Load secrets (Better Auth URL/Secret, Postgres URL, Qdrant API Key) from `.env`.
   - CORS enabled for frontend `http://localhost:3000`.

2. **Frontend (Docusaurus)**:
   - Auth button (login/signup/logout) that calls backend endpoints.
   - Form to send user query to backend `/query` endpoint and display LLM responses.
   - Load backend URL from `.env.local` (NEXT_PUBLIC_BACKEND_URL or similar).

3. **.env files**:
   - Backend `.env` with sensitive credentials (Better Auth secret, database URL, Qdrant key).
   - Frontend `.env.local` with public backend URL only.

6. **RAG workflow** integrated:
   - Convert user query to embeddings.
   - Search similar vectors in Qdrant.
   - Fetch related text from metadata.
   - Include this context when calling the llm.
