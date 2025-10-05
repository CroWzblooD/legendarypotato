"""
State Manager - Creates and manages orchestrator state.
"""
from typing import Dict, Any, Optional, List
from models.schemas import UserInfo


def create_initial_state(
    user_message: str,
    user_info: UserInfo,
    chat_history: List[Dict[str, str]],
    conversation_id: str,
    db_session: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Create initial state for LangGraph workflow.
    
    Args:
        user_message: Student's message
        user_info: Student profile
        chat_history: Conversation history
        conversation_id: Conversation ID
        db_session: Optional database session
        
    Returns:
        Initial state dictionary
    """
    return {
        # Input
        "user_message": user_message,
        "user_info": user_info,
        "chat_history": chat_history,
        "conversation_id": conversation_id,
        "db_session": db_session,
        
        # Workflow state
        "intent": None,
        "extracted_params": None,
        "validation_passed": False,
        "tool_input": None,
        "tool_response": None,
        
        # Output
        "final_message": None,
        "needs_clarification": False,
        "clarification_question": None,
        
        # Metadata
        "processing_steps": [],
        "errors": []
    }


def add_processing_step(state: Dict[str, Any], step: str) -> None:
    """
    Add a processing step to state.
    
    Args:
        state: Current state
        step: Step description
    """
    state["processing_steps"].append(step)


def add_error(state: Dict[str, Any], error: str) -> None:
    """
    Add an error to state.
    
    Args:
        state: Current state
        error: Error description
    """
    state["errors"].append(error)


def serialize_tool_input(tool_input: Any) -> Dict[str, Any]:
    """
    Serialize tool input to dictionary.
    
    Handles Pydantic models (v1 and v2) and dicts.
    
    Args:
        tool_input: Tool input object
        
    Returns:
        Dictionary representation
    """
    if not tool_input:
        return {}
    
    # Pydantic v2
    if hasattr(tool_input, 'model_dump'):
        return tool_input.model_dump()
    
    # Pydantic v1
    if hasattr(tool_input, 'dict'):
        return tool_input.dict()
    
    # Already a dict
    if isinstance(tool_input, dict):
        return tool_input
    
    return {}
