"""
Clarification Generator Node - Generates clarification questions for missing parameters.
"""
import logging
from typing import Dict, Any

from services.gemini_service import gemini_service
from utils.educational_logger import edu_logger
from graph.utils.node_persistence import NodePersistence
from graph.utils.state_manager import add_processing_step

logger = logging.getLogger(__name__)


async def clarification_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 4b: Generate clarification question if parameters are missing.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with clarification question
    """
    logger.info("=== Clarification Node ===")
    
    # Educational logging
    edu_logger.log_step(
        "❓",
        "STEP 4 (Alternative): Clarification Request",
        "Asking user for missing information",
        {
            "Trigger": "Missing required parameters",
            "Agent": "Clarification Generator (Gemini 2.5 Flash)",
            "Purpose": "Get missing information from user to complete request"
        }
    )
    
    try:
        extracted_params = state["extracted_params"]
        
        # Show what's missing
        print(f"\n   ⚠️  Need more information from user:")
        for missing_param in extracted_params.missing_required:
            print(f"      • {missing_param}")
        
        print(f"\n   💬 Generating natural clarification question...")
        
        # Generate clarification question using Gemini
        clarification = await gemini_service.generate_clarification_question(
            missing_params=extracted_params.missing_required,
            tool_type=extracted_params.tool_type,
            context=state["user_message"]
        )
        
        # Update state
        state["needs_clarification"] = True
        state["clarification_question"] = clarification
        state["final_message"] = clarification
        add_processing_step(state, "Generated clarification question")
        
        logger.info(f"Clarification: {clarification}")
        
        # Educational logging
        print(f"\n   ❓ Clarification question: \"{clarification}\"")
        edu_logger.log_result("Waiting for user to provide missing information", True)
        
        # Save to database
        await _save_clarification_to_db(state, clarification)
        
    except Exception as e:
        logger.error(f"Error generating clarification: {e}")
        state["clarification_question"] = "Could you provide more details?"
        state["final_message"] = "Could you provide more details?"
    
    return state


async def _save_clarification_to_db(state: Dict[str, Any], clarification: str) -> None:
    """Save clarification message to database."""
    persistence = NodePersistence(state.get("db_session"))
    
    # Save assistant's clarification question
    await persistence.save_assistant_message(
        conversation_id=state["conversation_id"],
        content=clarification
    )
    
    # Increment message count (user + assistant)
    await persistence.increment_message_count(
        conversation_id=state["conversation_id"],
        count=2
    )
    
    logger.info("Clarification question saved to database")
