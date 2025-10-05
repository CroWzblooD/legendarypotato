"""
Parameter Validation Node - Validates extracted parameters against tool schemas.
"""
import logging
from typing import Dict, Any

from agents.validator import validate_parameters
from utils.educational_logger import edu_logger
from graph.utils.state_manager import add_processing_step, add_error

logger = logging.getLogger(__name__)


async def validation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 3: Validate extracted parameters against tool schema.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with validation results
    """
    logger.info("=== Validation Node ===")
    
    # Educational logging
    edu_logger.log_step(
        "✅",
        "STEP 3: Parameter Validation",
        "Validating extracted parameters against tool requirements",
        {
            "Tool Type": state["intent"].value,
            "Agent": "Schema Validator (Pydantic)",
            "Challenge": "Ensure all required parameters are present and correctly formatted"
        }
    )
    
    try:
        extracted_params = state["extracted_params"]
        
        # Show what we're validating
        print(f"\n   📋 Validating parameters for {state['intent'].value}:")
        for param_name, param_value in extracted_params.parameters.items():
            print(f"      • {param_name} = '{param_value}'")
        
        # Validate using Pydantic schemas
        is_valid, tool_input, missing = await validate_parameters(
            tool_type=extracted_params.tool_type,
            parameters=extracted_params.parameters,
            user_info=state["user_info"],
            chat_history=state["chat_history"]
        )
        
        # Update state
        state["validation_passed"] = is_valid
        state["tool_input"] = tool_input
        
        if is_valid:
            add_processing_step(state, "Validation passed")
            logger.info("Validation successful")
            
            # Educational logging - success
            print(f"\n   ✅ All parameters valid!")
            edu_logger.log_result("Validation passed - ready for tool execution", True)
        else:
            add_processing_step(state, f"Validation failed: missing {missing}")
            logger.warning(f"Validation failed: {missing}")
            
            # Educational logging - missing parameters
            print(f"\n   ⚠️  Missing required parameters:")
            for missing_param in missing:
                print(f"      • {missing_param} (required for {state['intent'].value})")
            
            edu_logger.log_result("Validation failed - need clarification from user", False)
            
            # Update extracted params with missing list
            extracted_params.missing_required = missing
            state["extracted_params"] = extracted_params
        
    except Exception as e:
        logger.error(f"Error in validation: {e}")
        add_error(state, f"Validation error: {str(e)}")
        state["validation_passed"] = False
        
        edu_logger.log_result(f"Validation error: {str(e)}", False)
    
    return state
