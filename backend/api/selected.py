from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.utils.chatkit_client import create_chat_session, stream_message

router = APIRouter()

@router.get("/selected-chat-stream")
async def selected_chat_stream(user_id: str, question: str, selected_text: str):
    """
    Chatbot endpoint that answers questions based only on selected text using Google Gemini.
    Streams answer as it is generated.
    """
    # Create a session for the user
    session = create_chat_session(user_id)

    async def event_generator():
        for chunk in stream_message(session_id=session, message=question, context=selected_text):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
