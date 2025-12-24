import google.generativeai as genai
import os

# Configure Google Generative AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Models
EMBEDDING_MODEL = "models/text-embedding-004"


def embed_text(text: str):
    """Generate embeddings using Google's embedding model."""
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


def generate_translation(prompt: str):
    """Generate translation using Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)
    return response.text
