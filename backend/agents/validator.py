"""
Validator agent for parameter validation against tool schemas.
"""
import logging
from typing import Tuple, Optional, Dict, Any, List

from models.schemas import (
    ToolType,
    UserInfo,
    ChatMessage,
    NoteMakerInput,
    FlashcardGeneratorInput,
    ConceptExplainerInput
)

logger = logging.getLogger(__name__)


async def validate_parameters(
    tool_type: ToolType,
    parameters: Dict[str, Any],
    user_info: UserInfo,
    chat_history: List[ChatMessage]
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """
    Validate extracted parameters against tool schema using Pydantic.
    
    Args:
        tool_type: Which tool we're validating for
        parameters: Extracted parameters dict
        user_info: Student profile
        chat_history: Conversation history
        
    Returns:
        Tuple of (is_valid, tool_input_dict, missing_params)
    """
    logger.info(f"Validating parameters for {tool_type.value}")
    
    try:
        if tool_type == ToolType.NOTE_MAKER:
            return await _validate_note_maker(parameters, user_info, chat_history)
        elif tool_type == ToolType.FLASHCARD_GENERATOR:
            return await _validate_flashcard(parameters, user_info)
        else:  # CONCEPT_EXPLAINER
            return await _validate_concept_explainer(parameters, user_info, chat_history)
            
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False, None, ["validation_error"]


async def _validate_note_maker(
    params: Dict[str, Any],
    user_info: UserInfo,
    chat_history: List[ChatMessage]
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Validate Note Maker parameters."""
    
    required = ["topic", "subject", "note_taking_style"]
    missing = [field for field in required if not params.get(field)]
    
    if missing:
        logger.warning(f"Note Maker missing required params: {missing}")
        return False, None, missing
    
    try:
        # Build tool input
        tool_input = NoteMakerInput(
            user_info=user_info,
            chat_history=chat_history,
            topic=params["topic"],
            subject=params["subject"],
            note_taking_style=params["note_taking_style"],
            include_examples=params.get("include_examples", True),
            include_analogies=params.get("include_analogies", False)
        )
        
        logger.info("Note Maker validation passed")
        return True, tool_input.model_dump(), []
        
    except Exception as e:
        logger.error(f"Note Maker validation failed: {e}")
        return False, None, ["validation_failed"]


async def _validate_flashcard(
    params: Dict[str, Any],
    user_info: UserInfo
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Validate Flashcard Generator parameters."""
    
    required = ["topic", "count", "difficulty", "subject"]
    missing = [field for field in required if not params.get(field)]
    
    if missing:
        logger.warning(f"Flashcard missing required params: {missing}")
        return False, None, missing
    
    try:
        # Validate count range
        count = params["count"]
        if not isinstance(count, int) or not (1 <= count <= 20):
            logger.error(f"Invalid count: {count}")
            return False, None, ["count"]
        
        # Build tool input
        tool_input = FlashcardGeneratorInput(
            user_info=user_info,
            topic=params["topic"],
            count=count,
            difficulty=params["difficulty"],
            subject=params["subject"],
            include_examples=params.get("include_examples", True)
        )
        
        logger.info("Flashcard validation passed")
        return True, tool_input.model_dump(), []
        
    except Exception as e:
        logger.error(f"Flashcard validation failed: {e}")
        return False, None, ["validation_failed"]


async def _validate_concept_explainer(
    params: Dict[str, Any],
    user_info: UserInfo,
    chat_history: List[ChatMessage]
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Validate Concept Explainer parameters."""
    
    required = ["concept_to_explain", "current_topic", "desired_depth"]
    missing = [field for field in required if not params.get(field)]
    
    if missing:
        logger.warning(f"Concept Explainer missing required params: {missing}")
        return False, None, missing
    
    try:
        # Build tool input
        tool_input = ConceptExplainerInput(
            user_info=user_info,
            chat_history=chat_history,
            concept_to_explain=params["concept_to_explain"],
            current_topic=params["current_topic"],
            desired_depth=params["desired_depth"]
        )
        
        logger.info("Concept Explainer validation passed")
        return True, tool_input.model_dump(), []
        
    except Exception as e:
        logger.error(f"Concept Explainer validation failed: {e}")
        return False, None, ["validation_failed"]
