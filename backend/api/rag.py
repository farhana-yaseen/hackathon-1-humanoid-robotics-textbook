from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.utils.gemini_client import embed_text
from api.utils.qdrant_client import search_qdrant
from api.utils.db import save_query
from api.utils.chatkit_client import stream_message

router = APIRouter()


@router.get("/rag-chat-stream")
async def rag_chat_stream(user_id: str, question: str):
    """
    RAG chatbot streaming endpoint using Gemini ChatKit interface.
    Streams answer as it is generated.
    """

    # 1 Embed question
    query_embedding = embed_text(question)

    # 2 Retrieve context from Qdrant
    retrieved = search_qdrant(query_embedding)
    combined_context = "\n\n".join(retrieved)

    # 3 Create or get ChatKit session (Gemini version just returns user_id)
    session = create_chat_session(user_id)

    # 4 Generator function to yield SSE data
    async def event_generator():
        answer_chunks = []
        # Use session directly instead of session.session_id
        for chunk in stream_message(session_id=session, message=question, context=combined_context):
            answer_chunks.append(chunk)
            yield f"data: {chunk}\n\n"

        # Save full answer to Neon DB
        full_answer = "".join(answer_chunks)
        await save_query(question, full_answer)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

































# for openai
# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# from api.utils.gemini_client import embed_text
# from api.utils.qdrant_client import search_qdrant
# from api.utils.db import save_query
# from api.utils.chatkit_client import create_chat_session, stream_message

# router = APIRouter()

# @router.get("/rag-chat-stream")
# async def rag_chat_stream(user_id: str, question: str):
#     """
#     RAG chatbot streaming endpoint using ChatKit.
#     Streams answer as it is generated.
#     """

#     # 1. Embed question
#     query_embedding = embed_text(question)

#     # 2. Retrieve context from Qdrant
#     retrieved = search_qdrant(query_embedding)
#     combined_context = "\n\n".join(retrieved)

#     # 3. Create or get ChatKit session
#     session = create_chat_session(user_id)

#     # 4. Generator function to yield SSE data
#     async def event_generator():
#         answer_chunks = []
#         for chunk in stream_message(session_id=session.session_id, message=question, context=combined_context):
#             answer_chunks.append(chunk)
#             yield f"data: {chunk}\n\n"

#         # Save full answer to Neon DB
#         full_answer = "".join(answer_chunks)
#         await save_query(question, full_answer)

#     return StreamingResponse(event_generator(), media_type="text/event-stream")
