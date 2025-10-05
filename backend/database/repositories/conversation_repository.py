"""
Conversation Repository - Data access layer for conversations table.
"""
import logging
from typing import Optional
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Conversation
from database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ConversationRepository(BaseRepository[Conversation]):
    """Repository for Conversation operations."""
    
    async def create(
        self,
        conversation_id: str,
        user_id: str
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            conversation_id=self.to_uuid(conversation_id),
            user_id=self.to_uuid(user_id)
        )
        
        await self._add_and_flush(conversation)
        logger.info(f"Created conversation: {conversation.conversation_id}")
        return conversation
    
    async def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        result = await self.session.execute(
            select(Conversation).where(Conversation.conversation_id == self.to_uuid(conversation_id))
        )
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        conversation_id: str,
        user_id: str
    ) -> tuple[Conversation, bool]:
        """
        Get existing conversation or create new one.
        Returns (conversation, created) tuple.
        """
        conversation = await self.get_by_id(conversation_id)
        
        if conversation:
            return conversation, False
        else:
            conversation = await self.create(
                conversation_id=conversation_id,
                user_id=user_id
            )
            return conversation, True
    
    async def increment_message_count(self, conversation_id: str):
        """Increment message count and update last_message_at timestamp."""
        await self.session.execute(
            update(Conversation)
            .where(Conversation.conversation_id == self.to_uuid(conversation_id))
            .values(
                message_count=Conversation.message_count + 1,
                last_message_at=func.now()
            )
        )
        await self.session.flush()
