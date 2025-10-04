"""
Tool executor agent - calls educational tool APIs.
"""
import logging
import time
import httpx
from typing import Dict, Any

from config import settings
from models.schemas import ToolType, ToolResponse

logger = logging.getLogger(__name__)


async def execute_tool(
    tool_type: ToolType,
    tool_input: Dict[str, Any]
) -> ToolResponse:
    """
    Execute educational tool by calling its API endpoint.
    
    Args:
        tool_type: Which tool to execute
        tool_input: Validated input parameters
        
    Returns:
        ToolResponse with results or error
    """
    logger.info(f"Executing tool: {tool_type.value}")
    
    start_time = time.time()
    
    # Map tool type to endpoint
    endpoints = {
        ToolType.NOTE_MAKER: f"{settings.tool_service_url}/api/note-maker",
        ToolType.FLASHCARD_GENERATOR: f"{settings.tool_service_url}/api/flashcard-generator",
        ToolType.CONCEPT_EXPLAINER: f"{settings.tool_service_url}/api/concept-explainer"
    }
    
    endpoint = endpoints.get(tool_type)
    if not endpoint:
        logger.error(f"No endpoint found for tool: {tool_type}")
        return ToolResponse(
            tool_type=tool_type,
            success=False,
            error="Invalid tool type"
        )
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, json=tool_input)
            
            execution_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Tool executed successfully in {execution_time}ms")
                
                return ToolResponse(
                    tool_type=tool_type,
                    success=True,
                    data=data,
                    execution_time_ms=execution_time
                )
            else:
                logger.error(f"Tool returned error: {response.status_code}")
                return ToolResponse(
                    tool_type=tool_type,
                    success=False,
                    error=f"Tool API error: {response.status_code}",
                    execution_time_ms=execution_time
                )
                
    except httpx.TimeoutException:
        logger.error("Tool execution timeout")
        return ToolResponse(
            tool_type=tool_type,
            success=False,
            error="Tool execution timeout"
        )
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return ToolResponse(
            tool_type=tool_type,
            success=False,
            error=str(e)
        )
