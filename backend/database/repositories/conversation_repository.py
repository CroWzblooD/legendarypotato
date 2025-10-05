"""
Conversation Repository - Data access layer for conversations table.
"""
import logging
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models import Conversation

logger = logging.getLogger(__name__)


class ConversationRepository:
    """Repository for Conversation operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        conversation_id: str,
        user_id: str,
        status: str = "active"
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            user_id=UUID(user_id) if isinstance(user_id, str) else user_id,
            status=status
        )
        
        self.session.add(conversation)
        await self.session.flush()
        
        logger.info(f"Created conversation: {conversation.conversation_id}")
        return conversation
    
    async def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(Conversation).where(Conversation.conversation_id == uuid_id)
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
    
    async def get_with_messages(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation with all messages loaded."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.conversation_id == uuid_id)
            .options(selectinload(Conversation.messages))
        )
        return result.scalar_one_or_none()
    
    async def get_by_user(self, user_id: str, limit: int = 10) -> List[Conversation]:
        """Get recent conversations for a user."""
        uuid_id = UUID(user_id) if isinstance(user_id, str) else user_id
        
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.user_id == uuid_id)
            .order_by(Conversation.last_message_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def increment_message_count(self, conversation_id: str):
        """Increment message count for conversation."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        await self.session.execute(
            update(Conversation)
            .where(Conversation.conversation_id == uuid_id)
            .values(
                message_count=Conversation.message_count + 1,
                last_message_at=func.now()
            )
        )
        await self.session.flush()
    
    async def update_status(self, conversation_id: str, status: str):
        """Update conversation status."""
        uuid_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        
        await self.session.execute(
            update(Conversation)
            .where(Conversation.conversation_id == uuid_id)
            .values(status=status)
        )
        await self.session.flush()
        logger.info(f"Updated conversation {conversation_id} status to {status}")
