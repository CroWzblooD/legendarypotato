"""
User Repository - Data access layer for users table.
"""
import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):
    """Repository for User operations."""
    
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
            user_id=self.to_uuid(user_id),
            name=name,
            grade_level=grade_level,
            learning_style_summary=learning_style_summary,
            emotional_state_summary=emotional_state_summary,
            mastery_level_summary=mastery_level_summary,
            teaching_style=teaching_style
        )
        
        await self._add_and_flush(user)
        logger.info(f"Created user: {user.user_id}")
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(User).where(User.user_id == self.to_uuid(user_id))
        )
        return result.scalar_one_or_none()
    
    async def update(
        self,
        user_id: str,
        name: str,
        grade_level: str,
        learning_style_summary: str = "",
        emotional_state_summary: str = "",
        mastery_level_summary: str = "",
        teaching_style: str = "direct"
    ) -> User:
        """
        Update existing user with new information.
        Returns updated user.
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.name = name
        user.grade_level = grade_level
        user.learning_style_summary = learning_style_summary
        user.emotional_state_summary = emotional_state_summary
        user.mastery_level_summary = mastery_level_summary
        user.teaching_style = teaching_style
        await self.session.flush()
        return user
    
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
        If user exists, updates their information.
        Returns (user, created) tuple where created=True if new user was created.
        """
        user = await self.get_by_id(user_id)
        
        if user:
            # Update existing user with latest request data
            await self.update(
                user_id=user_id,
                name=name,
                grade_level=grade_level,
                learning_style_summary=learning_style_summary,
                emotional_state_summary=emotional_state_summary,
                mastery_level_summary=mastery_level_summary,
                teaching_style=teaching_style
            )
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
