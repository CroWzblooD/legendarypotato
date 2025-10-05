"""
Node Persistence - Database operations for workflow nodes.
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class NodePersistence:
    """Helper class for persisting node data to database."""
    
    def __init__(self, db_session: Optional[Any] = None):
        """
        Initialize persistence helper.
        
        Args:
            db_session: Optional database session
        """
        self.db = db_session
        self.enabled = db_session is not None
    
    async def save_user_message(
        self,
        conversation_id: str,
        content: str
    ) -> bool:
        """Save user message to database."""
        if not self.enabled:
            return False
        
        try:
            from database.repositories import MessageRepository
            repo = MessageRepository(self.db)
            await repo.create(
                conversation_id=conversation_id,
                role="user",
                content=content
            )
            logger.info("✅ Saved user message")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving user message: {e}")
            return False
    
    async def save_assistant_message(
        self,
        conversation_id: str,
        content: str,
        tool_used: Optional[str] = None
    ) -> bool:
        """Save assistant message to database."""
        if not self.enabled:
            return False
        
        try:
            from database.repositories import MessageRepository
            repo = MessageRepository(self.db)
            await repo.create(
                conversation_id=conversation_id,
                role="assistant",
                content=content,
                tool_used=tool_used
            )
            logger.info("✅ Saved assistant message")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving assistant message: {e}")
            return False
    
    async def save_parameter_extraction(
        self,
        conversation_id: str,
        user_message: str,
        extracted_params: Dict[str, Any],
        inferred_params: Dict[str, Any],
        confidence_score: float,
        missing_required: list
    ) -> bool:
        """Save parameter extraction (CRITICAL for scoring)."""
        if not self.enabled:
            return False
        
        try:
            from database.repositories import ParameterExtractionRepository
            repo = ParameterExtractionRepository(self.db)
            await repo.create(
                conversation_id=conversation_id,
                user_message=user_message,
                extracted_params=extracted_params,
                inferred_params=inferred_params or {},
                confidence_score=confidence_score,
                missing_required=missing_required or []
            )
            logger.info(f"✅ Saved parameter extraction (confidence: {confidence_score:.0%})")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving parameter extraction: {e}")
            return False
    
    async def save_tool_execution(
        self,
        conversation_id: str,
        tool_type: str,
        input_params: Dict[str, Any],
        output_data: Optional[Dict[str, Any]],
        execution_time_ms: int,
        success: bool,
        error_message: Optional[str] = None
    ) -> bool:
        """Save tool execution record."""
        if not self.enabled:
            return False
        
        try:
            from database.repositories import ToolExecutionRepository
            repo = ToolExecutionRepository(self.db)
            await repo.create(
                conversation_id=conversation_id,
                tool_type=tool_type,
                input_params=input_params,
                output_data=output_data if success else None,
                execution_time_ms=execution_time_ms,
                success=success,
                error_message=error_message if not success else None
            )
            logger.info(f"✅ Saved tool execution ({execution_time_ms}ms)")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving tool execution: {e}")
            return False
    
    async def increment_message_count(
        self,
        conversation_id: str,
        count: int = 1
    ) -> bool:
        """Increment conversation message count."""
        if not self.enabled:
            return False
        
        try:
            from database.repositories import ConversationRepository
            repo = ConversationRepository(self.db)
            for _ in range(count):
                await repo.increment_message_count(conversation_id)
            return True
        except Exception as e:
            logger.error(f"❌ Error incrementing message count: {e}")
            return False
