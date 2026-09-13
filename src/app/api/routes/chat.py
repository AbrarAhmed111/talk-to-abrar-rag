"""
Chatbot API Endpoints.
Thin route handlers delegating to chat_service.
"""

import json

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from src.app.schemas.chat import ChatRequest, ChatResponse, FastPromptsResponse
from src.app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.get("/fast-prompts", response_model=FastPromptsResponse, summary="Get Product Fast Prompts")
async def get_fast_prompts() -> FastPromptsResponse:
    """
    Returns curated, product-focused fast prompts / suggestion chips for the chatbot UI.
    """
    return chat_service.get_fast_prompts()


@router.post("", response_model=ChatResponse, summary="Chat Completion with Intent Detection & Gateway")
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main Chat Completion Endpoint:
    - Checks intent (bypasses LLM with 0 tokens for conversational greetings/thanks).
    - Routes the remaining requests directly through the LLM Gateway with multi-provider failover.
    """
    try:
        return await chat_service.process_chat(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat Execution Failed: {str(e)}",
        )


@router.post("/stream", summary="Streaming Chat Completion")
async def chat_stream_endpoint(request: ChatRequest) -> StreamingResponse:
    """Streams newline-delimited SSE events from the RAG chat service."""
    async def event_stream():
        try:
            async for event in chat_service.stream_chat(request):
                serializable_event = dict(event)
                serializable_event["status_events"] = [
                    {
                        "type": status_event.type,
                        "status": status_event.status,
                        "message": status_event.message,
                        "provider": status_event.provider,
                    }
                    for status_event in serializable_event.get("status_events", [])
                ]
                yield f"data: {json.dumps(serializable_event)}\n\n"
        except Exception as error:
            yield f"data: {json.dumps({'type': 'error', 'message': str(error)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
