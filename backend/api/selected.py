from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.utils.chatkit_client import stream_message

router = APIRouter()

@router.get("/selected-chat-stream")
async def selected_chat_stream(user_id: str, question: str, selected_text: str):

    async def event_generator():
        for chunk in stream_message(message=question, context=selected_text):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")
