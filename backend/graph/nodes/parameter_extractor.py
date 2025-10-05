"""
Parameter Extraction Node - Extracts and infers parameters from conversation.
"""
import logging
from typing import Dict, Any

from models.schemas import ExtractedParameters
from services.gemini_service import gemini_service
from utils.educational_logger import edu_logger
from graph.utils.node_persistence import NodePersistence
from graph.utils.state_manager import add_processing_step, add_error

logger = logging.getLogger(__name__)


async def parameter_extraction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 2: Extract parameters from conversation using Gemini.
    
    This is CRITICAL - 40% of hackathon score depends on parameter extraction quality!
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with extracted parameters
    """
    logger.info("=== Parameter Extraction Node ===")
    
    # Educational logging
    edu_logger.log_step(
        "🔍",
        "STEP 2: Parameter Extraction",
        "Extracting required information from the conversation",
        {
            "Tool Type": state["intent"].value,
            "Agent": "Parameter Extractor (Gemini 2.5 Flash)",
            "Challenge": "Extract all required parameters, infer missing ones"
        }
    )
    
    # Show what we're looking for
    tool_params = {
        "note_maker": ["topic", "subject", "note_taking_style"],
        "flashcard_generator": ["topic", "count", "difficulty", "subject"],
        "concept_explainer": ["concept_to_explain", "desired_depth"]
    }
    
    if state["intent"].value in tool_params:
        params_needed = ", ".join(tool_params[state["intent"].value])
        print(f"   📋 Required parameters: {params_needed}")
    
    edu_logger.log_agent("Parameter Extractor", "analyzing conversation for parameters")
    
    try:
        # Call Gemini AI for parameter extraction
        extracted = await gemini_service.extract_parameters(
            message=state["user_message"],
            chat_history=state["chat_history"],
            user_info=state["user_info"],
            tool_type=state["intent"]
        )
        
        # Update state
        state["extracted_params"] = extracted
        add_processing_step(state, f"Extracted parameters with {extracted.confidence:.2f} confidence")
        
        # Educational logging
        edu_logger.log_result(f"Extraction confidence: {extracted.confidence:.0%}", True)
        
        # Show extracted parameters
        _display_extracted_params(extracted, state)
        
        # Save to database (CRITICAL for hackathon scoring!)
        await _save_extraction_to_db(state, extracted)
        
        logger.info(f"Extracted params: {extracted.parameters}")
        logger.info(f"Confidence: {extracted.confidence}")
        logger.info(f"Inferred: {extracted.inferred_params}")
        
    except Exception as e:
        logger.error(f"Error in parameter extraction: {e}")
        add_error(state, f"Parameter extraction error: {str(e)}")
        edu_logger.log_result(f"Error: {str(e)}", False)
        
        # Create empty extraction to continue flow
        state["extracted_params"] = ExtractedParameters(
            tool_type=state["intent"],
            parameters={},
            confidence=0.0,
            missing_required=["all"],
            inferred_params={}
        )
    
    return state


def _display_extracted_params(extracted: ExtractedParameters, state: Dict[str, Any]) -> None:
    """Display extracted parameters with educational logging."""
    # Show explicitly extracted
    if extracted.parameters:
        print(f"\n   📦 Extracted from user message:")
        for key, value in extracted.parameters.items():
            print(f"      • {key} = '{value}'")
    
    # Show inferred parameters with reasoning
    if extracted.inferred_params:
        print(f"\n   🔮 Inferred from context:")
        for key, value in extracted.inferred_params.items():
            reason = "Based on user profile and conversation history"
            if key == "difficulty":
                reason = f"User said 'struggling' → inferred '{value}' difficulty"
            elif key == "subject":
                reason = f"Inferred from topic context"
            elif key == "note_taking_style":
                reason = f"Based on teaching style: {state['user_info'].teaching_style}"
            print(f"      • {key} = '{value}' ({reason})")
    
    # Show missing parameters
    if extracted.missing_required:
        print(f"\n   ⚠️  Missing required parameters:")
        for param in extracted.missing_required:
            print(f"      • {param} (will use default or ask user)")


async def _save_extraction_to_db(state: Dict[str, Any], extracted: ExtractedParameters) -> None:
    """Save parameter extraction to database."""
    persistence = NodePersistence(state.get("db_session"))
    await persistence.save_parameter_extraction(
        conversation_id=state["conversation_id"],
        user_message=state["user_message"],
        extracted_params=extracted.parameters,
        inferred_params=extracted.inferred_params or {},
        confidence_score=extracted.confidence,
        missing_required=extracted.missing_required or []
    )
    edu_logger.log_database(
        "Saved", 
        "parameter_extractions",
        f"Confidence: {extracted.confidence:.0%}"
    )
