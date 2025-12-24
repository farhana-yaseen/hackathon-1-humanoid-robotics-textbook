import google.generativeai as genai
import os
from typing import Generator

# Configure Google Generative AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"

def create_chat_session(user_id: str):
    """
    Create or get a chat session for the user.
    In a real implementation, this would manage session state.
    For now, we just return the user_id as the session identifier.
    """
    return user_id

def stream_message(session_id: str = None, message: str = "", context: str = ""):
    """
    Stream a message response using Gemini.
    """
    prompt = f"""
The user selected the following text:

{context}

They asked the following question:

{message}

Give a helpful, clear answer based ONLY on the selected text.
If the answer is not contained in the provided text,
say: "I cannot answer that based on the provided text."
"""

    try:
        model = genai.GenerativeModel(MODEL)

        # Generate content with streaming
        response = model.generate_content(
            prompt,
            stream=True
        )

        # Yield streamed chunks
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error: {str(e)}"
