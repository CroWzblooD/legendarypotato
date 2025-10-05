"""
Tool Execution Repository - Data access layer for tool_executions table.
"""
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ToolExecution
from database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ToolExecutionRepository(BaseRepository[ToolExecution]):
    """Repository for ToolExecution operations."""
    
    async def create(
        self,
        conversation_id: str,
        tool_type: str,
        input_params: Dict[str, Any],
        output_data: Optional[Dict[str, Any]] = None,
        execution_time_ms: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> ToolExecution:
        """Create a new tool execution record."""
        execution = ToolExecution(
            conversation_id=self.to_uuid(conversation_id),
            tool_type=tool_type,
            input_params=input_params,
            output_data=output_data,
            execution_time_ms=execution_time_ms,
            success=success,
            error_message=error_message
        )
        
        await self._add_and_flush(execution)
        logger.info(f"Logged tool execution: {tool_type} (success={success}, time={execution_time_ms}ms)")
        return execution
