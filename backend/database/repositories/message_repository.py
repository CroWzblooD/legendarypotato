"""
Message Repository - Data access layer for chat_messages table.
"""
import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ChatMessage
from database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class MessageRepository(BaseRepository[ChatMessage]):
    """Repository for ChatMessage operations."""
    
    async def create(
        self,
        conversation_id: str,
        role: str,
        content: str,
        tool_used: str = None
    ) -> ChatMessage:
        """Create a new chat message."""
        message = ChatMessage(
            conversation_id=self.to_uuid(conversation_id),
            role=role,
            content=content,
            tool_used=tool_used
        )
        
        await self._add_and_flush(message)
        logger.info(f"Created message: {message.message_id} (role={role}, conv={conversation_id})")
        return message
    
    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        order: str = "asc"
    ) -> List[ChatMessage]:
        """
        Get messages for a conversation with flexible ordering.
        
        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to return
            order: "asc" for chronological (oldest first), "desc" for newest first
            
        Returns:
            List of messages in requested order
        """
        query = (
            select(ChatMessage)
            .where(ChatMessage.conversation_id == self.to_uuid(conversation_id))
            .limit(limit)
        )
        
        if order == "desc":
            query = query.order_by(ChatMessage.timestamp.desc())
        else:
            query = query.order_by(ChatMessage.timestamp.asc())
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_recent_messages(
        self,
        conversation_id: str,
        count: int = 10
    ) -> List[ChatMessage]:
        """
        Get the N most recent messages in chronological order (oldest first).
        Returns up to 'count' messages, ordered by timestamp ascending.
        """
        # Use a subquery to get the N most recent, then order them chronologically
        query = (
            select(ChatMessage)
            .where(ChatMessage.conversation_id == self.to_uuid(conversation_id))
            .order_by(ChatMessage.timestamp.desc())
            .limit(count)
        ).alias("recent")
        
        # Wrap in outer query to re-order chronologically
        final_query = select(query).order_by(query.c.timestamp.asc())
        
        result = await self.session.execute(final_query)
        return list(result.scalars().all())
