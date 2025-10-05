"""
User Repository - Data access layer for users table.
"""
import logging
from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for User operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        user_id: str,
        name: str,
        grade_level: str,
        learning_style_summary: str = "",
        emotional_state_summary: str = "",
        mastery_level_summary: str = "",
        teaching_style: str = "direct"
    ) -> User:
        """Create a new user."""
        user = User(
            user_id=UUID(user_id) if isinstance(user_id, str) else user_id,
            name=name,
            grade_level=grade_level,
            learning_style_summary=learning_style_summary,
            emotional_state_summary=emotional_state_summary,
            mastery_level_summary=mastery_level_summary,
            teaching_style=teaching_style
        )
        
        self.session.add(user)
        await self.session.flush()
        
        logger.info(f"Created user: {user.user_id}")
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        uuid_id = UUID(user_id) if isinstance(user_id, str) else user_id
        
        result = await self.session.execute(
            select(User).where(User.user_id == uuid_id)
        )
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        user_id: str,
        name: str,
        grade_level: str,
        learning_style_summary: str = "",
        emotional_state_summary: str = "",
        mastery_level_summary: str = "",
        teaching_style: str = "direct"
    ) -> tuple[User, bool]:
        """
        Get existing user or create new one.
        Returns (user, created) tuple.
        """
        user = await self.get_by_id(user_id)
        
        if user:
            # Update user info
            user.name = name
            user.grade_level = grade_level
            user.learning_style_summary = learning_style_summary
            user.emotional_state_summary = emotional_state_summary
            user.mastery_level_summary = mastery_level_summary
            user.teaching_style = teaching_style
            await self.session.flush()
            return user, False
        else:
            user = await self.create(
                user_id=user_id,
                name=name,
                grade_level=grade_level,
                learning_style_summary=learning_style_summary,
                emotional_state_summary=emotional_state_summary,
                mastery_level_summary=mastery_level_summary,
                teaching_style=teaching_style
            )
            return user, True
    
    async def update(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user fields."""
        user = await self.get_by_id(user_id)
        
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        await self.session.flush()
        logger.info(f"Updated user: {user_id}")
        return user
