"""
FastAPI routes for the AI Tutor Orchestrator.
"""
import logging
import uuid
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from models.schemas import ChatRequest, ChatResponse, ToolResponse
from graph.workflow import orchestrate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint - orchestrates tool selection and execution.
    
    This is the PRIMARY endpoint that students interact with.
    It handles:
    1. Intent classification
    2. Parameter extraction
    3. Tool execution
    4. Response formatting
    """
    logger.info(f"Chat request from user: {request.user_info.name}")
    logger.info(f"Message: {request.message}")
    
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Run orchestration workflow
        result = await orchestrate(
            user_message=request.message,
            user_info=request.user_info,
            chat_history=request.chat_history,
            conversation_id=conversation_id
        )
        
        # Build response
        response = ChatResponse(
            conversation_id=conversation_id,
            message=result.get("final_message", "Processing complete."),
            tool_response=result.get("tool_response"),
            extracted_parameters=result.get("extracted_params"),
            needs_clarification=result.get("needs_clarification", False),
            clarification_question=result.get("clarification_question")
        )
        
        logger.info(f"Chat response prepared for conversation: {conversation_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-tutor-orchestrator",
        "version": "1.0.0"
    }


@router.get("/tools")
async def list_tools() -> Dict[str, Any]:
    """List available educational tools."""
    return {
        "tools": [
            {
                "name": "note_maker",
                "description": "Creates structured study notes with examples and analogies",
                "required_params": ["topic", "subject", "note_taking_style"]
            },
            {
                "name": "flashcard_generator",
                "description": "Generates practice flashcards at various difficulty levels",
                "required_params": ["topic", "count", "difficulty", "subject"]
            },
            {
                "name": "concept_explainer",
                "description": "Explains concepts with examples and practice questions",
                "required_params": ["concept_to_explain", "current_topic", "desired_depth"]
            }
        ]
    }


@router.get("/debug/state/{conversation_id}")
async def get_conversation_state(conversation_id: str) -> Dict[str, Any]:
    """
    Debug endpoint to view conversation state.
    (In production, this would query the database)
    """
    # TODO: Implement database query
    return {
        "conversation_id": conversation_id,
        "message": "State retrieval not yet implemented"
    }
