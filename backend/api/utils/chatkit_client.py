from google import generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

def stream_message(message: str, context: str = ""):
    prompt = f"""
The user selected the following text:

{context}

They asked the following question:

{message}

Give a helpful, clear answer based ONLY on the selected text.
"""

    # Start streaming
    response = genai.GenerativeModel(MODEL).generate_content(
        prompt,
        stream=True
    )

    # Yield streamed chunks
    for chunk in response:
        if chunk.text:
            yield chunk.text
