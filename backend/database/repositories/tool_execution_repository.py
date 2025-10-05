"""
Tool Execution Repository - Data access layer for tool_executions table.
"""
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ToolExecution

logger = logging.getLogger(__name__)


class ToolExecutionRepository:
    """Repository for ToolExecution operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
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
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            tool_type=tool_type,
            input_params=input_params,
            output_data=output_data,
            execution_time_ms=execution_time_ms,
            success=success,
            error_message=error_message
        )
        
        self.session.add(execution)
        await self.session.flush()
        
        logger.info(f"Logged tool execution: {tool_type} (success={success}, time={execution_time_ms}ms)")
        return execution
    
    async def get_by_conversation(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[ToolExecution]:
        """Get tool executions for a conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(ToolExecution)
            .where(ToolExecution.conversation_id == uuid_id)
            .order_by(ToolExecution.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_tool_type(
        self,
        tool_type: str,
        limit: int = 100
    ) -> List[ToolExecution]:
        """Get recent executions for a specific tool type."""
        result = await self.session.execute(
            select(ToolExecution)
            .where(ToolExecution.tool_type == tool_type)
            .order_by(ToolExecution.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_success_rate(self, tool_type: Optional[str] = None) -> float:
        """Calculate success rate for tool executions."""
        query = select(
            func.count(ToolExecution.execution_id).label("total"),
            func.sum(func.cast(ToolExecution.success, Integer)).label("successful")
        )
        
        if tool_type:
            query = query.where(ToolExecution.tool_type == tool_type)
        
        result = await self.session.execute(query)
        row = result.one()
        
        if row.total == 0:
            return 0.0
        
        return (row.successful / row.total) * 100
    
    async def get_average_execution_time(self, tool_type: Optional[str] = None) -> float:
        """Calculate average execution time in milliseconds."""
        query = select(func.avg(ToolExecution.execution_time_ms))
        
        if tool_type:
            query = query.where(ToolExecution.tool_type == tool_type)
        
        result = await self.session.execute(query)
        avg_time = result.scalar_one_or_none()
        
        return avg_time if avg_time else 0.0
