"""
Message Repository - Data access layer for chat_messages table.
"""
import logging
from typing import List
from uuid import UUID
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import ChatMessage

logger = logging.getLogger(__name__)


class MessageRepository:
    """Repository for ChatMessage operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        conversation_id: str,
        role: str,
        content: str,
        tool_used: str = None
    ) -> ChatMessage:
        """Create a new chat message."""
        message = ChatMessage(
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            role=role,
            content=content,
            tool_used=tool_used
        )
        
        self.session.add(message)
        await self.session.flush()
        
        logger.info(f"Created message: {message.message_id} (role={role}, conv={conversation_id})")
        return message
    
    async def get_by_conversation(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[ChatMessage]:
        """
        Get messages for a conversation, ordered by timestamp.
        Returns most recent messages first.
        """
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.conversation_id == uuid_id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(limit)
        )
        
        # Reverse to get chronological order (oldest first)
        messages = list(result.scalars().all())
        return list(reversed(messages))
    
    async def get_recent_messages(
        self,
        conversation_id: str,
        count: int = 10
    ) -> List[ChatMessage]:
        """Get the N most recent messages from a conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.conversation_id == uuid_id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(count)
        )
        
        # Reverse to get chronological order
        messages = list(result.scalars().all())
        return list(reversed(messages))
    
    async def count_by_conversation(self, conversation_id: str) -> int:
        """Count total messages in a conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(func.count(ChatMessage.message_id))
            .where(ChatMessage.conversation_id == uuid_id)
        )
        return result.scalar_one()
    
    async def delete_by_conversation(self, conversation_id: str):
        """Delete all messages in a conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        await self.session.execute(
            delete(ChatMessage).where(ChatMessage.conversation_id == uuid_id)
        )
        await self.session.flush()
        logger.info(f"Deleted all messages for conversation: {conversation_id}")
