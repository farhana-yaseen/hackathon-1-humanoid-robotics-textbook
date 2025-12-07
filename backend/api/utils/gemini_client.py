import google.generativeai as genai
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Models
EMBEDDING_MODEL = "models/text-embedding-004"
model = genai.GenerativeModel("gemini-2.5-flash")


def embed_text(text: str):
    """Generate embeddings using Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return result['embedding']


def generate_answer(context: str, question: str):
    """Generate chat response using Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an AI assistant for a humanoid robotics textbook.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

If the answer is not contained in the context,
say: "I cannot answer that based on the provided text."
"""

    response = model.generate_content(prompt)
    return response.text
