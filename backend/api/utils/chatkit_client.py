import google.generativeai as genai
import os
from typing import Generator

# Google Generative AI configuration - will be set dynamically in functions
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
        # Get the API key from environment
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            yield "Error: GEMINI_API_KEY is not set in environment"
            return

        # Configure with the API key
        genai.configure(api_key=gemini_api_key)
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
        error_msg = str(e)
        # Check if it's specifically an API key error
        if "API key" in error_msg or "403" in error_msg or "leaked" in error_msg:
            yield "Error: API key issue. Please check your GEMINI_API_KEY configuration."
        else:
            yield f"Error: {error_msg}"
