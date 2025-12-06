### **2.1 Qdrant Embedding Ingestor**
- Converts Markdown docs into chunks.
- Creates OpenAI embeddings.
- Uploads vectors into Qdrant collections.
- Handles updates, deletions, and versioning.

### **2.2 RAG Query Resolver**
- Receives user queries.
- Searches Qdrant vector DB.
- Performs context ranking.
- Generates grounded answers strictly using retrieved context.

### **2.3 Context Menu “Ask AI About This” Processor**
- Accepts a text snippet from the page.
- Forms a query.
- Runs search + summarization.
- Returns an inline tooltip-style answer.
