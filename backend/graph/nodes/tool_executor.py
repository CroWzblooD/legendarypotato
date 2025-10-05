"""
Tool Executor Node - Executes the educational tool with validated parameters.
"""
import logging
import time
from typing import Dict, Any

from models.schemas import ToolType, ToolResponse
from agents.tool_executor import execute_tool
from utils.educational_logger import edu_logger
from graph.utils.node_persistence import NodePersistence
from graph.utils.state_manager import add_processing_step, add_error, serialize_tool_input

logger = logging.getLogger(__name__)


# Tool metadata
TOOL_NAMES = {
    ToolType.NOTE_MAKER: "Note Maker",
    ToolType.FLASHCARD_GENERATOR: "Flashcard Generator",
    ToolType.CONCEPT_EXPLAINER: "Concept Explainer"
}

TOOL_ENDPOINTS = {
    ToolType.NOTE_MAKER: "http://localhost:8001/api/note-maker",
    ToolType.FLASHCARD_GENERATOR: "http://localhost:8001/api/flashcard-generator",
    ToolType.CONCEPT_EXPLAINER: "http://localhost:8001/api/explainer"
}


async def tool_execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 4a: Execute the educational tool with validated parameters.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with tool execution results
    """
    logger.info("=== Tool Execution Node ===")
    
    start_time = time.time()
    
    # Educational logging
    _log_execution_start(state)
    
    try:
        # Execute tool via HTTP API
        tool_response = await execute_tool(
            tool_type=state["intent"],
            tool_input=state["tool_input"]
        )
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Update state
        state["tool_response"] = tool_response
        add_processing_step(state, f"Tool executed: {tool_response.success}")
        
        if tool_response.success:
            state["final_message"] = "Tool executed successfully. Here are your results:"
            logger.info("Tool execution successful")
            
            # Educational logging - success
            _log_execution_success(state, tool_response, execution_time_ms)
        else:
            state["final_message"] = f"Tool execution failed: {tool_response.error}"
            add_error(state, f"Tool execution failed: {tool_response.error}")
            logger.error(f"Tool failed: {tool_response.error}")
            
            edu_logger.log_result(f"Tool execution failed: {tool_response.error}", False)
        
        # Save to database
        await _save_execution_to_db(state, tool_response, execution_time_ms)
        
    except Exception as e:
        logger.error(f"Error in tool execution: {e}")
        add_error(state, f"Tool execution error: {str(e)}")
        
        state["tool_response"] = ToolResponse(
            tool_type=state["intent"],
            success=False,
            error=str(e)
        )
        state["final_message"] = f"An error occurred: {str(e)}"
        
        edu_logger.log_result(f"Tool execution error: {str(e)}", False)
    
    return state


def _log_execution_start(state: Dict[str, Any]) -> None:
    """Log execution start with educational output."""
    tool_name = TOOL_NAMES.get(state["intent"], "Unknown")
    tool_endpoint = TOOL_ENDPOINTS.get(state["intent"], "Unknown")
    
    edu_logger.log_step(
        "🔧",
        "STEP 4: Tool Execution",
        "Calling educational tool API with validated parameters",
        {
            "Tool": tool_name,
            "API Endpoint": tool_endpoint,
            "Method": "POST (REST API)",
            "Processing": "AI-powered content generation"
        }
    )
    
    # Show parameters being sent
    print(f"\n   📤 Sending to {tool_name}:")
    params = serialize_tool_input(state["tool_input"])
    for key, value in params.items():
        print(f"      • {key} = '{value}'")
    
    print(f"\n   ⏳ Waiting for AI to generate content...")


def _log_execution_success(
    state: Dict[str, Any],
    tool_response: ToolResponse,
    execution_time_ms: int
) -> None:
    """Log successful execution with results summary."""
    print(f"\n   ✅ Tool execution successful!")
    print(f"   ⏱️  Execution time: {execution_time_ms}ms ({execution_time_ms/1000:.1f}s)")
    
    # Show what was generated
    if tool_response.data:
        if state["intent"] == ToolType.FLASHCARD_GENERATOR:
            flashcards = tool_response.data.get('flashcards', [])
            print(f"   📚 Generated {len(flashcards)} flashcards")
        elif state["intent"] == ToolType.NOTE_MAKER:
            notes = tool_response.data.get('notes', {})
            sections = len(notes.get('sections', []))
            print(f"   📝 Generated structured notes with {sections} sections")
        elif state["intent"] == ToolType.CONCEPT_EXPLAINER:
            explanation = tool_response.data.get('explanation', '')
            print(f"   💡 Generated detailed explanation ({len(explanation)} characters)")
    
    edu_logger.log_result(f"AI content generated successfully in {execution_time_ms}ms", True)


async def _save_execution_to_db(
    state: Dict[str, Any],
    tool_response: ToolResponse,
    execution_time_ms: int
) -> None:
    """Save tool execution and assistant response to database."""
    persistence = NodePersistence(state.get("db_session"))
    
    # Serialize tool input
    input_params = serialize_tool_input(state["tool_input"])
    
    # Save tool execution record
    await persistence.save_tool_execution(
        conversation_id=state["conversation_id"],
        tool_type=state["intent"].value,
        input_params=input_params,
        output_data=tool_response.data if tool_response.success else None,
        execution_time_ms=execution_time_ms,
        success=tool_response.success,
        error_message=tool_response.error if not tool_response.success else None
    )
    
    # Save assistant response
    await persistence.save_assistant_message(
        conversation_id=state["conversation_id"],
        content=state["final_message"],
        tool_used=state["intent"].value
    )
    
    # Increment message count (user + assistant)
    await persistence.increment_message_count(
        conversation_id=state["conversation_id"],
        count=2
    )
    
    logger.info(f"Tool execution saved to database (execution time: {execution_time_ms}ms)")
    
    # Educational logging
    edu_logger.log_database("Saved", "tool_executions", f"Execution time: {execution_time_ms}ms, Success: {tool_response.success}")
    edu_logger.log_database("Saved", "chat_messages", "Assistant response with tool results")
