"""
Orchestrator - Main entry point for AI workflow execution.
"""
import logging
from typing import Dict, Any, List, Optional

from models.schemas import UserInfo
from utils.educational_logger import edu_logger
from graph.workflow import create_orchestrator_graph
from graph.utils import create_initial_state

logger = logging.getLogger(__name__)


async def orchestrate(
    user_message: str,
    user_info: UserInfo,
    chat_history: List[Dict[str, str]],
    conversation_id: str,
    db_session: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Main orchestration function - executes the LangGraph workflow.
    
    Args:
        user_message: User's current message
        user_info: Student profile
        chat_history: Previous conversation
        conversation_id: Unique conversation ID
        db_session: Optional database session for persistence
        
    Returns:
        Final state dict with all processing results
    """
    logger.info(f"🚀 Starting orchestration for conversation: {conversation_id}")
    
    # Educational logging - Workflow Start
    _log_workflow_start(user_message, conversation_id)
    
    # Initialize state
    initial_state = create_initial_state(
        user_message=user_message,
        user_info=user_info,
        chat_history=chat_history,
        conversation_id=conversation_id,
        db_session=db_session
    )
    
    # Create and run graph
    app = create_orchestrator_graph()
    
    try:
        # Execute workflow
        final_state = await app.ainvoke(initial_state)
        
        logger.info("✅ Orchestration completed successfully")
        logger.info(f"Processing steps: {final_state['processing_steps']}")
        
        # Educational logging - Workflow Summary
        _log_workflow_summary(final_state)
        
        return final_state
        
    except Exception as e:
        logger.error(f"❌ Error in orchestration: {e}")
        edu_logger.log_result(f"Orchestration error: {str(e)}", False)
        
        return {
            **initial_state,
            "errors": [str(e)],
            "final_message": "An error occurred during processing. Please try again."
        }


def _log_workflow_start(user_message: str, conversation_id: str) -> None:
    """Log workflow start with educational output."""
    print("\n" + "="*80)
    edu_logger.log_step(
        "🚀",
        "AI ORCHESTRATION WORKFLOW STARTED",
        "LangGraph workflow processing student request",
        {
            "Architecture": "LangGraph StateGraph with 5 nodes",
            "AI Model": "Google Gemini 2.5 Flash",
            "Database": "PostgreSQL (Supabase)",
            "Conversation ID": conversation_id[:8] + "..."
        }
    )
    print(f"\n   💬 Student Question: \"{user_message}\"")
    print(f"\n    Processing Pipeline:")
    print(f"      Step 1: Intent Classification (Gemini AI)")
    print(f"      Step 2: Parameter Extraction (Gemini AI)")
    print(f"      Step 3: Parameter Validation (Pydantic)")
    print(f"      Step 4: Tool Execution / Clarification")
    print(f"      Step 5: Response Generation")
    print("="*80 + "\n")


def _log_workflow_summary(final_state: Dict[str, Any]) -> None:
    """Log workflow completion summary."""
    print("\n" + "="*80)
    edu_logger.log_step(
        "🎉",
        "WORKFLOW COMPLETE",
        "AI Orchestration finished successfully",
        {
            "Total Steps": len(final_state['processing_steps']),
            "Intent": final_state.get('intent', 'N/A').value if final_state.get('intent') else 'N/A',
            "Status": "✅ Success" if not final_state.get('needs_clarification') else "❓ Needs Clarification",
            "Database": "All operations persisted to PostgreSQL"
        }
    )
    
    if not final_state.get('needs_clarification'):
        _log_execution_summary(final_state)
    
    print("="*80 + "\n")


def _log_execution_summary(final_state: Dict[str, Any]) -> None:
    """Log execution summary details."""
    print(f"\n   📊 Workflow Summary:")
    print(f"      1. Intent Classification → {final_state.get('intent', 'N/A').value if final_state.get('intent') else 'N/A'}")
    
    # Get parameter count safely
    extracted_params = final_state.get('extracted_params')
    param_count = 0
    if extracted_params:
        if hasattr(extracted_params, 'parameters'):
            param_count = len(extracted_params.parameters)
        elif isinstance(extracted_params, dict):
            param_count = len(extracted_params.get('parameters', {}))
    
    print(f"      2. Parameter Extraction → {param_count} parameters")
    print(f"      3. Validation → {'Passed' if final_state.get('validation_passed') else 'Failed'}")
    
    # Get tool execution status safely
    tool_response = final_state.get('tool_response')
    tool_success = False
    if tool_response:
        if hasattr(tool_response, 'success'):
            tool_success = tool_response.success
        elif isinstance(tool_response, dict):
            tool_success = tool_response.get('success', False)
    
    print(f"      4. Tool Execution → {'Success' if tool_success else 'Failed'}")
    
    # Show database tables updated
    print(f"\n   💾 Database Updates:")
    print(f"      • users (profile information)")
    print(f"      • conversations (conversation metadata)")
    print(f"      • chat_messages (2 messages: user + assistant)")
    print(f"      • parameter_extractions (extraction record)")
    print(f"      • tool_executions (execution record)")
