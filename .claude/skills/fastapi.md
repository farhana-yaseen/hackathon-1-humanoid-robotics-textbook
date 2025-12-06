### **6.2 FastAPI Endpoint Generator**
- Writes Python endpoints for:
  - `/chat`
  - `/translate`
  - `/personalize`
  - `/rag/query`
- Adds Pydantic models + router registration.

### **6.3 Database Connector Setup**
- Generates Neon/Postgres connection boilerplate.
- Creates user profile schema & RAG metadata tables.

### **6.4 Deployment Preparer**
- Creates GitHub Actions workflow:
  - Build Docusaurus → Deploy to GitHub Pages
  - Deploy FastAPI to Cloud Run/Railway
- Generates `.dockerignore`, `Dockerfile`, and Python `requirements.txt`.
