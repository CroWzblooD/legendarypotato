"""
LangGraph Workflow - Graph construction and routing logic.

This file defines the workflow structure (nodes and edges) but delegates
actual processing to modular node handlers in graph/nodes/.
"""
import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END

from graph.nodes import (
    intent_classification_node,
    parameter_extraction_node,
    validation_node,
    clarification_node,
    tool_executor_node
)

logger = logging.getLogger(__name__)


# ============================================================================
# ROUTING LOGIC
# ============================================================================

def should_clarify(state: Dict[str, Any]) -> str:
    """
    Routing function: decide if we need clarification or can execute tool.
    
    Args:
        state: Current workflow state
        
    Returns:
        'execute' if validation passed, 'clarify' if validation failed
    """
    if state["validation_passed"]:
        return "execute"
    else:
        return "clarify"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_orchestrator_graph() -> StateGraph:
    """
    Create the LangGraph workflow for orchestration.
    
    Flow:
    1. Classify intent (which tool?)
    2. Extract parameters (from conversation)
    3. Validate parameters (Pydantic schemas)
    4. Branch:
       - If valid → Execute tool
       - If invalid → Ask for clarification
       
    Returns:
        Compiled LangGraph application
    """
    logger.info("Creating orchestrator graph")
    
    # Create graph
    workflow = StateGraph(dict)
    
    # Add nodes (imported from graph/nodes/)
    workflow.add_node("classify_intent", intent_classification_node)
    workflow.add_node("extract_parameters", parameter_extraction_node)
    workflow.add_node("validate", validation_node)
    workflow.add_node("clarify", clarification_node)
    workflow.add_node("execute_tool", tool_executor_node)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("classify_intent")
    workflow.add_edge("classify_intent", "extract_parameters")
    workflow.add_edge("extract_parameters", "validate")
    
    # Conditional routing after validation
    workflow.add_conditional_edges(
        "validate",
        should_clarify,
        {
            "execute": "execute_tool",
            "clarify": "clarify"
        }
    )
    
    # End nodes
    workflow.add_edge("execute_tool", END)
    workflow.add_edge("clarify", END)
    
    # Compile graph
    app = workflow.compile()
    
    logger.info("✅ Orchestrator graph created successfully")
    return app


# Export
__all__ = ["create_orchestrator_graph", "should_clarify"]
