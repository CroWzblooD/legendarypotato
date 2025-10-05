"""
Intent Classification Node - Determines which educational tool to use.
"""
import logging
from typing import Dict, Any

from models.schemas import ToolType
from services.gemini_service import gemini_service
from utils.educational_logger import edu_logger
from graph.utils.node_persistence import NodePersistence
from graph.utils.state_manager import add_processing_step, add_error

logger = logging.getLogger(__name__)


async def intent_classification_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 1: Classify user intent to determine which tool to use.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with intent classification
    """
    logger.info("=== Intent Classification Node ===")
    
    # Educational logging
    edu_logger.log_step(
        "🎯", 
        "STEP 1: Intent Classification",
        "Using Gemini AI to understand what the student needs",
        {
            "Input": state["user_message"][:60] + "..." if len(state["user_message"]) > 60 else state["user_message"],
            "Agent": "Intent Classifier (Gemini 2.5 Flash)",
            "Purpose": "Determine which educational tool to use"
        }
    )
    
    edu_logger.log_agent("Intent Classifier", "analyzing student's request")
    
    try:
        # Call Gemini AI for intent classification
        tool_type = await gemini_service.classify_intent(
            message=state["user_message"],
            chat_history=state["chat_history"],
            user_info=state["user_info"]
        )
        
        # Update state
        state["intent"] = tool_type
        add_processing_step(state, f"Intent classified as: {tool_type.value}")
        
        # Educational logging
        edu_logger.log_result(f"Intent: {tool_type.value}", True)
        
        # Show tool description
        tool_descriptions = {
            "note_maker": "Creates structured study notes with sections and key points",
            "flashcard_generator": "Generates Q&A flashcards for practice and memorization",
            "concept_explainer": "Provides detailed explanations with examples and analogies"
        }
        if tool_type.value in tool_descriptions:
            print(f"   💡 {tool_descriptions[tool_type.value]}")
        
        # Save user message to database
        persistence = NodePersistence(state.get("db_session"))
        await persistence.save_user_message(
            conversation_id=state["conversation_id"],
            content=state["user_message"]
        )
        edu_logger.log_database("Saved", "chat_messages", "User question stored")
        
    except Exception as e:
        logger.error(f"Error in intent classification: {e}")
        add_error(state, f"Intent classification error: {str(e)}")
        state["intent"] = ToolType.CONCEPT_EXPLAINER  # Safe default
        edu_logger.log_result(f"Error: {str(e)}", False)
    
    return state
